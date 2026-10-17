"""Verify that a quoted passage appears on the cited source page.

Match levels, strongest first:
  exact  normalised quote is a substring of the normalised page text
  loose  equal after also ignoring case, hyphens and whitespace
  fuzzy  rapidfuzz partial-ratio alignment >= FUZZY_MIN (typos, small OCR-like drift)
Offsets refer to the stored page text, which is the text the model is shown.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from rapidfuzz import fuzz

from afs_assistant import kb
from afs_assistant.normalize import normalize

FUZZY_MIN = 90.0
MIN_QUOTE_CHARS = 12


@dataclass
class QuoteCheck:
    doc: str
    page: int
    quote: str
    status: str            # exact | loose | fuzzy | not_found | bad_page | too_short
    start: int | None = None
    end: int | None = None
    score: float | None = None
    page_sha256: str | None = None

    @property
    def ok(self) -> bool:
        return self.status in ("exact", "loose", "fuzzy")

    def to_dict(self) -> dict:
        return asdict(self)


def _loose_with_map(text: str) -> tuple[str, list[int]]:
    """Lowercased text without hyphens/whitespace, plus index map back to `text`."""
    chars, index = [], []
    for i, ch in enumerate(text):
        if ch.isspace() or ch == "-":
            continue
        chars.append(ch.lower())
        index.append(i)
    return "".join(chars), index


def verify(doc: str, page: int, quote: str) -> QuoteCheck:
    record = kb.page(doc, page)
    q = normalize(quote)
    if record is None:
        return QuoteCheck(doc, page, quote, "bad_page")
    if len(q) < MIN_QUOTE_CHARS:
        return QuoteCheck(doc, page, quote, "too_short", page_sha256=record["sha256"])
    text = record["text"]
    sha = record["sha256"]

    pos = text.find(q)
    if pos >= 0:
        return QuoteCheck(doc, page, quote, "exact", pos, pos + len(q), 100.0, sha)

    loose_text, index = _loose_with_map(text)
    loose_q = re.sub(r"[\s\-]", "", q.lower())
    pos = loose_text.find(loose_q)
    if pos >= 0 and loose_q:
        return QuoteCheck(doc, page, quote, "loose", index[pos], index[pos + len(loose_q) - 1] + 1, 100.0, sha)

    alignment = fuzz.partial_ratio_alignment(q, text)
    if alignment is not None and alignment.score >= FUZZY_MIN:
        return QuoteCheck(doc, page, quote, "fuzzy", alignment.dest_start, alignment.dest_end,
                          round(alignment.score, 1), sha)
    score = round(alignment.score, 1) if alignment is not None else None
    return QuoteCheck(doc, page, quote, "not_found", score=score, page_sha256=sha)
