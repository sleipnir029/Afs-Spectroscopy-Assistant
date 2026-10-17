# UI research: from "report page" to an answer you can ask about

_Written 2026-10-17 23:11 CEST by a background research agent (Claude). Input for the Phase 5 web-UI redesign. No code was changed. Labels: **[P]** = primary source (vendor docs, design system, NN/g, standard) fetched today; **[S]** = secondary (reviews, teardowns, press). Versions and licences were read from the npm registry today._

**The problem in one line.** The current page lists ~20 equal-weight sections (Answer, Proposal, Options compared, Open questions, Expert detail with 12 sub-sections, How this answer was made). It reads like a datasheet. The user can't see where to ask a question, and the setup isn't shown as a picture.

---

## (a) Patterns that fit this app

**1. Answer first, in plain words, then the detail.** Put a 2–3 sentence verdict at the top ("Yes, likely feasible with NIR transflection at the line; confidence medium") before any section list. Teardowns of Perplexity describe the order *direct answer → sources → related questions* as the core of why it feels easy [S]. NN/g found Google's AI Mode answers "text heavy and very hard to scan" and saw users give up on long prose blocks [S, summary of NN/g study].
- https://www.925studios.co/blog/perplexity-design-breakdown [S]
- https://www.searchengineworld.com/influential-nielsen-norman-group-tees-off-on-google-ai-google-ai-mode [S]
- *Fit:* our `Answer` block exists but sits among many peers. Make it the hero card. Everything else hangs below it.

**2. Two disclosure levels at most, and nothing most readers need is hidden.** NN/g: designs that "go beyond 2 disclosure levels typically have low usability" [P]. GOV.UK *Details*: use it for "information that only some users will need"; "Do not use the details component to hide information that the majority of your users will need" [P].
- https://www.nngroup.com/articles/progressive-disclosure/ [P]
- https://design-system.service.gov.uk/components/details/ [P]
- *Fit:* level 1 = verdict, schematic, options, open questions. Level 2 = one "Expert detail" drawer (assumptions, spectral range, verification log, external evidence). Today's Expert detail has 12 sub-headings. Collapse them into tabs or `<details>` inside that one level.

**3. A citation chip next to the claim, a hover card with the quote, and a click that opens the passage.** NotebookLM: hovering a citation shows "the full quoted passage", and clicking scrolls the source viewer to it [P]. NN/g: "Place sources directly next to the specific claim or sentence they support" [P]. Wikipedia Page Previews (hover cards) cut back-button use and let readers check a term without leaving the page, with a ~0.01 % disable rate [P].
- https://support.google.com/notebooklm/answer/16179559 [P]
- https://www.nngroup.com/articles/explainable-ai/ [P]
- https://www.mediawiki.org/wiki/Page_Previews [P]
- *Fit:* we already have verified quotes per `S01 p.10` tag. The hover card shows the verbatim quote, document title and page. A click opens a right-hand **Sources panel** scrolled to that quote, not a new page.

**4. One sources list per answer, numbered, expandable.** Cloudscape's GenAI chat pattern: number inline citations in ascending order, and list sources in an expandable "Sources" section with title and description [P]. ChatGPT search and Google AI Overviews both moved to inline links plus a right-hand source panel on desktop [S].
- https://cloudscape.design/patterns/genai/generative-AI-chat/ [P]
- https://ahrefs.com/blog/google-ai-overviews [S]
- *Fit:* split the panel into two groups, **AFS documents** (S01–S0x) and **Literature** (external, with URL). The judges need to see that supplied material comes first.

**5. Option cards with a "best for" line, and a small comparison table under them.** Wirecutter-style labels ("our pick / budget pick / upgrade pick") tell people why each option exists [S]. NN/g on comparison tables: at most 5 options; "options as columns, attributes as rows"; let users hide rows where every option is the same; "The biggest problem with most comparison tables isn't design, it's content" [P].
- https://www.nngroup.com/articles/comparison-tables/ [P]
- https://birchtree.me/blog/on-the-wirecutter/ [S]
- *Fit:* we have Simple / Recommended / Extended. Show three cards: name, one-line "best for…", cost class, and a confidence pill. Pre-select **Recommended**. The table (rows: cost class, ease, maintenance, performance fit, confidence) comes after the cards, with rows where all options are equal greyed out.

**6. A suitability colour, always paired with a word.** E+H Applicator marks recommended instruments green, restricted ones amber and unsuitable ones red [S, press description]. Pair each colour with a word ("fits", "with limits", "not suitable") so the meaning survives colour-blindness and print.
- https://www.endress.com/applicator [P, tool landing page]
- https://www.theengineer.co.uk/content/news/more-online-selection-help [S]
- *Fit:* the per-option "performance fit" and the method screen (NIR / Raman / UV-Vis / MIR) map directly onto it.

**7. Calibrated confidence words with a "why".** IPCC AR5 rates evidence ("limited", "medium", "robust") and agreement ("low", "medium", "high"), then gives a confidence level. Authors must give "a traceable account" of how they judged it [P]. NN/g warns that confident-sounding answers win "undeserved trust" [P].
- https://www.ipcc.ch/site/assets/uploads/2017/08/AR5_Uncertainty_Guidance_Note.pdf [P] (mirror: stat.berkeley.edu copy)
- https://www.nngroup.com/articles/explainable-ai/ [P]
- *Fit:* our confidence rating is computed by code (D-022). Show it as a word ("Medium") plus a one-line reason ("2 supplied sources agree; turbidity unknown") and an expandable list of the inputs it came from. Never show a bare percentage.

**8. A composer that stays pinned, with follow-up chips beside it.** NN/g found "half of all conversations contained a followup action". Prompt controls are "UI components that surround the input field" [P]. Cloudscape: "Keep the composer pinned … so the input is always reachable". A suggested prompt that needs editing should fill the input rather than send [P].
- https://www.nngroup.com/articles/prompt-controls-genai/ [P]
- https://cloudscape.design/patterns/genai/generative-AI-chat/ [P]
- *Fit:* this answers the user's "where do I ask questions?". Pin one input bar to the bottom with a placeholder like "Add a detail or ask about this answer…". The chips above it come from our open questions ("Is the whey turbid?", "Line temperature?").

**9. A "What would change this answer" panel, answered inline, then a re-assessment that shows what changed.** NN/g on staged disclosure: wizards work when steps "have little interaction" with each other. Keep tightly linked choices on one screen [P]. Siemens PIA and E+H Applicator both split *basic* and *advanced/extended* inputs and offer guided selection by application [P/S].
- https://www.pia-portal.automation.siemens.com/help.htm?lang=en [P]
- https://www.nngroup.com/articles/progressive-disclosure/ [P]
- *Fit:* the open questions become small form controls (segmented yes / no / unknown, a number field with a unit). The button reads "Re-assess with 3 answers". The new turn opens with our existing "Re-assessed with the customer's answers" diff, shown as "changed: recommended option Raman → NIR; confidence low → medium".

**10. A named-step progress indicator for the run of a few minutes.** NN/g, for waits over 10 s: show steps or percent done, say what is happening, give a slightly generous estimate, offer a way to stop, and avoid looped spinners [P].
- https://www.nngroup.com/articles/progress-indicators/ [P]
- https://htmx.org/extensions/sse/ [P] (server-sent HTML fragments per named event)
- *Fit:* our pipeline already has named stages (intake → screen → assess → verify → repair → external → finalize) and Ctrl-C cancel. Stream each stage as an htmx SSE fragment. **Dynamic showcase:** as each stage finishes, reveal its piece of the answer: the method screen after *screen*, the schematic after *assess*, citation ticks after *verify*. The wait becomes the demo.

**11. Linked highlighting between options, schematic, parameters and sources.** Brushing and linking means a selection in one view is highlighted in the others [S, Wikipedia; MyBrush, IEEE VIS 2018].
- https://en.wikipedia.org/wiki/Brushing_and_linking [S]
- https://openaccess.city.ac.uk/id/eprint/18383/1/2018_VIS_mybrush.pdf [P, paper]
- *Fit:* hover the "Extended" card and the extra parts light up in the schematic (e.g. a second probe or a multiplexer). Hover "fiber" in the schematic and the fiber rows in the parameter list and their source chips light up. This takes about 20 lines of JS using `data-part` attributes.

**12. The setup schematic as the hero picture, like a configurator.** Instrument configurators (E+H Applicator, Siemens PIA, Ocean Insight's modular packages) are built around *the configured measuring point*, not around prose [P/S].
- https://www.oceaninsight.com/the-power-of-modular/ [P]
- *Fit:* process point → probe → fiber → spectrometer → model → result is short and linear. Draw it large, label each part with the chosen item and its citation, and let the option toggle redraw it.

**Layout and type** (applies to every direction below):
- Spacing on an 8-pt scale: 4 / 8 / 16 / 24 / 32 / 48 / 64, as in IBM Carbon's tokens (https://carbondesignsystem.com/elements/spacing/overview/ [P]).
- Body text 16–18 px with line-height 1.5, a text measure of 60–75 characters, and tabular numerals for values.
- One accent colour, plus green/amber/red used only for suitability.
- Cards with a 1 px border and no heavy shadows. Dark-mode tokens are already in the plan.

---

## (b) Recommended interaction flow

1. **Start screen.** One large input ("Paste or type the customer enquiry"), 3 example chips under it, and a "Saved runs" list in a quiet sidebar or below. Nothing else.
2. **Running (1–5 min).** The enquiry is shown as the first "turn". Under it, a vertical stepper with named stages, elapsed time and a generous estimate ("usually 2–4 min"), plus a **Stop** button. Answer pieces fade in as stages finish (pattern 10). The composer stays visible but disabled ("You can add details when the first answer is ready").
3. **Answer (above the fold at 1440×900):**
   - The **verdict card**: method + probe, confidence word + reason, 2–3 citation chips.
   - The **setup schematic**, full width, drawn for the selected option.
   - **3 option cards** as a toggle; Recommended is pre-selected and redraws the schematic.
4. **Below the fold:**
   - **What we need to know**: the open questions as inline controls, with a "Re-assess" button.
   - **Parameters to measure**: a short table of what, how and why, each row with a chip.
   - **Risks** and **Feasibility test plan**: numbered steps, collapsed after 3.
   - **Expert detail**: one drawer.
5. **Sources.** Every chip opens a hover card with the verbatim quote. A click opens the right **Sources panel** (AFS documents first, then literature), scrolled to that quote.
6. **Follow-ups.**
   - The pinned bottom composer takes free text ("the line runs at 70 °C") or a question about the answer.
   - Answering open questions or adding facts starts a **re-assessment**. It appears as a new turn with a "What changed" strip at the top. Earlier turns collapse to their verdict line.
   - A pure question that needs no new run is out of scope today. Every input re-assesses, and the turn says so.
7. **Hand-off.** "Copy as customer reply" and "Print / PDF" on the verdict card. The print stylesheet expands every drawer.

---

## (c) Diagram approach

**Recommendation: server-rendered inline SVG built by a Jinja macro (no library), with Lucide icons inlined.**
- *Why it fits:*
  - The topology is a fixed left-to-right chain of 5–7 nodes, with optional extras: 2nd probe, multiplexer, flow cell or bypass, reference measurement. A hand-placed slot grid (x = 0, 160, 320…, snapped to 8 px) gives a cleaner engineering look than any auto-layout.
  - The output is deterministic and testable (snapshot test), prints crisply, and needs no JS.
  - It takes theme colours through `currentColor` and CSS variables.
  - `<title>`/`<desc>` per part keep it accessible.
  - Each node carries `data-part="probe"` for pattern 11.
- *Icons:*
  - **Lucide** (`lucide-static` **1.59.0**, **ISC**). It has `flask-conical`, `test-tube`, `cable`, `cpu`, `chart-spline`, `activity`, `cylinder`, `container`, `factory`, `gauge`, `scan-line`, `zap`, `rainbow` (all checked in the package's tags file today).
  - Alternatives: **Tabler** `@tabler/icons` **3.49.0**, MIT; **Phosphor** `@phosphor-icons/core` **2.1.1**, MIT; **Carbon icons** **11.90.0**, Apache-2.0.
  - For a spectrometer box or probe tip, draw simple custom shapes (rounded rect plus lens) in the same 1.5 px stroke style.
  - **Bioicons** (bioicons.com, 2,829 icons) has a "Lab apparatus" category, but licences are **per icon** (CC0 / CC BY / CC BY-SA / MIT / BSD). Use only CC0 or MIT ones, and record each one.
- *Keep Mermaid as the fallback*, for any non-linear graph the LLM produces. The UI vendors **mermaid 11.12.2** (MIT). Latest is **12.2.0** (2026-10-13). 12.0 made **ELK the default flowchart layout**, and flowcharts support icon/image node shapes (v11.3+, an icon pack must be registered) [P: https://mermaid.js.org/syntax/flowchart.html]. Do not upgrade during the hackathon: the gain is small and rendering could change.
- *Rejected, or kept for special cases:*

| Option | Version / licence | Verdict |
|---|---|---|
| elkjs (auto layout) | 0.12.0, **EPL-2.0 OR GPL-3.0-or-later** | Only if topology becomes variable. Layered + orthogonal routing "suitable for … circuit schematics" [P: eclipse.dev/elk]. Pairs with our SVG renderer (ELK gives coordinates, we draw). |
| D3 | 7.9.0, ISC | Overkill for a fixed chain. |
| React Flow / xyflow | @xyflow/react 12.12.0, MIT (Svelte 1.7.0) | An editable node canvas. Needs React or Svelte. Users don't need to edit the schematic. |
| Cytoscape.js | 3.34.4, MIT | Built for network graphs; looks unlike an engineering schematic. |
| rough.js (sketch look) | 4.6.6, MIT (last release 2023-11) | Only for Direction C's "whiteboard" style. It can redraw our own SVG paths roughly. |
| Excalidraw | 0.18.1, MIT, React editor | Too heavy; it is an editor. |
| Schematex (ISA-5.1 / P&ID symbols) | 1.1.2, **AGPL-3.0-only** | **Avoid** (copyleft). Use it only as a visual reference for symbol shapes. |

---

## (d) Three design directions to mock up

### A. "Answer + Ask" (thread, Perplexity-like). **Recommended**
- **Layout:** one centred column (~760 px) with a pinned composer at the bottom and a Sources panel that slides in from the right.
- **Each turn:**
  - The enquiry, shown as a quiet grey block.
  - The verdict card.
  - The schematic.
  - The option toggle (3 cards).
  - "What we need to know" as chips and inline controls.
  - Collapsed detail.
- **Re-assessments:** new turns below, each opening with "What changed". Earlier turns collapse to one line.
- **Screens:**
  - Start: a centred input and example chips.
  - Running: the turn with a live stepper and pieces fading in.
  - Answer: as above.
  - Sources: the right panel.
- **Pros:**
  - Answers "where do I ask?" at once.
  - Familiar from ChatGPT, Perplexity and NotebookLM.
  - Re-assess history reads naturally.
  - Simplest to build with htmx (append a turn).
- **Cons:**
  - Long threads scroll.
  - Looks like "another chatbot" unless the schematic and option cards carry the identity.
  - Free-text follow-ups always trigger a full run (minutes), so set expectations in the composer hint.

### B. "Setup Builder" (configurator workbench, E+H Applicator / Siemens PIA-like)
- **Layout:** three panes.
  - Left (280 px): the enquiry plus **facts and open questions as a form**. Stated facts are ticked; unknowns are fields.
  - Centre: a **large schematic** with the Simple / Recommended / Extended toggle above it, and the parameter table and test plan under it.
  - Right (drawer): evidence.
- **Re-assessment:** filling a left-pane field marks the answer "out of date"; the user clicks "Re-assess".
- **Screens:** a start form, a running overlay on the centre pane, the workbench, and a compare view (the 3 options side by side as mini-schematics).
- **Pros:**
  - Most "engineering tool"-like, and the schematic is the hero.
  - Linked highlighting shines here.
  - It is obvious what inputs drive the answer.
- **Cons:**
  - Denser. Needs a wide screen; on a laptop or projector it gets cramped.
  - A free-text "ask" has no natural home, so it needs a composer in the left pane.
  - More layout work.

### C. "Briefing" (guided story, one card per step)
- **Layout:** a horizontal stepper at the top: **1 Verdict · 2 Setup · 3 Options · 4 What we need · 5 Test plan · 6 Sources**. One large card fills the screen per step, with Next/Back and keyboard arrows. During the run, steps unlock one by one as stages finish (strong live-demo effect).
- **Optional style:** a light "whiteboard" look for the schematic (rough.js).
- **Asking:** a floating "Ask / add detail" button opens a bottom sheet.
- **Screens:** start; running (steps light up); each step card; a print view of all cards.
- **Pros:**
  - Calmest and easiest to understand.
  - Great for presenting to a jury or a customer.
  - Each screen has one job.
- **Cons:**
  - Hides the whole picture: an engineer can't scan everything at once.
  - Paging adds clicks.
  - Re-assessment history is awkward.
  - Sketch styling can look less credible to engineers.

**Recommendation: A, borrowing two things.**
- From B: the option toggle that redraws the schematic, and linked highlighting.
- From C: stage-by-stage reveal during the run.

Why A:
- It fixes both complaints directly: "too much like a report" (verdict card first, two disclosure levels) and "where do I ask" (pinned composer plus question chips).
- It is the smallest step from the current htmx page.

---

## Stack check (FastAPI + Jinja2 + htmx)
- **Fit:** the htmx essay rates hypermedia a good fit for text-heavy UIs with well-defined update regions. It notes it is "easier to embed SPA components *within* a larger hypermedia architecture, than vice-versa" [P: https://htmx.org/essays/when-to-use-hypermedia/]. All of A's interactions fit:
  - appending a turn (`hx-post` + `hx-swap="beforeend"`);
  - streaming stages (SSE extension `htmx-ext-sse` **2.2.4**);
  - opening the sources panel (`hx-get` into a panel);
  - the re-assess form (`hx-post`).
- **Small JS needed:** hover cards (CSS `:hover`/`:focus-within` plus a `<template>`), linked highlighting (`data-part` + `mouseenter`), and the option toggle (CSS radio-button hack or 10 lines of JS). Our `app.js` is 59 lines today.
- **Alpine.js 3.17.4 (MIT):** optional, for declarative toggles (`x-data`, `x-show`, `@mouseenter`). It is worth adding only if the hand-written JS grows past ~150 lines.
- **Versions:**
  - htmx: vendored **2.0.4**; latest stable **2.0.11** (0BSD, 2026-09-22). npm also has **4.0.0** under the `next` tag. Do **not** move to 4.x before the deadline.
  - **Preact 11 / Svelte 5:** not needed. They add a build step and duplicate templates for no user-visible gain.

---

## (e) Examples to look at (open these before choosing)
| What | URL | Look for |
|---|---|---|
| Perplexity | https://www.perplexity.ai | answer → sources → related questions; pinned follow-up box |
| NotebookLM | https://notebooklm.google.com (help: https://support.google.com/notebooklm/answer/16179559) | hover a citation → quote; click → source scrolls to the passage |
| Elicit | https://elicit.com | table cells → click → supporting quote; numbered claim citations |
| Consensus | https://consensus.app | "Consensus Meter" (Yes / Possibly / No) as a compact evidence summary; study snapshot cards [S: https://aarontay.substack.com/p/a-2025-deep-dive-of-consensus-promises] |
| scite | https://scite.ai | quotes labelled supporting / contrasting / mentioning (idea for "supports / limits" tags on our quotes) [S: https://guides.lib.purdue.edu/scite] |
| Google AI Overviews / ChatGPT search | google.com, chatgpt.com | inline link chips and a right-hand sources panel |
| Cloudscape GenAI chat pattern | https://cloudscape.design/patterns/genai/generative-AI-chat/ | pinned composer, support prompts, numbered citations, loading states |
| E+H Applicator | https://www.endress.com/applicator | basic vs extended inputs; green / amber / red suitability |
| Siemens PIA Life Cycle Portal | https://www.pia-portal.automation.siemens.com | guided selection by application; configuration → order number |
| Ocean Insight modular | https://www.oceaninsight.com/the-power-of-modular/ | spectrometer + fiber + probe as a pre-built "package" (= our options) |
| Mettler Toledo ReactIR sampling | https://www.mt.com/us/en/home/library/datasheets/automated-reactors/ReactIR-Sampling-Technology.html | probe-selection steps: chemistry → tip material → size → T/P |
| GOV.UK Design System | https://design-system.service.gov.uk/components/details/ , /components/summary-list/ | calm type, key–value summaries, disclosure rules |
| IBM Carbon spacing | https://carbondesignsystem.com/elements/spacing/overview/ | 8-pt spacing tokens |
| Wikipedia Page Previews | any en.wikipedia.org article (hover a link) | hover-card style for our citation chips |

**Gaps and uncertainty.**
- No official Perplexity or OpenAI design documentation was found. Their behaviour above comes from teardowns and press [S].
- The E+H colour coding comes from a press article, not the live tool.
- The IPCC PDF on ipcc.ch returned 403 to the fetcher, so it was read from the Berkeley mirror (same document, AR5, Nov 2010).
- No open-licensed P&ID icon set was found. Schematex is AGPL.
