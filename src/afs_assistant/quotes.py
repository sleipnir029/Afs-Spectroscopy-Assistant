"""Verify that a quoted passage appears on the cited source page (or in a stored external paragraph).

Match levels, strongest first:
  exact         normalised quote is a substring of the normalised page text
  loose         equal after also ignoring case, whitespace and hyphens; a hyphen next to a digit (only
                whitespace between) is kept, so "1-10" matches "1 - 10" but "10-20" never matches "1020";
                whitespace between two digits stays one space, so "1 100" never matches "1100"
  fuzzy_review  close (rapidfuzz partial ratio >= FUZZY_MIN) with the same numbers and
                negation/comparison words; NOT verified, needs repair or human review
Only exact and loose count as verified (`ok`). A near match that changes a number or a
negation ("do not exhibit" -> "do exhibit", "below 0.1" -> "above 0.1") is `not_found`.
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
_NUM = re.compile(r"\d+(?:[.,]\d+)?")
_GUARD_WORDS = {"not", "no", "never", "cannot", "without", "only", "below", "above", "less", "more",
                "under", "over", "except", "neither", "nor", "none",
                "some", "all", "most", "every", "any", "few", "many",
                "millimolar", "micromolar", "nanomolar"}
_GUARD_UNITS = re.compile(r"(?<![a-zµμ])(nm|µm|μm|um|mm|cm-1|cm|km|m|%|ppm|ppb)(?![a-z])")


@dataclass
class QuoteCheck:
    doc: str
    page: int
    quote: str
    status: str            # exact | loose | fuzzy_review | not_found | bad_page | too_short
    start: int | None = None
    end: int | None = None
    score: float | None = None
    page_sha256: str | None = None

    @property
    def ok(self) -> bool:
        return self.status in ("exact", "loose")

    def to_dict(self) -> dict:
        return asdict(self)


def _next_to_digit(text: str, i: int) -> bool:
    """Is the nearest non-whitespace character on either side of position i a digit?"""
    j = i - 1
    while j >= 0 and text[j].isspace():
        j -= 1
    k = i + 1
    while k < len(text) and text[k].isspace():
        k += 1
    return (j >= 0 and text[j].isdigit()) or (k < len(text) and text[k].isdigit())


def _between_digits(text: str, i: int) -> bool:
    """Does the whitespace run starting at position i sit directly between two digits ("1 100")?"""
    if i == 0 or text[i - 1].isspace() or not text[i - 1].isdigit():
        return False
    k = i + 1
    while k < len(text) and text[k].isspace():
        k += 1
    return k < len(text) and text[k].isdigit()


def _loose_with_map(text: str) -> tuple[str, list[int]]:
    """Lowercased text without whitespace and without hyphens that are not next to a digit, plus an
    index map back to `text`. Whitespace between two digits stays as one space ("1 100" is not
    "1100"). Dashes are already "-" after normalize()."""
    chars, index = [], []
    for i, ch in enumerate(text):
        if ch.isspace() and _between_digits(text, i):
            chars.append(" ")
            index.append(i)
            continue
        if ch.isspace() or (ch == "-" and not _next_to_digit(text, i)):
            continue
        chars.append(ch.lower())
        index.append(i)
    return "".join(chars), index


def verify(doc: str, page: int, quote: str) -> QuoteCheck:
    record = kb.page(doc, page)
    if record is None:
        return QuoteCheck(doc, page, quote, "bad_page")
    return verify_text(record["text"], quote, record["sha256"], doc, page)


def verify_text(text: str, quote: str, sha: str, doc: str = "", page: int = 0) -> QuoteCheck:
    """The matcher on any stored text (a supplied page or an external paragraph); `sha` identifies that text."""
    q = normalize(quote)
    if len(q) < MIN_QUOTE_CHARS:
        return QuoteCheck(doc, page, quote, "too_short", page_sha256=sha)

    pos = text.find(q)
    if pos >= 0:
        return QuoteCheck(doc, page, quote, "exact", pos, pos + len(q), 100.0, sha)

    loose_text, index = _loose_with_map(text)
    loose_q, _ = _loose_with_map(q)
    pos = loose_text.find(loose_q)
    if pos >= 0 and loose_q:
        start, end = index[pos], index[pos + len(loose_q) - 1] + 1
        return QuoteCheck(doc, page, quote, "loose", start, end, 100.0, sha)

    alignment = fuzz.partial_ratio_alignment(q, text)
    score = round(alignment.score, 1) if alignment is not None else None
    if alignment is not None and alignment.score >= FUZZY_MIN:
        start, end = _widen_to_words(text, alignment.dest_start, alignment.dest_end)
        if _same_meaning_markers(q, text[start:end]):
            return QuoteCheck(doc, page, quote, "fuzzy_review", start, end, score, sha)
    return QuoteCheck(doc, page, quote, "not_found", score=score, page_sha256=sha)


def _widen_to_words(text: str, start: int, end: int) -> tuple[int, int]:
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    while end < len(text) and not text[end].isspace():
        end += 1
    return start, end


def _markers(s: str) -> tuple[list[str], set[str], list[str]]:
    lower = s.lower()
    numbers = sorted(n.replace(",", ".") for n in _NUM.findall(s))
    words = {w for w in re.findall(r"[a-z]+", lower) if w in _GUARD_WORDS}
    units = sorted(_GUARD_UNITS.findall(lower))
    return numbers, words, units


def _same_meaning_markers(quote: str, span: str) -> bool:
    """A near match must keep every number, unit and negation/comparison/quantifier word unchanged."""
    return _markers(quote) == _markers(span)
