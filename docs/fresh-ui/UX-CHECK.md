# UX check: four chat-first concepts

Date: 2026-10-18. Method: the Hallmark anti-slop gates (the relevant subset of its 69), the NN/g 10 heuristics, WCAG 2.x contrast computed from the real OKLCH tokens (OKLCH → linear sRGB → relative luminance; script kept in the session scratchpad), and a 5-second test of each answer screen. Screens were rendered with Playwright at 1440 px and 390 px. Checked so far: no horizontal scroll at 390 or 1440 in any concept. 320/375/414/768 px have not been checked yet.

This is a self-check by the author, not an independent review. A separate reviewer pass is still needed (global rule: no self-approval).

## Honesty of content

- Every sentence, citation, quote, cost class, confidence reason, rule ID and timing comes from `outputs/dev/D03.json` / `.md` (run time 821.7 s = 13 min 42 s; intake 58.7 s; 29/29 quotes; 167 checks). The source-page context shown in verification views is the real S01 p.18 text from `knowledge/pages.jsonl`.
- Turns after the user adds new facts (“60 °C, up to 200 NTU”) are marked **illustrative** on screen. They reuse only v1 claims and say that no source gives an NTU limit. They do not invent an outcome.
- One risk: D03 was 13.7 min, while the brief says “1–10 minutes”. The screens show the real time and do not promise a shorter one.

## Contrast (real token pairs, WCAG 2.x ratio)

| Concept | Pair | Ratio | Result |
|---|---|---|---|
| C1 light | ink / paper | 16.0 | AAA |
| C1 light | muted / paper | 6.4 | AA |
| C1 light | oxide accent / paper (refs, stamp) | 5.9 | AA |
| C1 dark | ink / paper · muted · accent | 15.4 · 7.6 · 7.3 | AAA / AAA / AAA |
| C2 light | ink / paper · muted / paper | 15.5 · 6.5 | AAA / AA |
| C2 light | amber cloud stroke / paper (non-text) | 4.5 | passes 3:1 |
| C2 light | ink / amber fill (selected part) | 10.2 | AAA |
| C2 dark | ink · muted · amber / paper | 15.5 · 7.5 · 9.7 | AAA |
| C3 light | ink / paper · muted / panel | 16.5 · 5.9 | AAA / AA |
| C3 light | indigo / cite chip wash | 6.0 | AA |
| C3 light / dark | ink / highlighter | 13.7 / 6.3 | AAA / AA |
| C4 dark | ink / paper · muted / raised | 16.5 · 7.7 | AAA |
| C4 dark | lime / paper · ink on lime button | 13.0 · 12.2 | AAA |
| C4 dark | amber status / raised | 10.0 | AAA |
| C4 light | ink · accent / paper · muted / raised | 16.6 · 6.8 · 6.5 | AAA / AA / AA |

All measured pairs pass AA. Nothing carries meaning by colour alone: status has a text stamp, questions have IDs, and diffs use ✓ ~ = symbols as well as colour.

## Hallmark anti-slop gates (relevant subset)

| Gate | C1 Brief | C2 Line | C3 Desk | C4 Casebook |
|---|---|---|---|---|
| 1 banned display font | pass (Newsreader) | pass (Instrument Sans) | pass (Hanken Grotesk) | pass (Bricolage) |
| 2/5 gradients, gradient text | none | none | none | none |
| 3 three-equal icon cards | none | none | none | none |
| 4 card-in-card | pass | pass (the sheet reference sits inside a chat turn, which is not a card) | pass | pass (big blocks sit directly in the flow) |
| 6 side-stripe card | **borderline**: opened margin note uses a 2 px left rule (Tufte margin, not a card) | pass | pass | **borderline**: drawer context quote has a 3 px left rule |
| 8 pure #000/#fff | pass, all tinted OKLCH | pass | pass | pass |
| 24 zero-chroma greys | pass | pass | pass | pass |
| 25 accent > 5 % of viewport | pass | pass (amber only on clouds and the selected part) | pass | pass (lime on refs, current dot, Send) |
| 39 more than 3 font families | 3 | 2 | 2 | 3 |
| 56 invented metrics | pass, all numbers from the run | pass | pass | pass |
| 57 re-drawn chrome | pass (phone view is a real 390 px iframe, no fake frame) | pass | pass | pass |
| 58 inline token bypass | **minor fail**: a few inline `style` spacing values | **minor fail**: wordmark SVG uses an inline `font-family` | **minor fail**: inline styles in the running pane | minor (inline styles in two places) |
| 26 off-scale spacing | minor (two inline offsets) | pass | pass | pass |
| 28 full 8 states | **partial**: hover, focus and active exist; disabled and loading are not drawn for every control | partial | partial | partial |
| 59 two-line clickable text | pass | pass | pass | intentional: question replies have a label and an “affects” line |
| 66 tag-left / header-right | pass | pass | pass | pass |

The minor fails are mockup shortcuts. In the build, every value moves into the token block and every control gets all 8 states. Not done in the mockup: Hallmark's `tokens.css` and `.hallmark/log.json` outputs, because the task limited writes to `docs/fresh-ui/`.

## NN/g heuristics (strong / weak per concept)

| Heuristic | C1 Brief | C2 Line | C3 Desk | C4 Casebook |
|---|---|---|---|---|
| 1 Visibility of status | Strong: pinned current-recommendation strip, timed activity lines | Strong: revision tabs plus title block | Strong: steps plus a quote counter | Strong: large clock, version rail |
| 2 Match to real world | Memo language, page refs | **Strongest**: P&ID tags, revision clouds, title block | Research-tool idioms | Plain language, big type |
| 3 User control | Stop, pin, expand, copy | Rev A/B switch, option switch | Pin, cite toggle | Fold and unfold turns, versions |
| 4 Consistency | High | Two places to look (chat and sheet) need clear links | High | High |
| 5 Error prevention | Placeholders say “or leave blank” | Answers bound to clouds | n/a | Questions say what they affect |
| 6 Recognition over recall | Chips for questions and follow-ups | Clouds on the drawing show what's open | Pinned rail | Reply chips |
| 7 Flexibility | Margin for experts, chips for novices | Experts click parts | **Best for experts**: claim → quote → page | **Weakest for experts**: low information density |
| 8 Minimalist design | Good; the long thread grows tall | Busy at first glance | Dense but orderly | **Most minimal** |
| 9 Recover from errors | “What changed” diff | Rev A/B compare | Diff card | Large diff |
| 10 Help | Hints in the composer | Legend | Source list | Hints |

## 5-second test (answer screen at 1440, judged by the author, not real users)

| Concept | What you get in 5 s | Verdict |
|---|---|---|
| C1 Brief | The pinned strip and the verdict headline (“Start with NIR transmission/transflection.”), the PROVISIONAL stamp, and the margin quote next to the claim | Passes: verdict, status and evidence are visible together |
| C2 Line | A drawing with amber clouds and a title block; the verdict is in the chat headline | Partial: impressive, but the eye goes to the drawing before the verdict |
| C3 Desk | The highlighted claim and the highlighted page quote, plus the recommendation card | Passes for engineers; on a projector three panes look busy |
| C4 Casebook | A huge “Still: start with NIR transmission/transflection.”, status pills, the diff | Passes best on a projector; least room for detail |

## Comparison

| | C1 Brief | C2 Line | C3 Desk | C4 Casebook |
|---|---|---|---|---|
| Chat-first mental model | Classic thread + evidence margin | Thread + live canvas | Thread + evidence pane + pinned rail | Stage-mode thread + versions |
| Verify a claim | In place, in the margin (no click needed to see the quote) | Popover on the sheet | Side pane with full page text | Drawer, large type |
| Show setup / options | Inline blocks | Always visible on the sheet | Pinned cards | Large inline blocks |
| “What changed” | Table diff in the turn | Change list + sheet revision | Diff card | Large diff + version rail |
| Jury on a projector | Good | Very impressive, busier | Busy | **Best** |
| AFS engineer reuse | **Best** (memo text copies cleanly) | Good | Very good | Fair |
| Build effort tonight (Jinja + htmx) | **Low**: one column, partial per block | **High**: SVG sheet, revisions, click targets | Medium: three panes, pane swap | Low–medium |
| Phone | Good (margin folds) but the sketch is tiny; it needs C2's vertical chain | Good (chain view) | Good | Good |

## Recommendation

**Build C1 Brief as the base, and take two things from the others:** C4's stage mode as a “Present” toggle (larger type, earlier turns folded, version rail) for the live demo, and C2's vertical chain list as the phone fallback for the setup sketch.

Why C1:
1. It meets both users with one layout. Engineers verify claims without clicking (evidence margin) and copy clean memo text. The jury reads the verdict, status and quote within 5 seconds.
2. It is the cheapest chat-first build tonight. Each block (recommendation, options, sketch, parameters, questions, diff) is one Jinja partial returned by htmx into a single thread, with no pane orchestration.
3. Its evidence model maps directly onto the existing verification data (doc, page, quote, check result).

Why not C2 as the base, even though it is the most original: the live sheet carries the most risk tonight (SVG layout per option, revision diffing, hit targets). It is worth doing later as a canvas side panel.

## Open issues before building

- An independent reviewer should check this file and the screenshots.
- C1 phone: replace the tiny SVG sketch with the vertical chain under 760 px.
- All concepts: draw the disabled and loading states, and move inline styles into tokens.
- Projector check: test the C1 “Present” toggle on a real projector or at 1280×720, 150 % zoom.
- A real re-run is needed before “what changed” can show real output. The diff must be computed by code between two runs, not written by the model.
