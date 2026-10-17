# First technical assessment: Glucose and lactate trends in an aqueous bioprocess

**Customer enquiry**

> We run a cell culture process in an aqueous medium. Glucose and lactate are measured from samples, and the delay makes it difficult to see changes promptly. We are exploring an in situ spectroscopy pilot that can be checked against those existing laboratory measurements. The medium and cell population change during the run; we have not yet selected a probe or a calibration strategy.

**Decision status:** Provisional feasibility assessment. A shortlist of single methods worth testing can be justified from the sources: Raman and mid-IR ATR pass the screening for an in-line aqueous application, and NIR transmission is conditional on the broth's optical density. The concentration ranges, required accuracy and required response time are not known, so this is a provisional assessment with stated assumptions, not a selection of a probe or a calibration strategy. Any combination is only a later hypothesis to test against the best single method.

## Premise check

- **Not covered:** An in situ spectroscopy pilot is appropriate for this cell culture process. The supplied sources describe fiber-probe in-line/on-line analysis in reactors in general, but none of them addresses this customer's process, medium or analytes, so appropriateness for this process is not established by the sources. *(no verified source: engineering judgement)*
- **Supported:** The in situ pilot can be checked against the existing laboratory measurements. Independent reference measurements are part of the feasibility comparison described in the guidance. Whether the existing laboratory method is accurate, traceable and time-aligned enough to serve as the reference is not established by the sources and must be confirmed by the customer. [1: REF §3]
- **Supported:** The delay of sampling makes it difficult to see changes promptly. The source states that in-process analysis removes sampling and its delays, which is the rationale the customer gives. [2: S01 p.3]
- **Not covered:** The medium and cell population change during the run. No supplied source addresses this customer's process. The consequence is covered in general terms: a calibration is specific to the matrix, so a model built on one process state has to be checked and usually rebuilt or extended on the new material. *(no verified source: engineering judgement)*

## Requirements

**Stated by the customer**


**Key unknowns**

- Typical and extreme concentrations of glucose and lactate in the broth, and the accuracy and precision needed for a result to be actionable.
- Required response time / update interval for the in-situ measurement.
- Optical density (turbidity) of the medium at the start and end of the run - this decides whether transmission geometry is possible at all.
- Fluorescence background of the medium and cells (it can swamp the Raman signal).
- Installation conditions: available port, temperature, pressure, cleaning/sterilization (CIP/SIP), and the distance from the vessel to the spectrometer.
- The existing laboratory reference method for glucose and lactate: identity, uncertainty, sampling delay, and whether reference samples can be time-stamped to the in-situ reading.

## Clarification questions (most decision-relevant first)

Q1. What are the typical and extreme glucose and lactate concentrations in the broth, what accuracy and precision do you need, and what response time (update interval) would let you act on the result? *Why it matters:* These numbers are the basis for the go/no-go criteria and decide whether a method with lower sensitivity for trace levels can be used at all. *(affects: method, technique, status)*
Q2. How turbid is the broth at the start and at the end of the run (optical density), and does it stay transparent or semi-transparent? *Why it matters:* Transmission geometry only works while light can pass through the sample; turbidity decides between transmission, ATR and reflection geometry, and therefore the technique. *(affects: technique, installation, status)*
Q3. Does the medium or the cell population show a strong fluorescence background, and can we measure a representative sample to check it? *Why it matters:* A strong fluorescence background can mask the weak Raman signal, which would change the method ranking. *(affects: method, technique)*
Q4. What are the installation conditions - available port, temperature, pressure, cleaning/sterilization (CIP/SIP) - and how far is the spectrometer from the vessel? *Why it matters:* These decide probe type, fiber family and whether a long fiber link is required; the achievable link length for a mid-IR connection is not stated in the sources. *(affects: installation, technique)*
Q5. Which laboratory method gives your glucose and lactate values today, with what uncertainty and sampling delay, and can reference samples be time-stamped to the in-situ reading? *Why it matters:* The pilot can only be judged against a reference that is accurate and time-aligned; this decides the comparison design. *(affects: status, calibration)*

## Recommendation

- **REC1 · Primary candidate: Raman, raman probe.** Raman passes the screening for an in-line aqueous application and is the single method whose physics fits an aqueous broth best: it is stated to be well suited to aqueous environments because water absorbs much less than in infrared methods. In the bioprocess section of the same source, Raman is described as usable in the reactor for direct detection of metabolites such as glucose, acetate or lactate, and Raman spectra are stated to support chemometric calibration or classification models. That is a reason to test Raman here, not proof that it will work for this customer's medium, cell line or concentration range. *Conditions:* Only after the fluorescence background of the medium and cells has been checked on real samples, because a fluorescence background can be much stronger than the weak Raman signal. The laser excitation wavelength must be chosen and reported separately from the Raman shift axis. Screening status: pass. [3: S01 p.16] [4: S01 p.16] [5: S01 p.12] [6: S01 p.11]
- **REC2 · Comparison candidate: MIR, ATR.** Mid-IR ATR passes the screening and is the second single method worth testing against Raman on the same samples. Mid-IR is described as one of the most informative methods of chemical analysis, and ATR fiber probes are described as enabling the analysis of liquids and solid elastic samples, with probe-based analysis in use for in-line, in-process environments. ATR gives an evanescent-wave measurement with a very short effective path, which matters in a water-dominated medium. The comparison tells us which single method carries usable glucose and lactate information in this matrix before any combination is considered. *Conditions:* ATR requires tight contact and suits liquids and soft solids; it samples only a surface layer of a few micrometres, so deposits, fouling and cell adhesion at the crystal are risks, as is sample representativeness in a changing broth. Screening status: pass. [7: S01 p.9] [8: S01 p.10] [9: S01 p.10] [10: S01 p.13] [11: REF §5]
- **REC3 · Conditional candidate: NIR, transmission transflection.** NIR transmission is conditional: it applies only if the broth stays transparent or semi-transparent throughout the run (Q2). In the dairy example, transmission is the preferred geometry for transparent or semi-transparent liquids, and in the bioprocess section NIR is described as effective for major components such as glucose in the millimolar range. That makes it worth testing as a third single method if - and only if - the optical density allows it. It is not recommended as a first choice for a broth that is or becomes turbid. *Conditions:* Applies only if the broth is and remains transparent or semi-transparent (deciding question Q2: optical density at the start and end of the run). The optical pathlength must be controlled; if it is too wide the signal is lost to absorption, if too narrow the sampled volume is negligible. NIR may lack sensitivity below the trace level stated in the source, so the required glucose and lactate ranges decide its usefulness. Screening status: unknown (Table 1 sample-type fit not confirmed for this sample). [12: S01 p.18] [13: S01 p.18] [14: S01 p.16]

## Measurement concept

- **Probe and geometry:** In-situ probe in contact with the broth. For Raman: a contact Raman probe with the excitation wavelength stated separately. For mid-IR: an ATR probe immersed in the liquid. For NIR (conditional): a transmission/transflection probe with a controlled optical pathlength, used only while the broth stays transparent or semi-transparent.
- **Location:** In the bioreactor or process line at a point representative of the broth. Medium and cell population change during the run, so the sampling point and the analysed volume matter; ATR analyses only a surface layer of a few micrometres, so contact, deposits and representativeness are risks.
- **Fiber link:** Fiber link to the spectrometer placed away from the vessel. Silica fibers carry the UV-Vis-NIR range; mid-IR needs chalcogenide (CIR) or polycrystalline (PIR) fibers. The usable fiber length is configuration-dependent; no source states an achievable length for a mid-IR link. [15: S01 p.10] [16: S01 p.15] [17: S02 p.6] [18: S02 p.6] [19: REF §5]

## Spectral range

- **Raman:** Raman is reported as Raman shift on a wavenumber (cm-1) axis; the laser excitation wavelength is stated separately. In the shown example, 785 nm excitation is used with a contact Raman probe. [20: S01 p.11] [21: S01 p.15]
- **MIR:** Nominal mid-IR range 4000-400 cm-1 (2.5-25 um). The usable range depends on the fiber, crystal and probe actually selected; it is limited by contact and fouling at the ATR crystal. [22: S01 p.9] [23: REF §5]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [24: S01 p.10] [25: REF §3]

## Risks and uncertainty

- The Raman signal can be swamped by fluorescence from the medium or the cells. *(rules: R-RAM-1)* [26: S01 p.11]
- Calibration is matrix-specific. As the medium and the cell population change during the run, a model built on one process state has to be checked and usually rebuilt or extended on the new material; a single calibration for the whole run is an assumption, not a given. *(rules: R-CAL-1)* [27: REF §5]
- Geometry risk: if the broth is or becomes turbid, NIR transmission loses its signal, and mid-IR ATR only probes a surface layer a few micrometres deep where deposits or fouling change the measurement. *(rules: R-GEN-4, R-MIR-3)* [28: S01 p.18] [29: S01 p.13] [30: REF §5]
- Performance figures are unconfirmed: no source states an achievable cable length for a mid-IR link, and no source gives accuracy, detection limits or response time for glucose and lactate in this medium. For trace levels, NIR sensitivity is a stated limitation. *(rules: R-FIB-2, R-NIR-4)* [31: S02 p.7] [32: S02 p.10] [33: S01 p.16]

## First feasibility experiment

1. **1. Representative samples across the run** Cover the expected chemical and physical variation: broth samples (or process states) from low to high cell density and across the expected glucose and lactate range, with spiked levels where useful. [34: REF §3]
2. **2. Single-method laboratory comparison first** Measure the same samples with the single candidates - Raman probe and mid-IR ATR, and NIR transmission only if the broth stays transparent - and record which method gives usable signal for glucose and for lactate. No combination in this step. [35: S01 p.3]
3. **3. Independent reference measurements** Measure glucose and lactate with the existing laboratory method on the same samples, plus a cell-density/viability reference for the biomass, time-stamped so in-situ and reference values can be paired. [36: REF §3]
4. **4. Calibration and validation on held-out runs** Build chemometric models per analyte on part of the data and validate them on held-out runs or batches, not on the runs used for calibration, given that the matrix changes during the run. [37: S03 p.14]
5. **5. Go/no-go** Fix the numerical go/no-go criteria with the customer before the trial (accuracy, precision and response time for glucose and lactate). Go if the in-situ prediction meets them on the held-out runs; otherwise fall back to the next single method before considering any combination. A combination is only a later hypothesis to test against the best single method. [38: REF §3]

**Reference measurements:** Existing laboratory glucose and lactate values on the same samples, plus cell density / viability, time-stamped to the in-situ readings.

**Decision basis:** Customer-defined numerical criteria for accuracy, precision and response time per analyte, checked on held-out runs.

## Assumptions

- The broth behaves as a liquid that can be brought into contact with a probe (stated as an aqueous medium).
- The existing laboratory glucose/lactate method is accurate and time-aligned enough to act as the reference; this is not established by the sources.
- Whether one single method can cover both analytes is an outcome of the trial, not an assumption; a combination is only considered after the single-method comparison.

## Not covered by the supplied sources

- Achievable accuracy, detection limits and response time for glucose and lactate in cell-culture medium: no supplied source states these figures.
- Probe compatibility with the customer's cleaning and sterilization regime (CIP/SIP): not covered by the supplied sources.

## Evidence (verified quotes)

1. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
2. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
3. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
4. ✓ **S01 p.16** (application precedent): "direct detection of specific metabolites like glucose, acetate, or lactate."
5. ✓ **S01 p.12** (general): "Raman spectra (as well as IR absorption spectra) can be used to construct chemometric models-calibration or classification ones."
6. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
7. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
8. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
9. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments"
10. ✓ **S01 p.13** (general): "typically at a depth of few microns"
11. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
12. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
13. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
14. ✓ (precedent only) **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
15. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments"
16. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
17. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
18. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
19. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
20. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
21. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
22. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
23. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
24. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
25. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
26. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
27. ✓ **REF §5** (general): "calibration specific to the matrix."
28. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
29. ✓ **S01 p.13** (general): "typically at a depth of few microns"
30. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
31. ✓ **S02 p.7** (general): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
32. ✓ **S02 p.10** (general): "1 Meter PolyMicro hollow fiber 1mm ID"
33. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
34. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
35. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
36. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
37. ✓ **S03 p.14** (general): "A thorough validation, including full, segmented and random-subset CVs, as well as randomization tests, are recommended in any cases for which important conclusions depend on calibration or discrimination models built on limited experimental material."
38. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 38 of 38 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 7; repair rounds: 1.
- Removed 5 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry
  - intake.process[5]: enquiry_quote not found verbatim in the enquiry
  - intake.process[6]: enquiry_quote not found verbatim in the enquiry
  - intake.process[8]: enquiry_quote not found verbatim in the enquiry

*Run D04-20261017T094013Z · models deepseek/deepseek-v4.1-flash · cost $0.0201*
