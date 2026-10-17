# Skill: combining spectroscopy methods (multi-method options and data fusion)

Guidance in our own words. Never quote this text. To cite a point, quote the source passage given in brackets (verbatim from that page) or another passage from the SOURCE PAGES. A point marked *(general practice)* has no supplied source: write it as engineering judgement with no citation.

## When to combine
- **Single method first.** Recommend the single best method when it can cover the stated targets. Combine methods only when one method cannot cover a stated target or a stated interference. The combined option is the `extended` tier, never the `recommended` tier by default.
- **Complementarity per target.** Say which method sees which target and why: fundamental vs overtone bands, water interference, fluorescence background, chromophores, morphology or depth. A second method must add information on a named target or interference.
  - Combining can help where one method is not enough: S01 p.7 ["The analysis of such systems may require a combination of two or even more spectral methods."]. Any gain from combining is a hypothesis to test (claim_kind `method_gain`).
  - Mid-IR and Raman complement each other: S01 p.11 ["This property makes mid-IR and Raman spectra complementary, that is, they complement each other."]; also S01 p.5.
  - Fluorescence can be combined with mid-IR or NIR: S01 p.12 ["Fluorescence spectroscopy can be used for multispectral measurements, for example, in combination with Mid-IR or NIR spectroscopy."].
  - The published combinations on S01 p.7, p.14 and p.15 are examples (precedent), not proof for a new process.

## What a combined option must state (`fusion_note`)
1. **Same spot, same volume.** The probes must look at the same material. Different techniques sample different depths or volumes (ATR a few micrometres, transmission a path length, Raman a focal volume). In heterogeneous or flowing material a mismatch makes the fusion meaningless.
   - S01 p.8 ["It is crucial that the spectral information obtained by different methods-Mid-IR, NIR, Raman, and fluorescence spectra-is collected from the same small, even pinpoint, area of the sample."]
   - A combined probe helps: S01 p.8 ["The use of a combined probe facilitates measurements and allows for the analysis of a smaller sample volume."]
2. **Synchronisation.** Methods acquire at different rates; data must be aligned to a common time step, and the dead time between ports accounted for.
   - S01 p.8 ["two or more probes, belonging to different methods, can be used for measurements, but the data from each method must be obtained simultaneously."]
   - S01 p.8 ["Ultimately, the measurement data must be normalized to a common time step."]
3. **Fusion level.** Start from one model per method (the baseline). Then fuse:
   - joined spectra or variables with block scaling, so that one method does not dominate: S01 p.8 ["Variables obtained from different spectral methods are not equivalent."], S01 p.8 ["If the variables have different units of measurement, the data should be normalized in some way, for example, using an autoscaling algorithm."], S01 p.9 ["Furthermore, methods containing a larger number of variables have a greater impact on the model."];
   - extracted features or scores per method, then joined *(general practice)*; watch overfitting with few reference samples;
   - one model per method with the results combined *(general practice)*, when the instruments are run and maintained separately.
4. **Calibration and maintenance per block.** Each instrument needs its own calibration and its own diagnostics; a fused model breaks when any block drifts or a probe is changed. Two instruments also mean more hardware to run: S01 p.9 ["One of the challenges of multispectral analysis is the need to simultaneously connect at least two independently operating measuring instruments."].
5. **Must beat the best single method.** Validate on independent batches or runs with the reference method, and show that the fused model is better than the best single method. Otherwise drop the extra instrument *(general practice)*.
6. **Hardware and fibers.** One probe and fiber per method, or a combined probe. Fiber families, length limits and multiplexing per method come only from the supplied sources. Never state a link length, product code or price.

## How it shows in the assessment
- `solution_options`: `simple` (one method, least effort), `recommended` (the best fit for the stated targets and constraints: not the cheapest, not the strongest), `extended` (two or more methods with a `fusion_note`). Two options are enough when no combination makes sense; then leave out `extended`.
- The extended option references recommendations whose methods are all worth testing; a combination stays a later hypothesis after the single-method tests (feasibility plan: single methods first).
