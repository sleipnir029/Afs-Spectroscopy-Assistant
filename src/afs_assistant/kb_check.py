"""Validate the committed knowledge files (`afs-assist kb check`)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import get_args

from afs_assistant import kb, paths, quotes, schema, screen

EXPECTED_PAGES = {"S01": 19, "S02": 20, "S03": 17, "S04": 6, "S05": 2, "S06": 1, "REF": 2}
SCOPE_TAGS = {"method", "concept", "component_spec", "lab_example", "process_example", "literature_map",
              "research_study", "clinical_aspiration", "business", "guidance"}
EFFECTS = {"exclude", "require", "warn", "scope_limit", "guidance"}
# Effects the screening applies to candidates (screen.py); their `when` must use the screening vocabulary.
SCREENING_EFFECTS = {"exclude", "require", "warn"}
# `when` keys of evidence rules, read by scope.py (not by the screening).
EVIDENCE_KEYS = {"claim", "evidence_scope"}
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
    # The supplied page text is rebuilt locally (`kb build`); without it the page checks cannot run.
    pages = kb.pages() if kb.pages_available() else None
    if pages is None:
        findings.append(Finding("pages_present", False, kb.PAGES_MISSING_HINT))
    else:
        findings.append(Finding("pages_present", True, f"{len(pages)} page records"))
        counts: dict[str, int] = {}
        for doc, _ in pages:
            counts[doc] = counts.get(doc, 0) + 1
        findings.append(Finding("page_counts", counts == EXPECTED_PAGES, f"{counts}"))

        bad_scope = [kb.citation_label(*k) for k, r in pages.items()
                     if not r["scope"] or set(r["scope"]) - SCOPE_TAGS]
        findings.append(Finding("page_scopes", not bad_scope, f"missing/unknown scope: {bad_scope}"))
        findings.append(doc_ids_in_schema(pages))

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
    findings.append(rule_when_vocabulary(rules))
    if pages is not None:
        findings.append(_source_quotes(rules))

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

    findings.append(_external_library())
    if pages is not None:
        findings.append(_s02_guard(pages))
    findings.append(Finding("graph_present", paths.GRAPH_FILE.exists(), str(paths.GRAPH_FILE.name)))
    return findings


def _source_quotes(rules: list[dict]) -> Finding:
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
    return Finding("source_quotes_exact", not not_exact, f"{total} quotes; problems: {not_exact}")


def doc_ids_in_schema(pages: dict) -> Finding:
    """Every document in pages.jsonl must be citable: a doc id missing from `schema.Doc` can never be cited."""
    docs = {doc for doc, _ in pages}
    allowed = set(get_args(schema.Doc))
    return Finding("doc_ids_in_schema", docs == allowed,
                   f"not in schema.Doc: {sorted(docs - allowed)}; in schema.Doc without pages: {sorted(allowed - docs)}")


def rule_when_vocabulary(rules: list[dict]) -> Finding:
    """Every `when` key and value must be in the screening vocabulary. An unknown key reads as an unknown
    slot in `screen._when_state`, so a typo would silently turn candidates "unknown" instead of failing."""
    methods = set(get_args(schema.Method))
    allowed = {"method": methods, "technique": set(screen.TECHNIQUE_FAMILY), **screen.SLOT_VALUES}
    problems = []
    for r in rules:
        for key, value in (r.get("when") or {}).items():
            if key in EVIDENCE_KEYS and r["effect"] not in SCREENING_EFFECTS:
                continue
            if key not in allowed:
                problems.append(f"{r['id']}: unknown key {key!r}")
                continue
            values = value if isinstance(value, list) else [value]
            bad = [v for v in values if v not in allowed[key]]
            if bad:
                problems.append(f"{r['id']}: {key}={bad} not allowed")
    return Finding("rule_when_vocabulary", not problems, f"{len(rules)} rules; problems: {problems}")


def _external_library() -> Finding:
    """Every curated external passage is short (<= 400 chars, <= 2 sentences), numbered and carries sha256."""
    from afs_assistant.external import library

    entries = library.load()
    problems = library.problems(entries)
    passages = sum(len(e.get("passages", [])) for e in entries)
    return Finding("external_library", not problems,
                   f"{len(entries)} entries, {passages} passages; problems: {problems}")


def _s02_guard(pages: dict) -> Finding:
    """S02 quotable text must be the PDF text layer plus non-empty transcribed lines, nothing else."""
    from afs_assistant.kb_build import parse_s02_notes

    problems = []
    slides = parse_s02_notes(paths.S02_NOTES.read_text(encoding="utf-8"))
    for number, slide in slides.items():
        if any(not line for line in slide["image_text"]):
            problems.append(f"slide {number}: empty transcribed line")
        if "Figure (our description)" in pages[("S02", number)]["text"]:
            problems.append(f"slide {number}: notes leaked into quotable text")
    pdf_path = paths.MATERIALS / paths.SOURCE_PDFS["S02"]
    if pdf_path.exists():
        import pymupdf

        from afs_assistant.normalize import normalize
        for number, page in enumerate(pymupdf.open(pdf_path), start=1):
            layer = normalize(page.get_text())
            if not pages[("S02", number)]["text"].startswith(layer):
                problems.append(f"slide {number}: text does not start with the PDF text layer")
        detail = f"20 slides checked against PDF text layer; problems: {problems}"
    else:
        detail = f"PDF not present (text-layer comparison skipped); problems: {problems}"
    return Finding("s02_text_provenance", not problems, detail)
