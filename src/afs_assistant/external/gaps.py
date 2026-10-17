"""Gap detection (code only): where the supplied-source assessment leaves a question open.

Signals, in priority order: a status of insufficient_information or outside_supported_scope,
parameters measured by an auxiliary sensor, an extended (multi-method) option, `not_in_sources`
items, `not_covered` premises, required parameters without a citation. At most MAX_GAPS gaps
(G1, ...); no gap means no external search, so no extra cost or latency.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from afs_assistant.schema import Assessment

MAX_GAPS = 4
OPEN_STATUSES = ("insufficient_information", "outside_supported_scope")


@dataclass
class Gap:
    id: str
    kind: str          # status | auxiliary_sensor | multi_method | not_in_sources | premise_not_covered | uncited_parameter
    text: str
    location: str      # where in the assessment it comes from
    option_id: str | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def detect(a: Assessment) -> list[Gap]:
    found: list[tuple[str, str, str, str | None]] = []
    if a.decision_status in OPEN_STATUSES:
        found.append(("status", f"{a.decision_status.replace('_', ' ')}: {a.status_reason}", "decision_status", None))
    for i, p in enumerate(a.parameters):
        if p.measured_by.type == "auxiliary_sensor":
            sensor = p.measured_by.sensor or "auxiliary sensor"
            found.append(("auxiliary_sensor", f"In-line measurement of {p.name} with {sensor}", f"parameters[{i}]",
                          _option_with_parameter(a, p.id)))
    for i, o in enumerate(a.solution_options):
        if o.tier == "extended":
            note = f" ({o.fusion_note})" if o.fusion_note else ""
            found.append(("multi_method", f"Combining several spectroscopy methods (data fusion){note}",
                          f"solution_options[{i}]", o.id))
    for i, text in enumerate(a.not_in_sources):
        found.append(("not_in_sources", text, f"not_in_sources[{i}]", None))
    for i, p in enumerate(a.premise_checks):
        if p.verdict == "not_covered":
            found.append(("premise_not_covered", p.premise, f"premise_checks[{i}]", None))
    for i, p in enumerate(a.parameters):
        if p.necessity == "required" and not p.citations and p.measured_by.type != "auxiliary_sensor":
            found.append(("uncited_parameter", f"Measuring {p.name}: {p.why}", f"parameters[{i}]",
                          _option_with_parameter(a, p.id)))

    gaps, seen = [], set()
    for kind, text, location, option_id in found:
        key = " ".join(text.lower().split())
        if not key or key in seen:
            continue
        seen.add(key)
        gaps.append(Gap(f"G{len(gaps) + 1}", kind, " ".join(text.split()), location, option_id))
        if len(gaps) == MAX_GAPS:
            break
    return gaps


def _option_with_parameter(a: Assessment, parameter_id: str) -> str | None:
    """The proposed option if it covers the parameter, else the first option that does."""
    covering = [o.id for o in a.solution_options if parameter_id in o.parameter_ids]
    if a.proposal.best_current_option in covering:
        return a.proposal.best_current_option
    return covering[0] if covering else None
