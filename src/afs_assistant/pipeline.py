"""The assessment pipeline: intake -> screen -> assess -> verify -> repair -> finalize.

AFS-Ashby steps 0-2 (LLM intake), 3-4 (deterministic screening and fiber coverage),
5-8 (LLM assessment over the full page-tagged knowledge base), then deterministic
verification with at most MAX_REPAIR_ROUNDS repair calls; the round with the fewest
hard failures is kept. Finalize never shows an unverified citation as verified: failing
citations are removed, items that lost one or failed a number check are flagged, and
duplicates, screen violations and inconsistent status are fixed deterministically.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cache, lru_cache

from afs_assistant import kb, paths, quotes
from afs_assistant.methods import named_methods
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import UNKNOWN, Candidate, screen
from afs_assistant.verify import Report, check_status, sanitize_intake, verify

MAX_REPAIR_ROUNDS = 2
# Highest role first: a duplicate method+technique keeps the entry with the best role.
ROLE_RANK = {"primary": 0, "comparison": 1, "conditional": 2, "not_recommended": 3}
PROMPTS = paths.ROOT / "prompts"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@cache
def prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8")


@lru_cache(maxsize=1)
def knowledge_block() -> str:
    """All source pages (quotable text only) and the rule list, as one stable, cacheable block."""
    lines = ["# SOURCE PAGES",
             "Each page starts with a header line [DOC p.N | scope | title]. Quote only from the text after the header."]
    for (doc, number), rec in kb.pages().items():
        label = kb.citation_label(doc, number)
        lines.append(f"\n[{label} | scope: {', '.join(rec['scope'])} | {rec['title']}]\n{rec['text']}")
    lines.append("\n# RULES (curated from the sources; cite the underlying page, not the rule)\n"
                 "Each rule statement is our paraphrase: never quote it. To cite a rule, quote one of its "
                 "verbatim source passages listed below it, with that passage's label.")
    for r in kb.rules():
        lines.append(f"[{r['id']}] ({r['effect']}) paraphrase, never quote this: {r['statement']}")
        lines += [f'  source [{kb.citation_label(s["doc"], s["page"])}]: "{s["quote"]}"' for s in r["sources"]]
    return "\n".join(lines)


def slots_from_intake(intake: Intake) -> dict:
    slots: dict = {}
    for name in ("physical_state", "optical_regime", "aqueous", "heterogeneous", "fluorophore"):
        value = getattr(intake.sample, name).value
        slots[name] = value if value != "unknown" else UNKNOWN
    f = intake.proposed_fiber
    if f.family != "none" and f.for_method != "none":
        slots["proposed_fiber"] = {"family": f.family, "for_method": f.for_method}
    return slots


def screening_table(candidates: list[Candidate]) -> str:
    rows = ["# SCREENING (deterministic; method x in-line technique)",
            "status | method | technique | reasons | warnings (rule ids) | notes"]
    for c in candidates:
        reasons = "; ".join(f"{r['rule']}: {r['message']}" for r in c.reasons) or "-"
        rows.append(f"{c.status} | {c.method} | {c.technique} | {reasons} | {', '.join(c.warnings) or '-'} | "
                    f"{' '.join(c.notes) or '-'}")
    return "\n".join(rows)


@dataclass
class RunResult:
    run_id: str
    enquiry: str
    intake: Intake
    slots: dict
    candidates: list[Candidate]
    assessment_raw: Assessment
    assessment: Assessment
    report: Report
    repairs: list[dict] = field(default_factory=list)
    removed: list[dict] = field(default_factory=list)
    intake_removed: list[dict] = field(default_factory=list)
    calls: list[dict] = field(default_factory=list)
    manifest: dict = field(default_factory=dict)
    flagged: dict[str, str] = field(default_factory=dict)    # item path -> why it is shown with a warning
    timings: dict[str, float] = field(default_factory=dict)  # seconds per stage, plus wall
    named_methods: dict[str, str] = field(default_factory=dict)  # method -> enquiry span naming it


def _assess_user(enquiry: str, intake: Intake, candidates: list[Candidate]) -> str:
    named = named_methods(enquiry)
    return "\n\n".join([
        "# CUSTOMER ENQUIRY (everything the customer said)\n" + enquiry,
        "# INTAKE (steps 0-2)\n" + intake.model_dump_json(indent=1),
        "# METHODS NAMED IN THE ENQUIRY (found by word list; judge whether the customer proposes them)\n"
        + (", ".join(f'{m} ("{q}")' for m, q in named.items()) or "none"),
        screening_table(candidates),
    ])


def _repair_user(previous: Assessment, report: Report, base_user: str) -> str:
    # For near-miss quotes, show the closest page passage (repair prompt only, never the user output).
    hints = {}
    for c in report.citations:
        if c["quote_status"] == "fuzzy_review":
            q = quotes.verify(c["doc"], c["page"], c["quote"])
            if q.start is not None:
                text = kb.page(c["doc"], c["page"])["text"]
                hints[c["location"]] = f'; closest passage on that page: "{text[q.start:q.end]}"'
    failures = "\n".join(f"- [{c.name}] {c.location}: {c.message}"
                         f"{hints.get(c.location, '') if c.name == 'quote_verified' else ''}"
                         for c in report.hard_failures)
    return "\n\n".join([base_user, "# YOUR PREVIOUS ASSESSMENT\n" + previous.model_dump_json(indent=1),
                        "# VERIFICATION FAILURES TO FIX\n" + failures])


def finalize(a: Assessment, report: Report,
             candidates: list[Candidate]) -> tuple[Assessment, list[dict], dict[str, str]]:
    """Make the kept round safe to show. Every change is recorded in `removed` with a reason.

    1. Remove citations that failed verification.
    2. A recommended entry whose candidate failed screening becomes not_recommended.
    3. Same method+technique listed twice: keep the highest role, drop the others.
    4. A `supported` or `contradicted` premise with no citation left becomes `not_covered`.
    5. Status inconsistent with premises -> premise_not_supported; with recommendations
       -> insufficient_information (re-checked on the result of steps 1-4).
    Locations in the change log use the numbering of `a`. Returns the assessment, the
    change log and the flagged items (path in the returned assessment -> reason) that
    render marks with a warning: items that lost a citation or failed a number check.
    """
    bad = {c["location"] for c in report.citations if not c["verified"]}
    removed: list[dict] = []
    flagged: dict[str, str] = {}
    data = json.loads(a.model_dump_json())

    def strip(container: dict, loc: str) -> None:
        kept = []
        for j, cit in enumerate(container.get("citations", [])):
            if f"{loc}.citations[{j}]" in bad:
                removed.append({"location": f"{loc}.citations[{j}]", "citation": cit,
                                "reason": "citation failed verification; removed"})
                flagged[loc] = "a citation failed verification and was removed"
            else:
                kept.append(cit)
        container["citations"] = kept

    for key in ("premise_checks", "recommendations", "spectral_ranges", "risks"):
        for i, item in enumerate(data[key]):
            strip(item, f"{key}[{i}]")
    strip(data["measurement_concept"], "measurement_concept")
    for i, step in enumerate(data["feasibility_plan"]["steps"]):
        strip(step, f"feasibility_plan.steps[{i}]")
    for c in report.hard_failures:
        if c.name in ("numbers_claim_local", "numbers_uncited_text"):
            flagged[c.location] = "contains a figure not found in its sources or the enquiry"

    status = {(c.method, c.technique): c.status for c in candidates}
    for i, r in enumerate(data["recommendations"]):
        if r["role"] != "not_recommended" and status.get((r["method"], r["technique"])) == "fail":
            removed.append({"location": f"recommendations[{i}]", "item": dict(r),
                            "reason": f"{r['method']} {r['technique']} failed screening; "
                                      f"role {r['role']} changed to not_recommended",
                            "corrects": "respects_screen"})
            flagged[f"recommendations[{i}]"] = "failed screening; changed to not recommended by verification"
            r["role"] = "not_recommended"

    # Dedupe method+technique (stable: on equal role the earlier entry wins), then renumber flags.
    recs = data["recommendations"]
    best: dict[tuple[str, str], int] = {}
    for i, r in enumerate(recs):
        key = (r["method"], r["technique"])
        if key not in best or ROLE_RANK[r["role"]] < ROLE_RANK[recs[best[key]]["role"]]:
            best[key] = i
    keep = sorted(best.values())
    for i, r in enumerate(recs):
        if i not in keep:
            winner = best[(r["method"], r["technique"])]
            removed.append({"location": f"recommendations[{i}]", "item": r,
                            "reason": f"duplicate method+technique; kept recommendations[{winner}] "
                                      f"(role {recs[winner]['role']})",
                            "corrects": "recommendations_unique"})
    new_index = {old: new for new, old in enumerate(keep)}
    renumbered = {}
    for path, why in flagged.items():
        if path.startswith("recommendations["):
            old = int(path[len("recommendations["):path.index("]")])
            if old in new_index:
                renumbered[f"recommendations[{new_index[old]}]{path[path.index(']') + 1:]}"] = why
        else:
            renumbered[path] = why
    flagged = renumbered
    data["recommendations"] = [recs[i] for i in keep]

    demoted_contradiction = False
    for i, p in enumerate(data["premise_checks"]):
        if p["verdict"] in ("supported", "contradicted") and not p["citations"]:
            change = {"location": f"premise_checks[{i}]", "item": dict(p),
                      "reason": f"verdict {p['verdict']} without a verified citation; changed to not_covered"}
            if p["verdict"] == "contradicted":
                change["corrects"] = "status_vs_premises"
                flagged[f"premise_checks[{i}]"] = ("contradiction not verified; changed to not covered, "
                                                   "explanation is the model's original")
                demoted_contradiction = True
            removed.append(change)
            p["verdict"] = "not_covered"

    interim = Report()
    check_status(Assessment.model_validate(data), interim)
    failed = {c.name for c in interim.hard_failures}
    for name, new_status in (("status_vs_premises", "premise_not_supported"),
                             ("status_vs_recommendations", "insufficient_information")):
        if name in failed and data["decision_status"] == "provisional_assessment":
            removed.append({"location": "decision_status", "item": data["decision_status"],
                            "reason": f"{name} failed; status changed to {new_status}", "corrects": name})
            data["decision_status"] = new_status
            flagged["status_reason"] = "status changed by verification; this reason text is the model's original"
    # The model's own premise_not_supported may rest on a contradiction that failed verification.
    if (demoted_contradiction and data["decision_status"] == "premise_not_supported"
            and not any(p["verdict"] == "contradicted" for p in data["premise_checks"])):
        flagged.setdefault("status_reason", "the contradiction behind this status failed verification")
    return Assessment.model_validate(data), removed, flagged


def run(enquiry: str, client, run_id: str | None = None) -> RunResult:
    run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    tracker = getattr(client, "tracker", None)
    if tracker is not None:
        tracker.start_run()
        first_call = len(tracker.calls)
    timings: dict[str, float] = {}
    wall = clock = time.monotonic()

    def lap(stage: str) -> None:
        nonlocal clock
        now = time.monotonic()
        timings[stage] = round(timings.get(stage, 0.0) + now - clock, 3)
        clock = now

    intake_res = client.complete_json("intake", prompt("intake"), "# CUSTOMER ENQUIRY\n" + enquiry,
                                      "intake", Intake.model_json_schema())
    intake, intake_removed = sanitize_intake(Intake.model_validate(intake_res.data), enquiry)
    lap("intake")
    slots = slots_from_intake(intake)
    candidates = screen(slots)
    lap("screen")

    system = prompt("assess") + "\n\n" + knowledge_block()
    base_user = _assess_user(enquiry, intake, candidates)
    res = client.complete_json("assess", system, base_user, "assessment", Assessment.model_json_schema())
    raw = Assessment.model_validate(res.data)
    lap("assess")
    current, report = raw, verify(enquiry, intake, raw, candidates, slots, intake_removed)
    lap("verify")
    best, best_report, best_round = current, report, 0

    repairs = []
    for round_no in range(1, MAX_REPAIR_ROUNDS + 1):
        if report.passed:
            break
        res = client.complete_json("repair", system + "\n\n" + prompt("repair"),
                                   _repair_user(current, report, base_user), "assessment",
                                   Assessment.model_json_schema())
        repairs.append({"round": round_no, "hard_failures_before": len(report.hard_failures)})
        current = Assessment.model_validate(res.data)
        lap("repair")
        report = verify(enquiry, intake, current, candidates, slots, intake_removed)
        lap("verify")
        repairs[-1]["hard_failures_after"] = len(report.hard_failures)
        repairs[-1]["assessment"] = json.loads(current.model_dump_json())
        if len(report.hard_failures) <= len(best_report.hard_failures):   # ties: the later round
            best, best_report, best_round = current, report, round_no

    final, removed, flagged = finalize(best, best_report, candidates)
    lap("finalize")
    timings["wall"] = round(time.monotonic() - wall, 3)
    calls = tracker.calls[first_call:] if tracker is not None else []
    manifest = {
        "run_id": run_id,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "models": sorted({c["model"] for c in calls}),
        "prompt_sha256": {n: sha(prompt(n)) for n in ("intake", "assess", "repair")},
        "knowledge_sha256": sha(knowledge_block()),
        "pages_sha256": sha(paths.PAGES_FILE.read_text(encoding="utf-8")),
        "rules_sha256": sha(paths.RULES_FILE.read_text(encoding="utf-8")),
        "cost_usd": round(sum(c["cost_usd"] for c in calls), 6),
        "tokens": {"prompt": sum(c["prompt_tokens"] for c in calls),
                   "completion": sum(c["completion_tokens"] for c in calls),
                   "cached": sum(c["cached_tokens"] for c in calls)},
        "calls": len(calls),
        "repair_rounds": len(repairs),
        "kept_round": best_round,
        "timings_s": timings,
        "verification": best_report.summary(),
    }
    return RunResult(run_id, enquiry, intake, slots, candidates, raw, final, best_report, repairs, removed,
                     intake_removed, calls, manifest, flagged, timings, named_methods(enquiry))
