"""Render a pipeline run as Markdown (organizer section order) and JSON."""

from __future__ import annotations

import json

from afs_assistant import kb
from afs_assistant.pipeline import RunResult

STATUS_LABEL = {
    "provisional_assessment": "Provisional feasibility assessment",
    "insufficient_information": "Insufficient information for a method choice",
    "premise_not_supported": "Premise not supported by the sources",
    "outside_supported_scope": "Outside the supported scope",
}
ROLE_LABEL = {"primary": "Primary candidate", "comparison": "Comparison candidate",
              "conditional": "Conditional candidate", "not_recommended": "Not recommended"}


class _Citer:
    """Numbers citations in order of appearance and collects them for the evidence list."""

    def __init__(self) -> None:
        self.entries: list[dict] = []

    def refs(self, citations) -> str:
        if not citations:
            return " *(no verified source: engineering judgement)*"
        marks = []
        for c in citations:
            self.entries.append(c)
            marks.append(f"[{len(self.entries)}: {kb.citation_label(c.doc, c.page)}]")
        return " " + " ".join(marks)


def to_markdown(r: RunResult, title: str = "") -> str:
    a = r.assessment
    cite = _Citer()
    out = [f"# First technical assessment{': ' + title if title else ''}", ""]
    out += ["**Customer enquiry**", "", f"> {r.enquiry}", ""]
    out += [f"**Decision status:** {STATUS_LABEL[a.decision_status]}. {a.status_reason}", ""]

    if a.premise_checks:
        out += ["## Premise check", ""]
        for p in a.premise_checks:
            out.append(f"- **{p.verdict.replace('_', ' ').capitalize()}:** {p.premise}. {p.explanation}{cite.refs(p.citations)}")
        out.append("")

    out += ["## Requirements", "", "**Stated by the customer**", ""]
    out += [f"- {s}" for s in a.requirements_stated] + ["", "**Key unknowns**", ""]
    out += [f"- {s}" for s in a.key_unknowns] + [""]

    out += ["## Clarification questions (most decision-relevant first)", ""]
    for q in a.clarification_questions:
        out.append(f"{q.id}. {q.question} *Why it matters:* {q.why_it_matters} *(affects: {', '.join(q.affects)})*")
    out.append("")

    out += ["## Recommendation", ""]
    for m in a.recommendations:
        cond = "" if m.conditions.strip().lower() in ("", "none") else f" *Conditions:* {m.conditions}"
        out.append(f"- **{m.id} · {ROLE_LABEL[m.role]}: {m.method}, {m.technique.replace('_', ' ')}.** "
                   f"{m.rationale}{cond}{cite.refs(m.citations)}")
    out.append("")

    mc = a.measurement_concept
    out += ["## Measurement concept", "",
            f"- **Probe and geometry:** {mc.probe_and_geometry}",
            f"- **Location:** {mc.location}",
            f"- **Fiber link:** {mc.fiber_link}{cite.refs(mc.citations)}", ""]

    out += ["## Spectral range", ""]
    out += [f"- **{s.method}:** {s.statement}{cite.refs(s.citations)}" for s in a.spectral_ranges] + [""]

    out += ["## Risks and uncertainty", ""]
    for k in a.risks:
        rules = f" *(rules: {', '.join(k.rule_ids)})*" if k.rule_ids else ""
        out.append(f"- {k.risk}{rules}{cite.refs(k.citations)}")
    out.append("")

    fp = a.feasibility_plan
    out += ["## First feasibility experiment", ""]
    out += [f"{i}. **{s.step}** {s.purpose}{cite.refs(s.citations)}" for i, s in enumerate(fp.steps, 1)]
    out += ["", f"**Reference measurements:** {fp.reference_measurements}", "",
            f"**Decision basis:** {fp.decision_basis}", ""]

    if a.assumptions:
        out += ["## Assumptions", ""] + [f"- {s}" for s in a.assumptions] + [""]
    if a.not_in_sources:
        out += ["## Not covered by the supplied sources", ""] + [f"- {s}" for s in a.not_in_sources] + [""]

    out += ["## Evidence (verified quotes)", ""]
    for i, c in enumerate(cite.entries, 1):
        out.append(f"{i}. ✓ **{kb.citation_label(c.doc, c.page)}** ({c.claim_kind.replace('_', ' ')}): \"{c.quote}\"")
    out.append("")

    s = r.report.summary()
    out += ["## Verification", "",
            (f"- Citations verified: {s['citations_verified']} of {s['citations_total']} "
             f"(exact or whitespace/hyphen-tolerant match on the cited page, scope checked)."),
            (f"- Remaining hard check failures: {s['hard_failures']}; soft warnings: {s['soft_failures']}; "
             f"repair rounds: {len(r.repairs)}.")]
    if r.removed:
        out.append(f"- Removed {len(r.removed)} citation(s) that failed verification:")
        out += [(f"  - ⚠ {x['location']}: {x['citation']['doc']} p.{x['citation']['page']} "
                 f"\"{x['citation']['quote'][:120]}\"") for x in r.removed]
    for c in r.report.hard_failures:
        if c.name not in ("quote_verified", "citation_scope"):
            out.append(f"- ⚠ {c.name} at {c.location}: {c.message}")
    if r.intake_removed:
        out.append(f"- Removed {len(r.intake_removed)} intake item(s) not quoted verbatim from the enquiry:")
        out += [f"  - {x['location']}: {x['reason']}" for x in r.intake_removed]
    out += ["", (f"*Run {r.run_id} · models {', '.join(r.manifest.get('models', []))} · "
            f"cost ${r.manifest.get('cost_usd', 0):.4f}*"), ""]
    return "\n".join(out)


def to_json(r: RunResult) -> dict:
    return {
        "run_id": r.run_id,
        "enquiry": r.enquiry,
        "intake": json.loads(r.intake.model_dump_json()),
        "slots": r.slots,
        "screening": [{"method": c.method, "technique": c.technique, "status": c.status, "reasons": c.reasons,
                       "warnings": c.warnings, "notes": c.notes} for c in r.candidates],
        "assessment": json.loads(r.assessment.model_dump_json()),
        "verification": r.report.to_dict(),
        "removed_citations": r.removed,
        "repairs": r.repairs,
        "manifest": r.manifest,
    }
