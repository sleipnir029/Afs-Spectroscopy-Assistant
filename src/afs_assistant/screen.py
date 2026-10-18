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
# Near-match Table 1 words per state (3.R3 B2): a row that lists only a neighbour is "to be tested",
# not a fail. Generic physics neighbours only; states far apart (e.g. powder vs liquid) still fail.
STATE_NEIGHBOURS = {
    "soft_solid": {"solid", "paste"},
    "paste": {"soft", "liquid"},
}
REGIME_SAMPLE_TYPES = {
    "clear": set(),
    "turbid": {"colloidal", "scattering media"},
    "opaque": {"scattering media"},          # opaque because it scatters (e.g. milk concentrate)
    "opaque_absorbing": set(),               # dark, absorbing, little scattering (e.g. dark oils)
}
# A `variable` sample changes between clear and turbid (D-061): screened as each of these states.
VARIABLE_REGIMES = ("clear", "turbid")
REGIME_SAMPLE_TYPES["variable"] = set().union(*(REGIME_SAMPLE_TYPES[r] for r in VARIABLE_REGIMES))

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
    notes: list[str] = field(default_factory=list)

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
    """'yes' if all conditions hold, 'no' if any fails, 'maybe' if any slot is unknown.

    A `variable` optical regime is checked as each of VARIABLE_REGIMES: a condition that holds for
    all of them is met, for some of them gives 'maybe', for none 'no'."""
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
        elif key == "optical_regime" and actual == "variable":
            hits = sum(_matches(expected, r) for r in VARIABLE_REGIMES)
            if hits == 0:
                return "no"
            if hits < len(VARIABLE_REGIMES):
                state = "maybe"
        elif not _matches(expected, actual):
            return "no"
    return state


# Allowed slot values; anything else is a caller error, not "unknown".
SLOT_VALUES = {
    "physical_state": {"liquid", "paste", "soft_solid", "powder", "solid"},
    "optical_regime": {"clear", "turbid", "opaque", "opaque_absorbing", "variable"},
    "fluorophore": {"yes", "no"},
    "aqueous": {"yes", "no"},
    "heterogeneous": {"yes", "no"},
    "remote_distance": {"yes", "no"},     # a distance or remote analyzer is stated or asked about
}
FIBER_FAMILIES = {"silica", "chalcogenide", "polycrystalline", "hollow_waveguide", "fluoride"}


def _rule(rule_id: str) -> dict:
    return next(r for r in kb.rules() if r["id"] == rule_id)


def validate_slots(slots: dict) -> None:
    for key, value in slots.items():
        if key == "proposed_fiber":
            if not isinstance(value, dict) or value.get("family") not in FIBER_FAMILIES:
                raise ValueError(f"proposed_fiber must be {{family: one of {sorted(FIBER_FAMILIES)}, for_method}}")
            if value.get("for_method") not in METHOD_RANGES_UM:
                raise ValueError(f"proposed_fiber.for_method is required, one of {sorted(METHOD_RANGES_UM)}")
            continue
        if key not in SLOT_VALUES:
            raise ValueError(f"unknown slot {key!r}")
        if value != UNKNOWN and value not in SLOT_VALUES[key]:
            raise ValueError(f"{key}={value!r}; allowed: {sorted(SLOT_VALUES[key])} or 'unknown'")


def _fiber_for(cand: Candidate, slots: dict) -> str | None:
    fiber = slots.get("proposed_fiber")
    if not fiber or fiber["for_method"] != cand.method:
        return None
    return fiber["family"]


def _target_applies(target: dict, cand: Candidate, fiber_family: str | None) -> bool:
    """A warn rule only applies to candidates its target names (technique / fiber family)."""
    if "technique" in target and not _technique_in(target["technique"], cand.technique):
        return False
    if "fiber_family" in target:
        families = target["fiber_family"] if isinstance(target["fiber_family"], list) else [target["fiber_family"]]
        if fiber_family not in families:
            return False
    return True


def screen(slots: dict) -> list[Candidate]:
    """Evaluate every in-line candidate against the known slots.

    slots keys (all optional): physical_state, optical_regime, fluorophore, aqueous,
    heterogeneous, remote_distance (values in SLOT_VALUES or "unknown"), and proposed_fiber
    {family, for_method} for an existing or proposed fiber link. Missing keys = unknown.
    """
    validate_slots(slots)
    result = []
    state = slots.get("physical_state", UNKNOWN)
    regime = slots.get("optical_regime", UNKNOWN)
    known_types = STATE_SAMPLE_TYPES.get(state, set()) | REGIME_SAMPLE_TYPES.get(regime, set())
    for cand in candidates():
        fiber_family = _fiber_for(cand, slots)
        # S01 Table 1 sample-type fit: pass on any overlap; unknown for a near-match state, a dark sample
        # under diffuse reflection or a missing slot. A near match keeps the other reason too (3.R4 N1).
        near = bool(STATE_NEIGHBOURS.get(state, set()) & cand.sample_types)
        if not known_types & cand.sample_types:
            if near:
                cand.downgrade("unknown", "S01 Table 1 (p.6)",
                               f"Table 1 lists {sorted(cand.sample_types)} for this technique; "
                               f"fit for {state.replace('_', ' ')} to be tested")
            if regime == "opaque_absorbing" and cand.technique.startswith("diffuse_reflection"):
                cand.downgrade("unknown", "S01 Table 1 (p.6)",
                               "dark, absorbing (non-scattering) sample: diffuse reflection signal must be tested")
            elif UNKNOWN in (state, regime):
                cand.downgrade("unknown", "S01 Table 1 (p.6)",
                               "sample state or optical regime unknown: Table 1 sample-type fit not confirmed")
            elif not near:
                cand.downgrade("fail", "S01 Table 1 (p.6)",
                               f"Table 1 lists {sorted(cand.sample_types)} for this technique; "
                               f"sample is {state}, {regime}")

        for rule in kb.rules():
            effect, target = rule["effect"], rule.get("target", {})
            match = _when_state(rule.get("when", {}), cand, slots)
            if match == "no":
                continue
            if effect == "exclude" and "technique" in target and _technique_in(target["technique"], cand.technique):
                if (cand.technique in TECHNIQUE_FAMILY["transflection"]
                        and _when_state(_rule("R-GEO-5")["when"], cand, slots) == "yes"):
                    # Combined transmission/transflection probe: transmission is excluded, but where
                    # R-GEO-5 applies, transflection works "in some cases", so this stays open.
                    cand.downgrade("unknown", rule["id"],
                                   rule["statement"] + " Transflection may still work in some cases (R-GEO-5): test it.")
                else:
                    cand.downgrade("fail" if match == "yes" else "unknown", rule["id"], rule["statement"])
            elif effect == "require" and "fluorophore" in target:
                value = slots.get("fluorophore", UNKNOWN)
                wanted = target["fluorophore"] if isinstance(target["fluorophore"], list) else [target["fluorophore"]]
                if value == UNKNOWN:
                    cand.downgrade("unknown", rule["id"], "no fluorescent species or indicator identified yet")
                elif value not in wanted:
                    cand.downgrade("fail", rule["id"], rule["statement"])
            elif effect == "require" and "physical_state" in target:
                if state == UNKNOWN:
                    cand.downgrade("unknown", rule["id"], "physical state unknown: " + rule["statement"])
                elif state not in target["physical_state"]:
                    cand.downgrade("fail", rule["id"], rule["statement"])
            elif (effect == "warn" and match == "yes" and rule.get("when")
                  and _target_applies(target, cand, fiber_family)):
                # Rules with an empty `when` are assessment-level guidance, not candidate warnings.
                cand.warnings.append(rule["id"])

        if fiber_family is not None:
            lo, hi = METHOD_RANGES_UM[cand.method]["range_um"]
            fams = [c for c in coverage(lo, hi) if c.family == fiber_family]
            if fams and all(c.status == "none" for c in fams):
                windows = ", ".join(f"{c.window_um[0]}-{c.window_um[1]} um" for c in fams)
                cand.downgrade("fail", "R-FIB-1",
                               f"{fiber_family} fibers ({windows}) do not transmit the {cand.method} range "
                               f"({lo}-{hi} um)")
            elif fams and not any(c.status == "full" for c in fams):
                best = max(fams, key=lambda c: (c.overlap_um[1] - c.overlap_um[0]) if c.overlap_um else 0)
                cand.notes.append(f"{best.name} covers {best.window_um[0]}-{best.window_um[1]} um: only part of the "
                                  f"nominal {cand.method} range ({lo}-{hi} um); usable range about "
                                  f"{best.overlap_um[0]}-{best.overlap_um[1]} um (S02 p.6 figure reading)")
        result.append(cand)
    return result
