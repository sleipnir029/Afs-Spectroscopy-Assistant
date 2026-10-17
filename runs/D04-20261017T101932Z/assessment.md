# First technical assessment: Glucose and lactate trends in an aqueous bioprocess

**Customer enquiry**

> We run a cell culture process in an aqueous medium. Glucose and lactate are measured from samples, and the delay makes it difficult to see changes promptly. We are exploring an in situ spectroscopy pilot that can be checked against those existing laboratory measurements. The medium and cell population change during the run; we have not yet selected a probe or a calibration strategy.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified: the medium is aqueous and the targets are glucose and lactate, and the sources describe Raman for these metabolites in the same reactor and NIR for glucose in the millimolar range. The optical regime of the suspension and the required accuracy are unknown, so the NIR geometry stays conditional and the numbers for the go/no-go decision must come from the customer.

## Premise check

- **Not covered:** The existing laboratory measurements can serve as a valid check for an in situ spectroscopy pilot. The supplied material requires independent reference measurements as part of a feasibility plan, but no page addresses whether these particular laboratory measurements are accurate or representative enough to act as that reference. *(no verified source: engineering judgement)*
- **Supported:** The sampling delay is the main problem and prompt measurement is required. The source states that in-process measurement without sampling removes the delay and the contamination risk that come with taking samples. [1: S01 p.3]
- **Supported:** An in situ spectroscopy pilot is the appropriate next step. The source describes testing various optical spectroscopy approaches as crucial when samples are of incompletely known composition, in order to select the most suitable method or combination of methods - which is the situation here, since the medium changes during the run and no method is fixed yet. [2: S01 p.3]

## Requirements

**Stated by the customer**

- In-line or in-situ measurement of glucose and lactate in an aqueous cell culture medium.
- Results prompt enough to see changes that offline sampling now hides.
- The pilot should be checkable against the existing laboratory measurements.

**Key unknowns**

- Concentration ranges of glucose and lactate during the run.
- Required accuracy and update interval (response time) for the two analytes.
- Optical regime of the medium and how it changes with cell density (clear vs turbid).
- The existing laboratory reference method, its uncertainty and sampling frequency.
- Installation: reactor type and port, distance to the spectrometer, sterilisation/cleaning, temperature and pressure.
- Presence of fluorescing species in the medium, or an intended fluorescent indicator.

## Clarification questions (most decision-relevant first)

Q1. What concentration ranges do glucose and lactate cover, and what accuracy and update interval do you need? *Why it matters:* These decide the method and the probe geometry, and they supply the numbers for the go/no-go decision. *(affects: method, technique, go/no-go criteria)*
Q2. Is the medium clear or semi-transparent, or turbid, and how does this change with cell density during the run? *Why it matters:* This decides between NIR transmission/transflection and diffuse reflection, and between UV-Vis transmission and ATR. *(affects: technique, probe)*
Q3. What is the existing laboratory method for glucose and lactate, with its uncertainty and sampling frequency? *Why it matters:* This decides whether it can serve as the independent reference for the pilot. *(affects: feasibility plan, status)*
Q4. Where would the probe be installed: reactor type and port, distance to the spectrometer, sterilisation and cleaning regime, temperature and pressure? *Why it matters:* This decides the probe form, the fiber type and whether a remote fiber link is practical. *(affects: installation, fiber)*
Q5. Are there fluorescing species in the medium, or do you intend to add a fluorescent indicator? *Why it matters:* Fluorescence only works for species that fluoresce, so this decides whether fluorescence is an option at all. *(affects: method)*

## Recommendation

- **R1 · Primary candidate: Raman, raman probe.** Raman is the single method to test first: it is described for direct detection of specific metabolites such as glucose and lactate in the same reactor, and it tolerates an aqueous medium better than infrared methods. Its known weakness is a weak signal and possible fluorescence background, which is exactly what the trials must check on your medium. *Conditions:* None beyond the general caveat that the Raman shift range and the excitation wavelength depend on the laser, spectrometer, fiber and probe actually selected. [3: S01 p.16] [4: S01 p.16] [5: S01 p.11]
- **R2 · Conditional candidate: NIR, transmission transflection.** NIR is the most common in-line fiber-probe method and is described as effective for glucose in the millimolar range. It applies only if the medium is transparent or semi-transparent enough for a controlled pathlength; if the suspension is too turbid or scattering, the geometry to test instead is diffuse reflection. Its broad overlapping bands require a chemometric model. *Conditions:* Applies if the medium is optically clear or semi-transparent and a defined optical pathlength can be maintained. The 1-10 mm pathlength quoted from the source is a dairy example, not a value for your process. [6: S01 p.10] [7: S01 p.16] [8: S01 p.18] [9: S01 p.18] [10: S01 p.18] [11: S01 p.10]
- **R3 · Comparison candidate: MIR, ATR.** MIR ATR probes are described for in-line, in-process biotechnological environments, and their vibrational spectra carry information complementary to Raman. Run MIR ATR on its own as the comparison method first; the pairing with Raman is a later hypothesis of gain, to be tested only after the single-method results are in. *Conditions:* Compare against the best single method (expected to be Raman) after the single-method tests. Treat any gain from the combination as a hypothesis, and align sampling location and timing. [12: S01 p.5] [13: S01 p.10] [14: S01 p.5] [15: S04 p.4] [16: REF §5] [17: REF §5] Later hypothesis, after single-method tests: combine with Raman, Raman.

## Measurement concept

- **Probe and geometry:** In-line, in-situ measurement with a fiber probe in the reactor or process line, with the spectrometers kept away from the process point. Raman: laser-excited fiber probe, contact measurement possible. NIR: transmission or transflection probe with a controlled pathlength if the medium is clear, or a flush-mounted diffuse-reflection probe if it is turbid. MIR: ATR probe whose crystal is in contact with the liquid.
- **Location:** At the reactor or process line; the exact port, immersion depth and distance to the spectrometer are not yet known and depend on the answers to Q4.
- **Fiber link:** The fiber family must transmit the method's range. The sources state long cables (100-300 m) for low-OH silica fibers, which cover NIR and Raman, while MIR needs chalcogenide or polycrystalline fibers, and no achievable MIR link length is stated. [18: S01 p.5] [19: S01 p.17] [20: S01 p.15] [21: S02 p.7]

## Spectral range

- **Raman:** Raman shift in cm-1 is the spectral axis; the excitation wavelength is stated separately. The laser wavelength is not yet chosen. A source example uses 785 nm excitation, but this is an example, not a specification for your process. [22: S01 p.11] [23: S01 p.15]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [24: S01 p.10] [25: REF §3]
- **MIR:** Nominal MIR range 4000-400 cm-1 (2.5-25 um). The usable range depends on the fiber and the ATR crystal selected. [26: S01 p.9] [27: REF §3]

## Risks and uncertainty

- The medium and the cell population change during the run. NIR and Raman calibrations are specific to the matrix, so a model built on part of the run may not hold for the rest of it, and will need re-validation or extension on new material. *(rules: R-CAL-1)* [28: REF §5] [29: REF §5]
- The optical regime of the suspension is unknown and changes with cell density. If it becomes turbid, a transmission geometry loses signal and the probe choice changes. *(rules: R-GEO-2, R-GEN-5)* [30: S01 p.18] [31: S01 p.7]
- No achievable MIR link length is given in the sources. Long cables are stated only for low-OH silica fibers, and the MIR fiber and hollow-waveguide examples in the sources are short laboratory runs. The installation distance for MIR is therefore an open question, not a given. *(rules: R-FIB-2)* [32: S02 p.7] [33: S02 p.9] [34: S02 p.10]
- Probe contact and cleanliness: ATR needs tight contact and samples only a surface layer, so fouling or deposits on the crystal can bias results; on real samples Raman can be disturbed by a fluorescence background. *(rules: R-MIR-3, R-RAM-1)* [35: S04 p.4] [36: S01 p.13] [37: S01 p.11]

## First feasibility experiment

1. **Agree the independent reference and the go/no-go basis with the customer before any measurement.** Without a defined reference and decision basis, no trial result can be judged. [38: REF §3]
2. **Collect representative samples or process states across the run, spanning the chemical and physical variation, and measure an independent reference value for each sample.** The samples must cover the changing medium and cell population, not just one process state. [39: REF §3] [40: S01 p.7]
3. **Run laboratory trials on those samples with in-line-type probe geometry (Raman probe, NIR transmission/transflection or reflection probe, MIR ATR probe) and compare each method against the reference.** Testing the candidate methods on the real matrix is the way to select the most suitable method; engineering judgement based on the shortlist above. *(no verified source: engineering judgement)*
4. **Build a chemometric model per method and validate it on held-out runs or batches, not on random splits of the same run; re-check the model whenever the medium or the cell population changes.** Calibrations are matrix-specific and validation must be independent of the calibration material. [41: S03 p.14] [42: REF §5]
5. **Compare the single methods first, then test the MIR ATR + Raman combination against the best single method, and take the go/no-go decision against the customer's criteria.** A gain from combining methods is a hypothesis to test, not an assumed benefit. [43: REF §5] [44: REF §5]

**Reference measurements:** The customer's existing laboratory glucose and lactate measurements are the intended reference. Their uncertainty and sampling frequency are unknown, and no supplied page states that they are adequate as a reference.

**Decision basis:** Numeric go/no-go criteria (accuracy, update interval, concentration ranges) must come from the customer; the supplied material gives no performance figures for this application.

## Assumptions

- The existing laboratory glucose and lactate measurements can be used as the independent reference; this is assumed, not confirmed by any source.
- The medium stays a liquid that can contact a probe during the run.
- The pilot is expected to start as a multi-method laboratory trial on samples, with the in-line installation decided afterwards.

## Not covered by the supplied sources

- Accuracy, detection limits and response time for glucose and lactate in this cell culture medium: not stated in the supplied material.
- Whether an in situ probe can be fitted, cleaned and sterilised in this customer's bioreactor: not covered by the supplied material.

## Evidence (verified quotes)

1. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
2. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
3. ✓ **S01 p.16** (general): "Raman spectroscopy can be used in the same reactor to provide a "molecular fingerprint" for direct detection of specific metabolites like glucose, acetate, or lactate."
4. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
5. ✓ **S01 p.11** (general): "measuring Raman spectra is hampered by the low intensity of Raman signals, which are several orders of magnitude weaker than IR absorption peaks"
6. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
7. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
8. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
9. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
10. ✓ (precedent only) **S01 p.18** (performance figure): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
11. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
12. ✓ **S01 p.5** (general): "the spectra of vibrational transitions in Raman and mid-IR spectroscopy carry complementary qualitative and quantitative information about the sample's composition."
13. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments"
14. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
15. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
16. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
17. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
18. ✓ **S01 p.5** (general): "The use of these probes can be essential for in-situ analysis-in the field or in an ongoing process."
19. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
20. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
21. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
22. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
23. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
24. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands"
25. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
26. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
27. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
28. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
29. ✓ **REF §5** (general): "Weak signal, fluorescence background; calibration specific to the matrix."
30. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
31. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
32. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
33. ✓ (precedent only) **S02 p.9** (performance figure): "HWG-750-2m PIR 600/700 -2m"
34. ✓ (precedent only) **S02 p.10** (performance figure): "1 Meter PolyMicro hollow fiber 1mm ID"
35. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
36. ✓ **S01 p.13** (general): "typically at a depth of few microns"
37. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
38. ✓ **REF §3** (general): "the basis for the go / no-go decision."
39. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
40. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
41. ✓ **S03 p.14** (general): "A thorough validation, including full, segmented and random-subset CVs, as well as randomization tests, are recommended in any cases for which important conclusions depend on calibration or discrimination models built on limited experimental material."
42. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
43. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
44. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."

## Verification

- Citations verified: 44 of 44 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 8; repair rounds: 1.
- Removed 1 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[0]: enquiry_quote not found verbatim in the enquiry

*Run D04-20261017T101932Z · models deepseek/deepseek-v4.1-flash · cost $0.0357*
