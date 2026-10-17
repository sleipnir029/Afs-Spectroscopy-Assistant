# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. Screening passes NIR diffuse reflection and Raman for an opaque powder. Both are named in the sources as the widely implemented pharma in-line techniques, and a feed-frame example with a NIR reflection probe and a Raman probe exists. A shortlist can therefore be justified, but it rests on assumptions about the customer's API, excipients and feed-frame conditions that are not yet known, so the assessment stays provisional.

## Premise check

- **Supported:** A fiber based measurement in the feed frame could follow API concentration changes. The sources describe probes inserted into a tablet-press feed frame and name NIR and Raman as the widely implemented pharma techniques. This is a precedent (a reason to test), not proof that it works for this customer's blend. [1: S01 p.15] [2: S01 p.15]
- **Not covered:** Laboratory checks are a suitable reference for whether the blend is on target. The sources only state that a feasibility plan needs independent reference measurements; they do not assess the customer's laboratory method, its accuracy or its timing. *(no verified source: engineering judgement)*
- **Supported:** A first pilot comparing reasonable measurement options is sufficient before committing to production equipment. The supplied material describes a staged path in which multi-method laboratory trials come first and a solution is chosen afterwards. It does not claim a pilot removes all later risk. [3: S02 p.20] [4: S01 p.3]

## Requirements

**Stated by the customer**

- Tablets are made from a powder blend of an active pharmaceutical ingredient (API) and excipients.
- Laboratory checks confirm the blend is on target but arrive after the material has passed the press.
- Goal: assess whether a fiber based measurement in the feed frame can follow API concentration changes.
- The first pilot should compare reasonable measurement options before production equipment is committed.

**Key unknowns**

- API identity, its concentration range, and the required accuracy and response time.
- Whether the API or any excipient fluoresces (this decides how viable Raman and any fluorescence option are).
- Feed-frame environment (temperature, humidity, dust, vibration) and where / at what working distance a probe could be mounted.
- Blend physical properties in the feed frame: particle size, density, flow behaviour and segregation risk.
- Reference laboratory method, its accuracy and its timing relative to the process.
- Whether the target is an absolute API concentration or a relative change / trend.

## Clarification questions (most decision-relevant first)

Q1. What is the API, over what concentration range must it be followed, and what accuracy and response time must the in-line result meet? *Why it matters:* Decides whether NIR sensitivity is adequate at the low end and whether a single method can meet the target. *(affects: method, technique, status)*
Q2. Do the API or the excipients fluoresce? *Why it matters:* Fluorescence background can limit Raman, and it also decides whether a fluorescence option is worth testing. *(affects: method, technique)*
Q3. Where and how could a probe be mounted in the feed frame — is it open or enclosed, and what are the temperature, humidity, dust and vibration conditions and the possible working distance? *Why it matters:* Determines probe geometry, interface to the powder, and whether the fiber link and probe can be installed at all. *(affects: technique, installation)*
Q4. What are the particle size, density and flow behaviour of the blend in the feed frame, and is segregation expected? *Why it matters:* Physical variation can mimic a composition change and must be covered by the calibration. *(affects: technique, status)*
Q5. What is the reference laboratory method, and what are its accuracy and timing? *Why it matters:* The reference values set the standard the in-line measurement is judged against. *(affects: status, technique)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** The sample is an opaque powder, so a backscatter geometry is the natural fit. NIR is named as a widely implemented pharma technique, it penetrates dense solids, and a NIR reflection probe is the one shown in the feed-frame example. Quantitative use needs a chemometric calibration because NIR bands overlap. *Conditions:* Applies if a diffuse-reflection probe can be brought to the flowing powder and the API is present above the detection level of the chosen instrument. [5: S01 p.15] [6: S01 p.5] [7: S01 p.10]
- **R2 · Comparison candidate: Raman, raman probe.** Raman is the other widely implemented pharma technique and gives complementary molecular-backbone information to NIR. It is a single-method comparison against R1. Raman signals are weak and can be swamped by fluorescence, so this must be checked on real blend samples. *Conditions:* Applies if the blend does not show a dominant fluorescence background; the excitation wavelength is a separate choice from the Raman shift. [8: S01 p.15] [9: S01 p.11] [10: S01 p.11]
- **R3 · Comparison candidate: NIR, diffuse reflection remote.** The NIR + Raman combination is a hypothesis to test after the single-method runs, not a demonstrated gain. It should be compared against the better single method, with the sampling location and timing of the two methods aligned. A combined (multispectral) probe is the way to keep both methods on the same small area; on the NIR side this entry is the diffuse-reflection route, including measurement at a distance from the powder. *Conditions:* Only after the single-method NIR and Raman tests, and only if they do not meet the target. [11: S01 p.15] [12: REF §5] [13: REF §5] Later hypothesis, after single-method tests: combine with Raman.
- **R4 · Not recommended: MIR, ATR.** A reader may expect MIR-ATR for pharma, but ATR needs tight contact and suits liquids, pastes and soft solids. A dry powder blend in a feed frame does not provide that contact, so ATR is not a suitable first option here. This is the screening outcome, not a judgement on MIR in other duties. *Conditions:* Not recommended for a dry powder feed frame. [14: S04 p.4]

## Measurement concept

- **Probe and geometry:** Diffuse-reflection (backscatter) NIR probe inserted into the feed frame so the powder flows past the probe tip; Raman measured at the same or a nearby port with a contact probe. Keep both methods on the same small area if a combined test is added.
- **Location:** Feed frame of the rotary tablet press, at the point where the blend passes the probe tip.
- **Fiber link:** Fiber probes let the sensitive spectrometers be placed away from the press (vibration, dust). [15: S01 p.15] [16: S01 p.15] [17: S01 p.5]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected (Vis-NIR silica fibers do not cover the full nominal range). [18: S01 p.10] [19: REF §5] [20: S02 p.6]
- **Raman:** Raman is reported as a Raman shift in cm-1 on the horizontal axis; the laser excitation wavelength is stated separately. The example feed-frame probe used 785 nm excitation. The usable shift range depends on the instrument, probe and excitation chosen. [21: S01 p.11] [22: S01 p.15]

## Risks and uncertainty

- Calibration is specific to the blend matrix. *(rules: R-CAL-1)* [23: REF §5]
- NIR may not have enough sensitivity for a low-level API. *(rules: R-NIR-4)* [24: S01 p.16]
- Physical variation (particle size, surface, segregation, feed-frame turbulence) can mimic a composition change. *(rules: R-GEO-6, R-GEN-5)* [25: S01 p.17] [26: S01 p.7]
- Raman's weak signal can be overwhelmed by fluorescence from the blend. *(rules: R-RAM-1)* [27: S01 p.11]

## First feasibility experiment

1. **1** Prepare representative samples. [28: REF §3]
2. **2** Measure each sample by NIR diffuse reflection and by Raman with fiber probes, and record independent reference values with the customer's laboratory method. [29: S02 p.20]
3. **3** Build a chemometric calibration per method and inspect NIR sensitivity at the low end of the API range. [30: S01 p.10]
4. **4** Compare the NIR + Raman combination against the better single method on the same samples. [31: REF §5]
5. **5** Validate the chosen model on held-out runs or batches and set the go / no-go on the accuracy and response time the customer supplies. [32: REF §3]

**Reference measurements:** The customer's laboratory method is the independent reference for the pilot; its accuracy and timing still need to be stated (see Q5).

**Decision basis:** Go / no-go thresholds (accuracy, response time) must come from the customer; they are not in the sources.

## Assumptions

- The blend stays an opaque, flowing powder at the measurement point.
- A probe can be brought into contact or near-contact with the powder in the feed frame.
- The API concentration varies over a range wide enough for NIR diffuse reflection to see, pending Q1.
- The reference laboratory method can supply time-stamped values for the pilot samples.

## Not covered by the supplied sources

- The customer's specific API, excipient identities, concentration range, required accuracy and response time are not in the supplied material.
- Feed-frame temperature, humidity, dust and vibration conditions and the mounting point are not in the supplied material.
- No source states an achievable fiber-link length or probe rating for this installation.

## Evidence (verified quotes)

1. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press."
2. ✓ **S01 p.15** (application precedent): "and widely implemented spectral techniques are Near-Infrared (NIR) and Raman spectroscopy."
3. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
4. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
5. ✓ **S01 p.15** (application precedent): "NIR spectrometer and light source coupled with a NIR reflection probe"
6. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
7. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
8. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
9. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
10. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
11. ✓ (precedent only) **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
12. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
13. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
14. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
15. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press."
16. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
17. ✓ **S01 p.5** (general): "making it ideal for online applications, including remote measurements via fiber optic probes."
18. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
19. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
20. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
21. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
22. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
23. ✓ **REF §5** (general): "calibration specific to the matrix."
24. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
25. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
26. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
27. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
28. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
29. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
30. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
31. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
32. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 32 of 32 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 5; repair rounds: 1.

*Run D01-20261017T092154Z · models deepseek/deepseek-v4.1-flash · cost $0.0191*
