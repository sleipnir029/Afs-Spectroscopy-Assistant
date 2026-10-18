# Submission text: AFS Spectroscopy Assistant (Team Helios)

**Short description (1–2 sentences)**
A chat assistant that turns an in-line spectroscopy customer enquiry into a cited first technical assessment for Art Fiber Systems. You can ask follow-up questions and add facts; the answer updates with live recommendation, options, setup-diagram and table blocks, and every quote is checked word for word against its page in the supplied AFS documents.

**What it does**
- **Methods:** recommends a spectroscopy method and probe technique to start with, plus 2–3 options (simple / recommended / extended). Each option has a relative cost class from S01 Table 1 (never a price), ease of use, upkeep and a setup sketch.
- **Citations:** cites the supplied AFS material (`S01 p.18`) for its key claims. Code checks every quote verbatim on the cited page and checks the page scope; failing citations are removed or flagged. "Verified" means the quote is on the page, not that it fully supports the claim (no entailment check yet).
- **Honesty:** asks clarification questions tied to the option they would change and gives an honest decision status. It always proposes a next step, also when the sources do not cover the question.
- **Literature:** when the supplied sources leave a gap, it searches keyless scholarly APIs. External quotes are verified, cached and replayable, and are always marked secondary.
- **Chat:** follow-up questions get grounded answers in 1.4–6.3 s per question in a 10-question live check (about $0.004 each); new facts trigger a re-assessment with a "What changed" block.

**Key numbers (from the committed outputs)**
- **H01–H06**, run once on the frozen pipeline (tag `freeze-1`), with nothing edited:
  - 0 hard verification failures and 120/120 citations verified;
  - 97–184 s per case, $0.288 in total;
  - external replay 13/13 equal;
  - cost class 6/6 in agreement with S01 Table 1.
- **Development and adversarial sets (19 cases):**
  - 0 hard failures, 0 runaway replies and 0 checklist failures;
  - about 105 s per case on average.
- **Model choice:** a blind bake-off of 7 configurations on D01–D08, judged by four blind LLM judge agents against the AFS evaluation data. The production setup ("mix-a": per-role models, a stronger model repairing only the failed checks, cross-model retry) is about 6× faster than the previous single-model setup (84 vs 504 s per case on D01–D08) at similar blind-judged quality (4.06 vs 4.08 of 5), for about $0.03 per case.

**Known limits:** answers are long (about 3,000+ words vs 300–400 in AFS's worked answers); "verified" means the quote is on the cited page, not that it entails the claim; a re-assessment can change the method without a clear reason (README "Known limitations").

**Deliverables (paths in the repository)**
- `README.md`: setup with uv, commands, results and known limitations.
- `ARCHITECTURE.md`: components, data flow and diagram.
- `docs/slides/slides.pdf`: 10 slides.
- `docs/video/demo.mp4`: 2:25 demo: captioned screenshots of the real app during a live run.
- `outputs/final/H01–H06` (`.md` + `.json`) and `outputs/final/REVIEW.md`: the rule-compliance review.

**Repository link:** _to add once the repository is published_.
