# First technical assessment: API concentration during hot polymer extrusion

**Customer enquiry**

> We are developing a hot polymer extrusion process that incorporates an active pharmaceutical ingredient. We want to investigate whether an optical measurement can detect composition changes while the melt is being processed. We have offline assays, but the process interface is hot and may be exposed to material build up. We need an initial comparison plan and the questions required before choosing a probe.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified with explicit assumptions, but the physical state of the melt, the target analyte, and the installation point are unknown. The screening status of all candidates is 'unknown' because the sample state and optical regime are not specified. The recommendation is therefore conditional on the answers to the clarification questions.

## Premise check

- **Not covered:** An optical measurement can detect composition changes while the melt is being processed.. No supplied source directly addresses this customer's hot polymer melt. A source shows NIR reflection and MIR-ATR spectroscopy used to control polymer extrusion in-line, which is a reason to test, not proof for this process. [1: S02 p.14]
- **Supported:** The process interface is hot and may be exposed to material build up, which may affect probe choice.. The source shows a hot melt extruder with a NIR probe in the extruder barrel and notes ATR probes can be sealed in PEEK, but it does not give temperature ratings or fouling performance. The premise that these factors affect probe choice is consistent with the sources. [2: S02 p.14] [3: S02 p.13]

## Requirements

**Stated by the customer**

- Initial comparison plan
- Questions required before choosing a probe

**Key unknowns**

- Physical state and optical behaviour of the melt (transparent, scattering, opaque)
- Target species and concentration range (API, polymer, moisture, degradant)
- Matrix composition and interferences
- Temperature and pressure at the measurement point
- Installation point and distance to analyzer
- Cleaning and fouling conditions
- Required accuracy and response time
- Reference method for calibration

## Clarification questions (most decision-relevant first)

Q1. What is the physical state and optical behaviour of the melt at the intended measurement point: transparent, scattering, opaque, or does it change during the process? *Why it matters:* This decides between transmission/transflection and diffuse reflection for NIR, and whether ATR is the only viable contact geometry. *(affects: method, technique, installation)*
Q2. What is the target analyte and its expected concentration range? Is the goal to quantify the API, detect a degradant, monitor moisture, or track a bulk property such as blend uniformity? *Why it matters:* This determines whether NIR, Raman, MIR, or a combination is most promising, and whether trace-level sensitivity is required. *(affects: method, technique)*
Q3. What is the melt temperature and pressure at the proposed measurement point, and what is the distance from that point to where a spectrometer could be located? *Why it matters:* Probe material, sealing, and fiber link length depend on temperature and pressure. No source states an achievable MIR link length, so this is an open question for AFS. *(affects: installation, fiber)*
Q4. What is the polymer matrix and are there known interferences, such as strong fluorescence, water, or other additives? *Why it matters:* Fluorescence can swamp Raman; water absorbs strongly in infrared methods; matrix changes require re-validation of chemometric calibrations. *(affects: method, technique)*
Q5. What is the required accuracy, precision, and response time for the composition measurement, and what offline reference method will be used for calibration? *Why it matters:* This sets the go/no-go criteria for the feasibility experiment and determines whether a full-spectrum analyzer or a simplified sensor is appropriate. *(affects: method, status)*

## Recommendation

- **R1 · Primary candidate: NIR + MIR + Raman (combination: a hypothesis to test), diffuse reflection.** NIR diffuse reflection is the most common online fiber-probe method and is shown in a source example for polymer extrusion control. It can work with glass optics and remote fiber probes, and it is suitable for scattering or opaque melts. The technique is conditional on the melt being scattering or opaque. *Conditions:* Melt is scattering or opaque; target analyte has NIR-active bands; temperature and fouling are compatible with the probe. [4: S01 p.10] [5: S02 p.14] [6: S01 p.5]
- **R2 · Comparison candidate: MIR, ATR.** MIR-ATR provides a chemical fingerprint with well-defined bands and is shown in a source example for polymer extrusion control. It is suitable for liquids, pastes, and soft solids in tight contact with the ATR crystal. It is conditional on the melt being a liquid, paste, or soft solid and on the probe surviving the temperature and fouling. *Conditions:* Melt is a liquid, paste, or soft solid; ATR crystal and probe materials are compatible with the melt temperature and chemistry; fouling can be managed. [7: S01 p.9] [8: S02 p.14] [9: S01 p.10]
- **R3 · Conditional candidate: Raman, raman probe.** Raman is a vibrational method that can provide complementary information to NIR and MIR, and it is used in pharmaceutical blend monitoring. It is conditional on the melt not exhibiting strong fluorescence and on the target analyte having a usable Raman signal. *Conditions:* Melt does not exhibit strong fluorescence; target analyte has a usable Raman signal; probe can withstand the process conditions. [10: S01 p.11] [11: S01 p.15]
- **R4 · Not recommended: NIR, transmission transflection.** NIR transmission or transflection is not recommended as a primary option because a hot polymer melt is likely to be too thick, opaque, or scattering for light to penetrate. This is a clear expectation to rule out unless the melt is confirmed to be transparent. *Conditions:* Only if the melt is confirmed to be transparent or semi-transparent with a controlled pathlength. [12: S01 p.18] [13: S01 p.18]

## Measurement concept

- **Probe and geometry:** For a first comparison, test NIR diffuse reflection and MIR-ATR as the two most likely single-method candidates. If the melt is scattering or opaque, use a NIR reflection probe flush-mounted or inserted into the extruder barrel or die. If the melt is a liquid, paste, or soft solid and can contact a crystal, use a MIR-ATR probe. Raman is a conditional third method if fluorescence is not prohibitive.
- **Location:** The source example shows a NIR probe in the extruder barrel and a MIR-ATR probe for polymer extrusion. The exact location must be confirmed with the customer.
- **Fiber link:** NIR can use silica fibers. MIR requires chalcogenide, polycrystalline, or hollow waveguide fibers. No source states an achievable MIR link length, so the distance to the analyzer is an open question. [14: S02 p.14] [15: S02 p.6] [16: S02 p.6]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber, and probe actually selected. [17: S01 p.10]
- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber, and probe actually selected. [18: S01 p.9]
- **Raman:** Raman shift is reported in cm-1; the laser excitation wavelength must be stated separately. The source example for pharmaceutical monitoring uses 785 nm excitation. [19: S01 p.15]

## Risks and uncertainty

- The melt may be too hot or too fouling for any contact probe, especially MIR-ATR, which requires tight contact and samples only a surface layer a few micrometres deep. *(rules: R-MIR-2, R-MIR-3)* [20: S01 p.13]
- NIR bands are broad and overlapping, so a chemometric calibration is required and is specific to the matrix. Any change in polymer grade, API form, or additives may require re-validation. *(rules: R-NIR-2, R-CAL-1)* [21: S01 p.10]
- Raman may be swamped by fluorescence from the polymer or additives, and the signal is weak. *(rules: R-RAM-1)* [22: S01 p.11]
- The MIR fiber link length is unknown from the sources. If the analyzer must be far from the hot process point, MIR may be impractical. *(rules: R-FIB-2)* [23: S02 p.7]
- The source example for polymer extrusion is a business/application slide, not a peer-reviewed study. It is a reason to test, not proof that the method will work for this customer. *(rules: R-EVI-2)* [24: S02 p.14]

## First feasibility experiment

1. **Collect representative samples of the hot polymer melt across the expected range of composition, including different API concentrations, polymer grades, and process temperatures.** Ensure the calibration and comparison cover the expected chemical and physical variation. *(no verified source: engineering judgement)*
2. **Obtain independent reference measurements for the target analyte using the customer's offline assays on the same samples.** Provide a ground truth for calibration and validation. *(no verified source: engineering judgement)*
3. **Measure the samples with single methods first: NIR diffuse reflection, MIR-ATR, and Raman (if fluorescence is not prohibitive).** Compare the best single method before testing combinations. *(no verified source: engineering judgement)*
4. **Build chemometric calibration models for each single method and validate them on held-out runs or batches.** Assess predictive performance and avoid overfitting. *(no verified source: engineering judgement)*
5. **If no single method meets the target, test combinations such as NIR + Raman or NIR + MIR, with synchronized sampling location and timing.** Test the hypothesis that combining methods provides a gain over the best single method. [25: S01 p.7]
6. **Define go/no-go criteria based on the customer's required accuracy, precision, and response time, using the independent reference measurements.** Provide a numerical basis for deciding whether to proceed to a process installation. *(no verified source: engineering judgement)*

**Reference measurements:** The customer's offline assays will serve as the independent reference method. The specific assay and its uncertainty must be confirmed.

**Decision basis:** The go/no-go decision will be based on the customer's required accuracy, precision, and response time, compared against the validated chemometric model predictions on held-out samples.

## Assumptions

- The melt is a scattering or opaque polymer, making NIR diffuse reflection the primary candidate.
- The melt is a liquid, paste, or soft solid, making MIR-ATR a viable comparison.
- The target analyte has a usable spectral signal in at least one of the candidate methods.
- The probe and fiber materials can withstand the melt temperature and fouling conditions.
- The distance from the measurement point to the analyzer is compatible with the fiber link.

## Not covered by the supplied sources

- Temperature ratings for probes or fibers in hot polymer extrusion
- Fouling or build-up performance of probes in this application
- Achievable MIR fiber link length for process installations
- Specific API or polymer spectral data for this customer
- Accuracy, detection limits, or response times for this application

## Evidence (verified quotes)

1. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
2. ✓ **S02 p.14** (application precedent): "Hot Melt Extruder"
3. ✓ **S02 p.13** (general): "ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing"
4. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
5. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
6. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics, as well as standard lamps as light sources, making it ideal for online applications, including remote measurements via fiber optic probes."
7. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
8. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
9. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
10. ✓ **S01 p.11** (general): "Raman spectroscopy is based on recording weak radiation signals observed when a sample is irradiated by a laser or high-power LED, typically in the visible light range."
11. ✓ **S01 p.15** (method gain): "The combination of these techniques is particularly effective because it captures complementary chemical information: NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups."
12. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
13. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
14. ✓ **S02 p.14** (application precedent): "Extruder barrel"
15. ✓ **S02 p.6** (general): "Standard VIS-NIR Silica Fibers"
16. ✓ **S02 p.6** (general): "Chalcogenide As-S IR Fibers"
17. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
18. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
19. ✓ **S01 p.15** (performance figure): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
20. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns"
21. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
22. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
23. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
24. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
25. ✓ **S01 p.7** (method gain): "This often provides a synergistic effect, allowing one to solve a problem that either method alone cannot handle or only partially."

## Verification

- Citations verified: 25 of 26 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 1; soft warnings: 6; repair rounds: 2.
- Removed 1 citation(s) that failed verification:
  - ⚠ measurement_concept.citations[0]: S02 p.14 "NIR probe"
- Removed 3 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry

*Run D07 · models deepseek/deepseek-v4-pro-0813 · cost $0.0550*
