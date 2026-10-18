# Review C: deliverables (items 7–9: docs, video, slides and submission)

Reviewer: independent, read-only. Repo HEAD 00d5975 (master). No repo file changed (`git status` clean after review).
Temporary renders: `<session scratchpad>/review/tmp-C/` (slide-01..10.png, hi-05.png, v_41/85/125/140.png, evalout/).

## 1. Verdict

**NEEDS_FIXES.** The numbers are mostly right. I recomputed nearly every figure from committed files, and all but three trace exactly. Four things must change before submission: the repository is not public yet; one number in SUBMISSION is wrong; two "every important claim" statements are contradicted by our own README and by our own video frames; and the climax of the video presents an unexplained method flip as a feature. Every one of these is a small text or caption fix. A full video re-record is **not** required.

## 2. Plan compliance (STATUS handoff items 7–9; brief requirements)

| Requirement | Source | State |
|---|---|---|
| Git repository, reproducible, **public** | Opening ceremony PDF p."Rules 2/3": "Reproducible code, setup instructions, public" | **Not met yet**: no remote, SUBMISSION.md:31 "to add once the repository is published" |
| PDF slides + demo video, video max. 5 min | Opening ceremony PDF "Rules 2/3"; brief "Final presentation and live demo (up to 5 mins) + slides" | Met: slides.pdf 10 pages 16:9; demo.mp4 145 s H.264 1440×900 |
| Short description of architecture and use of AFS materials | Brief "Expected output" | Met: ARCHITECTURE.md, slide 4 |
| Structured output per case: requirements, questions, recommendation, risks, feasibility plan | Brief "Expected output" | Met in outputs/final/H04.md (sections at lines 116, 133, 140, 157, 164), but README never maps to these five brief terms (see N1) |
| H01–H06 generated, unedited, in repo | Brief "Rules" | Met (manifests code_sha 1b3a7b9, code_dirty false) |
| Every number traceable to a committed file | STATUS handoff item 7 | 3 wrong or stale numbers, 2 mislabelled (below) |

### Number traceability (recomputed, not taken from docs)

| Claim (where) | Recomputed from | Result |
|---|---|---|
| H01–H06 120/120 citations, 0 hard, 97–184 s, $0.032–0.064, $0.288 (README:86,96–104; slides 4, 8; SUBMISSION:15–16; video 2:17) | `outputs/final/H0*.json` manifest | OK (97.2–183.9 s; sum $0.2882) |
| Status ×4/×1/×1 (slide 8) | assessment.decision_status | OK |
| 6 external items, 1 dropped, external 4–7 s, ≤$0.0014 (slide 6) | `external.items/dropped`, `timings_s.external` 3.96–7.25 s, external call cost max $0.00141 | OK |
| 3,058–3,455 words (README:166, slide 9) | `wc -w`-style split of outputs/final/*.md | OK exactly |
| 303–400 words AFS worked answers | scenarios/dev_reference.jsonl (400, 303) | OK |
| Gate 35–247 s, mean ~105 s, $0.013–0.070 (README:87, SUBMISSION:21, video card) | outputs/dev + adversarial manifests, 19 assessed cases | OK (mean 105.9 s without the off-topic A12) |
| must 33/34, must-not 12/13, checklist 0 failures | outputs/eval/summary.md; I also re-ran `afs-assist eval --external-cache <empty>` into tmp-C: same result, exit 0, so it reproduces in a fresh clone | OK |
| Bake-off table (README:132–140, slide 7) | outputs/bakeoff-dev/blind/summary.md | OK, all 28 cells |
| "3–6× faster than the other two" (README:142) | 259/84 = 3.1, 504/84 = 6.0 | OK |
| **"about 5× faster than the previous model" (SUBMISSION:22)** | 504/84 = **6.0** | **WRONG** (B2) |
| Chat 10/11, 1.4–6.3 s, $0.038, ~$0.004/question (README:88, slide 5) | docs/chat/live-check-20261018.json (sum $0.03767; latency 1.36–6.33 s; 10 kept, 1 dropped, 0 removed) | OK |
| "about 2–6 s" (SUBMISSION:11) | same file: 1.36–6.33 s | Imprecise (N8) |
| 44 rules, 67 pages, graph 161/245, library 9, "about 40 checks" (ARCHITECTURE, slide 4) | knowledge/*.json/yaml/jsonl; distinct check names in H01 verification = 41 | OK |
| 45 of 55 options Low (README:177, slide 9) | PHASES.md:783 (0 High / 10 Medium / 45 Low) | OK |
| Fresh clone 758/2, 92 s, $0.031, 25/25 (README:149–151, slide 8) | STATUS.md 12:37 | OK (traceable to STATUS only) |
| **"763 offline tests pass (2 skipped)" (slide 8 / slides.html)** | STATUS 13:27 says 764/2; `pytest --collect-only` = 766 collected = 764 + 2 skipped | **STALE** (N5) |
| "19/19 gate-run external replays equal" (slide 4) | STATUS 11:52 only. outputs/eval/summary.md shows 7/7 + 11/11 = 18 *applicable* replay items (D05 n/a) | Traceable to STATUS, not to the eval file named on the slide (N6) |
| Video: 107 s/$0.036, 5.3 s/$0.006, 147 s/$0.046 | docs/video/script.md "Live cost spent" table | OK |
| **Video closing card header "From STATUS.md (freeze-1, …)" over "~105 s"** | 105 s is the pre-freeze gate run (manifests code c226e48), not freeze-1 | **MISLABELLED** (N10) |
| Spend caps $1/$10, temperature 0, model table (README:70–82) | config/models.yaml:11,15–20,31–33 | OK |
| CLI table (README:54–64) | `afs-assist {assess,run,ui,eval,external,kb} --help` | OK; every flag matches. `scenarios` subcommand is undocumented (minor) |

## 3. Blocking issues

### B1. Repository not public; the submission has no repo link
- **File:** docs/SUBMISSION.md:31: "**Repository link:** _to add once the repository is published_." STATUS.md:29: no git remote, `gh` not logged in.
- **Evidence:** the organiser rules (SchubKI opening ceremony PDF, "RULES 2/3 · SUBMISSION") require a "Git repository: Reproducible code, setup instructions, public". The README also points to `docs/video/demo.mp4` and `docs/slides/slides.pdf`, and those are only reachable through the repo.
- **Fix (user action):** publish the repo after the item-10 sanitise review, then replace line 31 with `**Repository link:** https://github.com/<owner>/<repo>`. Also add the same URL to slide 10 (see N12). Check that the `provenance` branch is pushed, or reword README:66 to say "a local `provenance` branch" (see N3).

### B2. Wrong speed-up figure in the submission text
- **File:** docs/SUBMISSION.md:22: "is about 5× faster than the previous model at similar quality".
- **Evidence:** outputs/bakeoff-dev/blind/summary.md: baseline 504 s/case vs mix-a 84 s/case = 6.0×. README:142 says "3–6× faster".
- **Exact replacement:** `… is about 6× faster than the previous single-model setup (84 vs 504 s per case on D01–D08) at similar blind-judged quality (4.06 vs 4.08 of 5, four LLM judge agents), for about $0.03 per case.`

### B3. "Every important claim quotes … word for word" is contradicted by our own README and our own video
- **Files:**
  - docs/video/build_video.py:114 renders the closing card (frame 22, 2:17–2:25): "Every important claim quotes the supplied AFS documents word for word."
  - docs/SUBMISSION.md:8: "cites the supplied AFS material for every important claim".
- **Evidence:**
  - README.md:167 (our own limitation): "a claim can go beyond its valid quote, and a citation is sometimes used for a point the page does not really make (seen in four of the six H outputs)".
  - In the video itself, frame 08 (0:38–0:46) has the answer "ethanol has strong NIR overtone bands … Raman tolerates water well" with markers 1 2 3 4. All four quotes are about milk, online use and band overlap (S01 p.18, p.5, p.10, p.18); none says either thing.
  - Frame 20 status: "ethanol is a known NIR analyte" also has no supporting quote.
  - An AFS juror opening the margin notes sees this at once. The judges weight grounding at 20 % and explainability at 10 %, so an overclaim costs more than it gains.
- **Exact replacements:**
  - build_video.py:114: `"Every quote is checked word for word against its AFS page; claims without a source are labelled."`
  - SUBMISSION.md:8: `- **Citations:** cites the supplied AFS material (\`S01 p.18\`) for its key claims. Code checks every quote verbatim on the cited page and checks the page scope; failing citations are removed or flagged. "Verified" means the quote is on the page, not that it fully supports the claim (no entailment check yet).`
- **Note for the src/ reviewer:** the app's start page carries the same overclaim at src/afs_assistant/ui/templates/start.html:31, and it is visible in video frames 02 and 03. It is outside my scope (src/), but it should get the same wording.

### B4. The video's climax shows an unexplained method flip, and the headline contradicts the body, captioned as a feature
- **File / timestamp:** docs/video/captions.srt #20 (2:08–2:17), build_video.py:45: "What changed, v1 to v2: the proposed setup now tests NIR and Raman together; status and confidence unchanged."
- **Evidence:**
  - Frame 20/21: the only new fact is a temperature (28–36 °C), yet v2 adds Raman to the proposal.
  - The v2 headline (built by code) says "Test an NIR … probe together with a Raman probe", but the v2 body says "Test NIR transmission or transflection first … Raman is a useful … comparison". The next step tests NIR only.
  - The v2 options make "recommended" (NIR; Raman) the same method set as "extended" (NIR + Raman).
  - docs/video/script.md:71 and README:178 already say this is probably run-to-run variation. The video is the only place a juror sees it presented as a deliberate result.
- **Exact replacement caption #20:** `What changed, v1 to v2: the new fact is logged and v2 adds a Raman probe. A temperature alone does not justify that; a re-assessment is a fresh model run and can shift (a known limitation, see README).`
- Rebuilding needs no new live run (see "Smallest next patch").

## 4. Non-blocking issues

### README.md
- **N1 (high value, README:7–23):** the README is not jury-first.
  - Quick start (25–40) ends after `.env` and never says how to run. The run command is 15 lines further down, in a table. Add after line 38:
    ```
    uv run afs-assist ui      # open http://127.0.0.1:8765; pick a finished H01–H06 example (no API key needed) or type a new enquiry
    ```
  - Add a 6-line "Brief → where" map under "What it produces": requirements → `### Requirements`; questions → `### Clarification questions`; recommendation → `### Recommendation` and `### Proposal`; risks → `### Risks and uncertainty`; feasibility plan → `### First feasibility experiment`; sources → `### Evidence (verified quotes)` (headings as in outputs/final/H04.md).
  - Move a 3-line results summary (120/120, 0 hard, $0.288, PASS WITH CAVEATS) above Quick start.
  - At 192 lines the README is not short. Models and Reproducibility could move to ARCHITECTURE.md.
- **N2 (README:5):** "Hackathon deliverable. Deadline: Sun 18 Oct 2026, 23:59 Berlin." The deadline is internal noise for a jury reader. Replace with `Team Helios · SchubKI National AI Hackathon 2026 · Art Fiber Systems challenge.`
- **N3 (README:66):** "Every run is also written as a commit on the `provenance` branch". This is only true in the local repo unless that branch is pushed. The 300+ `run/*` tags are local too. Push it, or write "on a local `provenance` branch (not part of the public repo)".
- **N4 (README:21 and SUBMISSION:28):** "the real app with live model calls". The video is a slideshow of captioned stills (script.md:4–6), not a screen recording. Write "captioned screenshots of the real app during a live run".

### Slides (docs/slides/slides.pdf, slides.html, slides.md)
- **N5 (slide 8, "763 offline tests pass (2 skipped)"):** stale. STATUS 13:27 says 764/2, and 766 tests are collected now. Replace with `764 offline tests pass (2 skipped)`. Re-export the PDF.
- **N6 (slide 4 footer):** the "19/19" replay figure is sourced to "STATUS.md (gate 11:52)", which is correct. The eval file shows 18 applicable items, so do not change the source to outputs/eval. No text change is needed if the footer stays as it is.
- **N7 (slide 2):**
  - The footer "Criteria: outputs/eval/summary.md" names our own file as the source of the jury weights. Write `Criteria and weights: AFS challenge brief · mapping: outputs/eval/summary.md`.
  - The criterion names differ from the brief: "AFS grounding" should be "Use of AFS knowledge", and "Prototype" should be "Prototype & presentation".
- **N9 (slide 3):** the screenshot's text is about 5 pt at 16:9 (unreadable on a shared screen), and it shows an ad-hoc acrylate enquiry, not an H case. Crop to the headline, status strip and two margin notes at 2× scale. Better still, show one H answer, e.g. the H04 brief answer and proposal from outputs/final/H04.md:7–20. The jury grades H01–H06, and no slide shows a single real H answer, only aggregates.
- **N11 (slide 5):** both crops are cut off. The options crop ends mid-row at "Confidence", and the setup crop cuts the node labels ("To be decided", "ATR probe", "MIR spectrometer"). The extended cell also reads "MIR, ATR probe; MIR, ATR probe + Raman" (duplicated text). Re-crop with labels visible, or crop from a run whose extended cell is clean.
- **N12 (slide 10):** "Next" has no repo URL and no team member names. Add `github.com/<owner>/<repo>` above the `uv` block, and the names in the footer.
- **N13 (all slides):** the section labels are off by one from the page counter ("01 · THE PROBLEM" on page "2 / 10"). Drop the section numbers, or start at 02.
- **N14 (slides.md):** it says "Outline; the final slide text is in slides.html", but it has diverged from the PDF (no 763/758 line, different slide 3 bullets). Either regenerate it or add "(outline only, may differ from the PDF)".
- **Design overall:** good. Typography is consistent (Newsreader / IBM Plex), contrast is high (dark on cream), there is one accent colour, every numeric slide has a source footer, and density is acceptable except slides 7 and 8, which are at the limit. Slides 3 and 5 are the weak spots, because their images are too small or cut off.

### Submission (docs/SUBMISSION.md)
- **N8 (line 11):** "about 2–6 s" becomes `1.4–6.3 s per question in a 10-question live check (about $0.004 each)`.
- **N15 (line 9):** "asks only decision-relevant clarification questions". A07 got 4 where 3 were allowed (README:121), so write `asks clarification questions tied to the option they would change`.
- **N16:** there is no limitations line, so the submission reads as positives only. Add one line: `**Known limits:** answers are long (about 3,000+ words vs 300–400 in AFS's worked answers); "verified" means the quote is on the cited page, not that it entails the claim; a re-assessment can change the method without a clear reason (README "Known limitations").`
- **N17 (line 22):** "judged against the AFS evaluation data" should say who judged: "by four blind LLM judge agents against the AFS evaluation data" (README:128 does this already).

### Video (docs/video/*)
- **N10 (closing card, build_video.py:102–106):** the header "From STATUS.md (freeze-1, production models mix-a, external search live)" sits above "~105 s mean time per case", which comes from the pre-freeze gate run (code c226e48). The card also mixes the held-out set with dev numbers. Replace the third stat with `("97–184 s", "per case", "H01–H06 held-out set, run once")`, and the header with `"H01–H06 held-out set, tag freeze-1, production models mix-a, external search live."`
- **N18 (captions #15, 1:36–1:42; frame 16):** "the options table is shown again inside the answer" describes a bug that 4ac8f83 fixed after recording ("options table renders once per answer"). The video no longer matches the shipped app. Drop frame 16 from SHOTLIST (build_video.py:40), keep frame 17 with the caption `Inline result blocks: the setup sketch of the Raman (simple) option and the first feasibility test.`, and add one line to script.md "Things seen" #2: "fixed after recording in 4ac8f83".
- **N19 (story):** the video goes title card → demo → numbers. There is no problem statement and no limits. 2:35 of the 5:00 allowance is unused. Add two 8–10 s cards with Pillow, the same way as card_title:
  - Problem card: "Customers ask: which method and probe should we test first? A good first answer screens UV-Vis/NIR/MIR/Raman/fluorescence against sample, probe and fiber limits, proposes one option, asks what would change it, and cites AFS material."
  - Limits card (before the closing card): "Known limits: answers are long; 'verified' = quote on page, not entailment; confidence rarely varies; a re-assessment can shift the method; a full run takes 1.5–3 min."
  - The result is about 2:45, still well under 5 min.
- **N20 (caption speed):**
  - Captions #6 (5 s, 17 words, 3.4 w/s), #13 (4 s, 18 words, 4.5 w/s) and #19 (7 s, 22 words, 3.1 w/s) are too fast to read while also looking at a dense screenshot.
  - In SHOTLIST, set 07_repair to 7 s, 14_followup_wait to 6 s and 20_v2 to 9 s. Give 08_answer and 21_what_changed about 10 s each: they carry the most content.
- **N21 (frame 02, 0:04–0:10):** the start screen is scrolled so that the header and the "What do you want to measure?" heading are off screen. The viewer sees a list of example titles. Frame 03 fixes this 6 s later. Either cut frame 02 to 3 s, or recaption it as the example list ("Finished examples, including the H01–H06 held-out cases, open without an API key").
- **N22 (caption #1):** the backticks in "`uv run afs-assist ui`" are burned into the frame literally. Remove them, or rely on the monospace in the frame.
- **N23:** the video never opens an H01–H06 output, which is the thing the jury grades. If you re-record later, add one frame of a finished H case.
- **N24 (visible product oddities a juror may question; src/ scope, for the other reviewers):**
  - Frame 11: simple option (Raman, high cost) has confidence Medium, while the recommended option (NIR, average cost) has Low.
  - Frame 17: the simple-option sketch keeps the footer "Dashed: auxiliary sensor", but there is no dashed sensor.
  - Frame 20: the v2 margin numbering restarts at 4 after the follow-up used 5–7 (already in README:179).
- **N25 (build_video.py:125–127):** `shutil.rmtree(FR)` deletes the committed `docs/video/frames/` before writing the frames again. That is fine if every name comes back. If a SHOTLIST entry is removed (as in N18), the old PNG disappears from the working tree, and committing that would be a deletion. Under the user's git rule this needs the user's explicit OK, or else keep 16_followup_blocks.png on disk and simply leave it out of the video.
- **Re-record or not:** **No full re-record.**
  - Every blocking and high-value video fix is a caption or card change. All the source images exist in docs/video/frames/, and they are the clean screenshots (script.md:6), so `build_video.py` can rebuild without new live calls.
  - A re-record would cost about $0.09 and 30–45 min. Because of run-to-run variance it could produce a different oddity.
  - Re-record only if time remains after B1–B4 and N1. In that case use current master (4ac8f83+), answer Q1 (range and accuracy) instead of temperature, and add one frame of an H output.

### Documentation, other
- **N26 (pyproject.toml:4):** `description = "Add your description here"`, a placeholder a jury will see. Replace with `"Cited first technical assessments for in-line spectroscopy enquiries (AFS challenge, Team Helios)"`.
- **N27 (ARCHITECTURE.md):** it is accurate against the code. I spot-checked MAX_REPAIR_ROUNDS = 2 (pipeline.py:53), the Host 400 and cross-origin 403 responses (ui/server.py:425,432), HISTORY_TURNS = 3 (chat.py:47), the conversation path (chat.py:3) and 41 distinct check names. It has no "How to extend" section (new PDFs → `kb build`, new rule in rules.yaml + `kb check`, new model config through AFS_MODELS_CONFIG, new chat block). Item 3 of the review covers that; a 10-line section here would serve the jury's "easy for an expert to review" criterion.
- **N28 (code comments):** acceptable. Every module in src/afs_assistant has a module docstring, and the key modules (verify, pipeline, options, chat, render, llm, external/step) have 14–24 docstrings each. Comments often cite D-0xx ids, which point a reader to DEVIATIONS.md. Nothing to fix.

## 5. Test gaps
- No automated check that the numbers in the docs match the committed outputs. A 40-line script (offline, like the recomputation above) could assert the H totals, the gate range, the bake-off cells and the chat live-check figures against README, the slides HTML and SUBMISSION, and would have caught B2 and N5.
- `build_video.py` has no dry-run mode and no test. It needs macOS system fonts (/System/Library/Fonts/Supplemental) and /opt/homebrew/bin/ffmpeg, so the video is not rebuildable on another OS. Document this in script.md, or fall back to the fonts committed under src/afs_assistant/ui/static/fonts/.
- Not verified here: `uv run afs-assist ui` starting with no OPENROUTER_API_KEY (README:23). The code raises only when the real client is built (llm.py:200–202), which suggests it starts. A one-line test that starts `create_app` without the key would prove it.
- The slides PDF is not regenerated by any script in the repo (Chrome headless was used, according to the PDF metadata). Record the export command in slides.md.

## 6. Smallest next patch (in order; about 30–40 min, $0)
1. **SUBMISSION.md:** B2 line 22; B3 line 8; N8 line 11; N15 line 9; N16 add a limits line; N17. Line 31 waits for the user to publish (B1).
2. **build_video.py:**
   - B3 line 114.
   - B4 caption on line 45.
   - N10 lines 102–106.
   - N18: drop the 16_followup_blocks entry from SHOTLIST (line 40) and recaption 17.
   - N20 durations.
   - N19: add problem and limits cards.
   - Rebuild with WORKDIR/shots = copies of docs/video/frames/*.png under their original shot names (map in SHOTLIST column 2, e.g. `08_answer.png → s04_answer_top.png`): `uv run --with pillow python docs/video/build_video.py WORKDIR`.
   - Before committing, run `git status`. If 16_followup_blocks.png shows as deleted, restore it (N25).
   - Update script.md (shot table, length, "Things seen" #2) and README:21 / SUBMISSION:28 with the new length.
3. **slides.html:**
   - N5 (764).
   - N7 footer and criterion names.
   - N12 repo URL placeholder and names.
   - Re-export slides.pdf (10 pages).
   - If time allows: N9 (replace the slide 3 screenshot with the H04 answer crop) and N11 re-crops.
4. **README.md:** N1 (run line and the Brief → where map), N2, N3, N4. **pyproject.toml:** N26.
5. After the user publishes: B1, then re-check every relative link in README on GitHub.

## Executive summary
1. Verdict: NEEDS_FIXES. Four blocking items, each a small text or caption fix. No re-record is needed.
2. I recomputed the numbers from committed files. H01–H06, the gate run, the bake-off, the chat live-check, the KB counts and the word counts all trace exactly.
3. Wrong: SUBMISSION.md:22 says "about 5× faster"; the data say 6× (504 vs 84 s).
4. Stale: slide 8 says "763 tests"; the current count is 764 passed, 2 skipped. Mislabelled: the video closing card puts "freeze-1" over the pre-freeze ~105 s gate mean.
5. Overclaim: "every important claim quotes AFS word for word" (video closing card, SUBMISSION.md:8). Our own README limitation and video frame 08 contradict it.
6. Video: 2:25, captions match the frames and the cost/time records. But caption #20 frames an unexplained NIR→NIR+Raman flip, whose headline contradicts its body, as a feature; caption #15 shows a duplicate-table bug fixed since. It has no problem card and no limits card.
7. Fix the video by rebuilding from the committed clean frames with new captions and two cards. That costs $0 and no live calls, and the result is about 2:45, under the 5-minute cap.
8. Slides: clean, consistent design with sourced footers. Weak spots: an unreadable screenshot (slide 3), cut-off crops (slide 5), no H answer shown, and no repo URL or team names on the last slide.
9. README: accurate, and the CLI flags match `--help`. It is not jury-first: no run command in Quick start, results start at line 90, and there is no brief→section map. The pyproject description is a placeholder.
10. Submission blocker outside the docs: the repo must be public (organiser rule), and SUBMISSION.md:31 still has no link. That needs the user's decision and the item-10 sanitise pass first.
