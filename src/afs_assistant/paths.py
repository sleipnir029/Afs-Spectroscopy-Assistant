"""Filesystem locations used across the package."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Organizer-supplied files: local only, gitignored (see .gitignore).
RESOURCES = ROOT / "resources"
MATERIALS = RESOURCES / "materials"
MATERIALS_ZIP = RESOURCES / "materials.zip"

# Derived knowledge and our own notes: committed.
KNOWLEDGE = ROOT / "knowledge"
PAGES_FILE = KNOWLEDGE / "pages.jsonl"
S02_NOTES = KNOWLEDGE / "s02_slide_notes.md"
PAGE_SCOPES = KNOWLEDGE / "page_scopes.yaml"
TABLE1_FILE = KNOWLEDGE / "table1_methods.json"
FIBERS_FILE = KNOWLEDGE / "fibers.json"
RULES_FILE = KNOWLEDGE / "rules.yaml"
GRAPH_FILE = KNOWLEDGE / "graph.json"
# Curated external library: metadata, verified short passages and sha256 only (no full text).
EXTERNAL_LIBRARY = KNOWLEDGE / "external" / "library.jsonl"

SKILLS = ROOT / "skills"
SCENARIOS = ROOT / "scenarios"
OUTPUTS = ROOT / "outputs"
RUNS = ROOT / "runs"
# Fetched external responses and full text: local only (runs/ is gitignored).
EXTERNAL_CACHE = RUNS / "external_cache"

# Source PDFs keyed by the citation id the organizers use (S01 p.10, S02 p.13, ...).
SOURCE_PDFS = {
    "S01": "S01_Multispectral_Laboratory.pdf",
    "S02": "S02_AFS_Process_Control_Slides.pdf",
    "S03": "S03_LED_Kidney_Study_2017.pdf",
    "S04": "S04_Combi_MIR_Fluorescence_2021.pdf",
    "S05": "S05_AFS_Flyer.pdf",
}
