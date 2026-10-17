# First technical assessment: API concentration during hot polymer extrusion

**Customer enquiry**

> We are developing a hot polymer extrusion process that incorporates an active pharmaceutical ingredient. We want to investigate whether an optical measurement can detect composition changes while the melt is being processed. We have offline assays, but the process interface is hot and may be exposed to material build up. We need an initial comparison plan and the questions required before choosing a probe.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified: MIR-ATR and a Raman probe pass screening for an in-line measurement, and the supplied material contains a related precedent of MIR-ATR (and NIR reflection) on an API in hot polymer during extrusion. The shortlist rests on stated assumptions, because interface temperature, melt optical behaviour, target magnitude and fiber-link distance are not known. A precedent is a reason to test, not proof for this process.

## Premise check

- **Not covered:** Composition changes in the melt can be detected optically in-process. No supplied source addresses this specific hot API/polymer melt or whether the customer's composition change is optically detectable. S02 p.14 is a closely related application precedent (MIR-ATR/NIR reflection on API in hot polymer extrusion) and is a reason to test, not proof for a new process. This remains the open question the trial must answer. [1: S02 p.14] [2: REF §3]
- **Not covered:** Offline assays can serve as a reference for an in-line measurement. No supplied source says anything about comparability between a customer's offline assay and an in-line spectrum (sampling point, time lag, sample state). The feasibility guidance only requires independent reference measurements; it does not establish that these particular offline assays are comparable. This must be checked in the trial and confirmed by the customer. *(no verified source: engineering judgement)*
- **Supported:** The hot interface and possible material build-up are the governing constraints on method choice. Supported for contact (ATR-type) measurement: contact and fouling limit the usable range, and ATR samples only a very thin surface layer. Caveat: no supplied source states a temperature rating or limit for any probe or fiber, so the temperature value itself is still an open question, not a supported constraint value. [3: REF §5] [4: S01 p.13]

## Requirements

**Stated by the customer**

- Detect composition changes in the melt while it is being processed.
- Interface is hot and may be exposed to material build-up.
- Offline assays exist as reference.
- They want an initial comparison plan and the questions needed before choosing a probe.

**Key unknowns**

- Temperature and pressure at the intended measurement point.
- Optical behaviour of the melt at that point (clear/translucent vs opaque/scattering) and whether tight probe contact is possible.
- Target API species, its concentration range, and the size and rate of the composition change that must be detected.
- Distance from the measurement point to where a spectrometer could be housed (fiber-link length).
- Required accuracy, detection limit and response time, and the offline assay used as reference.
- Rate and nature of material build-up and cleaning requirements at the interface.

## Clarification questions (most decision-relevant first)

Q1. What are the temperature and pressure at the intended measurement point, and what are their normal operating ranges? *Why it matters:* Decides crystal/probe type, fiber family, sealing and whether a contact probe is possible at all. No supplied source gives a temperature rating or limit, so this cannot be assumed. *(affects: method, technique, installation)*
Q2. How does the melt behave optically at that point - clear and translucent, or opaque and strongly scattering - and can the melt be held in tight contact with a probe tip? *Why it matters:* Decides ATR versus diffuse reflection versus transmission geometry, and whether NIR options become usable. *(affects: method, technique, status)*
Q3. Which API is the target, at what concentration range, and how large and how fast is the composition change that must be detected? *Why it matters:* Sets the sensitivity requirement and decides whether the change is optically detectable at all; trace levels may be below what NIR can see. *(affects: method, technique, status)*
Q4. How far is it from the measurement point to a possible spectrometer location, and what are the ambient conditions along that route? *Why it matters:* An MIR fiber link length is not stated anywhere in the supplied material; the long remote-process-control link described there is for low-OH silica cables, which cannot carry MIR. This decides whether the MIR option is installable. *(affects: installation, method)*
Q5. What exactly is the offline assay (method, sampling point, time lag) and what accuracy, detection limit and response time would make the in-line result acceptable? *Why it matters:* Defines the independent reference and the go/no-go criteria. The numerical criteria must come from the customer. *(affects: status, technique)*

## Recommendation

- **R1 · Primary candidate: MIR, ATR.** The only MIR in-line technique that passed screening. MIR absorption is strong, which forces very thin samples or ATR, and ATR is the usual in-line route for liquids and soft solids in tight contact. There is a related precedent for MIR-ATR on an API in hot polymer during extrusion - a reason to test this first, not proof for this process. *Conditions:* Applies if the melt can be held in stable contact with the ATR crystal and the interface temperature is within the rated range of the probe and fiber (rating value not in the sources - see Q1). [5: S01 p.5] [6: S04 p.4] [7: S02 p.14]
- **R2 · Comparison candidate: Raman, raman probe.** Passed screening as a single in-line method and is spectroscopically complementary to MIR, so it is the natural second single-method comparison. Its limits must be checked on the real melt: the Raman signal is orders of magnitude weaker than IR absorption and can be swamped by fluorescence. A combined ATR + Raman probe design exists in the supplied material but is a later hypothesis, not the first test. *Conditions:* Run as a second single method on the same samples. If the melt fluoresces strongly, Raman may not be usable. [8: S01 p.11] [9: S01 p.11] [10: S02 p.16]
- **R3 · Conditional candidate: NIR, diffuse reflection.** NIR reflection is the most common online fiber-probe method and is suited to opaque or highly scattering media, but its screening status is unknown because the melt's optical regime is not known. It becomes relevant only if the melt is opaque/scattering or cannot be contacted. Combining it with MIR (and Raman) is a hypothesis to be tested against the best single method after the single-method tests, with sampling location and timing aligned. *Conditions:* Applies only if the melt proves opaque or strongly scattering, or if the interface cannot be contacted and a non-contact window measurement is needed. Deciding question: Q2. [11: S01 p.10] [12: S01 p.17] [13: REF §5] Later hypothesis, after single-method tests: combine with MIR, Raman.
- **R4 · Not recommended: NIR, transmission transflection.** Not recommended for the in-line interface as described. NIR transmission needs a precisely controlled optical pathlength through the sample, and it fails when the sample is too thick or opaque because the light cannot penetrate it. A probe in a hot extrusion melt does not provide a defined, controllable pathlength; if the melt turns out clear and a defined path can be engineered, this option can be revisited. *Conditions:* Revisit only if a defined transmission path through a clear, non-scattering melt can be engineered. [14: S01 p.18] [15: S01 p.18]

## Measurement concept

- **Probe and geometry:** First choice: an ATR fiber probe with the crystal in direct contact with the melt, mounted in the extruder barrel or die adaptor. Alternative to test only if contact is not possible or the melt is opaque: a non-contact diffuse-reflection window/probe. Both options keep the spectrometer away from the hot, vibrating process point via fiber link.
- **Location:** One defined measurement point in the melt stream (barrel or die adaptor) - to be agreed with the customer; the same point should be used for all methods compared.
- **Fiber link:** Fiber family depends on the method: MIR needs chalcogenide (CIR) or polycrystalline (PIR) fibers or a hollow waveguide; NIR/vis can use silica. No source states an achievable length for an MIR link, so the link length is an open question (Q4). [16: S01 p.15] [17: S01 p.8]

## Spectral range

- **MIR:** Nominal method range 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber and probe actually selected; the fiber family must be able to transmit the method's range. [18: S01 p.9] [19: REF §5]
- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [20: S01 p.10]
- **Raman:** Reported as a Raman shift in cm-1; the laser excitation wavelength is stated separately. The pharma example in the supplied material uses 785 nm excitation. Actual coverage depends on the spectrometer, laser and probe selected. [21: S01 p.11] [22: S01 p.15]

## Risks and uncertainty

- Contact and fouling: ATR samples only a few micrometres of the surface and its usable range is limited by contact and fouling. Build-up on the crystal can change or blank the signal, and stable contact on a viscous melt is not assured. *(rules: R-MIR-2, R-MIR-3)* [23: S01 p.13] [24: REF §5]
- Fiber-link length: no source states an achievable length for an MIR (CIR/PIR or hollow-waveguide) link. The MIR examples in the supplied material are short laboratory cable lengths, while the long remote-process-control figure is stated only for low-OH silica cables, which cannot carry MIR. The distance from the extruder to the spectrometer is therefore an open question, not an assumption. *(rules: R-FIB-1, R-FIB-2)* [25: S02 p.7] [26: S02 p.9] [27: S02 p.10]
- Detectability and calibration transfer: the composition change may be too small to see in a scattering polymer melt (in a cited bioprocess example NIR may lack sensitivity below 0.1 percent), and any model is matrix-specific, so a formulation, polymer-grade or temperature change requires re-validation. *(rules: R-NIR-4, R-CAL-1)* [28: S01 p.16] [29: REF §5]
- Temperature and process variability: no supplied source gives a temperature rating or limit for probes or fibers, so a hot interface could rule out a contact probe; sample inhomogeneity and process turbulence at the measurement point can dominate the signal. *(rules: R-GEN-5, R-PRO-3)* [30: S01 p.7]

## First feasibility experiment

1. **1. Build a representative sample set** Cover the expected chemical and physical variation, not only the nominal recipe. *(no verified source: engineering judgement)*
2. **2. Reference every sample independently** Use the existing offline assay at the same time and, where possible, the same point as the spectral measurement; record feed ratios and gravimetric data. First check whether the offline assay and the in-line sample are comparable (sampling point, time lag). *(no verified source: engineering judgement)*
3. **3. Measure single methods on the same samples and points** MIR-ATR first, Raman second, on the same sample points with replicates to quantify repeatability; add NIR diffuse reflection only if the melt is opaque/scattering or cannot be contacted (Q2). *(no verified source: engineering judgement)*
4. **4. Model each method, then test the combination as a hypothesis** Build chemometric models per method and validate on held-out runs or batches, not on the calibration samples. Compare the fused MIR + NIR model against the best single method; a combined gain is a hypothesis, not an assumption. [31: REF §5]
5. **5. Set the go/no-go basis from customer figures** Define the pass criteria (detection limit, accuracy, response time) with the customer before the trial. If these numbers are not supplied, the go/no-go decision cannot be made. [32: REF §3]

**Reference measurements:** The customer's existing offline assay, taken at a matched point and time; supplemented by feed-ratio and gravimetric records.

**Decision basis:** Customer-supplied numerical criteria (detection limit, accuracy, response time) applied to held-out runs or batches. No numerical criterion can be proposed from the supplied material.

## Assumptions

- The melt is a liquid or soft solid at the measurement point that can make contact with a probe head.
- A defined measurement point in the melt stream can be agreed and used for all compared methods.
- A spectrometer can be housed at a distance from the hot zone with a fiber link; the achievable link length is still an open question.

## Not covered by the supplied sources

- Whether a composition change of this kind in a hot API/polymer melt is optically detectable at all - no supplied source addresses this melt or API.
- Probe and fiber temperature (and pressure) ratings for extrusion conditions - the supplied material gives no rating values.
- Comparability of the customer's offline assays with an in-line measurement at the extruder (sampling point, time lag, sample state).

## Evidence (verified quotes)

1. ✓ **S02 p.14** (application precedent): "Spectra of API in hot polymer obtained with Diamond cone ATR probe coupled to iC10 FTIR (MTAC)"
2. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer."
3. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
4. ✓ **S01 p.13** (general): "typically at a depth of few microns"
5. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm)"
6. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
7. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
8. ✓ **S01 p.11** (general): "This property makes mid-IR and Raman spectra complementary, that is, they complement each other."
9. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
10. ✓ **S02 p.16** (application precedent): "Combi probe with 2 IR-fibers coupled to FTIR-spectrometer and 2 Silica fibers coupled to Fluo or Raman spectrometers"
11. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
12. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
13. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
14. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm)"
15. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
16. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
17. ✓ **S01 p.8** (general): "collected from the same small, even pinpoint, area of the sample."
18. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
19. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
20. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
21. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
22. ✓ (precedent only) **S01 p.15** (performance figure): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
23. ✓ **S01 p.13** (general): "typically at a depth of few microns"
24. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
25. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
26. ✓ (precedent only) **S02 p.9** (performance figure): "HWG-750-2m PIR 600/700 -2m"
27. ✓ (precedent only) **S02 p.10** (performance figure): "1 Meter PolyMicro hollow fiber 1mm ID"
28. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
29. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
30. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
31. ✓ **REF §5** (general): "compare with the best single method."
32. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 32 of 32 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 5; repair rounds: 1.

*Run D07-20261017T094810Z · models deepseek/deepseek-v4.1-flash · cost $0.0140*
