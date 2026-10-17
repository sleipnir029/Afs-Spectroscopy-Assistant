# First technical assessment: Water content in a petroleum stream

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified: there is a published laboratory application of MIR-ATR probes for measuring water content in petroleum, and NIR is the most common in-line fiber method with a documented sensitivity to water. However, the stream's physical and optical state, the required water range/accuracy/response time and the achievable fiber link length are not known, so the method choice, geometry and any combination are provisional and must be confirmed by the questions and the feasibility experiment below.

## Premise check

- **Supported:** A fiber based measurement closer to the process will make changes noticed sooner. The sources state that online/in-process fiber analysis removes sampling delay and gives results in near real time. This is a general statement, not a result for this stream. [1: S01 p.2]
- **Supported:** The analyzer can be outside the process area. The sources state that fiber probes allow analysis at a distance from the spectrometer, so the analyzer can be remote in principle. The achievable distance for a given fiber type is not stated and remains an open question (see risks). [2: S01 p.10]
- **Supported:** A first comparison experiment should establish what to clarify before selecting equipment. A feasibility comparison on representative samples with an independent reference and a defined go/no-go basis is the recommended structure before committing to a configuration. [3: REF §3]

## Requirements

**Stated by the customer**


**Key unknowns**

- Water concentration range to be measured and the required detection limit (in particular whether trace water below the current laboratory reporting limit must be seen).
- Required accuracy and response time behind 'changes can be noticed sooner'.
- Physical and optical state of the stream at the measurement point: clear liquid, emulsified water-in-oil, or turbid, and whether this changes with operating conditions.
- Process temperature, pressure and stream composition/interferences (hydrocarbon type, additives, solids, dissolved gases).
- Distance from the proposed probe point to the location available for the analyzer outside the process area, and the fiber link length that can be supported.
- The laboratory water-determination method currently used and how often samples are taken (needed as the independent reference).

## Clarification questions (most decision-relevant first)

Q1. What water concentration range must be measured, and what detection limit and accuracy are required - in particular, must the method resolve water below the reporting limit of the current laboratory method? *Why it matters:* This decides whether NIR can be sensitive enough or whether the MIR-ATR route is needed, and it sets the go/no-go criteria. *(affects: method, technique, status)*
Q2. What is the physical and optical state of the stream at the measurement point - clear and transparent, emulsified water-in-oil, or turbid - and does it change with operating conditions? *Why it matters:* This decides transmission/transflection versus diffuse reflection, and whether a contact ATR interface is appropriate. *(affects: technique, installation)*
Q3. What are the temperature and pressure at the measurement point, and what is the stream composition (hydrocarbon type, additives, solids, dissolved gases)? *Why it matters:* This decides probe/crystal materials, sealing and compatibility, and whether the ATR crystal will foul. *(affects: technique, installation)*
Q4. What distance is available between the probe point and the location for the analyzer outside the process area, and what response time is required? *Why it matters:* The achievable fiber link length for a MIR (CIR/PIR) link is not stated in the sources, so it must be confirmed before the layout is fixed. *(affects: installation, method)*
Q5. Which laboratory method is used today for water determination, and how frequently are samples taken? *Why it matters:* This is the independent reference for the comparison experiment and defines the achievable agreement. *(affects: status, technique)*

## Recommendation

- **R1 · Primary candidate: MIR, ATR.** Strongest single lead. A published laboratory application shows ATR probes used for measurement of water content in petroleum, and MIR is described as one of the most informative methods of chemical analysis. ATR fiber probes enable liquid analysis at a distance from the spectrometer, which matches the request for an analyzer outside the process area. This is a reason to test the method on the customer's stream, not proof that it will work there. *Conditions:* Requires a liquid or soft-solid stream that gives tight contact with the ATR crystal; usable range depends on the instrument, fiber and probe selected. [4: S02 p.13] [5: S01 p.9] [6: S01 p.10] [7: S01 p.10]
- **R2 · Comparison candidate: NIR, transmission transflection.** Single-method alternative to compare against MIR-ATR. NIR is the most common online analysis method performed with fiber probes, works with standard glass optics and lamps, and transmission/transflection is preferred for transparent or semi-transparent liquids. NIR must be calibrated chemometrically and is matrix-specific. *Conditions:* Applies if the stream at the measurement point is transparent to semi-transparent; the optical pathlength must be controlled. [8: S01 p.10] [9: S01 p.5] [10: S01 p.18]
- **R3 · Conditional candidate: NIR, diffuse reflection.** Applies only if the stream at the measurement point turns out to be opaque, turbid or strongly scattering (for example an emulsified water-in-oil stream) so that transmission loses signal. In that case the reflection geometry becomes the relevant NIR option; reflection signals are sensitive to surface and particle/globule characteristics, so scatter correction and matrix-specific calibration are needed. *Conditions:* Only if Q2 shows the stream is opaque or strongly scattering. [11: S01 p.17] [12: S01 p.18]
- **R4 · Not recommended: Fluorescence, fluorescence probe.** Water is not a native fluorophore and fluorescence measures only species that fluoresce or a justified fluorescent indicator; no such indicator is proposed for this stream, so fluorescence is not a direct route to water determination here. [13: S01 p.5] [14: S04 p.4]

## Measurement concept

- **Probe and geometry:** MIR-ATR contact probe as the primary route for a liquid/petroleum stream; NIR transmission/transflection as the comparison geometry, with NIR diffuse reflection only if the stream is opaque or scattering.
- **Location:** Probe at the process point; analyzer located outside the process area, linked by fiber. The achievable MIR link length is not stated in the sources and must be confirmed.
- **Fiber link:** MIR requires a fiber that transmits in the mid-IR (chalcogenide CIR or polycrystalline PIR); silica fibers end near 2.4 um and cannot carry MIR. The long-cable figure (100-300 m) is stated only for low-OH silica fibers. [15: S02 p.6] [16: S02 p.6] [17: S02 p.7]

## Spectral range

- **MIR:** Nominal MIR range 4000-400 cm-1 (2.5-25 um). The usable range depends on the instrument, fiber and probe actually selected. [18: S01 p.9] [19: REF §3]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [20: S01 p.10]

## Risks and uncertainty

- The petroleum-water evidence is laboratory spectra of model oil samples; it is a reason to test the method, not proof that it works for this stream under process conditions. *(rules: R-EVI-1, R-EVI-2)* [21: S02 p.13] [22: REF §3]
- If the stream is turbid, emulsified or strongly scattering, NIR transmission loses signal and the geometry (and possibly the method) must change; scatter also perturbs reflection signals, so physical variation can be mistaken for a composition change. *(rules: R-GEO-2, R-GEO-6)* [23: S01 p.18] [24: S01 p.17]
- MIR-ATR samples only a few micrometres at the crystal, so deposits, fouling and surface representativeness can make the reading unrepresentative, and the probe materials must be compatible with the stream. *(rules: R-MIR-3)* [25: S01 p.13] [26: REF §5]
- If water is a trace component, NIR may lack the required sensitivity; and the achievable MIR fiber link length between probe and a remote analyzer is not stated in the sources, which constrains the 'analyzer outside the process area' layout. *(rules: R-NIR-4, R-FIB-2)* [27: S01 p.16] [28: S02 p.7]

## First feasibility experiment

1. **1** Fix the measurement targets and the reference before any equipment choice. [29: REF §3]
2. **2** Take representative samples across the expected chemical and physical variation - low-to-high water content, clear to emulsified/turbid states, the process temperature range and different stream compositions - and hold out whole runs or batches for later validation. [30: REF §3]
3. **3** Measure each single method on the same samples against the reference: MIR-ATR first, then NIR (transmission/transflection), using the same measurement point, with chemometric calibration and cross-validation. Use multi-method laboratory trials to select the most suitable method or combination. [31: S01 p.3]
4. **4** Only if the single methods do not meet the required criteria, test a combined MIR-ATR + NIR measurement against the best single method, aligning sampling location and timing. A gain from combining is a hypothesis to test, not an expected result. [32: REF §5] [33: REF §5]
5. **5** Validate the chosen model on the held-out runs or batches and apply the go/no-go criteria (detection limit, accuracy, response time) supplied by the customer before any equipment selection. [34: REF §3]

**Reference measurements:** The customer's current laboratory water-determination method is used as the independent reference for every sample; its sampling frequency defines the achievable agreement.

**Decision basis:** Go/no-go criteria come from the customer (required detection limit, accuracy and response time) and are applied to the held-out validation set; no performance figure is assumed from the sources.

## Assumptions

- The stream is a liquid or soft-solid that can contact an ATR crystal at the measurement point.
- A probe point and an analyzer location outside the process area can be arranged with a fiber link; the achievable MIR link length is unconfirmed.
- The laboratory water-determination method can serve as the independent reference.

## Not covered by the supplied sources

- An achievable fiber-optic link length between the probe and a remote MIR analyzer: no source gives a length for a CIR/PIR (MIR) link; the long-cable figure in the sources is stated only for low-OH silica fibers.
- Water-in-petroleum measurement under process (in-line) conditions: the sources show only laboratory ATR spectra of model oil samples.

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "enabling on-site online analysis and obtaining results in near real time."
2. ✓ **S01 p.10** (general): "allow analysis at a significant distance from the spectrometer"
3. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
4. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum"
5. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
6. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
7. ✓ **S01 p.10** (general): "allow analysis at a significant distance from the spectrometer"
8. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
9. ✓ **S01 p.5** (general): "making it ideal for online applications, including remote measurements via fiber optic probes."
10. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
11. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
12. ✓ **S01 p.18** (general): "as the light cannot penetrate the sample."
13. ✓ **S01 p.5** (general): "However, most chemicals do not exhibit this property."
14. ✓ **S04 p.4** (general): "it is limited to the samples containing at least one fluorescent component"
15. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
16. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 µm"
17. ✓ **S02 p.7** (general): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
18. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
19. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
20. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
21. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum"
22. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer."
23. ✓ **S01 p.18** (general): "as the light cannot penetrate the sample."
24. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
25. ✓ **S01 p.13** (general): "typically at a depth of few microns"
26. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
27. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
28. ✓ **S02 p.7** (general): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
29. ✓ **REF §3** (general): "independent reference measurements"
30. ✓ **REF §3** (general): "Representative samples or process states"
31. ✓ **S01 p.3** (general): "in order to select the most suitable method or combination of methods."
32. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
33. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
34. ✓ **REF §3** (general): "the basis for the go / no-go decision."

## Verification

- Citations verified: 34 of 34 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 3; repair rounds: 1.

*Run D06-20261017T090057Z · models deepseek/deepseek-v4.1-flash · cost $0.0152*
