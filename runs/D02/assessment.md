# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for an opaque, concentrated milk product because the sources describe NIR diffuse reflection for opaque or concentrated dairy products and MIR-ATR for liquids and soft solids. However, several central facts are unknown, so the recommendation is conditional and a comparison experiment is required before any configuration is chosen.

## Premise check

- **Supported:** earlier information about composition changes is desirable and achievable. The sources describe fiber-optic probes integrated into production lines for online analysis and near-real-time results, which is a reason to test this approach for the customer's goal. [1: S01 p.2]
- **Supported:** an initial spectroscopy concept and a practical comparison experiment are appropriate next steps. The AFS pathway and the laboratory concept both start with multi-method trials on representative samples to select the best method, which matches the customer's request. [2: S02 p.20] [3: S01 p.3]
- **Supported:** laboratory checks should be retained. The sources describe online analysis as complementing laboratory methods, not replacing them; the feasibility plan below explicitly retains laboratory checks as the independent reference. [4: S01 p.2]

## Requirements

**Stated by the customer**

- The customer wants an initial spectroscopy concept, not a final installed configuration.
- The customer wants a practical comparison experiment.
- The customer wants to retain laboratory checks.

**Key unknowns**

- fat and protein concentration ranges and required accuracy
- temperature range and variation
- texture variation details and effect on optical properties
- installation point and distance from sampling point
- cleaning and fouling requirements
- flow rate and pressure
- matrix composition and potential interferences

## Clarification questions (most decision-relevant first)

Q1. What are the expected fat and protein concentration ranges, and what accuracy is required for the earlier composition information? *Why it matters:* This determines whether NIR is sufficient or whether a more selective method such as Raman or MIR-ATR is needed. NIR may lack sensitivity for trace components, and calibration requirements depend on the concentration range. *(affects: method, technique, go_no_go_criteria)*
Q2. What is the temperature range and how fast does temperature change during production? *Why it matters:* Temperature affects spectral response and probe compatibility. The sources do not state a temperature rating for any probe, so this is an open question for AFS. *(affects: installation, probe_selection)*
Q3. What is the nature of the texture variation, and does the product remain a flowing liquid throughout the process? *Why it matters:* Texture changes can alter scattering and surface properties, which affect reflection measurements. If the product becomes a paste or soft solid, MIR-ATR becomes more relevant. *(affects: method, technique)*
Q4. Where on the processing line would the probe be installed, and what is the distance from that point to a safe spectrometer location? *Why it matters:* Fiber length limits differ by fiber family. Long cables are stated only for low-OH silica fibers; MIR fiber link length is an open question for AFS. *(affects: installation, fiber_selection)*
Q5. What are the cleaning and fouling requirements at the proposed measurement point? *Why it matters:* ATR samples only a surface layer a few micrometres deep, so deposits on the crystal are a risk. Reflection probes are also sensitive to surface fouling. *(affects: technique, installation)*
Q6. What is the flow rate and pressure at the proposed measurement point? *Why it matters:* This affects probe insertion, sealing, and whether the probe can be flush-mounted or must be inserted into the flow. *(affects: installation, probe_selection)*
Q7. What is the matrix composition beyond fat and protein, and are there known interferences or fluorescent components? *Why it matters:* This determines whether fluorescence is a viable method and whether NIR or Raman calibrations will be affected by other components. *(affects: method, technique)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** NIR diffuse reflection is the stated method for opaque or highly concentrated dairy products such as yogurt, butter, or whole milk concentrates. The customer's product is opaque and concentrated, so this is the most direct match. *Conditions:* The product remains a flowing liquid or soft solid with a surface suitable for reflection measurement. Temperature and texture variation must be within the probe's operating limits. [5: S01 p.17] [6: S01 p.17]
- **R2 · Comparison candidate: MIR, ATR.** MIR-ATR is suitable for liquids and soft solids and provides well-defined bands with high selectivity. It is a strong comparison method for fat and protein because it samples the surface layer and can provide complementary chemical information. *Conditions:* The product must allow tight contact with the ATR crystal. If the product is a flowing liquid, an immersion ATR probe is appropriate. If it becomes a paste or soft solid, contact is still possible but fouling risk increases. [7: S01 p.10] [8: S01 p.9]
- **R3 · Comparison candidate: Raman, raman probe.** Raman is well suited to aqueous media and can provide a molecular fingerprint for fat and protein. It is a useful comparison because it may be less affected by water than infrared methods. *Conditions:* Fluorescence background must be checked on real samples. If the product or its components fluoresce strongly, Raman may be impractical. [9: S01 p.16] [10: S01 p.11]
- **R4 · Conditional candidate: NIR, transmission transflection.** Transmission normally fails for opaque samples, but a transflection probe can in some cases serve both low-fat and high-fat milk products. For this opaque, concentrated product, transflection is a hypothesis to test only if the product is not fully opaque or if a short pathlength can be used. *Conditions:* Only if the product is not fully opaque or if a controlled short pathlength is feasible. This is unlikely for a fully opaque product, so it is conditional on the answer to Q3. [11: S01 p.18] [12: S01 p.18]
- **R5 · Not recommended: Fluorescence, fluorescence probe.** No fluorescent species or indicator has been identified for this product. Fluorescence only measures species that fluoresce, and most chemicals do not. It is not a direct measurement of fat or protein. *Conditions:* Would only become relevant if the customer identifies a fluorescent component or indicator that correlates with fat or protein. [13: S01 p.5]
- **R6 · Not recommended: UV-Vis, ATR.** UV-Vis has low selectivity for fat and protein in a complex milk matrix, and the strong overlap of spectral signals complicates analysis. It is not a good primary method for this target. *Conditions:* Would only be relevant if a specific UV-absorbing species were the target, which is not the case here. [14: S01 p.5]

## Measurement concept

- **Probe and geometry:** Primary: NIR diffuse reflection probe flush-mounted into the pipe or vat, with one set of fibers delivering light and another collecting backscattered light. Comparison: MIR-ATR immersion probe in contact with the flowing product. Raman probe as a second comparison if fluorescence background is acceptable.
- **Location:** At a point on the processing line where the product is well-mixed and representative, upstream of the current sampling point to provide earlier information.
- **Fiber link:** For NIR and Raman, silica fibers are suitable. For MIR-ATR, chalcogenide or polycrystalline fibers are needed. The achievable MIR fiber length is an open question for AFS. [15: S01 p.17] [16: S01 p.15]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber, and probe actually selected. [17: S01 p.10]
- **MIR:** Nominal MIR range is 4000-400 cm-1 (2.5-25 µm). The usable range depends on the fiber and ATR crystal selected. [18: S01 p.9]
- **Raman:** Raman shift is reported in cm-1. The laser excitation wavelength must be stated separately. The source example uses 785 nm excitation for pharmaceutical blends. [19: S01 p.15]

## Risks and uncertainty

- NIR reflection is sensitive to surface characteristics and particle or globule size, so texture variation can mimic composition change. *(rules: R-GEO-6)* [20: S01 p.17]
- NIR bands are broad and overlapping, so a chemometric calibration is required and may lack sensitivity for trace components. *(rules: R-NIR-2, R-NIR-4)* [21: S01 p.10]
- MIR-ATR samples only a surface layer a few micrometres deep, so deposits on the crystal and surface representativeness are risks. *(rules: R-MIR-3)* [22: S01 p.13]
- Raman signals are weak and can be swamped by fluorescence; this must be checked on real samples. *(rules: R-RAM-1)* [23: S01 p.11]
- Temperature and texture variation during production may change the spectral response and require a robust calibration or temperature compensation. *(rules: R-GEN-5)* [24: S01 p.7]
- The achievable MIR fiber link length is unknown from the sources; long cables are stated only for low-OH silica fibers. *(rules: R-FIB-2)* [25: S02 p.7]

## First feasibility experiment

1. **Collect representative samples across the expected chemical and physical variation.** Samples must cover the full range of fat and protein concentrations, temperature, and texture states that occur during production. [26: S01 p.3]
2. **Obtain independent reference measurements for fat and protein on the same samples using the customer's laboratory checks.** The laboratory checks serve as the independent reference for calibration and validation. *(no verified source: engineering judgement)*
3. **Measure all samples with NIR diffuse reflection first as the primary single method.** Test the best single method before any combination. [27: S01 p.17]
4. **Measure the same samples with MIR-ATR and Raman as comparison single methods.** Compare the performance of each single method against the reference measurements. [28: S01 p.10]
5. **Build chemometric calibration models for fat and protein using each single method.** Quantify the relationship between spectra and reference values. [29: S01 p.10]
6. **Validate each model on held-out runs or batches that were not used for calibration.** Estimate prediction error on independent data. *(no verified source: engineering judgement)*
7. **Only after single-method results are available, test a combination of the best two methods if neither single method meets the target.** A combination gain is a hypothesis to test, not an assumption. [30: S01 p.7]

**Reference measurements:** The customer's existing laboratory checks for fat and protein are the independent reference. The same samples must be measured by both the laboratory method and the spectroscopy methods.

**Decision basis:** The go/no-go criteria must come from the customer's required accuracy for fat and protein. The customer has not yet stated this, so the numerical criteria are unknown and must be provided by the customer before the experiment is designed.

## Assumptions

- The product remains a flowing liquid or soft solid throughout the process.
- The product is aqueous, as is typical for milk products.
- The fat and protein concentrations are in a range where NIR or MIR can provide useful information.
- The installation point is accessible for a probe and the spectrometer can be located within the fiber length limit.

## Not covered by the supplied sources

- Temperature ratings for any probe or fiber.
- Achievable MIR fiber link length for this application.
- Detection limits or accuracy for fat and protein in opaque, concentrated milk products.
- Specific product codes or prices for AFS components.
- Response time for this specific application.
- Cleaning and fouling performance for this product.

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "Fiber optic probes and cells are being integrated into reactors and production lines of ongoing technological processes, enabling on-site online analysis and obtaining results in near real time."
2. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
3. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
4. ✓ **S01 p.2** (general): "Laboratory measurement methods based on titration, filtration, distillation, and weighing are becoming a thing of the past, becoming more a part of the educational process than practical chemical analysis."
5. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
6. ✓ **S01 p.17** (general): "The main equipment includes a fiber optic probe where one set of fibers delivers light to the sample and the other collects the "backscattered" light."
7. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
8. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
9. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
10. ✓ **S01 p.11** (general): "Raman spectroscopy is based on recording weak radiation signals observed when a sample is irradiated by a laser or high-power LED, typically in the visible light range."
11. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
12. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
13. ✓ **S01 p.5** (general): "Another highly sensitive method, UV/Vis fluorimetry, is based on the secondary emission of excited molecules of certain substances, most often of biological origin. However, most chemicals do not exhibit this property."
14. ✓ **S01 p.5** (general): "However, the strong overlap of spectral signals in UV spectra complicates the analysis of real samples and makes the use of chemometric algorithms a necessary component of qualitative mixture analysis methods."
15. ✓ **S01 p.17** (general): "Experimentally, the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
16. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
17. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
18. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
19. ✓ **S01 p.15** (performance figure): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
20. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
21. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
22. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns, providing information on molecular composition and biochemical changes."
23. ✓ **S01 p.11** (general): "Furthermore, observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
24. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
25. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
26. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
27. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
28. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
29. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
30. ✓ **S01 p.7** (method gain): "This often provides a synergistic effect, allowing one to solve a problem that either method alone cannot handle or only partially."

## Verification

- Citations verified: 30 of 30 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 2; repair rounds: 0.

*Run D02 · models deepseek/deepseek-v4-pro-0813 · cost $0.0218*
