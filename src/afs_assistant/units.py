"""Spectral unit conversion: nm, µm and wavenumber (cm-1).

wavelength_um = 10_000 / wavenumber_cm1 (REF §5 unit reminder: 4000 cm-1 = 2.5 µm).
"""

from __future__ import annotations

_ALIASES = {
    "nm": "nm", "um": "um", "µm": "um", "μm": "um", "micron": "um", "microns": "um",
    "cm-1": "cm-1", "cm^-1": "cm-1", "cm⁻¹": "cm-1", "1/cm": "cm-1", "wavenumber": "cm-1",
}


def canonical_unit(unit: str) -> str:
    key = unit.strip().lower().replace(" ", "")
    if key not in _ALIASES:
        raise ValueError(f"unknown spectral unit: {unit!r}")
    return _ALIASES[key]


def to_um(value: float, unit: str) -> float:
    u = canonical_unit(unit)
    if u == "um":
        return float(value)
    if u == "nm":
        return float(value) / 1000.0
    if value == 0:
        raise ValueError("wavenumber 0 has no wavelength")
    return 10_000.0 / float(value)


def from_um(value_um: float, unit: str) -> float:
    u = canonical_unit(unit)
    if u == "um":
        return value_um
    if u == "nm":
        return value_um * 1000.0
    return 10_000.0 / value_um


def convert(value: float, from_unit: str, to_unit: str) -> float:
    return from_um(to_um(value, from_unit), to_unit)


def range_to_um(a: float, b: float, unit: str) -> tuple[float, float]:
    """Any range (wavenumber ranges run high->low) as an ascending µm interval."""
    lo, hi = sorted((to_um(a, unit), to_um(b, unit)))
    return lo, hi
