# Demo video: script and shot list

- **File:** `docs/video/demo.mp4`, 1440×900, H.264 (yuv420p), 30 fps, **145 s (2:25)**, about 2.9 MB, no audio.
- **Captions:** drawn into the frames (Pillow, Arial 27 px). The same text with its timings is in `docs/video/captions.srt`.
- **Key frames:** `docs/video/frames/*.png`, 22 frames without captions (title card, 20 app screenshots, closing card).
- **Rebuild:** `uv run --with pillow python docs/video/build_video.py WORKDIR`. WORKDIR/shots/ holds the raw Playwright screenshots. Those stayed in the session scratchpad and are not committed; the committed frames are the same images without captions.
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
| 2 | 0:04–0:10 | 02_start | Start screen | Start screen: `uv run afs-assist ui` serves a local page. Describe what you want to measure. |
| 3 | 0:10–0:17 | 03_enquiry | Enquiry typed in | A new, generic enquiry: ethanol in a clear, filtered fermentation broth in a pipe; GC is the lab reference. |
| 4 | 0:17–0:21 | 04_running | Job started (2 s) | Get assessment: the real pipeline starts (production models, live literature search). |
| 5 | 0:21–0:26 | 05_steps | Step list at 0:34 | Pipeline steps with timings: read the enquiry, screen methods against the AFS rules, assess. |
| 6 | 0:26–0:33 | 06_feed | Activity feed at 1:23 | Live activity feed: methods ruled out with the S01 Table 1 reason; 29 citations checked against the AFS pages. |
| 7 | 0:33–0:38 | 07_repair | Repair round in the feed | One hard check failed, so the failed checks go back to the model for a repair round. |
| 8 | 0:38–0:46 | 08_answer | Answer turn, pinned strip, margin quotes | Answer after 107 s (pipeline wall time, $0.036): the recommendation, a pinned strip (status, confidence, open questions), quotes in the margin. |
| 9 | 0:46–0:54 | 09_recommendation | Status, confidence, next step | Status, confidence with its reason, and the next step. Every quote beside the answer is word for word from AFS. |
| 10 | 0:54–1:03 | 10_verify | Margin quote 1 opened (verification view) | Open a margin quote: the stored S01 p.18 page text with the quote highlighted, marked verified (exact match). |
| 11 | 1:03–1:11 | 11_options | Options table | Options: simple, recommended, extended. Cost class comes from S01 Table 1 (p.6) rows; it is not a price. |
| 12 | 1:11–1:19 | 12_setup | Setup sketch | Setup sketch drawn by code from the proposed option; the dashed sensor is auxiliary, to be confirmed with AFS. |
| 13 | 1:19–1:23 | 13_followup | Follow-up typed in the composer | A follow-up in the composer: "Why not Raman as the first choice?" |
| 14 | 1:23–1:27 | 14_followup_wait | Follow-up running | Follow-up questions are answered from the assessment and the AFS pages: one model call, quotes checked before display. |
| 15 | 1:27–1:36 | 15_followup_answer | Cited answer, margin quotes 5–7 | Answer in 5.3 s, $0.006: each point cited (S01 p.18, p.11, p.6), or marked as engineering judgement. |
| 16 | 1:36–1:42 | 16_followup_blocks | Inline options block | Inline result blocks: the options table is shown again inside the answer. |
| 17 | 1:42–1:48 | 17_followup_setup | Inline Raman setup and feasibility test | ...plus the setup sketch of the Raman (simple) option and the first feasibility test. |
| 18 | 1:48–1:55 | 18_answer_question | Q2 answered in place | Answer an open question in place: process temperature about 32 °C, 28 to 36 °C during a batch. |
| 19 | 1:55–2:01 | 19_reassess_running | Re-assessment running | Update the recommendation: the full assessment runs again with the new fact (v2). |
| 20 | 2:01–2:08 | 20_v2 | v2 answer | v2 after 147 s ($0.046): the temperature range is now part of the advice; the open questions drop to Q1 and Q3. |
| 21 | 2:08–2:17 | 21_what_changed | "What changed, v1 → v2" block | What changed, v1 to v2: the proposed setup now tests NIR and Raman together; status and confidence unchanged. |
| 22 | 2:17–2:25 | 22_closing | Closing card | none (numbers below) |

## Closing-card numbers (taken from STATUS.md only)

- **0 hard failures** and **120/120 citations verified**: STATUS.md entry 12:33, "H01–H06 run once (12:29–12:32, `--external live`)".
- **~105 s mean per case**: STATUS.md entry 11:52, "5.8 gate PASS on mix-a … Wall time per case 35–247 s (mean ~105 s)". This is the 19-case dev + adversarial gate, not H01–H06 (H01–H06 took 97–184 s per case). The card labels it that way.

## Live cost spent

| Call | Wall time | Cost (run record) |
|---|---|---|
| Assessment v1 (`ui-adhoc-20261018T103823Z-e0e0`) | 106.7 s (repair 45.5 s, external 5.5 s) | $0.035978 |
| Follow-up answer (chat_answer, GLM-5.3-Flash) | 5.33 s | $0.006226 |
| Re-assessment v2 (`ui-adhoc-20261018T104143Z-1683`) | 147.4 s (repair 79.8 s, external 10.4 s) | $0.045550 |
| **Total** | | **$0.0878** |

OpenRouter `/api/v1/credits` reported total_usage 25.3447 before and 25.4325 after, a difference of $0.0878, which matches the run records. The budget was ≤ $0.30.

## Things seen during recording (not fixed here; src/ was out of scope)

1. **v2 changed the proposed method.** v1 proposed NIR transmission/transflection alone. After only the temperature answer, v2 proposed NIR together with a Raman probe. The "What changed" block reports this honestly. A temperature fact does not obviously justify adding Raman, so this is probably run-to-run variation in the model.
2. **The follow-up answer showed the Options table twice** in its inline blocks: once with the recommended setup sketch, and again with the simple-option sketch. The second block repeats the table.
3. **Margin-quote numbering across turns.** v1 uses 1–4 and the follow-up uses 5–7, but the v2 margin starts again at 4. So within one page, numbers 4–7 refer to different quotes in different turns.
4. During both assessments the "Searching literature" step was still shown as pending while the repair round ran. External search ran afterwards (2 verified items each time). This matches the step order and is not a fault.
