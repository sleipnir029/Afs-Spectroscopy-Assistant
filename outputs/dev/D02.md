# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Premise not supported by the sources. One customer premise is contradicted by the sources: that the method can handle varying temperature and texture. A source warns that the reflection signal is sensitive to surface characteristics and fat globule size, and that calibration is specific to the matrix and its physical variation; the effect of temperature variation is not addressed at all. That premise underlies the request for earlier in-line composition information, so the honest status is premise_not_supported rather than a provisional method choice. The shortlist below is therefore offered as conditional hypotheses to test: it applies only if the physical state at the measurement point can be stabilised, or if the texture/temperature variation is deliberately covered in the calibration set and the model re-validated on that material. No performance figure (accuracy, detection limit, response time, fiber length) is claimed for this product; those remain unknown and are asked for.

## Premise check

- **Supported:** In-line spectroscopy can provide earlier information about composition changes (in-process, without sampling). Supported at the general level only: the source states online fiber-probe analysis gives in-process results without sampling. It does not establish that it will work for this specific product. [1: S01 p.3]
- **Not covered:** An initial spectroscopy concept and a practical comparison experiment can be defined without further details. No supplied source addresses this. A provisional concept and comparison experiment can be proposed, but the measurement point, target ranges and required accuracy must be answered before a technique is fixed. *(no verified source: engineering judgement)*
- **Not covered:** Laboratory checks can be retained alongside in-line spectroscopy. No supplied source addresses retaining the customer's laboratory checks. This is consistent with a feasibility plan that needs independent reference measurements, but the sources do not state it. *(no verified source: engineering judgement)*
- **Supported:** Spectroscopy can measure an opaque, concentrated milk product. Supported as a dairy application precedent (reason to test, not proof for this product). [2: S01 p.17]
- **Contradicted:** The method can handle varying temperature and texture. A source warns that reflection is sensitive to surface characteristics and fat globule size, and calibration is specific to the matrix and its physical variation, so varying texture is a known influence rather than a handled condition. The effect of temperature variation is not addressed by the sources. [3: S01 p.17] [4: REF §5]
- **Supported:** Fat and protein analysis can be moved earlier in the process. Supported as an application precedent: NIR reflection in dairy is used with PLS regression to quantify fat and protein, and in-process analysis removes sampling delays. Reason to test, not proof for this product. [5: S01 p.17] [6: S01 p.3]

## Requirements

**Stated by the customer**


**Key unknowns**

- Required accuracy and precision for fat and protein, versus the current laboratory method (this sets the go/no-go).
- Fat and protein concentration ranges, which composition changes matter, and their expected magnitude.
- Optical state at the intended measurement point: how opaque/concentrated the product is there, and whether any point on the line is clearer.
- Product temperature range and variation at the measurement point.
- Process and installation: pressure, flow, pipe diameter, available port, cleaning/CIP, and the distance from the point to the spectrometer.
- Required response time for the 'earlier information'.

## Clarification questions (most decision-relevant first)

Q1. Where exactly on the line should the measurement sit, and is the product at that point still opaque/concentrated, or can it be a clearer, more dilute stream? This decides NIR reflection versus transmission/transflection. *Why it matters:* method/technique *(affects: )*
Q2. What are the fat and protein concentration ranges, and what accuracy and precision must the in-line result match compared with your current laboratory method? *Why it matters:* feasibility and go/no-go *(affects: )*
Q3. What is the product temperature range and how much does it vary, and does texture/viscosity change systematically (e.g., during concentration)? *Why it matters:* technique and calibration strategy *(affects: )*
Q4. What are the process conditions at the measurement point: pressure, flow rate, pipe diameter, available port, cleaning/CIP regime, and the distance from the point to a safe place for the spectrometer? *Why it matters:* installation *(affects: )*
Q5. What response time counts as 'earlier information' (seconds, minutes), and are other components besides fat and protein of interest? *Why it matters:* acquisition approach and complexity *(affects: )*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** An opaque, concentrated milk product matches the documented dairy precedent for inline NIR reflection; NIR penetrates up to several millimetres and suits remote fiber-probe measurement; fat and protein are quantified in dairy by PLS regression on reflection data. Single method to test first. *Conditions:* Applies if the probe can be mounted at a point with adequate contact/backscatter and if the product is not so optically thick that the reflected signal is unusable. [7: S01 p.17] [8: S01 p.5] [9: S01 p.17]
- **R2 · Comparison candidate: MIR, ATR.** MIR ATR passes in-line screening and is listed as a dairy technique for chemical/structural information that NIR might miss; MIR shows well-defined bands, and in a tissue study the fat-related ester carbonyl C=O band and the protein amide I/II bands are used. Keep it as a single-method comparison against the best single method. *Conditions:* Applies only if the product allows tight contact with the ATR crystal (liquid or soft solid) and if crystal fouling/cleaning is manageable. [10: S01 p.18] [11: S01 p.9] [12: S04 p.3] [13: S04 p.3] [14: S04 p.4]
- **R3 · Conditional candidate: NIR, transmission transflection.** Conditional on the optical state at the measurement point. Screening is 'unknown': transmission fails for thick, opaque or fat-rich product, but a transflection probe can in some cases serve both low- and high-fat milk. Test only if the product at the chosen point is semi-transparent enough, or as a transflection geometry with a controlled pathlength. *Conditions:* Applies only if a suitable point exists and a defined pathlength (order 1-10 mm) can be maintained; otherwise not applicable. [15: S01 p.18] [16: S01 p.18] [17: S01 p.18]

## Measurement concept

- **Probe and geometry:** In-line insertion probe at one defined point on the processing line, with the spectrometer remotely connected by fiber. NIR diffuse reflection as the primary geometry (backscattered light collected at the probe); MIR ATR (contact crystal) and NIR transflection as comparisons. Probe type, mounting and fiber link depend on the chosen point (pressure, flow, cleaning, distance).
- **Location:** One defined point on the processing line, selected from the answers to Q1 and Q4.
- **Fiber link:** Not fixed here. The fiber family must transmit the chosen method's range; achievable length and ratings are an AFS question for the actual configuration, not a value assumed here. [18: S01 p.17] [19: S01 p.15]

## Spectral range

- **NIR:** Nominal method range 780-2500 nm. Usable range depends on the instrument, fiber and probe actually selected. [20: S01 p.10] [21: REF §3]
- **MIR:** Nominal method range 4000-400 cm-1. Usable range depends on the instrument, fiber and ATR crystal actually selected. [22: S01 p.9] [23: REF §3]
- **Raman:** If considered later, Raman is reported as Raman shift (cm-1) with the laser excitation wavelength stated separately. [24: S01 p.11]

## Risks and uncertainty

- Texture and temperature variation, and sample inhomogeneity, can change the reflection signal and be confounded with composition change; calibration is specific to the matrix and its physical variation. *(rules: R-GEO-6, R-CAL-1, R-GEN-5)* [25: S01 p.17] [26: REF §5] [27: S01 p.7]
- Opacity: the product is opaque and concentrated, so transmission geometries may fail because light cannot penetrate it, and even NIR reflection penetration at the chosen point is unverified. *(rules: R-GEO-2, R-GEN-4)* [28: S01 p.18] [29: S01 p.5]
- MIR ATR samples only a surface layer a few micrometres deep, so fouling, deposits and surface representativeness on a concentrated milk product are risks. *(rules: R-MIR-3)* [30: S01 p.13] [31: REF §5]
- The customer's required accuracy and response time are unknown, and the in-line point may not match the laboratory sample; without these the comparison may be inconclusive. *(rules: R-GEN-2)* [32: REF §3]

## First feasibility experiment

1. **1** Representative samples across the expected variation [33: REF §3]
2. **2** NIR diffuse reflection (primary), with MIR ATR and NIR transflection as comparisons *(no verified source: engineering judgement)*
3. **3** PLS calibration for fat and protein against the reference values, with scatter correction [34: S01 p.17] [35: S01 p.17]
4. **4** Validation on held-out runs or batches *(no verified source: engineering judgement)*
5. **5** Go/no-go against the customer's required accuracy [36: REF §3] [37: REF §5]

**Reference measurements:** The customer's current laboratory fat and protein method, measured on each sample, is the independent reference.

**Decision basis:** Compare each technique's fat and protein prediction error against the accuracy the customer requires. The numerical go/no-go criteria must come from the customer (Q2).

## Assumptions

- The product at the chosen measurement point behaves like the dairy reflection precedent (opaque/concentrated, backscatter-dominant).
- A suitable insertion point exists with acceptable pressure, cleaning and distance conditions.
- The current laboratory fat/protein method is accurate and precise enough to serve as the independent reference.

## Not covered by the supplied sources

- The supplied sources do not address the effect of product temperature variation on the measurement.
- The supplied sources give no accuracy, precision or response-time figures for in-line fat and protein measurement in dairy.

## Evidence (verified quotes)

1. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
2. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
3. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size"
4. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
5. ✓ **S01 p.17** (application precedent): "using Partial Least Squares (PLS) regression to quantify fat and protein"
6. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
7. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
8. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
9. ✓ **S01 p.17** (application precedent): "using Partial Least Squares (PLS) regression to quantify fat and protein"
10. ✓ **S01 p.18** (application precedent): "advanced labs often incorporate Fluorescence, Raman, and Mid-Infrared (MIR) ATR fiber optic techniques to capture specific chemical or structural information that NIR might miss."
11. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
12. ✓ **S04 p.3** (general): "the stretching vibration band of the ester carbonyl C=O at about 1740 cm-1"
13. ✓ **S04 p.3** (general): "the amide I and II bands, two major absorption peaks of the protein peptide group in the infrared region"
14. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
15. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
16. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
17. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm)"
18. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
19. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
20. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
21. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
22. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
23. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
24. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
25. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size"
26. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
27. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
28. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
29. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
30. ✓ **S01 p.13** (general): "typically at a depth of few microns"
31. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
32. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
33. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
34. ✓ **S01 p.17** (application precedent): "using Partial Least Squares (PLS) regression to quantify fat and protein"
35. ✓ **S01 p.17** (general): "applying Multiplicative Scatter Correction (MSC) or Standard Normal Variate (SNV) transformations"
36. ✓ **REF §3** (general): "the basis for the go / no-go decision."
37. ✓ **REF §5** (general): "compare with the best single method."

## Verification

- Citations verified: 37 of 37 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 10; repair rounds: 1.
- Removed 5 intake item(s) not quoted verbatim from the enquiry:
  - intake.targets[0]: enquiry_quote not found verbatim in the enquiry
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[5]: enquiry_quote not found verbatim in the enquiry

*Run D02-20261017T084415Z · models deepseek/deepseek-v4.1-flash · cost $0.0199*
