# First technical assessment: Biomass related monitoring during yeast fermentation

**Customer enquiry**

> We would like an optical measurement during yeast fermentation to help us follow growth and notice changes earlier. Our team has mentioned both a biomass signal and a metabolic signal, but these have not been defined as separate targets. The broth becomes more optically dense as the run develops. We need help turning this request into an initial feasibility study with useful reference measurements.

**Decision status:** Insufficient information for a method choice. The customer has not defined the biomass and metabolic signals as separate targets, and the broth's optical regime is unknown. A conditional shortlist is offered, but the deciding questions must be answered before a method can be selected.

## Premise check

- **Supported:** Optical measurement will help them follow growth and notice changes earlier. The source supports real-time biomass monitoring by UV/Vis. The word 'earlier' is not quantified and must be defined against an independent reference method. [1: S01 p.16]
- **Supported:** There are distinct biomass and metabolic signals to be measured. The source supports that biomass and metabolic signals can be tracked by different optical methods in bioprocessing. It does not confirm that they are distinct or measurable in this customer's broth. [2: S01 p.16]
- **Supported:** An initial feasibility study with useful reference measurements is the appropriate next step. This matches the guidance for a feasibility plan. [3: REF §3]

## Requirements

**Stated by the customer**

- Optical measurement during yeast fermentation.
- Help to follow growth and notice changes earlier.
- A biomass signal and a metabolic signal have been mentioned, but not defined as separate targets.
- The broth becomes more optically dense as the run develops.
- An initial feasibility study with useful reference measurements is requested.

**Key unknowns**

- What exactly is the biomass signal (e.g., cell density, turbidity, viable count) and what reference method defines it?
- What exactly is the metabolic signal (which species, concentration range, required detection limit)?
- What is the expected optical density or turbidity of the broth over the run, and at what point does it become opaque?
- What reference measurements are available and at what sampling frequency?
- What are the required accuracy, detection limit, and response time for earlier change detection?
- Is there any fluorescent species or indicator available for a fluorescence option?

## Clarification questions (most decision-relevant first)

Q1. What exactly is the biomass signal (e.g., cell density, turbidity, viable count) and what independent reference method will define it? *Why it matters:* The choice between UV-Vis transmission, UV-Vis ATR, and NIR diffuse reflection depends on the physical meaning of the biomass signal. *(affects: method, technique, installation)*
Q2. What exactly is the metabolic signal (which species: glucose, ethanol, glycerol, acetate, lactate, etc.), its expected concentration range, and required detection limit? *Why it matters:* Raman and NIR are candidates, but their suitability depends on the target species and whether it is a major or trace component. *(affects: method, technique)*
Q3. What is the expected optical density or turbidity of the broth over the run, and at what point does it become opaque? *Why it matters:* This decides between transmission, ATR, and diffuse reflection geometries. *(affects: technique, installation)*
Q4. What reference measurements are available (offline HPLC, cell dry weight, OD, etc.) and at what sampling frequency? *Why it matters:* Independent reference measurements are required for a meaningful feasibility study. *(affects: method, status)*
Q5. What are the required accuracy, detection limit, and response time for earlier change detection? *Why it matters:* These numbers must come from the customer and define the go/no-go criteria. *(affects: status, installation)*
Q6. What is the fermentation scale and installation point (lab, pilot, production; in-line in reactor, bypass, at-line)? *Why it matters:* This affects fiber length, probe choice, and whether an in-line measurement is practical. *(affects: installation, technique)*

## Recommendation

- **R1 · Primary candidate: UV-Vis, ATR.** UV-Vis can track biomass via turbidity, and a UV-ATR probe can measure high-optical-density or highly scattering fluids without dilution, which matches the broth becoming more optically dense over the run. *Conditions:* Applies if the biomass signal is related to cell density or turbidity and the broth becomes too opaque for a standard transmission path. If the broth remains clear, a transmission or transflection probe is preferred for low-OD liquids. [4: S01 p.16] [5: S01 p.16] [6: S01 p.16] [7: S01 p.18]
- **R2 · Primary candidate: Raman, raman probe.** Raman is well-suited to aqueous media and can provide a molecular fingerprint for metabolites such as glucose, acetate, or lactate, which addresses the metabolic signal for earlier change detection. *Conditions:* Applies if the metabolic target is Raman-active and the broth does not swamp the Raman signal with fluorescence. The laser excitation wavelength must be stated separately from the Raman shift. [8: S01 p.16] [9: S01 p.16] [10: S01 p.11]
- **R3 · Conditional candidate: NIR, diffuse reflection.** NIR diffuse reflection is used for opaque or highly concentrated samples and NIR is a common online method; it can track major components like glucose or glycerol in the millimolar range, but may lack sensitivity for trace compounds below 0.1 percent. It is conditional on the broth being highly scattering and the target being a major component. *Conditions:* Applies only if the broth is opaque or highly scattering and the metabolic target is a major component above the trace level. If the broth is clear, NIR transmission or transflection may be preferred but is not confirmed for this sample. [11: S01 p.17] [12: S01 p.16] [13: S01 p.10]

## Measurement concept

- **Probe and geometry:** For biomass, use a UV-Vis probe; for high-OD broth, an ATR probe is indicated, with transmission or transflection as the preferred geometry only while the broth remains clear. For metabolic signals, a Raman fiber probe is indicated, with NIR diffuse reflection as a conditional alternative for opaque, scattering broth. The measurement should be in-line or at-line at a representative point in the reactor or bypass.
- **Location:** In-line in the reactor or a bypass, or at-line if in-line is not practical. The exact point must be agreed after the optical density and fouling behaviour are known.
- **Fiber link:** Silica fibers are the likely link for UV-Vis and NIR; Raman also uses silica fibers. Actual fiber length, coating, and connector type depend on the selected probe and must be confirmed with AFS. [14: S02 p.6] [15: S02 p.7] [16: REF §3]

## Spectral range

- **UV-Vis:** Nominal UV region is 190-360 nm. The visible range depends on the target and the probe. [17: S01 p.5]
- **NIR:** Nominal NIR range is 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [18: S01 p.10] [19: REF §5]
- **Raman:** Raman is reported as Raman shift in cm-1. The laser excitation wavelength must be stated separately. The usable range depends on the instrument, fiber and probe actually selected. [20: S01 p.11] [21: REF §3]

## Risks and uncertainty

- The biomass and metabolic signals are not defined, so the chosen methods may measure the wrong variable. *(rules: R-PRO-2)* *(no verified source: engineering judgement)*
- The broth's optical density may exceed the usable range of the selected probe; transmission can saturate and ATR samples only a surface layer a few micrometres deep, with contact and fouling risks. *(rules: R-GEO-2, R-MIR-3, R-GEN-3)* [22: S01 p.16] [23: S01 p.13] [24: REF §5]
- Raman signal may be weak or swamped by fluorescence, especially if the broth contains fluorescent compounds. *(rules: R-RAM-1)* [25: S01 p.11] [26: S01 p.11]
- Calibration is specific to the matrix; changes in broth composition or process conditions may require re-validation. *(rules: R-CAL-1)* [27: REF §5]

## First feasibility experiment

1. **Define the two targets and the reference measurements with the customer. For biomass, use an independent reference such as cell dry weight or viable count; for the metabolic signal, use an offline reference such as HPLC or enzymatic assay.** Establish what the optical measurement must predict and how success will be judged. [28: REF §3]
2. **Collect representative samples across the expected chemical and physical variation: early, mid, and late fermentation, and across the range of optical densities or turbidities.** Cover the range of conditions the method must handle, including the increasing optical density. *(no verified source: engineering judgement)*
3. **Measure single methods first: UV-Vis ATR (and transmission or transflection if OD is low), Raman, and NIR diffuse reflection on the same samples. Compare each method's signal against the reference measurements.** Identify which single method best tracks each target before testing any combination. [29: S01 p.16] [30: S01 p.16] [31: S01 p.17]
4. **Build and validate chemometric models on held-out runs or batches: use some fermentation runs for calibration and independent runs for validation.** Test whether the calibration transfers to new runs and does not merely fit the calibration set. [32: REF §5]
5. **Go/no-go: the customer defines numerical criteria (accuracy, detection limit, response time) for each target; the feasibility study passes if the single best method or a justified combination meets those criteria on held-out runs.** Provide a clear, customer-owned basis for deciding whether to proceed. *(no verified source: engineering judgement)*

**Reference measurements:** Independent reference measurements must be agreed with the customer. Examples that may be relevant are cell dry weight or viable count for biomass, and HPLC or enzymatic assay for metabolites. The supplied sources do not specify which references are useful for this particular yeast fermentation.

**Decision basis:** The customer must provide the numerical go/no-go criteria; without them, the study can only report relative performance.

## Assumptions

- The broth is an aqueous liquid.
- The biomass signal is related to cell density or turbidity.
- The metabolic signal is a dissolved or suspended chemical species that can be measured optically.
- The measurement can be made in-line or at-line without sterilisation or cleaning requirements that would rule out a fiber probe.
- A suitable reference method for each target can be obtained at the required sampling frequency.

## Not covered by the supplied sources

- The specific biomass and metabolic targets for this customer's yeast fermentation are not defined in the supplied sources.
- The required reference measurements for this customer's process are not specified in the supplied sources.
- The customer's fermentation scale, installation point, cleaning requirements, and required accuracy, detection limit, and response time are not in the supplied sources.

## Evidence (verified quotes)

1. ✓ **S01 p.16** (general): "UV/Vis spectroscopy can be deployed as a low-cost, robust tool for real-time biomass monitoring, as cell suspension turbidity correlates well with cell density."
2. ✓ **S01 p.16** (general): "While UV/Vis tracks growth, Raman spectroscopy can be used in the same reactor to provide a "molecular fingerprint" for direct detection of specific metabolites like glucose, acetate, or lactate."
3. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
4. ✓ **S01 p.16** (general): "UV/Vis spectroscopy can be deployed as a low-cost, robust tool for real-time biomass monitoring, as cell suspension turbidity correlates well with cell density."
5. ✓ **S01 p.16** (general): "extremely short path length that enables the measurement of "black" or highly scattering fluids without dilution."
6. ✓ **S01 p.16** (general): "the signal in a standard transmission setup becomes saturated because the light cannot penetrate the bulk of the sample."
7. ✓ **S01 p.18** (application precedent): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
8. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
9. ✓ **S01 p.16** (general): "Raman spectroscopy can be used in the same reactor to provide a "molecular fingerprint" for direct detection of specific metabolites like glucose, acetate, or lactate."
10. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
11. ✓ **S01 p.17** (application precedent): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
12. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
13. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
14. ✓ **S02 p.6** (performance figure): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
15. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
16. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
17. ✓ **S01 p.5** (performance figure): "It has very high sensitivity, especially in the UV region (190-360 nm)"
18. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
19. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
20. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
21. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
22. ✓ **S01 p.16** (general): "the signal in a standard transmission setup becomes saturated because the light cannot penetrate the bulk of the sample."
23. ✓ **S01 p.13** (general): "typically at a depth of few microns"
24. ✓ **REF §5** (general): "contact, fouling, compatibility."
25. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
26. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
27. ✓ **REF §5** (general): "calibration specific to the matrix."
28. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
29. ✓ **S01 p.16** (general): "UV/Vis spectroscopy can be deployed as a low-cost, robust tool for real-time biomass monitoring, as cell suspension turbidity correlates well with cell density."
30. ✓ **S01 p.16** (general): "Raman spectroscopy can be used in the same reactor to provide a "molecular fingerprint" for direct detection of specific metabolites like glucose, acetate, or lactate."
31. ✓ **S01 p.17** (application precedent): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
32. ✓ **REF §5** (general): "calibration specific to the matrix."

## Verification

- Citations verified: 32 of 32 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 0; repair rounds: 0.

*Run D05-20261017T102656Z · models deepseek/deepseek-v4.1-flash · cost $0.0405*
