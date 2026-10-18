# AFS Spectroscopy Assistant: slides (source text)

Outline; the final slide text is in `slides.html` / `slides.pdf`. Every figure comes from a committed file, named on the slide.

---

## 1. AFS Spectroscopy Assistant

From a customer enquiry to a cited first technical assessment. Team Helios · AI hackathon, October 2026.

---

## 2. The problem

- AFS gets enquiries like "we want to follow X in our process; which method and probe should we test first?"
- A good first answer:
  - screens the methods (UV-Vis, NIR, MIR, Raman, fluorescence) against sample, probe and fiber limits;
  - proposes one option to test first;
  - says what is still unknown and what would change the choice.
- It must be grounded in the AFS materials. It must never invent accuracy, detection limits, response times, fiber lengths or prices, and never promise approval.
- Judging criteria: technical quality 30, AFS grounding 20, feasibility plan 15, clarification and uncertainty 15, explainability 10, prototype 10.

---

## 3. What it does

Screenshot: `docs/ui/brief-answer-1440.png`.
- A recommendation headline built by code from the proposed option.
- Status, confidence and next step.
- Margin notes with the verified quotes.
- A composer for follow-ups and re-assessment.

---

## 4. How it stays grounded

The pipeline:
- intake (LLM) → screening (code: 44 rules + S01 Table 1 + fibers) → assess (LLM, strict JSON);
- → verify (code, about 40 checks) → repair (stronger model) → finalize (code);
- → literature for gaps only → render + provenance commit.

The checks:
- every quote must be verbatim on the cited page (exact or loose; a fuzzy match is not verified);
- the page must be in scope for the claim kind;
- numbers must come only from the claim's own quotes or the enquiry;
- no prices, no guarantee or approval wording;
- cost class comes from S01 Table 1, and confidence is computed by code.

The numbers:
- H01–H06: 120/120 citations verified, 0 hard failures (`outputs/final`).
- The 19-case gate run: citations verified 100 % in every case, external replay 19/19 (STATUS.md 11:52).

---

## 5. Chat with live result blocks

Screenshots: crops of `docs/ui/brief-thread-full-1440.png` (options table, setup diagram).
- Routing is code: the first message assesses, new facts re-assess ("What changed"), any other text asks.
- An ask is one model call. Every claim is checked like the pipeline: quote on page, page scope, claim-local numbers, wording. A claim that fails is removed.
- The server renders the blocks from the verified run. The model picks blocks by name and never writes HTML.
- Live check (`docs/chat/live-check-20261018.json`): 10 questions, 1.4–6.3 s each, $0.038 in total, 10/11 citations verified (1 dropped by the checks), 0 claims removed.

---

## 6. Multi-method and literature

- Single method first. Combine only when one method cannot cover a target or an interference (S01 p.7). Mid-IR and Raman are complementary (S01 p.11).
- The extended option must carry a fusion note: same spot and volume (S01 p.8), data aligned to a common time step (S01 p.8), and the fusion level.
- Literature runs only for gaps the AFS sources leave open:
  - a curated open-access library (9 entries), then Europe PMC, OpenAlex and Unpaywall, with no keys;
  - queries are guarded, so no names or numbers from the enquiry are sent;
  - quotes are verbatim (at most 400 characters), shown as secondary, cached and replayable.
- H01–H06: 6 verified items, 1 dropped, external step 4–7 s and at most $0.0014 per case (`outputs/final/*.json`).

---

## 7. Model choice: evidence

D01–D08 × 7 arms, four blind judge agents (LLM) scoring against the AFS eval data (`outputs/bakeoff-dev/blind/summary.md`, `afs-score.md`).

| Arm | Quality (1–5) | s/case | $/case | Source recall |
|---|---|---|---|---|
| deepseek-v4.1-flash-1017 | 4.15 | 259 | 0.013 | 78 % |
| baseline v4.1-flash | 4.08 | 504 | 0.022 | 82 % |
| **mix-a (chosen)** | **4.06** | **84** | **0.030** | **85 %** |
| glm-5.3-flash | 3.96 | 322 | 0.006 | 85 % |
| gemini-3.8-flash | 3.75 | 173 | 0.059 | 82 % |
| mix-b | 3.38 | 69 | 0.030 | 75 % |
| gemini-3.5-flash-lite | 3.23 | 29 | 0.015 | 65 % |

How mix-a is built:
- Gemini 3.5 Flash-Lite does intake and literature.
- GLM-5.3-Flash writes the assessment.
- Gemini 3.8 Flash repairs, and only when the checks fail.
- Every role retries a failed reply on another model.

---

## 8. Results on H01–H06 (run once, tag freeze-1)

- 6/6 complete, 0 hard failures, 0 runaways or timeouts.
- 120/120 citations verified.
- 97–184 s per case, $0.288 in total.
- External replay 13/13 equal. Cost class matched S01 Table 1 in 6/6 cases.
- Status: premise_not_supported ×4, provisional ×1, insufficient_information ×1.
- Rule-compliance review: PASS WITH CAVEATS, no blocking violation (`outputs/final/REVIEW.md`).
- Dev + adversarial eval: checklist 0 failures; must 33/34, must-not 12/13 (`outputs/eval/summary.md`).

---

## 9. Limitations (honest)

- Answers are long: 3,058–3,455 words per H output vs 303–400 words in the AFS worked answers.
- "Verified" means the quote is on the page and in scope, not that it supports the claim. No entailment check yet.
- Short table cells and page references typed inline are not checked. There is no check across fields.
- A literature item can be tagged to the wrong option or be only weakly relevant.
- A complete enquiry can still get 4–5 questions (A07).
- Confidence rarely varies: 45 of 55 options were Low in the G5 review.
- A full assessment takes about 1.5–3 minutes. The flex tier can queue.

---

## 10. Team Helios · next steps

- An entailment critic: does the quote support the claim?
- A shorter customer reply that matches AFS's worked answers.
- Checks on table cells, on inline page references and across fields.
- Better confidence calibration and fewer questions on complete enquiries.
- Run it: `uv sync` → `uv run afs-assist ui`. README.md and ARCHITECTURE.md have the details.
