# First technical assessment

**Customer enquiry**

> We want to follow ethanol in a clear aqueous fermentation broth that flows through a pipe. Gas chromatography results from the lab are available as reference.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for ethanol in a clear aqueous fermentation broth, but several assumptions about concentration range, matrix composition, and installation conditions remain open.

## Requirements

**Stated by the customer**

- follow ethanol in a clear aqueous fermentation broth flowing through a pipe
- gas chromatography results from the lab are available as reference

**Key unknowns**

- ethanol concentration range
- other absorbing species in the broth
- temperature and pressure in the pipe
- installation point and distance
- required accuracy and response time
- cleaning and fouling conditions
- optical path length available

## Clarification questions (most decision-relevant first)

Q1. What is the expected ethanol concentration range in the broth? *Why it matters:* This determines whether NIR sensitivity is sufficient or whether a more sensitive method is needed. NIR may lack sensitivity for trace components in a bioprocess context. *(affects: method, technique, go_no_go_criteria)*
Q2. What other absorbing species are present in the broth, and do their concentrations vary? *Why it matters:* NIR bands are broad and overlapping; other species can interfere with ethanol quantification and require a chemometric calibration specific to the matrix. *(affects: method, calibration, feasibility)*
Q3. What is the temperature and pressure in the pipe at the intended measurement point? *Why it matters:* Temperature affects spectral features and probe compatibility; pressure affects probe installation and sealing. *(affects: installation, probe_selection)*
Q4. What is the distance between the intended measurement point and the spectrometer location? *Why it matters:* Fiber length limits depend on the fiber family. Long cables are stated only for low-OH silica fibers; MIR fiber link length is an open question. *(affects: method, fiber_selection, installation)*
Q5. What accuracy and response time are required for the ethanol measurement? *Why it matters:* This determines whether a full-spectrum method or a simplified sensor approach is appropriate, and sets the go/no-go criteria. *(affects: method, go_no_go_criteria)*
Q6. What are the cleaning and fouling conditions at the measurement point? *Why it matters:* ATR probes sample only a surface layer a few micrometres deep, so deposits on the crystal are a risk. Transmission probes may also foul. *(affects: technique, installation, maintenance)*
Q7. What optical path length is available in the pipe for a transmission or transflection measurement? *Why it matters:* NIR transmission requires a controlled pathlength; too wide loses signal to absorption, too narrow samples a negligible volume. *(affects: technique, installation)*

## Recommendation

- **R1 · Primary candidate: NIR, transmission transflection.** NIR transmission or transflection is the preferred geometry for transparent or semi-transparent liquids. The sample is stated as clear and aqueous, and ethanol has characteristic NIR absorption bands. NIR penetrates up to several millimetres, works with glass optics and standard lamps, and suits remote fiber-probe measurement. *Conditions:* Applies if the ethanol concentration is above the NIR sensitivity limit and the broth remains clear enough for transmission. Requires a controlled optical pathlength. [1: S01 p.18] [2: S01 p.5] [3: S01 p.10]
- **R2 · Comparison candidate: Raman, raman probe.** Raman is well suited to aqueous media because water interferes less than in infrared methods. Ethanol has a distinct Raman spectrum. Raman can be used for quantitative analysis of mixtures. *Conditions:* Applies if fluorescence background from the broth is manageable and the ethanol concentration is within the Raman detection range. Requires a Raman spectrometer and probe. [4: S01 p.16]
- **R3 · Conditional candidate: MIR, ATR.** MIR ATR can provide well-defined absorption bands for ethanol and is suitable for liquids in contact with the ATR crystal. It may be useful if NIR sensitivity or selectivity is insufficient. *Conditions:* Applies only if the broth is compatible with ATR contact, fouling is manageable, and the MIR fiber link length is feasible. MIR requires chalcogenide or polycrystalline fibers, not silica. [5: S01 p.9] [6: S01 p.10]
- **R4 · Not recommended: UV-Vis, transmission transflection.** UV-Vis transmission is possible for clear liquids, but ethanol has no strong, specific UV-Vis absorption that would allow selective quantification in a complex fermentation broth. UV-Vis signals of mixtures overlap strongly and selectivity is low. *Conditions:* Not recommended as a primary method for ethanol quantification. [7: S01 p.5]
- **R5 · Not recommended: Fluorescence, fluorescence probe.** Fluorescence only measures species that fluoresce or a justified fluorescent indicator. Ethanol is not a fluorescent species, and no fluorescent indicator has been identified. *Conditions:* Not recommended unless a fluorescent indicator specific to ethanol is identified. [8: S01 p.5]

## Measurement concept

- **Probe and geometry:** For NIR transmission/transflection: a transmission or transflection probe inserted into the pipe, with a controlled optical pathlength. For Raman: a Raman probe in contact with the flowing broth. For MIR ATR: an ATR probe in contact with the broth.
- **Location:** In the pipe, at a point where the broth is representative and well-mixed.
- **Fiber link:** For NIR and Raman: silica fibers are suitable. For MIR: chalcogenide or polycrystalline fibers are required; link length is an open question. [9: S01 p.18] [10: S02 p.6] [11: S02 p.6]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [12: S01 p.10]
- **Raman:** Raman shift is reported in cm-1; the laser excitation wavelength must be stated separately. No specific excitation wavelength is proposed here. [13: S01 p.11]
- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber and probe actually selected. [14: S01 p.9]

## Risks and uncertainty

- NIR sensitivity may be insufficient if ethanol is a trace component. *(rules: R-NIR-4)* [15: S01 p.16]
- Other absorbing species in the broth may interfere with ethanol quantification. *(rules: R-NIR-2, R-CAL-1)* [16: S01 p.10]
- Fouling or deposits on the probe may affect the measurement, especially for ATR. *(rules: R-MIR-3)* [17: S01 p.13]
- The broth may not remain clear during fermentation; turbidity or bubbles could affect transmission measurements. *(rules: R-GEN-5)* [18: S01 p.7]
- Raman fluorescence background from the broth may swamp the ethanol signal. *(rules: R-RAM-1)* [19: S01 p.11]

## First feasibility experiment

1. **Collect representative broth samples across the expected ethanol concentration range and fermentation stages.** To cover the expected chemical and physical variation. [20: REF §3]
2. **Measure each sample with the primary method (NIR transmission/transflection) and the comparison method (Raman) using the intended probe geometry.** To obtain spectral data for calibration and method comparison. *(no verified source: engineering judgement)*
3. **Obtain independent reference ethanol concentrations for the same samples using gas chromatography.** To provide reference values for calibration and validation. *(no verified source: engineering judgement)*
4. **Build chemometric calibration models for each single method (NIR and Raman) using the reference GC data.** To establish single-method performance. [21: S01 p.10]
5. **Validate the models on held-out runs or batches not used in calibration.** To assess prediction performance on independent data. *(no verified source: engineering judgement)*
6. **Compare the validated performance of NIR and Raman against the customer's required accuracy.** To select the best single method. *(no verified source: engineering judgement)*
7. **If neither single method meets the requirement, test a combination of NIR and Raman with synchronized data fusion.** To test the hypothesis that combining methods improves accuracy. [22: S01 p.7]

**Reference measurements:** Gas chromatography results from the lab.

**Decision basis:** The go/no-go decision should be based on the customer's required accuracy and response time for ethanol monitoring. The numerical criteria must come from the customer.

## Assumptions

- The broth remains clear enough for transmission measurements during the entire fermentation.
- Ethanol is present at a concentration above the NIR sensitivity limit.
- The measurement point is representative and well-mixed.
- The fiber link length is within the capability of the selected fiber family.

## Not covered by the supplied sources

- Ethanol concentration range in the customer's broth
- Other absorbing species in the broth
- Temperature and pressure in the pipe
- Required accuracy and response time
- Cleaning and fouling conditions
- Optical path length available
- Achievable MIR fiber link length
- Specific ethanol detection limits for NIR or Raman in fermentation broth

## Evidence (verified quotes)

1. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
2. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics, as well as standard lamps as light sources, making it ideal for online applications, including remote measurements via fiber optic probes."
3. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups, such as -OH, -NH2=NH, -CH3, =CH2, ≥CH, etc., found in many organic and inorganic compounds."
4. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
5. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
6. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
7. ✓ **S01 p.5** (general): "However, the strong overlap of spectral signals in UV spectra complicates the analysis of real samples and makes the use of chemometric algorithms a necessary component of qualitative mixture analysis methods."
8. ✓ **S01 p.5** (general): "Another highly sensitive method, UV/Vis fluorimetry, is based on the secondary emission of excited molecules of certain substances, most often of biological origin. However, most chemicals do not exhibit this property."
9. ✓ **S01 p.18** (general): "The setup typically consists of a transmission / transflection probe, where light passes entirely through a defined layer of the sample to a detector on the opposite side."
10. ✓ **S02 p.6** (general): "Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
11. ✓ **S02 p.6** (general): "Chalcogenide As-S IR Fibers 6500 nm"
12. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
13. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
14. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
15. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
16. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
17. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns, providing information on molecular composition and biochemical changes."
18. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
19. ✓ **S01 p.11** (general): "Furthermore, observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
20. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
21. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
22. ✓ **S01 p.7** (method gain): "This often provides a synergistic effect, allowing one to solve a problem that either method alone cannot handle or only partially."

## Verification

- Citations verified: 22 of 24 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 2; soft warnings: 4; repair rounds: 2.
- Removed 2 citation(s) that failed verification:
  - ⚠ recommendations[1].citations[1]: S01 p.12 "The Raman signal's dependence on concentration is linear over a wide range of intensities."
  - ⚠ feasibility_plan.steps[4].citations[0]: REF p.3 "Validation on held-out runs or batches."
- Removed 3 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.sample.fluorophore: slot value without a verbatim enquiry quote; reset to unknown

*Run 20261017T072405Z-d7ba65 · models deepseek/deepseek-v4-pro-0813 · cost $0.0642*
