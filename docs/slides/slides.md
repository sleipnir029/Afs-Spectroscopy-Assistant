# AFS Spectroscopy Assistant: slides (source text)

Source text of `slides.html` (kept in sync); `slides.pdf` is exported from `slides.html` (command and placeholder in `docs/slides/README.md`). Screenshots in `img/app-*.png` are crops of the real app showing evaluation case H04 (`outputs/final/H04.json`, unedited), taken 2026-10-18. Deck simplified on user request (D-068 follow-up): one picture or diagram per slide, little text, no judging criteria.

---

## 1. AFS Spectroscopy Assistant

A customer enquiry goes in. A cited first technical assessment comes out.
Team Helios: Rakibuzzaman Rahat, Md Mahmud Siddique · REPO_URL_PENDING

---

## 2. What we built: Ask in plain words. Get a cited answer.

- Recommends the method and probe to test first.
- Every key claim cites the AFS page it comes from.
- Asks only the questions that would change the advice.
- Follow-ups in seconds; new facts update the answer.

Screenshot: `img/app-recommendation.png` (question + recommendation, H04).

---

## 3. System architecture: Models write. Code checks.

Read the enquiry (model: Gemini 3.5 Flash-Lite) → Screen 5 methods (code) → Write the answer (model: GLM-5.3-Flash) → Check every quote (code) → Fix what failed (model: Gemini 3.8 Flash) → Answer with sources (code).

Three models, each on its own job. In a blind test of 7 setups, this mix was 3–6× faster at close to the best quality, about $0.03 per case. (config/models.yaml, outputs/bakeoff-dev/blind/summary.md)

---

## 4. Use of AFS materials: Built on the AFS documents

- 67 AFS pages the model reads.
- 44 rules from the AFS documents, each tied to a quote.
- 120/120 quotes found word for word on the cited page, in the six evaluation cases.

Code checks every quote against its page. Anything unsupported is removed or labelled.

---

## 5. Example recommendation (H04, unedited): "Can we reuse our silica cable for mid-IR?"

The agent's answer: not as asked: silica fibers cannot carry mid-IR light. Test MIR ATR with a CIR or PIR fiber.
Screenshot: `img/app-setup.png` (setup sketch of the recommended option).

---

## 6. Example feasibility-study plan (same case, unedited): It asks, then plans the first test

Screenshots: `img/app-questions.png` (3 questions for the customer) and `img/app-feasibility.png` (5-step first feasibility test, reference measurements, decision basis).

---

## 7. Results: Six evaluation cases, answered by the agent

| Customer asks | Agent's verdict |
|---|---|
| Reuse an NIR calibration on a new blend? | Not supported. Rebuild the calibration. |
| A clear and an opaque dairy stream? | Provisional. A different NIR probe for each. |
| Fluorescence for glucose? | Not supported. Test Raman first. |
| Silica cable for mid-IR? | Not supported. Use a CIR or PIR fiber. |
| Unknown contaminant, sensor now? | Not enough information. Lab trial first. |
| A kidney study as proof for surgery? | Not supported. Test on own tissue first. |

120/120 quotes verified · 1.5–3 min per case · $0.29 for all six. (outputs/final/H01–H06, run once, not edited)

---

## 8. Limitations and next steps

- Full answers are long (~3,000 words) → a short customer reply.
- A quote on the page is not yet proof → a second checker for support.
- Confidence is mostly "Low" → confidence that tracks the facts.
- A run takes 1.5–3 minutes → a faster fixing step.

Demo video (3:27): docs/video/demo.mp4 · Team Helios
