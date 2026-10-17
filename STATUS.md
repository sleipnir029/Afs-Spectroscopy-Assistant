# Status

_Last updated: 2026-10-17 12:22 CEST (Claude)._

**Deadline:** Sun 18 Oct 23:59 Berlin. **Q&A:** Sat 17 Oct 13:38–13:48 (Helios).

## Current phase
**Phase 2: Pipeline MVP.**
- **Code:** 2.R2 and 2.R3 are implemented. The independent review of Claude's commits 9a7e465, 10ff73a and 315a90a was APPROVE WITH FIXES (B1: an unverified contradiction behind the model's own status; B2: the negation aside let "No, honestly, it will work" through). Fixed in 75a4469 (D-014 amended, D-016).
- **2.R4 (12:09):** implemented with tests (spectral-range and plan-step checks, combination key, two assess-prompt lines, dash aside, fluorimetry words; D-018). Not yet reviewed; D01–D08 re-run not done.
- **Checks:** pytest 189 passed, 1 skipped; ruff clean; kb check PASS.
- **Run:** done (11:53, see Check results); the D01–D08 run on 75a4469 had started 11:29; the run on 315a90a was stopped at D03.
- **Next:** check the run → independent review of the outputs (and the 75a4469 diff) → G2 (user reads D01, D02 + 2 others) → close Phase 2 → Phase 3 plan in a new session.

## Next session starts with (handoff 09:55)
Session rule (user): ≤200k tokens per session, one phase or task per session.
1. Read `CLAUDE.md`, this file, `PHASES.md` (Phase 2 section incl. "first live run findings" and 2.R) and `DEVIATIONS.md` (D-009, D-010).
2. Check the D01–D08 re-run in `outputs/dev/*.json|md`. Summary numbers are below under "Check results"; `git log provenance` lists the runs.
3. Launch an independent reviewer agent on Phase 2: code (`src/afs_assistant/{llm,pipeline,verify,render,provenance,schema,scenarios,cli}.py`, `prompts/`) plus outputs D01/D02 vs `scenarios/dev_reference.jsonl` (organizer worked answers) and the REF §3 style rules. Fix blocking findings (plan → approve → fix).
4. G2: the user reads D01, D02 + 2 others. Then close Phase 2 and write the Phase 3 plan (critic, external reference library, adversarial set, eval harness, bake-off, baseline table) for approval, in a new session.
Known open points for Phase 3 (from the reviews; updated 12:05):
- **Entailment critic** for claims beyond their quotes: D01 flush-mount geometry cited to the dairy page, D03 "amide" bands, D06 "(including by water)", D02 off-domain precedents. Also a domain-error check: D07 dismisses NIR transmission in a melt.
- **Length:** 1,700–2,100 body words vs ~450; soft, user.
- **Premise policy:**
  - at most 3 premises;
  - a precedent-only verdict instead of "Supported" (REF §3: a published application is "not proof");
  - a reverse check: `premise_not_supported` with no contradicted premise.
- **Gate the "no MIR link length" line on relevance** (rules.yaml ~250; D-007 theme).
- **Primary-count rule:** D01 has two primaries.
- **Redesign the negation logic** with broader false-positive and false-negative tests ("and"/"so"/"since" clauses; "Nothing here is a guarantee").
- **Intake noise:** "unknown" placeholders are shown as "not quoted verbatim" removals.
- **`code_dirty`:** exclude `outputs/`.
- **Cosmetic labels:** e.g. "Raman, raman probe".
- **Review the S02 p.6 figure-text quotes.**
- **Eval harness, bake-off, external reference library, adversarial set:** as planned.
- **Jury:** may run the repo themselves or ask for a live run (both).

## Phase overview
| Phase | State | Gate | Notes |
|---|---|---|---|
| 0 Repo hygiene and setup | Done (see D-001) | G0 retro-review pending | backup tgz, `.gitignore`, history purged, uv project + deps |
| 1 Knowledge foundation | **Closed** | G1 passed | pytest 59/59, kb check 9/9 | G1 ~13:15 | kb check 8/8, pytest 51/51, ruff clean |
| 2 Pipeline MVP | In progress | G2 ~20:00 | |
| 3 Quality and evaluation | Not planned yet | G3 Sun 09:00 | |
| 4 Chat shell and evidence view | Not planned yet | G4 Sun 14:00 | |
| 5 Freeze | Not planned yet | G5 Sun ~16:00 | |
| 6 Deliverables | Not planned yet | Submit by 22:30 | |

## Done
- **Jury input (12:22, relayed by the user; paraphrase, not verbatim):**
  - The system should always make a proposal, even when the supplied data does not cover the question.
  - If the information is not in the system, it should search online (research papers, proper scientific forums), analyse what it finds and explain how it can be used.
  - It must be able to analyse how a multispectral system can be used for a chemical process.
  - → A re-plan of Phases 3–6 is needed (what we have, what we plan, what can be integrated). Clarifying questions asked; no code changes until a plan is approved.
- **Decisions on the jury input (12:24, user):**
  - "Multispectral system" = several spectroscopy methods combined on one process, plus how their data are fused (not imaging).
  - Search mode = live search when the supplied sources do not cover the question, with the curated external library as the offline fallback; every external quote is fetched and verified verbatim.
  - Sources = free scholarly APIs (OpenAlex, Semantic Scholar, arXiv, Europe PMC, Crossref) plus general web search; external sources are always marked secondary.
  - Process = a background research agent now (notes in `docs/research-replan.md`); the full re-plan of Phases 3–6 is written in the next session for approval.
- **Research done (865da99, `docs/research-replan.md`).** Recommendation: option B (curated library first, then keyless scholarly APIs only on an evidence gap; fetch, verify verbatim and cache every source; a separate secondary-evidence section; a required proposal block; ~14–17 h). Option C (web plugin behind `--web`) is a stretch. Notes: OpenAlex keyless = a shared ~100 searches/day per IP; Semantic Scholar returned 429 without a key.
- **Decisions (12:31, user):**
  - Git gets the metadata, verified quotes and sha256 of fetched sources; full fetched text stays in a local gitignored cache (confirm the exact path at planning).
  - General web search is off by default, enabled by a flag.
  - Add a required Proposal block and keep the honest decision status.
  - Final H01–H06 runs: live search once, then freeze (cache and replay).
  - Still open: optional OpenAlex key, and which contact email to use for Unpaywall/Crossref.
- Dev model switched to `deepseek/deepseek-v4.1-flash` (10:15, user; D-011). Providers [deepinfra, atlas-cloud, coreweave] (fp8, strict JSON); max_tokens 16k/32k/32k (reasoning tokens count). Smoke test: the D08 intake runs clean on flash (DeepInfra, finish=stop, $0.0031, proposed_methods [MIR, Fluorescence]). pytest 84 passed, 1 skipped. D01–D07 outputs are still from v4-pro: re-run on flash before G2.
- Decisions (09:29, user):
  - External reference library: **yes**. Curated, each entry with URL + verbatim quoted passage, marked secondary; to be planned in Phase 3.
  - Jury evaluation: **may be both** (jury runs the repo with their own key, and/or asks us to run an enquiry live). We therefore need a reproducible repo (README, fresh-clone test, own key) and a robust live demo (pinned providers, saved-run replay fallback, video).
- Live smoke run (09:27, generic ethanol enquiry; not a dev or final case):
  - End to end in 2.5 min, $0.064 (provider pinning D-010 after a first empty response).
  - 22/24 citations verified. The 2 removed were a quote taken from the organizer's worked answer (not in our knowledge base) and a quote spanning a page break; both were correctly caught.
  - 3 unverifiable intake items were sanitized.
  - Observed for Phase 3: claims that go beyond their (valid) quotes, e.g. "ethanol has characteristic NIR bands"; only an entailment check / critic can catch these. Output length is above the organizer examples.
- Phase 2 offline (09:19): LLM client (strict JSON, cost tracking, spend caps), scenario parser (8 dev, 2 worked references, 6 final), schemas, prompts (intake/assess/repair), pipeline, claim-local verifier, intake sanitizer (D-009), renderer, dulwich provenance, CLI. pytest 74 passed + 1 live test skipped.
- Decisions (09:12): Phase 2 approved; dev model deepseek/deepseek-v4-pro-0813; `runs/` gitignored; the user adds the key to `.env`.
- Phase 1 closed (09:06): 1.R2 leftovers fixed (transflection exception scoped to R-GEO-5, S02 provenance guard, performance_figure/method_gain scope, `for_method` required, R-GEN-3 reworded, unit/quantifier guard words, `+` ranges and time units). pytest 59/59, kb check 9/9.
- 1.R fixes:
  - R1: fuzzy quote matches become `fuzzy_review` (not verified); a changed number or negation is rejected.
  - R2: S02 `text` = PDF text layer + transcribed image text; our descriptions moved to `notes` (never quotable).
  - R3: R-FIB-2 corrected (MIR samples are 1–2 m lab lengths; no source gives an MIR link length); slide-10 legend added.
  - R4: number check matches value + unit dimension and whole ranges.
  - R5: warnings filtered by target; opaque transflection is `unknown`; slots validated; `proposed_fiber` per method; `opaque_absorbing`.
  - R6: scope check derived from R-EVI-1; readiness is at best `precedent_only`.
  - R7: 9 rule wording/quote fixes plus 5 new generic rules (44 rules / 76 exact quotes).
  - R8: private-use glyphs mapped, unit guards, `.gitignore` comment.
- Design note for Phase 2: number provenance must be claim-local (a claim's numbers are checked against that claim's own cited quotes); a KB-wide pool lets e.g. a silica '300 m' pass on an MIR claim.
- Review: APPROVE WITH FIXES. Decisions: fix all R1–R8; B8: keep `pages.jsonl` committed (user).
- 1.1 `normalize.py` (NFKC, keep line-break hyphens, collapse whitespace; `loose()` for tolerant matching).
- 1.2 `pages.jsonl`: S01 19, S03 17, S04 6, S05 2, S06 1, REF 2; reproducible (identical sha256 on rebuild).
- 1.3 `s02_slide_notes.md`: 20 slides (verbatim slide text, our figure descriptions, uncertain readings).
- 1.4 `page_scopes.yaml`: all 67 pages tagged (D-004 adds `guidance`).
- 1.6 `rules.yaml`: 39 generic rules, 58 source quotes, all exact matches.
- 1.7 `graph.json`: 156 nodes / 220 edges (pages, rules, table rows, techniques, sample types, fibers, methods).
- 1.8 tools: `units`, `fibers` (coverage), `screen` (method×technique: pass/fail/unknown), `quotes` (exact/loose/fuzzy + offsets + page sha256), `numbers` (unsupported-number flagging), `scope` (claim kind vs page scope).
- 1.9 CLI: `uv run afs-assist kb build` / `kb check`; the build is byte-reproducible.
- 1.10 `tests/test_phase1.py`: 21 tests.
- Bugs caught by our own checks and fixed: (a) one regime slot mixed state and optics (D-005); (b) a shadowed variable failed ATR for liquids (regression test added); (c) YAML `yes` parsed as boolean, so the fluorophore requirement never passed (quoted, plus a new `kb check` guard).
- 1.5 `table1_methods.json` (19 rows, path in mm) and `fibers.json` (7 fiber families with S02 p.6 quotes).
- Decision: docx §3/§5 citable as `REF`; D01–D08 and the worked answers are dev/eval data only.
- Phase 0. Verified: `git rev-list --objects --all` shows 0 objects under `resources/`; files still on disk; backup at `~/Desktop/aails-backup-2026-10-17.tgz`.

## Next
1. Phase 2 offline parts (config/LLM client, scenarios, schema, pipeline, verify, render, provenance, CLI, tests), then D01–D08 live runs.
2. 13:38 Q&A (user), using the questions in Plan v3 §10.

## Open decisions
- Output length (11:23, user): not a hard rule; minimise later (Phase 3). The soft length check stays a warning.
- Product name: later.

## Blockers
None.

## Check results
**Final Phase 2 dev run (finished 11:53), flash, code 75a4469, session cost $0.1455:**
- **Completion:** all 8 complete; 0 hard failures, 0 still open, 0 finalize corrections; citations 254/254 verified.
- **Status:** provisional ×8.
- **D08 fixed:** named methods MIR + fluorescence; state soft_solid; MIR-ATR primary, fluorescence comparison.
- **Shape:** questions 5–6; body 1,683–2,141 words (length deferred, user).
- **Cost:** $0.014–0.033 per case.
- Committed 7f3022a. Independent pre-G2 output review started 11:54.

**2.R2 run (finished 11:12), flash, code 9a7e465, session cost $0.1855:**
- **Completion:** all 8 complete; 0 hard failures; citations 304/304 verified; no finalize corrections needed.
- **Status:** provisional ×7, D02 premise_not_supported.
- **Shape:** recommendations 3–4, a single method as primary; questions 5–6; risks 4 each.
- **Cost and length:** $0.015–0.036 per case. Body (before Evidence) 1,616–2,483 words vs 2,100–3,650 total before; still far above the ~450 of the organizer examples and the 1,800 soft budget.

Problems found:
1. **`proposed_methods` is null in all 8 cases.** It is not the sanitizer: the model returns nulls and puts named methods into `process` as `existing_equipment`. Removing the schema docstring did not help (live A/B on D08, $0.004).
2. **D08 shows MIR-ATR as not_recommended although the customer asked for it.** Intake classified chicken muscle/fat/liver as `solid`, not `soft_solid`, so R-MIR-2 fails ATR. The screen is right for its input; the intake prompt never defines the physical_state values.
3. **Placeholder `"unknown"` process items** still appear (D01, D02, D08) despite the prompt; the sanitizer removes them (soft).

**Flash baseline, pre-2.R2 code (finished 10:40), deepseek-v4.1-flash, session cost $0.1415:** all 8 complete (D08 too); hard failures 0 in every case; citations 271/271 verified; status provisional ×7, D08 insufficient_information; recs 2–5; questions 5–6; cost $0.015–0.022 per case. Markdown 2,082–3,656 words (longer than v4-pro's 2,000–2,700). Committed 67ce484.

**Phase 2 re-run after 2.R (10:10), dev model deepseek-v4-pro-0813, session cost $0.345:**

| Case | Status | Recs | Questions | Citations verified | Hard failures left | Repair rounds | Cost |
|---|---|---|---|---|---|---|---|
| D01 | provisional | 4 | 6 | 21/21 | 0 | 1 | $0.047 |
| D02 | provisional | 4 | 5 | 24/25 | 1 | 2 | $0.057 |
| D03 | provisional | 4 | 5 | 17/17 | 1 | 2 | $0.047 |
| D04 | provisional | 3 | 5 | 18/23 | 6 | 2 | $0.057 |
| D05 | provisional | 5 | 5 | 22/22 | 0 | 1 | $0.040 |
| D06 | insufficient_information | 5 | 5 | 25/25 | 0 | 1 | $0.041 |
| D07 | provisional | 4 | 5 | 25/26 | 1 | 2 | $0.055 |
| D08 | **FAILED** | — | — | — | — | — | — |

- Recommendations dropped from up to 13 to 3–5; questions from 7 to 5–6.
- **D08 still fails at intake:** the reply is truncated at max_tokens 8000 (19k chars; Ionstream). The same scenario failed in both runs, so it is likely a degenerate or repetitive intake output for this enquiry. Fix next session (e.g. cap intake list lengths in the schema/prompt, inspect the raw reply).
  - **Diagnosed 10:13** (one raw intake call, $0.024, reply kept in the session scratchpad): a degenerate repetition loop in `Intake.proposed_methods` (a bare `list[Method]` enum array). After the premises the model wrote `"MIR"` 1,427 times until finish=length. At temperature 0 the retries repeat the same loop. Second finding: `proposed_methods` has no `enquiry_quote`, so it is unverifiable; in D02/D06/D07 it lists all 5 methods. Also: unknown process aspects are emitted with `enquiry_quote: "unknown"` (D03–D05: 3–6 per case) and then sanitized. A fix plan (2.R2) will be merged with the reviewer findings.
- D04 has the most remaining failures (6); inspect them in the review.

**Phase 1 (pre-review):** `afs-assist kb check` 8/8 PASS (page counts, scopes, rule ids/effects, string slot values, 58/58 quotes exact, no scenario ids, graph present); `pytest` 21 passed; `ruff check` clean; `kb build` run twice gives identical sha256 for all knowledge files.
Not yet done: visual spot check of 5 pages against the PDFs (assigned to the reviewer).
