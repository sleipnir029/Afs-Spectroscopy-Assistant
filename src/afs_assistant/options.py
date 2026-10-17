"""Code-derived fields of solution options (never written by the model).

Confidence per option (3.R item 4, D-022; calibrated in 3.R3, D-029): start at High and go
down one level for each named weakness (GRADE-style), floor Low; an open question on the
method caps it at Medium. IPCC-style qualitative wording. It rates the basis of the advice,
never a predicted accuracy or probability.

Cost class per option comes from the qualitative `cost` rating of S01 Table 1 (p.6)
for each method+technique the option uses: low < average < high; an option takes
the highest class of its rated rows. Only the in-line rows are used (the set the
screen evaluates). A combined method without its own entry takes the technique of another
recommendation with that method (3.R3 B6); otherwise the class is a lower bound ("at least").
A part without a Table 1 row is reported as not rated, never guessed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from afs_assistant import scope
from afs_assistant.schema import Assessment, Recommendation, SolutionOption
from afs_assistant.screen import SLOT_VALUES, UNKNOWN, Candidate, candidates

COST_ORDER = {"low": 0, "average": 1, "high": 2}
TABLE1_CITATION = "S01 Table 1 (p.6)"
NOT_RATED = "not rated in S01 Table 1"

# Technique labels for the reader; probe types that already name the method stand alone.
TECHNIQUE_LABEL = {
    "ATR": "ATR probe",
    "transmission_transflection": "transmission/transflection probe",
    "diffuse_reflection": "diffuse reflection probe",
    "diffuse_reflection_remote": "diffuse reflection at a distance",
    "raman_probe": "Raman probe",
    "fluorescence_probe": "fluorescence probe",
    "emission_probe": "emission probe (lens)",
    "combination": "combined probe",
    "to_be_determined": "technique to be determined",
}
_SELF_NAMED = {"raman_probe": "Raman", "fluorescence_probe": "Fluorescence"}


def method_label(method: str, technique: str | None) -> str:
    """'NIR, transmission/transflection probe'; 'Raman probe' (not 'Raman, raman probe')."""
    if technique is None:
        return f"{method} (technique not specified)"
    if _SELF_NAMED.get(technique) == method:
        return TECHNIQUE_LABEL[technique]
    return f"{method}, {TECHNIQUE_LABEL.get(technique, technique.replace('_', ' '))}"


def table1_rows(method: str, technique: str) -> list[dict]:
    """In-line S01 Table 1 rows for a method+technique, with their cost rating."""
    from afs_assistant import kb

    by_row = {r["row"]: r for r in kb.table1()}
    for c in candidates():
        if c.method == method and c.technique == technique:
            return [{"row": n, "method": method, "technique": technique, "cost": by_row[n]["cost"],
                     "table_technique": by_row[n]["measurement_technique"]} for n in c.table_rows]
    return []


@dataclass
class CostClass:
    cost_class: str | None                      # low | average | high | None (nothing rated)
    rows: list[dict] = field(default_factory=list)
    unrated: list[str] = field(default_factory=list)
    unidentified: list[str] = field(default_factory=list)   # combined methods whose Table 1 row is unknown

    def label(self) -> str:
        if self.cost_class is None:
            return NOT_RATED
        rows = ", ".join(str(r["row"]) for r in self.rows)
        text = f"{self.cost_class} cost (row{'s' if len(self.rows) > 1 else ''} {rows})"
        if self.unidentified:
            text = "at least " + text + "".join(f"; {m} row not identified" for m in self.unidentified)
        if self.unrated:
            text += f"; {NOT_RATED}: {', '.join(self.unrated)}"
        return text

    def to_dict(self) -> dict:
        return {"cost_class": self.cost_class, "label": self.label(), "citation": TABLE1_CITATION,
                "rows": self.rows, "unrated": self.unrated, "unidentified": self.unidentified}


def option_parts(option: SolutionOption, recs: dict[str, Recommendation]) -> list[tuple[str, str | None]]:
    """(method, technique) parts of an option; a combined method without its own entry has no technique."""
    used = [recs[i] for i in option.recommendation_ids if i in recs]
    parts: list[tuple[str, str | None]] = []
    for r in used:
        if (r.method, r.technique) not in parts:
            parts.append((r.method, r.technique))
    own_methods = {r.method for r in used}
    for r in used:
        for m in r.combined_with:
            if m not in own_methods and (m, None) not in parts:
                parts.append((m, None))
    return parts


def option_methods(option: SolutionOption, recs: dict[str, Recommendation]) -> list[str]:
    """Every method an option uses, including combined_with methods."""
    return list(dict.fromkeys(m for m, _ in option_parts(option, recs)))


def borrowed_rows(method: str, recs: dict[str, Recommendation]) -> list[dict]:
    """Table 1 rows for a combined method without its own entry in the option: the technique of
    the first other recommendation with that method that is recommended and has an in-line row."""
    for r in recs.values():
        if r.method == method and r.role != "not_recommended":
            found = table1_rows(r.method, r.technique)
            if found:
                return found
    return []


def cost_class(option: SolutionOption, recs: dict[str, Recommendation]) -> CostClass:
    """`recs` holds every recommendation of the assessment (a combined method may borrow a technique)."""
    rows: list[dict] = []
    unrated: list[str] = []
    unidentified: list[str] = []
    for method, technique in option_parts(option, recs):
        found = table1_rows(method, technique) if technique is not None else borrowed_rows(method, recs)
        if found:
            rows += [r for r in found if r["row"] not in {x["row"] for x in rows}]
        elif technique is None:
            unidentified.append(method)
        else:
            unrated.append(method_label(method, technique))
    if not rows:
        return CostClass(None, [], unrated + [method_label(m, None) for m in unidentified])
    top = max((r["cost"] for r in rows), key=COST_ORDER.__getitem__)
    return CostClass(top, sorted(rows, key=lambda r: r["row"]), unrated, unidentified)


def option_costs(a: Assessment) -> dict[str, dict]:
    recs = {r.id: r for r in a.recommendations}
    return {o.id: cost_class(o, recs).to_dict() for o in a.solution_options}


# ----------------------------------------------------------------- confidence (code-derived)
CONFIDENCE_LEVELS = ("High", "Medium", "Low")
CONFIDENCE_NOTE = ("Confidence rates the basis of the advice (how much is known and cited), not a predicted "
                   "accuracy or probability of success. It starts at High and drops one level per weakness listed "
                   "(floor Low); an open question on the method holds it at Medium at most.")
SLOT_PHRASE = {"physical_state": "physical state", "optical_regime": "sample clarity",
               "fluorophore": "fluorescent target", "aqueous": "water content",
               "heterogeneous": "sample homogeneity", "remote_distance": "distance to the analyzer"}
TABLE1_RULE = "S01 Table 1 (p.6)"


def _unknown_phrases(cand: Candidate, slots: dict) -> list[str]:
    """Short phrases for what keeps a candidate's screen result at `unknown`."""
    from afs_assistant import kb

    rules = {r["id"]: r for r in kb.rules()}
    phrases: list[str] = []
    for reason in cand.reasons:
        if reason["status"] != "unknown":
            continue
        if reason["rule"] == TABLE1_RULE:
            keys = ["physical_state", "optical_regime"]
            if reason["message"].startswith("dark"):
                phrases.append("diffuse reflection on a dark sample untested")
                continue
            if reason["message"].endswith("to be tested"):      # near-match sample type (3.R3 B2)
                phrases.append(reason["message"].rsplit("; ", 1)[-1])
                continue
        else:
            rule = rules.get(reason["rule"], {})
            keys = [k for k in (*rule.get("when", {}), *rule.get("target", {})) if k in SLOT_VALUES]
        open_slots = [SLOT_PHRASE[k] for k in keys if slots.get(k, UNKNOWN) == UNKNOWN]
        phrases += [f"{x} unknown" for x in open_slots] or ["suitability for this sample not confirmed"]
    return phrases


# Page scope tags that can carry a general statement about a method or component (page_scopes.yaml).
GENERAL_SCOPES = {"method", "component_spec", "guidance"}
OPEN_QUESTION_ANY = "method"     # a question that affects the method choice affects every option (3.R3 B3)


def _is_precedent(c) -> bool:
    """A citation is precedent when its claim kind or scope says so, or its page has no general tag
    (a 'general' citation to an example or study page is still only precedent; 3.R2 B1)."""
    from afs_assistant import kb

    page = kb.page(c.doc, c.page)
    tags = set(page["scope"]) if page else set()
    return (c.claim_kind == "application_precedent"
            or scope.check(c.claim_kind, c.doc, c.page)[0] == "precedent_only"
            or not tags & GENERAL_SCOPES)


def option_citations(option: SolutionOption, recs: dict[str, Recommendation]) -> list:
    """The citations of an option and of its recommendations, de-duplicated, order kept (3.R2 item 3).

    The confidence rating and the Sources cell use this same pool.
    """
    used = [recs[i] for i in option.recommendation_ids if i in recs]
    pool, seen = [], set()
    for c in [*option.citations, *(c for r in used for c in r.citations)]:
        key = (c.doc, c.page, c.quote)
        if key not in seen:
            seen.add(key)
            pool.append(c)
    return pool


def open_questions(a: Assessment, option: SolutionOption) -> list[str]:
    """Ids of the top clarification questions (as shown in the Answer) that affect the option."""
    from afs_assistant.verify import ANSWER_QUESTIONS, normalize_affects

    affected = {*option.recommendation_ids, OPEN_QUESTION_ANY}
    return [q.id for q in a.clarification_questions[:ANSWER_QUESTIONS]
            if affected & set(normalize_affects(q.affects)[0])]


def is_fusion(option: SolutionOption, recs: dict[str, Recommendation]) -> bool:
    """A data-fusion option: the extended tier, a fusion note, or a recommendation combined with
    another method. Two single methods side by side are a comparison, not fusion (3.R3 B4)."""
    used = [recs[i] for i in option.recommendation_ids if i in recs]
    return (option.tier == "extended" or bool(option.fusion_note and option.fusion_note.strip())
            or any(r.combined_with for r in used))


def confidence(a: Assessment, option: SolutionOption, cands: list[Candidate], slots: dict) -> dict:
    """{level, reasons}: High, minus one level per stacking rule that applies (each at most once),
    floor Low; an open top question on the option caps the level at Medium (3.R3 item 7).

    Every weakness is listed, the cap reason last. Runs on the finalized assessment, whose
    citations are all verified.
    """
    recs = {r.id: r for r in a.recommendations}
    by_key = {(c.method, c.technique): c for c in cands}
    reasons: list[str] = []

    # (a) A sample property that decides one of the option's methods is unknown, or the technique
    #     was not screened for this sample.
    unknown: list[str] = []
    for method, technique in option_parts(option, recs):
        if technique is not None:
            cand = by_key.get((method, technique))
            if cand is None:
                unknown.append("technique not screened for this sample")
            elif cand.status == "unknown":
                unknown += _unknown_phrases(cand, slots)
        else:   # a combined method without its own entry: open if none of its in-line candidates passes
            same = [c for c in cands if c.method == method]
            if not any(c.status == "pass" for c in same):
                for c in same:
                    if c.status == "unknown":
                        unknown += _unknown_phrases(c, slots)
    if unknown:
        reasons.append(", ".join(dict.fromkeys(unknown)))

    # (b) Only precedent citations, or no verified supplied-source citation, behind the option's methods.
    cits = option_citations(option, recs)
    if not cits:
        reasons.append("no verified source citation")
    elif all(_is_precedent(c) for c in cits):
        reasons.append("precedent only")

    # (c) Relies on a required parameter from an uncited auxiliary sensor or not measurable in-line
    #     (optional parameters do not count; 3.R3 item 7 undoes 3.R2 N5).
    params = {p.id: p for p in a.parameters}
    required = [params[i] for i in option.parameter_ids if i in params and params[i].necessity == "required"]
    weak = []
    if any(p.measured_by.type == "auxiliary_sensor" and not p.citations for p in required):
        weak.append("uncited auxiliary sensor")
    if any(p.measured_by.type == "not_measurable_inline" for p in required):
        weak.append("a parameter is not measurable in-line")
    if weak:
        reasons.append(" and ".join(weak))

    # A contradicted premise, or a status other than a provisional assessment.
    weak = []
    if any(p.verdict == "contradicted" for p in a.premise_checks):
        weak.append("a customer premise is contradicted")
    if a.decision_status != "provisional_assessment":
        weak.append(f"status: {a.decision_status.replace('_', ' ')}")
    if weak:
        reasons.append(", ".join(weak))

    # (d) Data fusion of two or more methods: the benefit is not shown yet (it must beat the best single method).
    if is_fusion(option, recs) and len(option_methods(option, recs)) >= 2:
        reasons.append("multi-method, fusion benefit not yet shown")

    level = min(len(reasons), len(CONFIDENCE_LEVELS) - 1)
    # An open top-3 question on the method or on the option's recommendations caps at Medium; it does not stack.
    questions = open_questions(a, option)
    if questions:
        reasons.append(f"open question: {', '.join(questions)} (at most Medium)")
        level = max(level, 1)
    return {"level": CONFIDENCE_LEVELS[level], "reasons": reasons}


def confidence_label(conf: dict) -> str:
    """'Medium: physical state unknown; precedent only' (High alone when nothing applies)."""
    return conf["level"] + (": " + "; ".join(conf["reasons"]) if conf["reasons"] else "")


def option_confidence(a: Assessment, cands: list[Candidate], slots: dict) -> dict[str, dict]:
    return {o.id: confidence(a, o, cands, slots) for o in a.solution_options}
