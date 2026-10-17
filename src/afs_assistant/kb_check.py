"""Validate the committed knowledge files (`afs-assist kb check`)."""

from __future__ import annotations

import re
from dataclasses import dataclass

from afs_assistant import kb, paths, quotes

EXPECTED_PAGES = {"S01": 19, "S02": 20, "S03": 17, "S04": 6, "S05": 2, "S06": 1, "REF": 2}
SCOPE_TAGS = {"method", "concept", "component_spec", "lab_example", "process_example", "literature_map",
              "research_study", "clinical_aspiration", "business", "guidance"}
EFFECTS = {"exclude", "require", "warn", "scope_limit", "guidance"}
# Scenario ids must never appear in knowledge, skills, prompts or code (no case-specific content).
CASE_ID = re.compile(r"\b[DH]0[1-8]\b")
LINT_DIRS = ("knowledge", "skills", "src", "prompts", ".pi")
LINT_SUFFIXES = {".py", ".md", ".yaml", ".yml", ".json", ".jsonl", ".ts", ".txt"}


@dataclass
class Finding:
    check: str
    ok: bool
    detail: str


def run() -> list[Finding]:
    findings: list[Finding] = []
    pages = kb.pages()

    counts: dict[str, int] = {}
    for doc, _ in pages:
        counts[doc] = counts.get(doc, 0) + 1
    findings.append(Finding("page_counts", counts == EXPECTED_PAGES, f"{counts}"))

    bad_scope = [kb.citation_label(*k) for k, r in pages.items()
                 if not r["scope"] or set(r["scope"]) - SCOPE_TAGS]
    findings.append(Finding("page_scopes", not bad_scope, f"missing/unknown scope: {bad_scope}"))

    rules = kb.rules()
    ids = [r["id"] for r in rules]
    findings.append(Finding("rule_ids_unique", len(ids) == len(set(ids)), f"{len(ids)} rules"))
    bad_effect = [r["id"] for r in rules if r["effect"] not in EFFECTS]
    findings.append(Finding("rule_effects", not bad_effect, f"bad effect: {bad_effect}"))

    # YAML 1.1 turns bare yes/no into booleans; slot values must stay strings.
    def _has_bool(value) -> bool:
        if isinstance(value, bool):
            return True
        if isinstance(value, dict):
            return any(_has_bool(v) for v in value.values())
        if isinstance(value, list):
            return any(_has_bool(v) for v in value)
        return False
    bool_rules = [r["id"] for r in rules if _has_bool(r.get("when", {})) or _has_bool(r.get("target", {}))]
    findings.append(Finding("rule_values_are_strings", not bool_rules, f"boolean slot values in: {bool_rules}"))

    not_exact = []
    total = 0
    for owner, sources in [(r["id"], r["sources"]) for r in rules] + \
                          [(f["id"], f["sources"]) for f in kb.fibers()]:
        if not sources:
            not_exact.append(f"{owner}: no sources")
        for s in sources:
            total += 1
            c = quotes.verify(s["doc"], s["page"], s["quote"])
            if c.status != "exact":
                not_exact.append(f"{owner} {kb.citation_label(s['doc'], s['page'])}: {c.status}")
    findings.append(Finding("source_quotes_exact", not not_exact, f"{total} quotes; problems: {not_exact}"))

    hits = []
    for d in LINT_DIRS:
        base = paths.ROOT / d
        if not base.exists():
            continue
        for f in base.rglob("*"):
            if f.is_file() and f.suffix in LINT_SUFFIXES and "__pycache__" not in f.parts:
                for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if CASE_ID.search(line) and "CASE_ID" not in line:
                        hits.append(f"{f.relative_to(paths.ROOT)}:{i}")
    findings.append(Finding("no_case_ids", not hits, f"scenario ids found at: {hits}"))

    findings.append(Finding("graph_present", paths.GRAPH_FILE.exists(), str(paths.GRAPH_FILE.name)))
    return findings
