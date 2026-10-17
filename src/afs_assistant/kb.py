"""Read access to the committed knowledge files."""

from __future__ import annotations

import json
from functools import lru_cache

import yaml

from afs_assistant import paths


@lru_cache(maxsize=1)
def pages() -> dict[tuple[str, int], dict]:
    with paths.PAGES_FILE.open(encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh if line.strip()]
    return {(r["doc"], r["page"]): r for r in records}


def page(doc: str, number: int) -> dict | None:
    return pages().get((doc, int(number)))


@lru_cache(maxsize=1)
def rules() -> list[dict]:
    return yaml.safe_load(paths.RULES_FILE.read_text(encoding="utf-8"))["rules"]


@lru_cache(maxsize=1)
def fibers() -> list[dict]:
    return json.loads(paths.FIBERS_FILE.read_text(encoding="utf-8"))["fibers"]


@lru_cache(maxsize=1)
def table1() -> list[dict]:
    return json.loads(paths.TABLE1_FILE.read_text(encoding="utf-8"))["rows"]


def citation_label(doc: str, number: int) -> str:
    return f"REF §{number}" if doc == "REF" else f"{doc} p.{number}"
