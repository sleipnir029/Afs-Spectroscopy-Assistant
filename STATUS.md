# Status

_Last updated: 2026-10-17 09:06 CEST (Claude)._

**Deadline:** Sun 18 Oct 23:59 Berlin. **Q&A:** Sat 17 Oct 13:38–13:48 (Helios).

## Current phase
**Phase 2: Pipeline MVP.** Plan being written in `PHASES.md` (awaiting approval). Phase 1 closed.

## Phase overview
| Phase | State | Gate | Notes |
|---|---|---|---|
| 0 Repo hygiene and setup | Done (see D-001) | G0 retro-review pending | backup tgz, `.gitignore`, history purged, uv project + deps |
| 1 Knowledge foundation | **Closed** | G1 passed | pytest 59/59, kb check 9/9 | G1 ~13:15 | kb check 8/8, pytest 51/51, ruff clean |
| 2 Pipeline MVP | Plan awaiting approval | G2 ~20:00 | |
| 3 Quality and evaluation | Not planned yet | G3 Sun 09:00 | |
| 4 Chat shell and evidence view | Not planned yet | G4 Sun 14:00 | |
| 5 Freeze | Not planned yet | G5 Sun ~16:00 | |
| 6 Deliverables | Not planned yet | Submit by 22:30 | |

## Done
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
1. User approves the Phase 2 plan (+ decisions: API key in `.env`, dev model, `runs/` gitignore).
2. 13:38 Q&A (user), using the questions in Plan v3 §10.

## Open decisions
- External reference library: after Q&A.
- Product name: later.

## Blockers
None.

## Check results
**Phase 1 (pre-review):** `afs-assist kb check` 8/8 PASS (page counts, scopes, rule ids/effects, string slot values, 58/58 quotes exact, no scenario ids, graph present); `pytest` 21 passed; `ruff check` clean; `kb build` run twice gives identical sha256 for all knowledge files.
Not yet done: visual spot check of 5 pages against the PDFs (assigned to the reviewer).
