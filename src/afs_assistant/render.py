"""Render a pipeline run as Markdown (organizer section order) and JSON."""

from __future__ import annotations

import json

from afs_assistant import kb, scope
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


def open_failures(r: RunResult) -> list:
    """Hard failures still open after finalize: removed citations and deterministic corrections are not."""
    corrected = {x["corrects"] for x in r.removed if "citation" not in x and "corrects" in x}
    return [c for c in r.report.hard_failures
            if c.name not in ("quote_verified", "citation_scope") and c.name not in corrected]


def to_markdown(r: RunResult, title: str = "") -> str:
    a = r.assessment
    cite = _Citer()

    def warn(path: str) -> str:
        """Inline warning for an item finalize flagged (lost a citation, unsupported figure)."""
        return f" ⚠ *({r.flagged[path]})*" if path in r.flagged else ""

    out = [f"# First technical assessment{': ' + title if title else ''}", ""]
    out += ["**Customer enquiry**", "", f"> {r.enquiry}", ""]
    out += [f"**Decision status:** {STATUS_LABEL[a.decision_status]}. {a.status_reason}{warn('status_reason')}", ""]

    if a.premise_checks:
        out += ["## Premise check", ""]
        for i, p in enumerate(a.premise_checks):
            out.append(f"- **{p.verdict.replace('_', ' ').capitalize()}:** {p.premise.rstrip().rstrip('.')}. "
                       f"{p.explanation}{cite.refs(p.citations)}{warn(f'premise_checks[{i}]')}")
        out.append("")

    out += ["## Requirements", "", "**Stated by the customer**", ""]
    out += [f"- {s}{warn(f'requirements_stated[{i}]')}" for i, s in enumerate(a.requirements_stated)]
    out += ["", "**Key unknowns**", ""]
    out += [f"- {s}{warn(f'key_unknowns[{i}]')}" for i, s in enumerate(a.key_unknowns)] + [""]

    out += ["## Clarification questions (most decision-relevant first)", ""]
    for i, q in enumerate(a.clarification_questions):
        out.append(f"{q.id}. {q.question} *Why it matters:* {q.why_it_matters} *(affects: {', '.join(q.affects)})*"
                   f"{warn(f'clarification_questions[{i}]')}")
    out.append("")

    out += ["## Recommendation", ""]
    for i, m in enumerate(a.recommendations):
        cond = "" if m.conditions.strip().lower() in ("", "none") else f" *Conditions:* {m.conditions}"
        # A combination is never part of the headline: single methods are tested first.
        combo = (f" Later hypothesis, after single-method tests: combine with {', '.join(m.combined_with)}."
                 if m.combined_with else "")
        out.append(f"- **{m.id} · {ROLE_LABEL[m.role]}: {m.method}, {m.technique.replace('_', ' ')}.** "
                   f"{m.rationale}{cond}{cite.refs(m.citations)}{combo}{warn(f'recommendations[{i}]')}")
    out.append("")

    mc = a.measurement_concept
    out += ["## Measurement concept", "",
            f"- **Probe and geometry:** {mc.probe_and_geometry}",
            f"- **Location:** {mc.location}",
            f"- **Fiber link:** {mc.fiber_link}{cite.refs(mc.citations)}{warn('measurement_concept')}", ""]

    out += ["## Spectral range", ""]
    out += [f"- **{s.method}:** {s.statement}{cite.refs(s.citations)}{warn(f'spectral_ranges[{i}]')}"
            for i, s in enumerate(a.spectral_ranges)] + [""]

    out += ["## Risks and uncertainty", ""]
    for i, k in enumerate(a.risks):
        rules = f" *(rules: {', '.join(k.rule_ids)})*" if k.rule_ids else ""
        out.append(f"- {k.risk}{rules}{cite.refs(k.citations)}{warn(f'risks[{i}]')}")
    out.append("")

    fp = a.feasibility_plan
    out += ["## First feasibility experiment", ""]
    out += [f"{i}. **{s.step}** {s.purpose}{cite.refs(s.citations)}{warn(f'feasibility_plan.steps[{i - 1}]')}"
            for i, s in enumerate(fp.steps, 1)]
    out += ["", (f"**Reference measurements:** {fp.reference_measurements}"
                 f"{warn('feasibility_plan.reference_measurements')}"), "",
            f"**Decision basis:** {fp.decision_basis}{warn('feasibility_plan.decision_basis')}", ""]

    if a.assumptions:
        out += ["## Assumptions", ""] + [f"- {s}{warn(f'assumptions[{i}]')}" for i, s in enumerate(a.assumptions)]
        out.append("")
    if a.not_in_sources:
        out += ["## Not covered by the supplied sources", ""]
        out += [f"- {s}{warn(f'not_in_sources[{i}]')}" for i, s in enumerate(a.not_in_sources)] + [""]

    out += ["## Evidence (verified quotes)", ""]
    for i, c in enumerate(cite.entries, 1):
        precedent = scope.check(c.claim_kind, c.doc, c.page)[0] == "precedent_only"
        badge = "✓ (precedent only)" if precedent else "✓"
        out.append(f"{i}. {badge} **{kb.citation_label(c.doc, c.page)}** ({c.claim_kind.replace('_', ' ')}): "
                   f"\"{c.quote}\"")
    out.append("")

    s = r.report.summary()
    removed_citations = [x for x in r.removed if "citation" in x]
    changes = [x for x in r.removed if "citation" not in x]
    still_open = open_failures(r)
    out += ["## Verification", "",
            (f"- Citations verified: {s['citations_verified']} of {s['citations_total']} "
             f"(exact or whitespace/hyphen-tolerant match on the cited page, scope checked)."),
            (f"- Hard check failures before deterministic corrections: {s['hard_failures']}; still open: "
             f"{len(still_open)}; soft warnings: {s['soft_failures']}; repair rounds: {len(r.repairs)}.")]
    if removed_citations:
        out.append(f"- Removed {len(removed_citations)} citation(s) that failed verification:")
        out += [(f"  - ⚠ {x['location']}: {x['citation']['doc']} p.{x['citation']['page']} "
                 f"\"{x['citation']['quote'][:120]}\"") for x in removed_citations]
    if changes:
        out.append(f"- Corrected deterministically after verification ({len(changes)}):")
        out += [f"  - ⚠ {x['location']}: {x['reason']}" for x in changes]
    for c in still_open:
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
        "named_methods": r.named_methods,
        "slots": r.slots,
        "screening": [{"method": c.method, "technique": c.technique, "status": c.status, "reasons": c.reasons,
                       "warnings": c.warnings, "notes": c.notes} for c in r.candidates],
        "assessment": json.loads(r.assessment.model_dump_json()),
        "assessment_raw": json.loads(r.assessment_raw.model_dump_json()),
        "verification": r.report.to_dict(),
        "still_open": [{"name": c.name, "location": c.location, "message": c.message} for c in open_failures(r)],
        "removed_citations": [x for x in r.removed if "citation" in x],
        "finalize_changes": [x for x in r.removed if "citation" not in x],
        "flagged": r.flagged,
        "intake_removed": r.intake_removed,
        "repairs": r.repairs,
        "calls": r.calls,
        "timings_s": r.timings,
        "manifest": r.manifest,
    }
