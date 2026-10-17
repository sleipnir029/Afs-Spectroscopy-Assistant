"""Spectroscopy methods named in an enquiry, found with a fixed word list (no LLM).

Deterministic and verbatim by construction: each value is the exact span of the
enquiry that names the method. "Named" is not "proposed"; the assess step judges
the customer's intent. Bare "IR"/"infrared" is ambiguous (NIR or MIR) and not mapped.
"""

from __future__ import annotations

import re

from afs_assistant.schema import Method

METHOD_PATTERNS: dict[Method, re.Pattern] = {
    "NIR": re.compile(r"\bNIRS?\b|\bnear[- ]?infra-?red\b", re.IGNORECASE),
    "MIR": re.compile(r"\bMIRS?\b|\bmid[- ]?infra-?red\b|\bFT-?IR\b", re.IGNORECASE),
    "Raman": re.compile(r"\bRaman\b", re.IGNORECASE),
    "Fluorescence": re.compile(r"\bfluoresc\w*", re.IGNORECASE),
    "UV-Vis": re.compile(r"\bUV(?:[-/ ]?vis(?:ible)?)?\b|\bultra-?violet\b", re.IGNORECASE),
}


def named_methods(enquiry: str) -> dict[str, str]:
    """{Method value: first verbatim enquiry span naming it}, in METHOD_PATTERNS order."""
    found = {}
    for method, rx in METHOD_PATTERNS.items():
        m = rx.search(enquiry)
        if m:
            found[method] = m.group(0)
    return found
