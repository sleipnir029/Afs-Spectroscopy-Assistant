# First technical assessment: Glucose and lactate trends in an aqueous bioprocess

**Customer enquiry**

> We run a cell culture process in an aqueous medium. Glucose and lactate are measured from samples, and the delay makes it difficult to see changes promptly. We are exploring an in situ spectroscopy pilot that can be checked against those existing laboratory measurements. The medium and cell population change during the run; we have not yet selected a probe or a calibration strategy.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified from the supplied material for an aqueous cell-culture medium with glucose and lactate as targets, but it rests on assumptions: the concentration ranges, the required accuracy and response time, the optical density of the medium and the presence of any fluorophore are all unknown. This is a shortlist to test, not a configuration or an approval.

## Premise check

- **Supported:** An in situ spectroscopy pilot is worth exploring.. The sources describe fiber-optic probes integrated into reactors and production lines for on-site, near-real-time analysis. [1: S01 p.2]
- **Supported:** The delay from sample-based measurement is what makes prompt change detection difficult.. In-process measurement without sampling is described as removing delays and the risk of sample contamination. [2: S01 p.3]
- **Supported:** The pilot can be checked against the existing laboratory measurements.. Independent reference measurements are part of the recommended structure of a feasibility plan. No source states that the customer's existing laboratory method is suitable as a reference for glucose and lactate; that has to be confirmed (see questions). [3: REF §3]

## Requirements

**Stated by the customer**

- Customer stated: aqueous medium, cell culture process, glucose and lactate measured from samples, delay in seeing changes, medium and cell population change during the run, no probe or calibration strategy selected. No concentration ranges, accuracy, response time, optical-density range or fluorophore information were given.

**Key unknowns**

- Concentration ranges of glucose and lactate, and required accuracy, precision and response time.
- Optical behaviour of the medium over the run (clear, semi-transparent, turbid or opaque) and whether it changes with cell density.
- Presence of any fluorescent species or a justified fluorescent indicator.
- Reference laboratory method, its uncertainty, and how often reference samples can be taken.
- Process conditions (temperature, pressure, pH, cleaning/sterilization) and the available installation point.
- Required distance from spectrometer to probe (in particular for any MIR link).

## Clarification questions (most decision-relevant first)

Q1. What are the expected concentration ranges of glucose and lactate, and what accuracy, precision and response time must the in situ result meet? *Why it matters:* These numbers decide which method can reach the target and set the go/no-go criteria. No performance figures for this matrix are in the sources, and the criteria must come from you. *(affects: method_choice, calibration_strategy, go_no_go_basis)*
Q2. How does the medium behave optically during the run - clear/semi-transparent or turbid/opaque - and does the optical density change with cell population? *Why it matters:* It decides whether NIR transmission/transflection with a controlled pathlength is possible at all, or whether a reflection or ATR geometry is required, and whether UV-Vis biomass tracking is a usable covariate. *(affects: technique_choice, geometry, pathlength)*
Q3. Is there any species in the medium that fluoresces (intrinsic fluorophore or an added indicator)? *Why it matters:* Fluorescence only measures species that fluoresce; without such a species it cannot be a direct method for glucose or lactate and would only enter as a conditional option. *(affects: fluorescence_status, combination_candidates)*
Q4. What exactly is the existing laboratory method for glucose and lactate (analyte form, sample handling, uncertainty), and how often can reference samples be taken during a run? *Why it matters:* It determines whether it can serve as the independent reference and how the calibration and validation must be organised. *(affects: reference_design, calibration_strategy)*
Q5. What are the process conditions at the intended measurement point (temperature, pressure, pH, cleaning/sterilization), where can the probe be installed, and what distance is available from the spectrometer to the probe? *Why it matters:* It decides probe construction and the fiber link. In particular, no source states an achievable length for an MIR fiber link, so this is an open AFS question, not a value to assume. *(affects: probe_construction, fiber_link, installation)*
Q6. Besides glucose and lactate, which other variables matter (biomass/cell density, dissolved oxygen, pH, product titre)? *Why it matters:* It decides whether a second, complementary method (for example UV-Vis biomass tracking) is worth including in the trial, and which interferences must be modelled. *(affects: combination_candidates, interference_model)*

## Recommendation

- **R1 · Primary candidate: Raman + MIR + NIR (combination: a hypothesis to test), raman probe.** Best fit for an aqueous medium with glucose and lactate as targets: water interferes less in Raman than in infrared methods, and the supplied bioprocess section describes Raman in the same reactor for direct detection of metabolites such as glucose, acetate and lactate. Screening status is pass. The cited bioprocess text is a literature/application description, so it is a reason to test Raman here, not proof that it will work in this medium. *Conditions:* Applies if a Raman probe can be placed in situ and the medium's fluorescence background is acceptable. Requires a matrix-specific calibration that is re-validated when the medium or cell population changes. [4: S01 p.16] [5: S01 p.16] [6: S01 p.11] [7: S01 p.11]
- **R2 · Comparison candidate: MIR, ATR.** Screening status is pass. MIR gives well-defined vibrational bands and high selectivity, and ATR is the route that copes with the strong water absorption of an aqueous medium by using a very short effective sampling depth. It is the natural comparison to Raman because the two give complementary vibrational information. *Conditions:* Applies if the ATR crystal can be in tight contact with the liquid and fouling can be managed, and if a MIR fiber link of the needed length is available. The sampling depth of a few micrometres makes the reading surface-representative only. [8: S01 p.9] [9: S01 p.5] [10: S01 p.10]
- **R3 · Conditional candidate: NIR, transmission transflection.** Screening status is unknown. Conditional on the medium being transparent or semi-transparent enough for a defined pathlength: NIR is the most common in-line fiber-probe method and is described as effective for major components such as glucose in the millimolar range, but it may lack sensitivity for low concentrations. If the medium is turbid or opaque, transmission fails and a reflection geometry would be the alternative to test. *Conditions:* Applies only after Q2 is answered. Deciding question: what is the optical density of the medium and does it change during the run? Pathlength must be controlled and fixed. [11: S01 p.10] [12: S01 p.16] [13: S01 p.18] [14: S01 p.18] [15: S01 p.18]

## Measurement concept

- **Probe and geometry:** In-situ probes in contact with the liquid: a Raman probe (contact immersion) as the primary option, and an ATR probe for the MIR comparison. NIR, if it becomes applicable, would be a transmission/transflection probe with a controlled pathlength, or a reflection probe if the medium is too turbid for transmission.
- **Location:** Directly in the reactor or vessel, or in a recirculation loop, at a point representative of the bulk liquid; the location must be chosen so that bubbles, foam and cell debris are considered.
- **Fiber link:** Silica fibers for Raman (and for NIR); MIR needs chalcogenide (CIR), polycrystalline (PIR) fibers or hollow waveguides, since silica does not transmit in the MIR. Metal-coated silica fibers avoid polymer-jacket fluorescence, which matters for Raman. The achievable MIR link length is not stated in the sources and must be asked (Q5). [16: REF §5] [17: S02 p.7] [18: S01 p.7]

## Spectral range

- **Raman:** The spectral axis is the Raman shift in cm-1; the laser excitation wavelength is a separate choice and must be stated with the shift range. A 785 nm excitation wavelength appears in a supplied example. The usable shift range depends on the spectrometer, laser, fiber and probe actually selected, and is not fixed by the sources. [19: S01 p.11] [20: S01 p.15]
- **MIR:** Nominal MIR range 4000-400 cm-1 (2.5-25 µm). The usable range depends on the fiber and the ATR crystal actually selected. [21: S01 p.9]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [22: S01 p.10]
- **Raman:** The nominal method range is not the range of a specific instrument, fiber or probe. [23: REF §5]

## Risks and uncertainty

- Raman signal is weak and can be swamped by fluorescence from the medium or cell components; the fluorescence background must be measured on the real medium before any commitment. *(rules: R-RAM-1)* [24: S01 p.11]
- Calibration is specific to the matrix. The medium and cell population change during the run, so a model built on one state may not hold for another; re-validation on new material is required. *(rules: R-CAL-1)* [25: REF §5]
- NIR may lack sensitivity for the low end of the glucose/lactate range; the cited example mentions trace compounds below 0.1 percent. *(rules: R-NIR-4)* [26: S01 p.16]
- Changing cell density changes turbidity; in a reflection or transmission geometry this physical variation can mimic a composition change and needs scatter handling. *(rules: R-GEO-6, R-GEN-4, R-GEN-5)* [27: S01 p.17]
- MIR-ATR samples only a surface layer a few micrometres deep, so deposits on the crystal and surface representativeness are real risks in a cell-culture medium. *(rules: R-MIR-3)* [28: S04 p.1]
- If two methods are combined, they must measure the same small area and their data must be synchronised to a common time step; this is a hypothesis to test, not a given gain. *(rules: R-CMB-2, R-CMB-3, R-CMB-1)* [29: S01 p.8] [30: S01 p.8] [31: REF §5]
- The supplied application examples are laboratory and research work. They are reasons to test a method, not evidence that a system is ready for this process. *(rules: R-EVI-1, R-EVI-2)* [32: REF §3]

## First feasibility experiment

1. **1. Sample set** Cover the expected chemical and physical variation: medium samples across the run (early, mid, late), across the expected glucose and lactate ranges, at different cell densities/turbidities, from more than one run or batch; include blank medium and spiked samples to extend the range at both ends. *(no verified source: engineering judgement)*
2. **2. Independent reference** Measure every sample with the existing laboratory glucose and lactate method, and record the time offset between the spectroscopic measurement and the reference sample. If available, add a second independent reference method for a subset. [33: REF §3]
3. **3. Single methods first** Build and evaluate one model per single method (Raman probe; MIR-ATR; NIR transmission/transflection only if the optical-density answer allows it) against the reference values. Do not start with the combination. *(no verified source: engineering judgement)*
4. **4. Combination afterwards** Only if at least one single method shows usable performance, test the Raman + MIR-ATR combination (fused data, same measurement point) against the best single method. Treat any gain as a hypothesis. [34: REF §5]
5. **5. Validation on held-out runs** Split by whole run or batch, not by single spectra: keep repeated measurements from the same run and the same sampling point together in the same fold, and report the prediction statistics on the held-out runs. *(no verified source: engineering judgement)*
6. **6. Go / no-go basis** The numerical criteria (accuracy, precision, response time, lowest concentration that must be resolved) are not in the supplied material and must be defined by the customer before the trial (Q1). The trial output is compared against those numbers; no such figure may be assumed from the sources. *(no verified source: engineering judgement)*

**Reference measurements:** Existing laboratory glucose and lactate measurements, with sample times recorded relative to the spectra.

**Decision basis:** Customer-supplied numerical targets; not available from the sources.

## Assumptions

- The medium is a liquid that can contact a probe, and a probe can be installed at a representative point.
- The customer's existing laboratory measurements are accurate enough to act as the reference (to be confirmed, Q4).
- Glucose and lactate are present at concentrations within the working range of at least one of the shortlisted methods; this is not established by the sources.

## Not covered by the supplied sources

- Any accuracy, precision, detection limit or response time for glucose or lactate by Raman, NIR or MIR in this or a similar cell-culture medium.
- The customer's concentration ranges, medium composition, optical density and fluorophore content.
- An achievable length for a MIR (CIR/PIR or hollow-waveguide) fiber link; only 1-2 m laboratory lengths appear in the material.
- Probe temperature, pressure, cleaning, sterilization and compatibility ratings.
- Any statement that a supplied system is suitable or qualified for production, GMP, clinical or surgical use.
- Prices, product codes and lead times.

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "Fiber optic probes and cells are being integrated into reactors and production lines of ongoing technological processes, enabling on-site online analysis and obtaining results in near real time."
2. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
3. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
4. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
5. ✓ **S01 p.16** (application precedent): "for direct detection of specific metabolites like glucose, acetate, or lactate"
6. ✓ **S01 p.11** (general): "measuring Raman spectra is hampered by the low intensity of Raman signals"
7. ✓ **S01 p.11** (general): "by the superposition of luminescence (fluorescence), which has a significantly higher intensity"
8. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
9. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR) by connecting appropriate attachments and probes."
10. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
11. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
12. ✓ **S01 p.16** (application precedent): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
13. ✓ **S01 p.18** (application precedent): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
14. ✓ **S01 p.18** (general): "The key experimental action is the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
15. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
16. ✓ **REF §5** (general): "The fiber determines which wavelengths reach the probe."
17. ✓ **S02 p.7** (general): "Free of Polymer jacket fluorescence for Raman and Fluo- Spectroscopy"
18. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
19. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
20. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
21. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
22. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
23. ✓ **REF §5** (general): "actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample"
24. ✓ **S01 p.11** (general): "by the superposition of luminescence (fluorescence), which has a significantly higher intensity"
25. ✓ **REF §5** (general): "calibration specific to the matrix"
26. ✓ **S01 p.16** (application precedent): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
27. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size"
28. ✓ **S04 p.1** (general): "ATR analysis with its penetration depth of a few micrometers acts as the single-cell level"
29. ✓ **S01 p.8** (general): "It is crucial that the spectral information obtained by different methods-Mid-IR, NIR, Raman, and fluorescence spectra-is collected from the same small, even pinpoint, area of the sample."
30. ✓ **S01 p.8** (general): "the acquisition rates of different spectra can vary greatly-from milliseconds to minutes"
31. ✓ **REF §5** (method gain): "a gain is a hypothesis to test"
32. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer"
33. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
34. ✓ **REF §5** (method gain): "compare with the best single method"

## Verification

- Citations verified: 34 of 34 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 2; repair rounds: 1.

*Run D04 · models deepseek/deepseek-v4.1-flash · cost $0.0169*
