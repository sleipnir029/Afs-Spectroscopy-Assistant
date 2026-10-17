# First technical assessment: Water content in a petroleum stream

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Provisional feasibility assessment. A shortlist of fiber methods for a first laboratory comparison can be justified: there is a published laboratory example of water content in petroleum measured with ATR probes, and NIR has stated geometries for clear and for scattering liquids. However, the physical state of the stream, the water range and the required accuracy and response time are not known, so no equipment can be selected yet. Each option below states the assumption it rests on.

## Premise check

- **Supported:** Fiber based measurement closer to the process will allow changes to be noticed sooner. The sources describe in-process analysis without sampling, eliminating delays, and on-site online analysis with results in near real time. This is a general statement about online fiber analysis, not a performance figure for this stream. [1: S01 p.3] [2: S01 p.2]
- **Supported:** The analyzer can be placed outside the process area while still measuring the process stream. ATR fiber probes are stated to allow analysis at a significant distance from the spectrometer without sampling, and fiber optics let the sensitive spectrometers sit away from the process floor. Long cables are stated only for low-OH silica fibers (VIS-NIR); the achievable distance for an MIR fiber link is not stated in the sources and is an open question. [3: S01 p.10] [4: S01 p.15] [5: S02 p.7]
- **Supported:** A first comparison experiment can establish what is needed before selecting equipment. The stated pathway begins with multi-method laboratory trials on the customer's process, and the guidance for a feasibility plan requires representative samples, independent reference measurements, a defined comparison and a go / no-go basis. [6: S02 p.20] [7: REF §3]

## Requirements

**Stated by the customer**

- Target: water in a petroleum stream; current reference is laboratory water determination.
- Measurement to be moved closer to the process; analyzer located outside the process area.
- Deliverable asked for: what to clarify and what a first comparison experiment should establish.

**Key unknowns**

- Physical state and phase of the stream at the measurement point (single-phase liquid, water dispersion or emulsion, multiphase with gas or solids)
- Water concentration range and the required accuracy and response time
- Optical behaviour of the stream (clear, turbid, highly scattering)
- Matrix composition and interferences (hydrocarbon type, additives, dissolved gas)
- Process conditions at the probe (temperature, pressure, fouling, cleaning) and the distance from the analyzer position
- Reference laboratory method and its uncertainty

## Clarification questions (most decision-relevant first)

Q1. What is the physical state of the stream at the planned measurement point: a single-phase liquid, a liquid carrying dispersed or free water, an emulsion, or a multiphase mixture with gas or solids? *Why it matters:* This decides the measurement geometry: contact ATR for a liquid, paste or soft solid, a transmission/transflection path for a clear liquid, or diffuse reflection for an opaque or scattering stream. *(affects: method, technique, installation)*
Q2. What water range must be measured, and what accuracy and response time would count as a successful result? *Why it matters:* These numbers become the go / no-go criteria of the comparison trial; they also decide whether a method with lower sensitivity to trace water is usable at the low end of the range. *(affects: method, technique, go/no-go criteria)*
Q3. How far is the analyzer position from the process measurement point, and what are the pressure, temperature, connection size, cleaning regime and area classification there? *Why it matters:* This decides the fiber family and the achievable link: long cables are stated only for low-OH silica fibers, while an MIR link length is not stated in the sources. *(affects: installation, fiber selection, feasibility)*
Q4. Is the stream optically clear, or opaque / turbid / highly scattering? *Why it matters:* This decides between a transmission or transflection geometry and a diffuse reflection geometry for NIR. *(affects: technique)*
Q5. How is the laboratory water determination performed, and what is its uncertainty and sample turnaround? *Why it matters:* The comparison experiment is judged against this reference, so its uncertainty bounds what the trial can resolve. *(affects: feasibility plan, go/no-go criteria)*

## Recommendation

- **R1 · Primary candidate: MIR, ATR.** Most direct lead for water in a petroleum stream. A supplied page shows a laboratory application measuring water content in petroleum with ATR probes. MIR absorption is strong, so ATR samples only a thin surface layer, which is the usual route for in-line MIR, and ATR fiber probes are stated to allow analysis at a distance from the spectrometer without sampling, which matches an analyzer outside the process area. The published example is a reason to test this method, not evidence of performance on this stream. *Conditions:* Applies only if the stream at the probe contacts the ATR crystal as a liquid, paste or soft solid. [8: S02 p.13] [9: S01 p.5] [10: S01 p.10] [11: REF §5]
- **R2 · Comparison candidate: NIR, transmission transflection.** Worth testing as a second single method, especially if the stream is a clear to semi-transparent liquid: transmission or transflection is the preferred geometry for such liquids, with the pathlength controlled (usually 1 - 10 mm in the source example). NIR runs through silica fibers, for which long cables (100-300 m) are stated, which matters for an analyzer outside the process area. NIR may lack the sensitivity to detect trace compounds below 0.1 percent, and the pathlength has to be matched to the stream. Nominal NIR range is 780-2500 nm; the usable range depends on the instrument, fiber and probe actually selected. *Conditions:* Comparison option in the first trial; it is the more relevant geometry the clearer the stream is. [12: S01 p.18] [13: S01 p.18] [14: S01 p.16] [15: S02 p.7] [16: S01 p.10]
- **R3 · Conditional candidate: NIR, diffuse reflection.** Test only if the stream is opaque, turbid, emulsified or highly scattering, so that a defined transmission path through the stream is impractical. Diffuse reflection is used for opaque or highly concentrated scattering products and needs no pathlength through the stream, but it is sensitive to surface characteristics and to droplet or particle size, so scatter correction is part of the method and physical variation can be mistaken for a composition change. *Conditions:* Applies if the answer to the physical-state and optical-clarity questions shows an opaque or highly scattering stream. [17: S01 p.17] [18: S01 p.17]
- **R4 · Not recommended: Raman, raman probe.** Raman is a standard in-line fiber method, so a reader may expect it here, but the supplied material gives no example of water determination in a hydrocarbon stream by Raman; Raman signals are weak and can be swamped by fluorescence, and a calibration would be specific to the matrix. It can be reconsidered later if a specific reason appears, for example a water-specific band or a non-fluorescing matrix. *Conditions:* Not proposed for the first comparison trial. [19: S01 p.11] [20: S01 p.11] [21: REF §5]

## Measurement concept

- **Probe and geometry:** A probe in contact with the stream at the process point: an ATR crystal head for the MIR option, and a transmission or transflection cell (or a diffuse reflection window) for the NIR options. ATR fiber probes are stated to allow analysis at a significant distance from the spectrometer without sampling, and fiber optics let the sensitive spectrometers sit away from the process floor.
- **Location:** To be fixed with the customer; it decides the fiber family and link, and is currently unknown.
- **Fiber link:** Silica VIS-NIR fibers carry the NIR options; MIR needs chalcogenide (CIR) or polycrystalline (PIR) fibers. The achievable MIR link length is not stated in the sources. [22: S01 p.10] [23: S01 p.15] [24: S02 p.14]

## Spectral range

- **MIR:** Nominal MIR range 4000-400 cm-1 (2.5-25 μm). This is the method range, not the range of a specific instrument, fiber or probe; MIR light needs chalcogenide or polycrystalline fibers, since silica fibers do not carry it. [25: S01 p.9] [26: REF §3] [27: S02 p.6]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. Silica fibers are stated to about 2400 nm. [28: S01 p.10] [29: S02 p.6] [30: REF §5]

## Risks and uncertainty

- The physical state of the stream is unknown. Contact ATR needs a liquid, paste or soft solid that wets the crystal; if the stream is a dry gas, a multiphase mixture with solids, or otherwise does not wet the crystal, ATR does not apply. Transmission also fails when the stream is too thick or too opaque for light to penetrate. *(rules: R-MIR-2, R-GEO-2)* [31: REF §5] [32: S01 p.18]
- The achievable fiber-link length for an MIR probe is not established in the sources. Long cables (100-300 m) are stated only for low-OH silica fibers (VIS-NIR), while the MIR fiber and hollow-waveguide comparisons shown are short laboratory lengths. Whether an MIR ATR probe can reach an analyzer outside the process area at the required distance is therefore an open question for AFS. *(rules: R-FIB-2)* [33: S02 p.7] [34: S02 p.10] [35: S02 p.9]
- Water level and matrix. The published petroleum example covers a limited set of water levels, and NIR may lack sensitivity for trace water below 0.1 percent. Calibrations are specific to the matrix, so a model built on trial samples must be re-validated if the stream composition or water level changes. *(rules: R-NIR-4, R-CAL-1)* [36: S01 p.16] [37: REF §5]
- ATR samples only a surface layer a few micrometres deep, so deposits on the crystal, and stream turbulence or inhomogeneity, can change the signal. The process temperature, pressure, cleaning regime and area classification are unknown and could rule out a given probe or installation. *(rules: R-MIR-3, R-GEN-5)* [38: S01 p.13] [39: S01 p.7]

## First feasibility experiment

1. **Representative samples across the expected variation** Cover the expected water range, including the low end and any separate water phase, the expected stream states (clear to turbid, if both occur) and the process temperature where possible. Have each sample measured by the current laboratory water determination as the independent reference. [40: REF §3]
2. **Measure the same samples by the single methods first** MIR ATR first, then NIR transmission/transflection (and NIR diffuse reflection only if the samples scatter). Keep the same sampling point for both methods where possible, and record spectra over the nominal ranges MIR 4000-400 cm-1 and NIR 780-2500 nm; the usable range of the actual fiber and probe is confirmed with AFS. [41: S01 p.9] [42: S01 p.10] [43: REF §3]
3. **Compare each method against the reference on held-out samples or batches** Build a simple chemometric model per method and compare the predicted water content with the laboratory reference on samples or runs not used for the model. Validate on held-out runs or batches, not on the calibration samples. [44: S01 p.10] [45: REF §5]
4. **Agree the go / no-go basis with the customer before the trial** Fix the numerical criteria in advance: the water range to be covered, the required accuracy, the required response or measurement interval, and how the laboratory reference is compared. The trial is judged against those numbers, not against a general impression. [46: REF §3]
5. **Combinations only after the single methods** If neither single method reaches the agreed criteria, compare a combined NIR + MIR evaluation against the best single method, with sampling location and timing aligned. A gain from combining is a hypothesis to test, not an expectation. [47: REF §5] [48: REF §5]

**Reference measurements:** The current laboratory water determination, run on the same samples as the fiber measurements.

**Decision basis:** The numerical criteria (water range, accuracy, response time) must come from the customer; they are not in the supplied material.

## Assumptions

- The stream at the probe is a liquid, paste or soft solid that can contact an ATR crystal or fill a transmission path.
- Water is present at levels high enough for the chosen method to resolve; the level range is unknown.
- An MIR fiber link of the required length can be built; this is not stated in the sources and must be confirmed by AFS.
- The laboratory water determination is a valid independent reference with an uncertainty suitable for the required accuracy.

## Not covered by the supplied sources

- The achievable fiber-link length for an MIR (ATR) probe over the distance from the process point to an analyzer outside the process area: long cables are stated only for low-OH silica fibers, and the MIR fiber and hollow-waveguide examples shown are short laboratory lengths.
- In-line or at-line performance of water determination in a petroleum stream: the supplied petroleum example is a laboratory ATR measurement, and no source covers an installed process measurement for this application.
- Pressure, temperature and area-classification ratings for probes and fibers for this kind of installation: no supplied source gives these figures.

## Evidence (verified quotes)

1. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
2. ✓ **S01 p.2** (general): "enabling on-site online analysis and obtaining results in near real time."
3. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
4. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
5. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
6. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
7. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
8. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"
9. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
10. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
11. ✓ **REF §5** (general): "Liquids, pastes and soft solids in contact with the ATR crystal."
12. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
13. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
14. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
15. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
16. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
17. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
18. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
19. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
20. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
21. ✓ **REF §5** (general): "Weak signal, fluorescence background; calibration specific to the matrix."
22. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
23. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
24. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
25. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
26. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
27. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
28. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
29. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
30. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
31. ✓ **REF §5** (general): "Liquids, pastes and soft solids in contact with the ATR crystal."
32. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
33. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
34. ✓ (precedent only) **S02 p.10** (performance figure): "1 Meter PolyMicro hollow fiber 1mm ID"
35. ✓ (precedent only) **S02 p.9** (performance figure): "HWG-750-2m PIR 600/700 -2m"
36. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
37. ✓ **REF §5** (general): "Weak signal, fluorescence background; calibration specific to the matrix."
38. ✓ **S01 p.13** (general): "typically at a depth of few microns"
39. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
40. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
41. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
42. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
43. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
44. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
45. ✓ **REF §5** (general): "Weak signal, fluorescence background; calibration specific to the matrix."
46. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
47. ✓ **REF §5** (general): "compare with the best single method."
48. ✓ **REF §5** (general): "Sampling location and timing must be aligned; a gain is a hypothesis to test."

## Verification

- Citations verified: 48 of 48 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 3; repair rounds: 1.

*Run D06-20261017T104139Z · models deepseek/deepseek-v4.1-flash · cost $0.0214*
