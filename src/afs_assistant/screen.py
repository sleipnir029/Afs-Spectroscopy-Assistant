"""Deterministic screening of method x technique candidates (AFS-Ashby step 3).

Hard constraints come from S01 Table 1 (sample types per technique) and from the
`exclude` / `require` rules in knowledge/rules.yaml. An unknown slot never fails a
candidate: it yields status "unknown" so the gap becomes a question, not a verdict.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from afs_assistant import kb
from afs_assistant.fibers import METHOD_RANGES_UM, coverage

UNKNOWN = "unknown"

# S01 Table 1 method names -> canonical method ids.
METHOD_IDS = {
    "IR spectroscopy": "MIR",
    "NIR spectroscopy": "NIR",
    "Raman spectroscopy": "Raman",
    "UV/Visible spectroscopy": "UV-Vis",
    "Fluorimetry": "Fluorescence",
}

# S01 Table 1 measurement techniques -> canonical technique ids; `in_line` marks
# fiber-probe techniques usable at a process point (cuvettes, films, spheres are lab set-ups).
TECHNIQUES = {
    "ATR platform": ("ATR", False),
    "ATR probe*": ("ATR", True),
    "ATR probe": ("ATR", True),
    "cuvette": ("cuvette", False),
    "cuvette 90 deg": ("cuvette", False),
    "sample layer": ("thin_film_transmission", False),
    "sample surface": ("diffuse_reflection", False),
    "transmission or transflection probe": ("transmission_transflection", True),
    "diffuse reflection probe": ("diffuse_reflection", True),
    "integrating sphere": ("diffuse_reflection", False),
    "surface at a distance": ("diffuse_reflection_remote", True),
    "Raman probe": ("raman_probe", True),
    "probe, lens": ("emission_probe", True),
    "fluorimetric probe": ("fluorescence_probe", True),
}

# Our mapping from the two sample slots to the S01 Table 1 sample-type words.
# Physical state says what the sample is; optical regime says how light behaves in it.
STATE_SAMPLE_TYPES = {
    "liquid": {"liquid"},
    "paste": {"paste"},
    "soft_solid": {"soft"},
    "powder": {"powder"},
    "solid": {"solid", "solid film", "pill"},
}
REGIME_SAMPLE_TYPES = {
    "clear": set(),
    "turbid": {"colloidal", "scattering media"},
    "opaque": {"scattering media"},
}

# Technique ids that a rule's `technique: transmission` / `transflection` refers to.
TECHNIQUE_FAMILY = {
    "transmission": {"transmission_transflection", "thin_film_transmission", "cuvette"},
    "transflection": {"transmission_transflection"},
    "diffuse_reflection": {"diffuse_reflection", "diffuse_reflection_remote"},
    "ATR": {"ATR"},
    "raman_probe": {"raman_probe"},
    "fluorescence_probe": {"fluorescence_probe"},
}


@dataclass
class Candidate:
    method: str
    technique: str
    table_rows: list[int]
    in_line: bool
    sample_types: set[str]
    status: str = "pass"                      # pass | fail | unknown
    reasons: list[dict] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def downgrade(self, status: str, rule: str, message: str) -> None:
        order = {"pass": 0, "unknown": 1, "fail": 2}
        if order[status] > order[self.status]:
            self.status = status
        self.reasons.append({"status": status, "rule": rule, "message": message})


def candidates(in_line_only: bool = True) -> list[Candidate]:
    merged: dict[tuple[str, str], Candidate] = {}
    for row in kb.table1():
        method = METHOD_IDS[row["method"]]
        technique, in_line = TECHNIQUES[row["measurement_technique"]]
        if in_line_only and not in_line:
            continue
        key = (method, technique)
        if key not in merged:
            merged[key] = Candidate(method, technique, [], in_line, set())
        merged[key].table_rows.append(row["row"])
        merged[key].sample_types.update(row["sample_types"])
    return list(merged.values())


def _matches(value_or_list, actual) -> bool:
    options = value_or_list if isinstance(value_or_list, list) else [value_or_list]
    return actual in options


def _technique_in(target_technique, technique: str) -> bool:
    options = target_technique if isinstance(target_technique, list) else [target_technique]
    return any(technique in TECHNIQUE_FAMILY.get(t, {t}) for t in options)


def _when_state(when: dict, cand: Candidate, slots: dict) -> str:
    """'yes' if all conditions hold, 'no' if any fails, 'maybe' if any slot is unknown."""
    state = "yes"
    for key, expected in when.items():
        if key == "method":
            actual = cand.method
        elif key == "technique":
            if not _technique_in(expected, cand.technique):
                return "no"
            continue
        else:
            actual = slots.get(key, UNKNOWN)
        if actual == UNKNOWN:
            state = "maybe"
        elif not _matches(expected, actual):
            return "no"
    return state


def screen(slots: dict) -> list[Candidate]:
    """Evaluate every in-line candidate against the known slots.

    slots keys (all optional): physical_state, optical_regime, fluorophore, aqueous,
    heterogeneous, fiber_family. Missing keys count as unknown.
    """
    result = []
    state = slots.get("physical_state", UNKNOWN)
    regime = slots.get("optical_regime", UNKNOWN)
    known_types = STATE_SAMPLE_TYPES.get(state, set()) | REGIME_SAMPLE_TYPES.get(regime, set())
    for cand in candidates():
        # S01 Table 1 sample-type fit: pass on any overlap; otherwise unknown if a slot is missing.
        if known_types & cand.sample_types:
            pass
        elif UNKNOWN in (state, regime):
            cand.downgrade("unknown", "S01 Table 1 (p.6)",
                           "sample state or optical regime unknown: Table 1 sample-type fit not confirmed")
        else:
            cand.downgrade("fail", "S01 Table 1 (p.6)",
                           f"Table 1 lists {sorted(cand.sample_types)} for this technique; "
                           f"sample is {state}, {regime}")

        for rule in kb.rules():
            effect, target = rule["effect"], rule.get("target", {})
            match = _when_state(rule.get("when", {}), cand, slots)
            if match == "no":
                continue
            if effect == "exclude" and "technique" in target and _technique_in(target["technique"], cand.technique):
                cand.downgrade("fail" if match == "yes" else "unknown", rule["id"], rule["statement"])
            elif effect == "require" and "fluorophore" in target:
                value = slots.get("fluorophore", UNKNOWN)
                if value == UNKNOWN:
                    cand.downgrade("unknown", rule["id"], "no fluorescent species or indicator identified yet")
                elif value not in (target["fluorophore"] if isinstance(target["fluorophore"], list) else [target["fluorophore"]]):
                    cand.downgrade("fail", rule["id"], rule["statement"])
            elif effect == "require" and "physical_state" in target:
                if state == UNKNOWN:
                    cand.downgrade("unknown", rule["id"], "physical state unknown: " + rule["statement"])
                elif state not in target["physical_state"]:
                    cand.downgrade("fail", rule["id"], rule["statement"])
            elif effect == "warn" and match == "yes":
                cand.warnings.append(rule["id"])

        fiber_family = slots.get("fiber_family", UNKNOWN)
        if fiber_family != UNKNOWN:
            lo, hi = METHOD_RANGES_UM[cand.method]["range_um"]
            fams = [c for c in coverage(lo, hi) if c.family == fiber_family]
            if fams and all(c.status == "none" for c in fams):
                cand.downgrade("fail", "R-FIB-1", f"{fiber_family} fibers do not transmit the {cand.method} range")
            elif fams and all(c.status == "partial" for c in fams):
                cand.warnings.append("R-FIB-1")
        result.append(cand)
    return result
