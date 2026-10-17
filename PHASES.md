# Phases

Master plan: approved Plan v3 (2026-10-17). This file breaks it into phases.

**Rules for every phase**
1. **Plan:** write the phase's detailed plan (goal, steps, deliverables, acceptance checks, risks, out of scope) in this file.
2. **Approve:** the user approves it. No code for the phase before approval.
3. **Implement:** only what the plan says. Any change goes to `DEVIATIONS.md` first, with the reason.
4. **Check:** run the phase's acceptance checks (`uv run pytest`, scripts) and record the results in `STATUS.md`.
5. **Review:** an independent reviewer agent reviews the phase (blocking vs non-blocking findings). Then the user reviews at the gate.
6. **Close:** commit named paths only, update `STATUS.md`, and only then plan the next phase.

**Tooling:** uv for everything: `uv add` / `uv sync` / `uv run`, with `uv.lock` committed. No bare `pip` or `python`.

| Phase | Name | Goal | Gate |
|---|---|---|---|
| 0 | Repo hygiene and setup | Keep organizer files out of git; uv project | G0 |
| 1 | Knowledge foundation | Verified knowledge layer + deterministic tools, no LLM | G1 |
| 2 | Pipeline MVP | AFS-Ashby steps 0–8 end to end on D01–D08, with deterministic checks + provenance | G2 |
| 3 | Quality and evaluation | Critic + repair, adversarial set, eval harness, model bake-off, baseline table | G3 |
| 4 | Chat shell and evidence view | pi shell (SYSTEM.md, extension, skills), HTML evidence view, clarification loop | G4 |
| 5 | Freeze | Independent review, fixes, generate H01–H06 once, commit | G5 |
| 6 | Deliverables | README, ARCHITECTURE, slides PDF, video, fresh-clone test, publish, submit | Submit |

Phases 2–6 get their detailed plans written when the previous phase closes. The outlines are in Plan v3, §9.

---

## Phase 0 — Repo hygiene and setup (DONE before this file existed; see DEVIATIONS D-001)
- Backup `~/Desktop/aails-backup-2026-10-17.tgz`.
- `.gitignore`: `resources/` (organizer files), `.env`, `.venv/`, caches, `.DS_Store`.
- Single commit amended. Reflog expired and gc'd: 0 objects reference `resources/`. No remote existed.
- `uv init --lib` (Python 3.12). Deps: openai, pydantic, pymupdf, openpyxl, python-docx, networkx, rapidfuzz, dulwich, python-dotenv, pyyaml. Dev: pytest, ruff.

---

## Phase 1 — Knowledge foundation (APPROVED 2026-10-17 08:55 — in progress)

**Goal.** A committed, checkable knowledge layer: page text, slide notes, scope tags, tables, generic rules, and a knowledge graph. Plus the deterministic tools that later phases use to check answers. **No LLM calls in this phase.**

**Inputs.** `resources/materials/*` (local only).

### Steps

**1.1 Text normalisation (one function, used everywhere).**
- Apply NFKC (fixes ligatures like "ﬁ").
- Join words hyphenated across line breaks.
- Collapse newlines and whitespace to single spaces.
- The verifier later uses the same function, so quotes are always checked against the exact text the model saw.

**1.2 Page extraction → `knowledge/pages.jsonl`.** Also the organizer docx §3 (good practice) and §5 (method overview + fiber table) as citable source `REF` (page = section number), approved by the user. D01–D08 and the worked answers stay out of the knowledge base (dev/eval data only).
- Sources: S01 (19 p), S03 (17 p), S04 (6 p), S05 (2 p), S06 (link, 1 "page").
- Fields: `doc, page, scope[], title, text, sha256, extraction`.

**1.3 S02 slide notes → `knowledge/s02_slide_notes.md`.**
- One section per slide (20).
- Each section has three parts:
  - (a) legible slide text transcribed verbatim, in quotes;
  - (b) a figure description in our own words;
  - (c) "Uncertain readings" (e.g. the UV-VIS silica lower edge reads "180 nm" on the slide vs "190 nm" in the organizer docx).
- Read from 200-dpi renders.
- Parsed into `pages.jsonl` as `doc=S02`, `extraction=transcription`.

**1.4 Page scope tags → `knowledge/page_scopes.yaml`.**
- Vocabulary: `method` (general method description), `concept` (system or vision), `component_spec` (fibers, probes), `lab_example`, `process_example`, `literature_map`, `research_study` (S03/S04), `clinical_aspiration`, `business`.
- A page can carry several tags.
- Each tag gets a one-line justification in our own words.

**1.5 Tables.**
- `knowledge/table1_methods.json`: Table 1 from the xlsx. Path/depth parsed into numeric ranges with units ("mu" means µm). Cited as "S01 Table 1 (p.6)".
- `knowledge/fibers.json`: from the S02 p.6 figure, with min/max in µm, the vendor (art photonics vs Le Verre Fluoré), and discrepancy notes.

**1.6 Generic rules → `knowledge/rules.yaml`.**
- About 30–50 rules, each with:
  - `id`, `statement` (our words)
  - `applies_when` (structured condition)
  - `effect`: `exclude | require | warn | scope_limit`
  - `sources`: list of `{doc, page, quote}`, each quote verbatim from `pages.jsonl`
- Examples:
  - silica fibers do not transmit the MIR range
  - fluorescence quantification needs a fluorescent species
  - transmission fails for thick/opaque media
  - a calibration is matrix-specific
  - ATR needs contact
  - lab and research pages cannot support process or clinical readiness
- **No scenario IDs, no scenario-specific content.**

**1.7 Knowledge graph → `knowledge/graph.json`** (networkx node-link JSON) built from 1.2–1.6.
- Nodes: Method, Technique, Phenomenon, SampleType/OpticalRegime, SpectralRange, FiberType, ProbeType, Analyte, Application, SourcePage, Rule.
- Edges: suits, excludedFor, operatesIn, transmits, requires, limits, demonstratedIn, supportedBy.

**1.8 Deterministic tools** (`src/afs_assistant/`):
- `units`: nm ↔ µm ↔ cm⁻¹
- `fiber_coverage`: which fibers cover a range
- `screen`: method×technique survivors given known slots; `unknown` stays distinct from `fail`
- `quotes`: verify `(doc, page, quote)` by exact normalised match, then fuzzy ≥90; returns offsets + page sha256
- `numbers`: extract numbers and units from text
- `scope`: allowed scopes per claim type

**1.9 CLI via uv:** `uv run afs-assist kb build` (rebuild everything from `resources/`) and `uv run afs-assist kb check` (validate everything).

**1.10 Tests:** `uv run pytest`.

### Deliverables
`knowledge/*` (committed), `src/afs_assistant/{paths,normalize,kb_build,graph,units,fibers,screen,quotes,numbers,scope,cli}.py`, `tests/`.

### Acceptance checks
- [ ] Page counts: S01 19, S02 20, S03 17, S04 6, S05 2, S06 1.
- [ ] Every rule quote verifies exactly against `pages.jsonl` (100%, not fuzzy).
- [ ] Unit tests:
  - 4000 cm⁻¹ = 2.5 µm
  - silica VIS-NIR does not cover 2.5–25 µm
  - CIR covers 2.5–6.5 µm
  - PIR does not cover 2.5–3.0 µm
  - opaque → transmission excluded
  - unknown regime → `unknown`, not `fail`
  - quote true/false cases
  - number extraction
- [ ] Lint test: no `D0[1-8]` / `H0[1-6]` strings in `knowledge/`, `skills/`, `src/`.
- [ ] `kb build` is reproducible: running it twice gives identical sha256 for each file.
- [ ] Spot check: 5 random pages compared against the PDFs by eye.

### Review
- A reviewer agent checks:
  - rules vs sources (right scope? overstated?)
  - hard-coding risk
  - S02 notes vs slide images (sample of 6 slides)
  - test coverage
- **G1 (user, ~13:15):** read the S02 notes for slides 6, 7, 13, 14, plus 10 rules.

### Risks
- S02 transcription errors → uncertain readings flagged; reviewer samples the slides.
- Rules drift into scenario answers → lint test + reviewer + rules stay generic.
- Time → timebox 3.5 h. If short, cut rules to about 25 and simplify the knowledge graph to rules + tables + pages.

### Out of scope
LLM calls, pipeline, prompts, UI, provenance, external references (decided after Q&A).
