# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for a powder blend in a tablet press feed frame, with explicit assumptions. The strongest candidates are NIR diffuse reflection and Raman, both of which pass screening and have direct pharmaceutical blend/feed-frame precedent in the sources. Several central facts (API identity, concentration range, excipients, optical regime, feed-frame access) are unknown, so the recommendation is conditional and the first experiment is designed to resolve the deciding unknowns.

## Premise check

- **Supported:** A fiber based measurement in the feed frame could follow API concentration changes.. The sources describe in-line monitoring of blend potency in the feed frame of a rotary tablet press using NIR and Raman fiber probes as a published application example. This is a reason to test, not proof for this customer's specific blend. [1: S01 p.14] [2: S01 p.15]
- **Supported:** The first pilot should compare reasonable measurement options before committing to production equipment.. The AFS guided pathway explicitly starts with multi-method lab trials to select the best method before choosing a custom solution. [3: S02 p.20] [4: S01 p.3]

## Requirements

**Stated by the customer**

- Compare reasonable measurement options before committing to production equipment
- Assess whether a fiber-based measurement in the feed frame could follow API concentration changes

**Key unknowns**

- API identity and concentration range
- Excipient composition and potential interferences
- Optical properties of the powder blend (scattering, absorption, fluorescence)
- Particle size distribution and flow behavior
- Feed frame geometry and optical access
- Temperature and pressure conditions in the feed frame
- Required measurement speed and response time
- Required accuracy and precision
- Reference method for calibration
- Cleaning and fouling considerations
- Regulatory constraints for pharmaceutical manufacturing

## Clarification questions (most decision-relevant first)

Q1. What is the API, what is its target concentration range, and what are the main excipients? *Why it matters:* This determines which spectral features are available and whether NIR, Raman, or both can see the API. It also drives the choice of reference method and the expected sensitivity requirement. *(affects: method, technique, go_no_go_criteria)*
Q2. What is the particle size distribution and flow behavior of the blend in the feed frame? *Why it matters:* Powder scattering, particle size and flow affect the optical regime, the choice between diffuse reflection and other geometries, and the representativeness of the measurement spot. *(affects: technique, installation)*
Q3. What is the geometry and available optical access at the feed frame, and what are the temperature, pressure and vibration conditions there? *Why it matters:* This determines whether a probe can be flush-mounted, what probe size and window are feasible, and whether the fiber link and probe can survive the process environment. *(affects: installation, technique)*
Q4. What measurement speed and response time are required to follow API concentration changes in the feed frame? *Why it matters:* This affects the choice of spectrometer type and acquisition settings, and whether a full-spectrum method or a reduced-wavelength sensor is appropriate. *(affects: method, technique)*
Q5. What accuracy and precision are required for API concentration, and what is the current laboratory reference method? *Why it matters:* The go/no-go criteria must come from the customer's own specification. The reference method is needed for calibration and independent validation. *(affects: go_no_go_criteria, feasibility_plan)*
Q6. Does the blend or any component fluoresce under the intended excitation? *Why it matters:* Fluorescence can swamp Raman signals and would also determine whether fluorescence spectroscopy is a viable option at all. *(affects: method, technique)*
Q7. Are there regulatory or cleaning constraints that restrict probe materials, contact geometry, or the use of a particular method in the feed frame? *Why it matters:* This affects whether a contact probe is acceptable, what materials can be used, and whether the pilot can be run on the actual press or must start off-line. *(affects: installation, status)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** NIR diffuse reflection is the most common online method for powders and scattering media, and the sources show it used directly in a tablet press feed frame for blend potency. It penetrates up to several millimetres, works with standard silica fibers and lamps, and is well suited to remote fiber-probe measurement. *Conditions:* The powder must be scattering or opaque enough for diffuse reflection; the API or a correlated matrix change must produce a detectable NIR signal; a chemometric calibration is required. [5: S01 p.5] [6: S01 p.6] [7: S01 p.15]
- **R2 · Primary candidate: Raman, raman probe.** Raman is the other widely implemented technique for pharmaceutical blend monitoring and is shown in the same feed-frame application. It provides complementary molecular-backbone information and is well suited to powders. *Conditions:* The API or a correlated excipient must have a usable Raman band; fluorescence background must be checked on the real blend; a chemometric calibration is required. [8: S01 p.15] [9: S01 p.11]
- **R3 · Conditional candidate: NIR, transmission transflection.** NIR transmission or transflection is the preferred geometry for transparent or semi-transparent liquids, but the powder blend is not a clear liquid. It is included only as a conditional option if the blend turns out to be unusually transparent or if a transflection probe is considered for a specific feed-frame geometry. *Conditions:* Only if the powder is sufficiently transparent or semi-transparent for transmission/transflection, which is unlikely for a typical tablet blend. This is a hypothesis to test, not a default. [10: S01 p.18] [11: S01 p.18]
- **R4 · Conditional candidate: NIR, diffuse reflection remote.** Remote diffuse reflection without direct contact is possible for powders and scattering media, but in a feed frame the probe is typically inserted directly. This is conditional on the feed-frame geometry and whether a non-contact measurement is required. *Conditions:* Only if the feed-frame geometry requires a non-contact measurement and the powder surface is stable enough for remote diffuse reflection. [12: S01 p.6]
- **R5 · Comparison candidate: NIR, diffuse reflection.** NIR diffuse reflection is the best single-method candidate and should be the baseline against which any combination is compared. *Conditions:* Same as R1. [13: S01 p.15]
- **R6 · Comparison candidate: Raman, raman probe.** Raman is the second single-method candidate and should be compared directly with NIR diffuse reflection on the same samples. *Conditions:* Same as R2. [14: S01 p.15]
- **R7 · Not recommended: NIR, diffuse reflection.** NIR diffuse reflection is recommended, but only as a single method first. A combination with Raman is a hypothesis to test only after the single methods have been evaluated. *Conditions:* Do not start with a combination. [15: S01 p.15]
- **R8 · Not recommended: MIR, ATR.** MIR ATR requires tight contact and suits liquids, pastes and soft solids. A powder blend in a feed frame is not a confirmed fit, and the screening status is fail. *Conditions:* Not recommended for this powder blend. [16: S01 p.6] [17: S04 p.4]
- **R9 · Not recommended: UV-Vis, ATR.** UV-Vis ATR has the same contact requirement as MIR ATR and is not a confirmed fit for a powder blend. The screening status is fail. *Conditions:* Not recommended for this powder blend. [18: S01 p.6]
- **R10 · Conditional candidate: UV-Vis, diffuse reflection.** UV-Vis diffuse reflection is listed for solid and pill samples, but the powder blend is not a confirmed fit and UV-Vis has low selectivity for mixtures. It is conditional only if the API has a strong, specific UV-Vis absorption and the blend is suitable for diffuse reflection. *Conditions:* Only if the API has a strong, specific UV-Vis absorption and the blend is suitable for diffuse reflection. [19: S01 p.6]
- **R11 · Not recommended: UV-Vis, transmission transflection.** UV-Vis transmission is for liquids and fails for opaque or thick samples. A powder blend is not a confirmed fit. *Conditions:* Not recommended for this powder blend. [20: S01 p.6]
- **R12 · Not recommended: UV-Vis, emission probe.** UV-Vis emission requires a radiating sample and is not a confirmed fit for a powder blend. *Conditions:* Not recommended for this powder blend. [21: S01 p.6]
- **R13 · Conditional candidate: Fluorescence, fluorescence probe.** Fluorescence only measures species that fluoresce. No fluorescent species or indicator has been identified for this powder blend. It is conditional only if the API or a justified indicator fluoresces. *Conditions:* Only if the API or a justified fluorescent indicator is present. [22: S01 p.5]

## Measurement concept

- **Probe and geometry:** For the primary candidates: NIR diffuse reflection probe or Raman probe inserted directly into the feed frame, flush-mounted or in contact with the flowing powder. The probe tip must be positioned where the powder passes reliably and where the measurement spot is representative of the blend.
- **Location:** Feed frame of the rotary tablet press, as described in the pharmaceutical application example.
- **Fiber link:** For NIR, standard low-OH silica fibers are suitable. For Raman, metal-coated silica fibers are preferred to avoid polymer-jacket fluorescence. The fiber link length must be confirmed with AFS; the sources state 100-300 m cables only for low-OH silica fibers, and no MIR link length is stated. [23: S01 p.15] [24: S02 p.7] [25: S02 p.7]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [26: S01 p.10]
- **Raman:** Raman shift is reported in cm-1. The excitation wavelength must be stated separately. The pharmaceutical example uses 785 nm excitation. [27: S01 p.15] [28: S01 p.11]

## Risks and uncertainty

- The powder blend may be too opaque or too transparent for the assumed geometry, making diffuse reflection unrepresentative or transmission impossible. *(rules: R-GEO-2, R-GEO-4, R-GEO-6)* [29: S01 p.18] [30: S01 p.17]
- The API may not have a detectable NIR or Raman signal, or its signal may overlap with excipients, making calibration impossible or unstable. *(rules: R-NIR-2, R-RAM-1, R-CAL-1)* [31: S01 p.10] [32: S01 p.11]
- Fluorescence from the blend or excipients could swamp the Raman signal. *(rules: R-RAM-1)* [33: S01 p.11]
- The feed-frame geometry may not allow a probe to be mounted where the powder is representative, or the probe may be subject to fouling, vibration or temperature effects. *(rules: R-GEN-5, R-FIB-5)* [34: S01 p.7] [35: S01 p.15]
- The calibration may not transfer from the pilot blend to production material if the matrix, particle size or process conditions change. *(rules: R-CAL-1)* [36: S01 p.10]
- The published feed-frame example is a reason to test, not proof that NIR or Raman will work for this specific API and blend. *(rules: R-EVI-2)* [37: S01 p.15]

## First feasibility experiment

1. **Collect representative powder blend samples across the expected API concentration range, including at least the target concentration and several off-target levels spanning the range the customer wants to detect.** To cover the expected chemical variation and provide a basis for calibration and validation. [38: S01 p.3]
2. **Include samples that vary in particle size, moisture, and excipient lot, and if possible samples taken from the feed frame under normal and upset conditions.** To cover the expected physical variation and test robustness against process changes. [39: S01 p.7]
3. **Obtain independent reference measurements of API concentration for every sample using the customer's laboratory method.** To provide the reference values needed for calibration and validation. [40: S01 p.2]
4. **Measure all samples with NIR diffuse reflection first, then with Raman, as single methods. Do not start with a combination.** To establish the best single method before testing any combination. *(no verified source: engineering judgement)*
5. **Build and validate chemometric models for each single method using held-out runs or batches, not just random sample splitting.** To test whether the method can predict API concentration on material it has not seen during calibration. [41: S01 p.2]
6. **Compare the prediction error of each single method against the customer's required accuracy and precision. If neither single method meets the requirement, test a combination of NIR and Raman as a hypothesis, with synchronized sampling location and timing.** To decide whether a combination is justified and to compare it against the best single method. [42: S01 p.15]
7. **Define go/no-go criteria from the customer's required accuracy, precision and response time. A method passes only if its validated prediction error on held-out batches meets the customer's specification.** To provide a numerical basis for the go/no-go decision that comes from the customer, not from the sources. [43: S01 p.2]

**Reference measurements:** The customer's current laboratory method for API concentration, applied to every sample used in the pilot.

**Decision basis:** The go/no-go decision must be based on the customer's own required accuracy, precision and response time. The sources do not provide these figures, so they must be obtained from the customer before the pilot is finalized.

## Assumptions

- The powder blend is a scattering or opaque solid suitable for diffuse reflection.
- The API or a correlated matrix change produces a detectable NIR or Raman signal.
- The feed frame allows a probe to be mounted where the powder is representative.
- The customer can provide representative samples and independent reference measurements.
- The required accuracy, precision and response time will be supplied by the customer.

## Not covered by the supplied sources

- API identity, concentration range, excipient composition and potential interferences
- Optical properties of the customer's specific powder blend
- Particle size distribution and flow behavior of the customer's blend
- Feed frame geometry and optical access for the customer's press
- Temperature, pressure and vibration conditions in the customer's feed frame
- Required measurement speed, accuracy and precision for this application
- Reference method details for this customer
- Cleaning and fouling behavior of the customer's blend
- Regulatory constraints for this specific pharmaceutical manufacturing process
- Achievable fiber link length for a specific probe and spectrometer configuration
- Any performance figures for the customer's specific API and blend

## Evidence (verified quotes)

1. ✓ **S01 p.14** (application precedent): "The primary objective is to determine "blend potency" - the precise concentration and uniformity of the Active Pharmaceutical Ingredient (API) - directly within the production line, specifically in the feed frame of a rotary tablet press."
2. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
3. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
4. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
5. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics, as well as standard lamps as light sources, making it ideal for online applications, including remote measurements via fiber optic probes."
6. ✓ **S01 p.6** (general): "Diffuse reflection-probe diffuse reflection Scattering media, powder 0.5-1 mm"
7. ✓ **S01 p.15** (application precedent): "NIR spectrometer and light source coupled with a NIR reflection probe"
8. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
9. ✓ **S01 p.11** (general): "Raman spectroscopy is based on recording weak radiation signals observed when a sample is irradiated by a laser or high-power LED, typically in the visible light range."
10. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
11. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
12. ✓ **S01 p.6** (general): "surface at a distance solid, powder 2-5 mm"
13. ✓ **S01 p.15** (application precedent): "NIR spectrometer and light source coupled with a NIR reflection probe"
14. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
15. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
16. ✓ **S01 p.6** (general): "ATR- platform absorption liquid,paste, soft 1-6 mu"
17. ✓ **S04 p.4** (general): "Another require-ment is the suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
18. ✓ **S01 p.6** (general): "ATR probe 0.1-1 mu"
19. ✓ **S01 p.6** (general): "Diffuse reflection-probe diffuse reflection solid, pill 1-5 mm low low"
20. ✓ **S01 p.6** (general): "Transmission or transflection probe Transmission liquid 1-10 mm low"
21. ✓ **S01 p.6** (general): "probe, lens emission of an external source radiating sample any high"
22. ✓ **S01 p.5** (general): "Another highly sensitive method, UV/Vis fluorimetry, is based on the secondary emission of excited molecules of certain substances, most often of biological origin. However, most chemicals do not exhibit this property."
23. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
24. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
25. ✓ **S02 p.7** (general): "Free of Polymer jacket fluorescence for Raman and Fluo- Spectroscopy"
26. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
27. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
28. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
29. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
30. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
31. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
32. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
33. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
34. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
35. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
36. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
37. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
38. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
39. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
40. ✓ **S01 p.2** (general): "Analysis is typically divided into quantitative and qualitative. The first answers the question, "What is the composition of a sample?", while the second answers the question, "What is its quantitative composition? How much of a particular substance does it contain?""
41. ✓ **S01 p.2** (general): "This is achieved through a special branch of analytical chemistry called chemometrics, which provides chemists with a rich toolkit for constructing calibration and classification models, as well as methods for in-depth research data analysis."
42. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
43. ✓ **S01 p.2** (general): "The task of an analytical chemist is to develop and improve methods for quantitative and qualitative analysis."

## Verification

- Citations verified: 43 of 45 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 3; soft warnings: 8; repair rounds: 2.
- Removed 2 citation(s) that failed verification:
  - ⚠ recommendations[1].citations[1]: S01 p.15 "In the pharmaceutical industry, the most popular"
  - ⚠ feasibility_plan.steps[3].citations[0]: S01 p.15 "In the pharmaceutical industry, the most popular"
- ⚠ forbidden_wording at assessment: certainty: 'will work'
- Removed 4 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry

*Run D01 · models deepseek/deepseek-v4-pro-0813 · cost $0.0791*
