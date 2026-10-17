"""Deterministic evaluation of saved runs (Phase 5.2): `uv run afs-assist eval`.

For every case of a scenario set it reads `outputs/<set>/<id>.json` + `.md` and scores a fixed
checklist of binary items, each mapped to one of the six judging criteria, plus the generic
`must` / `must_not` predicates a scenario may carry (the adversarial set does). No LLM or API
call anywhere; the optional Mermaid render runs mermaid-cli locally (`--mermaid`).

Results: "pass", "fail", "n/a" (the item does not apply to this run) or "not run" (no output).
`outputs/eval/summary.json` holds every evaluated set (a later run of one set replaces only that
set); `outputs/eval/summary.md` is rendered from it.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from collections.abc import Callable
from functools import cache
from pathlib import Path

from pydantic import ValidationError

from afs_assistant import paths, scenarios
from afs_assistant.options import option_citations, option_methods, option_parts
from afs_assistant.schema import Assessment
from afs_assistant.verify import (
    AFFECTS_WORDS,
    ANSWER_QUESTIONS,
    MAX_ANSWER_WORDS,
    MAX_OPTIONS,
    MAX_QUESTIONS,
    MIN_OPTIONS,
    MIN_STEP_WORDS,
    PLACEHOLDERS,
    _all_text,
    answer_texts,
    forbidden_hits,
    request_text,
)

SETS = ("dev", "adversarial")
PASS, FAIL, NA, NOT_RUN = "pass", "fail", "n/a", "not run"
CRITERIA = {          # the six judging criteria and their weights (master plan v3)
    "technical": "Technical quality (30)",
    "grounding": "AFS grounding (20)",
    "feasibility": "Feasibility plan (15)",
    "clarification": "Clarification and uncertainty (15)",
    "explainability": "Explainability (10)",
    "prototype": "Prototype (10)",
}
RUN_KEYS = ("run_id", "enquiry", "intake", "assessment", "verification", "still_open", "option_costs",
            "option_confidence", "setup_sketches", "flagged", "manifest")
# Markdown headings every assessed run needs (render.to_markdown); conditional ones are added per run.
HEADINGS = ("Answer", "Brief answer", "Proposal", "Setup sketch", "Expert detail", "Requirements",
            "Clarification questions", "Recommendation", "Measurement concept", "Spectral range",
            "Risks and uncertainty", "First feasibility experiment", "Evidence (verified quotes)", "Verification")
EXTERNAL_TITLE = "Secondary evidence (external, not AFS material)"
SUPPLIED_EVIDENCE = "Evidence (verified quotes)"
EXTERNAL_LABEL = re.compile(r"\bE\d+ ¶\d+")
ID_REF = re.compile(r"^[mo]\d+$", re.IGNORECASE)
DECIDING = ("method", "technique")          # question targets that can change the option choice
NO_METHOD_SUPPORT = ("auxiliary_sensor", "uncited_parameter")   # same rule as the external step (D-041)
CACHE_MISSING = "source text not in the local cache"


# ------------------------------------------------------------------ helpers
@cache
def _script(name: str):
    """Load scripts/<name>.py (the stand-alone checkers) so their logic is reused, not copied."""
    spec = importlib.util.spec_from_file_location(f"_afs_{name}", paths.ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@cache
def _table1() -> tuple:
    return tuple(json.loads(paths.TABLE1_FILE.read_text(encoding="utf-8"))["rows"])


def section(markdown: str, title: str) -> str | None:
    """The body under a heading (any level) up to the next heading; None when the heading is absent."""
    m = re.search(rf"^#+ {re.escape(title)}[^\n]*\n(.*?)(?=^#|\Z)", markdown, re.MULTILINE | re.DOTALL)
    return m.group(1) if m else None


def _empty(text: str | None) -> bool:
    return text is None or text.strip().lower() in PLACEHOLDERS


class Run:
    """One saved run: the JSON, the Markdown and the parsed assessment (None for an off-topic run)."""

    def __init__(self, data: dict, markdown: str, json_path: Path | None = None, md_path: Path | None = None):
        self.data, self.md, self.json_path, self.md_path = data, markdown, json_path, md_path
        self.off_topic = data.get("off_topic") is not None
        self.schema_error = None
        self.a: Assessment | None = None
        if not self.off_topic and data.get("assessment") is not None:
            try:
                self.a = Assessment.model_validate(data["assessment"])
            except ValidationError as exc:
                self.schema_error = f"assessment does not match the schema ({exc.error_count()} error(s))"

    @property
    def recs(self) -> dict:
        return {r.id: r for r in self.a.recommendations}

    @property
    def external(self) -> dict | None:
        return self.data.get("external")


Result = tuple[str, str]       # (pass|fail|n/a, reason)
_OFF = (NA, "off-topic run: no assessment")


def _ok(problems: list[str]) -> Result:
    return (FAIL, "; ".join(problems)) if problems else (PASS, "")


# ------------------------------------------------------------------ checklist items
def structured_output(run: Run) -> Result:
    missing = [k for k in RUN_KEYS if k not in run.data]
    if missing:
        return FAIL, f"run JSON lacks {missing}"
    if run.off_topic:
        return _ok([] if run.data["assessment"] is None else ["off-topic run carries an assessment"])
    if run.schema_error:
        return FAIL, run.schema_error
    return _ok([] if run.a is not None else ["no assessment and not marked off-topic"])


def sections_present(run: Run) -> Result:
    if run.a is None:
        return _OFF
    need = list(HEADINGS)
    need += ["Solution options"] if run.a.solution_options else []
    need += ["Key questions"] if run.a.clarification_questions else []
    need += ["Parameters"] if run.a.parameters else []
    need += ["Premise check"] if run.a.premise_checks else []
    missing = [h for h in need if section(run.md, h) is None]
    if "**Decision status:**" not in run.md.split("\n## Expert detail")[0]:
        missing.append("Decision status line in the Answer")
    return _ok([f"missing: {', '.join(missing)}"] if missing else [])


def citations_verified(run: Run) -> Result:
    if run.a is None:
        return _OFF
    s = run.data["verification"]["summary"]
    total, ok = s["citations_total"], s["citations_verified"]
    if total == 0:
        return FAIL, "no supplied-source citation at all"
    removed = len(run.data.get("removed_citations", []))
    return _ok([] if ok == total else [f"{ok}/{total} verified ({100 * ok / total:.0f} %); {removed} removed"])


def no_open_failures(run: Run) -> Result:
    if run.a is None:
        return _OFF
    return _ok([f"{c['name']} at {c['location']}" for c in run.data["still_open"]])


def no_flagged_figures(run: Run) -> Result:
    """Nothing finalize had to flag (unsupported figure, lost citation) and no open number check."""
    if run.a is None:
        return _OFF
    problems = [f"flagged {path}: {why}" for path, why in run.data["flagged"].items()]
    problems += [f"open {c['name']} at {c['location']}" for c in run.data["still_open"]
                 if c["name"].startswith("numbers_")]
    return _ok(problems)


def _without_enquiry(run: Run) -> str:
    """The Markdown without the customer's own words: the quoted `**Customer enquiry**` block and the
    Answer's `**Customer request:**` line when it is the enquiry verbatim (not the "our summary" line)."""
    md, enquiry = run.md, run.data.get("enquiry")
    if isinstance(enquiry, str) and enquiry.strip():
        md = md.replace(f"**Customer enquiry**\n\n> {enquiry}\n", "")
        md = md.replace(f"**Customer request:** {' '.join(enquiry.split())}\n", "")
    return md


def no_currency(run: Run) -> Result:
    cc = _script("check_cost_class")
    scanned = cc.EVIDENCE.sub("", _without_enquiry(run))
    hits = [scanned[max(0, m.start() - 30):m.end() + 30].replace("\n", " ") for m in cc.CURRENCY.finditer(scanned)]
    return _ok([f"currency: {h!r}" for h in hits[:3]])


def no_certainty_wording(run: Run) -> Result:
    """No guarantee, certainty, approval or readiness wording (the price words are `no_currency`)."""
    if run.a is None:
        return _OFF
    hits = [h for h in forbidden_hits(_all_text(run.a)) if not h.startswith("price")]
    return _ok(hits[:3])


def cost_class_table1(run: Run) -> Result:
    if run.a is None:
        return _OFF
    if run.json_path is None or run.md_path is None:
        return NA, "no files to cross-check"
    problems = [p for p in _script("check_cost_class").check_pair(run.json_path, run.md_path, list(_table1()))
                if not p.startswith("currency")]
    return _ok(problems[:3])


def options_rules(run: Run) -> Result:
    if run.a is None:
        return _OFF
    a, recs, problems = run.a, run.recs, []
    n = len(a.solution_options)
    if not MIN_OPTIONS <= n <= MAX_OPTIONS:
        problems.append(f"{n} options (need {MIN_OPTIONS}-{MAX_OPTIONS})")
    tiers = [o.tier for o in a.solution_options]
    if len(tiers) != len(set(tiers)):
        problems.append(f"tiers repeat {tiers}")
    if tiers.count("recommended") != 1:
        problems.append(f"{tiers.count('recommended')} recommended options")
    for o in a.solution_options:
        bad = [x for x in o.recommendation_ids if x not in recs or recs[x].role == "not_recommended"]
        if not o.recommendation_ids or bad:
            problems.append(f"{o.id} uses no valid recommendation {bad}")
        if o.tier == "extended" and _empty(o.fusion_note):
            problems.append(f"extended {o.id} has no fusion note")
        if o.tier == "extended" and len(option_methods(o, recs)) < 2:
            problems.append(f"extended {o.id} combines fewer than two methods")
    return _ok(problems)


def proposal_rules(run: Run) -> Result:
    if run.a is None:
        return _OFF
    a, pr, problems = run.a, run.a.proposal, []
    options = {o.id: o for o in a.solution_options}
    best = options.get(pr.best_current_option)
    if best is None:
        problems.append(f"best option {pr.best_current_option!r} is not an option")
    for name in ("what_would_change_it", "next_step"):
        if _empty(getattr(pr, name)):
            problems.append(f"{name} empty")
    if best is not None and pr.basis == "supplied" and not option_citations(best, run.recs):
        problems.append(f"basis 'supplied' but {best.id} has no citation")
    ext = run.external or {}
    items = {it["citation"]["label"]: it for it in ext.get("items", [])}
    access = {s["id"]: s.get("access") for s in ext.get("sources", [])}
    kinds = {g["id"]: g["kind"] for g in ext.get("gaps", [])}
    for label in ext.get("proposal_support", []):
        it = items.get(label)
        if it is None:
            problems.append(f"external support {label} is not a verified item")
        elif (it.get("option_id") != pr.best_current_option or access.get(it["citation"]["source_id"]) != "full_text"
              or kinds.get(it["gap_id"]) in NO_METHOD_SUPPORT):
            problems.append(f"external support {label} is not about the proposed option's method "
                            f"(gap {kinds.get(it['gap_id'])}, option {it.get('option_id')})")
    return _ok(problems)


def feasibility_plan(run: Run) -> Result:
    if run.a is None:
        return _OFF
    fp, problems = run.a.feasibility_plan, []
    real = [s for s in fp.steps if len(s.step.split()) >= MIN_STEP_WORDS]
    if len(real) < 2:
        problems.append(f"{len(real)} real step(s); need at least 2")
    if _empty(fp.reference_measurements):
        problems.append("no reference measurements")
    if _empty(fp.decision_basis):
        problems.append("no decision basis")
    return _ok(problems)


def premise_flags(run: Run) -> Result:
    """A premise, certainty or clinical enquiry gets a premise check; the status agrees with the verdicts."""
    if run.a is None:
        return _OFF
    intake, a = run.data["intake"], run.a
    triggers = bool(intake.get("customer_premises")) or bool(
        {"premise_to_check", "certainty_or_approval_requested", "clinical_context"} & set(intake.get("routes", [])))
    verdicts = [p.verdict for p in a.premise_checks]
    if not triggers and not verdicts:
        return NA, "no premise, certainty or clinical cue in the intake"
    problems = []
    if triggers and not verdicts:
        problems.append(f"intake routes {intake.get('routes')} but no premise check")
    if "contradicted" in verdicts and a.decision_status == "provisional_assessment":
        problems.append("a premise is contradicted but the status is provisional")
    if a.decision_status == "premise_not_supported" and "contradicted" not in verdicts:
        problems.append("premise_not_supported without a contradicted premise")
    return _ok(problems)


def questions_present(run: Run) -> Result:
    if run.a is None:
        return _OFF
    a, problems = run.a, []
    n = len(a.clarification_questions)
    if n == 0 and (a.key_unknowns or a.decision_status != "provisional_assessment"):
        problems.append("open unknowns or a non-provisional status but no clarification question")
    if n > MAX_QUESTIONS:
        problems.append(f"{n} questions (max {MAX_QUESTIONS})")
    shown = len(re.findall(r"^\d+\. ", section(run.md, "Key questions") or "", re.MULTILINE))
    if shown != min(n, ANSWER_QUESTIONS):
        problems.append(f"{shown} key question(s) in the Answer; expected {min(n, ANSWER_QUESTIONS)}")
    return _ok(problems)


def questions_tied_to_options(run: Run) -> Result:
    """Every question names what it affects; at least one top question can change the option choice."""
    if run.a is None:
        return _OFF
    a = run.a
    if not a.clarification_questions:
        return NA, "no clarification question"
    ids = {x.lower() for x in (*run.recs, *(o.id for o in a.solution_options))}
    in_options = {r.lower() for o in a.solution_options for r in o.recommendation_ids} | {
        o.id.lower() for o in a.solution_options}
    problems = []
    for q in a.clarification_questions:
        targets = [t.strip().lower() for t in q.affects]
        bad = [t for t in targets if t not in AFFECTS_WORDS and not (ID_REF.match(t) and t in ids)]
        if not targets or bad:
            problems.append(f"{q.id} affects {q.affects or 'nothing'}")
    top = a.clarification_questions[:ANSWER_QUESTIONS]
    if not any(t.strip().lower() in DECIDING or t.strip().lower() in in_options for q in top for t in q.affects):
        problems.append("no top question affects the method, technique or an option")
    return _ok(problems)


def answer_length(run: Run) -> Result:
    if run.a is None:
        return _OFF
    request = request_text(run.data["intake"].get("summary", ""), run.data["enquiry"])
    words = sum(len(t.split()) for t in answer_texts(run.a, request))
    return _ok([] if words <= MAX_ANSWER_WORDS else [f"{words} words of model text (soft target {MAX_ANSWER_WORDS})"])


def external_secondary(run: Run) -> Result:
    """External evidence sits only in its own secondary section, with quote and URL/DOI per item."""
    if run.a is None:
        return _OFF
    ext = run.external
    if not ext or not ext.get("items"):
        return NA, "no external item in this run"
    body, supplied = section(run.md, EXTERNAL_TITLE), section(run.md, SUPPLIED_EVIDENCE) or ""
    if body is None:
        return FAIL, f"no '{EXTERNAL_TITLE}' section"
    problems = []
    for it in ext["items"]:
        c = it["citation"]
        if c["label"] not in body:
            problems.append(f"{c['label']} not in the secondary section")
        if not c.get("quote", "").strip() or not (c.get("url") or c.get("doi")):
            problems.append(f"{c['label']} lacks its quote or URL/DOI")
    if EXTERNAL_LABEL.search(supplied):
        problems.append("an external label in the supplied-evidence list")
    basis = next((ln for ln in run.md.splitlines() if ln.startswith("- **Basis:**")), "")
    if EXTERNAL_LABEL.search(basis) and "not AFS material" not in basis:
        problems.append("proposal basis cites external support without 'not AFS material'")
    return _ok(problems)


def external_replay(run: Run, cache_root: Path | None = None) -> Result:
    """Every recorded external item whose source is in the local cache re-verifies offline to the same
    result (`afs-assist external replay`); items without cached text are listed, n/a only if none is cached."""
    if run.a is None:
        return _OFF
    ext = run.external
    if not ext or not (ext.get("items") or ext.get("dropped")):
        return NA, "no external item to replay"
    from afs_assistant.external import step

    rows = step.replay(ext, cache_root=cache_root)
    missing = [r for r in rows if r["replayed"] == CACHE_MISSING]
    cached = [r for r in rows if r["replayed"] != CACHE_MISSING]
    different = [r for r in cached if not r["equal"]]
    note = (f"{len(missing)}/{len(rows)} item(s) not checked, full text not in the local cache: "
            + ", ".join(r["item"] for r in missing[:3])) if missing else ""
    if different:
        return FAIL, "; ".join([f"{r['item']}: {r['recorded']} -> {r['replayed']}" for r in different[:3]]
                               + ([note] if note else []))
    if not cached:
        return NA, note
    return PASS, note


def off_topic_handled(run: Run) -> Result:
    if not run.off_topic:
        return NA, "not an off-topic run"
    ot, problems = run.data["off_topic"], []
    if not ot.get("message") or ot["message"] not in run.md:
        problems.append("redirect line missing")
    examples = [e for e in ot.get("examples", []) if e and e in run.md]
    if len(examples) < 2:
        problems.append(f"{len(examples)} example question(s) shown (need 2-3)")
    if run.data.get("assessment") is not None or run.external:
        problems.append("the pipeline ran past the intake")
    return _ok(problems)


def mermaid_renders(run: Run, enabled: bool = False) -> Result:
    if not enabled:
        return NA, "not requested (--mermaid)"
    if run.a is None:
        return _OFF
    cm = _script("check_mermaid")
    charts = cm.BLOCK.findall(run.md)
    if not charts:
        return FAIL, "no Mermaid chart"
    import shutil
    import tempfile

    if shutil.which("npx") is None:
        return NA, "npx not found"
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        ok, msg = cm.render("flowchart LR\n    a --> b", work, "smoke")
        if not ok:
            return NA, f"mermaid-cli cannot run here ({msg[:80]})"
        failed = [f"chart {i}: {m[:80]}" for i, c in enumerate(charts, 1)
                  for ok, m in [cm.render(c, work, f"c{i}")] if not ok]
    return _ok(failed)


# (id, criterion, what it checks, function)
CHECKLIST: list[tuple[str, str, str, Callable[..., Result]]] = [
    ("structured_output", "prototype", "run JSON has every key; the assessment matches the schema", structured_output),
    ("sections_present", "explainability", "Answer and Expert-detail sections all present", sections_present),
    ("citations_verified", "grounding", "100 % of supplied-source citations verified (at least one)",
     citations_verified),
    ("no_open_failures", "technical", "no hard verification failure left open", no_open_failures),
    ("no_flagged_figures", "grounding", "no flagged item or unsupported figure left", no_flagged_figures),
    ("no_currency", "technical", "no currency sign, code or word outside quoted evidence and the enquiry",
     no_currency),
    ("no_certainty_wording", "technical", "no guarantee, certainty, approval or readiness wording",
     no_certainty_wording),
    ("cost_class_table1", "technical", "every option's cost class matches S01 Table 1", cost_class_table1),
    ("options_rules", "technical", "2-3 options, distinct tiers, one recommended, extended = fusion note",
     options_rules),
    ("proposal_rules", "feasibility", "proposal names an option, change trigger, next step; support rules",
     proposal_rules),
    ("feasibility_plan", "feasibility", "at least two real plan steps, reference and decision basis",
     feasibility_plan),
    ("premise_flags", "clarification", "premise/certainty/clinical cues checked; status agrees", premise_flags),
    ("questions_present", "clarification", "questions when unknowns are open; top 3 in the Answer",
     questions_present),
    ("questions_tied_to_options", "clarification", "each question names what it affects; one changes the option",
     questions_tied_to_options),
    ("answer_length", "explainability", f"Answer model text within about {MAX_ANSWER_WORDS} words", answer_length),
    ("external_secondary", "grounding", "external items only in the secondary section, with quote and URL",
     external_secondary),
    ("external_replay", "grounding", "external items re-verify offline to the recorded result", external_replay),
    ("off_topic_handled", "prototype", "off-topic run: redirect line, example questions, no assessment",
     off_topic_handled),
    ("mermaid_renders", "prototype", "every Mermaid chart renders (optional, --mermaid)", mermaid_renders),
]


# ------------------------------------------------------------------ must / must_not predicates
TEXT_FIELDS = ("status_reason", "questions", "question_text", "first_question", "risks", "premises", "key_unknowns", "not_in_sources", "assumptions",
               "notes", "parameters", "options", "brief_answer", "proposal", "assessment")


def _field_text(a: Assessment, name: str) -> str:
    if name == "status_reason":
        return a.status_reason
    if name == "questions":
        return "\n".join(f"{q.question} {q.why_it_matters}" for q in a.clarification_questions)
    if name == "question_text":          # the questions only, without why_it_matters
        return "\n".join(q.question for q in a.clarification_questions)
    if name == "first_question":
        return a.clarification_questions[0].question if a.clarification_questions else ""
    if name == "risks":
        return "\n".join(r.risk for r in a.risks)
    if name == "premises":
        return "\n".join(f"{p.premise} {p.explanation}" for p in a.premise_checks)
    if name in ("key_unknowns", "not_in_sources", "assumptions"):
        return "\n".join(getattr(a, name))
    if name == "notes":
        return "\n".join(x for x in (a.chemometrics_note, a.realtime_tracking_note, a.future_direction) if x)
    if name == "parameters":
        return "\n".join(f"{p.name} {p.why}" for p in a.parameters)
    if name == "options":
        return "\n".join(" ".join(x for x in (o.ease_of_use, o.maintenance, o.performance_fit, o.cost_drivers,
                                              o.fusion_note) if x) for o in a.solution_options)
    if name == "brief_answer":
        return a.brief_answer
    if name == "proposal":
        return f"{a.proposal.what_would_change_it} {a.proposal.next_step}"
    if name == "assessment":
        return _all_text(a)
    raise ValueError(f"unknown text field {name!r}; use one of {TEXT_FIELDS}")


def predicate(run: Run, spec: dict) -> tuple[bool, str]:
    """Evaluate one generic predicate over a run: (holds, what was found)."""
    kind = spec["check"]
    if kind == "off_topic":
        return run.off_topic == spec.get("value", True), f"off_topic={run.off_topic}"
    if kind == "assessment_present":
        return run.a is not None, f"assessment {'present' if run.a is not None else 'absent'}"
    if kind == "route_in":
        routes = run.data.get("intake", {}).get("routes", [])
        return bool(set(routes) & set(spec["values"])), f"routes {routes}"
    if kind == "currency":
        hit = no_currency(run)[0] == FAIL
        return hit, "currency found" if hit else "no currency"
    if kind == "any_of":
        found = [predicate(run, s) for s in spec["items"]]
        return any(ok for ok, _ in found), " | ".join(d for _, d in found)
    if run.a is None:
        return False, "no assessment (off-topic run)"
    a = run.a
    if kind == "status_in":
        return a.decision_status in spec["values"], f"status {a.decision_status}"
    if kind in ("max_questions", "min_questions"):
        n = len(a.clarification_questions)
        return (n <= spec["n"] if kind == "max_questions" else n >= spec["n"]), f"{n} question(s)"
    if kind == "mentions":
        rx = re.compile(spec["pattern"], re.IGNORECASE)
        for name in spec["fields"]:
            m = rx.search(_field_text(a, name))
            if m:
                return True, f"{name}: {m.group(0)!r}"
        return False, f"no /{spec['pattern']}/ in {', '.join(spec['fields'])}"
    if kind == "parameter":
        rx = re.compile(spec.get("name", ""), re.IGNORECASE)
        types = set(spec.get("types", ["spectroscopy", "auxiliary_sensor", "reference_lab", "not_measurable_inline"]))
        found = [f"{p.name} ({p.measured_by.type})" for p in a.parameters if rx.search(p.name)]
        hits = [p for p in a.parameters if rx.search(p.name) and p.measured_by.type in types]
        return bool(hits), f"parameters {found or 'none matching'}"
    if kind == "premise_verdict_in":     # optional "pattern": only premises whose text matches it
        rx = re.compile(spec.get("pattern", ""), re.IGNORECASE)
        checks = [p for p in a.premise_checks if rx.search(f"{p.premise} {p.explanation}")]
        verdicts = [p.verdict for p in checks]
        shown = f"verdicts {verdicts}" + (f" of premises matching /{spec['pattern']}/" if spec.get("pattern") else "")
        return bool(set(verdicts) & set(spec["values"])), shown
    if kind in ("option_technique_in", "primary_technique_in"):
        recs = run.recs
        if kind == "option_technique_in":
            used = {t for o in a.solution_options for _, t in option_parts(o, recs) if t}
        else:
            used = {r.technique for r in a.recommendations if r.role == "primary"}
        return bool(used & set(spec["values"])), f"techniques {sorted(used)}"
    if kind == "extended_fusion":
        recs = run.recs
        ext = [o for o in a.solution_options if o.tier == "extended"]
        good = [o.id for o in ext if not _empty(o.fusion_note) and len(option_methods(o, recs)) >= 2]
        return bool(good), (f"extended {good} with fusion note" if good else
                            f"extended options {[o.id for o in ext]}, none with a fusion note and two methods")
    if kind == "primary_fused":
        fused = [r.id for r in a.recommendations if r.role == "primary" and r.combined_with]
        return bool(fused), f"fused primary {fused}" if fused else "primary is a single method"
    if kind == "forbidden_wording":
        hits = [h for h in forbidden_hits(_all_text(a)) if not h.startswith("price")]
        return bool(hits), "; ".join(hits[:2]) or "none"
    raise ValueError(f"unknown predicate {kind!r}")


def describe(spec: dict) -> str:
    """Short readable form of a predicate, for the summary."""
    args = {k: v for k, v in spec.items() if k not in ("check", "why")}
    if spec["check"] == "any_of":
        return "any of (" + "; ".join(describe(s) for s in spec["items"]) + ")"
    return spec["check"] + (" " + json.dumps(args, ensure_ascii=False) if args else "")


def _spec_text(spec: dict) -> str:
    try:
        return describe(spec)
    except Exception:  # noqa: BLE001 - a malformed spec still gets a row
        return json.dumps(spec, ensure_ascii=False, default=str)


# Predicates that read the run itself, not its assessment; every other predicate needs an assessment.
RUN_LEVEL_CHECKS = {"off_topic", "assessment_present", "route_in", "currency", "any_of"}


def scenario_items(run: Run, scenario: dict) -> list[dict]:
    """One row per must / must_not item; a predicate that raises fails that item only.

    A must_not on the assessment fails when there is no assessment (a wrong off-topic redirect),
    so it cannot pass vacuously."""
    out = []
    for kind in ("must", "must_not"):
        for spec in scenario.get(kind, []):
            try:
                holds, found = predicate(run, spec)
                ok = holds if kind == "must" else not holds
                if ok and kind == "must_not" and run.a is None and spec.get("check") not in RUN_LEVEL_CHECKS:
                    ok, found = False, "no assessment to check (off-topic run)"
            except Exception as exc:  # noqa: BLE001 - a malformed predicate or run fails the item, not the rest
                ok, found = False, f"check error: {type(exc).__name__}: {exc}"
            out.append({"kind": kind, "predicate": _spec_text(spec), "why": spec.get("why", ""),
                        "result": PASS if ok else FAIL, "reason": "" if ok else found, "found": found})
    return out


def failed_items(scenario: dict, reason: str) -> list[dict]:
    """Every must and must_not item as FAIL, for a run that cannot be evaluated."""
    return [{"kind": k, "predicate": _spec_text(s), "why": s.get("why", ""), "result": FAIL, "reason": reason,
             "found": reason} for k in ("must", "must_not") for s in scenario.get(k, [])]


# ------------------------------------------------------------------ evaluation of a set
def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def evaluate_case(scenario: dict, out_dir: Path, mermaid: bool = False, cache_root: Path | None = None) -> dict:
    sid = scenario["id"]
    case = {"id": sid, "title": scenario.get("title", ""), "status": "evaluated", "reason": "", "inputs": {},
            "checklist": {}, "scenario_items": []}
    json_path, md_path = out_dir / f"{sid}.json", out_dir / f"{sid}.md"
    missing = [p.name for p in (json_path, md_path) if not p.exists()]
    if missing:
        case.update(status=NOT_RUN, reason=f"missing {', '.join(missing)}")
        case["checklist"] = {item: {"result": NOT_RUN, "reason": ""} for item, *_ in CHECKLIST}
        case["scenario_items"] = [{"kind": k, "predicate": _spec_text(s), "why": s.get("why", ""), "result": NOT_RUN,
                                   "reason": "", "found": ""} for k in ("must", "must_not") for s in scenario.get(k, [])]
        return case
    case["inputs"] = {"json_sha256": _sha(json_path), "md_sha256": _sha(md_path)}
    try:
        run = Run(json.loads(json_path.read_text(encoding="utf-8")), md_path.read_text(encoding="utf-8"),
                  json_path, md_path)
    except (ValueError, AttributeError, TypeError, KeyError, OSError) as exc:
        run, reason = None, f"unreadable run JSON: {exc}"
    else:
        # An assessed run whose assessment is missing or off-schema cannot be judged: a must_not such as
        # `assessment_present` must not pass by accident, so it is treated like an unreadable run.
        reason = "" if run.off_topic or run.a is not None else (
            f"unreadable run: {run.schema_error or 'no assessment and not marked off-topic'}")
    if reason:
        case.update(status="error", reason=reason)
        case["checklist"] = {item: {"result": FAIL, "reason": reason} for item, *_ in CHECKLIST}
        case["scenario_items"] = failed_items(scenario, reason)
        return case
    for item, _, _, fn in CHECKLIST:
        try:
            if fn is mermaid_renders:
                result, reason = fn(run, mermaid)
            elif fn is external_replay:
                result, reason = fn(run, cache_root)
            else:
                result, reason = fn(run)
        except Exception as exc:  # noqa: BLE001 - a malformed run fails the item, never the harness
            result, reason = FAIL, f"check error: {type(exc).__name__}: {exc}"
        case["checklist"][item] = {"result": result, "reason": reason}
    case["scenario_items"] = scenario_items(run, scenario)
    return case


def _totals(cases: list[dict]) -> dict:
    per_item = {}
    for item, *_ in CHECKLIST:
        results = [c["checklist"][item]["result"] for c in cases]
        per_item[item] = {r: results.count(r) for r in (PASS, FAIL, NA, NOT_RUN)}
    per_criterion = {}
    for crit in CRITERIA:
        results = [c["checklist"][item]["result"] for item, cr, *_ in CHECKLIST if cr == crit for c in cases]
        per_criterion[crit] = {"pass": results.count(PASS), "applicable": results.count(PASS) + results.count(FAIL)}
    items = [x for c in cases for x in c["scenario_items"]]
    scen = {k: {"pass": sum(1 for x in items if x["kind"] == k and x["result"] == PASS),
                "fail": sum(1 for x in items if x["kind"] == k and x["result"] == FAIL),
                "not_run": sum(1 for x in items if x["kind"] == k and x["result"] == NOT_RUN)}
            for k in ("must", "must_not")}
    return {"cases": len(cases), "evaluated": sum(1 for c in cases if c["status"] == "evaluated"),
            "not_run": sum(1 for c in cases if c["status"] == NOT_RUN),
            "errors": sum(1 for c in cases if c["status"] == "error"), "per_item": per_item,
            "per_criterion": per_criterion, "scenario_items": scen}


def evaluate_set(set_name: str, out_dir: Path | None = None, mermaid: bool = False,
                 cache_root: Path | None = None, items: list[dict] | None = None) -> dict:
    out_dir = out_dir or paths.OUTPUTS / set_name
    items = scenarios.load(set_name) if items is None else items
    cases = [evaluate_case(s, out_dir, mermaid, cache_root) for s in items]
    try:
        shown = str(out_dir.resolve().relative_to(paths.ROOT))
    except ValueError:
        shown = str(out_dir)
    return {"outputs": shown, "mermaid": mermaid, "cases": cases, "totals": _totals(cases)}


# ------------------------------------------------------------------ summary files
def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


MARK = {PASS: "PASS", FAIL: "**FAIL**", NA: "–", NOT_RUN: "not run"}


def to_markdown(summary: dict) -> str:
    out = ["# Evaluation summary", "",
           ("Deterministic checklist over saved runs (`uv run afs-assist eval`); no model or API call. "
            "PASS / **FAIL** / – (not applicable) / not run (no output yet). Each item maps to one judging "
            "criterion; failures are listed with their reason below each table."), "",
           "## Checklist items", "", "| Item | Criterion | What it checks |", "|---|---|---|"]
    out += [f"| {item} | {CRITERIA[crit]} | {_cell(desc)} |" for item, crit, desc, _ in CHECKLIST]
    out.append("")
    for set_name in sorted(summary["sets"], key=lambda s: (SETS.index(s) if s in SETS else 99, s)):
        res = summary["sets"][set_name]
        cases, t = res["cases"], res["totals"]
        out += [f"## Set: {set_name}", "",
                (f"Outputs `{res['outputs']}`: {t['evaluated']} of {t['cases']} case(s) evaluated, "
                 f"{t['not_run']} not run, {t.get('errors', 0)} unreadable. Mermaid render {'checked' if res['mermaid'] else 'not checked'}."), ""]
        ids = [c["id"] for c in cases]
        out += ["| Item | " + " | ".join(ids) + " | Pass |", "|---|" + "---|" * len(ids) + "---|"]
        for item, *_ in CHECKLIST:
            counts = t["per_item"][item]
            applicable = counts[PASS] + counts[FAIL]
            out.append(f"| {item} | " + " | ".join(MARK[c["checklist"][item]["result"]] for c in cases)
                       + f" | {counts[PASS]}/{applicable} |")
        out += ["", "**Per criterion (passed / applicable item results):** "
                + "; ".join(f"{CRITERIA[c]} {v['pass']}/{v['applicable']}" for c, v in t["per_criterion"].items()), ""]
        fails = [(c["id"], item, v["reason"]) for c in cases for item, v in c["checklist"].items()
                 if v["result"] == FAIL]
        out += ["**Checklist failures:**", ""]
        out += [f"- {cid} · {item}: {_cell(reason)}" for cid, item, reason in fails] or ["- none"]
        not_run = [c for c in cases if c["status"] != "evaluated"]
        if not_run:
            out += ["", "**Not run / unreadable:** " + "; ".join(f"{c['id']} ({c['reason']})" for c in not_run)]
        out.append("")
        if any(c["scenario_items"] for c in cases):
            s = t["scenario_items"]
            out += [(f"**Per-enquiry checks:** must {s['must']['pass']} pass / {s['must']['fail']} fail / "
                     f"{s['must']['not_run']} not run; must-not {s['must_not']['pass']} pass / "
                     f"{s['must_not']['fail']} fail / {s['must_not']['not_run']} not run."), "",
                    "| Case | Kind | Check | Why | Result | Found |", "|---|---|---|---|---|---|"]
            for c in cases:
                for x in c["scenario_items"]:
                    out.append(f"| {c['id']} | {x['kind'].replace('_', '-')} | {_cell(x['predicate'])} | "
                               f"{_cell(x['why'])} | {MARK[x['result']]} | {_cell(x['found'])} |")
            out.append("")
    return "\n".join(out)


def write_summary(results: dict[str, dict], eval_dir: Path | None = None) -> dict:
    """Merge `results` (set -> evaluation) into summary.json (other sets kept) and render summary.md."""
    eval_dir = eval_dir or paths.OUTPUTS / "eval"
    eval_dir.mkdir(parents=True, exist_ok=True)
    json_path = eval_dir / "summary.json"
    summary = {"items": [], "sets": {}}
    if json_path.exists():
        try:
            summary = json.loads(json_path.read_text(encoding="utf-8"))
        except ValueError:
            pass
    summary["items"] = [{"id": item, "criterion": crit, "checks": desc} for item, crit, desc, _ in CHECKLIST]
    summary.setdefault("sets", {}).update(results)
    json_path.write_text(json.dumps(summary, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    (eval_dir / "summary.md").write_text(to_markdown(summary), encoding="utf-8")
    return summary
