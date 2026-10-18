# H01–H06 rule-compliance review (Phase 6 step 2; reviewer agent, 2026-10-18 ~12:40)

**Verdict: PASS WITH CAVEATS.** No blocking rule violation. The outputs stay exactly as generated (no edits, no re-run).

| Case | Result | Status | Citations verified |
|---|---|---|---|
| H01 | PASS WITH NOTES | premise_not_supported (REF §5: calibrations are matrix-specific) | 14/14 |
| H02 | PASS WITH NOTES | provisional_assessment | 16/16 |
| H03 | PASS WITH NOTES | premise_not_supported (no fluorescent target; S01 p.5) | 21/21 |
| H04 | PASS | premise_not_supported (silica ends at 2400 nm, S02 p.6; MIR range S01 p.9) | 25/25 |
| H05 | PASS WITH NOTES | insufficient_information | 22/22 |
| H06 | PASS WITH NOTES | premise_not_supported (S03 p.14 proof of concept; S03 p.3 ex vivo) | 22/22 |

**Checked across all six:**
- Every verification passed, with 0 hard failures.
- External items appear only in the secondary section, each with quote, URL and date.
- Cost is given only as a Table 1 class; no prices.
- No invented accuracy, detection limit, response time or fiber length. Every number traces to a source page.
- Every case has a proposal, a change trigger, a next step, and 4–5 questions.
- None of the four premise_not_supported cases looks over-triggered.

**Known limitations (generic patterns; recorded, not fixed):**
- Short table cells (performance fit, future direction) are not screened for overclaiming (H03, H05).
- A page reference typed inline in prose skips verification (H05 "S02 p.20"; the page does support the claim).
- "Verified" means the quote is on the page and in scope, not that it supports the claim (H01 [7], H03 [8], H04 [19], H06 [3]).
- An external item can be tagged to the wrong option, or be only weakly relevant (H03, H06).
- A cited quote can carry the source's own certainty wording (H02 [5]).
- No cross-field consistency check (H06: contact vs non-contact; superficial vs deeper).
- The setup sketch's NIR fiber label lists every family that overlaps the range (H01, H02, H06).
- Lab reference methods (Kjeldahl, Karl Fischer, …) are engineering judgement, marked "e.g." and flagged as unsourced.
