"""Find numbers (with units) in generated text and check where they came from.

Organizer rule: no accuracy, detection limit, response time, fiber length or other
figure that no source supports. Checks are claim-local: a claim's numbers must appear,
with a compatible unit, in that claim's own verified quotes or in the customer's enquiry
(never a global pool and never the whole cited page). A real number moved onto the wrong
subject (e.g. a silica cable length used for an MIR link) is a meaning error this module
cannot see; rules (R-FIB-2) and the critic must catch it.

Comparison is on (value, unit dimension): nm / µm / cm-1 are converted to µm; mm / cm /
m / km to metres; %, percent, wt%, vol% are one dimension. A unitless number only matches
a unitless number. A range is supported only if the same range occurs in an allowed text;
a single number may match a single value or a range endpoint. Small unitless counts
(integers <= SMALL_COUNT_MAX, e.g. "3 steps", "5 questions") are not treated as figures.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from afs_assistant.normalize import normalize

SMALL_COUNT_MAX = 10

# Longest first; a unit must not run into a following letter ("5 samples" is not "5 s").
_UNITS = ["minutes", "minute", "seconds", "second", "hours", "hour", "days", "day", "weeks", "week",
          "months", "month", "years", "year",
          "dB/km", "dB/m", "mg/L", "g/L", "wt%", "vol%", "cm-1", "cm⁻¹", "cm^-1", "percent", "ppm",
          "ppb", "°C", "µm", "μm", "um", "nm", "mm", "km", "cm", "m", "%", "bar", "psi", "ms", "min",
          "s", "h", "mW", "W", "kHz", "MHz", "Hz", "mM", "M", "mL", "L", "K", "-fold", "x", "×", "dB", "°"]
_UNIT_RE = "|".join(re.escape(u) for u in _UNITS)
_NUM = re.compile(
    r"(?<![\w.])(?P<sign>[-−+](?=\d))?(?P<num>\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?(?:,\d+)?)"
    r"(?:\s*(?P<unit>" + _UNIT_RE + r")(?![A-Za-zµμ]))?"
)
_RANGE_SEP = re.compile(r"^\s*(?:-|–|to)\s*$")
# Citation locators, identifiers and labels are not quantities.
_MASKS = [
    re.compile(r"\b[SR]\d{2}\b"),
    re.compile(r"\bpp?\.\s*\d+(?:\s*[-–,]\s*\d+)*"),
    re.compile(r"(?:REF\s*)?§\s*\d+"),
    re.compile(r"\b(?:Table|Fig(?:ure)?\.?|Slide|Section|Phase|Stage|Path|Option|Step|Round|Level|Tier)\s*\d+"
               r"(?:\s+of\s+\d+)?", re.IGNORECASE),
    re.compile(r"\bR-[A-Z]+-\d+\b"),
    re.compile(r"\bD-\d{3}\b"),
    re.compile(r"(?m)^\s*\d+[.)]\s"),
]
_SPECTRAL = {"nm": 1e-3, "µm": 1.0, "μm": 1.0, "um": 1.0}
_LENGTH = {"mm": 1e-3, "cm": 1e-2, "m": 1.0, "km": 1e3}
_PERCENT = {"%", "percent", "wt%", "vol%"}
_WAVENUMBER = {"cm-1", "cm⁻¹", "cm^-1"}
_TIME_S = {"s": 1, "second": 1, "seconds": 1, "ms": 1e-3, "min": 60, "minute": 60, "minutes": 60,
           "h": 3600, "hour": 3600, "hours": 3600, "day": 86400, "days": 86400, "week": 604800, "weeks": 604800}
_CALENDAR = {"month": "month", "months": "month", "year": "year", "years": "year"}


@dataclass
class NumberMention:
    text: str
    low: float
    high: float | None     # None for a single value
    unit: str | None
    dim: str               # comparison dimension: spectral_um | length_m | percent | <unit> | unitless
    start: int
    end: int

    @property
    def is_range(self) -> bool:
        return self.high is not None


def _value(sign: str | None, num: str) -> float:
    if re.fullmatch(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", num):
        num = num.replace(",", "")
    else:
        num = num.replace(",", ".")
    v = float(num)
    return -v if sign in ("-", "−") else v


def _canon(value: float, unit: str | None) -> tuple[str, float]:
    if unit is None:
        return "unitless", value
    if unit in _SPECTRAL:
        return "spectral_um", value * _SPECTRAL[unit]
    if unit in _WAVENUMBER:
        return ("spectral_um", 10_000.0 / value) if value else ("cm-1", value)
    if unit in _LENGTH:
        return "length_m", value * _LENGTH[unit]
    if unit in _PERCENT:
        return "percent", value
    if unit in ("x", "×", "-fold"):
        return "factor", value
    if unit in _TIME_S:
        return "time_s", value * _TIME_S[unit]
    if unit in _CALENDAR:
        return _CALENDAR[unit], value
    return unit, value


def _mask(text: str) -> str:
    for rx in _MASKS:
        text = rx.sub(lambda m: " " * len(m.group(0)), text)
    return text


def find_numbers(text: str) -> list[NumberMention]:
    text = normalize(text)
    masked = _mask(text)
    tokens = list(_NUM.finditer(masked))
    found: list[NumberMention] = []
    i = 0
    while i < len(tokens):
        a = tokens[i]
        b = tokens[i + 1] if i + 1 < len(tokens) else None
        joiner = masked[a.end():b.start()] if b else ""
        sign_b_is_dash = bool(b and b.group("sign") in ("-", "−") and joiner.strip() == "")
        if b and (_RANGE_SEP.match(joiner) or sign_b_is_dash):
            unit = b.group("unit") or a.group("unit")
            lo_dim, lo = _canon(_value(a.group("sign"), a.group("num")), unit)
            _, hi = _canon(_value(None if sign_b_is_dash else b.group("sign"), b.group("num")), unit)
            found.append(NumberMention(text[a.start():b.end()].strip(), min(lo, hi), max(lo, hi), unit,
                                       lo_dim, a.start(), b.end()))
            i += 2
            continue
        unit = a.group("unit")
        dim, value = _canon(_value(a.group("sign"), a.group("num")), unit)
        if not (dim == "unitless" and value.is_integer() and 0 <= value <= SMALL_COUNT_MAX):
            found.append(NumberMention(text[a.start():a.end()].strip(), value, None, unit, dim,
                                       a.start(), a.end()))
        i += 1
    return found


def _close(x: float, y: float) -> bool:
    return math.isclose(x, y, rel_tol=1e-6, abs_tol=1e-9)


def unsupported_numbers(answer: str, allowed_texts: list[str]) -> list[NumberMention]:
    """Numbers in `answer` that no allowed text supports (same value and unit dimension)."""
    singles: list[tuple[str, float]] = []
    ranges: list[tuple[str, float, float]] = []
    for t in allowed_texts:
        for n in find_numbers(t):
            if n.is_range:
                ranges.append((n.dim, n.low, n.high))
                singles += [(n.dim, n.low), (n.dim, n.high)]
            else:
                singles.append((n.dim, n.low))
    missing = []
    for n in find_numbers(answer):
        if n.is_range:
            ok = any(d == n.dim and _close(lo, n.low) and _close(hi, n.high) for d, lo, hi in ranges)
        else:
            ok = any(d == n.dim and _close(v, n.low) for d, v in singles)
        if not ok:
            missing.append(n)
    return missing
