"""Code-derived fields of solution options (never written by the model).

Cost class per option comes from the qualitative `cost` rating of S01 Table 1 (p.6)
for each method+technique the option uses: low < average < high; an option takes
the highest class of its rated rows. Only the in-line rows are used (the set the
screen evaluates). A part without a Table 1 row is reported as not rated, never guessed.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from afs_assistant.schema import Assessment, Recommendation, SolutionOption
from afs_assistant.screen import candidates

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
