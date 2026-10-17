# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Provisional feasibility assessment. A defensible shortlist can be built from the deterministic screening plus dairy-relevant source precedents (opaque/concentrated dairy by NIR reflection; ATR for liquids/pastes). It rests on stated assumptions: fat and protein are the main target components, the matrix is dairy-like and aqueous, and a contact probe can be installed in the line. The final technique, probe, fiber and installation cannot be fixed before the clarification answers; the combined-method gain is a hypothesis only.

## Premise check

- **Not covered:** Earlier information about composition changes is achievable and useful.. No supplied source demonstrates in-line composition measurement for this product. The closest passage describes the general concept of in-process analysis without sampling; it is a reason to test, not evidence for this case. [1: S01 p.3]
- **Not covered:** Current laboratory checks should be retained alongside the new spectroscopy approach.. No source discusses this customer's laboratory organisation. Keeping the lab checks is consistent with the guidance that a feasibility plan needs independent reference measurements. [2: REF §3]
- **Supported:** An initial spectroscopy concept and a practical comparison experiment are the appropriate next step.. Both the concept paper and the AFS pathway describe multi-method laboratory trials as the way to select the method when the best approach is not predictable in advance. [3: S01 p.3] [4: S02 p.20]

## Requirements

**Stated by the customer**

- Opaque, concentrated milk product flowing through a processing line.
- Fat and protein are currently measured by sampling.
- Earlier information about composition changes is wanted.
- Product temperature and texture vary during production.
- Laboratory checks are to be retained.

**Key unknowns**

- Fat and protein ranges, and required accuracy, repeatability and response time.
- Whether the product is a solution, emulsion, dispersion or slurry, and its particle/globule size.
- Temperature range and rate of change at the measurement point.
- Installation point, pressure/flow, cleaning (CIP) and distance to the spectrometer.
- Whether any target species is fluorescent.

## Clarification questions (most decision-relevant first)

Q1. What fat and protein concentration ranges must be covered, and what accuracy, repeatability and response time must the in-line result reach compared with your current laboratory checks? *Why it matters:* Sets the go/no-go basis and decides whether NIR (strong for major components, weaker for trace levels) is sufficient or whether a second method must be added. No source gives accuracy or detection limits for this product, so these numbers must come from you. *(affects: method, technique, go_no_go_basis)*
Q2. Is the product a true solution, an emulsion, a dispersion or a slurry; what is the typical fat-globule/particle size, and what are the minimum and maximum product temperature at the intended measurement point? *Why it matters:* Decides the scattering regime and therefore the geometry (diffuse reflection vs ATR vs transmission) and the temperature requirements of probe and fiber. Reflection signals are sensitive to surface characteristics and globule size. *(affects: technique, probe, fiber, installation)*
Q3. Which composition changes must be detected earlier, and on what timescale (seconds, minutes) - step changes at product transitions, or slow drifts? *Why it matters:* Decides required acquisition speed and whether a single method or a synchronised combination is needed; data from different methods must be synchronised to a common time step before fusion. *(affects: method, technique, combination)*
Q4. Where can a probe be installed (pipe, vat, transfer line), at what pressure and flow, with what cleaning regime, and how far is that point from the spectrometer? *Why it matters:* Decides probe type and fiber family. MIR light cannot travel in silica fiber, and no source states an achievable MIR link length, so the MIR link length must be answered by AFS, not assumed. *(affects: installation, fiber, status)*
Q5. Does the product contain a fluorescent species you care about (for example riboflavin or other vitamins), or should the comparison stay with vibrational methods for fat and protein? *Why it matters:* Fluorescence only measures species that fluoresce, or a justified indicator. Without a defined fluorophore, fluorescence cannot be ranked as a fat/protein method. *(affects: method, status)*

## Recommendation

- **R1 · Primary candidate: NIR + MIR (combination: a hypothesis to test), diffuse reflection.** Screening passes NIR diffuse reflection for an opaque liquid. In the sources, inline NIR reflection is the technique used for opaque or highly concentrated dairy products, and NIR is described as the most common online method with fiber probes. This is the single method to test first. *Conditions:* Valid only while the product stays scattering/opaque and the probe can be flush-mounted in contact with the flowing product. If the product becomes transparent in some production states, a transmission or transflection geometry must be tested as well (screening lists that technique as unknown, not failed). [5: S01 p.17] [6: S01 p.10] [7: S01 p.5]
- **R2 · Comparison candidate: MIR, ATR.** Screening passes MIR-ATR. MIR has well-defined bands and high selectivity, and ATR fiber probes are described for liquids and soft solids with measurement at a distance from the spectrometer without sampling. It is worth testing against NIR because it samples a different, very thin layer and can carry information NIR misses. *Conditions:* Requires tight contact of the crystal with the product, and a MIR-transparent fiber link (silica fiber cannot carry MIR). Fouling on the crystal and surface representativeness must be checked on the real product. [8: S01 p.9] [9: S01 p.10] [10: S04 p.4]
- **R3 · Conditional candidate: Raman, raman probe.** Screening passes the Raman probe. Raman is attractive here because the product is aqueous and Raman tolerates water better than infrared methods. It is only conditional, because the weak Raman signal can be swamped by fluorescence in a real dairy matrix. *Conditions:* Applies only if a check on the real product shows that the fluorescence background does not dominate the Raman bands, and if the complementary structural information is needed beyond NIR and MIR. Deciding check is part of the first experiment. [11: S01 p.16] [12: S01 p.11]
- **NR1 · Not recommended: UV-Vis, transmission transflection.** You proposed UV-Vis. Screening fails UV-Vis transmission/transflection, diffuse reflection and emission for an opaque liquid: light cannot penetrate this type of sample, and Table 1 lists the reflection and emission geometries for solid/pill or radiating samples. UV-Vis ATR passed screening but is not shortlisted for fat and protein, because UV-Vis signals overlap strongly in mixtures and the method's selectivity is low. *Conditions:* Could be revisited only for a different target (for example a specific UV-absorbing species or a biomass-type signal), not for fat and protein in an opaque concentrated product. [13: S01 p.18] [14: S01 p.5]
- **NR2 · Not recommended: Fluorescence, fluorescence probe.** You proposed fluorescence. Screening is unknown, and no fluorescent target species has been identified in this product for a fat/protein measurement: fluorescence only reports species that fluoresce, or a justified fluorescent indicator, and most chemicals do not. Fluorescence is highly sensitive but not selective for a given analyte, so it is not a fat/protein method as the enquiry stands. *Conditions:* Becomes a conditional candidate if Q5 identifies a relevant intrinsic fluorophore (for example riboflavin or another vitamin) or if a justified indicator is acceptable. [15: S01 p.5] [16: S01 p.16] [17: REF §5]

## Measurement concept

- **Probe and geometry:** Primary: NIR diffuse-reflection probe in contact with the product, flush-mounted into the pipe or vat. Comparison: MIR-ATR probe, crystal in contact with the product. Raman probe only if the conditional check passes.
- **Location:** A single, fixed measurement point in the process line or vat, chosen so that the same volume is seen by every method compared.
- **Fiber link:** NIR can use silica Vis-NIR fibers; MIR needs chalcogenide (CIR) or polycrystalline (PIR) fibers, since silica fiber cannot carry MIR light. The achievable MIR link length is not stated in the sources and must be answered by AFS. Fiber link keeps the spectrometers away from the process point. [18: S01 p.17] [19: S01 p.15] [20: REF §5]

## Spectral range

- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected and is not fixed by this assessment. [21: S01 p.10]
- **MIR:** Nominal method range 4000-400 cm-1 (2.5-25 um). The usable range depends on the fiber, crystal and spectrometer selected. [22: S01 p.9]
- **Raman:** Raman is stated as a Raman shift in cm-1, with the laser excitation wavelength reported separately. The excitation wavelength depends on the laser and probe actually selected and is not fixed by this assessment. [23: S01 p.11]

## Risks and uncertainty

- Scattering-dominated opaque matrix. Physical variation (fat-globule size, air, texture) can mimic a composition change, because the reflection signal is sensitive to surface characteristics and globule size. *(rules: R-GEO-6)* [24: S01 p.17]
- Varying temperature. No supplied source gives a temperature tolerance for probes or fibers in this product; if temperature swings change the spectra or exceed the probe limits, the shortlist or the installation changes. This is an open question, not a value to assume. *(no verified source: engineering judgement)*
- Calibration is matrix-specific. If the recipe, concentration range or product form changes, the model must be re-validated (usually rebuilt or extended) on the new material. *(rules: R-CAL-1)* [25: REF §5]
- NIR sensitivity for minor components. If a target is a trace component, NIR may not reach it; the cited figure is from a bioprocess context, not from this product. *(rules: R-NIR-4)* [26: S01 p.16]
- MIR-ATR samples only a very thin surface layer and needs tight contact; deposits or fouling on the crystal and cleaning in place can invalidate the measurement. *(rules: R-MIR-2, R-MIR-3)* [27: S04 p.4]
- MIR fiber link. Silica fiber cannot carry MIR light; CIR/PIR fibers are required, and no source states an achievable MIR cable length, so the MIR link length is an open AFS question. *(rules: R-FIB-1, R-FIB-2)* *(no verified source: engineering judgement)*
- Combining NIR and MIR on the same point. A multispectral probe covering four methods is described as under development, and alternating separate probes cannot guarantee that both methods analyse the same spot. Data from different methods also need synchronising to a common time step before fusion. *(rules: R-CMB-1, R-CMB-2, R-CMB-3)* [28: S01 p.8] [29: S01 p.8] [30: S01 p.8]
- Evidence scope. The dairy and process examples in the sources are laboratory or literature examples. They are a reason to test the methods, not proof that they work for this customer's product or that any configuration is suitable for a production environment. *(rules: R-EVI-1, R-EVI-2)* [31: REF §3]
- Sample inhomogeneity and process turbulence must be considered when choosing the measurement technique and the sampling location; a fixed point in a turbulent line may not be representative of the bulk. *(rules: R-GEN-5)* [32: S01 p.7]

## First feasibility experiment

1. **1. Samples** Cover the real chemical and physical variation, not one ideal sample. [33: REF §3]
2. **2. Reference measurements** Measure fat and protein on every sample with your existing laboratory method, blind to the spectral result. These are the independent references for the comparison; no accuracy figure is taken from a source. [34: REF §3]
3. **3. Single methods first** Measure NIR diffuse reflection and MIR-ATR separately on the same sample set and the same measurement point; add Raman only if the conditional fluorescence-background check passes. No combination before the single-method results exist. [35: REF §3]
4. **4. Combination as a hypothesis** Only after single methods, test a fused NIR + MIR-ATR model against the best single method. The gain is a hypothesis, and sampling location and timing must be aligned. [36: S01 p.18] [37: REF §5]
5. **5. Validation on held-out runs or batches** Leave whole production runs or batches out of the calibration, not single measurements. Repeated measurements in the same position are similar and must be excluded together, otherwise the validation is optimistic. [38: S03 p.13]
6. **6. Go / no-go basis** The numerical criteria must come from the customer (Q1): required accuracy and repeatability for fat and protein against the retained laboratory method, and required response time. No such numbers are taken from the sources. *(no verified source: engineering judgement)*

**Reference measurements:** Your retained laboratory fat and protein checks, run on the same samples and blind to the spectral data.

**Decision basis:** Go only if the in-line method meets the customer's own accuracy, repeatability and response-time criteria on held-out runs or batches, and if the result is stable across the temperature and texture variation seen in production.

## Assumptions

- Fat and protein are the primary target components; no other analyte is yet specified.
- The product is dairy-like and aqueous, and stays scattering/opaque at the measurement point.
- A contact probe can be installed at a fixed point in the line or vat, with cleaning possible.
- Retained laboratory checks can serve as the independent reference method.

## Not covered by the supplied sources

- Any accuracy, precision, limit of detection or response time for fat and protein in this product.
- Achievable MIR fiber or cable length, and any probe/fiber temperature rating.
- Food-contact, CIP or sanitation compliance for any probe.
- Any spectral data or measurement result for this customer's product.
- Whether a combined NIR + MIR probe is available for this configuration (a four-method multispectral probe is described as under development).
- Prices and product codes.
- An AFS dairy in-line MIR-ATR case; the MIR examples in the sources are water content in petroleum and API in polymer extrusion.

## Evidence (verified quotes)

1. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
2. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
3. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
4. ✓ **S02 p.20** (general): "Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
5. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
6. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
7. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics, as well as standard lamps as light sources, making it ideal for online applications, including remote measurements via fiber optic probes."
8. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
9. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
10. ✓ **S04 p.4** (general): "allowing a tight contact with the probe head"
11. ✓ **S01 p.16** (general): "This combination is practical because Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
12. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
13. ✓ **S01 p.18** (general): "as the light cannot penetrate the sample"
14. ✓ **S01 p.5** (general): "However, the strong overlap of spectral signals in UV spectra complicates the analysis of real samples and makes the use of chemometric algorithms a necessary component of qualitative mixture analysis methods."
15. ✓ **S01 p.5** (general): "However, most chemicals do not exhibit this property."
16. ✓ **S01 p.16** (application precedent): "To fill this gap, Fluorescence spectroscopy can be used for high-sensitivity detection (down to the nM-μM range) of critical cofactors and amino acids like NADH, tryptophan, and riboflavin."
17. ✓ **REF §5** (general): "Only a defined fluorescent species or a justified indicator."
18. ✓ **S01 p.17** (application precedent): "Experimentally, the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
19. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
20. ✓ **REF §5** (general): "The fiber determines which wavelengths reach the probe."
21. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
22. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
23. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
24. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
25. ✓ **REF §5** (general): "calibration specific to the matrix"
26. ✓ **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
27. ✓ **S04 p.4** (general): "allowing a tight contact with the probe head"
28. ✓ **S01 p.8** (general): "Another multispectral probe is also under development, combining four spectral methods: Mid-IR, NIR, Raman, and fluorescence."
29. ✓ **S01 p.8** (general): "It is crucial that the spectral information obtained by different methods-Mid-IR, NIR, Raman, and fluorescence spectra-is collected from the same small, even pinpoint, area of the sample."
30. ✓ **S01 p.8** (general): "data synchronization can be challenging, as the acquisition rates of different spectra can vary greatly-from milliseconds to minutes, while the interval between measurements can also differ."
31. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer."
32. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
33. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
34. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
35. ✓ **REF §3** (general): "An honest provisional plan is more useful than a final configuration built on missing facts."
36. ✓ **S01 p.18** (method gain): "While NIR is the workhorse of the dairy industry, advanced labs often incorporate Fluorescence, Raman, and Mid-Infrared (MIR) ATR fiber optic techniques to capture specific chemical or structural information that NIR might miss."
37. ✓ **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
38. ✓ **S03 p.13** (general): "Repeated measurements in the same sample position produced similar spectra or sensor data; therefore, these should always be simultaneously excluded for every CV iteration."

## Verification

- Citations verified: 38 of 38 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 4; repair rounds: 1.

*Run D02 · models deepseek/deepseek-v4.1-flash · cost $0.0170*
