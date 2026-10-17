# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. The sample form is decisive and the deterministic screening gives a usable split: NIR diffuse reflection (contact and standoff) and a Raman probe pass for an opaque powder, while MIR-ATR, all UV-Vis in-line techniques and fluorescence fail for this sample form. So a shortlist of single methods can be justified. What cannot be justified yet: the choice between NIR-only and NIR+Raman, the probe geometry (contact vs standoff), and the numerical go/no-go criteria. All three depend on customer facts that are still unknown, so the recommendation is provisional and conditional.

## Premise check

- **Supported:** A fiber-based spectroscopic measurement placed in the tablet-press feed frame can follow API concentration changes in a powder blend. Supported as a published application precedent only. The source describes NIR and Raman probes inserted into the feed frame of a rotary tablet press for in-line blend potency. This is a reason to test, not proof that it works for this blend on this press. [1: S01 p.14] [2: S01 p.15]
- **Supported:** A first pilot comparing reasonable measurement options is the appropriate gate before committing to production equipment. The AFS pathway places multi-method lab trials before the choice of a solution path, which matches the staged approach the customer asks for. The sources do not define what makes such a trial sufficient, so the go/no-go criteria have to come from the customer. [3: S02 p.20]
- **Not covered:** The existing laboratory checks are adequate as an independent reference for the pilot (sampling point, timing and uncertainty). No supplied source addresses the customer's laboratory method, its sampling point relative to the press, its uncertainty or its turnaround. The customer states results arrive after the material has moved through the press; whether those results can be matched in time and location to an in-line feed-frame measurement is not established by any source and must be clarified. *(no verified source: engineering judgement)*

## Requirements

**Stated by the customer**


**Key unknowns**

- API concentration range and the smallest change (and required accuracy) the in-line measurement must resolve.
- Whether the API or any excipient fluoresces (decides Raman viability and rules fluorescence in or out).
- Whether a probe can contact the powder in the feed frame or needs a standoff window; feed-frame temperature, dust load, cleaning regime and available space.
- The existing laboratory reference: method, sampling point before or after the press, uncertainty and turnaround.
- Blend physical variability: particle size distribution, segregation behaviour and flow rate at the probe.
- Required response time / measurement frequency, and what the result must drive.

## Clarification questions (most decision-relevant first)

Q1. What API concentration range must be covered, what is the smallest concentration change the in-line measurement must resolve, and over what time (update rate)? These numbers set the go/no-go criteria and decide whether NIR reflection alone has enough sensitivity. *Why it matters:* Sets the acceptance figures for the pilot and the single-method vs combination decision. They must come from the customer; no source supplies them. *(affects: method, technique, status)*
Q2. What is the API, what are the excipients, and does any component fluoresce? *Why it matters:* Decides spectral interferences and whether a Raman comparison is worth running (fluorescence background) and whether a fluorescence channel could ever be justified. *(affects: method, technique)*
Q3. Can a probe contact the flowing powder in the feed frame, or is a window / standoff measurement required? What are the temperature, dust level, cleaning regime and available space at the installation point, and how far is the spectrometer? *Why it matters:* Decides contact diffuse reflection vs a standoff geometry, and the probe and fiber link design. *(affects: technique, installation)*
Q4. What is your current laboratory reference method, exactly where is the sample taken relative to the press, what is its uncertainty and how long does it take? *Why it matters:* Without a reference that can be matched to the in-line measurement in time and location, the pilot cannot be evaluated. *(affects: status, installation)*
Q5. What particle size distribution, blend homogeneity and segregation behaviour should the pilot cover, and which production states (start-up, steady state, product changeover) must be represented? *Why it matters:* Defines the sample set for the feasibility experiment and the physical variation the model must survive. *(affects: method, installation)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** Passes screening for an opaque powder. NIR reflection with a fiber probe in the feed frame of a rotary tablet press is the closest published precedent for this exact target, and NIR tolerates scattering solids and remote fiber-probe measurement. *Conditions:* Applies if the probe can be mounted at the feed frame (contact or a defined standoff) and a chemometric model can be built and validated on the customer's blend. The published example is a reason to test, not proof for this blend. [4: S01 p.14] [5: S01 p.15] [6: S01 p.5] [7: S01 p.6]
- **R2 · Comparison candidate: Raman, raman probe.** Raman passes screening for a powder and is described as complementary to NIR (NIR: hydrogen bonds and asymmetric polar groups; Raman: molecular backbone and symmetrical non-polar groups). The published feed-frame work merges synchronised NIR and Raman spectra and reports higher accuracy and robustness than single-method models - that is a hypothesis to test against the best single method, not a given. *Conditions:* Test the Raman probe as a single method alongside NIR first; only then test the synchronised NIR+Raman fusion, and only if the NIR-only model misses the customer's criteria. Check the fluorescence background and the API Raman signal on the real blend. [8: S01 p.15] [9: S01 p.15] [10: S01 p.15] [11: S01 p.6] Later hypothesis, after single-method tests: combine with NIR.
- **R3 · Conditional candidate: NIR, diffuse reflection remote.** A standoff (non-contact) NIR reflection measurement is listed for powders at a distance. It applies only if the feed-frame geometry or the powder flow does not allow a contacting probe, or if a window is needed for cleaning and fouling control. *Conditions:* Conditional on the answer to Q3 (contact vs standoff and available space). Standoff changes the signal (surface-sensitive, distance-dependent), so the model must be built for the geometry actually used. [12: S01 p.6]
- **R4 · Not recommended: MIR, ATR.** A reader would expect MIR-ATR because it is the standard in-line MIR route, but it does not fit this sample: Table 1 lists ATR for liquids, pastes and soft samples, and ATR requires tight contact, which a dry flowing powder blend does not provide. It is also outside the current shortlist because the screening status is fail. *Conditions:* Not proposed for this pilot. Could be reconsidered only if the customer's material or measurement point changes to a liquid, paste or soft solid in contact with the crystal. [13: S01 p.6] [14: S01 p.10]

## Measurement concept

- **Probe and geometry:** NIR diffuse reflection probe mounted at the tablet-press feed frame, either contacting the powder flow or at a defined standoff behind a window; the source precedent is a reflection probe inserted directly into the feed frame. Raman, if tested, uses a separate Raman probe at the same measurement point.
- **Location:** Feed frame of the rotary tablet press. The exact mounting point, window material and cleaning arrangement are not established by any source and must be agreed with AFS.
- **Fiber link:** VIS-NIR silica fibers are the natural link for a NIR reflection probe (stated transmission to 2400 nm). The achievable fiber link length for this installation is not stated for this application; the source states 100-300 m cables made with low-OH silica fibers for remote industrial process control, which is an indication to be confirmed, not a specification. [15: S01 p.15] [16: S02 p.6] [17: S02 p.7] [18: S01 p.15]

## Spectral range

- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected; a silica-fiber probe is stated only to 2400 nm, so the usable window ends below the nominal NIR range. [19: S01 p.10] [20: REF §5] [21: S02 p.6]
- **Raman:** Reported as Raman shift in cm-1 with the laser excitation wavelength stated separately. The pharmaceutical feed-frame example uses 785 nm excitation; the Raman spectrometer in that example works in the visible and short-wave NIR region. The usable shift range depends on the selected laser, spectrometer and probe. [22: S01 p.11] [23: S01 p.15]

## Risks and uncertainty

- Sensitivity: NIR may not resolve small API concentration changes or low-level components. In a bioprocess context the source notes NIR may lack sensitivity below 0.1 percent. Whether this blend and this target need that sensitivity is unknown (Q1). *(rules: R-NIR-4)* [24: S01 p.16]
- Physical variation can be mistaken for chemistry: reflection is sensitive to surface characteristics and particle size, and inhomogeneity, segregation or process turbulence affect the choice of technique and sampling location. *(rules: R-GEO-6, R-GEN-5)* [25: S01 p.17] [26: S01 p.7]
- Calibration is matrix-specific. A model built on one blend, excipient set or particle size distribution may not transfer to another product or after a formulation change, so re-validation would be required. *(rules: R-CAL-1)* [27: REF §5]
- The Raman comparison and the NIR+Raman fusion rest on the API giving a usable Raman signal. Raman signals are weak and can be swamped by fluorescence, and the reported accuracy gain of the fusion is a hypothesis for this blend, not an established result. *(rules: R-RAM-1, R-CMB-1)* [28: S01 p.11] [29: REF §5]

## First feasibility experiment

1. **1** Fix the sample set and the reference before any spectra are taken. [30: REF §3]
2. **2** Off-line first, single methods: measure representative blend samples with a NIR diffuse reflection probe, and separately with a Raman probe, over the expected concentration range and the expected particle size / segregation states. Build a chemometric calibration for API concentration against the reference values. [31: S01 p.10] [32: S01 p.12] [33: S01 p.3]
3. **3** At the feed frame: mount the probe (contact or standoff per Q3) and record during production. Check signal stability, dust and fouling, and whether spectral change tracks the reference samples taken at the same time. [34: S01 p.15]
4. **4** Validate on held-out runs or batches: keep whole production runs out of the calibration and predict them, and compare the prediction against the reference. Repeat the same split for the Raman-only model so the two single methods are compared on equal footing. *(no verified source: engineering judgement)*
5. **5** Only if the NIR single-method model misses the customer's criteria, test the synchronised NIR+Raman fusion at the same measurement point and compare it with the best single method. Alignment of the sampling location and timing is a precondition. [35: S01 p.15] [36: REF §5] [37: S01 p.8]

**Reference measurements:** The customer's existing laboratory method, applied to samples taken at the same time as the in-line measurement. Its uncertainty and its sampling point relative to the press must be established first (Q4).

**Decision basis:** Numerical go/no-go criteria must be supplied by the customer: the concentration range, the smallest change to be resolved, the allowed deviation from the reference, and the false-alarm / missed-change limits. No such figures exist in the supplied sources and none are assumed here.

## Assumptions

- The blend is an opaque dry powder at the feed frame, as stated; if it is wet, granulated or a paste at that point, the MIR-ATR screening result would have to be revisited.
- A probe can be mounted at the feed frame with optical access; the mounting arrangement is not established by any source.
- The customer's laboratory method measures API concentration with an uncertainty small enough to serve as reference; this is unverified.
- The published feed-frame examples are treated as reasons to test, not as evidence of performance on this blend or press.

## Not covered by the supplied sources

- Installation engineering for a feed-frame probe (mounting, window material, cleaning and fouling control) is not covered by the supplied material.
- No performance figures (accuracy, detection limit, response time) for API concentration measurement in a tablet-press feed frame appear in the supplied sources.

## Evidence (verified quotes)

1. ✓ **S01 p.14** (application precedent): "the precise concentration and uniformity of the Active Pharmaceutical Ingredient (API) - directly within the production line, specifically in the feed frame of a rotary tablet press"
2. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
3. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
4. ✓ **S01 p.14** (application precedent): "In-line Monitoring of Blend Potency and Coating Processes"
5. ✓ **S01 p.15** (application precedent): "NIR spectrometer and light source coupled with a NIR reflection probe"
6. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
7. ✓ **S01 p.6** (performance figure): "Diffuse reflection-probe diffuse reflection Scattering media, powder 0.5-1 mm"
8. ✓ **S01 p.15** (general): "NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups."
9. ✓ (precedent only) **S01 p.15** (method gain): "predict API potency or coating thickness with higher accuracy and robustness than single-method models"
10. ✓ (precedent only) **S01 p.15** (method gain): "the synchronized NIR and Raman spectra are merged into a single augmented matrix"
11. ✓ **S01 p.6** (general): "Raman-probe liquid, powder, solid"
12. ✓ **S01 p.6** (performance figure): "surface at a distance solid, powder 2-5 mm"
13. ✓ **S01 p.6** (general): "ATR- platform absorption liquid,paste, soft"
14. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
15. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
16. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
17. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
18. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
19. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
20. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
21. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
22. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
23. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
24. ✓ (precedent only) **S01 p.16** (performance figure): "may lack the sensitivity to detect trace compounds below 0.1 percent."
25. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
26. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
27. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
28. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
29. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
30. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
31. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
32. ✓ **S01 p.12** (general): "Raman spectra (as well as IR absorption spectra) can be used to construct chemometric models-calibration or classification ones."
33. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
34. ✓ **S01 p.15** (application precedent): "captures spectra at high speeds without interrupting the production flow"
35. ✓ (precedent only) **S01 p.15** (method gain): "the synchronized NIR and Raman spectra are merged into a single augmented matrix"
36. ✓ (precedent only) **REF §5** (method gain): "compare with the best single method."
37. ✓ **S01 p.8** (general): "collected from the same small, even pinpoint, area of the sample."

## Verification

- Citations verified: 37 of 37 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 11; repair rounds: 1.
- Removed 5 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[0]: enquiry_quote not found verbatim in the enquiry
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry

*Run D01-20261017T084056Z · models deepseek/deepseek-v4.1-flash · cost $0.0227*
