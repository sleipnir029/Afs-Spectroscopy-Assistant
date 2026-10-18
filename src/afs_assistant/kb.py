"""Read access to the committed knowledge files."""

from __future__ import annotations

import json
from functools import lru_cache

import yaml

from afs_assistant import paths

# The full page text of the supplied materials is not distributed with the repository: it is rebuilt locally.
PAGES_MISSING_HINT = ("needs knowledge/pages.jsonl: run `uv run afs-assist kb build` with the organiser "
                      "materials in resources/materials/ (the supplied page text is not distributed)")


class PagesMissing(FileNotFoundError):
    """knowledge/pages.jsonl is absent (a fresh clone before `afs-assist kb build`)."""


def pages_available() -> bool:
    return paths.PAGES_FILE.exists()


@lru_cache(maxsize=1)
def pages() -> dict[tuple[str, int], dict]:
    if not pages_available():
        raise PagesMissing(PAGES_MISSING_HINT)
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
