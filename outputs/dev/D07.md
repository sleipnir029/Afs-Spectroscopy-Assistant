# First technical assessment: API concentration during hot polymer extrusion

**Customer enquiry**

> We are developing a hot polymer extrusion process that incorporates an active pharmaceutical ingredient. We want to investigate whether an optical measurement can detect composition changes while the melt is being processed. We have offline assays, but the process interface is hot and may be exposed to material build up. We need an initial comparison plan and the questions required before choosing a probe.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified from the screening plus one directly analogous application example, but several deciding facts (target species and range, melt optical behaviour, interface temperature/pressure, fluorescence) are still unknown, so the shortlist is provisional and conditional.

## Premise check

- **Not covered:** An optical measurement can detect composition changes in the melt. No supplied source establishes this for this customer's hot polymer melt. A related application example exists (spectra of an API in hot polymer obtained with an ATR probe; NIR-Reflex & MIR-ATR for polymer extrusion in-line, S02 p.14), but an application example is a reason to test, not proof for a new process. [1: REF §3]
- **Not covered:** The existing offline assays are relevant to the process and usable as the reference. The existence of offline assays is a customer fact; whether they are suitable as the independent reference for optical validation is not addressed by the supplied material and must be confirmed. [2: REF §3]

## Requirements

**Stated by the customer**

- Detect composition changes in the melt while it is being processed (in-line).
- Provide an initial comparison plan and the probe-selection questions before choosing a probe.
- The process interface is hot and may be exposed to material build-up.
- Offline assays are available (claimed relevant).

**Key unknowns**

- Target species and expected concentration range; size of the composition change to detect.
- Melt optical behaviour: clear, turbid, opaque or strongly scattering.
- Interface temperature and pressure, and the distance available for the spectrometer/probe link.
- Whether the API or polymer matrix fluoresces under visible/NIR excitation.
- Rate of material build-up at the interface and how it is cleaned.
- Suitability of the offline assay as the independent reference on the trial samples.

## Clarification questions (most decision-relevant first)

Q1. What is the target species, its expected concentration range, and how large a composition change must be detected? *Why it matters:* Sets the required sensitivity/selectivity and could decide between MIR-ATR, Raman and NIR. *(affects: method, technique)*
Q2. Is the melt optically clear, turbid or opaque, and how strongly does it scatter? *Why it matters:* Decides NIR geometry (transmission vs diffuse reflection) and whether ATR is the right interface. *(affects: technique, installation)*
Q3. What are the temperature and pressure at the measurement interface, and at what distance from the process can the spectrometer be placed? *Why it matters:* Decides probe/fiber selection; no source states an achievable MIR link length for a hot melt, so this is an open question for AFS. *(affects: installation, fiber)*
Q4. Does the API or the polymer matrix fluoresce under visible/NIR excitation? *Why it matters:* Fluorescence background can swamp Raman, and fluorescence measurement only works for fluorescing species. *(affects: method)*
Q5. How much material build-up occurs at the interface, and how is the interface cleaned? *Why it matters:* ATR samples only a surface layer and needs tight contact, so build-up/fouling is a direct risk. *(affects: technique, installation)*
Q6. Which offline reference assay is available, and can it be run on the same samples used for the optical trials? *Why it matters:* Validation needs an independent reference measurement on the same material. *(affects: validation)*

## Recommendation

- **R1 · Primary candidate: MIR, ATR.** The only in-line candidate that passed screening as a contact technique, and the one with a directly analogous application example: spectra of an API in hot polymer obtained with a diamond-cone ATR probe coupled to an FTIR, and NIR-Reflex & MIR-ATR used to control polymer extrusion in-line. ATR suits liquids, pastes and soft solids held in tight contact with the crystal, consistent with a melt at the probe. MIR bands are well-defined and selective. Treat as a method to test, not proof for this process. *Conditions:* Requires the melt to make tight contact with the ATR crystal and the crystal material to be compatible with the polymer/API. [3: S02 p.14] [4: S02 p.14] [5: S04 p.4] [6: S01 p.5]
- **R2 · Comparison candidate: Raman, raman probe.** Passed screening. Raman is complementary to MIR for molecular structure, so it is worth measuring the same samples with a second vibrational method. Report as Raman shift (cm-1) with the laser excitation wavelength stated separately. Main risk is weak signal and fluorescence background from the polymer/API, which must be checked on real melt material. *Conditions:* Applicable if the melt gives an acceptable Raman signal above the fluorescence background at the chosen excitation. [7: S01 p.11] [8: S01 p.11] [9: S01 p.11] [10: S01 p.11]
- **R3 · Conditional candidate: NIR, diffuse reflection.** Screening is unknown because the melt's optical regime is not known. NIR diffuse reflection is used for opaque or highly concentrated scattering media, and the S02 p.14 example also used NIR reflection in polymer extrusion. Applies only if the melt is scattering/opaque and the API/matrix have usable NIR bands; otherwise the geometry question (reflection vs transmission/transflection) stays open. *Conditions:* Applies only if Q2 shows the melt is opaque/scattering rather than clear. [11: S02 p.14] [12: S01 p.17] [13: S01 p.5]

## Measurement concept

- **Probe and geometry:** Primary route: an immersion ATR probe (contact, surface layer of a few microns). Comparison route: a Raman probe. Conditional route: an NIR diffuse-reflection probe if the melt scatters. A combination (for example NIR + MIR-ATR) is a later hypothesis to test against the best single method.
- **Location:** In-line at the process interface; the exact installation point and cleaning are open (Q3, Q5).
- **Fiber link:** Fiber family and any remote-link length depend on the method and are not fixed by the sources; long (100-300 m) links are stated only for low-OH silica fibers, and no source states an achievable length for an MIR link, so any MIR link length is an open question for AFS. [14: S02 p.7] [15: S01 p.15]

## Spectral range

- **MIR:** Nominal MIR range 4000-400 cm-1 (2.5-25 µm). The usable range depends on the instrument, fiber and ATR crystal actually selected. [16: S01 p.9]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [17: S01 p.10]
- **Raman:** Raman shift (cm-1) is reported on the spectral axis; the laser excitation wavelength is stated separately and the wavelength for this case is not fixed. [18: S01 p.11]

## Risks and uncertainty

- The melt's optical behaviour and the API/matrix spectra are unknown, so the shortlist may not fit: the NIR geometry (reflection vs transmission) is unresolved, and the target may lack a detectable band. *(no verified source: engineering judgement)*
- ATR samples only a surface layer a few microns deep and needs tight contact; build-up/fouling at the hot interface could corrupt the signal and may require cleaning or a different interface. *(rules: R-MIR-3, R-MIR-2)* [19: S01 p.13]
- No source states a probe temperature/pressure rating or an achievable MIR fiber-link length for a hot polymer melt, so probe and fiber selection (and any remote-link distance) remain open questions for AFS. *(rules: R-FIB-2)* *(no verified source: engineering judgement)*
- The closest precedent (API in hot polymer, S02 p.14) is an application example, not proof for this process; NIR and Raman calibrations are matrix-specific and would have to be built and re-validated on this material. *(rules: R-CAL-1)* [20: REF §5]

## First feasibility experiment

1. **1. Assemble representative melt samples across the expected composition variation (API concentration and any matrix/additive changes) that the customer can produce, and run the existing offline assay on each as the independent reference.** Cover chemical and physical variation; establish the reference for validation. [21: REF §3]
2. **2. Acquire MIR-ATR spectra (primary method) on these samples under process-relevant conditions, keeping sampling location and timing consistent.** Test the best single method first. *(no verified source: engineering judgement)*
3. **3. Acquire Raman spectra (comparison) on the same samples and check the fluorescence background on real melt material.** Test the second single method and the main Raman risk. [22: S01 p.11]
4. **4. If the melt is scattering/opaque, add NIR diffuse reflection and compare each single method against the others; only then test a combination (for example NIR + MIR-ATR) as a hypothesis against the best single method.** Decide the NIR geometry; keep combinations as a later hypothesis. [23: REF §5] [24: REF §5]
5. **5. Validate on held-out runs or batches not used for calibration, and decide go/no-go against the customer's numerical criteria.** Independent validation on unseen material. *(no verified source: engineering judgement)*

**Reference measurements:** The existing offline assay, run on the same samples, is the intended independent reference; its suitability must be confirmed (Q6).

**Decision basis:** The go/no-go thresholds (accuracy, precision, response time) must be supplied by the customer; no such figures are given in the sources or the enquiry.

## Assumptions

- The melt behaves as a viscous liquid that can make contact with a probe at the interface.
- The offline assay can be run on the trial samples as the reference.
- The process can tolerate a probe at the interface and some cleaning/maintenance.

## Not covered by the supplied sources

- Probe temperature, pressure and chemical-compatibility ratings for a hot polymer melt are not given in the supplied material.
- An achievable MIR fiber-link length for this process is not stated in the supplied material.

## Evidence (verified quotes)

1. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer."
2. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
3. ✓ **S02 p.14** (application precedent): "Spectra of API in hot polymer obtained with Diamond cone ATR probe coupled to iC10 FTIR (MTAC)"
4. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
5. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
6. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
7. ✓ **S01 p.11** (general): "This property makes mid-IR and Raman spectra complementary, that is, they complement each other."
8. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
9. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
10. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
11. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
12. ✓ **S01 p.17** (application precedent): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
13. ✓ **S01 p.5** (general): "NIR spectroscopy, with its relatively large penetration depth (up to several millimetres) even into dense solid samples due to low absorption and strong scattering, allows the use of ordinary glass for optics"
14. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
15. ✓ **S01 p.15** (general): "located safely away from the vibration and dust of the manufacturing floor."
16. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
17. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
18. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
19. ✓ **S01 p.13** (general): "typically at a depth of few microns"
20. ✓ **REF §5** (general): "calibration specific to the matrix."
21. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
22. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
23. ✓ **REF §5** (general): "compare with the best single method."
24. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."

## Verification

- Citations verified: 24 of 24 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 1; repair rounds: 1.

*Run D07-20261017T090322Z · models deepseek/deepseek-v4.1-flash · cost $0.0147*
