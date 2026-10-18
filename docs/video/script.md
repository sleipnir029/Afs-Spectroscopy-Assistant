# Demo video: script and shot list

- **File:** `docs/video/demo.mp4`, 1440×900, H.264 (yuv420p), 30 fps, **173 s (2:53)**, about 3.2 MB, no audio.
- **Captions:** drawn into the frames (Pillow, Arial 27 px). The same text with its timings is in `docs/video/captions.srt`.
- **Key frames:** `docs/video/frames/*.png`, without captions: 4 cards (title, problem, known limits, closing) and 20 app screenshots. The video uses 23 of them; `16_followup_blocks.png` stays in the repo but is not shown (it shows a bug fixed after recording, see "Things seen" #2).
- **Rebuild:** `uv run --with pillow python docs/video/build_video.py [WORKDIR]` (macOS: needs the system fonts in /System/Library/Fonts/Supplemental and /opt/homebrew/bin/ffmpeg). The script reads the committed screenshots in `frames/` in place and never deletes or rewrites them; it redraws only the four cards. WORKDIR (default: a temp dir) gets the captioned frames and the ffmpeg concat list. No live model calls.
- **Rebuilt:** 2026-10-18 from the committed frames (final review fix F7): corrected closing card, honest "What changed" caption, frame 16 dropped, slower captions, problem and limits cards added. The 2:25 first cut is in git history.
- **Recorded:** 2026-10-18, 12:38–12:44 CEST, on master at 094d955 (freeze-1 pipeline, `config/models.yaml` mix-a, sha256 1437179f…), `--external live`.

## How it was recorded

- The browser was Playwright (Chromium) with a 1440×900 viewport. Every frame is a real screenshot of the live page. Nothing was edited or mocked.
- The server was the production app, `afs_assistant.ui.server.create_app(outputs=<scratchpad>/outputs, external="live")`, served by uvicorn on 127.0.0.1:8765. This is what `uv run afs-assist ui` starts, with one difference: the outputs root points to a scratch folder. The `ui` command has no `--outputs` flag, and this task was not allowed to write to `outputs/ui/`. The dev, adversarial and final sets were copied into the scratch folder so that the start page lists the same finished examples.
- As usual, each assessment wrote its provenance record (`runs/<run_id>/`, which is gitignored) and a commit on the provenance ref. That is what the app always does. Nothing was committed to master.
- After recording, the server was stopped and the browser closed.

## The enquiry used

It is new and generic, written for the demo, and not taken from `scenarios/*.jsonl`:

> We produce ethanol by fermentation. After filtration the broth is a clear, slightly yellow aqueous liquid that flows through a stainless steel pipe to a holding tank. We would like to follow the ethanol concentration in-line in that pipe instead of taking manual samples. Today we take samples a few times per shift and measure them by gas chromatography in our lab, so GC would be our reference method. Which spectroscopic method and probe would you suggest we test first, and what do you need to know from us?

Follow-up question: "Why not Raman as the first choice?"

Answer to open question Q2 (a demo fact, typed into the question's field before "Update the recommendation"): "About 32 °C; it varies between 28 and 36 °C during a batch."

## Shot list

| # | Time | Frame | What is shown | Caption |
|---|---|---|---|---|
| 1 | 0:00–0:04 | 01_title | Title card | none |
| 2 | 0:04–0:14 | 01b_problem | Problem card: what an AFS sales engineer gets and needs | none (text on the card) |
| 3 | 0:14–0:21 | 02_start | Start screen (examples, finished examples) | The local app (uv run afs-assist ui): type an enquiry, try an example, or open a finished one. |
| 4 | 0:21–0:28 | 03_enquiry | Enquiry typed in | A new, generic enquiry: ethanol in a clear, filtered fermentation broth in a pipe; GC is the lab reference. |
| 5 | 0:28–0:33 | 04_running | Job started (2 s) | Get assessment: the real pipeline starts (production models, live literature search). |
| 6 | 0:33–0:39 | 05_steps | Step list at 0:34 | Pipeline steps with timings: read the enquiry, screen methods against the AFS rules, assess. |
| 7 | 0:39–0:46 | 06_feed | Activity feed at 1:23 | Live activity feed: methods ruled out with the S01 Table 1 reason; 29 citations checked against the AFS pages. |
| 8 | 0:46–0:53 | 07_repair | Repair round in the feed | One hard check failed, so the failed checks go back to the model for a repair round. |
| 9 | 0:53–1:02 | 08_answer | Answer turn, pinned strip, margin quotes | Answer after 107 s (pipeline wall time, $0.036): the recommendation, a pinned strip (status, confidence, open questions), quotes in the margin. |
| 10 | 1:02–1:10 | 09_recommendation | Status, confidence, next step | Status, confidence with its reason, and the next step. Every quote beside the answer is word for word from AFS. |
| 11 | 1:10–1:17 | 10_verify | Margin quote 1 opened (verification view) | Open a margin quote: the stored S01 p.18 page text with the quote highlighted, marked verified (exact match). |
| 12 | 1:17–1:24 | 11_options | Options table | Options: simple, recommended, extended. Cost class comes from S01 Table 1 (p.6) rows; it is not a price. |
| 13 | 1:24–1:32 | 12_setup | Setup sketch | Setup sketch drawn by code from the proposed option; the dashed sensor is auxiliary, to be confirmed with AFS. |
| 14 | 1:32–1:37 | 13_followup | Follow-up typed in the composer | A follow-up in the composer: "Why not Raman as the first choice?" |
| 15 | 1:37–1:45 | 14_followup_wait | Follow-up running | Follow-up questions are answered from the assessment and the AFS pages: one model call, quotes checked before display. |
| 16 | 1:45–1:52 | 15_followup_answer | Cited answer, margin quotes 5–7 | Answer in 5.3 s, $0.006: each point cited (S01 p.18, p.11, p.6), or marked as engineering judgement. |
| 17 | 1:52–1:59 | 17_followup_setup | Inline Raman setup and feasibility test | Inline result blocks: the setup sketch of the Raman (simple) option and the first feasibility test. |
| 18 | 1:59–2:06 | 18_answer_question | Q2 answered in place | Answer an open question in place: process temperature about 32 °C, 28 to 36 °C during a batch. |
| 19 | 2:06–2:11 | 19_reassess_running | Re-assessment running | Update the recommendation: the full assessment runs again with the new fact (v2). |
| 20 | 2:11–2:20 | 20_v2 | v2 answer | v2 after 147 s ($0.046): the temperature range is now part of the advice; the open questions drop to Q1 and Q3. |
| 21 | 2:20–2:34 | 21_what_changed | "What changed, v1 → v2" block | What changed, v1 to v2: the method now adds a Raman probe; status and confidence unchanged. A temperature alone does not justify that: a re-assessment is a fresh model run and can shift (a known limitation). |
| 22 | 2:34–2:44 | 21b_limits | Known limits card (3 lines) | none (text on the card) |
| 23 | 2:44–2:53 | 22_closing | Closing card | none (numbers below) |

Captions run at 2.1–2.7 words per second; the three that were too fast in the first cut (repair round, follow-up running, v2) are now 2.25–2.44. Card texts are in `build_video.py` (`card_problem`, `card_limits`, `card_closing`).

## Closing-card numbers (H01–H06, recomputed from `outputs/final/H0*.json`)

- Header: "H01–H06 held-out set, run once at tag freeze-1". The run manifests carry code_sha 1b3a7b9, which is the commit tagged `freeze-1` (STATUS.md entry 12:33).
- **0 hard failures** and **120/120 citations verified**: `verification.summary` in the six files (hard_failures 0 each; citations 14+16+21+25+22+22 = 120, all verified, quote_status exact).
- **97–184 s per case** and **$0.288 for all six cases**: `manifest.timings_s.wall` 97.2–183.9 s; `manifest.cost_usd` sums to $0.2882. Same as README "Results".
- Closing line: "Every quote is checked word for word against its AFS page; claims without a source are labelled." It replaces the earlier "every important claim quotes … word for word", which overclaimed (README "Known limitations": a citation can be used for a point the page does not really make).
- The first cut showed "~105 s mean per case". That is the 19-case dev + adversarial gate run before the freeze (STATUS.md 11:52), not freeze-1, so it was replaced.

## Known-limits card (from README "Known limitations")

- Reports are long: 3,000–3,500 words (H01–H06: 3,058–3,455), vs 300–400 in the AFS worked answers.
- "Verified" means the quote is on the cited page, not that it fully supports the claim.
- A re-assessment is a fresh model run and can shift the method, as in this demo.

## Live cost spent

| Call | Wall time | Cost (run record) |
|---|---|---|
| Assessment v1 (`ui-adhoc-20261018T103823Z-e0e0`) | 106.7 s (repair 45.5 s, external 5.5 s) | $0.035978 |
| Follow-up answer (chat_answer, GLM-5.3-Flash) | 5.33 s | $0.006226 |
| Re-assessment v2 (`ui-adhoc-20261018T104143Z-1683`) | 147.4 s (repair 79.8 s, external 10.4 s) | $0.045550 |
| **Total** | | **$0.0878** |

OpenRouter `/api/v1/credits` reported total_usage 25.3447 before and 25.4325 after, a difference of $0.0878, which matches the run records. The budget was ≤ $0.30.

## Things seen during recording (not fixed here; src/ was out of scope)

1. **v2 changed the proposed method.** The video caption on the "What changed" frame says so and calls it a known limitation. v1 proposed NIR transmission/transflection alone. After only the temperature answer, v2 proposed NIR together with a Raman probe. The "What changed" block reports this honestly. A temperature fact does not obviously justify adding Raman, so this is probably run-to-run variation in the model.
2. **The follow-up answer showed the Options table twice** in its inline blocks: once with the recommended setup sketch, and again with the simple-option sketch. The second block repeats the table. Fixed after recording in 4ac8f83 ("options table renders once per answer"); the frame that showed it (`16_followup_blocks.png`) is no longer in the video.
3. **Margin-quote numbering across turns.** v1 uses 1–4 and the follow-up uses 5–7, but the v2 margin starts again at 4. So within one page, numbers 4–7 refer to different quotes in different turns.
4. During both assessments the "Searching literature" step was still shown as pending while the repair round ran. External search ran afterwards (2 verified items each time). This matches the step order and is not a fault.
