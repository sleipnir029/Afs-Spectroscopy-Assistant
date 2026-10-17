# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for an opaque powder measured in-line: NIR diffuse reflection passed screening and a published pharmaceutical example mounts a NIR reflection probe in a tablet-press feed frame; Raman is the second single method to compare. The blend-specific performance, acceptance numbers and feed-frame installation details are not known, so the shortlist is conditional on the questions below.

## Premise check

- **Not covered:** A fiber based measurement in the feed frame could follow API concentration changes. The sources contain a published pharmaceutical in-line example in a tablet-press feed frame, but they do not establish that it works for this customer's blend. The example is a reason to test, not proof. [1: S01 p.15]
- **Not covered:** The feed frame is the appropriate location for the measurement. A feed-frame mounting is described in the sources as an example, but no supplied source compares the feed frame against other sampling locations (blender, at-line, transfer line) for this or a similar powder blend. [2: S01 p.15]
- **Supported:** A first pilot comparing reasonable measurement options is sufficient before committing to production equipment. The sources describe testing several optical approaches on incompletely known samples in order to select the most suitable method or combination, which matches a comparison pilot before equipment commitment. [3: S01 p.3]
- **Supported:** The delay of laboratory checks after the press is the problem to solve with in-line measurement. The stated advantage of in-line fiber-probe analysis is exactly the removal of the sampling delay and the risk of contamination. [4: S01 p.3]

## Requirements

**Stated by the customer**

- Compare reasonable measurement options in a first pilot before committing to production equipment.
- Follow API concentration changes in the feed frame of a tablet press, with the result available before the material passes through the press.

**Key unknowns**

- API identity, target concentration and expected variation range (decides whether NIR sensitivity is sufficient).
- Excipient composition and whether any blend component fluoresces strongly (Raman background).
- Required accuracy, precision, detection limit and response time for the in-line result, plus the reference laboratory method and its uncertainty.
- Particle size distribution, moisture, bulk density and flow behaviour of the blend (scatter and calibration effects).
- Feed-frame installation: available port, working distance, window material, fiber length, temperature, cleaning and powder build-up.
- Whether the pilot may start off-line/at-line on sampled blend before any in-line probe is installed.

## Clarification questions (most decision-relevant first)

Q1. What is the API, its target concentration and its expected variation range in the blend, and what accuracy, precision, detection limit and response time must the in-line result meet? *Why it matters:* These numbers decide whether NIR sensitivity is sufficient and set the go/no-go basis; they are not in the sources. *(affects: method choice, go/no-go basis, status)*
Q2. What are the excipients, and does any blend component fluoresce strongly under the proposed Raman excitation laser? *Why it matters:* A strong fluorescence background can swamp the weak Raman signal and change the Raman technique or the excitation wavelength. *(affects: technique choice)*
Q3. What physical variation must the method tolerate (particle size distribution, moisture, bulk density, flow in the feed frame), and what is the reference laboratory method with its uncertainty? *Why it matters:* Physical variation can mimic a concentration change, and the in-line error cannot be assessed more precisely than the reference method. *(affects: calibration, pilot design)*
Q4. What feed-frame installation is available: port, working distance, window material, fiber length, temperature, and cleaning / powder build-up behaviour? *Why it matters:* These decide the probe geometry and whether a fiber link of the required length can be used; no source states an achievable MIR link length. *(affects: installation, probe geometry)*
Q5. May the pilot begin with off-line / at-line measurements of sampled blend before any in-line probe is installed? *Why it matters:* It changes the order and the cost of the first feasibility experiment. *(affects: pilot design)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** This candidate passed screening. NIR diffuse reflection is the route described for opaque, scattering samples, and a published pharmaceutical example mounts a NIR reflection probe in a tablet-press feed frame. This is a reason to test it on this blend, not proof that it will follow the API here. *Conditions:* Applies as long as the API concentration is high enough for NIR to see it; if the API is low-dose this entry may be replaced by R2 or the combination R3. [5: S01 p.17] [6: S01 p.15]
- **R2 · Primary candidate: Raman, raman probe.** This candidate passed screening. Raman is the second single method to compare on the same material: it is a vibrational method suited to powders and, in the published example, a Raman fiber probe is used for contact measurements in the same feed-frame setting. The sources describe NIR and Raman as carrying complementary information, which makes Raman the natural single-method comparator. *Conditions:* Applies if the blend does not show a strong fluorescence background; check this on real samples first. The Raman shift axis and the laser excitation wavelength must be reported separately. [7: S01 p.15] [8: S01 p.15]
- **R3 · Comparison candidate: NIR, diffuse reflection remote.** A combined NIR reflection + Raman measurement is a later hypothesis to test against the better of R1 and R2 after the single-method tests. The published example describes a multispectral NIRaman fiber probe that combines NIR reflection and Raman in one shaft fitting the tablet-press feed frame. The NIR channel of that combination is entered here as the remote-probe variant of NIR diffuse reflection, because in the in-line case the spectrometer sits away from the process point; this is the same optical technique as R1, listed separately only to keep one entry per method and technique. The sources warn that a combination gain must be tested, not assumed, and that the sampling location and timing must be aligned. *Conditions:* Only if no single method meets the customer's acceptance numbers. It requires a combined probe or two probes measuring the same small area and synchronised to a common time step. [9: S01 p.15] [10: S01 p.15] [11: REF §5] [12: REF §5] Later hypothesis, after single-method tests: combine with Raman.
- **R4 · Not recommended: MIR, ATR.** This candidate failed screening for a dry powder. ATR needs tight optical contact and suits liquids, pastes and soft solids, and it samples only a surface layer a few micrometres deep, so a powder bed at the feed frame cannot be relied on to give the required contact. It is listed here only because it is the in-line fiber technique a reader would expect from the sources. *Conditions:* Not recommended for this powder sample. [13: S04 p.4] [14: S01 p.13]

## Measurement concept

- **Probe and geometry:** NIR diffuse reflection with a fiber probe, as the single method to test first; Raman probe contact measurement as the second single method for comparison. A flush-mounted reflection probe interacting directly with the flowing powder is the geometry shown in the published feed-frame example.
- **Location:** Feed frame of the tablet press for the in-line step; the same samples measured off-line/at-line in the first steps of the pilot.
- **Fiber link:** Fiber type and length depend on the final configuration and are not fixed by the sources; the usable spectral coverage, fiber length and probe ratings depend on the configuration and the sample. [15: S01 p.17] [16: REF §5]

## Spectral range


## Risks and uncertainty

- The calibration is matrix-specific: a change of API grade, excipient source or blend composition requires re-validation, and usually rebuild or extension, on the new material. *(rules: R-CAL-1)* [17: REF §5]
- NIR may not see a low-dose API: the sources state that NIR may lack sensitivity for trace compounds below 0.1 percent. If the API is low-dose, NIR alone may not follow it and Raman or a combination becomes the deciding test. *(rules: R-NIR-4)* [18: S01 p.16]
- Physical variation (particle size, density, flow/turbulence in the feed frame) can change the diffuse-reflection signal in a way that looks like a concentration change, so the pilot must separate chemical from physical variation. *(rules: R-GEO-6, R-GEN-5)* [19: S01 p.7]
- The Raman signal is weak and can be swamped by fluorescence from the blend, so the fluorescence background has to be checked on real samples before Raman can be relied on. *(rules: R-RAM-1)* [20: S01 p.11]

## First feasibility experiment

1. **Assemble representative blend samples spanning the expected API concentration range (on-target, deliberately low, deliberately high) and the expected physical variation (particle size, moisture, bulk density), each with an independent reference assay by the customer's laboratory method.** Give the pilot a reference basis and cover the variation the in-line result must survive. [21: REF §3]
2. **Measure all samples off-line with a NIR diffuse-reflection fiber probe, then with a Raman fiber probe at the same sample positions. Record the Raman excitation wavelength separately from the Raman shift axis.** Single methods first, on identical material, so the two techniques can be compared directly. *(no verified source: engineering judgement)*
3. **Build and cross-validate a chemometric calibration for each single method against the reference assay values and report the error of each method on held-out samples.** Establish which single method can follow API concentration before any combination is considered. [22: S01 p.10]
4. **Install the better single method at the feed frame and run it on production-representative runs, taking reference samples from the feed frame during the run for validation on held-out runs or batches.** Test the method under real feed-frame conditions (flow, dust, vibration, build-up) rather than only on static samples. [23: S01 p.15]
5. **Only if no single method meets the customer's acceptance numbers, test the NIR + Raman combination on the same samples and compare it with the best single method, keeping the sampling point and the time step aligned.** Treat the combination gain as a hypothesis to test, not as the default. [24: REF §5] [25: S01 p.8]

**Reference measurements:** The customer's existing laboratory check on the blend is the reference method; its uncertainty must be stated, because the in-line error cannot be assessed more precisely than the reference.

**Decision basis:** Go / no-go numbers (accuracy or prediction error, repeatability, detection limit, response time) are not given in the enquiry and are not in the sources. The customer must set these numbers before the pilot; the pilot then compares each method's measured error against them. No performance figure can be promised here.

## Assumptions

- The blend is a dry, opaque, scattering powder at the feed frame.
- The pilot can include off-line or at-line measurements of sampled blend before an in-line probe is installed.
- A NIR diffuse-reflection probe can be mounted at the feed frame without disturbing the powder flow; this has to be confirmed by the customer's engineering team.

## Evidence (verified quotes)

1. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press."
2. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press."
3. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
4. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
5. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
6. ✓ **S01 p.15** (application precedent): "NIR spectrometer and light source coupled with a NIR reflection probe"
7. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
8. ✓ **S01 p.15** (general): "while Raman provides information on the molecular backbone and symmetrical non-polar groups."
9. ✓ **S01 p.15** (application precedent): "A multispectral NIRaman fiber probe has industrial grade design that combines NIR reflection and Raman optical techniques in a compact shaft that fits in a tablet press feed frame."
10. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
11. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
12. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
13. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
14. ✓ **S01 p.13** (general): "typically at a depth of few microns"
15. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium."
16. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
17. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
18. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
19. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
20. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
21. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
22. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
23. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press."
24. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
25. ✓ **S01 p.8** (general): "collected from the same small, even pinpoint, area of the sample."

## Verification

- Citations verified: 25 of 25 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 7; repair rounds: 2.
- Removed 4 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[0]: enquiry_quote not found verbatim in the enquiry
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry

*Run D01-20261017T092908Z · models deepseek/deepseek-v4.1-flash · cost $0.0333*
