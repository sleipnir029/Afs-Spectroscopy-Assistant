"""Find numbers (with units) in generated text and check where they came from.

Organizer rule: no accuracy, detection limit, response time, fiber length or other
figure that no source supports. A number in an answer must appear in a cited quote,
in the knowledge base page it cites, or in the customer's enquiry.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from afs_assistant.normalize import normalize

_UNIT = (r"(?:nm|µm|μm|um|mm|cm-1|cm⁻¹|cm\^-1|cm|km|m|%|ppm|ppb|°C|K|bar|psi|s|ms|min|h|"
         r"dB/m|dB/km|dB|mW|W|Hz|kHz|MHz|mg/L|g/L|mM|M|wt%|vol%|L|mL|°)")
_NUMBER = re.compile(
    r"(?<![\w.])(?P<num>\d+(?:[.,]\d+)?(?:\s*(?:-|to|–)\s*\d+(?:[.,]\d+)?)?)"
    r"\s*(?P<unit>" + _UNIT + r")?(?![\w])"
)
# Citation locators and identifiers are not quantities.
_LOCATOR = re.compile(r"(?:\b[SR]\d{2}\s*p\.\s*\d+|\bp\.\s*\d+|\bREF\s*§\s*\d+|§\s*\d+|\bTable\s+\d+|"
                      r"\bFig\.?\s*\d+|\bR-[A-Z]+-\d+|\bstep\s+\d+)", re.IGNORECASE)


@dataclass
class NumberMention:
    text: str          # e.g. "780-2500 nm"
    number: str        # e.g. "780-2500"
    unit: str | None
    start: int
    end: int


def _canon(number: str) -> str:
    return re.sub(r"\s*(?:to|–|-)\s*", "-", number.replace(",", "."))


def find_numbers(text: str) -> list[NumberMention]:
    text = normalize(text)
    masked = _LOCATOR.sub(lambda m: " " * len(m.group(0)), text)
    found = []
    for m in _NUMBER.finditer(masked):
        unit = m.group("unit")
        found.append(NumberMention(text[m.start():m.end()].strip(), _canon(m.group("num")), unit,
                                   m.start(), m.end()))
    return found


def unsupported_numbers(answer: str, allowed_texts: list[str]) -> list[NumberMention]:
    """Numbers in `answer` whose value does not occur in any allowed text.

    Matching is on the number itself (unit-insensitive) to tolerate "780-2500 nm"
    vs "780–2500 nm"; each end of a range is checked separately.
    """
    pool = set()
    for t in allowed_texts:
        for n in find_numbers(t):
            pool.add(n.number)
            pool.update(n.number.split("-"))
    missing = []
    for n in find_numbers(answer):
        parts = [n.number] if n.number in pool else n.number.split("-")
        if not all(p in pool for p in parts):
            missing.append(n)
    return missing
