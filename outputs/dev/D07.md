# First technical assessment: API concentration during hot polymer extrusion

**Customer enquiry**

> We are developing a hot polymer extrusion process that incorporates an active pharmaceutical ingredient. We want to investigate whether an optical measurement can detect composition changes while the melt is being processed. We have offline assays, but the process interface is hot and may be exposed to material build up. We need an initial comparison plan and the questions required before choosing a probe.

**Decision status:** Provisional feasibility assessment. A short comparison can be justified: a mid-IR ATR measurement as the first candidate, a Raman probe as the head-to-head alternative, and NIR reflection only if the melt turns out opaque/scattering. The facts that decide sensitivity, geometry and installation (temperature, optical behaviour of the melt, target concentration, distance to the spectrometer) are not yet known, so this is a plan to test, not a chosen probe.

## Premise check

- **Supported:** An optical measurement can detect composition changes while the melt is being processed. A directly comparable case is shown: mid-IR ATR spectra of an API in hot polymer, and NIR-Reflex & MIR-ATR spectroscopy used to control polymer extrusion in-line. This is a reason to test the methods on your material; it is not a result for your line or your formulation. [1: S02 p.14] [2: S02 p.14]
- **Not covered:** The process interface is hot. The enquiry does not quantify the temperature, and no supplied page states an operating temperature rating for a probe or a fiber. The only related statement is that Al/Cu-coated silica fibers are offered with high temperature resistance, without any number. The actual melt and interface temperature must come from you (or from AFS) before a probe can be selected. [3: S02 p.7]
- **Supported:** The process interface may be exposed to material build up. The concern fits the documented limits of ATR probes: they need tight contact with the sample and are subject to contact and fouling, and build-up would sit in the same surface layer the measurement sees. [4: REF §5] [5: S04 p.4]
- **Supported:** An initial comparison plan is needed before choosing a probe. The sources support testing several optical approaches on the customer's own sample before fixing a method, and the AFS pathway starts with multi-method laboratory trials. [6: S01 p.3] [7: S02 p.20]

## Requirements

**Stated by the customer**


**Key unknowns**

- Melt temperature and pressure at the intended measurement point (no source gives a probe or fiber rating).
- Whether the melt is transparent or opaque/highly scattering at the probe, and whether it wets or sticks to a surface.
- The composition variable to be followed, its expected concentration range, and the smallest change that must be detected.
- The distance from the measurement point to where the spectrometer can be installed (a mid-IR link length is not stated anywhere in the material).
- Reference (offline) assay used, and the accuracy and response time required for the in-line result.
- How the line is cleaned and whether a probe can be removed or cleaned during a run.

## Clarification questions (most decision-relevant first)

Q1. What are the melt temperature and pressure at the intended measurement point, and how far is that point from where the spectrometer could be installed? *Why it matters:* It decides the fiber family and the probe head, and whether the spectrometer link is feasible at all. No supplied page states a temperature rating or an achievable mid-IR link length. *(affects: method, technique, installation, status)*
Q2. Is the melt optically transparent or opaque/highly scattering where the probe would sit, does it wet or stick to a crystal or metal surface, and do the API or the polymer fluoresce? *Why it matters:* Opaque/scattering melt supports a reflection geometry; a transparent melt does not, and the geometry then has to be re-decided. Sticking affects ATR contact and build-up. Fluorescence raises the background of a Raman measurement. *(affects: technique, installation, status)*
Q3. Which composition change must be detected, at what concentration level, and how small a change must be seen? *Why it matters:* It decides whether the sensitivity of each method is sufficient; for example NIR may lack the sensitivity to detect a trace component. *(affects: method, status)*
Q4. Which offline assay do you use as reference, and what accuracy and response time must the in-line measurement meet? *Why it matters:* These numbers are the go/no-go basis of the test; they cannot be taken from the sources. *(affects: method, status)*
Q5. How is the extruder started, stopped and cleaned, and can a probe be withdrawn or cleaned during a run? *Why it matters:* It decides the installation concept and how build-up on the measurement surface is handled. *(affects: installation)*

## Recommendation

- **R1 · Primary candidate: MIR, ATR.** Mid-IR ATR is the strongest single candidate for a first test. No source rule excludes it for a liquid/paste in contact with a probe, and the closest published/company case is exactly this task: mid-IR ATR spectra of an API in hot polymer, and MIR-ATR used to control polymer extrusion in-line. Mid-IR spectra have well-defined absorption bands, which helps when composition changes must be separated, and ATR is the practical way around the strong mid-IR absorption, which otherwise limits mid-IR to very thin samples. *Conditions:* Applies if the melt keeps tight contact with the ATR crystal (the suitable case is liquid, paste or soft solid) and if a mid-IR fiber link to the spectrometer can be realised at the required distance. [8: S02 p.14] [9: S01 p.9] [10: S01 p.5] [11: S04 p.4]
- **R2 · Comparison candidate: Raman, raman probe.** Raman is the natural head-to-head alternative in the same test: no source rule excludes a Raman probe, and mid-IR and Raman spectra are complementary, so it is worth seeing which of the two follows your composition change better on the same samples. The caution is signal strength: Raman signals are weak and can be covered by fluorescence from the sample. *Conditions:* Applies if the API and the polymer do not show strong fluorescence at the chosen excitation wavelength. The Raman shift (cm-1) must be reported separately from the laser excitation wavelength (nm), which is not yet chosen. [12: S01 p.11] [13: S01 p.11] [14: S01 p.11] [15: S01 p.15]
- **R3 · Conditional candidate: NIR, diffuse reflection.** NIR reflection is the other technique shown for this application, next to mid-IR ATR, and NIR penetrates up to several millimetres even into dense solids, which is why it is the common in-line method. It is listed as conditional because its geometry depends on an unknown: it is only worth testing if the melt is opaque or strongly scattering, since reflection works well in highly scattering media but is less representative for clear liquids. NIR bands are broad and overlapping and need a chemometric calibration, and NIR may lack sensitivity for a trace component. *Conditions:* Applies if the melt at the probe is opaque/highly scattering. If it turns out transparent, this entry does not apply and the NIR geometry has to be re-decided with AFS (pathlength control becomes the deciding point). [16: S02 p.14] [17: S01 p.5] [18: S01 p.18] [19: S01 p.10] [20: S01 p.16]
- **R4 · Not recommended: Fluorescence, fluorescence probe.** Not part of the first comparison. No fluorescent species or indicator has been identified in the enquiry, most chemicals do not fluoresce, and fluorescence is high-sensitivity but low-selectivity, so it is not a direct measurement of an API in a polymer melt. [21: S01 p.5] [22: REF §5] [23: REF §5]

## Measurement concept

- **Probe and geometry:** First geometry is mid-IR ATR: the probe head is in contact with the melt, which is the suitable case for liquid, paste and soft solid samples. Raman is measured with a contact probe on the same samples as the comparison. A reflection (backscatter) probe is added only if the melt is opaque/scattering.
- **Location:** A flush-mounted probe in the melt stream, for example at the extruder barrel or the die adaptor, so that the probe interacts directly with the flowing medium rather than with a sampled aliquot.
- **Fiber link:** The spectrometers stay away from the machine (vibration, dust, heat) and are connected by fiber probes. Mid-IR needs chalcogenide or polycrystalline infrared fibers or hollow waveguides, since silica fibers stop near 2.4 µm. The achievable length of a mid-IR link for a process installation is not stated in the supplied material and must be confirmed by AFS. [24: S04 p.4] [25: S01 p.17] [26: S01 p.15] [27: S02 p.6] [28: S02 p.6]

## Spectral range

- **MIR:** Nominal mid-IR range 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, the fiber and the probe/crystal actually selected. [29: S01 p.9] [30: REF §3]
- **NIR:** Nominal near-IR range 780-2500 nm. The usable range depends on the instrument, the fiber and the probe actually selected. [31: S01 p.10] [32: REF §5]
- **Raman:** Reported as Raman shift in cm-1; the laser excitation wavelength is stated separately and is not yet chosen for your case. [33: S01 p.11]

## Risks and uncertainty

- ATR contact and build-up. An ATR measurement needs tight contact and sees only a thin surface layer, so the melt must wet the crystal and any deposit on it would dominate the reading. *(rules: R-MIR-2, R-MIR-3)* [34: S04 p.4] [35: REF §5]
- Temperature is unquantified. 'Hot' is not a number, and no supplied page gives an operating temperature rating for a probe or a fiber, so the probe selection could change once the real value is known. [36: S02 p.7]
- Mid-IR fiber link length. Long cables are stated only for low-OH silica fibers; the mid-IR fiber and hollow-waveguide samples in the material are short laboratory lengths. If the spectrometer must sit far from the extruder, this is an open question for AFS, not a value to assume. *(rules: R-FIB-2)* [37: S02 p.7] [38: S02 p.10]
- Calibration and concentration range. The models are specific to the matrix, so a change of formulation or additive package invalidates them until re-validated, and a trace-level API may be below what NIR can see. *(rules: R-CAL-1, R-NIR-4)* [39: REF §5] [40: S01 p.16]

## First feasibility experiment

1. **Samples and reference measurements** Cover the expected chemical and physical variation and give every spectrum an independent number. [41: REF §3]
2. **Single-method spectra first** Record mid-IR ATR spectra first, then Raman spectra, on the same samples and process states; add NIR reflection only if the melt is opaque/scattering. Repeat each measurement to see repeatability, signal quality and, for Raman, the fluorescence background. *(no verified source: engineering judgement)*
3. **Per-method comparison against the offline assay** Build one chemometric model per method and check which method follows the composition change, and how closely it matches the offline reference. *(no verified source: engineering judgement)*
4. **Validation on held-out runs or batches** Keep whole runs (not single spectra) out of the model building and predict them, then compare with the offline assay. [42: S03 p.14]
5. **Go / no-go and next step** Compare each single method against your own numerical criteria (minimum detectable composition change, accuracy, response time - to be supplied by you). Only if no single method reaches them, evaluate a combined multi-method measurement at the same point. [43: REF §5]

**Reference measurements:** Your existing offline assay, run on the same samples/states that are measured optically, is the independent reference.

**Decision basis:** Numbers must come from you: minimum detectable composition change, accuracy and response time. No performance figures for this application are available in the supplied material.

## Assumptions

- The melt keeps tight contact with an ATR crystal (liquid/paste/soft-solid case).
- The interface temperature is within what the probe and fiber can take - no source gives a rating, so AFS must confirm it.
- The spectrometer can be placed away from the extruder and linked with mid-IR fibers - the achievable length is not stated in the sources.
- Your offline assay can be run on samples that represent the in-line measurement point.
- The API or the polymer is not strongly fluorescent, so a Raman measurement is usable.

## Not covered by the supplied sources

- No temperature or pressure rating for a probe or fiber at a hot extrusion interface; these values must come from AFS or from you.
- No achievable length for a mid-IR (chalcogenide or polycrystalline) fiber link in a process installation; long cable lengths are stated only for low-OH silica cables.
- No cleaning or anti-fouling method for a build-up-prone measurement surface.

## Evidence (verified quotes)

1. ✓ **S02 p.14** (application precedent): "Spectra of API in hot polymer obtained with Diamond cone ATR probe coupled to iC10 FTIR (MTAC)"
2. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
3. ✓ **S02 p.7** (general): "High temperature resistance"
4. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
5. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
6. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
7. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
8. ✓ **S02 p.14** (application precedent): "Spectra of API in hot polymer obtained with Diamond cone ATR probe coupled to iC10 FTIR (MTAC)"
9. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
10. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
11. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
12. ✓ **S01 p.11** (general): "This property makes mid-IR and Raman spectra complementary, that is, they complement each other."
13. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
14. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
15. ✓ **S01 p.15** (application precedent): "During the experimental action, the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press."
16. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
17. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
18. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
19. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
20. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
21. ✓ **S01 p.5** (general): "However, most chemicals do not exhibit this property."
22. ✓ **REF §5** (general): "Only a defined fluorescent species or a justified indicator."
23. ✓ **REF §5** (general): "High sensitivity, low selectivity; not a direct measurement of every analyte."
24. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
25. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
26. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
27. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
28. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
29. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
30. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
31. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
32. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
33. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
34. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
35. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
36. ✓ **S02 p.7** (general): "High temperature resistance"
37. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
38. ✓ (precedent only) **S02 p.10** (performance figure): "1 Meter PolyMicro hollow fiber 1mm ID"
39. ✓ **REF §5** (general): "calibration specific to the matrix."
40. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
41. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
42. ✓ **S03 p.14** (general): "A thorough validation, including full, segmented and random-subset CVs, as well as randomization tests, are recommended in any cases for which important conclusions depend on calibration or discrimination models built on limited experimental material."
43. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."

## Verification

- Citations verified: 43 of 43 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 4; repair rounds: 1.

*Run D07-20261017T104829Z · models deepseek/deepseek-v4.1-flash · cost $0.0222*
