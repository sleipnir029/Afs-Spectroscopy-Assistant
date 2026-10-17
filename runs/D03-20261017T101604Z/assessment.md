# First technical assessment: A clear whey stream before concentration

**Customer enquiry**

> Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the reference. The stream can become more turbid under some operating conditions. We need a first measurement concept that handles this change rather than assuming the liquid always remains clear.

**Decision status:** Provisional feasibility assessment. A defensible shortlist can be proposed, but it rests on stated assumptions: that the whey is an aqueous, clear-to-semi-transparent liquid, and that the target is a major component. The decisive numbers (protein range, required accuracy, actual turbidity range) are not yet known and must come from the customer.

## Premise check

- **Supported:** Laboratory results can be used as the reference for the protein measurements. A feasibility plan is expected to include independent reference measurements; the customer must define the reference method and its uncertainty. [1: REF §3]
- **Not covered:** One first measurement concept can handle the change from clear to more turbid. No supplied source states that a single measurement concept covers both a clear and a turbid state of the same stream. The closest statements are a dairy example where a transflection probe works 'in some cases' for low- and high-fat products, and the general point that keeping more than one technique available gives flexibility. Both are reasons to test, not a demonstration. [2: S01 p.18]
- **Supported:** Do not assume the liquid always remains clear. The source states plainly that a transmission measurement fails once the sample becomes too thick or opaque, so the turbid state must be taken into account when choosing the technique. [3: S01 p.18] [4: S01 p.7]
- **Supported:** Spectroscopy can track protein concentration. There is a published dairy precedent for quantifying protein from NIR spectra with chemometrics. This is a reason to test the method on the customer's whey, not proof that it will work for this stream. [5: S01 p.17]

## Requirements

**Stated by the customer**

- Track protein concentration in a dairy whey stream before a concentration stage.
- Use laboratory results as the reference.
- The stream is relatively clear but can become more turbid under some operating conditions.
- The first measurement concept must handle that change rather than assuming the liquid stays clear.

**Key unknowns**

- Target protein species and concentration range, and the required accuracy (the go/no-go numbers).
- Expected turbidity / optical-density range and how often or how long the stream is turbid.
- Matrix composition and interferences (other components, additives, dissolved solids, temperature).
- Installation point, flow, temperature, pressure, distance from the spectrometer, and cleaning/fouling regime.
- Reference laboratory method and its uncertainty and sampling procedure.
- Whether the stream ever becomes opaque, which decides the measurement geometry.

## Clarification questions (most decision-relevant first)

Q1. What is the target protein concentration range, and what accuracy or uncertainty limit defines a successful measurement (the go/no-go numbers)? *Why it matters:* Without a number for accuracy, the method choice and the feasibility test cannot be judged. The go/no-go basis must come from the customer. *(affects: method, status)*
Q2. How turbid does the stream actually get (optical density or suspended-solids range), how often and for how long, and does it ever become opaque? *Why it matters:* Transmission loses signal when the sample becomes too thick, and reflection is less representative for clear liquids; the turbidity range decides which geometry can be tested first. *(affects: technique, installation)*
Q3. Where and how would the probe be installed (in-line in a pipe, flow rate, temperature, pressure), at what distance from the spectrometer, and what cleaning or fouling regime applies? *Why it matters:* Contact, fouling and fiber-link length differ strongly between NIR transmission/transflection and MIR ATR, and the MIR link length is not stated in the sources. *(affects: technique, installation)*
Q4. What is the reference laboratory method for protein, and what is its uncertainty and sampling procedure? *Why it matters:* The reference defines the achievable calibration accuracy and must be independent of the spectroscopic measurement. *(affects: status)*
Q5. What is the rest of the matrix (other components, additives, dissolved solids) and does the whey show a fluorescence background? *Why it matters:* Matrix-specific calibration and fluorescence background decide whether NIR alone is sufficient and whether methods such as Raman are worth testing. *(affects: method)*

## Recommendation

- **R1 · Primary candidate: NIR, transmission transflection.** Whey is named in the source as an example of a transparent-to-semi-transparent dairy liquid for which NIR transmission is the preferred route, and NIR suits remote in-line measurement through fiber probes. The transflection variant is the closest thing in the sources to one geometry covering both a clear and a more scattering (turbid) state, but this is stated only as 'in some cases' and must be treated as a hypothesis to test. *Conditions:* Applies while the stream is transparent to semi-transparent. The optical pathlength must be controlled; too wide loses signal to absorption, too narrow samples a negligible volume. Requires a matrix-specific chemometric calibration. [6: S01 p.18] [7: S01 p.18] [8: S01 p.5] [9: S01 p.18]
- **R2 · Comparison candidate: MIR, ATR.** MIR is described as one of the most informative methods of chemical analysis, with well-defined absorption bands; it needs very thin samples or ATR. ATR suits liquids and soft solids in tight contact and samples only a surface layer, which makes it a natural comparison for the more turbid end of the stream and gives chemically complementary information to NIR. Protein peptide bands fall in this region. *Conditions:* Requires tight contact with the probe head and a sample suitable for ATR; the surface layer is only a few micrometres deep, so deposits and fouling matter. Usable range is set by the crystal and fiber actually chosen. [10: S01 p.9] [11: S01 p.5] [12: S04 p.4] [13: S04 p.3]
- **R3 · Conditional candidate: NIR, transmission transflection.** A combination of NIR and MIR ATR is the later hypothesis to test if neither single method meets the accuracy target across the whole clear-to-turbid range. Combining methods can help for complex or varying samples, but any gain is a hypothesis, must be compared with the best single method, and requires the two measurements to be aligned at the same point and time. *Conditions:* Applies only after the single-method NIR and MIR ATR tests, and only if one of them alone does not meet the customer's go/no-go numbers over the full range of stream states. [14: S01 p.7] [15: REF §5] [16: REF §5] [17: S01 p.8] Later hypothesis, after single-method tests: combine with MIR, MIR, MIR.
- **R4 · Not recommended: NIR, diffuse reflection.** Not the first geometry to test for this stream: NIR reflection is described for opaque, concentrated or scattering products, and reflection can be less representative for clear liquids, which is the state the customer describes as the normal one. If the stream turns out to be turbid most of the time, this choice should be re-assessed with AFS. *Conditions:* Revisit only if the dominant process state is turbid/opaque rather than clear. [18: S01 p.17] [19: S01 p.18]

## Measurement concept

- **Probe and geometry:** Start with an in-line NIR transmission/transflection probe through the flowing whey before the concentration stage, with a defined, controlled optical pathlength. Keep MIR ATR as the comparison route for the more turbid state, where contact with an ATR crystal gives a very short effective path in a scattering liquid.
- **Location:** In the process line at the point before the concentration stage; the exact tapping point and flow conditions are not yet known (see Q3).
- **Fiber link:** For NIR, Vis-NIR silica fibers are the appropriate family (nominal transmission to about 2.4 µm); if Raman or fluorescence is added later, metal-coated silica avoids polymer-jacket fluorescence. For MIR ATR, chalcogenide or polycrystalline infrared fibers are needed because silica cannot carry mid-IR light. The achievable length of a mid-IR fiber link to the process is not stated in the supplied material and must be confirmed with AFS. [20: S02 p.6] [21: S02 p.6] [22: S02 p.6] [23: S02 p.7] [24: S02 p.7]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [25: S01 p.10] [26: REF §3]
- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the ATR crystal and the fiber selected. [27: S01 p.9] [28: REF §5]

## Risks and uncertainty

- The calibration is specific to the matrix; if the whey composition or its turbidity changes, the model must be re-validated (and usually rebuilt or extended) on the new material. *(rules: R-CAL-1)* [29: REF §5]
- One geometry may not cover both states: transmission loses signal when the stream becomes too thick or opaque, while reflection is less representative for clear liquids. *(rules: R-GEO-2, R-GEO-4)* [30: S01 p.18] [31: S01 p.18]
- If the protein is a minor component or the accuracy target is tight, NIR may lack sensitivity; the source notes it may not detect trace compounds below 0.1 percent in a bioprocess context. *(rules: R-NIR-4)* [32: S01 p.16]
- ATR samples only a surface layer of a few micrometres, so deposits, fouling and surface representativeness are real risks in a process stream. *(rules: R-MIR-3)* [33: S01 p.13] [34: REF §5]

## First feasibility experiment

1. **Agree with the customer on the target protein range, the accuracy limit, the acceptable failure rate and the reference method, so that the go/no-go basis is numerical and comes from the customer.** Define the decision criterion before any measurement. [35: REF §3]
2. **Collect representative whey samples across the expected protein range and across the expected physical variation, including the clearest and the most turbid states the process produces, and note the temperature.** Cover the variation the model must handle rather than a single clear state. [36: S02 p.20]
3. **Measure the samples with NIR transmission/transflection first, and obtain independent reference protein values by the customer's laboratory method on the same samples.** Test the primary single method against an independent reference. [37: S01 p.3]
4. **Build and cross-validate a chemometric model on part of the runs or batches, then test it on held-out runs or batches that were not used in the calibration.** Check that the model generalises across process states rather than fitting one run. [38: REF §5]
5. **Repeat the measurement and modelling with MIR ATR as a second single method on the same samples. Only if neither single method meets the go/no-go numbers across the whole clear-to-turbid range, test the NIR + MIR ATR combination with sampling aligned to the same point and time.** Compare single methods first and treat the combination as a later hypothesis. [39: REF §5] [40: REF §5]

**Reference measurements:** Independent laboratory protein determination on the same samples, defined by the customer (see Q4).

**Decision basis:** The customer's own accuracy/uncertainty limit and acceptable failure rate (see Q1); no accuracy figure is available from the supplied material.

## Assumptions

- The whey is an aqueous liquid that is normally clear to semi-transparent and becomes more turbid only under some operating conditions.
- Protein is present as a major component rather than a trace component.
- The measurement point is in-line before the concentration stage.

## Not covered by the supplied sources

- No supplied source shows protein quantification in whey specifically; the dairy protein examples are for milk, so the whey application would have to be established by testing.
- No supplied source states an achievable fiber length for a mid-IR (ATR) link to a process point; the mid-IR fiber and hollow-waveguide comparison in the supplied material is at laboratory scale, so any longer MIR link is an open question for AFS.

## Evidence (verified quotes)

1. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
2. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
3. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
4. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
5. ✓ **S01 p.17** (application precedent): "before using Partial Least Squares (PLS) regression to quantify fat and protein."
6. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
7. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
8. ✓ **S01 p.5** (general): "making it ideal for online applications, including remote measurements via fiber optic probes."
9. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
10. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
11. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
12. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
13. ✓ **S04 p.3** (general): "amide I and II bands, two major absorption peaks of the protein peptide group in the infrared region."
14. ✓ **S01 p.7** (general): "The analysis of such systems may require a combination of two or even more spectral methods."
15. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
16. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
17. ✓ **S01 p.8** (general): "collected from the same small, even pinpoint, area of the sample. This is difficult to achieve by using two probes alternately for measurements."
18. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
19. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
20. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
21. ✓ **S02 p.6** (general): "1100 nm Chalcogenide As-S IR Fibers 6500 nm"
22. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 µm"
23. ✓ **S02 p.7** (general): "Free of Polymer jacket fluorescence for Raman and Fluo- Spectroscopy"
24. ✓ **S02 p.7** (general): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
25. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
26. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
27. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
28. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
29. ✓ **REF §5** (general): "calibration specific to the matrix."
30. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
31. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
32. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
33. ✓ **S01 p.13** (general): "typically at a depth of few microns"
34. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
35. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
36. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
37. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
38. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
39. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
40. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."

## Verification

- Citations verified: 40 of 40 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 4; repair rounds: 1.

*Run D03-20261017T101604Z · models deepseek/deepseek-v4.1-flash · cost $0.0166*
