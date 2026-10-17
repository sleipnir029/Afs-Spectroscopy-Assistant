"""Load customer enquiries from the organizer files into scenarios/*.jsonl.

dev.jsonl            development enquiries (docx section 1): id, title, enquiry, plus the
                     organizer's "facts stated" / "useful sources" kept for evaluation only
dev_reference.jsonl  organizer worked answers (docx section 2), for evaluation only
final.jsonl          final evaluation enquiries (txt): id, title, enquiry

The parser keys on document structure (section headings, "ID · title" / "ID | title"
lines), never on specific scenario ids.
"""

from __future__ import annotations

import json
import re

from afs_assistant import paths
from afs_assistant.kb_build import DOCX_NAME, _docx_blocks
from afs_assistant.normalize import normalize

FINAL_NAME = "customer_scenarios_for_final_evaluation.txt"
_DOCX_HEADING = re.compile(r"^([A-Z]\d{2})\s+·\s+(.+)$")
_TXT_HEADING = re.compile(r"^([A-Z]\d{2}) \| (.+)$")


def _is_heading(block: str, prefix: str) -> bool:
    # Table rows (contents table) also start with section names; headings have no " | ".
    return block.startswith(prefix) and " | " not in block


def _section(blocks: list[str], start_prefix: str, end_prefix: str) -> list[str]:
    start = next(i for i, b in enumerate(blocks) if _is_heading(b, start_prefix))
    end = next(i for i, b in enumerate(blocks) if i > start and _is_heading(b, end_prefix))
    return blocks[start + 1:end]


def _split_by_heading(blocks: list[str]) -> list[tuple[str, str, list[str]]]:
    items, current = [], None
    for block in blocks:
        m = _DOCX_HEADING.match(block)
        if m:
            current = (m.group(1), m.group(2).strip(), [])
            items.append(current)
        elif current is not None:
            current[2].append(block)
    return items


def load_dev() -> tuple[list[dict], list[dict]]:
    from docx import Document

    blocks = _docx_blocks(Document(paths.MATERIALS / DOCX_NAME))
    dev = []
    for sid, title, body in _split_by_heading(_section(blocks, "1. Development scenarios", "2. Worked examples")):
        enquiry = body[0]
        facts = next((b.removeprefix("Facts stated").strip() for b in body if b.startswith("Facts stated")), "")
        sources = next((b.removeprefix("Useful sources").strip() for b in body if b.startswith("Useful sources")), "")
        dev.append({"id": sid, "title": title, "enquiry": normalize(enquiry),
                    "eval_facts_stated": facts, "eval_useful_sources": sources})
    reference = [{"id": sid, "title": title, "worked_answer": "\n".join(body)}
                 for sid, title, body in _split_by_heading(_section(blocks, "2. Worked examples", "3. Answer structure"))]
    return dev, reference


def load_final() -> list[dict]:
    lines = (paths.MATERIALS / FINAL_NAME).read_text(encoding="utf-8").splitlines()
    items, current = [], None
    for line in lines:
        m = _TXT_HEADING.match(line.strip())
        if m:
            current = {"id": m.group(1), "title": m.group(2).strip(), "lines": []}
            items.append(current)
        elif current is not None and not set(line.strip()) <= {"="}:
            current["lines"].append(line)
    return [{"id": c["id"], "title": c["title"], "enquiry": normalize(" ".join(c["lines"]))} for c in items]


def _write(records: list[dict], name: str) -> None:
    paths.SCENARIOS.mkdir(exist_ok=True)
    with (paths.SCENARIOS / name).open("w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def build() -> dict[str, int]:
    dev, reference = load_dev()
    final = load_final()
    _write(dev, "dev.jsonl")
    _write(reference, "dev_reference.jsonl")
    _write(final, "final.jsonl")
    return {"dev": len(dev), "dev_reference": len(reference), "final": len(final)}


def load(set_name: str) -> list[dict]:
    path = paths.SCENARIOS / f"{set_name}.jsonl"
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]
