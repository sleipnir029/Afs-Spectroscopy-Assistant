# F9 independent re-review: F1 to F8 and the public-copy script (631e5f4..f41cd8d)

Reviewer: independent, read-only. No edits, commits, model calls or network calls. All scratch work is under this folder.

## 1. Verdict: APPROVE WITH FIXES

The core is sound. The frozen H outputs are untouched. Pipeline inputs are hash-pinned and unchanged. The brief view is faithful and adds no facts. The fresh-clone path works and was re-proven here. The publish script is deterministic and keeps provenance intact.

Before F10 (publish), four cheap fixes are needed: B1 to B4 below. None of them changes pipeline output.

## 2. Check results (run by this reviewer)

| Check | Result |
|---|---|
| `uv run pytest -q` (local, with pages.jsonl) | **890 passed, 2 skipped** (API-key smoke test and live-network test). Matches slide 8. |
| `uv run ruff check` | All checks passed |
| `uv run afs-assist kb check` | 13/13 PASS |
| Public copy, fresh clone, no pages.jsonl, no resources/ (`uv sync --offline`) | **357 passed, 535 skipped**, 0 failed. Skip reasons: the kb-build hint only, plus the 2 usual skips. `kb check`: `pages_present` FAIL with hint; the other 7 PASS. `eval --set dev` and `external replay outputs/final/H01.json` work. `assess`, `ui` and `brief` stop with exit 2 and the hint. |
| Same clone with pages.jsonl copied in | **890 passed, 2 skipped**. sha256 `7e23c2ae…` = manifest `pages_sha256`. |
| Same clone, `kb build` from a copy of resources/materials | pages.jsonl byte-identical (`7e23c2ae…`); `git status` clean (no committed knowledge file changed); kb check 13/13 |
| Brief regeneration (`afs-assist brief outputs/final` and `outputs/dev` into scratch) | Identical to the committed files except line 3 (relative link, which depends on the out dir, as expected) |
| `scripts/publish_public_copy.sh` run twice (pub1, pub2) | Both give master `eaf1616`, freeze-1 → `0b35037`, provenance `d6eb961` (unchanged). Deterministic. |
| Commit map | `docs/commit-map.txt` agrees line for line with filter-repo's map (265 lines). The 3 later commits are missing, as expected. `1b3a7b9 → 0b35037` = public freeze-1. |
| run/* tags | 279 tags with identical hashes in the public copy. All six H `provenance_commit`s are present. All six H `code_sha` = 1b3a7b9, `code_dirty: false`, mapped. |
| `git diff 631e5f4 HEAD -- outputs/final` | Only additions under `outputs/final/brief/`. H0x.json/.md last touched in 64c6179 (the freeze run). freeze-1 is the code tag (1b3a7b9); outputs came one commit later. |
| Pipeline code since freeze-1 | Untouched: pipeline.py, render.py, verify.py, prompts/, skills/, config/, knowledge/ (except removing pages.jsonl). Changed: cli.py, kb.py, kb_check.py (guards plus the brief subcommand), the new brief.py, and start.html wording. chat.py and ui/view.py changed before 631e5f4 (chat/UI only, not the assess path). `tests/test_frozen_inputs.py` passes, so prompts, skill, knowledge block, rules, library, models config and strict schemas still match the H01 manifest. The only behaviour change: `kb.pages()` raises `PagesMissing` when the file is absent (before, a bare FileNotFoundError). |
| Deletions | `git diff --name-status 631e5f4..HEAD`: only `D knowledge/pages.jsonl` (user-approved, D-066) plus `R100` icon folder → `outputs/bakeoff-dev/unnamed-arm/`. `.gitignore` adds `knowledge/pages.jsonl` and `.claude/worktrees/`; both user-approved per comments and D-066. |
| Slides | `docs/slides/slides.pdf`: 11 pages, each rendered and viewed |
| Video | `docs/video/demo.mp4`: 173.0 s = 2:53. Frames pulled at every caption midpoint plus the title, limits and closing cards. Captions 1–19 match their frames: 107 s/$0.036, 29 citations, 1 hard check, 5.3 s/$0.006, Q1+Q3 open in v2, method adds Raman in v2. |

## 3. Plan compliance (PLAN.md F1–F8)

- **F1 done.** SUBMISSION has 6× (84 vs 504 s) and "Verified means the quote is on the page…". start.html:31 is reworded. README copyright wording is fixed. pyproject description is set.
- **F2 done.** I checked the 3 corrected statements against the code: `graph.load` has no runtime caller, `STEP_BUDGET_S` covers search/fetch, render and provenance live in `cli._assess_one`. "Stronger repair model" is scoped to mix-a. Every symbol named in "Extending" exists where stated: `_SAMPLE_SLOTS`, `SLOT_VALUES`, `METHOD_IDS`, `TECHNIQUE_FAMILY`, `METHOD_RANGES_UM`, `METHOD_PATTERNS`, `RANGES`/`BAND`, `BLOCK_TYPES`, `block_ids`, `API_NAMES`, `build_pages`.
- **F3 done.** README is jury-first: results, how to read an output, REF section map, honest notes. Two traceability gaps remain: see B2 and N1.
- **F4 done.** `tests/test_frozen_inputs.py`, plus the `doc_ids_in_schema` and `rule_when_vocabulary` kb checks.
- **F5 done.** Brief view: 555–698 words (H), 539–638 (D), REF §3 order, no "…", ids replaced, only run-verified citations, external line only when an item exists.
- **F6 done, one miss.** 11 slides, readable slide-3 crop, clean slide-5 crops, H04 short-view slide 9, `REPO_URL_PENDING` on slide 11 (to be filled in F10). The miss: SUBMISSION still says 10 slides (B1).
- **F7 done.** Problem card and limits card added, frame 16 dropped, closing card fixed, caption 19 states the known limitation. 2:53 vs the planned ~2:45 is fine.
- **F8 done.** LICENSE (MIT), `.claude/worktrees/` ignored, icon folder renamed with `git mv` (R100).
- **D-066 public copy.** Implemented and verified, with one hole in the script's own safety check (B3).

## 4. Blocking (fix before F10; all are text or script fixes, no output change)

### B1. Wrong slide count and no brief view in the submission text
- `docs/SUBMISSION.md:29`: "`docs/slides/slides.pdf`: 10 slides." The PDF has 11 pages (`docs/slides/README.md` also says 11).
- The Deliverables list (SUBMISSION:26–30) does not mention `outputs/final/brief/`, the short view the README now tells the jury to read first. The "Known limits" line (SUBMISSION:24) says answers are 3,000+ words and does not mention the 555–698-word short view.
- **Fix:**
  - line 29 → "`docs/slides/slides.pdf`: 11 slides."
  - add the line "- `outputs/final/brief/H01–H06.md`: code-built short view (555–698 words, REF §3 order, no model call; the full answers stay authoritative)."
  - in Known limits → "full answers are long (about 3,000+ words…); a code-built short view (555–698 words) is in `outputs/final/brief/`."

### B2. The public repo has no path from the manifest hashes to its own commits
- README.md:125: "The run used … code 1b3a7b9 (clean tree)". Every manifest's `code_sha` is also 1b3a7b9.
- In the public repo, 1b3a7b9 does not exist (it maps to `0b35037`). README, ARCHITECTURE and SUBMISSION never mention `docs/commit-map.txt`; only DEVIATIONS D-066 does.
- A juror who tries `git show 1b3a7b9`, or opens the GitHub URL for it, hits a dead end. That undercuts the "generated by the assistant, not edited" provenance claim.
- **Fix (README.md:125):** append "In the public repository, commit hashes differ because `knowledge/pages.jsonl` was filtered out of history. Tag `freeze-1` points to the same tree; `docs/commit-map.txt` maps each original hash (as in `code_sha`) to its public hash. The `provenance` branch and `run/*` tags are unchanged."

### B3. `publish_public_copy.sh` leaves the pages.jsonl blobs in DEST/.git, and its check says OK
- Evidence: after the script, both pages.jsonl blobs ever committed are still in the pack:
  - `00f7cfbd…` (169,843 B)
  - `a5883ba1…` (169,744 B)
- `git cat-file -e` succeeds for both, and `git rev-list --objects --all --reflog` lists them as `knowledge/pages.jsonl`. The clone's reflog (`HEAD@{2}: clone`) keeps the old history alive, so `git gc --prune=now` does not remove them.
- The check at `scripts/publish_public_copy.sh:29–32` uses `rev-list --objects --all` without `--reflog`, so it passes. The comment "no pages.jsonl object anywhere" is false.
- A push by name sends only reachable objects, so GitHub would not receive the file. But the guarantee D-066 relies on is not what the script checks. Anyone who tars, copies or rsyncs DEST, or pushes with a tool that sends the whole pack, ships S01/S04 full text.
- **Fix:** replace lines 29–34 with:
  ```bash
  git reflog expire --expire=now --all
  git gc -q --prune=now
  for b in $(git -C "$src" log --all --format=%H -- knowledge/pages.jsonl \
             | while read c; do git -C "$src" rev-parse -q --verify "$c:knowledge/pages.jsonl"; done | sort -u); do
    git cat-file -e "$b" 2>/dev/null && { echo "FAIL: pages.jsonl blob $b still present" >&2; exit 1; }
  done
  git rev-list --objects --all --reflog | grep -q 'knowledge/pages.jsonl' && { echo "FAIL: pages.jsonl reachable" >&2; exit 1; }
  ```
  Keep the provenance hash check.

### B4. A committed review report contains a local absolute path, against PLAN.md:4
- PLAN.md:4 says: "Author e-mail addresses and local paths are redacted in the committed copies."
- But `docs/review-final/C-deliverables.md:4` contains `<session scratchpad>/review/tmp-C/`.
- This is the only personal absolute path in the public master tree (I grepped for `/Users/`, `rakibuzzamanrahat` and `private/tmp`). It is also ironic, because D-repo.md:18 states "No `/private/tmp/claude-…` in any blob."
- **Fix:** replace the path with `<scratch>/review/tmp-C/`. This changes no history and needs no rewrite: earlier commits never held it outside this file's own commit, and that commit is new since 631e5f4.

## 5. Non-blocking (ordered by jury impact)

- **N1. README reproducibility numbers are stale.**
  - README.md:180–181 say "357 passed, 432 skipped" and "787 passed, 2 skipped".
  - Measured here on the public copy: 357 passed, **535** skipped; with pages: **890** passed, 2 skipped.
  - Slide 8 shows both 890 and "787/2 (14:38)", which reads as an inconsistency.
  - **Fix:** update to "357 passed, 535 skipped" and "890 passed, 2 skipped" (re-run 2026-10-18 on master f41cd8d, public copy eaf1616), and slide 8 to "a fresh clone with pages.jsonl rebuilt: 890/2".
- **N2. `tests/conftest.py:30–43` can hide real failures, even when pages.jsonl is present.**
  - The `pytest_runtest_setup` and `pytest_runtest_call` wrappers turn **any** `kb.PagesMissing` into a skip, regardless of whether the real file exists.
  - The fresh-clone guard tests use `no_pages`, which monkeypatches `PAGES_FILE` to a missing path (`tests/test_kb_guards.py:59–93`). If a regression made `kb_check.run()` or `cli.main` let `PagesMissing` escape, `test_kb_check_reports_missing_pages_with_the_hint` and `test_cli_commands_that_need_pages_fail_cleanly` would **skip instead of fail**. The guards for the fresh-clone path would go silent.
  - **Fix:** capture `_REAL_PAGES = kb.pages_available()` at conftest import, and in both wrappers `if _REAL_PAGES: raise` before `pytest.skip`. Today's run has only the 2 expected skips, so nothing is hidden now.
- **N3. Brief: an uncited risk with no related rule is shown bare.**
  - Examples: `outputs/final/brief/H01.md:45` (risk 1) and `outputs/final/brief/H06.md:47` (risk 3).
  - The full answer labels the same items "(no verified source: engineering judgement)". The brief drops the label, so a juror cannot tell judgement from an omitted citation.
  - **Fix:** in `src/afs_assistant/brief.py:321`, use `refs or b.related_source(...) or " (engineering judgement, no source)"`. Regenerate the briefs (new files only, no H change), and add a test.
- **N4. Brief id replacement is too broad.**
  - `brief.py:66` `_ID = r"\b[A-Z]\d+\b"` replaces any token equal to a run id, so oxygen written "O2" becomes "the recommended option" (for example "dissolved O2").
  - No current D/H output is affected: I listed every id hit in all 14 runs and each was a real id.
  - `tests/test_brief.py:22` `INTERNAL_ID` would also falsely fail on a chemical "O2" or "N2".
  - **Fix:** replace only ids in id-only brackets, in `X/Y` pairs, or after "option"/"question"/"method", or skip `O\d`/`N\d` tokens preceded by a chemistry word. Low priority after the deadline; it is generic.
- **N5. Brief wording edge case.** `outputs/dev/brief/D06.md:50` reads "method per an open clarification question". Faithful but vague. **Fix:** for a question that is not shown, use "(see the full answer)".
- **N6. The brief status clause adds an interpretation.** For `premise_not_supported`, `brief.py:47` adds "the assessment below is provisional". It is generic, not case-specific, and consistent with the six H texts, but it is not in the run JSON. **Fix:** keep it, or soften to "…as stated; see the reason in the full answer."
- **N7. README.md:11 overclaims slightly.** "every citation shown is one the run verified": the related-rule quotes are shown citations the run did not verify. They are kb-checked and labelled, and `outputs/final/brief/README.md` explains this correctly. **Fix:** append "(rule-source quotes are marked 'related AFS source' and are not checked against the sentence)".
- **N8. Video: the start page in the screenshots still shows the old overclaim.** At 0:14–0:28 the start-page frames show "Every important claim quotes the AFS documents word for word…", the text F1 removed from start.html:31. Caption 8 says "Every quote beside the answer is word for word from AFS", but slide 4 says loose matches also count as verified. **Fix (optional, $0):** change caption 8 to "Every quote beside the answer is checked against its AFS page." The frames cannot change without a new capture; accept that.
- **N9. Slide 4 headline overclaims.** "Code checks every quote, number and word." contradicts slide 10 ("short table cells … are not checked"). **Fix:** "Models write. Code checks the quotes, numbers and wording."
- **N10. Slides 10–11 and SUBMISSION do not mention the short view.** Slide 10 says "Too long: 3,058–3,455 words", and slide 11 lists "a short customer reply that matches the length" as next, while slide 9 shows that view exists. **Fix:** slide 10 → "Full reports 3,058–3,455 words; the code-built short view is 555–698", and slide 11 → "a model-written customer reply at AFS length".
- **N11. REF label still inconsistent (A-N14 not done).** Slide 6 (`docs/slides/slides.html:238`) says "REF p.5", while README and outputs say "REF §5". **Fix:** "REF §5".
- **N12. Commit map lags by design.** `docs/commit-map.txt` cannot include its own commit or later ones. The header says "Commits after this file was written map 1:1 in the same way", which is unclear. **Fix:** "Later commits are not listed; DEST/.git/filter-repo/commit-map of a fresh run has them." Only `1b3a7b9` matters for the manifests, and it is present.
- **N13. `afs-assist eval` dirties two tracked files.** It rewrites `outputs/eval/summary.json|md` (timestamp lines) in a fresh clone. This is harmless, but README:67 invites jurors to run it. **Fix:** mention it, or leave as is.

## 6. Brief view, read as a jury member (H01–H06)

- **Status:** brief and full .md agree in all six (premise ×4, provisional ×1, insufficient ×1).
- **Options table:** the proposed option is "recommended" (O2) in all six, matching "Best current option: O2" in each full .md. Cost classes match the full tables, including H06 O3 "at least high". Confidence levels match.
- **Citations:** a test enforces that every inline citation is in the run's verified set; I confirmed it by reading. H04 marks S02 p.10 as "(precedent only)".
- **Related-source quotes** (H01 risks 2–3, H05 risks 1–3) are each labelled "not checked against this sentence". Never presented as verifying.
- **Ids:** no internal ids remain. "if M2/M3 proceed" → "if Raman or NIR + Raman proceed" (H01) is correct.
- **Stated facts:** "Stated by the customer" quotes are verbatim enquiry quotes. Some are fragments (H02 "and an opaque milk concentrate."); readable.
- **H06:** the short view avoids the full answer's "Non-contact" slip (the measurement concept says light contact).
- **External items:** H02 and H03 each show one verified secondary item with URL and quote. In H02 the item (OH-band temperature sensitivity, from a biopharma downstream review) is only loosely relevant. It is labelled secondary, so acceptable.
- **Lint:** kb check `no_case_ids` PASS; brief.py has no scenario-specific code.

## 7. Test gaps

- No test that the publish script removes the pages.jsonl **blobs** (see B3). Add a shell test or a pytest that runs the script into tmp and calls `cat-file -e` on the known blob ids. Skip it if `uvx` is offline.
- No test that the conftest skip hook re-raises when the real file exists (see N2).
- No brief test for uncited risks without a rule (N3) or for chemical tokens that look like ids (N4).
- No test that SUBMISSION and slides/README agree with the slides.pdf page count (B1). A one-line `pymupdf` page-count assertion would do.

## 8. Smallest next patch (about 20 minutes, no model calls, no H change)

1. `docs/SUBMISSION.md`: 11 slides, brief view line, short view in Known limits (B1).
2. README.md:125: commit-map sentence (B2). README.md:180–181: 357/535 and 890/2 (N1).
3. `scripts/publish_public_copy.sh`: reflog expire, gc, blob-id check (B3). Re-run into a new dir and confirm `cat-file -e` fails for `00f7cfbd…` and `a5883ba1…`.
4. `docs/review-final/C-deliverables.md:4`: redact the path (B4).
5. Optional before the deadline: N2 (2 lines in conftest), N3 (1 line plus regenerated briefs), N9/N10/N11 slide text, then re-export the PDF.
6. Then F10. After committing, re-run the publish script, because the commit map and public master hash change with each new commit.
