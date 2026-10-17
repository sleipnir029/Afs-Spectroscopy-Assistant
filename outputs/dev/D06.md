# First technical assessment: Water content in a petroleum stream

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Insufficient information for a method choice. The customer's central premises are plausible but not yet supported by the supplied sources for this specific petroleum stream. The physical state, optical regime, water concentration range, and installation distance are unknown, so no method can be justified as primary without clarification. A conditional shortlist is given with explicit assumptions.

## Premise check

- **Supported:** A fiber based measurement closer to the process will allow changes to be noticed sooner.. The sources state that fiber optic probes enable on-site online analysis and near real-time results, and that online analysis eliminates delays from sampling. [1: S01 p.2] [2: S01 p.3]
- **Supported:** The analyzer can be located outside the process area while the measurement is made closer to the process.. The sources state that fiber optics allow spectrometers to be located away from the process point, and that long silica fiber cables enable remote industrial process control. [3: S01 p.15] [4: S02 p.7]
- **Supported:** A first comparison experiment should be performed before selecting equipment.. The sources describe a guided pathway that begins with multi-method laboratory trials to select the best method before choosing a solution. [5: S02 p.20] [6: S01 p.3]

## Requirements

**Stated by the customer**

- Water determination in a petroleum stream
- Fiber-based measurement closer to the process
- Analyzer outside the process area
- Earlier detection of changes
- Clarification questions and first comparison experiment design before equipment selection

**Key unknowns**

- Physical state and optical regime of the petroleum stream (transparent, opaque, scattering, single-phase or multiphase)
- Water concentration range and required accuracy
- Whether water is dissolved, emulsified, or free water
- Matrix composition and potential interferences
- Temperature and pressure at the measurement point
- Distance from the process point to the analyzer location
- Required response time and measurement frequency
- Reference method and its uncertainty
- Fouling and cleaning considerations at the measurement point

## Clarification questions (most decision-relevant first)

Q1. What is the physical state and optical appearance of the petroleum stream at the intended measurement point? Is it transparent, opaque, highly scattering, or multiphase? *Why it matters:* This determines whether transmission/transflection, diffuse reflection, or ATR geometry is viable. Transmission fails for opaque or highly scattering samples; reflection is less representative for clear liquids; ATR requires tight contact with liquids, pastes, or soft solids. *(affects: method, technique, installation)*
Q2. What is the expected water concentration range and the required accuracy and response time for the measurement? *Why it matters:* NIR may lack sensitivity for trace components in some contexts. MIR-ATR has been shown for water in petroleum in a laboratory example, but the usable range depends on the actual configuration. The required response time affects whether a full-spectrum analyzer or a simpler sensor is appropriate. *(affects: method, status)*
Q3. Is the water dissolved, emulsified, or present as free water? What is the matrix composition and are there known interferences? *Why it matters:* The water state and matrix affect which spectral features are informative and whether a chemometric calibration is needed. Different methods respond differently to dissolved versus emulsified water. *(affects: method, technique)*
Q4. What is the distance from the intended measurement point to the analyzer location, and what are the temperature and pressure conditions at the measurement point? *Why it matters:* Long cables are stated only for low-OH silica fibers, which do not transmit MIR light. MIR fiber link length is not stated in the sources and is an open question for AFS. Temperature and pressure affect probe compatibility and installation. *(affects: method, installation, status)*
Q5. What is the current laboratory reference method for water determination and its uncertainty? *Why it matters:* The first comparison experiment needs an independent reference measurement to establish accuracy. Without knowing the reference method and its uncertainty, no go/no-go criterion can be set. *(affects: feasibility_plan)*

## Recommendation

- **R1 · Conditional candidate: MIR, ATR.** MIR-ATR is the most directly relevant method in the supplied sources for water in petroleum. A laboratory example shows ATR probe spectra of petroleum with different water contents. MIR has well-defined bands and high selectivity. This is conditional on the stream being a liquid, paste, or soft solid that can make tight contact with the ATR crystal, and on the MIR fiber link length being feasible for the customer's installation. *Conditions:* The stream is a liquid or soft solid suitable for ATR contact; the MIR fiber link length is confirmed as feasible by AFS; the water concentration range is within the demonstrated laboratory example or can be calibrated. [7: S02 p.13] [8: S02 p.13] [9: S01 p.9]
- **R2 · Conditional candidate: NIR, transmission transflection.** NIR is the most common online analysis method with fiber optic probes and works with standard silica fibers, which can support long cable runs. Transmission or transflection is the preferred geometry for transparent or semi-transparent liquids. This is conditional on the petroleum stream being sufficiently transparent for a controlled pathlength. *Conditions:* The stream is transparent or semi-transparent at the measurement point; the water concentration is above the NIR sensitivity limit; the pathlength can be controlled. [10: S01 p.10] [11: S01 p.18] [12: S01 p.5]
- **R3 · Conditional candidate: NIR, diffuse reflection.** NIR diffuse reflection suits opaque, concentrated, or scattering samples. If the petroleum stream is opaque or highly scattering, this geometry may be more appropriate than transmission. This is conditional on the stream being opaque or scattering. *Conditions:* The stream is opaque, concentrated, or highly scattering; physical variation is controlled or corrected with scatter correction. [13: S01 p.17] [14: S01 p.6]
- **R4 · Not recommended: Raman, raman probe.** Raman is not recommended as a primary method for water determination in petroleum. Water is a weak Raman scatterer, and the sources do not show a Raman example for water in petroleum. Raman is better suited to aqueous media where water interferes less than in infrared methods, which is the opposite of the customer's need to measure water in a non-aqueous matrix. *Conditions:* Not applicable. [15: S01 p.16]
- **R5 · Not recommended: Fluorescence, fluorescence probe.** Fluorescence is not recommended for water determination in petroleum. Fluorescence only measures species that fluoresce, and most chemicals do not. Water does not fluoresce, and no fluorescent indicator has been identified for this application. *Conditions:* Not applicable. [16: S01 p.5]

## Measurement concept

- **Probe and geometry:** Conditional on the stream's optical regime. If the stream is a transparent or semi-transparent liquid, NIR transmission or transflection with a controlled pathlength is the preferred geometry. If the stream is opaque or highly scattering, NIR diffuse reflection is preferred. If the stream is a liquid or soft solid suitable for tight contact, MIR-ATR is the most directly relevant method for water in petroleum.
- **Location:** Closer to the process, at a point where the stream is representative and the probe can be installed with appropriate contact or pathlength control.
- **Fiber link:** For NIR, standard silica fibers can support long cable runs. For MIR, the fiber link length is an open question and must be confirmed with AFS. [17: S01 p.18] [18: S02 p.7]

## Spectral range

- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber, and probe actually selected. [19: S01 p.9]
- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber, and probe actually selected. [20: S01 p.10]

## Risks and uncertainty

- The physical state and optical regime of the petroleum stream are unknown. If the stream is opaque or highly scattering, transmission will fail; if it is clear, reflection may be less representative. *(rules: R-GEO-2, R-GEO-4)* [21: S01 p.18]
- The water concentration range is unknown. NIR may lack sensitivity for trace components in some contexts. If the customer needs trace water determination, NIR may be insufficient. *(rules: R-NIR-4)* [22: S01 p.16]
- The MIR fiber link length is not stated in the sources. If the analyzer must be far from the process point, MIR may not be feasible with the available fiber technology. *(rules: R-FIB-2)* [23: S02 p.7]
- ATR requires tight contact and samples only a surface layer a few micrometres deep. Fouling or deposits on the crystal could bias the measurement. *(rules: R-MIR-3)* [24: S01 p.13]
- NIR and Raman calibrations are specific to the matrix. If the petroleum stream composition changes, the calibration must be re-validated or rebuilt. *(rules: R-CAL-1)* *(no verified source: engineering judgement)*
- The laboratory example of water in petroleum by MIR-ATR is a reason to test, not proof that it will work for this customer's stream. The actual performance depends on the specific matrix and installation. *(rules: R-EVI-2)* [25: S02 p.13]

## First feasibility experiment

1. **Collect representative samples of the petroleum stream across the expected range of water concentrations, including the physical states and matrix variations that occur in the process.** Ensure the experiment covers the expected chemical and physical variation. *(no verified source: engineering judgement)*
2. **Measure each sample with the candidate single methods first: MIR-ATR, NIR transmission/transflection, and NIR diffuse reflection, depending on the sample's optical regime.** Compare single methods before testing combinations. *(no verified source: engineering judgement)*
3. **Obtain independent reference water measurements for each sample using the customer's current laboratory method, with known uncertainty.** Provide the ground truth for calibration and validation. *(no verified source: engineering judgement)*
4. **Build chemometric calibration models for each method and validate them on held-out runs or batches, not just on the calibration samples.** Avoid overfitting and estimate real prediction performance. *(no verified source: engineering judgement)*
5. **Compare the prediction accuracy of each method against the reference method. If no single method meets the customer's accuracy requirement, test a combination of methods as a hypothesis.** Determine whether a single method is sufficient or a combination is needed. *(no verified source: engineering judgement)*
6. **Set a go/no-go criterion based on the customer's required accuracy and response time. For example, the method must achieve a specified maximum prediction error for water concentration on held-out samples.** Provide a numerical basis for the go/no-go decision. *(no verified source: engineering judgement)*

**Reference measurements:** The customer's current laboratory water determination method, with its uncertainty documented.

**Decision basis:** The go/no-go criterion must come from the customer's required accuracy and response time. The sources do not provide a universal accuracy figure for water in petroleum, so the criterion must be set by the customer based on their process needs.

## Assumptions

- The petroleum stream is a liquid at the measurement point.
- The water concentration is in a range that can be detected by at least one of the candidate methods.
- The analyzer can be located within a feasible fiber link distance from the process point.
- The customer's current laboratory method provides a reliable reference for water determination.

## Not covered by the supplied sources

- The specific water concentration range and required accuracy for this customer's petroleum stream
- The physical state and optical regime of this customer's petroleum stream
- The achievable MIR fiber link length for this installation
- The temperature and pressure ratings of specific probes for this application
- The customer's current laboratory reference method and its uncertainty
- Any performance figures for water determination in petroleum beyond the laboratory example shown on S02 p.13

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "Fiber optic probes and cells are being integrated into reactors and production lines of ongoing technological processes, enabling on-site online analysis and obtaining results in near real time."
2. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
3. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
4. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
5. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
6. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
7. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"
8. ✓ **S02 p.13** (performance figure): "Pure Oil | 0.1% Water | 0.5% Water | 1.0% Water | 2.0% Water"
9. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
10. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
11. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
12. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics, as well as standard lamps as light sources, making it ideal for online applications, including remote measurements via fiber optic probes."
13. ✓ **S01 p.17** (general): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
14. ✓ **S01 p.6** (general): "Diffuse reflection-probe diffuse reflection Scattering media, powder 0.5-1 mm"
15. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
16. ✓ **S01 p.5** (general): "However, most chemicals do not exhibit this property."
17. ✓ **S01 p.18** (general): "The key experimental action is the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
18. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
19. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
20. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
21. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
22. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
23. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
24. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns, providing information on molecular composition and biochemical changes."
25. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"

## Verification

- Citations verified: 25 of 25 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 3; repair rounds: 1.
- Removed 2 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry

*Run D06 · models deepseek/deepseek-v4-pro-0813 · cost $0.0413*
