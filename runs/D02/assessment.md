# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for an opaque, concentrated milk product because the sources contain direct application precedent for inline NIR reflection on opaque dairy products and for MIR-ATR on liquids/pastes. The recommendation is conditional on open questions about installation, temperature range, and reference values.

## Premise check

- **Supported:** An initial spectroscopy concept can be provided for an opaque, concentrated milk product without further specification of the measurement geometry or optical access.. The sources describe inline NIR reflection for opaque or highly concentrated dairy products such as yogurt, butter, or whole milk concentrates, and MIR-ATR for liquids and pastes. A provisional concept can therefore be offered, with geometry and installation as open questions. [1: S01 p.17] [2: S01 p.6]
- **Supported:** A practical comparison experiment can be designed while retaining laboratory checks.. The sources describe multi-method laboratory trials as the first step of the AFS guided pathway, and the organizer guidance requires a feasibility plan with independent reference measurements. Retaining laboratory checks is consistent with this approach. [3: S02 p.20]
- **Supported:** Earlier information about composition changes is obtainable from the processing line.. The sources state that fiber optic probes are being integrated into production lines for on-site online analysis and near real time results, and that NIR is the most common online analysis method using fiber optic probes. [4: S01 p.2] [5: S01 p.10]

## Requirements

**Stated by the customer**

- Initial spectroscopy concept
- Practical comparison experiment
- Retain laboratory checks
- Earlier information about composition changes
- Targets: fat and protein

**Key unknowns**

- Target concentration ranges for fat and protein
- Temperature range and texture variation details
- Installation point and optical access on the processing line
- Distance from analyzer to measurement point
- Cleaning and fouling requirements
- Required accuracy and response time
- Reference method details for laboratory checks

## Clarification questions (most decision-relevant first)

Q1. What are the expected concentration ranges for fat and protein in this product, and what accuracy do you require relative to your laboratory reference method? *Why it matters:* This determines whether NIR is sufficient or whether a more selective method such as MIR-ATR or Raman is needed. NIR may lack sensitivity for trace components, and calibration targets must be defined for a go/no-go criterion. *(affects: method_choice, go_no_go_criteria)*
Q2. What is the temperature range at the intended measurement point, and how fast do temperature and texture change during production? *Why it matters:* Temperature affects spectral response and probe material compatibility. Rapid texture changes can alter scattering and require scatter correction or a different geometry. *(affects: technique_choice, installation)*
Q3. Where on the processing line can a probe be installed, and what is the distance from that point to where the analyzer would be located? *Why it matters:* The installation point determines whether a contact probe can be used and whether the fiber link length is feasible. MIR fiber link length is an open question; long cables are stated only for low-OH silica fibers. *(affects: installation, fiber_choice)*
Q4. What are the cleaning and fouling conditions at the measurement point, and how often can the probe be accessed for cleaning? *Why it matters:* ATR probes require tight contact and are sensitive to surface deposits. Fouling on the crystal can change the measurement and must be managed. *(affects: technique_choice, installation)*
Q5. What laboratory reference method do you currently use for fat and protein, and how many reference samples can you provide during the comparison experiment? *Why it matters:* Independent reference measurements are required for calibration and validation. The reference method defines the accuracy target and the number of samples determines the feasibility of a robust chemometric model. *(affects: feasibility_plan, go_no_go_criteria)*

## Recommendation

- **R1 · Primary candidate: NIR + MIR + Raman (combination: a hypothesis to test), diffuse reflection.** NIR diffuse reflection is the direct application precedent for opaque, concentrated dairy products. It is the most common online fiber-optic method and can be used with standard silica fibers. The main risk is that reflection signals are sensitive to surface characteristics and particle/globule size, so physical variation from temperature and texture changes can mimic composition change. Scatter correction and a matrix-specific calibration are required. *Conditions:* Requires a contact or near-contact reflection probe installed in the product flow. Calibration must be built on representative samples covering the expected temperature and texture variation. [6: S01 p.17] [7: S01 p.10] [8: S01 p.17]
- **R2 · Comparison candidate: MIR, ATR.** MIR-ATR is a strong comparison method because it provides well-defined absorption bands and high selectivity for fat and protein. It is suitable for liquids and pastes in contact with the ATR crystal. The main limitations are that it samples only a surface layer a few micrometres deep, requires tight contact, and is sensitive to fouling. The usable range and fiber link length depend on the actual MIR fiber and probe selected. *Conditions:* Requires a contact ATR probe installed in the product flow. The MIR fiber link length is an open question and must be confirmed with AFS. [9: S01 p.9] [10: S01 p.6] [11: S01 p.13]
- **R3 · Conditional candidate: Raman, raman probe.** Raman is a conditional option if NIR diffuse reflection proves insufficient for protein or fat specificity, or if fluorescence background is manageable. Raman is well suited to aqueous media and provides complementary vibrational information. The main risks are weak signal and fluorescence background, which must be checked on real samples. *Conditions:* Only if NIR diffuse reflection fails to meet accuracy targets and if fluorescence background on the real product is acceptable. Requires a Raman probe and laser excitation wavelength to be selected. [12: S01 p.16] [13: S01 p.11]
- **R4 · Not recommended: NIR, transmission transflection.** NIR transmission or transflection is not recommended as a primary option for an opaque, concentrated product because transmission fails when the sample is too thick, opaque, or fat-rich. A transflection probe may work in some cases, but this is a hypothesis that would require testing and is not the first choice for an opaque product. *Conditions:* Only if the product is less opaque than stated or if a transflection probe is specifically tested and shown to work. [14: S01 p.18]

## Measurement concept

- **Probe and geometry:** Primary: NIR diffuse reflection probe in contact or near-contact with the flowing product. Comparison: MIR-ATR probe in contact with the product. Both require installation in the processing line at a point where the product is representative and accessible.
- **Location:** In the processing line, at a point where the product is well mixed and representative of the bulk composition. The exact location depends on the customer's process layout and must be confirmed.
- **Fiber link:** NIR can use standard silica fibers. MIR requires chalcogenide, polycrystalline, or hollow waveguide fibers; the achievable link length is an open question and must be confirmed with AFS. [15: S01 p.17] [16: S01 p.10]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber, and probe actually selected. [17: S01 p.10]
- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber, and probe actually selected. [18: S01 p.9]
- **Raman:** Raman shift is reported in cm-1. The laser excitation wavelength must be stated separately and is not specified in the sources for this application. [19: S01 p.11]

## Risks and uncertainty

- Temperature and texture variation may cause spectral changes that mimic composition changes, especially for NIR diffuse reflection. *(rules: R-GEO-6, R-GEN-5)* [20: S01 p.17]
- NIR may lack sensitivity for the required accuracy, especially if fat or protein is present at low concentration. *(rules: R-NIR-4)* [21: S01 p.16]
- MIR-ATR samples only a surface layer and is sensitive to fouling on the crystal, which could bias the measurement. *(rules: R-MIR-3)* [22: S01 p.13]
- The MIR fiber link length is unknown and may be limited; no source states an achievable length for an MIR link. *(rules: R-FIB-2)* [23: S02 p.7]
- Calibration models are specific to the matrix and must be re-validated if the product composition or texture changes. *(rules: R-CAL-1)* *(no verified source: engineering judgement)*

## First feasibility experiment

1. **Collect representative samples of the opaque, concentrated milk product across the expected range of fat and protein concentrations, and across the expected temperature and texture variation.** Ensure the calibration and validation data cover the chemical and physical variation that will be encountered in the process. *(no verified source: engineering judgement)*
2. **Measure each sample with the primary method (NIR diffuse reflection) and the comparison method (MIR-ATR) under controlled conditions. If NIR fails, test Raman as a conditional method.** Compare the performance of single methods before considering combinations. *(no verified source: engineering judgement)*
3. **Obtain independent reference measurements for fat and protein using the customer's laboratory method for every sample.** Provide the reference values needed to build and validate chemometric calibration models. *(no verified source: engineering judgement)*
4. **Build separate calibration models for fat and protein using each single method. Validate the models on held-out runs or batches that were not used for calibration.** Assess the accuracy and robustness of each method independently. *(no verified source: engineering judgement)*
5. **Compare the prediction errors of the single-method models against the customer's required accuracy. If no single method meets the target, test a combination of NIR and MIR or NIR and Raman as a hypothesis.** Determine whether a single method is sufficient or whether a combination provides a gain. [24: REF §5]
6. **Define a go/no-go criterion based on the customer's required accuracy for fat and protein, expressed as prediction error relative to the laboratory reference method.** Provide a numerical basis for deciding whether to proceed with a method. *(no verified source: engineering judgement)*

**Reference measurements:** The customer's existing laboratory method for fat and protein analysis will serve as the independent reference. The number of reference samples and the accuracy of the reference method must be confirmed.

**Decision basis:** The go/no-go decision will be based on whether the prediction error for fat and protein, validated on held-out samples, meets the customer's required accuracy. The numerical criteria must come from the customer.

## Assumptions

- The product is a liquid or paste that can be contacted by a probe in the processing line.
- The customer can provide representative samples and reference measurements for fat and protein.
- The installation point allows a contact or near-contact probe and has acceptable cleaning access.
- The temperature range is compatible with the selected probe materials.

## Not covered by the supplied sources

- Achievable MIR fiber link length for a process installation
- Specific accuracy or detection limits for fat and protein in opaque, concentrated milk products
- Response time for a specific NIR or MIR configuration
- Product codes, prices, or component ratings for AFS systems
- In vivo or production-validated performance for this specific product

## Evidence (verified quotes)

1. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
2. ✓ **S01 p.6** (general): "ATR- platform absorption liquid,paste, soft"
3. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
4. ✓ **S01 p.2** (general): "Fiber optic probes and cells are being integrated into reactors and production lines of ongoing technological processes, enabling on-site online analysis and obtaining results in near real time."
5. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
6. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
7. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
8. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
9. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
10. ✓ **S01 p.6** (general): "ATR- platform absorption liquid,paste, soft"
11. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns"
12. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
13. ✓ **S01 p.11** (general): "Measurement of the Raman scattering (RS) effect, is also a type of vibrational spectroscopy."
14. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
15. ✓ **S01 p.17** (general): "The main equipment includes a fiber optic probe where one set of fibers delivers light to the sample and the other collects the "backscattered" light."
16. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
17. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules"
18. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
19. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
20. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
21. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
22. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns"
23. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
24. ✓ **REF §5** (method gain): "Combinations | Only the ranges confirmed for the actual components | For example NIR + Raman, MIR ATR + fluorescence; compare with the best single method."

## Verification

- Citations verified: 24 of 25 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 1; soft warnings: 4; repair rounds: 2.
- Removed 1 citation(s) that failed verification:
  - ⚠ premise_checks[1].citations[1]: REF p.3 "A feasibility plan needs representative samples or process states, independent reference measurements, a defined compari"
- Removed 3 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry

*Run D02 · models deepseek/deepseek-v4-pro-0813 · cost $0.0573*
