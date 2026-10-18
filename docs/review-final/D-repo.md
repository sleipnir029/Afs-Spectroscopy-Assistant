# D: Repository publish-readiness audit (item 10)

Reviewer: independent, read-only. Repo: <repo>
Audited state: master at 00d5975 (moved from eb60291 during the audit: "STATUS: final review session started"), working tree clean.
No remote configured (`git remote -v` empty); `gh auth status`: not logged in.

## 1. Verdict

**NEEDS_FIXES (one user decision blocks a public push).** Hygiene is good: no secrets, no `.env`, no `resources/` file, no organiser PDF, no personal absolute path and no file over 5 MB anywhere in history. The one blocker is copyright. `knowledge/pages.jsonl` holds the **complete verbatim text of every page of S01 to S05** plus the REF docx, and that includes S01's own "All rights reserved, no part ... may be reproduced, distributed" notice and the full text of a non-open-access ACS article (S04). The organiser rules require a **public** repository (Opening Ceremony deck: "Git repository: Reproducible code, setup instructions, public"), so a private repo does not get around this. The user has to decide.

## 2. Plan compliance (CLAUDE.md git and challenge rules)

| Rule | Result | Evidence |
|---|---|---|
| `resources/` never committed | PASS | No path under `resources/` in `git log --all --name-only` (4055 distinct paths checked). `resources/` is ignored (.gitignore:3). |
| No organiser PDFs in git | PASS | The only PDF ever committed is `docs/slides/slides.pdf` (our own 10-page deck; its 3 embedded images are our app screenshots). |
| `.env` / keys never committed | PASS | `.env` (212 B) exists locally and is ignored (.gitignore:9). A scan of all 3795 unique blobs in all refs found no match for `sk-or-v1-`, `sk-ant-`, `sk-…{20+}`, `ghp_`/`github_pat_`, `AKIA`, `AIza`, `hf_`, private-key headers, or `Bearer …` tokens. The only `token=` hits were mermaid.min.js code. |
| No personal absolute paths | PASS | No `/Users/…` and no `/private/tmp/claude-…` in any blob. `CLAUDE.md` names `~/.claude/plans/in-this-repository-you-ll-cozy-knuth.md` (tilde path, harmless; the file itself is not in the repo). |
| Author identity | PASS | Commits use `Rakibuzzaman Rahat <<GitHub noreply address>>` (248) and `afs-assistant pipeline <pipeline@afs-assistant.local>` (293). The private gmail address does not appear in any commit or blob. |
| No unrequested deletions | PASS | The only deletion in history is `src/afs_assistant/ui/static/vendor/mermaid-11.12.2.min.js` in 8154aa5, which the user approved (DEVIATIONS D-044, 23:27). |
| Large files | PASS | Largest blobs ever: `docs/video/demo.mp4` 2,956,820 B; mermaid.min.js 2,754,895 B (history only); `docs/ui/brief-thread-full-1440.png` 1,162,279 B; `docs/ui/brief-phone-full-390.png` 1,088,903 B. Nothing over 5 MB. HEAD tree is about 40.4 MB; the provenance tree is about 32.9 MB. Both are within GitHub limits. |
| No scenario IDs in `knowledge/`, `src/` | Not in scope here (lint test owns it). |

## 3. Blocking for publishing

### B1. Full verbatim text of copyrighted organiser documents in `knowledge/pages.jsonl` (in every commit since ce69daa)

- File: `knowledge/pages.jsonl`, 169,843 B, 67 records. Coverage against the local originals in `resources/materials/` (page counts from `mdls`):
  - S01 19/19 pages (46,297 chars). It contains the disclaimer verbatim: "© 2026 art photonics GmbH and MIR Photonics LLC. All rights reserved. … No part of this publication may be reproduced, distributed, modified, or transmitted … without the prior written permission" (`grep -c 'All rights reserved' knowledge/pages.jsonl` gives 1).
  - S02 20/20 slides (11,864 chars, text layer plus manual transcription). AFS-owned slides.
  - S03 17/17 pages (54,788 chars). MDPI, **CC BY 4.0**, so redistribution is allowed with attribution. Low risk.
  - S04 6/6 pages (26,227 chars). ACS *Analytical Chemistry* Technical Note, **not open access**. The committed text includes the watermark "Downloaded via TU BERLIN on April 19, 2021 … See https://pubs.acs.org/sharingguidelines …". This is the highest third-party risk: ACS is not the organiser, and its sharing guidelines do not allow posting full text publicly.
  - S05 2/2 pages (AFS flyer), S06 link, REF 2 records (organiser docx guidance, 5,101 chars).
- First introduced: ce69daa "Phase 1: knowledge foundation (pre-review)" (2026-10-17). It is present in all of master's history after that (248 commits) and in every worktree-agent-* branch.
- README.md:44 and README.md:187 say the organiser files "are copyrighted, so they are **not in git**", while `knowledge/` "holds derived page text". "Derived" understates this. It is the full extracted text, and a public reader would see the contradiction.
- Same file: about 17 third-party e-mail addresses from paper author blocks and contact pages (for example `<author e-mail redacted>`, `<author e-mail redacted>`, `<author e-mail redacted>`, `<author e-mail redacted>`). They are already public in the source papers, but they become scrapeable in a public repo.
- Plain assessment: S03 is fine. S01, S02, S05 and REF are AFS/organiser material handed out for this challenge. Publishing their full text in a public repo the organiser asked for is a grey area: there may be an implied licence, but S01's explicit notice says otherwise. **S04 is a clear third-party (ACS) full-text redistribution.** This is the user's call, not the reviewer's.
- **Options for the user (pick one):**
  1. **Publish as is and accept the risk.** This is the fastest option. Change the README wording so it states honestly that `knowledge/pages.jsonl` contains the extracted full text of the supplied materials, for grounding and verification.
  2. **Ask the organiser (AFS / SchubKI) right now** whether the extracted page text may be in the public repo. Publish when they answer, falling back to option 3 if there is no answer before about 22:30.
  3. **Strip or reduce the text and rewrite history.** This means a reduced `pages.jsonl`, for example S04 replaced by sha256 plus short cited quotes and S01 trimmed, with `kb build` regenerating the full file locally from `resources/`. The file is in every commit since ce69daa, so removing it from public view means either:
     - (3a) `git filter-repo --path knowledge/pages.jsonl --invert-paths` (or a blob replace) on a **fresh clone**. This rewrites all 248 master commit hashes, so the `code_sha` in the run manifests and `outputs/final/*.json` stop matching. That is bad for the provenance story.
     - (3b) Push a **single squashed orphan commit** of the cleaned master tree to the public repo, and keep full history local. This is simpler, but the same `code_sha` mismatch applies.
     The tests and app read `pages.jsonl` (`src/afs_assistant/paths.py`, `graph.py`, `external/query_guard.py`, `tests/test_phase2.py`), so a reduced file needs a test run, and README.md:149 claims a fresh clone passes pytest without `resources/`. Under the user rule ("no tracked file removed without explicit per-file OK"), this needs an explicit yes for `knowledge/pages.jsonl`, and a deviation entry.
  4. Remove only S04 (the ACS article) from `pages.jsonl` and keep S01 to S03, S05 and REF. This has the same history-rewrite cost as option 3, so it is not much cheaper.
- Reviewer recommendation: option 1 or 2. A history rewrite with under 10 hours left breaks the code-sha provenance chain, which is a core claim of the submission (no manual editing of H01 to H06). If the user picks option 1, add one README sentence on the source and licence of the page text, including the CC BY attribution for S03.
- Questions for the user (yes/no):
  - Q1: Publish `knowledge/pages.jsonl` with the full page text of S01 to S05 in the public repo? (yes / ask organiser / no, strip)
  - Q2: If no: may `knowledge/pages.jsonl` be replaced and history rewritten (all commit hashes change)?

### B2. Push scope must be explicit: never `git push --all`, `--mirror` or `--tags`

- 14 local branches: `master`, `provenance` and 12 `worktree-agent-*`. 280 tags: `freeze-1` (annotated, points to 1b3a7b9 on master) plus 279 `run/*` tags (every one on `provenance`, checked with `merge-base --is-ancestor`).
- `gh repo create --source . --push` pushes only the current branch, which is safe. `git push --all` would publish 12 throwaway agent branches.
- Exact commands after the user says yes (with B1 resolved):
  ```
  cd <repo>
  git status && git log -1 --oneline master          # confirm clean, expected HEAD
  gh auth login                                       # user, interactive
  gh repo create <owner>/<name> --public --source . --remote origin   # no --push
  git push -u origin master
  git push origin provenance                          # recommended, see N1
  git push origin refs/tags/freeze-1                  # optional
  # optional, only if provenance is pushed: git push origin 'refs/tags/run/*'
  ```
  Then put the repo URL into `docs/SUBMISSION.md:31` ("to add once the repository is published") and commit it as a named path.

## 4. Non-blocking

### N1. `provenance` branch: push it (recommended)
- Orphan history (no merge base with master). 293 commits, f027d1d (2026-10-17 07:26Z) to d6eb961 (2026-10-18 10:44Z), all by `afs-assistant pipeline`. The tree is only `runs/` (3464 files, about 32.9 MB). One folder per run holds `assessment*.json/md`, `calls.json`, `enquiry.txt`, `external.json`, `intake.json`, `manifest.json`, `repair_round_*.json`, `screening.json` and `verification.json`.
- Secret and path scan: clean. No `Downloaded via` or `All rights reserved` text in it, so it carries only short cited quotes, not full pages.
- `outputs/final/H01..H06.json` reference `provenance_commit` hashes (for example `bea3dd0…`, `54d6315…`, `4ef7a27…`), and all of them are on `provenance`. README.md:66 tells readers that every run is a commit on the `provenance` branch. If the branch is not pushed, that claim and the "generated by the assistant" evidence cannot be checked by the jury. Recommendation: push it.

### N2. Worktree branches: all 12 fully merged and clean, safe to clean up later (user decides)
| Branch | Tip | Ahead of master | Behind |
|---|---|---|---|
| worktree-agent-a207b0059aa193d71 | 24c929b UI review: diagram labels may break after a slash | 0 | 126 |
| worktree-agent-a5dda1b856731189d | b15b4c7 Eval confirm-review fixes | 0 | 101 |
| worktree-agent-a5eb81de11b70317d | 92c7c86 C1 Brief polish | 0 | 27 |
| worktree-agent-a6544799fb0b3f60a | 248d529 5.0b review F1/F2 | 0 | 125 |
| worktree-agent-a6abe957d0b17c545 | 7d0378b 5.12 live-check script | 0 | 35 |
| worktree-agent-a88b0f7407591c588 | 5f4e53e C1 Brief review fixes | 0 | 16 |
| worktree-agent-a9d3b9be6febd2b03 | 5b767ce 4.R G4 code review fixes | 0 | 164 |
| worktree-agent-aa5b6cec4db578daa | 916ee1f D-061 proposal follows tier | 0 | 43 |
| worktree-agent-ad6e2cbf49c6a5071 | add6c87 5.0.R cancel during external step | 0 | 141 |
| worktree-agent-ade5f3a7df4d96488 | 7c52803 5.R1 review fixes | 0 | 90 |
| worktree-agent-af27b84c238dd6dba | 84f4a1f D-050 review fixes | 0 | 83 |
| worktree-agent-afb707f25a8e611cf | 5dc4f18 5.8 step 2 bake-off arm configs | 0 | 68 |

- `git branch --merged master` lists all 12. `git status --porcelain` in each worktree is empty. No unmerged commits anywhere except `provenance` (orphan, by design).
- They live under `.claude/worktrees/` (ignored through `.git/info/exclude`: `**/.claude/worktrees/`), so they never reach the remote unless they are pushed explicitly.
- Cleanup after the deadline, only if the user agrees. This deletes no tracked file; the commits stay in master:
  ```
  for w in <repo>/.claude/worktrees/agent-*; do git -C <repo> worktree remove "$w"; done
  git -C <repo> branch -d $(git -C <repo> branch --format='%(refname:short)' --merged master | grep '^worktree-agent-')
  ```
  (`-d`, not `-D`, so git refuses any branch that is not merged.)

### N3. A junk directory name from a pasted `ls` icon
- `outputs/bakeoff-dev/<U+E5FF>/eval-dev/summary.json` and `summary.md`, committed in ace38cc ("D01-D08 x 7 arms…"). The folder name is a single Nerd-Font folder-icon glyph (bytes EE 97 BF). An agent probably copied `eza --icons` output into a path. It shows as an unreadable folder on GitHub and is copied into two worktrees. Its content is an eval summary with 955 lines against 979 for the real arms, so it is probably a stale or extra run.
- Question for the user: may these 2 files be removed (`git rm` of that folder) or renamed (`git mv` to, for example, `outputs/bakeoff-dev/unnamed-arm/`)? Rename is the safer choice under the no-loss rule. History keeps them either way.

### N4. No LICENSE file
- No `LICENSE`/`COPYING` at the root. A public repo without one defaults to "all rights reserved", which is legal but unusual for a hackathon. Fonts carry `OFL.txt` and `OFL-Newsreader.txt` (good). htmx is vendored with `vendor/README.md`. Question for the user: add a LICENSE (for example MIT for our code, with a note that `knowledge/` derives from third-party material under its own terms)? This ties in with B1.

### N5. `.gitignore` coverage
- Ignored and present locally (good): `resources/`, `runs/`, `.env`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.DS_Store`, `.playwright-mcp/`. `.claude/` runtime files (worktrees, scheduled_tasks.lock) are covered by `.git/info/exclude`, which is local only and does not travel with the repo. A teammate cloning and running Claude Code could commit `.claude/worktrees`. Optional: ask the user whether to add `.claude/worktrees/` to `.gitignore` (per user rules, this needs a yes).
- No stray tracked runtime files: no `__pycache__`, `.pyc`, `.DS_Store` or logs in `git ls-files`.
- `outputs/ui/` (5 files: 2 ad-hoc runs plus `turns/adhoc-20261018T054714Z.json`) is tracked on purpose. It is G5 live-UI evidence from a49ee31, and the content is a synthetic emulsion-polymerisation enquiry with no personal data. It is fine to keep. If the UI writes new runs there during the live demo, they will show as untracked: do not sweep them in with a broad `git add`.
- `docs/video/frames/*.png` (22 frames) are tracked build inputs for the video. Fine.

### N6. Organiser scenario text in `scenarios/`
- `scenarios/final.jsonl` has the H01 to H06 enquiries verbatim from `customer_scenarios_for_final_evaluation.txt`; `dev.jsonl` and `dev_reference.jsonl` have D01 to D08 and the reference content from the organiser docx. The brief requires the H answers in the repo, and the enquiries are needed to reproduce them, so this is expected and low risk. It is listed because it falls under the same organiser-material question as B1.

### N7. History bloat
- mermaid-11.12.2.min.js (2.75 MB) stays in history (7e44865) even though it was removed in 8154aa5. It is MIT-licensed, so there is no legal issue. It makes a clone about 2.7 MB larger. Not worth a rewrite.

### N8. Process docs are candid
- DEVIATIONS.md:28 (D-020) records that the user was "too tired" and that reviewers replaced the user's reading. STATUS.md:11 records OpenRouter credit and key-limit figures (no key value). Nothing secret. It is the user's call whether this candour is wanted in a public repo. It also arguably shows that the process was honest.

## 5. Test gaps (for this audit)
- I did not check whether `outputs/final/*.json` manifests show `dirty: false` and `code_sha` on master (another reviewer's scope).
- I did not run `uv run pytest` from a fresh clone (README.md:149 claims 758 passed, 2 skipped; the figure is 764 per STATUS). Running it is not read-only-safe here.
- I did not check what the organiser's track form needs beyond "public repo" (for example a licence or a specific structure).

## 6. Smallest next patch
1. User answers Q1 on B1 (publish `pages.jsonl` full text: yes / ask organiser / strip).
2. If yes: one README edit (README.md:44 and :187) to state honestly that `knowledge/pages.jsonl` contains the extracted full text of the supplied AFS materials, used for grounding and verification, with S03 under CC BY 4.0 (MDPI). Commit it as a named path.
3. `gh auth login`, `gh repo create … --public --source . --remote origin`, `git push -u origin master`, `git push origin provenance`. No `--all` and no `--tags`.
4. Fill in `docs/SUBMISSION.md:31` with the URL, commit, push.
5. After the deadline (optional, user OK): remove the 12 merged worktrees and branches; rename the icon-named folder.

## Executive summary (10 lines)
1. History is clean of secrets: no API keys, tokens, `.env` or private-key material in any of 3795 blobs on any ref.
2. No `resources/` file and no organiser PDF has ever been committed. The only PDF is our own `docs/slides/slides.pdf`.
3. No personal absolute paths. The author e-mail is the GitHub noreply address, and the private gmail address appears nowhere.
4. No file over 5 MB. The largest is `docs/video/demo.mp4` at 2.96 MB. HEAD is about 40 MB and provenance about 33 MB.
5. BLOCKER (user decision): `knowledge/pages.jsonl` is the full verbatim text of S01 to S05 plus REF, including S01's "All rights reserved" notice and a non-OA ACS article (S04).
6. The organiser requires a public repo, so going private is not an option. Choose: accept the risk / ask the organiser / strip and rewrite history (this breaks the code-sha provenance chain).
7. The README's claim that the copyrighted files are "not in git" contradicts point 5 and should be reworded whatever the choice.
8. All 12 worktree-agent-* branches are fully merged and clean, so they are safe to remove after the deadline. Only `provenance` (orphan, runs only, clean) is unmerged.
9. Push `master` and `provenance` explicitly (H01 to H06 outputs cite provenance commits). Never use `--all`, `--mirror` or `--tags`.
10. Minor: an icon-glyph folder name under `outputs/bakeoff-dev/`, no LICENSE, `.claude/worktrees` ignored only through the local `info/exclude`.
