"""Text normalisation shared by the knowledge build and the quote verifier.

The knowledge base stores text in this normalised form, the model sees that
same text, and quotes are verified against it. Keeping one function for all
three avoids "verified against different text than the model saw" errors.
"""

from __future__ import annotations

import re
import unicodedata

_HYPHEN_BREAK = re.compile(r"(\w)-\s*\n\s*(\w)")
_WHITESPACE = re.compile(r"\s+")
# Characters that differ only typographically between PDF text and model output.
_TRANSLATE = str.maketrans({
    "­": "",    # soft hyphen
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "−": "-",
    "‘": "'", "’": "'", "“": '"', "”": '"',
    " ": " ", " ": " ", " ": " ",
    "\ue0c8": "=",  # private-use glyph S04 uses for the double bond in "C=O"
})
# Other private-use glyphs carry no reliable meaning; drop them.
_PRIVATE_USE = re.compile("[\ue000-\uf8ff]")


def normalize(text: str) -> str:
    """NFKC, unify dashes/quotes/spaces, join line-break hyphens, collapse whitespace.

    A hyphen at a line break is kept ("measure-\\nment" -> "measure-ment"): in the
    supplied PDFs real compounds ("fiber-optic") and syllable breaks both occur,
    so dropping it would corrupt compounds. `loose()` handles the difference.
    """
    text = unicodedata.normalize("NFKC", text).translate(_TRANSLATE)
    text = _PRIVATE_USE.sub("", text)
    text = _HYPHEN_BREAK.sub(r"\1-\2", text)
    return _WHITESPACE.sub(" ", text).strip()


def loose(text: str) -> str:
    """Lowercase form without hyphens or whitespace, for tolerant quote matching."""
    return re.sub(r"[\s\-]", "", normalize(text).lower())
