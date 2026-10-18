# AFS Spectroscopy Assistant: slides (source text)

Source text of `slides.html` (kept in sync); `slides.pdf` is exported from `slides.html`. Every figure comes from a committed file, named in the slide footer (repeated here as "Sources"). Export, and the two placeholders for the team members' names and the repository URL: see `docs/slides/README.md`.

<!-- Re-export (from the repo root): "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html" -->

---

## 1. AFS Spectroscopy Assistant

Art Fiber Systems challenge · SchubKI National AI Hackathon 2026

*A customer enquiry goes in. A cited first technical assessment comes out.*

Team Helios
TEAM_MEMBERS_PENDING
REPO_URL_PENDING

---

## 2. The challenge: help an AFS expert answer a new customer

- A customer describes what they want to measure in their process. **Which method and probe should they test first?**
- The answer must rest on the **AFS documents**. Nothing invented: no prices, accuracy figures or fiber lengths.
- It should **ask the right questions** and **propose a first feasibility test**.

How it is judged (weight %, shown as bars):

| Criterion | Weight |
|---|---|
| Technical quality | 30 |
| Use of AFS knowledge | 20 |
| Feasibility-study plan | 15 |
| Clarification & uncertainty | 15 |
| Explainability | 10 |
| Prototype & presentation | 10 |

**The jury also asked:** Always make a proposal. Search the literature when the AFS documents don't cover it. Handle setups that combine several methods.

Sources: AFS challenge brief (organiser PDF): tasks, rules, criteria and weights · jury input: STATUS.md (12:22).

---

## 3. What we built: a chat assistant that writes the first assessment

Screenshot: `answer-recommendation.png`. Caption: "A live answer. Each numbered source on the right is the exact AFS quote with its page."

- **Recommendation:** what to test first, with a decision status and a confidence level.
- **Three options:** simple, recommended, extended. Cost class from AFS Table 1, never a price.
- **Setup sketch:** process, probe, fiber, spectrometer.
- **Questions for the customer:** the ones that could change the choice.
- **Chat:** ask a follow-up or add a fact: the answer updates.

Sources: screenshot is a crop of `docs/video/frames/09_recommendation.png` (live run in the web chat) · README.md "What it does".

---

## 4. How it works: models write, code checks

Six steps, left to right:

1. **Understand the enquiry** (model): picks out what the customer actually wrote, and what is missing.
2. **Screen the 5 methods** (code): UV-Vis, NIR, mid-IR, Raman, fluorescence, against 44 AFS rules and fiber limits.
3. **Write the assessment** (model): reads all 67 AFS pages. Every claim must quote its page.
4. **Check every claim** (code): 122 to 161 checks per answer: quotes, pages, numbers, wording.
5. **Fix what failed** (stronger model): gets the list of failures and rewrites. At most 2 rounds.
6. **Answer with sources** (code): anything still failing is removed or labelled.

Legend: language model · code (same input, same result).

- The literature is searched only for gaps the AFS documents leave open. Those quotes are shown apart and marked **secondary**, not AFS material.
- The same steps run for every enquiry. Nothing is written for a specific case.

Sources: ARCHITECTURE.md · `src/afs_assistant/pipeline.py` (max 2 repair rounds) · checks per case: `outputs/final/H0*.json` · `knowledge/rules.yaml`.

---

## 5. How it works: the AFS files become checkable knowledge

What AFS gave us:
- Lab report, slide deck, flyer: PDFs (S01, S02, S05); slide images typed in by hand.
- Two research papers: kidney tissue study (S03), mid-IR + fluorescence (S04).
- Guidance document: answer structure and method overview (REF).
- Table 1 spreadsheet: methods compared, with a cost rating.
- A laboratory web page, saved as text (S06).

What the code builds from them:
- **67 pages of text.** The model reads them. The checker compares every quote against them.
- **44 rules.** Each backed by a word-for-word AFS quote. Example: silica fibers stop near 2.4 µm, so they cannot carry mid-IR (fiber chart, S02 p.6).
- **19 Table 1 rows.** Method and probe type, with the cost class: low, average or high (S01 p.6).
- **7 fiber families.** The wavelength range each one carries (S02 p.6).

Same files in, same files out. A check confirms all 77 rule quotes are on their page.

Sources: `src/afs_assistant/kb_build.py` · `knowledge/rules.yaml`, `table1_methods.json`, `fibers.json` · kb check 13/13 PASS · ARCHITECTURE.md.

---

## 6. How it works: four checks on every claim

1. **The quote is on the page.** Word for word. A changed number or a dropped "not" fails.
2. **The page fits the claim.** A similar application elsewhere is not proof for this customer.
3. **Numbers have a source.** Only from the quote or the customer's own text.
4. **No promises.** No prices, no guarantees, no approval wording.

If a check fails: the failures go to the stronger fixer model, which rewrites. Still failing? The claim is removed, or labelled so the reader sees it.

**120/120** citations verified in the six held-out answers.

What the reader sees next to each claim:
- `AFS source`: backed by a checked AFS quote.
- `precedent only`: a similar published use: a reason to test, not proof.
- `engineering judgement, no source`: our reasoning, clearly marked as such.

Sources: `src/afs_assistant/verify.py`, `scope.py`, `chat.py` (labels) · `outputs/final/H0*.json` (120/120) · `outputs/final/REVIEW.md`.

---

## 7. How it works: a team of models (each job goes to the model that does it best)

| Role | Model | Job |
|---|---|---|
| Reader | Gemini 3.5 Flash-Lite | Understands the enquiry; writes literature searches. |
| Writer | GLM-5.3-Flash | Writes the first draft of the assessment. |
| Fixer | Gemini 3.8 Flash | Rewrites, only when checks fail. |
| Backup | every step | Retries on a different model if a reply breaks. |

In all six held-out cases the checks caught problems in the first draft, so each answer shown is the fixer's rewrite.

Why this mix: we tested 7 setups blind on 8 practice cases, scored by 4 judge agents.

| Setup | Quality /5 | Time |
|---|---|---|
| Best single model | 4.15 | 259 s |
| Our old setup | 4.08 | 504 s |
| **This mix** | **4.06** | **84 s** |

Quality on par, **3–6× faster**, about **$0.03** per case.

Sources: `config/models.yaml` · `outputs/bakeoff-dev/blind/summary.md` · README.md "Models".

---

## 8. Proof: the six held-out questions, answered by the agent

| | The customer asks | What was tricky | The agent's verdict |
|---|---|---|---|
| H01 | New powder blend: can we reuse our NIR calibration if we add Raman? | A calibration only fits the mixture it was built on. | **Premise not supported.** Rebuild the NIR calibration on the new blend; test Raman separately. |
| H02 | Clear whey and opaque milk concentrate: what should we test first? | Two very different streams. | **Provisional.** NIR: transmission/transflection for the whey, diffuse reflection for the concentrate. |
| H03 | Can our fluorescence spectrometer report glucose and viable biomass? | Glucose is not fluorescent; no marker named. | **Premise not supported.** Test Raman first, NIR as the comparison. |
| H04 | Reuse a silica cable for MIR ATR on a petroleum line? | Silica fibers cannot carry mid-IR light. | **Premise not supported.** Test MIR ATR, with a CIR or PIR fiber. |
| H05 | A liquid goes off-spec. Give us the exact sensor now. | Contaminant and quality variable unknown. | **Insufficient information.** Lab trial first: Raman and mid-IR ATR on normal and off-spec samples. |
| H06 | Does the kidney study prove our sensor is ready for live surgery? | It is an ex vivo proof of concept; no own data. | **Premise not supported.** Ex vivo NIR test on own tissue, with histopathology as reference. |

Run once on the frozen system; outputs not edited. An independent review found all six reach the right core verdict.

Sources: `outputs/final/H0*.json` (enquiries) · `outputs/final/brief/H0*.md` · `docs/review-final/A-brief-and-outputs.md` · `outputs/final/REVIEW.md`.

---

## 9. Proof: one answer up close (H04, short view, text unchanged)

Title: Reuse of a silica link for petroleum MIR ATR

> **Premise not supported:** the sources do not support the customer's premise as stated; the assessment below is provisional.
>
> The concept cannot be approved as stated: silica fibers cannot carry mid-IR light, so MIR ATR needs a CIR or PIR fiber instead of the existing cable. MIR ATR itself is worth testing first, with a published precedent for water in petroleum. Open items: the MIR link length to the other building, the sample state, and the required accuracy.
>
> **Proposed now:** the recommended option (basis: supplied AFS sources): MIR, ATR probe as primary candidate [S02 p.13; S01 p.9].

Clarification questions:
1. What is the actual link length and routing between the petroleum line and the analyzer building?
2. What is the physical state and condition of the petroleum at the measurement point (liquid, viscous, opaque, temperature, fouling)?
3. What water-content range, accuracy and response time does the investigation require?

Sources: excerpt of `outputs/final/brief/H04.md` (built by code from the saved run, no model call) · full answer: `outputs/final/H04.md`.

---

## 10. Results in numbers: the six held-out questions, run once

- **6/6** questions answered in full.
- **120/120** citations verified on the cited page.
- **0** blocking check failures left in any answer.
- **1.5–3 min** per question.
- **$0.29** for all six questions together.
- **1.4–6.3 s** per chat follow-up (10 tested).

890 automated tests pass, with no model calls.

Sources: `outputs/final/H0*.json` (timings 97–184 s, cost $0.288) · `docs/chat/live-check-20261018.json` · tests: `docs/slides/README.md`.

---

## 11. What we'd add next

- **Next: a short customer reply by default.** Full answers are about 3,000 words; the short view built by code is 560–698.
- **Next: a second checker: does the quote really support the sentence?** Today a quote is verified when it is on the right page.
- **Next: confidence that moves with what is known.** Today most options say "Low" (45 of 55 in our review).
- **Next: fewer questions when the enquiry is already complete.** A complete test enquiry still got 4–5 questions.
- **Next: faster runs.** The fixing step takes 46–72 % of each run.

Sources: `outputs/final/H0*.md`, `brief/` (word counts) · README.md "Known limitations" · `outputs/final/H0*.json` (timings).

---

## 12. Thank you

Team Helios
TEAM_MEMBERS_PENDING
REPO_URL_PENDING
Demo video: 2:53

Source: `docs/video/demo.mp4` (173 s).
