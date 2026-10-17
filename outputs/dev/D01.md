# First technical assessment: Blend potency in a tablet press feed frame

**Customer enquiry**

> We manufacture tablets from a powder blend containing an active pharmaceutical ingredient and excipients. Laboratory checks tell us whether the blend is on target, but results arrive after the material has moved through the press. We want to assess whether a fiber based measurement in the feed frame could follow API concentration changes. Our first pilot should compare reasonable measurement options before we commit to production equipment.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for a powder blend in a tablet press feed frame, with explicit assumptions. The screening passes NIR diffuse reflection and Raman probe measurements; fluorescence remains conditional on an unknown fluorophore. The customer's central premise is a question to be tested, not a supported fact.

## Premise check

- **Not covered:** A fiber based measurement in the feed frame could follow API concentration changes.. No supplied source demonstrates this for the customer's specific API, blend, or feed frame. The sources show a published example of NIR and Raman in a tablet press feed frame for blend potency, which is a reason to test, not proof for this customer. [1: S01 p.15]
- **Supported:** A pilot comparing measurement options is the right step before committing to production equipment.. The sources describe multi-method trials as the first step in the AFS guided pathway and as a way to select the best method for a process. [2: S02 p.20] [3: S01 p.3]

## Requirements

**Stated by the customer**

- Follow API concentration changes in a powder blend
- Fiber-based measurement in the feed frame
- Pilot to compare measurement options before production commitment

**Key unknowns**

- API identity and whether it is spectroscopically active in NIR, Raman, or fluorescence
- API concentration range and required detection limit
- Excipient composition and potential spectral interferences
- Optical behaviour of the powder blend (opaque, turbid, clear)
- Particle size distribution and its effect on scattering
- Temperature and pressure in the feed frame
- Installation point and available access for a fiber probe
- Cleaning and fouling requirements
- Required accuracy, precision and response time
- Reference method for calibration

## Clarification questions (most decision-relevant first)

Q1. What is the API identity and its concentration range in the blend? *Why it matters:* Determines whether the API has usable NIR or Raman spectral features and whether the required detection limit is within the method's capability. NIR may lack sensitivity for trace components. *(affects: method, technique, go_no_go)*
Q2. What are the excipients and their approximate proportions? *Why it matters:* Excipient absorption and scattering can overlap with API signals and dominate the spectrum. This determines whether a single method can resolve the API or whether a combination is needed. *(affects: method, technique)*
Q3. What is the particle size distribution and flow behaviour of the powder blend in the feed frame? *Why it matters:* Diffuse reflection signals are sensitive to particle size and surface characteristics. Physical variation can mimic composition change, so scatter correction and probe placement depend on this. *(affects: technique, installation)*
Q4. What is the required accuracy, precision, and response time for following API concentration changes? *Why it matters:* Sets the go/no-go criteria for the pilot and determines whether a full-spectrum method or a simplified sensor is appropriate. *(affects: go_no_go, method)*
Q5. What independent reference method is available for API concentration in the blend? *Why it matters:* A calibration model requires reference values. The reference method's accuracy and sampling procedure determine the achievable model quality. *(affects: feasibility_plan, go_no_go)*
Q6. Does the API or any excipient fluoresce under the excitation wavelengths being considered? *Why it matters:* Fluorescence is only applicable if the API or a justified indicator fluoresces. Most chemicals do not, so this determines whether fluorescence can be considered at all and whether fluorescence background could interfere with Raman measurements. *(affects: method, technique)*

## Recommendation

- **R1 · Primary candidate: NIR + Raman (combination: a hypothesis to test), diffuse reflection.** NIR diffuse reflection is the most common online method for powder and scattering samples, and the sources show a published example of NIR in a tablet press feed frame for blend potency. It penetrates several millimetres and works with standard fiber probes. *Conditions:* API has NIR-active functional groups and is present above the NIR sensitivity limit; powder is scattering or opaque. [4: S01 p.5] [5: S01 p.15]
- **R2 · Comparison candidate: Raman, raman probe.** Raman provides complementary molecular information to NIR and is shown in the same feed frame example. It is well suited to powders and can detect API-specific vibrational bands. *Conditions:* API has Raman-active bands and fluorescence background is manageable. [6: S01 p.15] [7: S01 p.11]
- **R3 · Conditional candidate: Fluorescence, fluorescence probe.** Fluorescence is only applicable if the API or a justified indicator fluoresces. Most chemicals do not, so this is conditional on the API identity and the answer to Q6. *Conditions:* API or a defined excipient is fluorescent, or a fluorescent indicator is justified. This is unknown and must be confirmed before considering fluorescence. [8: S01 p.5]
- **R4 · Not recommended: NIR, transmission transflection.** Transmission fails when the sample is too thick, opaque, or fat-rich because light cannot penetrate it. A powder blend in a feed frame is likely opaque or highly scattering, so transmission is not a reasonable first option. *Conditions:* Only if the powder is unexpectedly transparent or semi-transparent. [9: S01 p.18] [10: S01 p.18]

## Measurement concept

- **Probe and geometry:** NIR diffuse reflection probe flush-mounted or inserted into the feed frame to interact with the moving powder. Raman probe for contact measurements at the same location. Fiber optics allow the spectrometers to be located away from vibration and dust.
- **Location:** Feed frame of the rotary tablet press, where the powder blend passes the probe tip.
- **Fiber link:** Silica fibers for NIR and Raman. Metal-coated silica fibers are preferred for Raman to avoid polymer-jacket fluorescence. [11: S01 p.15] [12: S01 p.15] [13: S02 p.7]

## Spectral range

- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber, and probe actually selected. [14: S01 p.10]
- **Raman:** Raman shift is reported in cm-1. The excitation wavelength must be stated separately. The feed frame example used 785 nm excitation. [15: S01 p.11] [16: S01 p.15]

## Risks and uncertainty

- The API may not have sufficiently strong or unique NIR or Raman spectral features at the required concentration. *(rules: R-NIR-4, R-RAM-1)* [17: S01 p.16]
- Particle size, packing density, and flow variation in the feed frame can change the diffuse reflection signal independently of API concentration. *(rules: R-GEO-6, R-GEN-5)* [18: S01 p.17]
- Raman measurements may be swamped by fluorescence from the API, excipients, or contaminants. *(rules: R-RAM-1)* [19: S01 p.11]
- The calibration will be specific to this blend matrix. Any change in excipient composition, particle size, or API form will require re-validation or rebuilding. *(rules: R-CAL-1)* *(no verified source: engineering judgement)*
- The feed frame environment may cause probe fouling, vibration, or temperature effects that degrade measurement stability. *(rules: R-GEN-5)* *(no verified source: engineering judgement)*

## First feasibility experiment

1. **Collect representative powder blend samples spanning the expected API concentration range, including at least three concentration levels (low, target, high) and multiple excipient lots.** Capture chemical and physical variation relevant to the process. *(no verified source: engineering judgement)*
2. **Measure each sample with NIR diffuse reflection and Raman probe, using the same probe geometry intended for the feed frame.** Compare single-method performance before testing combinations. *(no verified source: engineering judgement)*
3. **Obtain independent reference API concentrations for each sample using the customer's laboratory method.** Provide calibration and validation targets. *(no verified source: engineering judgement)*
4. **Build chemometric calibration models (e.g., PLS) for NIR and Raman separately, with appropriate scatter correction for NIR.** Quantify API concentration from spectra. [20: S01 p.10]
5. **Validate models on held-out runs or batches not used in calibration.** Estimate prediction error independent of calibration data. *(no verified source: engineering judgement)*
6. **If single methods are insufficient, test NIR + Raman data fusion and compare against the best single method.** Test whether a combination provides a real gain. [21: S01 p.7]
7. **Define go/no-go criteria from the customer's required accuracy and precision, e.g., root mean square error of prediction (RMSEP) below a specified fraction of the API concentration range.** Provide a numerical basis for deciding whether to proceed to production equipment. *(no verified source: engineering judgement)*

**Reference measurements:** Independent laboratory assay of API concentration in the blend, using the customer's established method.

**Decision basis:** Go/no-go based on prediction error against the customer's required accuracy and precision for following API concentration changes. The numerical criteria must come from the customer.

## Assumptions

- The powder blend is opaque or highly scattering, making diffuse reflection the appropriate NIR geometry.
- The API is present at a concentration above the NIR sensitivity limit and has NIR-active or Raman-active functional groups.
- The feed frame provides a stable, representative measurement point with adequate probe access.
- The customer can provide independent reference API concentrations for calibration samples.
- The API or an excipient does not fluoresce, or fluorescence background is manageable for Raman. This is unknown and must be confirmed.

## Not covered by the supplied sources

- The customer's specific API identity, concentration range, and excipient composition
- The optical behaviour and particle size distribution of the customer's powder blend
- The temperature, pressure, and fouling conditions in the customer's feed frame
- The required accuracy, precision, and response time for this application
- Any performance figures for a specific NIR or Raman instrument, fiber, or probe configuration for this customer's blend
- Whether a combination of NIR and Raman provides a real gain for this specific API and blend
- Whether the API or any excipient fluoresces

## Evidence (verified quotes)

1. ✓ **S01 p.15** (application precedent): "The combination of these techniques is particularly effective because it captures complementary chemical information: NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups."
2. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
3. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
4. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics, as well as standard lamps as light sources, making it ideal for online applications, including remote measurements via fiber optic probes."
5. ✓ **S01 p.15** (application precedent): "The equipment used for such task involves next spectral systems: - NIR spectrometer and light source coupled with a NIR reflection probe - Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
6. ✓ **S01 p.15** (application precedent): "The combination of these techniques is particularly effective because it captures complementary chemical information: NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups."
7. ✓ **S01 p.11** (general): "The Raman spectrometer supplied with this multispectral laboratory is designed to record Raman spectra of various samples, such as liquid mixtures containing organic and inorganic substances, biological tissue, powdered materials of various origins, etc."
8. ✓ **S01 p.5** (general): "Another highly sensitive method, UV/Vis fluorimetry, is based on the secondary emission of excited molecules of certain substances, most often of biological origin. However, most chemicals do not exhibit this property."
9. ✓ **S01 p.18** (general): "Conversely, reflection can work well in highly scattering environments but can be less representative for clear liquids."
10. ✓ **S01 p.18** (general): "While transmission is superior for the high-precision analysis of dilute process streams (like whey filtration), it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
11. ✓ **S01 p.15** (application precedent): "During the experimental action, the probes are inserted directly into the process environment, such as the feed frame of a rotary tablet press. As the powder blend passes the probe tip, the system captures spectra at high speeds without interrupting the production flow."
12. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
13. ✓ **S02 p.7** (general): "Free of Polymer jacket fluorescence for Raman and Fluo- Spectroscopy"
14. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
15. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
16. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
17. ✓ **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
18. ✓ **S01 p.17** (general): "Because the light does not penetrate deeply, the method is sensitive to the surface characteristics and fat globule size."
19. ✓ **S01 p.11** (general): "Furthermore, observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
20. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
21. ✓ **S01 p.7** (method gain): "This often provides a synergistic effect, allowing one to solve a problem that either method alone cannot handle or only partially."

## Verification

- Citations verified: 21 of 21 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 6; repair rounds: 1.
- Removed 4 intake item(s) not quoted verbatim from the enquiry:
  - intake.process[1]: enquiry_quote not found verbatim in the enquiry
  - intake.process[2]: enquiry_quote not found verbatim in the enquiry
  - intake.process[3]: enquiry_quote not found verbatim in the enquiry
  - intake.process[4]: enquiry_quote not found verbatim in the enquiry

*Run D01 · models deepseek/deepseek-v4-pro-0813 · cost $0.0471*
