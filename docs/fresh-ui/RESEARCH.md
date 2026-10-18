# Fresh UI research: AFS Spectroscopy Assistant

Date: 2026-10-18. Scope: how strong products present AI answers with evidence, how engineering tools present a technical setup, how briefings are typeset, and how long runs report progress. Earlier mockups in this repo were deliberately not consulted.

Where a source was only reachable through secondary write-ups, that is said next to it.

## Sources

| # | Source | URL | What it shows |
|---|---|---|---|
| 1 | NN/g, *Explainable AI in chat interfaces* (summary read via a mirror) | https://www.nngroup.com/articles/explainable-ai/ | Explanation text in AI chat is often "inaccurate, hidden, or confusing". Explanations must be visible, specific and checkable. |
| 2 | Ding et al., *Citations and Trust in LLM Generated Responses* (arXiv 2501.01303) | https://arxiv.org/pdf/2501.01303 | Citations raise trust a lot, even when nobody checks them. So a citation has to *be* checkable, or it just creates false confidence. |
| 3 | He et al., *Conversational XAI and overreliance* (arXiv 2501.17546) | https://arxiv.org/html/2501.17546v1 | Conversational explanation increased understanding *and* overreliance compared with a dashboard. The UI should show what is unknown, not only what is known. |
| 4 | NotebookLM inline citations (secondary guides: FreeAcademy, XDA) | https://freeacademy.ai/es/lessons/notebooklm-grounded-qa-citations | Numbered inline markers. Hover previews the quoted passage, click jumps to it in the source. Grounding is visible next to the claim. |
| 5 | Elicit release notes on supporting quotes (Elicit emails) | https://email.elicit.com/deliveries/dgTd9ggDAKHze6DzewGQLYz99hAnIjqTlaRVpeE= | Numbers after *parts* of an answer, each opening the supporting quote for that claim, with the most relevant quote first. Citations are claim-level, not answer-level. |
| 6 | Consensus Meter (Aaron Tay's 2025 review) | https://aarontay.substack.com/p/a-2025-deep-dive-of-consensus-promises | A one-glance verdict bar is powerful but turns into vote counting when it hides how strong each basis is. Any status chip needs its reason next to it. |
| 7 | scite, *Smart Citations* (Nicholson et al., QSS 2021) | https://direct.mit.edu/qss/article/2/3/882/102990/scite-A-smart-citation-index-that-displays-the | Shows the *citation statement in context* and its role (supporting or contrasting), not just a link. Our equivalent: verbatim quote plus "exact match" status, and premise checks marked supported or not covered. |
| 8 | Google PAIR, *People + AI Guidebook: Explainability + Trust* | https://pair.withgoogle.com/chapter/explainability-trust/ | Calibrate trust. Explain the basis and the limits, and let confidence displays describe the *data basis*, not a fake probability. |
| 9 | Microsoft HAX, *Guidelines for Human-AI Interaction* | https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/ | G1/G2 (make clear what the system can do and how well), G9 (support efficient correction), G11 (make clear why the system did what it did). These map to the status, confidence reasons and the answer-the-questions loop. |
| 10 | NN/g, *Progressive Disclosure* | https://www.nngroup.com/articles/progressive-disclosure/ | Put the few things most people need up front and the rest one step away. Here that means the verdict, the options and the questions first, with rules, checks and fusion details on demand. |
| 11 | NN/g, *Response Times: 3 Important Limits* and *Progress Indicators* | https://www.nngroup.com/articles/response-times-3-important-limits/ · https://www.nngroup.com/articles/progress-indicators/ | Past 10 s, users need a progress indicator that shows how far along it is and lets them do something else. A 13-minute run needs named stages, elapsed time and partial results, not a spinner. |
| 12 | Tufte CSS (sidenotes and margin notes) | https://edwardtufte.github.io/tufte-css/ | Evidence in the margin, next to the sentence it supports, so the eye doesn't leave the text. This is the model for verifying a claim without opening anything. |
| 13 | Butterick, *Practical Typography*: line length, body text | https://practicaltypography.com/line-length.html | 45 to 90 characters per line. Body text decides the quality of the page, so one good text face is better than many weights. |
| 14 | ANSI/ISA-5.1 instrument identification (secondary summary) | https://industrialmonitordirect.com/ru/blogs/knowledgebase/plc-and-dcs-tag-naming-conventions-isa-51-structure-and-examples | P&ID tag letters (A = analysis, AE/AT = analyzer element or transmitter, T = temperature) drawn in a circle. Process engineers read setups in this visual language. Revision clouds and title blocks are standard drawing conventions too (general drafting knowledge, not checked against the standard). |
| 15 | W3C, *WCAG 2.2* | https://www.w3.org/TR/WCAG22/ | 1.4.3 text contrast 4.5:1, 1.4.11 non-text 3:1, 2.4.11 focus not obscured, 2.5.8 target size 24×24. |
| 16 | Vercel AI SDK, *Generative User Interfaces* | https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces | The model calls a tool and the UI renders that tool's result as a component inside the message stream. Our equivalent: the server returns typed blocks (recommendation, options, sketch, parameters, questions, diff) and htmx swaps in a server-rendered partial for each one. No client framework is needed. |
| 17 | OpenAI, *Introducing canvas* | https://openai.com/index/introducing-canvas/ | A side panel for the work object, with the chat beside it. You edit and re-ask without losing the conversation. This is the model for concept 2's live drawing sheet. |
| 18 | Anthropic, *What are artifacts* (help centre) | https://support.anthropic.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them | Substantial standalone content opens in a dedicated window next to the chat and keeps versions you can switch between. This is the model for pinning and expanding blocks and for v1/v2 versioning. |
| 19 | Perplexity, *How does Perplexity work* | https://www.perplexity.ai/hub/faq/how-does-perplexity-work | Sources come first, numbered inline citations follow, and suggested follow-up questions sit under the answer. This is the model for concept 3's source chips and follow-up chips. |

Sources 16–19 were added after the brief changed to chat-first. Their URLs come from prior knowledge and were not re-fetched in this session; check them before citing externally.

## Principles for this product

1. **Verdict first, reason attached.** In 5 seconds a jury member must read: *what to start with*, *how sure*, *what is missing*. Status and confidence always come with the reason ("Medium: open question Q1, Q2"), never as a bare badge (sources 6, 8).
2. **Claim-level evidence, verifiable in place.** Every important claim carries a marker that shows the verbatim quote and its page *in place* (margin, inline expand or evidence pane), plus the code check result ("exact match"). Opening another window is a second level, not the first (4, 5, 7, 12).
3. **Show the unknowns as first-class objects.** Overreliance is the main risk (2, 3). Clarification questions, premise checks and "no verified source: engineering judgement" must look different from cited claims, and stay visible.
4. **Internal vs. external evidence must look different.** AFS documents are primary. External literature is labelled "secondary, not AFS material", with quote and URL, set in a quieter style.
5. **Long runs report named stages with real elapsed time, plus partial results.** The stages are intake, screening against rules, writing the assessment, verifying quotes and external search. Show what is done and let people read what's ready (11).
6. **The setup sketch speaks the engineer's language.** Probe → fiber → spectrometer → model → result, with auxiliary sensors on dotted signal lines. ISA-style tag bubbles make it readable to process engineers at a glance (14).
7. **Correction loop = the questions.** Answering Q1–Q5 *is* the way to correct the assessment (9: G9). Each question says what it affects, so the user knows why to answer it. A re-run must show what changed.
8. **Reuse is a job.** Engineers paste text into customer replies. Every section needs a clean copy path, and a "customer reply" composer should start from the brief answer and the questions.
9. **Projector legibility.** Body text ≥ 17 px, verdict ≥ 32 px, contrast ≥ 7:1 for body where possible, no information carried by colour alone (15).
10. **Typography carries hierarchy, not boxes.** Avoid card-in-card. One containment layer, hairline rules and a real text face (13).
11. **Chat-first, block-rich.** The assessment is not one static report. Each assistant turn is a short grounded answer plus only the blocks that turn needs, rendered inline (16). Long-lived blocks (current recommendation, setup, options) can be pinned or expanded into a side panel and are versioned per turn (17, 18).
12. **Follow-ups are offered, not just allowed.** Open customer questions appear as reply chips that say what they affect. Common follow-ups ("Compare the options", "Show the setup", "Why not X?") are chips too (19), so a jury sees what to ask next.
13. **New facts create a version, and the version leads with “what changed”.** Status, confidence, closed and opened questions, and option changes are shown as a diff before anything else (9: G9, G11).
