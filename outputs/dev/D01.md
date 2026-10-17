# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. A short method shortlist can be justified: NIR diffuse reflection and Raman are the only screened techniques that pass for an opaque powder, and there is a published example of NIR and Raman probes inserted in the feed frame of a rotary tablet press (S01 p.15). That example is a reason to test, not proof for this blend (REF §3). The decisive facts - API identity, concentration range, required accuracy, NIR/Raman response of API and excipients - are unknown, so the shortlist is provisional and conditional on the clarification questions.

## Premise check

- **Supported:** A fiber based measurement in the feed frame could follow API concentration changes.. Supported only as an application precedent. The source describes NIR and Raman probes inserted in the feed frame of a rotary tablet press to track blend potency; it is not evidence that it works for this customer's blend. [1: S01 p.15] [2: S01 p.15]
- **Supported:** The feed frame is a suitable measurement location.. The published example places reflection and Raman probes in that location, so it is a reasonable place to test. Whether it is suitable for this press, product and cleaning regime is not covered by the sources. [3: S01 p.15]
- **Supported:** The first pilot can compare reasonable measurement options before production commitment.. Supported at concept level: testing several optical approaches to choose a method or combination is described as the normal route for samples of incompletely known behaviour. [4: S01 p.3]
- **Not covered:** Laboratory checks are a sufficient reference for whether the blend is on target.. No supplied source addresses the adequacy of the customer's laboratory reference. A feasibility plan requires an independent reference measurement, so the reference method and its sampling uncertainty must be clarified; they cannot be assumed sufficient. [5: REF §3]

## Requirements

**Stated by the customer**

- Customer states: tablets are made from a powder blend of API and excipients; lab checks are retrospective; the goal is to assess whether a fiber-based measurement in the feed frame can follow API concentration changes; the first pilot should compare measurement options before production equipment.

**Key unknowns**

- API identity, target concentration and range, required accuracy/precision and response time
- Whether the API or excipients absorb in the NIR or fluoresce
- Physical state in the feed frame (dry, wet, granulated), particle size, moisture, bulk density, flow
- Probe mounting point and feed-frame environment (temperature, dust, vibration, cleaning)
- Laboratory reference method and its sampling uncertainty

## Clarification questions (most decision-relevant first)

Q1. What is the API, at what concentration and range is it present in the blend, and what accuracy, precision and response time must the pilot demonstrate to count as a pass (your go/no-go numbers)? *Why it matters:* These numbers decide whether NIR has enough sensitivity at your API level and define the pass/fail basis. No source gives accuracy, detection limits or response times for this matrix, so they must come from you. *(affects: status, method)*
Q2. Do the API or any of the excipients absorb in the near-infrared, or fluoresce under visible/NIR laser excitation, and at what levels are the excipients present? *Why it matters:* Decides whether NIR and Raman have a usable, specific signal and whether fluorescence should be re-screened. Fluorescence only works for species that actually fluoresce. *(affects: method, technique)*
Q3. In the feed frame, is the blend a dry free-flowing powder or a wet/granulated mass, and what are the typical particle size, moisture and bulk density? *Why it matters:* A wet or paste-like mass would re-open ATR-based options that the current screening rejects for a dry powder, and it changes the probe geometry. *(affects: technique, installation)*
Q4. Where exactly could a probe be mounted in the feed frame (existing port, window, flush insertion), and what are the temperature, dust, vibration and cleaning conditions at that point? *Why it matters:* Decides the probe design, whether the analyzer can sit remotely on a fiber link, and the fouling/cleaning risk at the measurement window. *(affects: installation, technique)*
Q5. What is your current laboratory reference method for blend potency, how is the sample taken from the blend, and what is its measurement uncertainty? *Why it matters:* The pilot must be judged against an independent reference; the reference's own sampling and analytical error limits what the pilot can prove. *(affects: status, installation)*

## Recommendation

- **R1 · Primary candidate: NIR + Raman (combination: a hypothesis to test), diffuse reflection.** The only screened technique that both passes for an opaque powder and has a published in-line precedent in a tablet press feed frame. NIR reflection is described as the common online fiber-probe method and is used for opaque, scattering materials. *Conditions:* Applies if the API gives a measurable, specific NIR response at the concentration of interest and the blend can be presented to a reflection window in the feed frame. Fails if the API level is below the NIR detection capability of the chosen configuration. [6: S01 p.10] [7: S01 p.15] [8: S01 p.17] [9: S01 p.17]
- **R2 · Comparison candidate: Raman, raman probe.** Second passing technique, worth running as a single method against NIR on the same samples. Raman carries molecular-backbone information complementary to NIR, and the feed-frame precedent uses a Raman fiber probe for contact measurement. Excitation wavelength must be chosen; the source example uses 785 nm, which is not a recommendation for your blend. *Conditions:* Applies if the API or an excipient gives a usable Raman signal above the fluorescence background at the chosen excitation wavelength. If the blend fluoresces strongly, single Raman may not be usable. [10: S01 p.15] [11: S01 p.15] [12: S01 p.11]
- **R3 · Not recommended: MIR, ATR.** Not recommended for this application: ATR needs tight optical contact with the sample, which is true for liquid or soft solid samples, not for a dry powder bed passing a probe window. The deterministic screening also returns fail for MIR-ATR on a powder. This would only change if Q3 shows the feed-frame material is wet, paste-like or soft. *Conditions:* Would need re-screening if the material in the feed frame is a wet or paste-like mass. [13: S04 p.4]
- **R4 · Not recommended: Fluorescence, fluorescence probe.** Not recommended on the current facts: fluorescence measures only species that fluoresce, and no fluorescent species or justified fluorescent indicator has been identified in the blend. The deterministic screening returns fail for this reason. It would only become testable if Q2 shows the API or an excipient fluoresces. *Conditions:* Conditional on a fluorescent component being identified in the API or excipients. [14: S01 p.5] [15: S04 p.4]

## Measurement concept

- **Probe and geometry:** For R1: a fiber-optic NIR diffuse-reflection probe, flush-mounted into a port or window in the feed frame so the flowing blend passes the probe tip. For R2: a Raman fiber probe at the same or a directly comparable point. Contact between probe window and flowing powder, and window fouling, are the main mechanical unknowns and are not covered by the sources.
- **Location:** Tablet press feed frame, at the point where the powder blend flows past the probe.
- **Fiber link:** Fiber coupling lets the spectrometers stand away from the vibration and dust of the production floor. Which fiber carries which wavelengths depends on the method and must be confirmed for the actual probe; the nominal method range is not the usable range of a specific instrument, fiber and probe. [16: S01 p.15] [17: REF §5]

## Spectral range

- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected and must be confirmed with AFS for the chosen configuration. [18: S01 p.10]
- **Raman:** Raman is reported as a Raman shift in cm-1, with the laser excitation wavelength stated separately. The excitation wavelength for this application is not yet chosen; the source example uses 785 nm. [19: S01 p.11] [20: S01 p.15]

## Risks and uncertainty

- The shortlist rests on the stated 'powder blend' and the inferred opaque regime. If the material in the feed frame is a wet or paste-like mass, or a much less scattering powder, the deterministic screening result changes. *(rules: R-GEN-5)* *(no verified source: engineering judgement)*
- NIR may not see the API at low concentration. The source notes this limitation for trace compounds in a bioprocess context; your concentration range is unknown, so NIR sensitivity must be tested on your blend. *(rules: R-NIR-4)* [21: S01 p.16]
- Raman signals are weak and can be swamped by fluorescence from the excipients or the API. This must be checked on real blend samples, not assumed. *(rules: R-RAM-1)* [22: S01 p.11]
- NIR and Raman calibrations are matrix-specific. A change of API, excipient or blend composition requires re-validation (usually rebuild or extension) of the model on the new material. *(rules: R-CAL-1)* [23: REF §5]
- The feed-frame example in the sources is a published application, not proof that it works for this blend, press or production use. It justifies a trial, nothing more. *(rules: R-EVI-2)* [24: REF §3]
- Representativeness: a probe at a window sees a small volume. Blend inhomogeneity and flow behaviour can make that volume unrepresentative of the blend that reaches the press. *(rules: R-GEN-5)* [25: S01 p.7]
- A gain from combining NIR and Raman is a hypothesis to test against the better single method, not an established outcome for this blend. *(rules: R-CMB-1)* [26: S01 p.15]
- The customer's laboratory reference may itself carry sampling and analytical error that limits what the pilot can prove. No source covers this. *(rules: R-EVI-2)* *(no verified source: engineering judgement)*

## First feasibility experiment

1. **1. Fix the target and the go/no-go numbers with the customer before any measurement: API concentration range to be covered, required accuracy and precision, required response time and measurement frequency. These are not in the sources and must come from the customer.** Without customer-defined numeric criteria the pilot has no pass/fail basis. *(no verified source: engineering judgement)*
2. **2. Run a laboratory multi-method trial on representative blend samples: NIR diffuse reflection first, Raman second, on the same samples and the same measurement points, each as a single method. Do not start with the combination.** Select the method on evidence rather than on expectation. [27: S01 p.3] [28: REF §3]
3. **3. Sample set must span the expected chemical and physical variation: API levels from below to above target (including off-target and borderline blends), different excipient lots, and the particle-size, moisture and bulk-density ranges seen in production. Sample count and level spacing come from the customer.** A calibration or comparison built on one blend state will not transfer across the variation the process actually shows. [29: S01 p.7]
4. **4. Measure an independent reference for every sample with the customer's existing laboratory method, taken at the same time and from the same blend state as the spectral measurement. The reference method and its uncertainty must be confirmed first (Q5).** Provides the comparison against which the fiber measurement is judged. [30: REF §3]
5. **5. Compare single NIR against single Raman on the same points. Only then test the NIR + Raman combination as a hypothesis: does fusion beat the better single method on held-out data?** A combination gain is a hypothesis and must be demonstrated against the best single method. [31: S01 p.15]
6. **6. In-line feed-frame trial on the press with the selected probe flush-mounted at the agreed port, at production flow. Confirm the probe sees flowing blend, that the window stays clean over a run, and that the spectrometers can sit remotely on the fiber link.** Separates a laboratory spectral response from an installable in-line measurement. [32: S01 p.15] [33: S01 p.15]
7. **7. Validate on held-out runs or batches, not on individual spectra: keep whole runs/batches out of model building and test on them. Re-validate after any change of API, excipient or blend composition.** Tests transfer to new material, which is where matrix-specific calibrations usually fail. [34: REF §5]

**Reference measurements:** Independent laboratory assay of the same blend samples, method and sampling procedure to be confirmed by the customer (Q5).

**Decision basis:** Go/no-go against numeric criteria supplied by the customer (accuracy, precision and response time for API concentration, and acceptable false-alarm/miss rates). No such figures exist in the supplied sources and none are proposed here.

## Assumptions

- The feed-frame material is a dry, opaque, free-flowing powder as stated and inferred; this drives the screening outcome.
- A probe can be mounted so that the blend flows past it without disturbing the press.
- The customer's existing laboratory method can serve as the independent reference.
- NIR diffuse reflection and Raman are comparable on the same sample points.

## Not covered by the supplied sources

- API identity, concentration range, required accuracy, precision or response time
- Excipient composition and levels
- Powder particle size, bulk density, moisture and flow behaviour
- Optical behaviour (NIR absorbance, Raman response, fluorescence) of this blend
- Feed-frame mounting options, temperature, dust, vibration and cleaning requirements
- Achievable fiber or cable length for any link; only low-OH silica cables are quoted with long lengths in the sources, and no source states an achievable length for an MIR link
- Accuracy, detection limits or response times of any method on a pharmaceutical powder blend
- Regulatory or production qualification status for tablet manufacture
- Whether the customer's laboratory reference is adequate
- AFS product codes, prices and component ratings

## Evidence (verified quotes)

1. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
2. ✓ **S01 p.15** (application precedent): "As the powder blend passes the probe tip, the system captures spectra at high speeds without interrupting the production flow."
3. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
4. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems"
5. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
6. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
7. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
8. ✓ **S01 p.17** (general): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products"
9. ✓ **S01 p.17** (general): "the probe is flush-mounted into a pipe or vat to interact directly with the flowing medium"
10. ✓ **S01 p.15** (general): "NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups"
11. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
12. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence)"
13. ✓ **S04 p.4** (general): "the suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head"
14. ✓ **S01 p.5** (general): "most chemicals do not exhibit this property"
15. ✓ **S04 p.4** (general): "it is limited to the samples containing at least one fluorescent component that often has a biological or natural origin"
16. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
17. ✓ **REF §5** (general): "The fiber determines which wavelengths reach the probe."
18. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm)"
19. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
20. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
21. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent"
22. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence)"
23. ✓ **REF §5** (general): "calibration specific to the matrix"
24. ✓ **REF §3** (general): "A published application is a reason to test a method, not proof that it will work for a new customer."
25. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
26. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
27. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems"
28. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
29. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
30. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
31. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
32. ✓ **S01 p.15** (application precedent): "the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press"
33. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
34. ✓ **REF §5** (general): "calibration specific to the matrix"

## Verification

- Citations verified: 34 of 34 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 6; repair rounds: 1.
- Removed 3 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry

*Run D01 · models deepseek/deepseek-v4.1-flash · cost $0.0217*
