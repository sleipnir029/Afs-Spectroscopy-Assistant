"""Code-derived fields of solution options (never written by the model).

Confidence per option (3.R item 4, D-022): start at High and go down one level for each
named weakness (GRADE-style), floor Low; IPCC-style qualitative wording. It rates the basis
of the advice, never a predicted accuracy or probability.

Cost class per option comes from the qualitative `cost` rating of S01 Table 1 (p.6)
for each method+technique the option uses: low < average < high; an option takes
the highest class of its rated rows. Only the in-line rows are used (the set the
screen evaluates). A part without a Table 1 row is reported as not rated, never guessed.
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

    def label(self) -> str:
        if self.cost_class is None:
            return NOT_RATED
        rows = ", ".join(str(r["row"]) for r in self.rows)
        text = f"{self.cost_class} (row{'s' if len(self.rows) > 1 else ''} {rows})"
        if self.unrated:
            text += f"; {NOT_RATED}: {', '.join(self.unrated)}"
        return text

    def to_dict(self) -> dict:
        return {"cost_class": self.cost_class, "label": self.label(), "citation": TABLE1_CITATION,
                "rows": self.rows, "unrated": self.unrated}


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


def cost_class(option: SolutionOption, recs: dict[str, Recommendation]) -> CostClass:
    rows: list[dict] = []
    unrated: list[str] = []
    for method, technique in option_parts(option, recs):
        found = table1_rows(method, technique) if technique is not None else []
        if found:
            rows += [r for r in found if r["row"] not in {x["row"] for x in rows}]
        else:
            unrated.append(method_label(method, technique))
    if not rows:
        return CostClass(None, [], unrated)
    top = max((r["cost"] for r in rows), key=COST_ORDER.__getitem__)
    return CostClass(top, sorted(rows, key=lambda r: r["row"]), unrated)


def option_costs(a: Assessment) -> dict[str, dict]:
    recs = {r.id: r for r in a.recommendations}
    return {o.id: cost_class(o, recs).to_dict() for o in a.solution_options}


# ----------------------------------------------------------------- confidence (code-derived)
CONFIDENCE_LEVELS = ("High", "Medium", "Low")
CONFIDENCE_NOTE = ("Confidence rates the basis of the advice (how much is known and cited), not a predicted "
                   "accuracy or probability of success. It starts at High and drops one level per weakness listed.")
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
        else:
            rule = rules.get(reason["rule"], {})
            keys = [k for k in (*rule.get("when", {}), *rule.get("target", {})) if k in SLOT_VALUES]
        open_slots = [SLOT_PHRASE[k] for k in keys if slots.get(k, UNKNOWN) == UNKNOWN]
        phrases += [f"{x} unknown" for x in open_slots] or ["suitability for this sample not confirmed"]
    return phrases


def _is_precedent(c) -> bool:
    return c.claim_kind == "application_precedent" or scope.check(c.claim_kind, c.doc, c.page)[0] == "precedent_only"


def confidence(a: Assessment, option: SolutionOption, cands: list[Candidate], slots: dict) -> dict:
    """{level, reasons}: High, minus one level per rule that applies (each rule at most once), floor Low.

    Runs on the finalized assessment, whose citations are all verified.
    """
    recs = {r.id: r for r in a.recommendations}
    used = [recs[i] for i in option.recommendation_ids if i in recs]
    by_key = {(c.method, c.technique): c for c in cands}
    reasons: list[str] = []

    # 1. A sample property that decides one of the option's methods is unknown.
    unknown: list[str] = []
    for method, technique in option_parts(option, recs):
        if technique is not None:
            cand = by_key.get((method, technique))
            if cand is not None and cand.status == "unknown":
                unknown += _unknown_phrases(cand, slots)
        else:   # a combined method without its own entry: open if none of its in-line candidates passes
            same = [c for c in cands if c.method == method]
            if not any(c.status == "pass" for c in same):
                for c in same:
                    if c.status == "unknown":
                        unknown += _unknown_phrases(c, slots)
    if unknown:
        reasons.append(", ".join(dict.fromkeys(unknown)))

    # 2. Only precedent citations, or no verified supplied-source citation, behind the option's methods.
    cits = [*option.citations, *(c for r in used for c in r.citations)]
    if not cits:
        reasons.append("no verified source citation")
    elif all(_is_precedent(c) for c in cits):
        reasons.append("precedent only")

    # 3. Relies on an uncited auxiliary sensor or a parameter not measurable in-line.
    params = {p.id: p for p in a.parameters}
    required = [params[i] for i in option.parameter_ids if i in params and params[i].necessity == "required"]
    weak = []
    if any(p.measured_by.type == "auxiliary_sensor" and not p.citations for p in required):
        weak.append("uncited auxiliary sensor")
    if any(p.measured_by.type == "not_measurable_inline" for p in required):
        weak.append("a required parameter is not measurable in-line")
    if weak:
        reasons.append(" and ".join(weak))

    # 4. A contradicted premise, or a status other than a provisional assessment.
    weak = []
    if any(p.verdict == "contradicted" for p in a.premise_checks):
        weak.append("a customer premise is contradicted")
    if a.decision_status != "provisional_assessment":
        weak.append(f"status: {a.decision_status.replace('_', ' ')}")
    if weak:
        reasons.append(", ".join(weak))

    # 5. Multi-method: the fusion benefit is not shown yet (it must beat the best single method).
    if len(option_methods(option, recs)) >= 2:
        reasons.append("multi-method, fusion benefit not yet shown")

    level = CONFIDENCE_LEVELS[min(len(reasons), len(CONFIDENCE_LEVELS) - 1)]
    return {"level": level, "reasons": reasons}


def confidence_label(conf: dict) -> str:
    """'Medium: physical state unknown; precedent only' (High alone when nothing applies)."""
    return conf["level"] + (": " + "; ".join(conf["reasons"]) if conf["reasons"] else "")


def option_confidence(a: Assessment, cands: list[Candidate], slots: dict) -> dict[str, dict]:
    return {o.id: confidence(a, o, cands, slots) for o in a.solution_options}
