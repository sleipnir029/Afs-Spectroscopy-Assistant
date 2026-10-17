# First technical assessment: A clear whey stream before concentration

**Customer enquiry**

> Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the reference. The stream can become more turbid under some operating conditions. We need a first measurement concept that handles this change rather than assuming the liquid always remains clear.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified from dairy precedents and fiber-probe method descriptions, but it rests on assumptions about protein level, turbidity behaviour and the reference method. The recommendation is therefore provisional, not an approved or ready configuration.

## Premise check

- **Not covered:** The whey stream is relatively clear before concentration and becomes more turbid only under some operating conditions. The sources describe dairy milk streams and mention whey as an example of a transparent liquid, but they give no whey-specific clarity, turbidity or process-variation data. This remains customer process knowledge. *(no verified source: engineering judgement)*
- **Not covered:** A single measurement concept can cover both the clear and the more turbid states. The closest source statement is a dairy example in which a transflection probe 'in some cases' works for low-fat and high-fat milk products. That is a hypothesis to test for whey, not a rule. No source establishes one concept for both whey states. *(no verified source: engineering judgement)*
- **Not covered:** Laboratory results are a suitable independent reference for protein concentration. The sources require independent reference measurements for a feasibility plan, but they do not cover the customer's specific laboratory method or its uncertainty. *(no verified source: engineering judgement)*

## Requirements

**Stated by the customer**

- Track protein concentration in a dairy whey stream before a concentration stage.
- Use laboratory results as the reference.
- Provide a first measurement concept that handles a possible increase in turbidity rather than assuming the liquid always remains clear.

**Key unknowns**

- Protein concentration range and required accuracy and response time.
- Turbidity range, frequency and whether turbidity correlates with protein or is an independent disturbance.
- Reference laboratory method for protein and its uncertainty.
- Other varying components (fat, lactose, minerals) and possible interferences.
- Line conditions (temperature, pressure, flow, cleaning-in-place) and available installation port and distance from the analyzer.
- Presence of a suitable fluorophore or fluorescent indicator if fluorescence is considered.

## Clarification questions (most decision-relevant first)

Q1. What is the expected protein concentration range, and what accuracy and response time are required? *Why it matters:* Needed to judge whether NIR or MIR sensitivity is sufficient and to set the go/no-go criteria. *(affects: method, technique, status)*
Q2. What is the turbidity range (for example in NTU or optical density), how often does the stream become turbid, and is turbidity correlated with protein or an independent disturbance? *Why it matters:* Determines whether a single geometry can cover both states or whether a combination is needed. *(affects: method, technique, installation)*
Q3. What is the reference laboratory method for protein and its uncertainty? *Why it matters:* An independent reference is required for calibration and validation. *(affects: method, status)*
Q4. What are the line conditions (temperature, pressure, flow, cleaning-in-place) and the available installation port and distance from the analyzer? *Why it matters:* Affects probe and fiber selection and whether remote measurement is possible. *(affects: technique, installation)*
Q5. If fluorescence is considered, which fluorescent species or indicator is relevant (for example riboflavin or tryptophan)? *Why it matters:* Fluorescence only works for a defined fluorescent species; otherwise it is not a direct protein measurement. *(affects: method, status)*

## Recommendation

- **R1 · Primary candidate: NIR, transmission transflection.** NIR is the most common online fiber-probe method and the dairy PAT workhorse. Transmission is preferred for transparent or semi-transparent liquids such as whey. A transflection probe can in some dairy cases cover both low-fat and high-fat products, which is the closest source statement for handling a turbidity change; treat this as a hypothesis to test. *Conditions:* Applies if protein is a major (not trace) component and the stream is mostly transparent. The transflection variant should be tested for the turbid periods. Optical pathlength must be controlled. [1: S01 p.10] [2: S01 p.18] [3: S01 p.17] [4: S01 p.18] [5: S01 p.10] [6: S01 p.18]
- **R2 · Comparison candidate: MIR, ATR.** MIR gives direct protein amide I and II bands. ATR suits liquids and soft solids in contact and is a standard in-line route. It samples only a thin surface layer, so it is complementary to bulk NIR. *Conditions:* ATR requires tight contact; risk of fouling on the crystal. Water absorbs strongly in MIR, so the ATR evanescent layer is thin. Confirm fiber and crystal coverage for the required range. [7: S04 p.3] [8: S04 p.4] [9: S01 p.5] [10: S01 p.10] [11: S01 p.13]
- **R3 · Comparison candidate: Raman, raman probe.** Raman is well suited to aqueous media and provides complementary molecular information. It could serve as a comparison for protein backbone signals. *Conditions:* Only if the fluorescence background from the whey (for example riboflavin) is manageable. Verify on real samples before relying on it. [12: S01 p.16] [13: S01 p.11] [14: S01 p.11]
- **R4 · Not recommended: NIR, diffuse reflection.** Fails deterministic screening for a clear liquid sample. Reflection is less representative for clear liquids and sensitive to surface characteristics and particle size. If turbidity dominates the stream this may need revisiting, but it is not suitable as the primary concept for the clear baseline. *Conditions:* Not for the clear baseline. Revisit only if the stream becomes predominantly turbid. [15: S01 p.18] [16: S01 p.17]

## Measurement concept

- **Probe and geometry:** In-line NIR transmission or transflection probe across the whey line; MIR ATR probe in contact with the liquid as a comparison; Raman probe only if the fluorescence background is acceptable.
- **Location:** Before the concentration stage, in the process line.
- **Fiber link:** NIR: standard or Al/Cu-coated VIS-NIR silica fibers, whose transmission range is given on the cited figure page. MIR: chalcogenide (CIR) or polycrystalline (PIR) fibers. The achievable MIR fiber length for this installation is not stated in the sources; confirm with AFS. [17: S02 p.6] [18: S02 p.6] [19: S02 p.6] [20: S01 p.15]

## Spectral range

- **NIR:** Nominal range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [21: S01 p.10] [22: REF §5]
- **MIR:** Nominal range 4000-400 cm-1. The usable range depends on the fiber and crystal actually selected. [23: S01 p.9] [24: REF §5]
- **Raman:** Raman shift (cm-1) and laser excitation wavelength (nm) are stated separately. The usable shift range depends on the laser, spectrometer, fiber and probe selected. [25: S01 p.11]

## Risks and uncertainty

- Turbidity change may alter the effective light path and scattering, degrading a single NIR transmission calibration. The transflection option covering both states is a hypothesis, not established for whey. *(rules: R-GEO-5, R-GEO-6)* [26: S01 p.18] [27: S01 p.17]
- NIR bands are broad and overlapping; the calibration is matrix-specific and must be re-validated if whey composition or turbidity changes. *(rules: R-NIR-2, R-CAL-1)* [28: S01 p.10] [29: REF §5]
- MIR ATR samples only a few micrometres and is prone to fouling and contact problems in a dairy stream. *(rules: R-MIR-3)* [30: S01 p.13] [31: REF §5]
- Protein may be a major component (good for NIR), but if it is a trace component or if other components vary, sensitivity or selectivity may be insufficient. Raman may be swamped by fluorescence. *(rules: R-NIR-4, R-RAM-1)* [32: S01 p.16] [33: S01 p.11]

## First feasibility experiment

1. **Collect representative whey samples across the expected protein range and the turbidity range (clear to turbid), plus process states; measure protein by the customer's independent laboratory method.** Representative samples and an independent reference are the basis of the feasibility plan. [34: REF §3]
2. **Acquire NIR transmission or transflection spectra with a fiber probe in-line or at-line; test both geometries if possible.** Single-method NIR is the primary candidate. [35: S01 p.18]
3. **Acquire MIR ATR and Raman spectra on the same samples as single-method comparisons.** Test each single method before any combination. [36: S04 p.4]
4. **Build chemometric models per method and validate on held-out runs or batches, not only random splits.** Validate the calibration on independent runs or batches. [37: S01 p.10] [38: S03 p.14]
5. **Compare single methods; only if turbidity degrades the best single method, test a NIR plus MIR data-fusion hypothesis against that best single method. Go/no-go criteria (accuracy and robustness across turbidity) are set by the customer.** A combination is a later hypothesis, not a starting point. Numerical go/no-go limits must come from the customer. [39: REF §5] [40: REF §5]

**Reference measurements:** The customer's laboratory protein result is the independent reference. Its method and uncertainty are unknown and must be stated before the go/no-go criteria can be set.

**Decision basis:** Go/no-go must be based on numerical criteria supplied by the customer (for example acceptable error and robustness across the turbidity range). No such numbers are in the enquiry or the sources.

## Assumptions

- Protein is a major component of the whey stream, not a trace component.
- The whey stream is mostly transparent in the baseline state, with turbidity as an intermittent condition.
- The customer's laboratory protein result is available at sufficient frequency and with known uncertainty.
- An in-line or at-line probe can be installed before the concentration stage.

## Not covered by the supplied sources

- Whey-specific protein calibration or validation data.
- The customer's reference laboratory method and its accuracy requirements.
- The achievable MIR fiber link length for this installation.

## Evidence (verified quotes)

1. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
2. ✓ **S01 p.18** (application precedent): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
3. ✓ **S01 p.17** (application precedent): "Partial Least Squares (PLS) regression to quantify fat and protein."
4. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
5. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
6. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
7. ✓ **S04 p.3** (general): "These are, respectively, the amide I and II bands, two major absorption peaks of the protein peptide group in the infrared region."
8. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
9. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
10. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments"
11. ✓ **S01 p.13** (general): "typically at a depth of few microns"
12. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
13. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
14. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
15. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
16. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
17. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
18. ✓ **S02 p.6** (general): "1100 nm Chalcogenide As-S IR Fibers 6500 nm"
19. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
20. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
21. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
22. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
23. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
24. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
25. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
26. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
27. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
28. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
29. ✓ **REF §5** (general): "calibration specific to the matrix."
30. ✓ **S01 p.13** (general): "typically at a depth of few microns"
31. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
32. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
33. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
34. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
35. ✓ **S01 p.18** (application precedent): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
36. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
37. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
38. ✓ **S03 p.14** (general): "A thorough validation, including full, segmented and random-subset CVs, as well as randomization tests, are recommended in any cases for which important conclusions depend on calibration or discrimination models built on limited experimental material."
39. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
40. ✓ (precedent only) **REF §5** (method gain): "a gain is a hypothesis to test."

## Verification

- Citations verified: 40 of 40 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 2; repair rounds: 1.

*Run D03-20261017T084753Z · models deepseek/deepseek-v4.1-flash · cost $0.0202*
