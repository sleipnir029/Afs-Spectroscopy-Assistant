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
| 1 | Knowledge foundation | Verified knowledge layer + deterministic tools, no LLM | G1 (passed) |
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

## Phase 1 — Knowledge foundation (CLOSED 2026-10-17 09:06: review APPROVE WITH FIXES → fixed; G1 OK)

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

### Phase 1 review fixes (1.R) — APPROVED 2026-10-17 (all R1–R8; implemented); B8 decision: keep `pages.jsonl` committed (user)
The reviewer verdict was APPROVE WITH FIXES (B1–B8 blocking). Fixes, in order:
- **R1 `quotes.py`:** a fuzzy match becomes status `fuzzy_review` (`ok=False`). On top of that, fuzzy is rejected if the numbers or negation words (not, no, never, cannot, without, only, below, above, less, more) differ between the quote and the matched span. Only `exact` and `loose` count as verified. Tests: "above 0.1 percent", "below 1 percent", "do exhibit" must all fail.
- **R2 S02 provenance:** `pages.jsonl` S02 `text` = verbatim slide text only. Our figure descriptions and uncertain readings move to a `notes` field the verifier never searches. Slide-6 values are recorded as verbatim label sequences, tagged `figure_reading`. R-FIB-1, R-FIB-2 and `fibers.json` are re-quoted against verbatim text. New `kb check`: S02 verbatim text is compared against the PDF text layer where one exists. Test: our own description text must NOT verify.
- **R3 factual fixes:** R-FIB-2 rewritten. The MIR samples on S02 p.9–10 are 1–2 m lab lengths, the long cables are silica only, and no source gives an MIR link length. Add the slide-10 FX80 legend and slide-16 "excitation". Move the slide-13 "laboratory spectra" inference to uncertain readings. Fix the `page_scopes` S02 p.9 note.
- **R4 `numbers.py`:** match on (value, unit dimension); a unitless number only matches a unitless number; a range is supported only as the same range; `float` canonicalisation, `percent`→`%`, thousands separators, signs, `10x`. Mask page ranges, Phase/Stage/Path/Option/Step n, and list markers. A test for each reviewer probe.
- **R5 `screen.py`:**
  - Warn rules apply only when their `target` technique / fiber family matches.
  - `transmission_transflection` + opaque → `unknown` (R-GEO-2 vs R-GEO-5), not `fail`.
  - Slot values validated against the vocabulary (unknown value → error).
  - The fiber slot becomes `proposed_fiber: {family, for_method}` (applies only to that method).
  - Fiber-specific coverage messages.
  - Add regime `opaque_absorbing` (dark, non-scattering) → reflection `unknown`.
- **R6 `scope.py`:** forbidden tags, derived from R-EVI-1 in `rules.yaml` (single source of truth); any forbidden tag on the page fails. Readiness claims never "pass"; best case `precedent_only` (R-EVI-2). Tests updated (S01 p.14/15 and S02 p.14 → precedent_only).
- **R7 rule fixes (non-blocking list):**
  - R-GEO-7 `when` method UV-Vis
  - R-MIR-1 wording (transflexion probes exist)
  - quotes added for R-MIR-2/3/4, R-NIR-1, R-CMB-1, R-EVI-3 (full sentence), R-EVI-4
  - R-CAL-1 limited to NIR/Raman with "re-validated" wording
  - R-GEO-1/5 say "dairy example"
  - **5 new generic rules:** IR water absorption limits aqueous path; nominal range ≠ instrument/fiber range (all methods); independent reference measurements on representative samples; NIR transmission path 1–10 mm controlled; inhomogeneity/turbulence affect technique choice.
- **R8 small fixes:**
  - `normalize` maps private-use glyphs
  - `units` rejects 0 / negative values
  - `.gitignore` comment `make kb` → `uv run afs-assist kb build` (comment only)
  - S02 header line about the text layer corrected
- **Acceptance:** `kb check` all PASS (incl. new S02 text-layer check); `pytest` all PASS with the new tests; reviewer re-checks B1–B7 (focused re-review); then G1.

**1.R re-review result:** APPROVE WITH FIXES. B1–B6 fixed, B7 partial; no new blocking issues.

### Phase 1 leftovers (1.R2) — APPROVED 2026-10-17 09:04 (user); G1 content review: OK (user)
1. `screen.py`: the transflection exception only applies when R-GEO-5's own `when` holds (NIR; clear/turbid/opaque). So UV-Vis on opaque samples, and NIR on `opaque_absorbing`, go back to `fail`.
2. `kb check` gets the promised S02 guard: every S02 `text` starts with its PDF text-layer content, and every transcribed line is non-empty.
3. `scope.py`: `performance_figure` uses the forbidden-tag test (a literature_map page gives `precedent_only`). Add claim kind `method_gain` → `precedent_only` (R-CMB-1).
4. `screen.py`: `proposed_fiber.for_method` becomes required (it no longer applies globally).
5. `rules.yaml` R-GEN-3 rewording: MIR in aqueous samples → thin layer or ATR; NIR → pathlength-limited (see R-GEN-4). Not "use ATR" for NIR.
6. `quotes.py` guard words: add units (nm, µm, mm, m, cm-1, %), quantifiers (some, all, most, every), and molar prefixes (millimolar, micromolar, nanomolar).
7. `numbers.py`: "+" sign in ranges ("-5 °C to +40 °C"); time units minutes/hours/days/weeks/months/years; docstring states number checks are claim-local (each claim's own verified quotes + enquiry).
- **Acceptance:** tests for each item; pytest, kb check and ruff all pass; reproducible build.

**1.R2 result (09:06):** all 7 items done; pytest 59/59, kb check 9/9, ruff clean, reproducible build. Phase 1 closed.

---

## Phase 2 — Pipeline MVP (APPROVED 2026-10-17 09:12; dev model deepseek/deepseek-v4-pro-0813; `runs/` gitignored — user)

**Goal.** A working end-to-end assessment pipeline for any enquiry text. It follows the AFS-Ashby steps 0–8 with deterministic checks and provenance, runs on D01–D08, and produces JSON + Markdown. Out of scope here: the cross-family critic, the eval harness, the model bake-off (Phase 3), the chat shell and HTML evidence view (Phase 4).

**Inputs.** The Phase 1 knowledge layer and tools, the dev scenarios (docx D01–D08), and an OpenRouter API key in `.env`, which the user creates (`.env` is gitignored).

### Steps

**2.1 Config + LLM client** (`config.py`, `llm.py`).
- OpenRouter through the OpenAI SDK.
- Models come from `config/models.yaml`: `intake`, `assess` and `repair` roles, pinned ids, no `~latest` aliases.
- `response_format` json_schema strict with `provider.require_parameters=true`; temperature 0; retries on transient errors only.
- Tokens, cost and latency are logged per call.
- A hard spend cap per run and per session lives in config.

**2.2 Scenario loader** (`scenarios.py`). A generic parser:
- `scenarios/dev.jsonl` from the docx (dev enquiry text only; facts and "useful sources" are kept for eval, not shown to the model)
- `scenarios/final.jsonl` from the H txt (enquiry text only)
- The parser splits on the `ID | title` pattern. No scenario IDs appear in the code; the lint stays green.

**2.3 Schemas** (`schema.py`, pydantic → JSON schema).
- **Intake** (steps 0–2):
  - route flags (stackable): in_scope, needs_clarification, premise_to_check, certainty_or_approval_requested, clinical_context, out_of_scope
  - `facts_stated[]`: each item is `{text, enquiry_quote}`
  - `targets[]`: what to measure and why
  - sample slots: `physical_state, optical_regime, aqueous, heterogeneous, fluorophore`. Each is `{value | "unknown", enquiry_quote | null}`.
  - process constraints: location, temperature, pressure, distance/remote analyzer, hazards, cleaning, response time. Each is `{value | "unknown", enquiry_quote}`.
  - `customer_premises[]`
  - `proposed_methods[]` / `proposed_fiber`
- **Assessment** (steps 5–8):
  - `decision_status` ∈ provisional_assessment / insufficient_information / premise_not_supported / outside_supported_scope
  - `premise_checks[]`: `{premise, verdict: supported|contradicted|not_covered, explanation, citations}`
  - `requirements {stated[], unknowns[]}`
  - `clarification_questions[]` (at most 7): `{question, why_it_matters, affects[] (candidate ids or decision), priority}`
  - `recommendations[]`: `{method, technique, role: primary|comparison|conditional|not_recommended, rationale, conditions, citations}`
  - `measurement_concept {probe_and_geometry, location, fiber_link, citations}`
  - `spectral_ranges[]`: `{method, statement, citations}`
  - `risks[]`: `{risk, citations, rule_ids}`
  - `feasibility_plan {samples, reference_measurements, comparison, validation, decision_basis}`
  - `assumptions[]`
  - `not_in_sources[]`
  - Every citation is `{doc, page, quote, claim_kind}`.

**2.4 Pipeline** (`pipeline.py`).
- **S0–2 Intake:** an LLM call with only the enquiry and the slot vocabulary.
- **S3–4 Screen + fiber coverage:** code. Slots taken from the intake; unknown stays unknown.
- **S5–8 Assess:** an LLM call. The context holds:
  - the system prompt (AFS-Ashby procedure + style rules, our words, `prompts/assess.md`)
  - the full page-tagged knowledge base (about 36k tokens, every page, marked `[S01 p.10] …`; S02 text only, not notes)
  - the rules list with ids
  - the screening table and fiber notes
  - the intake JSON
- **D Verify:** code, claim-local. See 2.5.
- **Repair:** an LLM call with the failure list, fixing only the flagged items. At most 2 rounds.
- **Finalize:**
  - remaining failing citations are dropped
  - items left without a valid citation are labelled "engineering judgement (no supporting source)" or removed
  - the status is downgraded where required
  - nothing unverified is shown as verified

**2.5 Deterministic verification** (`verify.py`, MatSage-style `VerificationCheck`/`Report`, hard/soft). Hard checks:
- every citation quote is `exact` or `loose` on its page (`fuzzy_review` = fail; the matched span is never shown)
- the scope check passes for each citation's `claim_kind` (`precedent_only` is allowed only where the text does not assert readiness or proof)
- numbers in each item appear in that item's own verified quotes or in the enquiry (claim-local)
- every intake `enquiry_quote` appears verbatim in the enquiry, so no client fact is invented
- recommended (non-`not_recommended`) items do not include a candidate the screen marked `fail`
- a contradicted premise means the status is not `provisional_assessment`, unless the premise is explicitly corrected in the answer
- every unknown slot that decides a candidate is either asked about or listed as an assumption
- forbidden lexicon: prices/currency, SKU-like codes, "guarantee", "will work", "approved", "validated for", "proven"

Soft checks: length budget; question count ≤7; each question has `affects`.

**2.6 Render** (`render.py`). Markdown following the organizer section order:
- decision status; premise check; requirements (stated vs unknown)
- prioritised questions; recommendations; measurement concept; spectral range; risks
- feasibility plan; assumptions; not in sources; sources
- inline citations `[S01 p.10]`, plus a quotes appendix with ✓ (verified) / ⚠ (flagged) badges
- a verification summary

**2.7 Provenance** (`provenance.py`).
- Each run builds an in-memory tree containing: enquiry, intake, screen, assessment (raw/repaired/final), verifier report, and a manifest (model ids, prompt sha256, knowledge sha256, code git sha, tokens, cost, timings).
- dulwich writes it as one commit on `refs/heads/provenance` through the object API, so the working tree and index are never touched. The commit is tagged `run/<id>`.
- The same files also go to `runs/<id>/` for local viewing (needs a `.gitignore` entry for `runs/`: see decision 3).

**2.8 CLI.**
- `uv run afs-assist assess --text "..." | --file f.txt` prints the Markdown and the output paths.
- `uv run afs-assist run --set dev` runs all dev scenarios → `outputs/dev/<id>.{json,md}`.

**2.9 Tests.**
- Offline tests with a fake LLM client: intake span check, each verify check (passing and failing fixtures), repair-loop flow, finalize downgrade, render, provenance commit in a temp repo, scenario parser.
- One live smoke test, skipped when no API key is set.

### Acceptance checks
- [ ] `uv run pytest`: all offline tests pass; ruff clean; `kb check` passes.
- [ ] D01–D08 run end to end with the dev model, and each output has all sections.
- [ ] 100% of citations shown as verified are exact or loose; failures are visible.
- [ ] 0 unflagged invented numbers.
- [ ] Cost per run is logged and the total stays within budget.
- [ ] Every run has a provenance commit, and `git log provenance` shows them.
- [ ] H01–H06 are **not** run in Phase 2.

### Review
- A reviewer agent checks the code plus D01–D08 outputs against the organizer D01/D02 worked answers and the style rules.
- **G2 (user):** read D01, D02 and two other D outputs.

### Risks
| Risk | Mitigation |
|---|---|
| Model ignores the schema | Strict json_schema + require_parameters; one retry |
| Quotes fail often | Repair loop; prompt shows page text exactly as stored |
| Token cost | About 36k-token context per assess call; with caching it stays mid-tier cheap; spend cap |
| Over-long answers | Length budget + style rules |

### Decisions needed
1. API key: the user puts `OPENROUTER_API_KEY=...` into `.env` (never committed or printed).
2. Phase 2 dev model: proposed `deepseek/deepseek-v4-pro-0813` (cheap, strict JSON supported); alternatively `google/gemini-3.8-flash`. The final choice is the Phase 3 bake-off.
3. Add `runs/` to `.gitignore` (local copies; the durable record is the `provenance` branch).

### Phase 2 first live run: findings
D01–D07 produced; D08 crashed.

| Case | Citations verified | Hard failures left | Cost |
|---|---|---|---|
| D01 | 43/45 | 3 | $0.079 |
| D02 | 30/30 | 0 | $0.022 |
| D03 | 30/30 | 1 | $0.063 |
| D04 | 30/33 | 3 | $0.167 |
| D05 | 28/28 | 1 | $0.069 |
| D06 | 37/37 | 0 | $0.095 |
| D07 | 31/31 | 0 | $0.044 |

Problems:
1. **Bloated, contradictory recommendations.** The model lists every screening row (D01: 13 entries; the same method+technique appears as primary, comparison and not_recommended). The organizer worked answer has 3.
2. **The forbidden-wording check flags negated, cautious phrases** ("not proof that … will work", "do not guarantee"): 3 false positives.
3. **D08 crash.** An intake reply was truncated (DeepInfra, finish=length, about 10k chars); after retries the whole set aborted.
4. **Feasibility-plan steps get invented quotes** (most of the remaining quote failures); the model feels it must cite generic plan steps.
5. Always 7 questions (the maximum); the organizer examples have about 4.

### Phase 2 fixes (2.R) — APPROVED 2026-10-17 09:49 (user), with re-run of D01–D08
1. **Prompt (assess):**
   - Recommend 1–3 method/technique options worth testing, one entry per method+technique.
   - Use `not_recommended` at most 2 times, only for options the customer proposed or a reader would expect.
   - Never list every screening row.
   - Combinations go in a new `combined_with` field (a hypothesis to test).
   - Questions: usually 3–5.
   - Feasibility-plan steps cite a source only where one really fits (e.g. REF §3); otherwise leave `citations` empty (shown as engineering judgement). Never construct a quote.
2. **Schema:** `Recommendation.combined_with: list[Method]` (empty for a single method).
3. **Verifier:**
   - Hard check: method+technique unique across recommendations.
   - Soft check: recommendations ≤5.
   - Forbidden-wording check is negation-aware (ignore a match preceded within about 6 words by not/no/never/cannot/without/do not/does not/is not).
4. **LLM client:**
   - Provider `order` [ionstream, together, deepinfra] (Ionstream first; it was reliable).
   - Intake max_tokens 8000.
   - `finish=length` counts as an invalid reply (retry).
5. **CLI:** `run --set` continues after a failed scenario, records the error, and exits non-zero at the end.
6. **Tests** for 2–5. Then re-run D01–D08 (about $0.6) → reviewer → G2.

### Phase 2 review (2026-10-17, report received 10:18; reviewer agent): APPROVE WITH FIXES
- Verifier sound: 152/152 citations shown as verified are exact on their page (independent check). 20 sampled for meaning: ~4 claims go beyond the quote (Phase 3 critic).
- Acceptance: pytest/ruff/kb check PASS; D01–D08 end to end FAIL (D08); verified citations PASS; invented numbers PASS on outputs (code gap N6); cost logging FAIL (B3); provenance PASS with gaps (B4, N8); H not run PASS.
- Blocking:
  - B1: empty or whitespace `enquiry_quote` passes the verbatim check.
  - B2: finalize only strips citations. No dedupe, no status downgrade, and "Supported" premises are left with no source.
  - B3: discarded (truncated/invalid) replies are not costed; the cap is checked per call, not per attempt.
  - B4: the manifest lacks per-call records (provider, latency), timings, the raw and per-round assessments, and the removed intake items.
  - B5: the headline primary recommendation is a multi-method fusion (5/7 outputs).
  - B6: intake prompt examples may be tailored to held-out wording; line 13 quotes a dev enquiry verbatim.
- Non-blocking:
  - N1: rule paraphrases get quoted as REF (4 of D04's 6 failures).
  - N2: repair feedback is thin.
  - N3: the repair loop keeps the last round, not the best.
  - N4: slot keywords match inside other words.
  - N5: the negation window crosses clauses.
  - N6: some fields are not number-checked.
  - N7: precedent-only citations are not marked.
  - N8: run_id = scenario id, so tags are overwritten.
  - N9: no dirty-tree flag.
  - N10: double period.
  - N11: length 2000–2700 words vs ~450, from padding.
  - N12: claims beyond quotes (Phase 3).
  - N13: `scenarios/final.jsonl` committed (user decision).
- Test gaps: retry/costing, provider order, set-run continuation, scenario parser, finalize, empty quotes, negation bypass, rule-as-quote.

### Phase 2 fixes (2.R2) — APPROVED 2026-10-17 10:23 (user: all items; B6 rewrite + D-012; N13 keep `scenarios/final.jsonl` committed)
Also covers the D08 diagnosis: a repetition loop in the bare enum array `Intake.proposed_methods` (see STATUS 10:13), and the model switch D-011.
1. **Intake schema and prompt** (D08, B6):
   - `proposed_methods` becomes a fixed object with one field per method; each value is a verbatim enquiry quote or null. It is bounded (cannot loop) and quote-checked by the sanitizer. Pipeline and assess context are adapted.
   - The prompt lists only process aspects the enquiry states; missing ones go to `unknowns`, never `enquiry_quote: "unknown"`.
   - The examples are rewritten from REF §3 wording plus neutral invented examples; no enquiry text (B6). Logged as D-012 citing D-007.
2. **verify.py:**
   - B1: a quote needs ≥4 normalized chars and a word character.
   - N4: word-boundary slot keywords.
   - N5: the negation window stops at `; . ,` and "but".
   - N6: number-check requirements, unknowns and not_in_sources.
   - N1: a citation quote that matches a rule statement fails with a hint giving the rule's source quote.
3. **pipeline.py:**
   - N1: the context lists each rule's verbatim source quotes; statements are marked as paraphrase, never to be quoted.
   - B2: deterministic finalize steps, each logged in `removed`:
     - dedupe method+technique, keeping the highest role;
     - force `not_recommended` on a screen fail;
     - downgrade the status on a status-vs-premises or status-vs-recommendations failure;
     - a `supported` premise with no citation left becomes `not_covered`;
     - an inline ⚠ on items that lost a citation or failed a number check.
   - N2: repair feedback includes the matched span for fuzzy quotes.
   - N3: keep the round with the fewest hard failures.
4. **llm.py** (B3): cost discarded attempts (role `<role>:discarded`); `tracker.check()` per attempt.
5. **Provenance and output:**
   - B4: `calls`, `assessment_raw`, per-round repairs, `intake_removed` items and timings go into the JSON and the provenance tree.
   - N8: run_id = `<id>-<utc>`.
   - N9: `code_dirty` flag.
6. **render.py and prompts/assess.md:**
   - B5: `combined_with` is empty for primary (prompt + soft check); combinations are rendered as a later hypothesis.
   - N7: "✓ (precedent only)" badge.
   - N10: fix the double period.
   - N11: caps of ≤6 unknowns, ≤4 risks and ≤5 plan steps; premises only for beliefs or requests that need checking; no boilerplate `not_in_sources`.
7. **Tests** for every item above plus the review's test gaps: retry and costing, set-run continuation, scenario parser.
8. **Re-run D01–D08 on v4.1-flash** (about $0.15) → short re-review → G2.

Deferred to Phase 3: entailment critic (N12), length scoring, eval harness, bake-off, external reference library.

### Phase 2 fixes (2.R3) — APPROVED 2026-10-17 11:20 (user), from the 2.R2 run findings
1. **Methods named in the enquiry, detected in code.** `proposed_methods` leaves the LLM intake schema. Code finds method names in the enquiry with a fixed generic word list (NIR/near-infrared, MIR/mid-infrared/FTIR, Raman, fluorescence, UV-Vis/UV/Vis/ultraviolet). Quotes are verbatim by construction. The result goes to the assess context and the run JSON as "methods the customer named"; the assess model judges whether they are proposed.
2. **Intake prompt: short generic definitions of the physical_state values**, tied to S01 Table 1's sample types: liquid, paste, soft_solid (soft, deformable material such as gels, soft food or soft tissue), powder, solid (rigid).
3. Tests for 1–2; re-run D01–D08 (~$0.2); then an independent review of the outputs plus 9a7e465, 10ff73a and 2.R3; then G2.
