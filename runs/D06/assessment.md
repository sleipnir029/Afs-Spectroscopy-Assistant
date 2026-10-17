# First technical assessment: Water content in a petroleum stream

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for water in a petroleum stream, with explicit assumptions. The strongest source-supported candidate is MIR ATR, with Raman as a comparison. NIR and UV-Vis remain conditional because the optical regime of the stream is unknown. Fluorescence is not recommended for direct water determination.

## Premise check

- **Supported:** A fiber-based measurement closer to the process will allow changes to be noticed sooner than laboratory sampling.. The sources state that fiber optic probes enable on-site online analysis and near real-time results, eliminating sampling delays. [1: S01 p.2] [2: S01 p.3]
- **Supported:** The analyzer can be located outside the process area while the measurement is made closer to the process.. Fiber optics allow the spectrometer to be located away from the process point. However, the achievable distance depends on the fiber type and method; long cables are stated only for low-OH silica fibers, not for MIR fibers. [3: S01 p.15] [4: S02 p.7]
- **Supported:** A first comparison experiment should be planned before selecting equipment.. The AFS guided pathway and the laboratory concept both describe multi-method trials on representative samples as the first step to select the best method. [5: S02 p.20] [6: S01 p.3]

## Requirements

**Stated by the customer**

- Water determination in a petroleum stream
- Fiber-based measurement closer to the process
- Analyzer outside the process area
- Earlier change detection than laboratory sampling
- Clarification questions and first comparison experiment design before equipment selection

**Key unknowns**

- Water concentration range and required accuracy
- Matrix composition and potential interferences
- Optical behavior of the petroleum stream (transparent, opaque, scattering)
- Temperature and pressure at the measurement point
- Installation point and distance from analyzer
- Cleaning and fouling considerations
- Required response time
- Reference method details and sampling protocol

## Clarification questions (most decision-relevant first)

Q1. What is the expected water concentration range and the required accuracy or detection limit? *Why it matters:* This determines whether NIR is viable at all. The sources state NIR may lack sensitivity for trace components in a bioprocess context; the equivalent limit for water in petroleum is unknown and must be established. MIR ATR is more sensitive but the calibration range must match the process. *(affects: method_choice, go_no_go_criteria)*
Q2. What is the composition of the petroleum stream? Specifically, what other components are present (e.g., hydrocarbons, additives, dissolved gases) and do any of them absorb in the same spectral regions as water? *Why it matters:* Interferences determine whether a single method can resolve water or whether a combination is needed. MIR ATR has well-defined bands and high selectivity, but overlapping bands from other components could still require chemometric separation. *(affects: method_choice, calibration_design)*
Q3. What is the optical behavior of the stream? Is it transparent, opaque, highly scattering, or does it contain particulates or emulsions? *Why it matters:* This decides the measurement geometry. Transmission or transflection requires a transparent or semi-transparent liquid; diffuse reflection suits opaque or scattering samples; ATR requires tight contact and suits liquids, pastes and soft solids. The wrong geometry will fail. *(affects: technique_choice, probe_selection)*
Q4. What are the temperature and pressure at the proposed measurement point, and what is the process environment (e.g., hazardous area classification, vibration, dust)? *Why it matters:* Probe and fiber materials must withstand the process conditions. The analyzer location outside the process area is supported, but the fiber link length and routing depend on the distance and environment. No source states an achievable length for an MIR fiber link. *(affects: installation, fiber_selection, probe_selection)*
Q5. What is the distance between the proposed measurement point and the analyzer location, and what fiber routing constraints exist? *Why it matters:* Long cables are stated only for low-OH silica fibers. MIR fibers and hollow waveguides are shown only at laboratory lengths. If the distance is large, MIR may be impractical and NIR or Raman may be preferred. *(affects: method_choice, fiber_selection, installation)*
Q6. What is the current laboratory reference method for water determination, and what is its accuracy and sampling protocol? *Why it matters:* The reference method defines the independent values for calibration and validation. Without a reliable reference, no chemometric model can be built or validated. *(affects: feasibility_experiment, calibration_design)*
Q7. What is the required response time for detecting a change in water content? *Why it matters:* This determines whether a full-spectrum analyzer or a simplified sensor is appropriate, and whether data acquisition speed is a constraint. Online measurements require high-speed spectral acquisition, but the required speed depends on the process dynamics. *(affects: instrument_selection, go_no_go_criteria)*

## Recommendation

- **REC-1 · Primary candidate: MIR, ATR.** MIR ATR is the strongest source-supported candidate for water in petroleum. A laboratory example shows MIR-ATR spectra of water in petroleum, with well-defined absorption bands. MIR has high selectivity and ATR is the usual in-line route for liquids. *Conditions:* Requires tight contact with the liquid, a fiber that transmits MIR light (CIR or PIR), and a manageable fiber link length. The stream must be compatible with the ATR crystal material. [7: S02 p.13] [8: S01 p.9] [9: S01 p.5]
- **REC-2 · Comparison candidate: Raman, raman probe.** Raman is well suited to aqueous media because water interferes less than in infrared methods. It is a vibrational method that can provide complementary information. However, Raman signals are weak and can be swamped by fluorescence, which must be checked on real petroleum samples. *Conditions:* Requires a Raman probe and laser excitation. Fluorescence background from the petroleum matrix must be assessed. The Raman shift range and excitation wavelength must be selected for water detection. [10: S01 p.16] [11: S01 p.11] [12: S01 p.11]
- **REC-3 · Conditional candidate: NIR, transmission transflection.** NIR transmission or transflection is the preferred geometry for transparent or semi-transparent liquids. NIR works with silica fibers, which support long cable runs, making it attractive for remote analyzer placement. However, NIR bands are broad and overlapping, and sensitivity for trace water may be insufficient. *Conditions:* Applies only if the petroleum stream is transparent or semi-transparent and the water concentration is above the NIR sensitivity limit. The optical pathlength must be controlled. [13: S01 p.18] [14: S02 p.7] [15: S01 p.10] [16: S01 p.16]
- **REC-4 · Conditional candidate: NIR, diffuse reflection.** NIR diffuse reflection suits opaque, concentrated or scattering samples. If the petroleum stream is opaque or contains scattering particulates, this geometry may be appropriate. *Conditions:* Applies only if the stream is opaque or highly scattering. Reflection signals are sensitive to surface characteristics and particle size, so physical variation can mimic composition change. [17: S01 p.17] [18: S01 p.17]
- **REC-5 · Not recommended: Fluorescence, fluorescence probe.** Fluorescence only measures species that fluoresce or a justified fluorescent indicator. Water does not fluoresce, and no fluorescent indicator has been identified for this application. Most chemicals do not exhibit fluorescence. *Conditions:* Would only apply if a fluorescent water-sensitive indicator were added to the stream, which is not stated and would require separate justification. [19: S01 p.5] [20: S04 p.4]
- **REC-6 · Not recommended: UV-Vis, ATR.** UV-Vis ATR is technically possible but water determination in petroleum by UV-Vis is not supported by any source. UV-Vis has low selectivity and overlapping signals in mixtures, making it a poor candidate for water in a complex petroleum matrix without a specific absorption feature. *Conditions:* Would only apply if a specific UV-Vis absorption feature for water or a water-related species were identified in the petroleum matrix. [21: S01 p.5]

## Measurement concept

- **Probe and geometry:** For MIR ATR: an immersion ATR probe with a ZrO2 or diamond crystal tip in direct contact with the flowing petroleum stream. The probe is inserted into the process line or reactor. For Raman: a Raman fiber probe in contact with the stream. For NIR transmission/transfection: a transmission or transflection probe with a controlled optical pathlength inserted into the stream.
- **Location:** At a point in the process where the water content is representative and where changes are expected to be detected. The exact location depends on the process flow and mixing characteristics.
- **Fiber link:** For MIR: CIR or PIR fiber, length to be confirmed with AFS. For Raman and NIR: silica fiber, with long runs stated for low-OH silica fibers. [22: S01 p.10] [23: S01 p.18]

## Spectral range

- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber and probe actually selected. For water in petroleum, the relevant absorption bands must be identified from the measured spectra. [24: S01 p.9]
- **Raman:** Raman shift is reported in cm-1. The laser excitation wavelength must be stated separately. The relevant Raman shift range for water must be identified from the measured spectra. [25: S01 p.11]
- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [26: S01 p.10]

## Risks and uncertainty

- The petroleum stream may be opaque or highly scattering, making transmission or transflection NIR impossible and requiring diffuse reflection or ATR instead. *(rules: R-GEO-2)* [27: S01 p.18]
- The water concentration may be below the sensitivity limit of NIR, making MIR ATR or Raman the only viable options. *(rules: R-NIR-4)* [28: S01 p.16]
- The MIR fiber link length may be too short for the required distance between the measurement point and the analyzer. No source states an achievable length for an MIR link. *(rules: R-FIB-2)* [29: S02 p.7]
- Fouling or deposits on the ATR crystal can change the measured surface and bias the water determination. ATR samples only a surface layer a few micrometres deep. *(rules: R-MIR-3)* [30: S01 p.13]
- Raman signals may be swamped by fluorescence from the petroleum matrix, making water detection impossible without special filters or probe designs. *(rules: R-RAM-1)* [31: S01 p.11]
- The calibration may not transfer if the petroleum matrix composition changes. NIR and Raman calibrations are specific to the matrix and must be re-validated on new material. *(rules: R-CAL-1)* [32: S01 p.10]
- Sample inhomogeneity or process turbulence at the measurement point may make the measurement unrepresentative of the bulk stream. *(rules: R-GEN-5)* [33: S01 p.7]

## First feasibility experiment

1. **Collect representative samples** Cover the expected range of water concentrations and the expected variation in petroleum matrix composition. Include samples from different batches or process conditions. [34: S01 p.3]
2. **Measure independent reference values** Use the customer's current laboratory water determination method on the same samples to obtain reference water concentrations. The reference method must be reliable and its accuracy known. *(no verified source: engineering judgement)*
3. **Acquire spectra with single methods first** Measure MIR ATR spectra, Raman spectra, and NIR transmission/transfection or diffuse reflection spectra (depending on the optical regime) on the same samples. Do not combine methods yet. [35: S01 p.3]
4. **Build and validate single-method calibration models** Use chemometric methods (e.g., PLS regression) to relate spectra to reference water concentrations. Validate on held-out runs or batches, not just random subsets of the same batch. [36: S01 p.2]
5. **Compare single-method performance** Compare the prediction accuracy of MIR ATR, Raman, and NIR (if applicable) against the reference values. Select the best single method based on the go/no-go criteria. *(no verified source: engineering judgement)*
6. **Test combinations only if no single method is sufficient** If no single method meets the accuracy requirement, test combinations (e.g., MIR ATR + Raman) as a hypothesis. Compare the combination against the best single method. [37: S01 p.7]

**Reference measurements:** The customer's current laboratory water determination method, applied to the same samples used for spectral acquisition. The reference method must be independent of the optical methods being tested.

**Decision basis:** The go/no-go criteria must be defined by the customer based on their required accuracy and response time. A method passes if its validated prediction error on held-out samples is within the customer's required accuracy for water determination. If no method meets the criteria, the investigation should either expand the sample set, test combinations, or conclude that fiber-based measurement is not suitable for this application.

## Assumptions

- The petroleum stream is a liquid at the measurement point.
- The water concentration is within a range detectable by at least one of the candidate methods.
- The stream is compatible with the probe materials (e.g., no aggressive solvents that would damage the ATR crystal or fiber).
- The distance between the measurement point and the analyzer is within the achievable fiber link length for the selected method.
- The customer's laboratory reference method provides sufficiently accurate water concentrations for calibration.

## Not covered by the supplied sources

- Achievable MIR fiber link lengths for process installations
- Specific water absorption bands in petroleum for MIR, Raman, or NIR
- Detection limits for water in petroleum by any optical method
- Compatibility of ATR crystal materials with specific petroleum stream compositions
- Response times for specific water determination applications
- Any AFS product codes, prices, or component ratings

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "Fiber optic probes and cells are being integrated into reactors and production lines of ongoing technological processes, enabling on-site online analysis and obtaining results in near real time."
2. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
3. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
4. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
5. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
6. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
7. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"
8. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis. Due to the high extinction coefficients of various molecules in this region, the method is highly sensitive and can be used to analyze a wide variety of samples: solids, liquids, and gases."
9. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR) by connecting appropriate attachments and probes."
10. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
11. ✓ **S01 p.11** (general): "Measurement of the Raman scattering (RS) effect, is also a type of vibrational spectroscopy."
12. ✓ **S01 p.11** (general): "From a technical standpoint, measuring Raman spectra is hampered by the low intensity of Raman signals, which are several orders of magnitude weaker than IR absorption peaks in the IR range (when these spectra are compared in the original photon count units)."
13. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
14. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
15. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
16. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
17. ✓ **S01 p.17** (general): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
18. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
19. ✓ **S01 p.5** (general): "Another highly sensitive method, UV/Vis fluorimetry, is based on the secondary emission of excited molecules of certain substances, most often of biological origin. However, most chemicals do not exhibit this property."
20. ✓ **S04 p.4** (general): "Of course, it is limited to the samples containing at least one fluorescent component that often has a biological or natural origin."
21. ✓ **S01 p.5** (general): "the strong overlap of spectral signals in UV spectra complicates the analysis of real samples and makes the use of chemometric algorithms a necessary component of qualitative mixture analysis methods."
22. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
23. ✓ **S01 p.18** (general): "The key experimental action is the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
24. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
25. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
26. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
27. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
28. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
29. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
30. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns, providing information on molecular composition and biochemical changes."
31. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
32. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
33. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
34. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
35. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
36. ✓ **S01 p.2** (general): "This is achieved through a special branch of analytical chemistry called chemometrics, which provides chemists with a rich toolkit for constructing calibration and classification models, as well as methods for in-depth research data analysis."
37. ✓ **S01 p.7** (method gain): "This often provides a synergistic effect, allowing one to solve a problem that either method alone cannot handle or only partially."

## Verification

- Citations verified: 37 of 37 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 2; repair rounds: 1.

*Run D06 · models deepseek/deepseek-v4-pro-0813 · cost $0.0949*
