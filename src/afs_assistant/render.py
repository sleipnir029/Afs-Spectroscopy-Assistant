"""Render a pipeline run as Markdown and JSON.

Two layers (D-022): a short Answer part (request, brief answer, proposal, options table,
setup sketch, top questions) and an Expert detail part with everything else.
Code-derived parts (never model text): the cost class per option (S01 Table 1), the
confidence rating per option, the auxiliary-sensor label, the not-measurable-in-line
wording and the Mermaid setup sketch.
"""

from __future__ import annotations

import json
import re

from afs_assistant import kb, scope
from afs_assistant.fibers import method_fiber_coverage
from afs_assistant.numbers import unsupported_numbers
from afs_assistant.options import (
    CONFIDENCE_NOTE,
    TABLE1_CITATION,
    confidence,
    confidence_label,
    cost_class,
    is_fusion,
    method_label,
    option_citations,
    option_confidence,
    option_costs,
    option_parts,
)
from afs_assistant.pipeline import RunResult
from afs_assistant.schema import Assessment, Parameter, SolutionOption
from afs_assistant.verify import (
    ANSWER_QUESTIONS,
    RECHECK_NAMES,
    forbidden_hits,
    request_text,
)

STATUS_LABEL = {
    "provisional_assessment": "Provisional feasibility assessment",
    "insufficient_information": "Insufficient information for a method choice",
    "premise_not_supported": "Premise not supported by the sources",
    "outside_supported_scope": "Outside the supported scope",
}
ROLE_LABEL = {"primary": "Primary candidate", "comparison": "Comparison candidate",
              "conditional": "Conditional candidate", "not_recommended": "Not recommended"}
TIER_LABEL = {"simple": "Simple", "recommended": "Recommended", "extended": "Extended (multi-method)"}
BASIS_LABEL = {"supplied": "supplied AFS sources", "engineering_judgement": "engineering judgement"}
AUX_UNCITED = "engineering judgement: confirm availability with AFS"
AUX_CITED = "cited; confirm availability with AFS"   # a citation supports the point, not the sensor supply
NOTE_LABEL = {"chemometrics_note": "Chemometrics", "realtime_tracking_note": "Real-time tracking",
              "future_direction": "Future direction"}
# Mermaid label escapes (entity codes); '#' first so the codes themselves are not escaped again.
_MERMAID_ESCAPES = [("#", "#35;"), ('"', "#quot;"), ("[", "#91;"), ("]", "#93;"), ("|", "#124;"),
                    ("<", "#lt;"), (">", "#gt;"), ("{", "#123;"), ("}", "#125;"), ("`", "#96;")]
MERMAID_LABEL_CHARS = 60
# A step text that starts with its own number ("1." / "1)") would show the number twice in the list.
_STEP_NUMBER = re.compile(r"^\s*\d+[.)](?!\d)\s*")   # not a decimal such as "1.5 mm"


class _Citer:
    """Numbers citations in order of appearance and collects them for the evidence list.

    An identical quote (same document, page and text) keeps its first number (3.R3 item 8)."""

    def __init__(self) -> None:
        self.entries: list = []
        self._numbers: dict[tuple, int] = {}

    def refs(self, citations) -> str:
        if not citations:
            return " *(no verified source: engineering judgement)*"
        marks = []
        for c in citations:
            key = (c.doc, c.page, c.quote)
            if key not in self._numbers:
                self.entries.append(c)
                self._numbers[key] = len(self.entries)
            marks.append(f"[{self._numbers[key]}: {kb.citation_label(c.doc, c.page)}]")
        return " " + " ".join(marks)


def open_failures(r: RunResult) -> list:
    """Hard failures still open after finalize: removed citations and deterministic corrections are not.

    Option, proposal, primary and premise-basis checks take their open state from the
    re-run on the finalized assessment (`r.recheck`).
    """
    corrected = {x["corrects"] for x in r.removed if "citation" not in x and "corrects" in x}
    kept = [c for c in r.report.hard_failures
            if c.name not in ("quote_verified", "citation_scope") and c.name not in corrected
            and c.name not in RECHECK_NAMES]
    return kept + list(r.recheck)


def _cell(text: str) -> str:
    """Text safe for one Markdown table cell."""
    return " ".join(str(text).split()).replace("|", "\\|")


def mermaid_escape(text: str) -> str:
    text = " ".join(str(text).split())
    for old, new in _MERMAID_ESCAPES:
        text = text.replace(old, new)
    return text


def _short(text: str, limit: int = MERMAID_LABEL_CHARS) -> str:
    text = " ".join(str(text).split())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    return (cut or text[:limit]).rstrip(",;:.") + "…"


def fiber_label(method: str, slots: dict) -> str:
    """Fiber family for a method: the proposed one, else the families covering its range (S02 p.6)."""
    proposed = slots.get("proposed_fiber")
    if proposed and proposed.get("for_method") == method:
        return f"Fiber: {proposed['family'].replace('_', ' ')} (proposed)"
    families = list(dict.fromkeys(c.family.replace("_", " ") for c in method_fiber_coverage(method)
                                  if c.status != "none"))
    return f"Fiber: {' or '.join(families) if families else 'to be selected'} (S02 p.6)"


def _aux_cited(p: Parameter) -> bool:
    """Citations left after finalize are verified ones."""
    return bool(p.citations)


def measured_by_text(p: Parameter) -> str:
    """Code wording for how a parameter is measured; auxiliary sensors always keep the AFS label."""
    mb = p.measured_by
    if mb.type == "spectroscopy":
        return f"Spectroscopy: {mb.method or 'method not named'}"
    if mb.type == "auxiliary_sensor":
        label = f"Auxiliary sensor: {mb.sensor or 'not named'}"
        return f"{label} ({AUX_CITED})" if _aux_cited(p) else f"{label} ({AUX_UNCITED})"
    if mb.type == "reference_lab":
        return f"Reference lab method: {mb.sensor or 'not named'}"
    return f"Not measurable in-line by spectroscopy; alternative: {mb.alternative or 'none named'}"


def mermaid_chart(a: Assessment, option: SolutionOption, slots: dict) -> str:
    """flowchart LR: process point -> probe -> fiber -> spectrometer -> model -> result; aux sensors dashed.

    One data fusion model only for a fusion option (`is_fusion`); otherwise one chemometric model
    per spectrometer (two methods side by side are a comparison, 3.R3 B4)."""
    recs = {r.id: r for r in a.recommendations}
    params = {p.id: p for p in a.parameters}
    used = [params[i] for i in option.parameter_ids if i in params]
    nodes = [("proc", f"Process point: {a.measurement_concept.location}")]
    edges = []
    parts = option_parts(option, recs)
    fused = len(parts) <= 1 or is_fusion(option, recs)
    models = ["model"] if fused else [f"model{k}" for k in range(1, len(parts) + 1)]
    for k, (method, technique) in enumerate(parts, 1):
        model = "model" if fused else f"model{k}"
        nodes += [(f"probe{k}", method_label(method, technique)), (f"fiber{k}", fiber_label(method, slots)),
                  (f"spec{k}", f"{method} spectrometer")]
        edges += [f"proc --> probe{k}", f"probe{k} --> fiber{k}", f"fiber{k} --> spec{k}", f"spec{k} --> {model}"]
        if not fused:
            nodes.append((model, f"Chemometric model ({method})"))
    if fused:
        nodes.append(("model", "Chemometric model" if len(parts) <= 1
                      else "Data fusion model (per-method calibration)"))
    spectro = [p.name for p in used if p.measured_by.type == "spectroscopy"] or [p.name for p in used]
    nodes.append(("result", "Result: " + (", ".join(spectro) if spectro else "measured parameters")))
    edges += [f"{m} --> result" for m in models]
    aux = [p for p in used if p.measured_by.type == "auxiliary_sensor"]
    for k, p in enumerate(aux, 1):
        nodes.append((f"aux{k}", f"Auxiliary: {p.measured_by.sensor or p.name} (confirm with AFS)"))
        edges += [f"aux{k} -.-> {m}" for m in models]
    lines = ["flowchart LR"]
    lines += [f'    {nid}["{mermaid_escape(_short(label))}"]' for nid, label in nodes]
    lines += [f"    {e}" for e in edges]
    return "\n".join(lines)


def setup_charts(r: RunResult) -> list[tuple[SolutionOption, str]]:
    """The recommended option's chart, then the extended option's (if any)."""
    a = r.assessment
    charts = []
    for tier in ("recommended", "extended"):
        option = next((o for o in a.solution_options if o.tier == tier), None)
        if option is not None:
            charts.append((option, mermaid_chart(a, option, r.slots)))
    return charts


def _option_methods_text(option: SolutionOption, a: Assessment) -> str:
    recs = {x.id: x for x in a.recommendations}
    items = []
    for rid in option.recommendation_ids:
        rec = recs.get(rid)
        if rec is None:
            items.append(f"{rid} (missing)")
            continue
        combo = f" + {', '.join(rec.combined_with)} (combination)" if rec.combined_with else ""
        items.append(f"{rid} {method_label(rec.method, rec.technique)}{combo}")
    return "; ".join(items) or "none"


def request_line(r: RunResult) -> str:
    """The customer request in one line (`verify.request_text`, which the answer_length check counts)."""
    return request_text(r.intake.summary, r.enquiry)


def request_label(r: RunResult) -> str:
    """'Customer request (our summary)' for the intake summary; the enquiry text itself needs no note."""
    summary = " ".join(r.intake.summary.split())
    return "Customer request (our summary)" if summary and request_line(r) == summary else "Customer request"


def _intake_text(text: str, quote: str, enquiry: str) -> str:
    """Model wording of an intake item, unless it adds a figure or forbidden wording; then its enquiry quote."""
    text = " ".join(text.split())
    return quote if unsupported_numbers(text, [enquiry]) or forbidden_hits(text) else text


def stated_from_intake(r: RunResult) -> list[str]:
    """The intake's verified facts and targets, for when the assessment states no requirement (3.R3 B5)."""
    items = [_intake_text(f.text, f.enquiry_quote, r.enquiry) for f in r.intake.facts_stated]
    items += [_intake_text(f"Target: {t.variable} ({t.purpose})", t.enquiry_quote, r.enquiry)
              for t in r.intake.targets]
    return items


def to_markdown(r: RunResult, title: str = "") -> str:
    a = r.assessment
    cite = _Citer()

    def warn(path: str) -> str:
        """Inline warning for an item finalize flagged (lost a citation, unsupported figure)."""
        return f" ⚠ *({r.flagged[path]})*" if path in r.flagged else ""

    # ================================================================ Answer
    out = [f"# First technical assessment{': ' + title if title else ''}", "", "## Answer", ""]
    still_open = open_failures(r)
    if still_open:
        out += [f"⚠ {len(still_open)} verification check(s) still open; see Verification.", ""]
    out += [f"**{request_label(r)}:** {request_line(r)}", ""]
    out += ["### Brief answer", "", f"{a.brief_answer}{warn('brief_answer')}", ""]

    options = {o.id: o for o in a.solution_options}
    pr = a.proposal
    best = options.get(pr.best_current_option)
    best_text = f"{best.id} ({best.tier})" if best else "(invalid option id)"   # the table names the methods
    out += ["### Proposal", "",
            f"- **Best current option:** {best_text}{warn('proposal')}",
            f"- **Basis:** {BASIS_LABEL[pr.basis]}",
            f"- **What would change it:** {pr.what_would_change_it}{warn('proposal.what_would_change_it')}",
            f"- **Next step:** {pr.next_step}{warn('proposal.next_step')}", ""]
    out += [f"**Decision status:** {STATUS_LABEL[a.decision_status]}", ""]     # the reason is in Expert detail

    if a.solution_options:
        recs = {x.id: x for x in a.recommendations}
        out += ["### Solution options", "",
                (f"| ID | Tier | Methods | Confidence | Cost class, {TABLE1_CITATION} | Ease of use | Maintenance | "
                 f"Performance fit | Sources |"), "|---|---|---|---|---|---|---|---|---|"]
        for i, o in enumerate(a.solution_options):
            conf = confidence(a, o, r.candidates, r.slots)    # per index: ids may repeat (still open then)
            out.append(f"| {_cell(o.id)} | {TIER_LABEL[o.tier]} | {_cell(_option_methods_text(o, a))} | "
                       f"{_cell(confidence_label(conf))} | {_cell(cost_class(o, recs).label())} | "
                       f"{_cell(o.ease_of_use)} | {_cell(o.maintenance)} | "
                       f"{_cell(o.performance_fit)}{_cell(warn(f'solution_options[{i}]'))} | "
                       f"{_cell(cite.refs(option_citations(o, recs)))} |")
        out += ["", f"*{CONFIDENCE_NOTE}*", "",
                (f"*Cost class is the relative rating in {TABLE1_CITATION} for the in-line method+technique "
                 f"rows named (the highest one for a multi-method option); it is not a price.*"), ""]

    def sketch(o: SolutionOption, chart: str) -> list[str]:
        return [(f"*{TIER_LABEL[o.tier]} option {o.id}; drawn by code from the option, a schematic, "
                 f"not a configuration.*"), "", "```mermaid", chart, "```", ""]

    charts = setup_charts(r)
    answer_charts = [(o, c) for o, c in charts if o.tier == "recommended"]
    out += ["### Setup sketch", ""]
    if not answer_charts:
        out += ["No recommended option, so no setup sketch.", ""]
    for o, chart in answer_charts:
        out += sketch(o, chart)

    top = a.clarification_questions[:ANSWER_QUESTIONS]
    if top:
        out += ["### Key questions", ""]
        out += [f"{k}. {q.question}{warn(f'clarification_questions[{k - 1}]')}" for k, q in enumerate(top, 1)]
        out.append("")

    # ================================================================ Expert detail
    out += ["## Expert detail", "", "**Customer enquiry**", "", f"> {r.enquiry}", ""]
    out += [f"**Decision status:** {STATUS_LABEL[a.decision_status]}. {a.status_reason}{warn('status_reason')}", ""]

    if a.parameters:
        out += ["### Parameters", "", "| ID | Parameter | Kind | Need | Measured by | Why | Sources |",
                "|---|---|---|---|---|---|---|"]
        for i, p in enumerate(a.parameters):
            out.append(f"| {_cell(p.id)} | {_cell(p.name)} | {p.kind} | {p.necessity} | "
                       f"{_cell(measured_by_text(p))} | {_cell(p.why)}{_cell(warn(f'parameters[{i}]'))} | "
                       f"{_cell(cite.refs(p.citations))} |")
        out.append("")

    if a.solution_options:
        out += ["### Solution option details", ""]
        for o in a.solution_options:
            out.append(f"- **{o.id} cost drivers:** {o.cost_drivers}")
            if o.fusion_note:
                out.append(f"- **{o.id} combining methods:** {o.fusion_note}")
        out.append("")
        for o, chart in charts:
            if o.tier != "recommended":          # the extended sketch is expert detail (3.R3 item 8)
                out += sketch(o, chart)

    if a.premise_checks:
        out += ["### Premise check", ""]
        for i, p in enumerate(a.premise_checks):
            out.append(f"- **{p.verdict.replace('_', ' ').capitalize()}:** {p.premise.rstrip().rstrip('.')}. "
                       f"{p.explanation}{cite.refs(p.citations)}{warn(f'premise_checks[{i}]')}")
        out.append("")

    out += ["### Requirements", "", "**Stated by the customer**", ""]
    out += [f"- {s}{warn(f'requirements_stated[{i}]')}" for i, s in enumerate(a.requirements_stated)]
    if not a.requirements_stated:
        out += [f"- {s}" for s in stated_from_intake(r)]
    out += ["", "**Key unknowns**", ""]
    out += [f"- {s}{warn(f'key_unknowns[{i}]')}" for i, s in enumerate(a.key_unknowns)] + [""]

    out += ["### Clarification questions (most decision-relevant first)", ""]
    for i, q in enumerate(a.clarification_questions):
        out.append(f"{q.id}. {q.question} *Why it matters:* {q.why_it_matters} *(affects: {', '.join(q.affects)})*"
                   f"{warn(f'clarification_questions[{i}]')}")
    out.append("")

    out += ["### Recommendation", ""]
    for i, m in enumerate(a.recommendations):
        cond = "" if m.conditions.strip().lower() in ("", "none") else f" *Conditions:* {m.conditions}"
        # A combination shows in the headline; it stays a later hypothesis after the single-method tests.
        combo = f" + {', '.join(m.combined_with)} (combination)" if m.combined_with else ""
        later = " Later hypothesis, after single-method tests." if m.combined_with else ""
        out.append(f"- **{m.id} · {ROLE_LABEL[m.role]}: {method_label(m.method, m.technique)}{combo}.** "
                   f"{m.rationale}{cond}{cite.refs(m.citations)}{later}{warn(f'recommendations[{i}]')}")
    out.append("")

    mc = a.measurement_concept
    out += ["### Measurement concept", "",
            f"- **Probe and geometry:** {mc.probe_and_geometry}",
            f"- **Location:** {mc.location}",
            f"- **Fiber link:** {mc.fiber_link}{cite.refs(mc.citations)}{warn('measurement_concept')}", ""]

    out += ["### Spectral range", ""]
    out += [f"- **{s.method}:** {s.statement}{cite.refs(s.citations)}{warn(f'spectral_ranges[{i}]')}"
            for i, s in enumerate(a.spectral_ranges)] + [""]

    out += ["### Risks and uncertainty", ""]
    for i, k in enumerate(a.risks):
        rules = f" *(rules: {', '.join(k.rule_ids)})*" if k.rule_ids else ""
        out.append(f"- {k.risk}{rules}{cite.refs(k.citations)}{warn(f'risks[{i}]')}")
    out.append("")

    fp = a.feasibility_plan
    out += ["### First feasibility experiment", ""]
    out += [f"{i}. **{_STEP_NUMBER.sub('', s.step)}** {s.purpose}{cite.refs(s.citations)}{warn(f'feasibility_plan.steps[{i - 1}]')}"
            for i, s in enumerate(fp.steps, 1)]
    out += ["", (f"**Reference measurements:** {fp.reference_measurements}"
                 f"{warn('feasibility_plan.reference_measurements')}"), "",
            f"**Decision basis:** {fp.decision_basis}{warn('feasibility_plan.decision_basis')}", ""]

    if a.assumptions:
        out += ["### Assumptions", ""] + [f"- {s}{warn(f'assumptions[{i}]')}" for i, s in enumerate(a.assumptions)]
        out.append("")
    if a.not_in_sources:
        out += ["### Not covered by the supplied sources", ""]
        out += [f"- {s}{warn(f'not_in_sources[{i}]')}" for i, s in enumerate(a.not_in_sources)] + [""]

    notes = [(NOTE_LABEL[n], getattr(a, n), n) for n in NOTE_LABEL if getattr(a, n)]
    if notes:
        out += ["### Further notes", ""] + [f"- **{label}:** {text}{warn(n)}" for label, text, n in notes] + [""]

    out += ["### Evidence (verified quotes)", ""]
    for i, c in enumerate(cite.entries, 1):
        precedent = scope.check(c.claim_kind, c.doc, c.page)[0] == "precedent_only"
        badge = "✓ (precedent only)" if precedent else "✓"
        out.append(f"{i}. {badge} **{kb.citation_label(c.doc, c.page)}** ({c.claim_kind.replace('_', ' ')}): "
                   f"\"{c.quote}\"")
    out.append("")

    s = r.report.summary()
    removed_citations = [x for x in r.removed if "citation" in x]
    changes = [x for x in r.removed if "citation" not in x]
    out += ["### Verification", "",
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
    intake_removed = [x for x in r.intake_removed if not x.get("placeholder")]
    if intake_removed:
        out.append(f"- Removed {len(intake_removed)} intake item(s) not quoted verbatim from the enquiry:")
        out += [f"  - {x['location']}: {x['reason']}" for x in intake_removed]
    # The API cost stays in the run JSON and manifest: no currency sign in any Markdown output.
    out += ["", f"*Run {r.run_id} · models {', '.join(r.manifest.get('models', []))}*", ""]
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
        "option_costs": option_costs(r.assessment),
        "option_confidence": option_confidence(r.assessment, r.candidates, r.slots),
        "setup_sketches": {o.id: chart for o, chart in setup_charts(r)},
        "removed_citations": [x for x in r.removed if "citation" in x],
        "finalize_changes": [x for x in r.removed if "citation" not in x],
        "flagged": r.flagged,
        "intake_removed": r.intake_removed,
        "repairs": r.repairs,
        "calls": r.calls,
        "timings_s": r.timings,
        "manifest": r.manifest,
    }
