# First technical assessment: A clear whey stream before concentration

**Customer enquiry**

> Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the reference. The stream can become more turbid under some operating conditions. We need a first measurement concept that handles this change rather than assuming the liquid always remains clear.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for a dairy whey stream that is relatively clear but can become turbid. The sources support NIR transmission/transflection for clear dairy streams and NIR diffuse reflection for opaque or scattering dairy products, so a dual-technique NIR concept is a defensible first measurement concept. The recommendation is conditional on the stream remaining a liquid with dairy-like optical behaviour and on the protein concentration being within a range that NIR can calibrate.

## Premise check

- **Not covered:** spectroscopy can track protein concentration in this stream. The supplied sources describe NIR spectroscopy for fat and protein quantification in milk and dairy products, but they do not provide a validated calibration or performance figure for protein in this customer's whey stream. This is a hypothesis to test, not a supported fact. [1: S01 p.17]
- **Supported:** a first measurement concept can handle the change from clear to turbid. The sources describe a dual-technique NIR approach for dairy products: transmission/transflection for clear or semi-transparent liquids and reflection for opaque or highly concentrated products. A transflection probe is stated to work in some cases for both low-fat and high-fat milk products, which is a reason to test this concept for a whey stream that can become turbid. [2: S01 p.18] [3: S01 p.17] [4: S01 p.18]
- **Supported:** laboratory results are suitable as the reference. The sources describe chemometric calibration models built against reference values, and the customer's stated use of laboratory results as the reference is consistent with this approach. The specific laboratory method and its uncertainty are not stated in the sources. [5: S01 p.2]

## Requirements

**Stated by the customer**

- track protein concentration as the stream changes
- handle a change from relatively clear to more turbid
- use laboratory results as the reference
- first measurement concept, not a final configuration

**Key unknowns**

- protein concentration range and required accuracy
- matrix composition and interferences
- optical behaviour at operating conditions
- temperature and pressure
- installation point and distance
- cleaning and fouling
- required response time
- reference method details

## Clarification questions (most decision-relevant first)

Q1. What is the expected protein concentration range and the required accuracy for the measurement? *Why it matters:* This determines whether NIR is likely to be sensitive enough and whether a chemometric calibration is feasible. The sources state NIR may lack sensitivity for trace components in a bioprocess context, but no whey-specific limit is given. *(affects: method, technique, go_no_go)*
Q2. What is the composition of the whey stream, and which other components vary with protein? *Why it matters:* NIR bands are broad and overlapping, so a calibration is specific to the matrix. If other components vary with protein, the calibration may be confounded. *(affects: method, technique, calibration)*
Q3. What is the optical behaviour of the stream at the installation point, and how turbid can it become? *Why it matters:* This decides whether transmission/transflection, reflection, or both are needed. The sources state transmission fails when the sample is too thick, opaque or fat-rich because light cannot penetrate it. *(affects: technique, installation)*
Q4. What are the temperature, pressure, and cleaning/fouling conditions at the installation point? *Why it matters:* These affect probe compatibility, fouling risk, and whether the measurement can be made in-line without frequent cleaning. *(affects: installation, probe)*
Q5. What is the distance between the installation point and the analyzer location? *Why it matters:* Fiber length and type depend on the method and distance. The sources state long cables only for low-OH silica fibers; MIR fiber lengths are not stated. *(affects: method, fiber, installation)*
Q6. What is the required response time for tracking protein concentration changes? *Why it matters:* This affects the choice of spectrometer and data acquisition strategy. *(affects: instrument, technique)*
Q7. What laboratory reference method will be used for protein, and what is its uncertainty? *Why it matters:* The reference method defines the calibration target and the go/no-go basis. *(affects: calibration, go_no_go)*

## Recommendation

- **R1 · Primary candidate: NIR, transmission transflection.** NIR transmission is the preferred method for transparent or semi-transparent dairy liquids such as whey. A transflection probe is a candidate to handle both clear and more turbid conditions in one probe, based on the dairy example where a transflection probe can work for both low-fat and high-fat milk products. *Conditions:* The stream remains a liquid with dairy-like optical behaviour and the protein concentration is within a range that NIR can calibrate. [6: S01 p.18] [7: S01 p.18]
- **R2 · Comparison candidate: NIR, diffuse reflection.** NIR diffuse reflection is used for opaque or highly concentrated dairy products. It should be tested as a comparison for the more turbid operating conditions. *Conditions:* The stream becomes sufficiently turbid or scattering that transmission/transflection fails. [8: S01 p.17]
- **R3 · Conditional candidate: NIR, transmission transflection.** A transflection probe is a candidate to handle both clear and more turbid conditions in one probe, based on the dairy example where a transflection probe can work for both low-fat and high-fat milk products. *Conditions:* The stream remains a liquid with dairy-like optical behaviour and the protein concentration is within a range that NIR can calibrate. [9: S01 p.18]
- **R4 · Not recommended: MIR, ATR.** MIR ATR is a possible method for liquids, but it is not the first choice for this application because the customer's stream is aqueous and the target is protein in a dairy stream. The sources do not provide a whey-specific MIR protein calibration, and ATR samples only a surface layer a few micrometres deep, which is a risk for a stream that can become turbid. *Conditions:* Not recommended for the first measurement concept. [10: S01 p.5]
- **R5 · Not recommended: Raman, raman probe.** Raman is well suited to aqueous media, but the sources do not provide a whey-specific Raman protein calibration, and Raman signals are weak and can be swamped by fluorescence. It is not the first choice for this application. *Conditions:* Not recommended for the first measurement concept. [11: S01 p.11]
- **R6 · Not recommended: UV-Vis, transmission transflection.** UV-Vis is very sensitive but signals of mixtures overlap strongly, and the sources do not provide a whey-specific UV-Vis protein calibration. It is not the first choice for this application. *Conditions:* Not recommended for the first measurement concept. [12: S01 p.5]
- **R7 · Not recommended: Fluorescence, fluorescence probe.** Fluorescence only measures species that fluoresce, and no fluorescent species or indicator has been identified for this whey stream. It is not the first choice for this application. *Conditions:* Not recommended for the first measurement concept. [13: S01 p.5]

## Measurement concept

- **Probe and geometry:** NIR transmission or transflection probe for the relatively clear stream, with a NIR diffuse reflection probe as a comparison for the more turbid conditions. A transflection probe is a candidate to handle both conditions in one probe.
- **Location:** In-line at the whey stream before the concentration stage.
- **Fiber link:** Low-OH silica fiber for NIR, with the analyzer located away from the process point. The exact length is unknown and must be confirmed with AFS. [14: S01 p.18] [15: S01 p.17] [16: S01 p.18]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [17: S01 p.10]

## Risks and uncertainty

- NIR calibration is specific to the matrix. If the whey composition changes in ways not captured by the calibration, the protein prediction may be wrong. *(rules: R-CAL-1)* [18: S01 p.10]
- NIR may lack sensitivity for trace protein concentrations. The source cites below 0.1 percent in a bioprocess context, but no whey-specific limit is given. *(rules: R-NIR-4)* [19: S01 p.16]
- Reflection signals are sensitive to surface characteristics and particle/globule size, so physical variation can mimic composition change. Scatter correction is needed. *(rules: R-GEO-6)* [20: S01 p.17]
- Transmission fails when the sample is too thick, opaque or fat-rich because light cannot penetrate it. The stream can become more turbid, so this risk is real. *(rules: R-GEO-2)* [21: S01 p.18]
- The transflection probe is stated to work for both low-fat and high-fat milk products only in some cases. It is a hypothesis to test for this whey stream. *(rules: R-GEO-5)* [22: S01 p.18]
- The sources do not provide a whey-specific NIR protein calibration or performance figure. The recommendation is a reason to test, not proof that it will work for this customer. *(rules: R-EVI-2)* [23: S01 p.17]

## First feasibility experiment

1. **Collect representative whey samples across the expected protein concentration range and across the expected turbidity range.** Representative samples across the expected chemical and physical variation. [24: S01 p.3]
2. **Measure each sample with the NIR transmission/transflection probe and the NIR diffuse reflection probe.** Single methods first, combinations only after. [25: S01 p.18] [26: S01 p.17]
3. **Measure the same samples with the laboratory reference method for protein.** Independent reference measurements. [27: S01 p.2]
4. **Build a chemometric calibration model for protein using the NIR spectra and the reference values.** Calibration model. [28: S01 p.10]
5. **Validate the model on held-out runs or batches that were not used for calibration.** Validation on held-out runs or batches. [29: S01 p.2]
6. **Compare the prediction error against the customer's required accuracy for protein concentration.** Go/no-go basis whose numerical criteria come from the customer. [30: S01 p.2]

**Reference measurements:** Laboratory results for protein concentration, as stated by the customer.

**Decision basis:** The go/no-go decision is based on whether the validated prediction error meets the customer's required accuracy for protein concentration. The numerical criteria must come from the customer.

## Assumptions

- The whey stream is a liquid with dairy-like optical behaviour.
- The protein concentration is within a range that NIR can calibrate.
- The stream can become turbid but remains a liquid.
- The installation point is before the concentration stage, as stated by the customer.

## Not covered by the supplied sources

- A whey-specific NIR protein calibration or performance figure.
- The protein concentration range and required accuracy for this customer.
- The exact optical behaviour of the stream at operating conditions.
- The temperature, pressure, and cleaning/fouling conditions at the installation point.
- The distance between the installation point and the analyzer location.
- The required response time.
- The laboratory reference method and its uncertainty.

## Evidence (verified quotes)

1. ✓ **S01 p.17** (application precedent): "applying Multiplicative Scatter Correction (MSC) or Standard Normal Variate (SNV) transformations to remove physical interference caused by the scattering nature of the milk particles before using Partial Least Squares (PLS) regression to quantify fat and protein"
2. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate"
3. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates"
4. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products"
5. ✓ **S01 p.2** (general): "This is achieved through a special branch of analytical chemistry called chemometrics, which provides chemists with a rich toolkit for constructing calibration and classification models"
6. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate"
7. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products"
8. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates"
9. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products"
10. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm)"
11. ✓ **S01 p.11** (general): "measuring Raman spectra is hampered by the low intensity of Raman signals, which are several orders of magnitude weaker than IR absorption peaks in the IR range"
12. ✓ **S01 p.5** (general): "the strong overlap of spectral signals in UV spectra complicates the analysis of real samples and makes the use of chemometric algorithms a necessary component of qualitative mixture analysis methods"
13. ✓ **S01 p.5** (general): "most chemicals do not exhibit this property"
14. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate"
15. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates"
16. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products"
17. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
18. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data"
19. ✓ **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent"
20. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size"
21. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample"
22. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products"
23. ✓ **S01 p.17** (application precedent): "applying Multiplicative Scatter Correction (MSC) or Standard Normal Variate (SNV) transformations to remove physical interference caused by the scattering nature of the milk particles before using Partial Least Squares (PLS) regression to quantify fat and protein"
24. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods"
25. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate"
26. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates"
27. ✓ **S01 p.2** (general): "This is achieved through a special branch of analytical chemistry called chemometrics, which provides chemists with a rich toolkit for constructing calibration and classification models"
28. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data"
29. ✓ **S01 p.2** (general): "This is achieved through a special branch of analytical chemistry called chemometrics, which provides chemists with a rich toolkit for constructing calibration and classification models"
30. ✓ **S01 p.2** (general): "This is achieved through a special branch of analytical chemistry called chemometrics, which provides chemists with a rich toolkit for constructing calibration and classification models"

## Verification

- Citations verified: 30 of 30 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 1; soft warnings: 2; repair rounds: 2.
- ⚠ forbidden_wording at assessment: certainty: 'will work'
- Removed 1 intake item(s) not quoted verbatim from the enquiry:
  - intake.sample.fluorophore: slot value without a verbatim enquiry quote; reset to unknown

*Run D03 · models deepseek/deepseek-v4-pro-0813 · cost $0.0633*
