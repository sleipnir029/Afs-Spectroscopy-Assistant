"""Query privacy guard (code only): search queries go to public APIs, so they must not carry
the customer's names, places, brands or settings.

A query is dropped (the reason is logged in `dropped_queries`) when it contains
  - a word that looks like a proper name in the enquiry or the intake: written capitalised where it
    does not start a sentence, longer than one letter ("°C"), and not in the domain vocabulary (gap
    texts are not used: they put model-capitalised parameter names inside our own sentence templates);
  - a number that also appears in the enquiry or the intake (a size, a temperature, a rate or a
    code copied from the customer).
URLs, e-mail addresses, DOIs and the word cap are checked in `step.clean_queries`. The query
planner never sees the enquiry itself (only the gap texts, targets and sample slots).

Domain vocabulary: every word that occurs in lower case in the supplied page text
(knowledge/pages.jsonl; words only ever capitalised there are mostly names of people, places
and companies), the method, technique and fiber-family names of the schema, and GENERIC_TERMS
(common acronyms of the field and of laboratory reference methods).
"""

from __future__ import annotations

import re
from functools import cache
from typing import get_args

from afs_assistant import kb
from afs_assistant.schema import Intake, Method, ProposedFiber, Technique

GENERIC_TERMS = frozenset({
    "nir", "mir", "ir", "ftir", "ft", "atr", "uv", "vis", "raman", "fourier", "led", "leds", "qcl", "hwg",
    "pat", "api", "cip", "sip", "pls", "pca", "snv", "da", "gc", "hplc", "lc", "ms", "nmr", "libs", "toc",
})
_WORD = re.compile(r"[^\W\d_][^\W_]*")                        # letters first, then letters or digits
_NUMBER = re.compile(r"(?<![^\W_])\d+(?:[.,]\d+)?")          # not glued to a word before it ("CO2" is no number)
_BULLET_END = re.compile(r"(?:^|\n)\s*[-*•]$")
_OPENERS = " \t\"'“‘([{"


@cache
def vocabulary() -> frozenset[str]:
    lower = {w for p in kb.pages().values() for w in _WORD.findall(p["text"]) if w.islower()}
    schema_words = {w.lower() for lit in (Method, Technique) for value in get_args(lit)
                    for w in _WORD.findall(value)}
    schema_words |= {w.lower() for value in get_args(ProposedFiber.model_fields["family"].annotation)
                     for w in _WORD.findall(value)}
    return frozenset(lower | schema_words | GENERIC_TERMS)


def _sentence_initial(text: str, start: int) -> bool:
    before = text[:start].rstrip(_OPENERS)
    return not before or before[-1] in ".!?:;\n" or bool(_BULLET_END.search(before))


def name_like_words(texts: list[str]) -> set[str]:
    """Lower-cased words that look like proper names in `texts` (see the module docstring)."""
    vocab = vocabulary()
    names = set()
    for text in texts:
        for m in _WORD.finditer(text):
            word, key = m.group(), m.group().lower()
            if word[0].isupper() and len(word) > 1 and key not in vocab and not _sentence_initial(text, m.start()):
                names.add(key)
    return names


def numbers(text: str) -> set[str]:
    return {n.replace(",", ".") for n in _NUMBER.findall(text)}


def intake_texts(intake: Intake | None) -> list[str]:
    if intake is None:
        return []
    texts = [intake.summary, *intake.unknowns, intake.proposed_fiber.enquiry_quote or ""]
    texts += [x for f in intake.facts_stated for x in (f.text, f.enquiry_quote)]
    texts += [x for t in intake.targets for x in (t.variable, t.purpose, t.enquiry_quote)]
    texts += [x for p in intake.process for x in (p.value, p.enquiry_quote)]
    texts += [x for p in intake.customer_premises for x in (p.claim, p.enquiry_quote)]
    texts += [getattr(intake.sample, n).enquiry_quote or "" for n in type(intake.sample).model_fields]
    return [t for t in texts if t]


class Guard:
    """Built once per run from the customer's text; `problem(query)` is the drop reason or None."""

    def __init__(self, enquiry: str = "", intake: Intake | None = None) -> None:
        customer = [t for t in (enquiry, *intake_texts(intake)) if t]
        self.names = name_like_words(customer)
        self.numbers = {n for t in customer for n in numbers(t)}

    def problem(self, query: str) -> str | None:
        named = sorted({w.lower() for w in _WORD.findall(query)} & self.names)
        if named:
            return f"possible name from the enquiry: {', '.join(named)}"
        copied = sorted(numbers(query) & self.numbers)
        if copied:
            return f"number from the enquiry: {', '.join(copied)}"
        return None
