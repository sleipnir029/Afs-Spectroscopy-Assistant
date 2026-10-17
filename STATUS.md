# Status

_Last updated: 2026-10-17 10:50 CEST (Claude)._

**Deadline:** Sun 18 Oct 23:59 Berlin. **Q&A:** Sat 17 Oct 13:38–13:48 (Helios).

## Current phase
**Phase 2: Pipeline MVP.** Review: APPROVE WITH FIXES. 2.R2 approved and implemented (5479553..4455326). Re-review: APPROVE WITH FIXES; BF1/BF2/N-a fixed in 9a7e465 (Claude, not yet reviewed). The D01–D08 run on 2.R2 code started 10:41. Next: check that run → short independent review (outputs + 9a7e465) → G2. N-b fixed in 10ff73a (10:50, D-014, user: "choose whatever makes it better"). Caveat: the running set loaded the 9a7e465 code at 10:42, so it does not include N-b, and the code_sha of its later scenarios may name a newer commit than the code it ran.

## Next session starts with (handoff 09:55)
Session rule (user): ≤200k tokens per session, one phase or task per session.
1. Read `CLAUDE.md`, this file, `PHASES.md` (Phase 2 section incl. "first live run findings" and 2.R) and `DEVIATIONS.md` (D-009, D-010).
2. Check the D01–D08 re-run in `outputs/dev/*.json|md`. Summary numbers are below under "Check results"; `git log provenance` lists the runs.
3. Launch an independent reviewer agent on Phase 2: code (`src/afs_assistant/{llm,pipeline,verify,render,provenance,schema,scenarios,cli}.py`, `prompts/`) plus outputs D01/D02 vs `scenarios/dev_reference.jsonl` (organizer worked answers) and the REF §3 style rules. Fix blocking findings (plan → approve → fix).
4. G2: the user reads D01, D02 + 2 others. Then close Phase 2 and write the Phase 3 plan (critic, external reference library, adversarial set, eval harness, bake-off, baseline table) for approval, in a new session.
Known open points for Phase 3: claims that go beyond their valid quotes (needs critic/entailment); output length; external references (approved in principle); jury may run the repo themselves or ask for a live run (both).

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
- Product name: later.

## Blockers
None.

## Check results
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
