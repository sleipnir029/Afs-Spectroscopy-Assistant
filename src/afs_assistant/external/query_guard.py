"""Query privacy guard (code only): search queries go to public APIs, so they must not carry
the customer's names, places, brands or settings.

A query is dropped (the reason is logged in `dropped_queries`) when it contains
  - a word that looks like a proper name in the enquiry or the intake: written capitalised (also at
    a sentence or line start: "Kestrelwerk produces...", "Mr. Smith"), longer than one letter ("°C"),
    not in the domain vocabulary and never written in lower case in the customer's text (gap texts
    are not used: they put model-capitalised parameter names inside our own sentence templates);
  - a word of an e-mail address, URL or domain in the customer's text ("jan@kestrel.de" -> kestrel),
    except www/http(s) and common top-level domains;
  - a product or size code from the customer's text, compared without its space or hyphen
    ("XR-200" = "XR 200" = "XR200", "DN 50" = "DN50");
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
_ADDRESS = re.compile(r"\S+@\S+|https?://\S+|www\.\S+|\b[\w-]+\.[a-z]{2,6}\b")
_ADDRESS_PARTS = frozenset({"www", "http", "https", "com", "de", "org", "net", "eu", "ch", "at", "uk", "co", "io"})
_CODE = re.compile(r"\b[A-Za-z]{1,5}[\s-]?\d+\b")       # "XR-200", "DN 50", "XR200"


@cache
def vocabulary() -> frozenset[str]:
    lower = {w for p in kb.pages().values() for w in _WORD.findall(p["text"]) if w.islower()}
    schema_words = {w.lower() for lit in (Method, Technique) for value in get_args(lit)
                    for w in _WORD.findall(value)}
    schema_words |= {w.lower() for value in get_args(ProposedFiber.model_fields["family"].annotation)
                     for w in _WORD.findall(value)}
    return frozenset(lower | schema_words | GENERIC_TERMS)


def name_like_words(texts: list[str]) -> set[str]:
    """Lower-cased words that look like proper names in `texts` (see the module docstring)."""
    vocab = vocabulary()
    lower = {w for t in texts for w in _WORD.findall(t) if w.islower()}
    return {w.lower() for t in texts for w in _WORD.findall(t)
            if w[0].isupper() and len(w) > 1 and w.lower() not in vocab and w.lower() not in lower}


def address_words(text: str) -> set[str]:
    """Words of the e-mail addresses, URLs and domains in `text`, without www/http(s) and common TLDs."""
    return {w.lower() for m in _ADDRESS.findall(text) for w in _WORD.findall(m)} - _ADDRESS_PARTS


def codes(text: str, capitalised: bool = False) -> set[str]:
    """Letter + number codes, squashed: "XR-200" / "XR 200" -> "xr200". `capitalised`: only codes whose
    letters include a capital (the customer's "XR-200", not "at 37", which the number rule covers)."""
    return {re.sub(r"[\s-]", "", c).lower() for c in _CODE.findall(text)
            if not capitalised or any(ch.isupper() for ch in c)}


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
        self.names |= {w for t in customer for w in address_words(t) | codes(t, capitalised=True)}
        self.numbers = {n for t in customer for n in numbers(t)}

    def problem(self, query: str) -> str | None:
        named = sorted(({w.lower() for w in _WORD.findall(query)} | codes(query)) & self.names)
        if named:
            return f"possible name from the enquiry: {', '.join(named)}"
        copied = sorted(numbers(query) & self.numbers)
        if copied:
            return f"number from the enquiry: {', '.join(copied)}"
        return None
