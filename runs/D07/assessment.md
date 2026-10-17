# First technical assessment: API concentration during hot polymer extrusion

**Customer enquiry**

> We are developing a hot polymer extrusion process that incorporates an active pharmaceutical ingredient. We want to investigate whether an optical measurement can detect composition changes while the melt is being processed. We have offline assays, but the process interface is hot and may be exposed to material build up. We need an initial comparison plan and the questions required before choosing a probe.

**Decision status:** Provisional feasibility assessment. A short method shortlist can be justified from the supplied material, with assumptions stated. MIR-ATR passed screening and there is a directly comparable application example (API in a hot polymer, in-line polymer-extrusion control). NIR reflection and Raman are worth comparing; NIR is conditional because the melt's optical state is unknown. The specific probe, ATR crystal, fiber, cable length and installation point cannot be chosen from the facts given, so this is a basis for a first comparison, not a probe selection.

## Premise check

- **Supported:** An optical measurement can detect composition changes while the melt is being processed.. A supplied application example shows spectra of an API in hot polymer taken with a diamond-cone ATR probe coupled to an FTIR spectrometer, and in-line polymer extrusion controlled with NIR reflection and MIR-ATR together. This is a precedent for testing the approach, not proof that it will work for this process. [1: S02 p.14] [2: S02 p.14]
- **Not covered:** The process interface is hot and may be exposed to material build up.. No supplied source gives a temperature or pressure rating for any probe, crystal, seal or fiber, and none addresses deposit build-up on a probe in an extruder. The sources only warn that ATR is limited by contact and fouling, and that metal-coated silica fibers are stated to have high temperature resistance, without a number. [3: REF §5] [4: S02 p.7]
- **Not covered:** Offline assays are available for comparison.. This is a customer fact about their own laboratory; no supplied source addresses it. It is nevertheless exactly what a feasibility plan needs as an independent reference. [5: REF §3]
- **Supported:** An initial comparison plan and the questions required before choosing a probe can be provided.. The supplied guidance says exactly this: when the facts cannot justify a method choice, ask the deciding questions and propose the next step rather than guessing. [6: REF §3]

## Requirements

**Stated by the customer**

- Detect composition changes in a hot polymer melt containing an active pharmaceutical ingredient, during processing.
- Initial comparison plan.
- Questions to be answered before choosing a probe.

**Key unknowns**

- Target species, expected concentration range and required accuracy.
- Melt optical state at the measurement point (clear vs opaque/scattering) and its behaviour on cooling.
- Actual temperature and pressure at the interface; cleaning and build-up behaviour.
- Planned measurement point and distance to the spectrometer.
- Whether the API or any formulation component fluoresces.
- Reference assay capability and required response time.

## Clarification questions (most decision-relevant first)

Q1. What is the API target and the composition change that must be detected, over what concentration range and with what accuracy? *Why it matters:* This decides sensitivity. NIR is stated to be effective for major components but may lack the sensitivity for trace compounds; MIR-ATR and Raman have different strengths. Without a number no method can be ranked on performance. *(affects: method, status)*
Q2. At the intended measurement point, is the melt clear/semi-transparent or opaque and strongly scattering, and does it stay soft enough to make tight contact with an ATR crystal? *Why it matters:* This decides the technique: ATR needs tight contact with a liquid or soft solid; NIR transmission/transflection needs a clear liquid and a controlled pathlength; NIR diffuse reflection suits opaque, scattering material. Both NIR options are currently screening as 'unknown' for exactly this reason. *(affects: method, technique, installation)*
Q3. What are the actual temperature and pressure at the interface, and what cleaning or purging cycle must the probe survive? *Why it matters:* No source gives a temperature, pressure or cleaning rating for any probe, crystal, seal or fiber, so a probe cannot be specified without this. It also determines whether deposit build-up on the measuring surface is the limiting factor. *(affects: installation, status)*
Q4. Where is the measurement point (barrel, die adaptor, feed section) and what distance is available between it and the spectrometer? *Why it matters:* MIR light needs chalcogenide, polycrystalline or hollow-waveguide fibers; silica fiber cannot carry it. No source states an achievable length for an MIR link, so the distance must be confirmed with AFS rather than assumed. *(affects: fiber, installation)*
Q5. Is the API, or any additive or degradation product in the melt, known to fluoresce? *Why it matters:* Fluorimetry only measures species that fluoresce, and a strong fluorescence background can swamp a Raman signal. This decides whether fluorescence is worth including and whether Raman is usable on this matrix. *(affects: method, technique)*
Q6. What is the reference method for each sample, its repeatability, and how quickly must the in-line result be available? *Why it matters:* The spectroscopic error has to be judged against the reference method, and the required response time affects acquisition and averaging. No source gives accuracy, detection limits or response times for this application. *(affects: status, installation)*

## Recommendation

- **R1 · Primary candidate: MIR + NIR (combination: a hypothesis to test), ATR.** Closest supplied match. The application example shows API in a hot polymer measured with a diamond-cone ATR probe coupled to an FTIR spectrometer, and in-line polymer extrusion controlled with MIR-ATR. MIR absorption is strong, so ATR is the usual in-line route for liquids and soft solids, and ATR probes are used for in-line, in-process measurement. *Conditions:* The melt must make tight contact with the ATR crystal and must not harden or deposit on it faster than the measurement interval. ATR samples only a very shallow surface layer, so a deposit can dominate the spectrum. The usable spectral range depends on the fiber and crystal actually selected. [7: S02 p.14] [8: S02 p.14] [9: S01 p.5] [10: S01 p.10] [11: S01 p.10] [12: REF §5]
- **R2 · Comparison candidate: Raman, raman probe.** Second vibrational method, complementary to MIR in the information it carries, and it passed screening. The pharmaceutical example uses a Raman fiber probe for contact measurements with 785 nm excitation inserted directly into the process environment, with the spectrometers placed away from the process point. *Conditions:* The fluorescence background of the real melt must be checked first; Raman signals are weak and can be swamped by fluorescence. Contact with a hot, possibly fouling melt raises the same probe-life questions as R1. Excitation wavelength is not fixed by the sources; 785 nm is only the wavelength used in the cited example. [13: S01 p.15] [14: S01 p.15] [15: S01 p.15] [16: S01 p.11]
- **R3 · Conditional candidate: NIR, diffuse reflection.** NIR is described as the most common online analysis method using fiber-optic probes, penetrates several millimetres even into dense scattering samples, and works with ordinary glass optics and standard lamps. It is also the technique used alongside MIR-ATR in the cited in-line polymer-extrusion example. *Conditions:* Applies only if the melt at the measurement point is opaque or strongly scattering. If the melt is clear or semi-transparent, the appropriate NIR geometry is transmission or transflection with a controlled pathlength, which is a different technique and is also currently 'unknown' in screening. Deciding question: Q2. [17: S01 p.10] [18: S01 p.5] [19: S02 p.14]
- **R4 · Not recommended: Fluorescence, fluorescence probe.** No fluorescent species or indicator has been identified in the formulation. Fluorimetry only measures species that fluoresce, and most chemicals do not exhibit this property. A multispectral probe combining MIR-ATR with fluorescence exists and is a plausible expectation, but it cannot be justified for this enquiry until Q5 is answered. *Conditions:* Reconsider only if the API or an additive is known to fluoresce, or if a fluorescent indicator is deliberately justified. [20: S01 p.5] [21: S04 p.4]

## Measurement concept

- **Probe and geometry:** Contact ATR head (crystal) in the melt stream is the first candidate, following the cited API-in-hot-polymer example. A flush-mounted diffuse-reflection probe is the alternative for an opaque melt. Transmission/transflection is only an option if the melt is clear. This is a plan to test, not a probe selection.
- **Location:** Extruder barrel or die adaptor, downstream of the material feeder. The exact point must be agreed with the customer and with AFS, because the required distance to the spectrometer drives the fiber choice.
- **Fiber link:** MIR light cannot travel in silica fiber; it needs chalcogenide, polycrystalline or hollow-waveguide fiber. The sources state 100-300 m cables only for low-OH silica fibers, so the achievable length of an MIR link is unknown and must be confirmed, not assumed. For Raman and NIR, metal-coated silica fibers avoid polymer-jacket fluorescence. [22: REF §5] [23: S02 p.7] [24: S02 p.7]

## Spectral range

- **MIR:** Nominal method range 4000-400 cm-1. The usable range depends on the ATR crystal and the infrared fiber actually selected; the nominal method range is not the range of a specific configuration. [25: S01 p.9] [26: REF §5]
- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected, and on whether reflection or transmission geometry is used. [27: S01 p.10] [28: REF §5]
- **Raman:** The spectral axis is the Raman shift in cm-1; the excitation wavelength is stated separately and is not fixed by the sources. The cited pharmaceutical example used 785 nm excitation. The excitation wavelength for this process is an open choice. [29: S01 p.11] [30: S01 p.15]

## Risks and uncertainty

- Build-up on the measuring surface. *(rules: R-MIR-3)* [31: REF §5] [32: S01 p.13]
- Temperature and pressure limits are unknown. The sources show a PEEK-sealed zirconia/diamond ATR probe used in microwave furnaces and metal-coated fibers described as high-temperature resistant, but no numeric rating is given anywhere, so no probe can be specified on temperature grounds. *(rules: R-PRO-3)* [33: S02 p.13]
- Calibration is matrix-specific: after a change of polymer grade, additive package or API level, the model must be re-validated on the new material. *(rules: R-CAL-1)* [34: REF §5]
- NIR may not see small composition changes: it is stated to be effective for major components but may lack sensitivity for trace compounds. *(rules: R-NIR-4)* [35: S01 p.16]
- Fluorescence background can mask the Raman signal; this must be checked on real melt samples before Raman is relied on. *(rules: R-RAM-1)* [36: S01 p.11]
- Any gain from combining methods is a hypothesis, not an established result for this process. It must be compared against the best single method, and the different methods must sample the same small area and be synchronised in time. *(rules: R-CMB-1, R-CMB-2, R-CMB-3)* [37: S01 p.8] [38: S01 p.8]
- Melt inhomogeneity and flow turbulence at the measurement point can make the signal vary for physical reasons rather than compositional ones. *(rules: R-GEN-5)* [39: S01 p.7]
- The cited examples are laboratory or application illustrations. They are a reason to test MIR-ATR, NIR and Raman on this process, not evidence that any of them is ready for this production line. *(rules: R-EVI-1, R-EVI-2)* [40: REF §3]

## First feasibility experiment

1. **1. Representative sample set** Span the expected chemical and physical variation before any probe decision: API concentration levels across the specification range (levels and tolerances to be set by the customer), at least two polymer lots or grades, melt temperatures across the process window, and deliberately off-specification material. Include a sample of the material that builds up on the interface. [41: REF §3]
2. **2. Independent reference measurements** Use the existing offline assays on every sample as the reference. Record their repeatability, so the spectroscopic error can be judged against it rather than against zero. [42: REF §3]
3. **3. Single methods first** Measure MIR-ATR first on a laboratory spectrometer with an ATR probe. Then measure NIR (reflection if the melt is opaque, transmission/transflection if clear) and Raman, each as a single method. Do not start with a combined probe. This is the multi-method laboratory trial stage used to select the method. [43: S02 p.20] [44: S01 p.3]
4. **4. Build and compare models** Build one chemometric model per single method against the offline reference. Only afterwards build a fused model on the combined data and compare it against the best single method. The gain from fusion is a hypothesis. [45: S01 p.15] [46: S01 p.10]
5. **5. Validate on held-out runs or batches** Split the data by run or batch, not by individual measurement. Repeated measurements taken at the same position must be excluded together, otherwise the validation is too optimistic. [47: S03 p.13]
6. **6. Go / no-go basis** The numerical criteria must come from the customer, not from the sources: allowed prediction error against the offline assay, the smallest API change that must be detected, and the acceptable rate of missed changes. The sources give no accuracy, detection limit or response time for this application. [48: REF §3]
7. **7. In-line check only after laboratory feasibility** If a single method or a justified combination passes step 6, install it at the agreed point and check signal stability and deposit build-up over a full production run before any further commitment. *(no verified source: engineering judgement)*

**Reference measurements:** The customer's existing offline assays; no additional reference is required by the sources.

**Decision basis:** To be set by the customer: maximum allowed prediction error versus the offline assay, minimum detectable API change, and acceptable missed-change rate. No numeric performance target can be taken from the supplied sources.

## Assumptions

- The melt reaches and wets the measuring surface (ATR crystal or window) at the intended point.
- The existing offline assay is fit to serve as the reference for API content.
- A laboratory spectrometer with the relevant probe can be used for the first comparison before any in-line installation.
- No fluorescent species is assumed present; if one is, R4 changes.

## Not covered by the supplied sources

- Maximum operating temperature and pressure of any ATR probe, crystal, seal or fiber.
- Achievable cable length for an MIR (chalcogenide / polycrystalline / hollow-waveguide) link.
- Detection limits, accuracy or response time for an API in a polymer melt.
- Behaviour of polymer melt build-up on a probe surface, and any cleaning strategy.
- PEEK or other seal temperature limits.
- Any requirement of pharmaceutical production (GMP, validation, regulatory filing).
- The specific API, polymer matrix or additive package of this customer.

## Evidence (verified quotes)

1. ✓ **S02 p.14** (application precedent): "Spectra of API in hot polymer obtained with Diamond cone ATR probe coupled to iC10 FTIR (MTAC)"
2. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
3. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
4. ✓ **S02 p.7** (general): "Alu- & Cu-alloy coated fibers - High temperature resistance - Increased durability, high strength, hermetically sealed"
5. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
6. ✓ **REF §3** (general): "If the known facts cannot justify a method choice, say so, ask the questions that would decide it and propose the next step."
7. ✓ **S02 p.14** (application precedent): "Spectra of API in hot polymer obtained with Diamond cone ATR probe coupled to iC10 FTIR (MTAC)"
8. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
9. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR) by connecting appropriate attachments and probes."
10. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
11. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments, as well as in-situ measurements, such as for field testing or for spectral diagnostics during surgery."
12. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
13. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
14. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
15. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
16. ✓ **S01 p.11** (general): "measuring Raman spectra is hampered by the low intensity of Raman signals, which are several orders of magnitude weaker than IR absorption peaks in the IR range"
17. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
18. ✓ **S01 p.5** (general): "making it ideal for online applications, including remote measurements via fiber optic probes."
19. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
20. ✓ **S01 p.5** (general): "Another highly sensitive method, UV/Vis fluorimetry, is based on the secondary emission of excited molecules of certain substances, most often of biological origin. However, most chemicals do not exhibit this property."
21. ✓ **S04 p.4** (general): "Of course, it is limited to the samples containing at least one fluorescent component that often has a biological or natural origin."
22. ✓ **REF §5** (general): "The fiber determines which wavelengths reach the probe."
23. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
24. ✓ **S02 p.7** (general): "Free of Polymer jacket fluorescence for Raman and Fluo- Spectroscopy"
25. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
26. ✓ **REF §5** (general): "The fiber determines which wavelengths reach the probe."
27. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
28. ✓ **REF §5** (general): "The fiber determines which wavelengths reach the probe."
29. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
30. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
31. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
32. ✓ **S01 p.13** (general): "typically at a depth of few microns"
33. ✓ **S02 p.13** (general): "ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"
34. ✓ **REF §5** (general): "calibration specific to the matrix"
35. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
36. ✓ **S01 p.11** (general): "measuring Raman spectra is hampered by the low intensity of Raman signals, which are several orders of magnitude weaker than IR absorption peaks in the IR range"
37. ✓ **S01 p.8** (general): "It is crucial that the spectral information obtained by different methods-Mid-IR, NIR, Raman, and fluorescence spectra-is collected from the same small, even pinpoint, area of the sample."
38. ✓ **S01 p.8** (general): "data synchronization can be challenging, as the acquisition rates of different spectra can vary greatly-from milliseconds to minutes, while the interval between measurements can also differ"
39. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
40. ✓ **REF §3** (general): "A published application is a reason to test a method, not proof that it will work for a new customer."
41. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
42. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
43. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
44. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
45. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
46. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
47. ✓ **S03 p.13** (general): "Repeated measurements in the same sample position produced similar spectra or sensor data; therefore, these should always be simultaneously excluded for every CV iteration."
48. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 48 of 48 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 3; repair rounds: 1.
- Removed 1 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry

*Run D07 · models deepseek/deepseek-v4.1-flash · cost $0.0180*
