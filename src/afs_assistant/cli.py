"""Command-line entry point: `uv run afs-assist ...`."""

from __future__ import annotations

import argparse
import sys


def _kb_build(_: argparse.Namespace) -> int:
    from afs_assistant import graph, kb, kb_build

    if not kb_build.paths.MATERIALS.exists():
        print("resources/materials/ not found: unzip the organizer materials.zip into resources/ first.")
        return 2
    counts = kb_build.build_all()
    for cache in (kb.pages, kb.rules, kb.fibers, kb.table1):
        cache.cache_clear()
    g = graph.build()
    graph.save(g)
    print(f"pages: {counts}")
    print(f"graph: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
    return 0


def _kb_check(_: argparse.Namespace) -> int:
    from afs_assistant import kb_check

    findings = kb_check.run()
    for f in findings:
        print(f"[{'PASS' if f.ok else 'FAIL'}] {f.check}: {f.detail}")
    return 0 if all(f.ok for f in findings) else 1


def _scenarios_build(_: argparse.Namespace) -> int:
    from afs_assistant import scenarios

    print(scenarios.build())
    return 0


def _assess_one(enquiry: str, scenario_id: str | None, client, out_dir=None, title: str = "",
                external: str = "off") -> dict:
    import json
    from datetime import UTC, datetime

    from afs_assistant import pipeline, provenance, render

    # Unique per run so provenance tags are never overwritten; output files keep the scenario id.
    run_id = f"{scenario_id or 'adhoc'}-{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
    result = pipeline.run(enquiry, client, run_id=run_id, external=external)
    result.manifest["code_sha"] = provenance.code_sha()
    result.manifest["code_dirty"] = provenance.code_dirty()
    data = render.to_json(result)
    markdown = render.to_markdown(result, title)
    commit = provenance.record(result.run_id, provenance.run_files(data, markdown), provenance.commit_message(data))
    data["manifest"]["provenance_commit"] = commit
    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = scenario_id or result.run_id
        (out_dir / f"{stem}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        (out_dir / f"{stem}.md").write_text(markdown, encoding="utf-8")
    summary = "off-topic (stopped after the intake)" if result.report is None else result.report.summary()
    return {"run_id": result.run_id, "markdown": markdown, "summary": summary,
            "cost_usd": result.manifest["cost_usd"], "provenance_commit": commit}


def _assess(args: argparse.Namespace) -> int:
    from pathlib import Path

    from afs_assistant.llm import OpenRouterClient

    enquiry = args.text if args.text else Path(args.file).read_text(encoding="utf-8")
    out = _assess_one(enquiry.strip(), None, OpenRouterClient(), Path(args.out) if args.out else None,
                      external=args.external)
    print(out["markdown"])
    print(f"\n[run {out['run_id']} | verification {out['summary']} | ${out['cost_usd']:.4f} | "
          f"provenance {out['provenance_commit'][:10]}]")
    return 0


def _run_set(args: argparse.Namespace) -> int:
    """Assess a scenario set on `--workers` threads (1 = one after the other). A line per case as it
    finishes, then a summary in scenario order. A spend cap (or an unexpected error) stops new cases;
    the running ones finish, then it is raised. Ctrl-C cancels the queued cases and sets the tracker's
    cancel event, so running cases stop at their next model call."""
    from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

    from openai import APIError

    from afs_assistant import paths, scenarios
    from afs_assistant.llm import OpenRouterClient, SpendCapExceeded

    if args.set == "final" and not args.final_ok:
        print("The final set is held out. Pass --i-know-this-is-the-final-run to generate it (Phase 5 only).")
        return 2
    if args.workers < 1:
        print("--workers must be at least 1.")
        return 2
    client = OpenRouterClient()
    items = scenarios.load(args.set)
    if args.only:
        items = [s for s in items if s["id"] in args.only.split(",")]
    lines: dict[str, str] = {}
    failed: set[str] = set()
    stop: Exception | None = None
    queue = list(items)
    pool = ThreadPoolExecutor(max_workers=args.workers)
    try:
        running = {}
        while queue or running:
            while queue and stop is None and len(running) < args.workers:
                s = queue.pop(0)
                running[pool.submit(_assess_one, s["enquiry"], s["id"], client, paths.OUTPUTS / args.set,
                                    s["title"], external=args.external)] = s["id"]
            if not running:
                break
            done, _ = wait(running, return_when=FIRST_COMPLETED)
            for future in done:
                sid = running.pop(future)
                try:
                    out = future.result()
                except Exception as exc:  # noqa: BLE001 - one bad scenario must not stop the set
                    failed.add(sid)
                    lines[sid] = f"{sid}: FAILED {type(exc).__name__}: {exc}"
                    if isinstance(exc, SpendCapExceeded) or not isinstance(exc, (RuntimeError, ValueError, APIError)):
                        stop = stop or exc      # a spend cap or an unexpected error: no new cases
                else:
                    lines[sid] = f"{sid}: verification {out['summary']} cost ${out['cost_usd']:.4f}"
                print(lines[sid], flush=True)
    except KeyboardInterrupt:      # Ctrl-C: queued cases never start; running ones stop at their next LLM wait
        client.tracker.cancel.set()
        pool.shutdown(wait=False, cancel_futures=True)
        print("interrupted: queued cases cancelled; running cases stop at their next model call", flush=True)
        raise
    pool.shutdown()
    order = [s["id"] for s in items]
    print("summary (scenario order):")
    for sid in order:
        print(f"  {lines.get(sid, f'{sid}: not run (stopped)')}")
    print(f"session cost ${client.tracker.session_usd:.4f}; "
          f"failed: {[sid for sid in order if sid in failed] or 'none'}")
    if stop is not None:
        raise stop
    return 1 if failed else 0


def _external_replay(args: argparse.Namespace) -> int:
    """Re-verify every recorded external item of a run JSON offline; exit 1 on any difference."""
    import json
    from pathlib import Path

    from afs_assistant.external import step

    data = json.loads(Path(args.run_json).read_text(encoding="utf-8"))
    if data.get("off_topic") is not None:
        print("This is an off-topic run (stopped after the intake): no external block to re-verify.")
        return 2
    block = data.get("external")
    if block is None:
        print("This run has no external block (it ran with --external=off).")
        return 2
    rows = step.replay(block)
    for row in rows:
        mark = "equal" if row["equal"] else "DIFFERENT"
        detail = "" if row["equal"] else f" (recorded: {row['recorded']}; replayed: {row['replayed']})"
        print(f"{mark}: {row['item']}{detail}")
    different = sum(1 for row in rows if not row["equal"])
    print(f"{len(rows)} item(s) re-verified offline; {different} different")
    return 1 if different else 0


def _eval(args: argparse.Namespace) -> int:
    """Deterministic checklist over saved runs; writes outputs/eval/summary.md and summary.json.
    Exit 1 when a must-not item fails, else 0 (other failures are information in the summary)."""
    from pathlib import Path

    from afs_assistant import evaluate

    if args.outputs and not args.set:
        print("--outputs needs --set (one set per outputs directory).")
        return 2
    sets = [args.set] if args.set else list(evaluate.SETS)
    results = {s: evaluate.evaluate_set(s, Path(args.outputs) if args.outputs else None, mermaid=args.mermaid,
                                        cache_root=Path(args.external_cache) if args.external_cache else None)
               for s in sets}
    evaluate.write_summary(results, Path(args.out) if args.out else None)
    must_not_failed = 0
    for s, res in results.items():
        t = res["totals"]
        fails = sum(v["fail"] for v in t["per_item"].values())
        scen = t["scenario_items"]
        must_not_failed += scen["must_not"]["fail"]
        print(f"{s}: {t['evaluated']}/{t['cases']} evaluated ({t['not_run']} not run); checklist failures {fails}; "
              f"must fail {scen['must']['fail']}, must-not fail {scen['must_not']['fail']}")
    print(f"summary: {Path(args.out) if args.out else evaluate.paths.OUTPUTS / 'eval'}/summary.md")
    return 1 if must_not_failed else 0


EXTERNAL_HELP = ("external evidence: live (search the web APIs; falls back to the curated library on a network "
                 "error or rate limit), cache (no network: answers HTTP requests from the recorded responses only; "
                 "the model calls run again, so queries that differ from the recorded run miss and fall back to "
                 "the library; `afs-assist external replay RUN.json` is the exact offline re-check), off")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="afs-assist")
    sub = parser.add_subparsers(dest="command", required=True)
    kb_parser = sub.add_parser("kb", help="knowledge base commands")
    kb_sub = kb_parser.add_subparsers(dest="kb_command", required=True)
    kb_sub.add_parser("build", help="rebuild knowledge/ from resources/").set_defaults(func=_kb_build)
    kb_sub.add_parser("check", help="validate knowledge/").set_defaults(func=_kb_check)
    sc_parser = sub.add_parser("scenarios", help="scenario files")
    sc_sub = sc_parser.add_subparsers(dest="sc_command", required=True)
    sc_sub.add_parser("build", help="parse organizer scenario files into scenarios/").set_defaults(func=_scenarios_build)
    a = sub.add_parser("assess", help="assess one enquiry")
    src = a.add_mutually_exclusive_group(required=True)
    src.add_argument("--text")
    src.add_argument("--file")
    a.add_argument("--out", help="directory for .json/.md output")
    a.add_argument("--external", choices=["live", "cache", "off"], default="live", help=EXTERNAL_HELP)
    a.set_defaults(func=_assess)
    r = sub.add_parser("run", help="assess a scenario set")
    r.add_argument("--set", choices=["dev", "adversarial", "final"], required=True)
    r.add_argument("--only", help="comma-separated scenario ids")
    r.add_argument("--i-know-this-is-the-final-run", dest="final_ok", action="store_true")
    r.add_argument("--external", choices=["live", "cache", "off"], default="live", help=EXTERNAL_HELP)
    r.add_argument("--workers", type=int, default=4, help="scenarios assessed in parallel (1 = one at a time)")
    r.set_defaults(func=_run_set)
    ev = sub.add_parser("eval", help="deterministic checklist over saved runs (no model calls)")
    ev.add_argument("--set", choices=["dev", "adversarial"], help="one set (default: both)")
    ev.add_argument("--outputs", help="outputs directory of the set (default outputs/<set>)")
    ev.add_argument("--out", help="directory for summary.md/json (default outputs/eval)")
    ev.add_argument("--mermaid", action="store_true", help="also render every Mermaid chart with mermaid-cli")
    ev.add_argument("--external-cache", help="external full-text cache for the replay item "
                                             "(default runs/external_cache)")
    ev.set_defaults(func=_eval)
    e = sub.add_parser("external", help="external evidence commands")
    e_sub = e.add_subparsers(dest="external_command", required=True)
    rp = e_sub.add_parser("replay", help="re-verify a run's external items offline against the cached text")
    rp.add_argument("run_json")
    rp.set_defaults(func=_external_replay)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
