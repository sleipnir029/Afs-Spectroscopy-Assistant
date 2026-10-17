# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified for a powder blend in a tablet-press feed frame: NIR diffuse reflection and a Raman probe are the two techniques the supplied material addresses for this kind of task, and a NIR + Raman combination is a testable hypothesis. The choice rests on assumptions that must be confirmed (API level, reference method, fluorescence background, mounting).

## Premise check

- **Supported:** A fiber-based measurement in the feed frame can follow API concentration changes. The supplied material describes exactly this kind of task and shows it as a worked application, with NIR and Raman probes inserted into the feed frame. This is a published example and a reason to test, not proof that it will work for this formulation. [1: S01 p.14] [2: S01 p.15]
- **Supported:** A first pilot comparing reasonable measurement options is sufficient before committing to production equipment. The material supports testing several optical methods on samples of incompletely known composition in order to select the most suitable method or combination. It does not state at what point a pilot is 'sufficient' to commit to production equipment; that decision criterion has to come from the customer. [3: S01 p.3]

## Requirements

**Stated by the customer**

- Compare reasonable measurement options in a first pilot before committing to production equipment.
- Assess whether a fiber-based measurement in the feed frame could follow API concentration changes.

**Key unknowns**

- Identity of the API and its expected concentration range in the blend.
- Which independent reference method will be used, and the accuracy and response time the in-line result must reach (the go/no-go basis).
- Whether the API or any excipient fluoresces, which would raise the background for Raman.
- Normal process variation: particle size, moisture, excipient lots, flow and turbulence at the probe.
- Feed-frame mounting: probe position and distance, temperature, cleaning and fouling of the probe window.

## Clarification questions (most decision-relevant first)

Q1. What is the API and over what concentration range must it be followed (target and expected variation)? *Why it matters:* Decides whether NIR sensitivity is adequate for the API level or whether a lower-limit technique is needed. *(affects: method, technique)*
Q2. Which reference method will define the correct value, and what accuracy and response time must the in-line measurement achieve? *Why it matters:* Sets the comparison basis and the numerical go/no-go criteria for the pilot. *(affects: status, feasibility)*
Q3. Do the API or the excipients fluoresce under visible/NIR excitation? *Why it matters:* Fluorescence background can swamp the weak Raman signal and would change the technique choice or probe design. *(affects: technique, installation)*
Q4. Where exactly would the probe sit in the feed frame, at what distance from the spectrometer, and under what temperature, cleaning and dust conditions? *Why it matters:* Determines whether a contact probe is possible, the fiber link, and fouling risk. *(affects: installation, technique)*
Q5. Can you supply blend samples across the expected API range plus the normal variation (particle size, moisture, excipient lots), and the matching reference values? *Why it matters:* Representative samples and independent references are the basis of the pilot. *(affects: feasibility)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** The blend is an opaque powder that scatters light; NIR diffuse reflection is the geometry the material gives for scattering solids and powders, and NIR is one of the two techniques the source names as most widely implemented for this task. It is also the natural single method to test first. *Conditions:* Assumes a contact reflection probe can be mounted at the feed frame wall and that the API level is within NIR working range. [4: S01 p.10] [5: S01 p.15]
- **R2 · Primary candidate: Raman, raman probe.** Raman is the second technique the source names as widely implemented for this pharmaceutical task and is measured with a contact fiber probe. It should be run as a single method alongside NIR so the two can be compared on equal terms. Note the source example states 785 nm excitation; the excitation wavelength and the Raman shift must be reported separately, and the excitation wavelength for the actual instrument is not yet fixed. *Conditions:* Assumes the fluorescence background from the blend is tolerable; this must be checked on real samples. [6: S01 p.15] [7: S01 p.11] [8: S01 p.11]
- **R3 · Comparison candidate: NIR, diffuse reflection.** Hypothesis to test only after the single-method runs: the two techniques carry complementary chemical information and the source reports higher accuracy and robustness for combined NIR + Raman models than for single-method models in this exact application. Any gain is a hypothesis, to be judged against the best single method, with both data streams taken at the same location and synchronised to a common time step. *Conditions:* Only if R1 and R2 both give usable single-method signals and the two streams can be aligned in time. [9: S01 p.15] [10: S01 p.15] [11: REF §5] [12: REF §5] Later hypothesis, after single-method tests: combine with Raman, Raman.
- **R4 · Not recommended: MIR, ATR.** A reader may expect MIR-ATR as the 'fingerprint' method, but ATR needs tight contact and is described for liquids, pastes and soft solids; a flowing, opaque powder blend in a feed frame does not present that contact, so this is not a candidate for the pilot. *Conditions:* Would only become relevant if the sample were a paste or a soft solid in contact with the crystal. [13: S04 p.4]

## Measurement concept

- **Probe and geometry:** Contact probes at the feed frame wall of the rotary tablet press, tip in contact with the moving powder (NIR reflection and Raman probe). The same measurement point should be used for both methods so the two data sets refer to the same material.
- **Location:** Feed frame of the tablet press, as in the source application; the probe tip must be arranged so the flowing powder passes it without blocking.
- **Fiber link:** Fibers carry light between the probe and the spectrometers, so the instruments can sit away from the press. The fiber family must match the method: silica fibers for NIR, silica-based Raman probe fibers for the Raman channel. [14: S01 p.17] [15: S01 p.15]

## Spectral range

- **NIR:** Nominal NIR range 780-2500 nm. The usable range for this pilot depends on the spectrometer, fiber and probe actually selected and is not fixed by the sources. [16: S01 p.10] [17: REF §5]
- **Raman:** Reported as Raman shift in cm-1, with the laser excitation wavelength stated separately. The source example uses 785 nm excitation; the excitation wavelength for the pilot instrument is not yet chosen. No usable spectral range is given for this sample. [18: S01 p.11] [19: S01 p.15]

## Risks and uncertainty

- The calibration is specific to the blend matrix; a change of formulation, excipient source or API level means the model must be re-validated on the new material. *(rules: R-CAL-1)* [20: REF §5]
- If the API is a low-level component, NIR may lack the sensitivity to follow it; the API level is not yet known. *(rules: R-NIR-4, R-NIR-2)* [21: S01 p.16]
- The weak Raman signal can be swamped by fluorescence from the API or excipients; this can only be judged on real samples. *(rules: R-RAM-1)* [22: S01 p.11]
- The powder is a heterogeneous, flowing medium: the probe sees a small region, and inhomogeneity or turbulence can make the reading unrepresentative or vary between measurements. *(rules: R-GEN-5, R-CMB-2)* [23: S01 p.7]

## First feasibility experiment

1. **Collect representative blend samples spanning the expected API range plus normal process variation (particle size, moisture, excipient lots), with the customer's reference values attached to each sample.** Representative samples and an independent reference are the basis of the comparison. [24: REF §3]
2. **Measure the whole sample set with NIR diffuse reflection and with the Raman probe, at the same points and under the same conditions, keeping each method separate.** Single methods first, so each can be judged on its own. *(no verified source: engineering judgement)*
3. **Build a chemometric calibration per method and compare each single method against the reference values.** NIR bands are broad and overlapping, so a calibration model is needed to turn spectra into concentration. [25: S01 p.10]
4. **Only after the single-method results, test the combined NIR + Raman model against the best single method, with the two data streams synchronised to a common time step.** The combination is a hypothesis and must be compared with the best single method. [26: REF §5] [27: S01 p.8]
5. **Validate the selected model on held-out runs or batches and decide go/no-go against the accuracy and response-time criteria the customer sets.** Held-out validation and a numerical go/no-go basis agreed with the customer. [28: REF §3]

**Reference measurements:** The customer's existing laboratory check (or another independent method) supplies the reference value for each sample; it is not named in the enquiry and must be confirmed.

**Decision basis:** The accuracy, precision and response-time targets are the customer's to set; no performance figures for this application are given in the sources.

## Assumptions

- A contact probe can be mounted at the feed frame wall so the flowing powder passes the tip.
- The API is present at a level NIR can follow (to be confirmed by Q1).
- The blend's fluorescence background is low enough for the Raman channel (to be confirmed by Q3).
- The customer can supply representative samples with reference values (to be confirmed by Q5).

## Evidence (verified quotes)

1. ✓ **S01 p.14** (application precedent): "the precise concentration and uniformity of the Active Pharmaceutical Ingredient (API) - directly within the production line, specifically in the feed frame of a rotary tablet press"
2. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
3. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
4. ✓ **S01 p.10** (general): "high light scattering by solid and dispersed samples, which enables measurements using diffuse reflectance, including measurements without direct contact with the sample, at a distance."
5. ✓ **S01 p.15** (application precedent): "NIR spectrometer and light source coupled with a NIR reflection probe"
6. ✓ (precedent only) **S01 p.15** (performance figure): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
7. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
8. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
9. ✓ (precedent only) **S01 p.15** (method gain): "The combination of these techniques is particularly effective because it captures complementary chemical information: NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups."
10. ✓ (precedent only) **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
11. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
12. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
13. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
14. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium"
15. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
16. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
17. ✓ **REF §5** (general): "actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
18. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
19. ✓ (precedent only) **S01 p.15** (performance figure): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
20. ✓ **REF §5** (general): "calibration specific to the matrix."
21. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
22. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
23. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
24. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
25. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
26. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
27. ✓ **S01 p.8** (general): "data synchronization can be challenging, as the acquisition rates of different spectra can vary greatly-from milliseconds to minutes"
28. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 28 of 28 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 7; repair rounds: 0.

*Run D01-20261017T100944Z · models deepseek/deepseek-v4.1-flash · cost $0.0154*
