# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified from the stated product and the sources: NIR diffuse reflection for an opaque, concentrated dairy product, MIR ATR as a band-resolved comparison, and NIR transmission/transflection only if some process state is semi-transparent. The final configuration, achievable accuracy and fiber link cannot be fixed until the questions below are answered. All three premises the customer raised are supported by the sources at general scope, so this is a provisional assessment rather than a premise failure.

## Premise check

- **Supported:** In-line spectroscopy can give earlier information about composition changes than the current laboratory sampling. The sources state that fiber probes integrated into production lines give on-site online analysis with results in near real time, and in-process analysis without sampling, eliminating delays. This is a general statement and is not proof for this product. [1: S01 p.3] [2: S01 p.2]
- **Supported:** An initial spectroscopy concept and a practical comparison experiment can be defined before key details are known. The sources support starting with laboratory trials on samples of incompletely known composition in order to select the most suitable method or combination. The resulting concept is provisional, not a final configuration. [3: S01 p.3] [4: REF §3]
- **Supported:** Retaining laboratory checks is compatible with the desired in-line spectroscopy approach. A feasibility plan is expected to include independent reference measurements, which is where the retained laboratory checks fit. No source states a specific accuracy target for this. [5: REF §3]

## Requirements

**Stated by the customer**

- Opaque, concentrated milk product flowing through a processing line.
- Current laboratory sampling for fat and protein analysis.
- Wanted: earlier information about composition changes.
- Product temperature and texture vary during production.
- Wanted: an initial spectroscopy concept and a practical comparison experiment.
- Laboratory checks are to be retained.

**Key unknowns**

- Concentration ranges and the magnitude of the composition changes to be detected (fat, protein and any other component).
- Whether the product is semi-transparent or lower-scattering at any process state.
- Temperature range and rate of temperature and texture change at the measurement point.
- Installation point, line geometry and the distance from the measurement point to the spectrometer (fiber link feasibility).
- Cleaning, fouling and sanitation requirements at the measurement point.
- Required accuracy, detection limit and response time (go / no-go criteria).

## Clarification questions (most decision-relevant first)

Q1. What concentration ranges must be covered, and how large is the composition change you need to see for fat, protein and any other component? *Why it matters:* This decides the needed sensitivity and whether NIR diffuse reflection alone can deliver it. The sources note NIR may lack the sensitivity to detect trace compounds in a bioprocess context. *(affects: method, technique, status)*
Q2. Is the product semi-transparent or clearly lower-scattering at any point or process state in the line, or is it opaque throughout? *Why it matters:* This decides whether NIR transmission or transflection is worth testing at all. Transmission is described for transparent or semi-transparent liquids and fails for thick or fat-rich samples. *(affects: technique, status)*
Q3. What are the expected temperature range and the rate of temperature and texture change at the intended measurement point? *Why it matters:* NIR reflection is sensitive to surface characteristics and particle/globule size, so physical variation can be confused with composition change and affects calibration stability. *(affects: technique, calibration)*
Q4. Where on the line would the measurement sit, what is the pipe or vat geometry and flow, and how far is it from where the spectrometer can be installed? What cleaning and fouling conditions apply there? *Why it matters:* This decides probe type and geometry and whether the fiber link is feasible. Long cables are stated only for low-OH silica fibers; no source states an achievable length for a MIR link. *(affects: installation, fiber, technique)*
Q5. What are your reference laboratory method and sampling protocol for fat and protein, and what accuracy, detection limit and response time would count as a useful improvement? *Why it matters:* These are the reference values and the go / no-go criteria for the trial. No accuracy figure should be assumed from the sources. *(affects: status, go_no_go, calibration)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** The product is stated opaque and concentrated. NIR diffuse reflection is the technique the source gives for opaque or highly concentrated dairy products, and PLS regression on NIR reflection spectra is used to quantify fat and protein in milk. NIR is described as suitable for online measurement including remote measurement via fiber probes. *Conditions:* Applies to the opaque, concentrated product across its stated temperature and texture variation. Requires a chemometric calibration built on this product; NIR bands overlap, and physical variation (scattering, fat globule size) can interfere with the composition signal. [6: S01 p.17] [7: S01 p.17] [8: S01 p.5] [9: S01 p.17]
- **R2 · Comparison candidate: MIR, ATR.** MIR gives well-defined absorption bands and high selectivity. Because water absorbs strongly in the infrared, the source route is ATR with a very thin sampled layer, and ATR fiber probes enable the analysis of liquids. A published MIR-ATR example resolves fat through the ester carbonyl C=O band near 1740 cm-1 and protein through amide bands, which is a reason to test this technique, not proof that it works on this product. *Conditions:* Needs tight contact of the product with the ATR crystal; only a surface layer a few microns deep is sampled, so deposits and surface representativeness are risks. Needs a MIR-transmitting fiber (chalcogenide CIR or polycrystalline PIR); the usable range depends on the fiber and crystal actually selected. [10: S01 p.9] [11: S01 p.5] [12: S01 p.10] [13: S04 p.3] [14: S01 p.13]
- **R3 · Conditional candidate: NIR, transmission transflection.** Transmission is preferred for transparent or semi-transparent liquids but fails when the sample is too thick or fat-rich, because the light cannot penetrate it. A transflection probe can in some cases serve both low-fat and high-fat milk products. This option applies only if the product is, or becomes, semi-transparent and low enough in scattering at some process state. *Conditions:* Deciding question: does any point in the line give a semi-transparent, low-scattering product, and is a controlled pathlength (typically 1-10 mm in the source example) practical there? If the product is opaque throughout, this option does not apply. [15: S01 p.18] [16: S01 p.18] [17: S01 p.18] [18: S01 p.18]

## Measurement concept

- **Probe and geometry:** NIR diffuse reflection with a fiber probe flush-mounted into the pipe or vat so that it interacts with the flowing product; MIR ATR with the probe head in contact with the product; NIR transflection only if a controlled pathlength through a semi-transparent stream is possible. In the source dairy example the reflection probe is flush-mounted into a pipe or vat.
- **Location:** At the point on the line where composition changes need to be seen earliest. Sample inhomogeneity and process turbulence must be considered when choosing the technique and the location.
- **Fiber link:** NIR can use Vis-NIR silica fibers (nominal transmission to 2400 nm); MIR needs chalcogenide CIR or polycrystalline PIR fibers. Long cables (100-300 m) are stated only for low-OH silica fibers; no source states an achievable length for a MIR link, so the MIR link length is an open question for AFS. [19: S01 p.17] [20: S01 p.7] [21: S02 p.6] [22: S02 p.6] [23: S02 p.7]

## Spectral range

- **NIR:** Nominal method range 780-2500 nm. [24: S01 p.10]
- **MIR:** Nominal method range 4000-400 cm-1 (2.5-25 μm). [25: S01 p.9]
- **Raman:** If Raman is used, report the Raman shift in cm-1 and state the laser excitation wavelength separately. [26: S01 p.11]
- **NIR:** The usable range depends on the instrument, fiber and probe actually selected; a nominal method range is not the range of a specific configuration. [27: REF §3] [28: REF §5]

## Risks and uncertainty

- Physical variation: product temperature and texture change during production. NIR reflection is sensitive to surface characteristics and fat globule size, so scattering and physical variation can mask or mimic a composition change. *(rules: R-GEO-6)* [29: S01 p.17]
- Calibration transfer: NIR and Raman calibrations are specific to the matrix. A model built on one product state may not hold when concentration, temperature or texture change. *(rules: R-CAL-1)* [30: REF §5]
- Magnitude of change: if the composition changes to be detected are small, NIR diffuse reflection may lack the sensitivity to see them. The source notes NIR may lack sensitivity for trace compounds below 0.1 percent in a bioprocess context; the magnitude here is unknown. *(rules: R-NIR-4)* [31: S01 p.16]
- MIR ATR practicality: only a surface layer a few microns deep is sampled and tight contact is required, so fouling or deposits and an unrepresentative surface layer can bias results. In addition, MIR light needs CIR or PIR fibers, and no source states an achievable MIR link length for an in-line installation. *(rules: R-MIR-3, R-FIB-2)* [32: S01 p.13] [33: S01 p.10] [34: S02 p.7]

## First feasibility experiment

1. **Collect representative samples across the expected chemical and physical variation: the opaque concentrated product at the fat/protein levels, temperatures and textures seen in production, plus any less-concentrated process states. Keep the existing laboratory fat and protein checks as the reference.** Representative samples and independent reference measurements. [35: REF §3]
2. **Measure each sample with NIR diffuse reflection first (single method), and with MIR ATR as the single-method comparison. No combination in this first round.** Single methods first; combinations only after. *(no verified source: engineering judgement)*
3. **Measure independent references on the same samples using the retained laboratory method and the same sampling protocol, so that every spectrum has a reference fat and protein value.** Independent reference measurements. [36: REF §3]
4. **Build and validate a chemometric model per method, and validate on held-out runs or batches rather than on the samples used for calibration. Compare each single method against the reference. Only if a single method is insufficient, test a combination (for example fused NIR and MIR ATR data) as a later hypothesis.** Matrix-specific calibration and comparison against the best single method. [37: REF §5] [38: REF §5] [39: REF §5]
5. **Go / no-go: apply the numerical accuracy, detection-limit and response-time criteria that the customer sets for a useful improvement over current sampling, and decide on those numbers rather than on any figure from the sources.** Go / no-go basis with criteria from the customer. [40: REF §3]

**Reference measurements:** Retained laboratory fat and protein analysis on the same samples, with the same sampling protocol, as the independent reference.

**Decision basis:** Customer-set numerical accuracy, detection-limit and response-time criteria for a useful improvement over current sampling.

## Assumptions

- The product behaves like a scattering, aqueous dairy matrix, so the source dairy examples are relevant to it.
- The product is opaque throughout the line; no semi-transparent state has been reported.
- The retained laboratory checks can serve as the independent reference for the trial.
- No fluorescent species has been identified, so fluorescence and fluorescence-based combinations are left as later, conditional hypotheses.

## Evidence (verified quotes)

1. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
2. ✓ **S01 p.2** (general): "enabling on-site online analysis and obtaining results in near real time."
3. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
4. ✓ **REF §3** (general): "If the known facts cannot justify a method choice, say so, ask the questions that would decide it and propose the next step."
5. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
6. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
7. ✓ **S01 p.17** (application precedent): "before using Partial Least Squares (PLS) regression to quantify fat and protein."
8. ✓ **S01 p.5** (general): "making it ideal for online applications, including remote measurements via fiber optic probes."
9. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
10. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
11. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
12. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
13. ✓ **S04 p.3** (application precedent): "the stretching vibration band of the ester carbonyl C=O at about 1740 cm-1, which is characteristic of saturated triglycerides."
14. ✓ **S01 p.13** (general): "typically at a depth of few microns"
15. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
16. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
17. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
18. ✓ (precedent only) **S01 p.18** (performance figure): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
19. ✓ **S01 p.17** (application precedent): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
20. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
21. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
22. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
23. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
24. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
25. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
26. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
27. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
28. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
29. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
30. ✓ **REF §5** (general): "calibration specific to the matrix."
31. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
32. ✓ **S01 p.13** (general): "typically at a depth of few microns"
33. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
34. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
35. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
36. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
37. ✓ **REF §5** (general): "calibration specific to the matrix."
38. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
39. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
40. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 40 of 40 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 5; repair rounds: 1.
- Removed 1 intake item(s) not quoted verbatim from the enquiry:
  - intake.targets[0]: enquiry_quote not found verbatim in the enquiry

*Run D02-20261017T101210Z · models deepseek/deepseek-v4.1-flash · cost $0.0185*
