"""Spectroscopy methods named in an enquiry, found with a fixed word list (no LLM).

Deterministic and verbatim by construction: each value is the exact span of the
enquiry that names the method. "Named" is not "proposed"; the assess step judges
the customer's intent. Bare "IR"/"infrared" and bare "Vis" are ambiguous and not mapped
("Vis-NIR" still names NIR).
"""

from __future__ import annotations

import re

from afs_assistant.schema import Method

METHOD_PATTERNS: dict[Method, re.Pattern] = {
    "NIR": re.compile(r"\bNIRS?\b|\bnear[- ]?infra-?red\b", re.IGNORECASE),
    "MIR": re.compile(r"\bMIRS?\b|\bmid[- ]?infra-?red\b|\bmid[- ]?IR\b|\bFT-?IR\b", re.IGNORECASE),
    "Raman": re.compile(r"\bRaman\b|\bSERS\b", re.IGNORECASE),
    # Not "non-fluorescent"/"nonfluorescent"; "autofluorescence" counts.
    "Fluorescence": re.compile(r"(?<!non-)\b(?!non)\w*fluoresc\w*", re.IGNORECASE),
    # Not UV used for curing, lamps or stabilisers.
    "UV-Vis": re.compile(r"\bUV(?:[-/ ]?vis(?:ible)?)?\b(?![- ]?(?:cur|lamp|stabili))|\bultra[- ]?violet\b",
                         re.IGNORECASE),
}


def named_methods(enquiry: str) -> dict[str, str]:
    """{Method value: first verbatim enquiry span naming it}, in METHOD_PATTERNS order."""
    found = {}
    for method, rx in METHOD_PATTERNS.items():
        m = rx.search(enquiry)
        if m:
            found[method] = m.group(0)
    return found
