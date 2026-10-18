# Review B: code (items 3-6: extensibility, architecture, speed and cost, simplification)

Reviewer: independent, read-only. Repo: <repo> @ eb60291 (master, clean). Date 2026-10-18.

## 1. Verdict: PASS_WITH_CAVEATS

The code is in good shape for a hackathon deliverable: tests are green, ruff is clean, kb check passes, and the frozen pipeline inputs still match the H manifests byte for byte. The caveats:
- three statements in ARCHITECTURE.md are false or misleading;
- there is no "how to extend" documentation at all;
- one repair call, triggered in 24 of 25 assessed runs, eats about 60 % of wall time and 76 % of cost;
- there are about 40 lines of dead or duplicated code.

## 2. Evidence gathered (offline only, no model or network calls)

| Check | Result |
|---|---|
| `uv run pytest -q` | **764 passed, 2 skipped**, 5 warnings (SWIG DeprecationWarnings from pymupdf), 15.07 s |
| `uv run ruff check` | **All checks passed!** |
| `uv run afs-assist kb check` | **10/10 PASS** (page_counts, page_scopes, rule_ids_unique, rule_effects, rule_values_are_strings, source_quotes_exact 77 quotes, no_case_ids, external_library 9/28, s02_text_provenance 20 slides vs PDF, graph_present) |
| Frozen-input check | The current tree's `sha(knowledge_block())`, all five prompt sha256 values, the skill sha256 and the `config/models.yaml` sha256 **equal** the values in the `outputs/final/H01.json` manifest. Since `freeze-1` there are 13 commits. The only files changed under src/prompts/skills/knowledge/config are `src/afs_assistant/chat.py` (+7/-1) and `src/afs_assistant/ui/view.py` (+24/-5), both chat/UI only. |
| Re-verification of `assessment_raw` | I re-ran `verify()` offline on every `assessment_raw` in outputs/final, outputs/dev and outputs/adversarial. It reproduces `hard_failures_before` exactly in all 24 repaired runs (scratch script, not committed). |

Note: the README "Reproducibility" line says 758 passed. The suite is now 764. The README line is dated, so this is fine, but mention it if you refresh the README.

---

## 3. Extensibility (item 3)

How many files a maintainer must touch, and whether that is documented anywhere. **No document anywhere has a "how to extend" section** (grep over README.md, ARCHITECTURE.md, docs/*.md and knowledge/*.md for "how to add", "adding a", "new rule" and so on found nothing relevant).

| Change | Files to touch (code) | Documented? | Traps |
|---|---|---|---|
| **New knowledge PDF** (e.g. S07) | 1. `src/afs_assistant/paths.py:34-40` `SOURCE_PDFS`<br>2. `src/afs_assistant/kb_build.py:124` doc tuple<br>3. `kb_build.py:131` `order` dict (KeyError if missed: fails fast, good)<br>4. `src/afs_assistant/schema.py:18` `Doc = Literal[...]`<br>5. `src/afs_assistant/kb_check.py:10` `EXPECTED_PAGES`<br>6. `knowledge/page_scopes.yaml` (a title and scope for every page, or kb check fails)<br>Then `kb build`, `kb check`. **6 places in 5 files.** | README only covers rebuilding the *existing* archive. | **Silent trap:** if `schema.Doc` is not extended, the strict JSON enum makes the new document impossible to cite. Every claim from it gets dropped or cited elsewhere, and nothing fails. kb check does not compare the doc ids in pages.jsonl with `get_args(Doc)`. Adding pages also changes `knowledge_sha256`, so all outputs change (expected). |
| **New rule** (existing slot vocabulary) | `knowledge/rules.yaml` only, then `kb check` (verifies the quote). **1 file.** | Yes: a good header in `knowledge/rules.yaml:1-30`. | **Silent trap:** kb check does not validate `when` keys or values against `screen.SLOT_VALUES` / `METHOD_RANGES_UM` / `TECHNIQUE_FAMILY`. In `screen._when_state` (`screen.py:125-149`) an unknown key reads `slots.get(key, UNKNOWN)`, which gives "maybe". So a typo such as `phys_state: liquid` silently downgrades every matching candidate to `unknown` instead of erroring. Today all screening `when` keys are valid (I checked offline). |
| **New rule needing a new slot** | `schema.py` (Intake/Sample), `pipeline.py:118` and `:137` (`_SAMPLE_SLOTS` / `slots_from_intake`), `screen.py:152-159` `SLOT_VALUES`, `prompts/intake.md`, `rules.yaml` header. **5 files.** | No. | Intake prompt change: changes output. |
| **New spectroscopy method** | 1. `schema.py:14` `Method`<br>2. `schema.py:78` (a duplicated literal)<br>3. `screen.py:18-24` `METHOD_IDS`, plus `TECHNIQUES` / `TECHNIQUE_FAMILY` (`:28-80`) if it brings a technique<br>4. `fibers.py:12-21` `METHOD_RANGES_UM`<br>5. `methods.py:15-26` `METHOD_PATTERNS`<br>6. `ui/diagrams.py:323-333` `RANGES` / `BAND`<br>7. `options.py:30-40` labels and `_SELF_NAMED` for a new technique<br>8. the S01 Table 1 xlsx rows (kb build)<br>9. `rules.yaml` header vocabulary<br>**About 7 code files plus knowledge.** | No. | The method ranges are duplicated in `fibers.METHOD_RANGES_UM` and `diagrams.RANGES`. A Table 1 method missing from `METHOD_IDS` raises KeyError in `screen.candidates` (fails fast, good). |
| **New external source** (API) | 1. `external/clients.py`: search function and parser<br>2. `external/step.py:222-223`: the hard-coded `searches` list<br>3. `step.py:237-240`: an `if api == "europepmc" ... else` dispatch (a third API needs an `elif`)<br>4. `step.py:92` `API_NAMES`<br>5. `step.py:261-300` `fetch()` if it has a full-text path<br>6. `external/http.py:46` intervals<br>**6 places in 3 files**, plus recorded-response tests. | No. | `http.py:46` already holds dead entries for `api.crossref.org` and `export.arxiv.org` (README: "The pipeline never calls Crossref"). |
| **New external library entry** | `scripts/external_library_spec.yaml`, then `scripts/build_external_library.py`, then kb check. **1 file.** | Partly (ARCHITECTURE §7 names the library; no how-to). | |
| **New model** | `config/models.yaml` (or a new `config/bakeoff/*.yaml` plus `AFS_MODELS_CONFIG`): `roles.*.model` / `fallback_model`, `provider_routing.<model>.only` (load-bearing for strict JSON), `prices`, optional `model_params.<model>.omit`. **1 file.** | Yes: README "Models", the models.yaml header, `docs/model-research.md:203` (smoke test advice). | Not documented: how to find strict-JSON endpoints for `only` (the OpenRouter endpoints API, `supported_parameters`). `prices` is only a fallback when `usage.cost` is missing. With no price entry and no `usage.cost`, cost is 0 and the spend cap is blind (`llm.py:270`, `:323-324`). `omit` only supports `temperature` (`llm.py:26`). |
| **New chat block** | 1. `chat.py:38-39` `BLOCK_TYPES`<br>2. `chat.py:219-223` `block_ids` if it takes an id<br>3. `ui/templates/blocks.html:200-209` an `elif` branch and macro<br>4. `prompts/chat_answer.md:18` block list<br>5. `ui/view.py` `build()` if it needs new data<br>**3-5 files.** | No (ARCHITECTURE "Blocks" lists them only). | The chat_answer prompt change affects chat only, not frozen H. |

**What is missing in the docs:** a short "Extending" section in ARCHITECTURE.md with the six checklists above. That is about 30 lines, documentation only, and changes no behaviour.

---

## 4. Architecture vs code (item 4)

### Blocking (documentation truthfulness: the reader is a judge, and each fix is one line with zero risk)

**B1. `ARCHITECTURE.md:137`: graph.json "Used for lookup and explanations" is false.**
- Evidence:
  - `graph.load()` (`graph.py:99-102`) is called only by `graph.neighbors()` (`graph.py:105-115`), and `neighbors()` has **zero callers** in src, tests or scripts.
  - The only runtime touch of `GRAPH_FILE` is `kb_check.py:85`, which checks that the file exists.
  - `cli.py:18-19` builds the graph and saves it.
  - So graph.json is write-only, and the `networkx` dependency (`pyproject.toml:14`) exists only to write it. No test covers `graph.build()`.
- Fix: replace the sentence with "Built by `kb build` and checked for presence; not read at runtime (the checks live in code)." Optionally delete `neighbors()` (11 lines).
- Risk: none.

**B2. `ARCHITECTURE.md:91`: "A time budget caps the whole step" is false.**
- Evidence: `external/step.py:91` `STEP_BUDGET_S = 60.0  # wall time for searching and fetching`. The two LLM calls (`external_queries`, `external_evidence`) are outside the budget, each with its own 180 s timeout (`config/models.yaml:19-20`).
- Worst case: about 60 s + 2 × 180 s × 2 attempts.
- Fix: "A 60 s budget caps searching and fetching; the two model calls have their own per-role timeouts."
- Risk: none.

**B3. `ARCHITECTURE.md:33`, `:96-97`: Render and Provenance are listed as steps 8-9 of "Pipeline steps (`pipeline.py`)", but `pipeline.run` does neither.**
- Evidence:
  - `pipeline.run` (`pipeline.py:514-615`) returns a `RunResult`.
  - Rendering, `code_sha`, `code_dirty` and the provenance commit all happen in `cli._assess_one` (`cli.py:41-65`).
  - The UI reaches them by importing that private CLI function (server.py docstring line 8).
  - A library caller of `pipeline.run` gets no provenance and no code sha.
- Fix: rename the heading to "Pipeline steps (`pipeline.py`, steps 8-9 in `cli._assess_one`)".
- Risk: none.

### Non-blocking

- **N1. `ARCHITECTURE.md:16`, `:73`: "The repair model is a different, stronger model".** This is true for mix-a only. Under `config/bakeoff/baseline-v4.1-flash.yaml` it is the same model. Add "(in the production config)".
- **N2. Package depends on the repo `scripts/` folder at runtime.** `evaluate.py:71-77` loads `scripts/check_cost_class.py` and `scripts/check_mermaid.py` with `importlib`, by path from `paths.ROOT`. `afs-assist eval` therefore breaks outside a source checkout. This is an inverted layering. Fix after the deadline: move `check_pair` / mermaid helpers into `afs_assistant/checks/` and have the scripts import them.
- **N3. UI depends on a CLI private function** (`server.py` uses `cli._assess_one`). Fix after the deadline: move `_assess_one` to `afs_assistant/runner.py`.
- **N4. Duplicated domain constants (the source of the extensibility traps):**
  - `schema.py:78` repeats the `Method` literal plus `"none"`;
  - `schema.py:77` `ProposedFiber.family` literal duplicates `screen.py:160` `FIBER_FAMILIES`;
  - `fibers.py:12-21` `METHOD_RANGES_UM` vs `ui/diagrams.py:323-331` `RANGES` (same ranges and pages, two encodings).
- **N5. Dead code (verified with an AST scan plus grep over src, tests and scripts):**

  | Item | Location | Refs |
  |---|---|---|
  | `hello()` (uv init leftover) | `src/afs_assistant/__init__.py:1-2` | 0 |
  | `MATERIALS_ZIP` | `paths.py:12` | 0 |
  | `neighbors()` (and so `load()`) | `graph.py:99-115` | 0 |
  | `KINDS` | `chat.py:37` | 0 |
  | `SourceText` Protocol | `external/sources.py:34-37` | 0 |
  | `HOST_INTERVAL_S` crossref/arxiv entries | `external/http.py:46` | APIs never called |
  | `response_mode != json_schema` branch | `llm.py:211-215` | no config or test uses `json_object` |
  | `units.convert` | `units.py:46-47` | tests only (keep: harmless) |
  | `pyproject.toml:4` `description = "Add your description here"` | | judge-visible leftover |
- **N6. Silent failure modes worth a kb check** (see §3): `schema.Doc` vs the doc ids in pages.jsonl, and rule `when` keys/values vs the slot vocabulary.
- **N7. Tests are organised by project history** (`test_phase3_r4.py`, `test_phase5_d061.py`, …), not by module. A maintainer cannot find a module's tests by name. Not worth changing now.

---

## 5. Speed and cost (item 5)

### Where the time and money go (from `calls` in every run JSON)

| Set | Wall (sum) | Cost | intake | assess | **repair** | external (2 calls + HTTP) |
|---|---|---|---|---|---|---|
| H01-H06 | 887 s | $0.288 | 44 s / 6.9 % | 272 s (30.6 %) / 15.1 % | **537 s (60.5 %) / 75.8 %** | about 5 s per case; LLM part 2.2 % of cost |
| D01-D08 | 1005 s | $0.350 | 5.2 % / 6.4 % | 21.9 % / 17.7 % | **66.1 % / 73.5 %** | about 1 % |
| A01-A12 | 1009 s | $0.385 | 8.3 % / 10.2 % | 27.1 % / 18.9 % | **56.6 % / 67.7 %** | about 1 % |

Screen, verify and finalize are code and together take under 0.1 s per case.

### Repairs: triggered in 24 of 25 assessed runs
- The rate is 6/6 H, 7/8 D (all but D01) and 11/11 A (A12 is off-topic).
- Round 2 never ran: every repair took the run from N hard failures to 0 in round 1 (`kept_round` 1 everywhere). `MAX_REPAIR_ROUNDS = 2` (`pipeline.py:53`) has never been needed on mix-a.

Hard failures that triggered the repair (offline re-verify of `assessment_raw`, 77 failures over 24 runs):

| Check | Count | Share |
|---|---|---|
| `numbers_claim_local` | 32 | 42 % |
| `numbers_uncited_text` | 12 | 16 % |
| `citation_scope` | 10 | 13 % |
| `recommendations_unique` | 7 | 9 %; finalize fixes this deterministically anyway (`pipeline.py:272-286`) |
| `quote_verified` | 7 | 9 % |
| other (`option_recommended_tier` 2, `parameter_method_in_option` 2, `unknown_slot_addressed` 2, `extended_two_methods`, `plan_step_text`, `forbidden_wording`) | 9 | 11 % |

**58 % of repair triggers are number-provenance checks.** The figures recur across cases. They are domain constants, not case facts:
- `785 nm`: cited on S01 p.11, but the figure is on S01 p.15;
- the fiber windows `1.1-6.5 um` and `3-17 um`: `screen.py:278-280` hands these to the model in the screening notes, without a quotable citation;
- `1-10 mm`, `100-300 m`, `1-2 m`, `350-2400 nm`.

**A checker false positive (5 of 38 failing figures):**
- `numbers.unsupported_numbers` (`numbers.py:154-155`) accepts a range only if the *same range* appears in an allowed text.
- The S02 p.6 chart labels give the endpoints separately. So `H04 spectral_ranges[0]` "PIR fibers transmit about 3-17 um", citing the verified quote `"3000 nm Polycrystalline Infrared Fibers 17 μm"`, fails even though its own quote supports it.
- Same pattern: `H02 measurement_concept` (350-2400 nm), `H04 measurement_concept` (1.1-6.5 um), D03, A03.
- In no run is this the *only* failure, so fixing it alone would have removed 0 repairs. It is a correctness fix, not a speed fix.

**Why repair is slow:**
- The repair rewrites the whole Assessment JSON. Visible output is about 4-5.5k tokens, the same as the assess output.
- Its completion is 7k-29k tokens. Estimating visible size as JSON chars / 3.6, roughly **42-81 % of repair completion is hidden reasoning** (Gemini 3.8 Flash, `reasoning.effort: medium`, `config/models.yaml:18`).
- Over H, that is about 56k reasoning tokens: about $0.105 (36 % of H cost) and about 360 s at the measured 157 tok/s.
- **This is an estimate** (a chars-per-token heuristic). OpenRouter can report reasoning tokens separately, but `_account` (`llm.py:315-324`) does not record `completion_tokens_details.reasoning_tokens`.

### Prompt caching (`cached_tokens`)
- H: 255k of 589k prompt tokens cached (43 %).
- **assess** (GLM via BaseTen): a cache hit in 3/6 H cases (32,768 tokens).
- **repair** (Gemini): a hit in 4/6 (about 39.4k tokens, which is exactly the shared `assess_system()` prefix).
- intake and external calls: never cached (prompts too short).
- The hits are cross-case and implicit (no `cache_control` is sent; `docs/model-research.md:126`, `:256`, citing https://openrouter.ai/docs/features/prompt-caching: "Gemini implicit").
- Within one run the repair cannot reuse the assess cache, because it is another model.
- Measured price effect:
  - Gemini cached input bills at about 10 % (H01 repair: 39,327 cached tokens cost about $0.0015 vs about $0.0147 uncached);
  - so a 100 % hit rate would have saved about $0.027 on repair plus about $0.014 on assess, **about $0.04 of $0.288 (14 %), with about 0 s latency gain**;
  - interactive UI runs after an idle period will miss anyway (cache TTL).

### Sequential calls that could be parallel
- The critical path intake → screen → assess → verify → repair → finalize → external is strictly data-dependent. External gaps come from the *final* assessment. **No safe in-run parallelism with a meaningful gain exists.**
- Inside the external step, the Europe PMC and OpenAlex searches are serial (`step.py:227-256`), but the whole step takes 4-7 s, of which about 2-3.5 s is the two LLM calls.
- Parallel searches would save at most about 2 s per case (about 2 %). They would also reorder `search_log` and the hit ranking input (`_rank_hits` uses arrival order, `step.py:314-325`): **changes output**. Not worth it.
- Set runs are already parallel (`--workers 4`, `cli.py:110`).

### Proposed changes, ranked by gain / risk

| # | Change | Gain (est.) | Risk | Output? |
|---|---|---|---|---|
| P1 | Record `reasoning_tokens` in `_account` / `SpendTracker.add` (`llm.py:135-138`, `:315-324`). New key in `calls` only. | Measurement, so P2 can be decided on data | Very low. New field only; old run JSONs lack it (readers must use `.get`). | Adds a field to future run JSON. Pipeline answers unchanged. |
| P2 | `repair.reasoning.effort: medium → low` (`config/models.yaml:18`) | Up to about 35-40 % of wall and cost per repaired case (from the reasoning-share estimate) | Medium: repair success is now 24/24 to 0 failures, and that may drop. Needs a D+A re-run (about $0.7). | **Changes output; needs user decision** |
| P3 | Put a quotable citation next to code-made figures: in `screen.py:278-280` notes, append the fiber's verbatim `sources[].quote` and its page, so the model cites S02 p.6 for the window it copies. | Removes a recurring `numbers_claim_local` source | Low-medium | **Changes output (assess prompt input); needs user decision** |
| P4 | `numbers.py:154-155`: accept a range when both endpoints occur with the same dimension in *one* allowed text | Fixes 5/38 false positives. 0 repairs avoided in recorded data. | Medium: loosens a shared check (also chat and external `check_item`, `step.py:465`). An unrelated pair of numbers in one quote could pass. | **Changes output (verify, chat, external replay); needs user decision** |
| P5 | Skip repair when every hard failure is finalize-handled (`recommendations_unique`) or a number check that finalize flags | Would skip 8/24 repairs (H01, H02, H04, H06, D04, A03, A07, A11), about 50-130 s each | High: leaves flagged figures, which fail checklist item `no_flagged_figures`. A quality regression. | **Changes output; needs user decision. Not recommended.** |
| P6 | Patch-style repair (send failing items, receive only the replaced items) | Largest structural gain: repair output from 7-29k tokens to perhaps 1-3k | High effort and new schema | **Changes output; post-deadline only** |
| P7 | Explicit `cache_control` for the Gemini repair prefix | At most about 9 % cost, about 0 latency | Request shape changes (content parts); provider support under `only` routing unverified | Same prompt text; reruns differ anyway. Not before the deadline. |

---

## 6. Simplification without changing frozen behaviour (item 6)

Every item below keeps prompt bytes, schema bytes and pipeline output identical. **Pre-condition for all of them:** add the sha-pin test from §7 first, so a "safe" refactor that alters `knowledge_block()` or a schema fails loudly.

| # | Where | What | Lines saved | Risk |
|---|---|---|---|---|
| S1 | `pipeline.py:137` | `for name in _SAMPLE_SLOTS:` instead of re-listing the 5 slot names (the tuple already exists at `:118`) | 0 net; one source of truth | None |
| S2 | `pipeline.py:288-296` and `:450-459` | Two copies of "renumber `flagged` paths after an index remap". Extract `_renumber(flagged, prefix, new_index) -> dict`. | about 8 | Low; finalize tests cover both |
| S3 | `chat.py:181-188` vs `pipeline.py:100-104` | Same page-block text built twice. Have `knowledge_block()` start with `pages_block()` (move it to `pipeline` or `kb`), and assert `sha(knowledge_block())` unchanged. | about 6 | Low **if** the sha-pin test exists. The bytes must stay identical: current sha equals the H01 manifest `knowledge_sha256`. |
| S4 | `pipeline.py:77-78`, `external/sources.py:30-31`, `kb_build.py:34-35`, `evaluate.py:614-616` | Four sha256 helpers. Keep one (`kb.sha256_text`), import it elsewhere. | about 6 | None |
| S5 | `external/step.py:133-135` vs `pipeline.py:81-83` | Two identical `prompt()` loaders (step cannot import pipeline: circular). Move `prompt()` to `kb.py` or `paths.py`. | about 3 | None |
| S6 | `external/step.py:546-550` vs `:589-595` | The external block dict literal is written twice with the same keys. A `_block(mode, gaps, error=None, **over)` helper. | about 6 | Low; `test_phase4` covers `failed_block` |
| S7 | `schema.py:78` | `for_method: Literal[Method, "none"]`. I verified offline that pydantic emits the **identical** JSON schema (same enum, same order). Optionally derive `screen.FIBER_FAMILIES` from `get_args(ProposedFiber.model_fields["family"].annotation) - {"none"}`. | 0; removes an extensibility trap | Very low (assert the `Intake.model_json_schema()` sha is unchanged) |
| S8 | `evaluate.py:80-83` | `_table1()` re-reads `TABLE1_FILE`. Use `tuple(kb.table1())`. | 3 | None |
| S9 | Dead code (N5) | Delete `hello`, `MATERIALS_ZIP`, `graph.neighbors` (and `graph.load` if nothing else needs it), `chat.KINDS`, `SourceText` (plus its `Protocol` import), the crossref/arxiv interval entries, the `json_object` branch in `llm.py:211-215` (replace with `if cfg.get("response_mode", "json_schema") != "json_schema": raise ValueError(...)`). Fix the `pyproject.toml:4` description. | about 30 | None. Run pytest. Check that none of the 2 test refs to `hello` import it (they don't: `tests/test_ui.py:90` is a query string). |
| S10 | ARCHITECTURE.md | Fix B1-B3 and N1. Add the "Extending" checklists (+about 30 lines). | n/a | None |

Total: about 65-70 lines of code removed (S2-S9), no behaviour change. **Recommendation:** before the deadline do only S9's `pyproject` line, B1-B3 and the sha-pin test. Do S1-S9 after submission. Each step is cheap, but it is churn on a frozen tree, and the reward on judging day is zero.

---

## 7. Test gaps

1. **No test pins the frozen prompt bytes.** No test asserts:
   - `sha(pipeline.knowledge_block())`;
   - `sha(pipeline.assess_system())`;
   - the sha of `Assessment.model_json_schema()` / `Intake.model_json_schema()`.

   So a refactor (S3, S7) could silently change what the model sees. Add `tests/test_frozen_inputs.py`, with constants copied from the freeze manifest: `knowledge_sha256`, `prompt_sha256`, `skills_sha256`, plus strict-schema sha values computed now.
2. **No test for `graph.build()`** (or delete the graph).
3. **No test for chart-label quotes** in `numbers.unsupported_numbers` (`"3000 nm … 17 μm"` vs `"3-17 um"`). Add an xfail or documenting test today, whatever P4 decides.
4. **No kb check that every doc id in pages.jsonl is in `schema.Doc`.**
5. **No kb check that rule `when` keys/values are in the slot vocabulary** (`screen.SLOT_VALUES`, `METHOD_RANGES_UM`, `TECHNIQUE_FAMILY`). Exclude the `claim` / `evidence_scope` keys, which `scope.py` handles.
6. **`reasoning_tokens` not recorded**, so cost attribution (P2) cannot be tested or decided on data.
7. **`afs-assist eval` from an installed wheel** (N2) is untested and would fail.

## 8. Smallest next patch (zero output change, about 30 minutes)

1. `ARCHITECTURE.md:91`, `:33`/`:96-97`, `:137`, `:73`: the four one-line truth fixes (B1-B3, N1).
2. `pyproject.toml:4`: a real description.
3. `src/afs_assistant/kb_check.py`: two new findings:
   - `doc_ids_in_schema`: `set(doc for doc, _ in kb.pages()) == set(get_args(schema.Doc))`;
   - `rule_when_vocabulary`: for effect in {exclude, require, warn}, every `when` key in {method, technique, *SLOT_VALUES} and every value allowed.
4. `tests/test_frozen_inputs.py`: the sha pins from §7.1.

Then run `uv run pytest -q`, `uv run ruff check` and `uv run afs-assist kb check`. Stage the named paths only.

---

## Executive summary (10 lines)

1. Checks: pytest 764 passed / 2 skipped; ruff clean; kb check 10/10 PASS. Frozen pipeline inputs (knowledge, prompts, skill, models config) still match the H manifest sha256.
2. Verdict PASS_WITH_CAVEATS. The code is sound; the caveats are false doc claims, missing extension docs and a repair-dominated cost profile.
3. Blocking (docs only): ARCHITECTURE says graph.json is "used for lookup" (it is write-only and `neighbors()` has no caller), that a time budget caps the whole external step (only search and fetch), and lists render/provenance as `pipeline.py` steps (they are in `cli._assess_one`).
4. Extensibility: a rule or model change is 1 file and documented. A PDF is 6 places / 5 files; a method about 7 files; an external API 6 places / 3 files; a chat block 3-5 files. None of these is documented.
5. Two silent traps: a new doc not added to `schema.Doc` can never be cited, and a typo'd rule `when` key turns candidates "unknown". Neither is caught by kb check.
6. Repair fires in 24/25 assessed runs (6/6 H) and takes 60 % of H wall time and 76 % of H cost. Round 2 was never needed.
7. 58 % of repair triggers are number-provenance checks on recurring domain figures. 5/38 failing figures are checker false positives (range endpoints given separately in an S02 p.6 chart-label quote).
8. Repair output is roughly 42-81 % hidden reasoning (estimate). Lowering the repair reasoning effort is the biggest lever, but it changes output and needs a user decision.
9. Caching: 43 % of H prompt tokens were cached, implicitly and across cases. A perfect hit rate would save about 14 % of cost and no latency. No meaningful safe parallelism exists.
10. Simplification: about 65-70 lines of dead or duplicated code can go with no behaviour change. Pin the prompt and schema sha first, and do it after submission.
