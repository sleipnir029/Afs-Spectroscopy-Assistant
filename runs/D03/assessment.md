# First technical assessment: A clear whey stream before concentration

**Customer enquiry**

> Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the reference. The stream can become more turbid under some operating conditions. We need a first measurement concept that handles this change rather than assuming the liquid always remains clear.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for tracking protein in a whey stream that may become turbid, with explicit assumptions about the optical regime and the need for a chemometric calibration.

## Premise check

- **Supported:** spectroscopy can track protein concentration in the whey stream. The sources describe NIR spectroscopy as a cornerstone of dairy PAT and show inline NIR monitoring of milk fat and protein, including whey-related streams. [1: S01 p.17] [2: S01 p.18]
- **Supported:** a first measurement concept can handle the turbidity change. The sources describe a dual-technique approach for dairy streams where transmission is preferred for clear liquids and reflection for opaque or highly concentrated products, and note that a transflection probe can in some cases serve both. [3: S01 p.18] [4: S01 p.18]

## Requirements

**Stated by the customer**

- track protein concentration as the stream changes
- laboratory results used as the reference
- first measurement concept that handles the turbidity change

**Key unknowns**

- target protein concentration range and required accuracy
- matrix composition and interferences
- optical behaviour of the whey stream under normal and turbid conditions
- temperature and pressure at the measurement point
- installation point and distance from the process line
- cleaning and fouling requirements
- required response time
- reference method details

## Clarification questions (most decision-relevant first)

Q1. What is the expected protein concentration range and the required accuracy for tracking it? *Why it matters:* This determines whether NIR is sufficient or whether a more sensitive method is needed, and sets the go/no-go criteria for the feasibility experiment. *(affects: method_choice, go_no_go_criteria)*
Q2. What is the composition of the whey stream besides protein, and are there known interferences such as lactose, fat, or minerals? *Why it matters:* NIR and Raman calibrations are matrix-specific; interferences can overlap with protein bands and require a different method or a more complex calibration. *(affects: method_choice, calibration_design)*
Q3. How turbid can the stream become, and is the turbidity caused by suspended solids, fat globules, or something else? *Why it matters:* The optical regime determines whether transmission, transflection, or diffuse reflection is appropriate, and whether a single probe can handle the full range. *(affects: technique_choice, probe_selection)*
Q4. What are the temperature, pressure, and cleaning/fouling conditions at the proposed measurement point? *Why it matters:* These affect probe material compatibility, installation design, and the risk of surface deposits that can bias the measurement. *(affects: installation, probe_selection)*
Q5. What is the required response time for tracking protein concentration changes? *Why it matters:* This determines whether a scanning spectrometer or a faster diode-array or sensor approach is needed. *(affects: instrument_choice)*

## Recommendation

- **R1 · Primary candidate: NIR, transmission transflection.** NIR transmission or transflection is the preferred geometry for transparent or semi-transparent dairy liquids such as whey, and a transflection probe can in some cases serve both low-fat and high-fat products, making it a strong first candidate for a stream that may become turbid. *Conditions:* Applies if the stream remains at least partially transmissive in its most turbid state and the optical pathlength can be controlled. [5: S01 p.18] [6: S01 p.18]
- **R2 · Comparison candidate: NIR, diffuse reflection.** NIR diffuse reflection is used for opaque or highly concentrated dairy products and is the fallback if the stream becomes too turbid for transmission. *Conditions:* Applies if the stream becomes opaque or highly scattering under some operating conditions. [7: S01 p.17]
- **R3 · Conditional candidate: Raman, raman probe.** Raman is well suited to aqueous media and can provide a molecular fingerprint for specific components, but its weak signal and fluorescence background must be checked on real whey samples. *Conditions:* Applies only if NIR proves insufficient for the required accuracy or if complementary molecular information is needed, and if fluorescence background is manageable. [8: S01 p.16]
- **R4 · Not recommended: NIR, transmission transflection.** A single fixed-path transmission probe is not recommended as the only option because it fails when the stream becomes too turbid or opaque, and the customer explicitly asked for a concept that handles the turbidity change. *Conditions:* Not recommended as the sole measurement concept. [9: S01 p.18]

## Measurement concept

- **Probe and geometry:** Start with a NIR transflection probe for the relatively clear whey stream, with a controlled optical pathlength. In parallel, test a NIR diffuse reflection probe for the turbid state. If a single probe must cover both regimes, evaluate whether a transflection probe can handle the full turbidity range; otherwise, plan for two probe types or a switchable configuration.
- **Location:** In-line at the whey stream before the concentration stage, with the probe inserted or flush-mounted so that the measurement point is representative of the flowing stream.
- **Fiber link:** Vis-NIR silica fibers are suitable for the NIR range. The actual fiber length and installation distance must be confirmed with AFS. [10: S01 p.18] [11: S01 p.17]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [12: S01 p.10]
- **Raman:** Raman shift is reported in cm-1; the laser excitation wavelength must be stated separately. No specific excitation wavelength is proposed here. [13: S01 p.11]

## Risks and uncertainty

- The turbid state may be too opaque for transflection, forcing a switch to diffuse reflection or a different probe. *(rules: R-GEO-2, R-GEO-4)* [14: S01 p.18]
- NIR calibration is matrix-specific and may need to be rebuilt or extended if the stream composition changes. *(rules: R-CAL-1)* [15: S01 p.10]
- Reflection signals are sensitive to surface characteristics and particle size, so physical variation can mimic composition change. *(rules: R-GEO-6)* [16: S01 p.17]
- Fouling or deposits on the probe surface can bias the measurement, especially for ATR or contact probes. *(rules: R-MIR-3)* [17: S01 p.13]

## First feasibility experiment

1. **Collect representative whey samples across the expected protein concentration range and across the full range of turbidity states, from clear to the most turbid operating condition.** Ensure the calibration and validation cover the chemical and physical variation the method will encounter. *(no verified source: engineering judgement)*
2. **Measure each sample with independent laboratory reference methods for protein concentration, and record turbidity or optical density.** Provide the reference values needed to build and validate the chemometric model. *(no verified source: engineering judgement)*
3. **Acquire NIR spectra with the transflection probe on the clear and moderately turbid samples, and with the diffuse reflection probe on the turbid samples.** Test the primary and comparison techniques on the same sample set. *(no verified source: engineering judgement)*
4. **Build separate PLS calibration models for protein concentration using the transflection and reflection data, and compare their prediction errors.** Determine which single technique performs best and whether a combined or switchable approach is needed. *(no verified source: engineering judgement)*
5. **Validate the models on held-out runs or batches that were not used for calibration, including samples from both clear and turbid conditions.** Estimate the real prediction error and check robustness to turbidity changes. *(no verified source: engineering judgement)*
6. **Apply the go/no-go criteria agreed with the customer, based on the required accuracy for protein tracking.** Decide whether the method is suitable for further development or whether another method such as Raman should be tested. *(no verified source: engineering judgement)*

**Reference measurements:** Laboratory protein analysis results provided by the customer, with the specific reference method to be confirmed.

**Decision basis:** The go/no-go decision should be based on the prediction error of the validated model compared with the customer's required accuracy for protein concentration tracking. The numerical criteria must come from the customer.

## Assumptions

- The whey stream is aqueous and contains protein as the main target analyte.
- The stream remains at least partially transmissive in its most turbid state, or a diffuse reflection probe can be used when it does not.
- A chemometric calibration will be required for quantitative protein prediction.
- The measurement point can accommodate a fiber-optic probe and the associated installation.

## Not covered by the supplied sources

- Specific protein concentration range or required accuracy for this customer
- Exact composition of the whey stream and potential interferences
- Quantitative performance figures for protein measurement in whey
- Achievable fiber length for the NIR link in this installation
- Temperature, pressure, cleaning and fouling ratings for the probe
- Response time of a specific NIR instrument configuration

## Evidence (verified quotes)

1. ✓ **S01 p.17** (application precedent): "The use of Near-Infrared (NIR) spectroscopy for the inline monitoring of milk is a cornerstone of modern dairy "Process Analytical Technology" (PAT)."
2. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
3. ✓ **S01 p.18** (general): "The Advantage of Dual-Technique Availability: having both fiber optic techniques available in a lab rather than relying on one provides the flexibility needed to monitor the entire production chain."
4. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
5. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
6. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
7. ✓ **S01 p.17** (application precedent): "NIR Reflection: Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
8. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
9. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
10. ✓ **S01 p.18** (general): "The setup typically consists of a transmission / transflection probe, where light passes entirely through a defined layer of the sample to a detector on the opposite side."
11. ✓ **S01 p.17** (general): "The main equipment includes a fiber optic probe where one set of fibers delivers light to the sample and the other collects the "backscattered" light."
12. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
13. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
14. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
15. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
16. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
17. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns"

## Verification

- Citations verified: 17 of 17 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 1; soft warnings: 1; repair rounds: 2.
- ⚠ recommendations_unique at recommendations: same method+technique listed more than once: ['NIR transmission_transflection']
- Removed 1 intake item(s) not quoted verbatim from the enquiry:
  - intake.sample.fluorophore: slot value without a verbatim enquiry quote; reset to unknown

*Run D03 · models deepseek/deepseek-v4-pro-0813 · cost $0.0471*
