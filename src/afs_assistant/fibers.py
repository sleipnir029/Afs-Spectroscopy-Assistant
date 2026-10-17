"""Which fiber families transmit a spectral range (data: knowledge/fibers.json, from S02 p.6)."""

from __future__ import annotations

from dataclasses import dataclass

from afs_assistant import kb
from afs_assistant.units import range_to_um

# Nominal method ranges with their source pages. Raman and fluorescence light is
# visible/short-wave NIR, so their range is the detection region, not the Raman shift.
METHOD_RANGES_UM = {
    "NIR": {"range_um": (0.78, 2.5), "source": "S01 p.10", "basis": "NIR spectra (780-2500 nm)"},
    "MIR": {"range_um": (2.5, 25.0), "source": "S01 p.9", "basis": "mid-IR range (4000-400 cm-1)"},
    "UV-Vis": {"range_um": (0.19, 0.74), "source": "S01 p.5; S01 p.17",
               "basis": "UV region (190-360 nm); VIS 400-740 nm on Fig. 7"},
    "Raman": {"range_um": (0.4, 1.1), "source": "S01 p.11; S01 p.15",
              "basis": "Raman signal recorded in the visible/short-wave NIR (400-1100 nm); 785 nm excitation"},
    "Fluorescence": {"range_um": (0.19, 0.74), "source": "S01 p.12",
                     "basis": "irradiation in the UV and visible regions; emission shifted to longer wavelengths"},
}


@dataclass
class Coverage:
    fiber_id: str
    name: str
    family: str
    window_um: tuple[float, float]
    status: str                      # full | partial | none
    overlap_um: tuple[float, float] | None
    sources: list[dict]


def coverage(lo: float, hi: float, unit: str = "um") -> list[Coverage]:
    """Classify every fiber family against the requested range."""
    r_lo, r_hi = range_to_um(lo, hi, unit)
    result = []
    for f in kb.fibers():
        f_lo, f_hi = f["min_um"], f["max_um"]
        o_lo, o_hi = max(r_lo, f_lo), min(r_hi, f_hi)
        if f_lo <= r_lo and f_hi >= r_hi:
            status = "full"
        elif o_lo < o_hi:
            status = "partial"
        else:
            status = "none"
        overlap = (round(o_lo, 4), round(o_hi, 4)) if o_lo < o_hi else None
        result.append(Coverage(f["id"], f["name"], f["family"], (f_lo, f_hi), status, overlap, f["sources"]))
    return result


def method_fiber_coverage(method: str) -> list[Coverage]:
    lo, hi = METHOD_RANGES_UM[method]["range_um"]
    return coverage(lo, hi, "um")
