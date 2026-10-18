# Final review: fix plan (2026-10-18 14:20 CEST)

Reports: `A-brief-and-outputs.md` (items 1–2), `B-code.md` (3–6), `C-deliverables.md` (7–9), `D-repo.md` (10).
Author e-mail addresses and local paths are redacted in the committed copies.

**Verdicts:** A PASS WITH CAVEATS (content) / NEEDS FIXES (submission) · B PASS WITH CAVEATS · C NEEDS FIXES · D NEEDS FIXES (one copyright decision).
**Checks (offline, reviewers):** pytest 764 passed, 2 skipped; ruff clean; kb check PASS; no secrets, no resources/ files, no file > 5 MB in any commit.

**Hard constraint:** H01–H06 outputs stay frozen (tag `freeze-1`). Nothing below changes pipeline output. Output-changing items are listed under "Not before the deadline".

## Steps (in order, one agent at a time, then one re-review)

| # | What | Files | Source | Output change |
|---|---|---|---|---|
| F1 | Text fixes: SUBMISSION "5×" → "6×" (504 vs 84 s on D01–D08); "every important claim quoted word for word" → "key claims; verified = the quote is on the page, not that it fully supports the claim" (SUBMISSION:8, start page `ui/templates/start.html:31`, video card); README "copyrighted files not in git" wording (README:44, :187) per the Q1 answer; `pyproject.toml` description | SUBMISSION.md, README.md, start.html, pyproject.toml | C-B2, C-B3, D-B1, B-9 | none |
| F2 | ARCHITECTURE: fix 3 false statements (graph.json not read at runtime; 60 s budget covers search/fetch only; render + provenance run in `cli._assess_one`); "stronger repair model" holds for mix-a only; add an "Extending" section (new PDF, rule, method, external source, model, chat block: files to touch) | ARCHITECTURE.md | B-1, B-4 | none |
| F3 | README jury-first: run command in Quick start; "how to read an output" (Answer section first); brief-section → output-section map; honest notes: general web search cut, repair model writes the shown answer, live run takes 1.5–3 min | README.md | C-10, A-B2, A-N8, A-N11, A-N12 | none |
| F4 | Safety checks, no behaviour change: `tests/test_frozen_inputs.py` (pins hashes of knowledge block, prompts, skill, schemas = the hashes in `outputs/final/H01.json`); kb check: every doc id in pages.jsonl is in `schema.Doc`; every rule `when` key/value is in the screening vocabulary | tests/, src/afs_assistant/kb check | B-2, B-3 | none |
| F5 | **Short brief view (needs Q3):** code-generated from the frozen JSON, organiser section order (REF §3), ~400–600 words per case, confidence level only, external line only when a source was found, rule source quote shown as "related rule source", no internal ids, no "…" truncation; written to `outputs/final/brief/H0x.md` and `outputs/dev/brief/`; frozen H .md untouched; DEVIATIONS entry | new `src/afs_assistant/brief.py`, CLI subcommand, tests | A-B2, A-B3(a), A-N4/N5/N7/N9/N14 | new files only |
| F6 | Slides: 764 tests; repo URL + team names on slide 10; readable slide-3 screenshot; fix slide-5 crops; add one slide with a real H answer (the brief view if F5); re-export PDF | docs/slides/ | C-9 | none |
| F7 | **Video rebuild (needs Q2):** from the committed frames, $0, no live calls: fix closing card ("freeze-1" label, overclaim), caption #20 (v2 method switch is a known limitation, not a feature), drop frame 16 (fixed bug), slower captions #6/#13/#19, add a problem card and a limits card (~2:45) | docs/video/ | C-B3, C-B4, C-7/8 | none |
| F8 | Repo hygiene (needs Q4): LICENSE; `.claude/worktrees/` in .gitignore; `git mv` the icon-named folder under outputs/bakeoff-dev/ to `unnamed-arm/` | LICENSE, .gitignore | D-minor | none |
| F9 | Independent re-review of F1–F8 (one reviewer agent) | — | rules | — |
| F10 | **Publish (needs Q1, Q5):** `gh auth login` (user), `gh repo create --public`, push `master` + `provenance` + tag `freeze-1` by name (never `--all`); fill the link in SUBMISSION + slide 10; fresh-clone test (`uv sync`, pytest, kb check) | — | A-B1, C-B1, D-B2 | none |

Estimated time: F1–F4 ~1 h, F5 ~1.5 h, F6 ~45 min, F7 ~40 min, F9 ~30 min, F10 ~20 min. Target: everything done by ~19:30, submit well before 22:30.

## Not before the deadline (change pipeline output; would need an H re-run)
- Repair reasoning effort medium → low (B-6; est. −35–40 % time/cost per repaired case).
- Verbatim fibre quote in screening notes; range check accepts both ends in one quote (B-7, B-8).
- Prompt lines to cite S02 p.20 / S01 p.3 for plan steps (A-B3(b)).
- H06 "Non-contact" vs S03 p.4 slight contact (A-N1), H03 priority (A-N3): recorded as known limitations in README.
- Dead-code removal and duplicate merges (B-9, B-10): after submission, behind F4's frozen-input test.
- Removing merged worktree branches: after the deadline, `git branch -d` only, with the user's OK.
