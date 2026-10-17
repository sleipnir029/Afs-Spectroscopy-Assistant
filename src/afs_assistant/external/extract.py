"""Turn fetched bytes into normalised paragraphs: Europe PMC XML, HTML (trafilatura), PDF (pymupdf).

`clean()` is applied to every result: whitespace normalised with `normalize()`, empty
paragraphs dropped, and paragraphs that read like instructions to a model removed before
any model sees them (an extra guard; verification is the main one). A source with fewer
than MIN_CHARS characters left is dropped (`None`): never quote what could not be fetched.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET

from afs_assistant.normalize import normalize

MIN_CHARS = 500
# Whole subtrees that are not running text.
_XML_DROP = {"ref-list", "table-wrap", "table", "fig", "script", "style", "supplementary-material",
             "inline-formula", "disp-formula", "ack", "fn-group", "glossary"}
INSTRUCTION = re.compile(
    r"\b(?:ignore|disregard|forget|override)\b[^.]{0,40}\b(?:instructions?|prompts?|rules)\b"
    r"|\bsystem prompt\b|\byou are (?:an? )?(?:ai|assistant|language model|chatbot|llm)\b"
    r"|\bas an ai\b|\bnew instructions?\b",
    re.IGNORECASE,
)


def clean(paragraphs: list[str]) -> tuple[list[str] | None, int]:
    """Normalise, drop instruction-like paragraphs; None if under MIN_CHARS. Returns (paragraphs, removed count)."""
    kept, removed = [], 0
    for p in paragraphs:
        p = normalize(p)
        if not p:
            continue
        if INSTRUCTION.search(p):
            removed += 1
            continue
        kept.append(p)
    if sum(len(p) for p in kept) < MIN_CHARS:
        return None, removed
    return kept, removed


def _local(tag) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


def _text(node: ET.Element) -> str:
    """Text of a node without dropped subtrees (tails of dropped nodes are kept)."""
    parts = [node.text or ""]
    for child in node:
        if _local(child.tag) not in _XML_DROP:
            parts.append(_text(child))
        parts.append(child.tail or "")
    return "".join(parts)


def xml_paragraphs(data: bytes | str) -> list[str]:
    """JATS (Europe PMC fullTextXML): every outermost <p> outside dropped subtrees, in document order."""
    root = ET.fromstring(data)
    out: list[str] = []

    def walk(node: ET.Element) -> None:
        name = _local(node.tag)
        if name in _XML_DROP:
            return
        if name == "p":
            out.append(_text(node))
            return
        for child in node:
            walk(child)

    walk(root)
    return out


def html_paragraphs(data: bytes | str) -> list[str]:
    import trafilatura

    html = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data
    text = trafilatura.extract(html, include_comments=False, include_tables=False, favor_precision=True)
    return [line for line in (text or "").split("\n") if line.strip()]


def pdf_paragraphs(data: bytes) -> list[str]:
    import pymupdf

    out = []
    with pymupdf.open(stream=data, filetype="pdf") as doc:
        for page in doc:
            out += [b[4] for b in page.get_text("blocks") if b[6] == 0]      # text blocks only
    return out


def paragraphs_for(content: bytes, content_type: str, url: str = "") -> list[str]:
    """Pick the extractor by content type (or the url as a hint)."""
    ct, u = content_type.lower(), url.lower()
    if "pdf" in ct or u.endswith(".pdf"):
        return pdf_paragraphs(content)
    if ("xml" in ct and "html" not in ct) or u.endswith("fulltextxml"):
        return xml_paragraphs(content)
    return html_paragraphs(content)
