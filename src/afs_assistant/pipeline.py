"""The assessment pipeline: intake -> screen -> assess -> verify -> repair -> finalize.

AFS-Ashby steps 0-2 (LLM intake), 3-4 (deterministic screening and fiber coverage),
5-8 (LLM assessment over the full page-tagged knowledge base), then deterministic
verification with at most MAX_REPAIR_ROUNDS repair calls. Finalize never shows an
unverified citation as verified: failing citations are removed and flagged.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cache, lru_cache

from afs_assistant import kb, paths
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import UNKNOWN, Candidate, screen
from afs_assistant.verify import Report, sanitize_intake, verify

MAX_REPAIR_ROUNDS = 2
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
    lines.append("\n# RULES (curated from the sources; cite the underlying page, not the rule)")
    for r in kb.rules():
        srcs = ", ".join(kb.citation_label(s["doc"], s["page"]) for s in r["sources"])
        lines.append(f"[{r['id']}] ({r['effect']}) {r['statement']} -- sources: {srcs}")
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


def _assess_user(enquiry: str, intake: Intake, candidates: list[Candidate]) -> str:
    return "\n\n".join([
        "# CUSTOMER ENQUIRY (everything the customer said)\n" + enquiry,
        "# INTAKE (steps 0-2)\n" + intake.model_dump_json(indent=1),
        screening_table(candidates),
    ])


def _repair_user(previous: Assessment, report: Report, base_user: str) -> str:
    failures = "\n".join(f"- [{c.name}] {c.location}: {c.message}" for c in report.hard_failures)
    return "\n\n".join([base_user, "# YOUR PREVIOUS ASSESSMENT\n" + previous.model_dump_json(indent=1),
                        "# VERIFICATION FAILURES TO FIX\n" + failures])


def finalize(a: Assessment, report: Report) -> tuple[Assessment, list[dict]]:
    """Remove citations that failed verification; record what was removed."""
    bad = {c["location"] for c in report.citations if not c["verified"]}
    removed: list[dict] = []
    data = json.loads(a.model_dump_json())

    def strip(container: dict, loc: str) -> None:
        kept = []
        for j, cit in enumerate(container.get("citations", [])):
            if f"{loc}.citations[{j}]" in bad:
                removed.append({"location": f"{loc}.citations[{j}]", "citation": cit})
            else:
                kept.append(cit)
        container["citations"] = kept

    for key in ("premise_checks", "recommendations", "spectral_ranges", "risks"):
        for i, item in enumerate(data[key]):
            strip(item, f"{key}[{i}]")
    strip(data["measurement_concept"], "measurement_concept")
    for i, step in enumerate(data["feasibility_plan"]["steps"]):
        strip(step, f"feasibility_plan.steps[{i}]")
    return Assessment.model_validate(data), removed


def run(enquiry: str, client, run_id: str | None = None) -> RunResult:
    run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    tracker = getattr(client, "tracker", None)
    if tracker is not None:
        tracker.start_run()
        first_call = len(tracker.calls)

    intake_res = client.complete_json("intake", prompt("intake"), "# CUSTOMER ENQUIRY\n" + enquiry,
                                      "intake", Intake.model_json_schema())
    intake, intake_removed = sanitize_intake(Intake.model_validate(intake_res.data), enquiry)
    slots = slots_from_intake(intake)
    candidates = screen(slots)

    system = prompt("assess") + "\n\n" + knowledge_block()
    base_user = _assess_user(enquiry, intake, candidates)
    res = client.complete_json("assess", system, base_user, "assessment", Assessment.model_json_schema())
    raw = Assessment.model_validate(res.data)
    current, report = raw, verify(enquiry, intake, raw, candidates, slots, intake_removed)

    repairs = []
    for round_no in range(1, MAX_REPAIR_ROUNDS + 1):
        if report.passed:
            break
        res = client.complete_json("repair", system + "\n\n" + prompt("repair"),
                                   _repair_user(current, report, base_user), "assessment",
                                   Assessment.model_json_schema())
        repairs.append({"round": round_no, "hard_failures_before": len(report.hard_failures)})
        current = Assessment.model_validate(res.data)
        report = verify(enquiry, intake, current, candidates, slots, intake_removed)
        repairs[-1]["hard_failures_after"] = len(report.hard_failures)

    final, removed = finalize(current, report)
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
        "repair_rounds": len(repairs),
        "verification": report.summary(),
    }
    return RunResult(run_id, enquiry, intake, slots, candidates, raw, final, report, repairs, removed,
                     intake_removed, calls, manifest)
