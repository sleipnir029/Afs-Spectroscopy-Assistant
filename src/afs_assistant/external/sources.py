"""External source records and verbatim quote checks on their paragraphs.

A `SourceRecord` holds one fetched source: metadata (4.1 fields) and its paragraphs.
Paragraph numbers are 1-based and cited as `E01 ¶3`. A library entry keeps only its
stored passages, numbered as in the fetched text (`paragraph_numbers`).

Full text is written only under runs/external_cache/sources/ (gitignored). `meta()` is
what outputs and the provenance commit get: metadata and sha256, never paragraphs.
External quotes use the supplied-page matcher (`quotes.verify_text`) with a stricter
quotation policy: exact or loose only, 12-400 characters and at most two sentences.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Protocol

from afs_assistant import paths, quotes
from afs_assistant.normalize import normalize

MAX_QUOTE_CHARS = 400
MAX_QUOTE_SENTENCES = 2
_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z])")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class SourceText(Protocol):
    """Anything that can hand the matcher one stored text: a supplied page or an external paragraph."""

    def paragraph(self, number: int) -> str | None: ...


@dataclass
class SourceRecord:
    id: str                         # E01, ... (run-local)
    url: str
    doi: str | None
    title: str
    authors: list[str]
    year: int | None
    venue: str | None
    licence: str | None
    access: str                     # full_text | abstract_only
    retrieved_at: str               # real clock, ISO UTC, when the text was fetched
    retrieval_query: str
    api: str                        # library | europepmc | openalex | unpaywall
    http_status: int | None
    sha256: str                     # of the full extracted text (library: of the text it was built from)
    paragraphs: list[str] = field(default_factory=list)
    library_id: str | None = None
    paragraph_numbers: list[int] = field(default_factory=list)   # empty: 1..n

    def numbered(self) -> list[tuple[int, str]]:
        numbers = self.paragraph_numbers or range(1, len(self.paragraphs) + 1)
        return list(zip(numbers, self.paragraphs, strict=True))

    def paragraph(self, number: int) -> str | None:
        return dict(self.numbered()).get(number)

    def meta(self) -> dict:
        """Everything except the text: safe for outputs and the provenance commit."""
        data = asdict(self)
        data.pop("paragraphs")
        data.pop("paragraph_numbers")
        data["paragraph_count"] = len(self.paragraphs)
        return data


def full_text_sha(paragraphs: list[str]) -> str:
    return sha("\n\n".join(paragraphs))


def cache_dir() -> Path:
    return paths.EXTERNAL_CACHE / "sources"


def save_text(record: SourceRecord, root: Path | None = None) -> Path:
    """Store the full record (with paragraphs) by its text sha256; local cache only."""
    target = (root or cache_dir()) / f"{record.sha256}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(asdict(record), ensure_ascii=False), encoding="utf-8")
    return target


def load_text(sha256: str, root: Path | None = None) -> SourceRecord | None:
    target = (root or cache_dir()) / f"{sha256}.json"
    if not target.exists():
        return None
    return SourceRecord(**json.loads(target.read_text(encoding="utf-8")))


def sentence_count(quote: str) -> int:
    return len([p for p in _SENTENCE_BREAK.split(normalize(quote)) if p.strip()])


def policy_problem(quote: str) -> str | None:
    """Quotation policy for third-party text (short attributed quotes only)."""
    q = normalize(quote)
    if len(q) > MAX_QUOTE_CHARS:
        return f"quote longer than {MAX_QUOTE_CHARS} characters ({len(q)})"
    if sentence_count(q) > MAX_QUOTE_SENTENCES:
        return f"quote longer than {MAX_QUOTE_SENTENCES} sentences"
    return None


@dataclass
class ExternalQuoteCheck:
    source_id: str
    para: int                       # the paragraph the quote was found in (corrected if needed)
    cited_para: int                 # the paragraph the model cited
    status: str                     # exact | loose | fuzzy_review | not_found | too_short | too_long | bad_para
    paragraph_sha256: str | None = None
    problem: str = ""

    @property
    def ok(self) -> bool:
        return self.status in ("exact", "loose")

    @property
    def corrected(self) -> bool:
        return self.ok and self.para != self.cited_para


def verify_quote(source: SourceRecord, para: int, quote: str) -> ExternalQuoteCheck:
    """Check `quote` against the cited paragraph; if it is verbatim in another paragraph, cite that one."""
    problem = policy_problem(quote)
    if problem:
        return ExternalQuoteCheck(source.id, para, para, "too_long", problem=problem)
    text = source.paragraph(para)
    if text is None:
        status = "bad_para"
    else:
        check = quotes.verify_text(text, quote, sha(text))
        if check.ok or check.status == "too_short":
            return ExternalQuoteCheck(source.id, para, para, check.status, check.page_sha256)
        status = check.status
    for number, other in source.numbered():
        if number == para:
            continue
        check = quotes.verify_text(other, quote, sha(other))
        if check.ok:
            return ExternalQuoteCheck(source.id, number, para, check.status, check.page_sha256,
                                      f"found in ¶{number}, not in the cited ¶{para}; paragraph corrected")
    return ExternalQuoteCheck(source.id, para, para, status,
                              problem="cited paragraph does not exist" if status == "bad_para" else "")
