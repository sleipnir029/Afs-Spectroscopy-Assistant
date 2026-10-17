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


def _assess_one(enquiry: str, scenario_id: str | None, client, out_dir=None, title: str = "") -> dict:
    import json
    from datetime import UTC, datetime

    from afs_assistant import pipeline, provenance, render

    # Unique per run so provenance tags are never overwritten; output files keep the scenario id.
    run_id = f"{scenario_id or 'adhoc'}-{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
    result = pipeline.run(enquiry, client, run_id=run_id)
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
    return {"run_id": result.run_id, "markdown": markdown, "summary": result.report.summary(),
            "cost_usd": result.manifest["cost_usd"], "provenance_commit": commit}


def _assess(args: argparse.Namespace) -> int:
    from pathlib import Path

    from afs_assistant.llm import OpenRouterClient

    enquiry = args.text if args.text else Path(args.file).read_text(encoding="utf-8")
    out = _assess_one(enquiry.strip(), None, OpenRouterClient(), Path(args.out) if args.out else None)
    print(out["markdown"])
    print(f"\n[run {out['run_id']} | verification {out['summary']} | ${out['cost_usd']:.4f} | "
          f"provenance {out['provenance_commit'][:10]}]")
    return 0


def _run_set(args: argparse.Namespace) -> int:
    from openai import APIError

    from afs_assistant import paths, scenarios
    from afs_assistant.llm import OpenRouterClient, SpendCapExceeded

    if args.set == "final" and not args.final_ok:
        print("The final set is held out. Pass --i-know-this-is-the-final-run to generate it (Phase 5 only).")
        return 2
    client = OpenRouterClient()
    items = scenarios.load(args.set)
    if args.only:
        items = [s for s in items if s["id"] in args.only.split(",")]
    failed = []
    for s in items:
        try:
            out = _assess_one(s["enquiry"], s["id"], client, paths.OUTPUTS / args.set, s["title"])
        except SpendCapExceeded:
            raise
        except (RuntimeError, ValueError, APIError) as exc:  # one bad scenario must not stop the set
            failed.append(s["id"])
            print(f"{s['id']}: FAILED {type(exc).__name__}: {exc}")
            continue
        print(f"{s['id']}: verification {out['summary']} cost ${out['cost_usd']:.4f}")
    print(f"session cost ${client.tracker.session_usd:.4f}; failed: {failed or 'none'}")
    return 1 if failed else 0


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
    a.set_defaults(func=_assess)
    r = sub.add_parser("run", help="assess a scenario set")
    r.add_argument("--set", choices=["dev", "final"], required=True)
    r.add_argument("--only", help="comma-separated scenario ids")
    r.add_argument("--i-know-this-is-the-final-run", dest="final_ok", action="store_true")
    r.set_defaults(func=_run_set)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
