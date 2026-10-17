# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Provisional feasibility assessment. An opaque, concentrated dairy stream is a case where a single method can be shortlisted with stated assumptions: NIR diffuse reflection is the established inline technique for opaque/concentrated dairy, with MIR ATR as a single-method comparison. Several facts (targets, accuracy, temperature/texture range, installation, cleaning) are still missing, so this is a provisional shortlist, not a configuration.

## Premise check

- **Supported:** Earlier information about composition changes can be obtained by spectroscopy. Sources support in-process optical analysis in near real time in general. This is a general capability, not proof for this product. [1: S01 p.3]
- **Supported:** An initial spectroscopy concept and a practical comparison experiment can be defined before key method-choice facts are known. Guidance explicitly allows a provisional plan built on missing facts; it must state its assumptions. [2: REF §3]
- **Supported:** The opaque, concentrated milk product can be measured in-line by spectroscopy. Supported only as an application precedent (a reason to test), not as proof that it will work for this customer's product. To be confirmed by test. [3: S01 p.17]
- **Not covered:** Variation in product temperature and texture during production can be accommodated by the proposed spectroscopy concept. No source states that the proposed concept accommodates this product's temperature and texture variation. Sources only warn that physical variation must be considered and that reflection is sensitive to surface and globule size. Treat as open: it must be handled by scatter correction and by a calibration spanning the real variation, and confirmed by test. [4: S01 p.7]

## Requirements

**Stated by the customer**

- In-line (earlier) information about composition changes for an opaque, concentrated milk product in a processing line.
- Targets named: fat and protein.
- Temperature and texture vary during production.
- Retain existing laboratory checks.

**Key unknowns**

- Required accuracy, precision, detection limit and response time for the in-line fat/protein measurement.
- Temperature range and the texture/viscosity states at the intended measurement point, and whether they vary within a batch or between batches.
- Installation point (pipe or vat), process pressure/flow, cleaning/fouling (CIP) requirements, and the distance from the measurement point to the spectrometer.
- Whether the product is transparent or semi-transparent anywhere in the line.
- Detailed matrix composition and the reference laboratory method used for fat and protein.
- Whether the product contains a fluorescent species (would open fluorescence-based combinations).

## Clarification questions (most decision-relevant first)

Q1. What must the in-line measurement deliver: only fat and protein, or other composition changes too, and with what accuracy, precision, detection limit and response time? *Why it matters:* Defines whether a method can meet the target and sets the go/no-go numbers. *(affects: method, calibration, status)*
Q2. What are the temperature range and the texture/viscosity states at the intended measurement point, and do they vary within a batch or between batches? *Why it matters:* Decides whether NIR diffuse reflection alone is adequate or whether scatter correction and a range-spanning calibration are essential, and whether MIR ATR contact is stable. *(affects: technique, calibration, status)*
Q3. Where can the probe be installed (pipe or vat), and what are the pressure, flow, cleaning/fouling (CIP) conditions and the distance from the measurement point to the spectrometer? *Why it matters:* Decides the probe geometry, fiber type/length and installation feasibility. *(affects: installation, fiber, status)*
Q4. Is the product transparent or semi-transparent anywhere in the line (e.g., early or late stages), so that a transmission or transflection measurement could be tried? *Why it matters:* Decides whether the conditional NIR transmission/transflection option is worth testing at all. *(affects: technique, status)*
Q5. What is the current laboratory reference method for fat and protein, and what precision does it achieve? *Why it matters:* Defines the independent reference and the comparison basis for the feasibility experiment. *(affects: experiment, calibration)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** For an opaque, concentrated dairy stream, NIR reflection is the established inline technique; NIR penetrates up to several millimetres and works with ordinary glass optics, which suits a remote fiber-probe link. *Conditions:* Applies if the product at the probe behaves as an opaque scattering medium. Requires scatter correction and a matrix-specific chemometric calibration. [5: S01 p.17] [6: S01 p.5]
- **R2 · Comparison candidate: MIR, ATR.** MIR is highly informative with well-defined bands, and ATR suits liquids and soft solids in contact, giving a very short effective path. Advanced dairy labs add MIR ATR for information NIR may miss. Test as a separate single method against the NIR reflection result. *Conditions:* Applies if the product makes tight contact with the ATR crystal and fouling is manageable. Needs MIR-capable fibers (chalcogenide/CIR or polycrystalline/PIR), not silica. [7: S01 p.18] [8: S01 p.9] [9: S01 p.10]
- **R3 · Conditional candidate: NIR, transmission transflection.** Screening left this as unknown: transmission fails for thick, opaque or fat-rich product, but a transflection probe may work in some cases. Worth testing only if the product is transparent or semi-transparent somewhere in the line and the optical pathlength can be controlled. *Conditions:* Applies only if Q4 shows a transparent/semi-transparent window and a controllable pathlength. [10: S01 p.18] [11: S01 p.18]

## Measurement concept

- **Probe and geometry:** Primary: fiber-optic diffuse-reflection (reflex) probe flush-mounted into the pipe or vat so the tip interacts directly with the flowing product. Comparison: MIR ATR probe in contact with the product. A combination of methods is a later hypothesis, to be compared with the best single method after the single-method tests.
- **Location:** At a point where the product is representative and the probe tip can be kept clean; the exact point depends on Q3 and is not yet fixed.
- **Fiber link:** NIR reflection can use silica fibers (Vis-NIR, to about 2400 nm). MIR ATR needs chalcogenide (CIR) or polycrystalline (PIR) fibers, because silica does not carry MIR. Spectrometers can be placed away from the line. [12: S01 p.17] [13: S01 p.10] [14: S02 p.6] [15: S02 p.6] [16: S01 p.15]

## Spectral range

- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected; this is not a configuration. [17: S01 p.10] [18: REF §3]
- **MIR:** Nominal method range 4000-400 cm-1. The usable range is limited by the fiber and ATR crystal actually selected. [19: S01 p.9] [20: REF §5]

## Risks and uncertainty

- Physical variation (temperature, texture/viscosity, fat-globule size) changes the diffuse-reflection signal and can be mistaken for a composition change; scatter correction and a calibration spanning the real variation are needed. *(rules: R-GEO-6, R-GEN-5)* [21: S01 p.17] [22: S01 p.17] [23: S01 p.7]
- MIR ATR samples only a surface layer a few micrometres deep; on an opaque, concentrated product the crystal can foul or accumulate deposits, and the surface may not represent the bulk. *(rules: R-MIR-3)* [24: S01 p.13] [25: REF §5]
- Calibrations are matrix-specific, so a change in composition, temperature or texture may require re-validation; NIR may also be insensitive to small or trace changes. *(rules: R-CAL-1, R-NIR-4)* [26: REF §5] [27: S01 p.16]
- MIR needs MIR-capable fibers (silica ends near 2400 nm), and no source states an achievable MIR link length for a process line, so the MIR option's installation distance is unconfirmed. *(rules: R-FIB-1, R-FIB-2)* [28: S02 p.6] [29: S02 p.7]

## First feasibility experiment

1. **Select representative samples across the expected chemical and physical variation: several fat and protein levels, and the temperature and texture states seen in production, including the extremes.** Cover the real variation the calibration must handle. [30: REF §3]
2. **Measure every sample first with the single leading method, NIR diffuse reflection, using the intended in-line probe geometry (flush-mounted reflex probe) and the selected fiber link, at the intended temperature(s).** Test the best single method before any combination. [31: REF §5]
3. **Measure an independent reference (the existing laboratory fat and protein method) on the same samples, and build a chemometric model (with scatter correction) against that reference.** Independent reference and model building. [32: S01 p.17]
4. **Then test MIR ATR on the same sample set as a separate single method, and only afterwards test whether combining methods adds anything over the best single method.** Single methods first; combinations as a later hypothesis. [33: REF §5]
5. **Validate the models on held-out runs or batches (not used for calibration) and decide go/no-go against the customer's own numerical criteria (target accuracy, precision, detection limit and response time, to be supplied).** Held-out validation and go/no-go basis. [34: REF §3]

**Reference measurements:** Existing laboratory fat and protein method (details to be supplied by the customer).

**Decision basis:** Go/no-go is defined by the customer's own numerical criteria (accuracy, precision, detection limit, response time). None are available yet, so the experiment cannot be judged passed or failed until they are set.

## Assumptions

- The product is a liquid at the measurement point and remains in contact with the probe.
- The product behaves as an opaque scattering medium at the intended point (basis: the customer's statement 'opaque, concentrated').
- Fat and protein are the only targets for the first test.
- Laboratory reference values are available per sample for model building.

## Not covered by the supplied sources

- No source gives accuracy, detection limits or response time for in-line fat/protein measurement of an opaque concentrated milk product.
- No source states an achievable MIR fiber link length for a process line.
- No source covers probe cleaning or sanitation (CIP) compatibility for an in-line installation.

## Evidence (verified quotes)

1. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
2. ✓ **REF §3** (general): "An honest provisional plan is more useful than a final configuration built on missing facts."
3. ✓ **S01 p.17** (application precedent): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
4. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
5. ✓ **S01 p.17** (application precedent): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
6. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
7. ✓ **S01 p.18** (general): "advanced labs often incorporate Fluorescence, Raman, and Mid-Infrared (MIR) ATR fiber optic techniques to capture specific chemical or structural information that NIR might miss."
8. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
9. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
10. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
11. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
12. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
13. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments"
14. ✓ **S02 p.6** (performance figure): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
15. ✓ **S02 p.6** (performance figure): "1100 nm Chalcogenide As-S IR Fibers 6500 nm"
16. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
17. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
18. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
19. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
20. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
21. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
22. ✓ **S01 p.17** (general): "applying Multiplicative Scatter Correction (MSC) or Standard Normal Variate (SNV) transformations to remove physical interference caused by the scattering nature of the milk particles"
23. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
24. ✓ **S01 p.13** (general): "typically at a depth of few microns"
25. ✓ **REF §5** (general): "contact, fouling, compatibility."
26. ✓ **REF §5** (general): "calibration specific to the matrix."
27. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
28. ✓ **S02 p.6** (performance figure): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
29. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
30. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
31. ✓ **REF §5** (general): "compare with the best single method."
32. ✓ **S01 p.17** (general): "applying Multiplicative Scatter Correction (MSC) or Standard Normal Variate (SNV) transformations to remove physical interference caused by the scattering nature of the milk particles"
33. ✓ **REF §5** (general): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
34. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 34 of 34 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 0; repair rounds: 0.

*Run D02-20261017T092526Z · models deepseek/deepseek-v4.1-flash · cost $0.0140*
