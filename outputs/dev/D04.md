# First technical assessment: Glucose and lactate trends in an aqueous bioprocess

**Customer enquiry**

> We run a cell culture process in an aqueous medium. Glucose and lactate are measured from samples, and the delay makes it difficult to see changes promptly. We are exploring an in situ spectroscopy pilot that can be checked against those existing laboratory measurements. The medium and cell population change during the run; we have not yet selected a probe or a calibration strategy.

**Decision status:** Provisional feasibility assessment. A method shortlist can be justified for an aqueous cell-culture pilot, but the choice between Raman, NIR and MIR-ATR depends on concentration ranges, optical density and installation details that the customer has not yet supplied. The recommendation is therefore conditional and the first feasibility experiment is designed to resolve the deciding unknowns.

## Premise check

- **Supported:** In situ spectroscopy can be checked against existing laboratory measurements.. The customer proposes a pilot checked against existing laboratory measurements. This is a reasonable feasibility-study design, not a claim that the method is already validated. *(no verified source: engineering judgement)*
- **Supported:** The delay in laboratory measurements is the reason changes are not seen promptly.. The customer states that the delay makes it difficult to see changes promptly. The sources support the general motivation for in-line or in-situ fiber-optic analysis to obtain results in near real time. [1: S01 p.2]
- **Supported:** The changing medium and cell population are relevant to probe or calibration selection.. The sources state that sample inhomogeneity and process turbulence must be considered when selecting a measurement technique, and that calibrations are matrix-specific. [2: S01 p.7]

## Requirements

**Stated by the customer**

- In situ measurement in an aqueous cell-culture medium
- Targets: glucose and lactate
- Pilot must be checkable against existing laboratory measurements
- Medium and cell population change during the run
- No probe or calibration strategy selected yet

**Key unknowns**

- Concentration ranges for glucose and lactate
- Optical density, turbidity and cell density of the medium
- Matrix composition and potential interferences
- Temperature, pressure and cleaning/fouling conditions at the measurement point
- Required accuracy, precision and response time
- Installation point and probe access
- Reference method details and sampling frequency

## Clarification questions (most decision-relevant first)

Q1. What are the expected concentration ranges for glucose and lactate during the run, and what accuracy and response time do you need? *Why it matters:* This decides whether NIR is viable at all. NIR may lack sensitivity for trace components, and the source cites a limitation below 0.1 percent in a bioprocess context. Raman is more likely to be suitable for lower concentrations in aqueous media. *(affects: method_choice, calibration_strategy)*
Q2. What is the optical appearance of the medium: clear, slightly turbid, highly turbid or opaque, and how does cell density change during the run? *Why it matters:* This determines whether transmission/transflection is possible or whether diffuse reflection or ATR is required. Transmission fails when the sample is too thick, opaque or highly scattering. *(affects: technique_choice, probe_geometry)*
Q3. Where exactly would the probe be installed, and what are the temperature, pressure, cleaning and fouling conditions at that point? *Why it matters:* ATR requires tight contact and samples only a surface layer a few micrometres deep, so deposits on the crystal are a risk. The installation point also determines whether a remote fiber link is needed and what length is required. *(affects: technique_choice, installation, probe_selection)*
Q4. What is the composition of the culture medium beyond glucose and lactate, and are there known fluorescent species or strong absorbers? *Why it matters:* Fluorescence is only usable if a relevant fluorescent species or indicator exists. Strong absorbers or overlapping bands affect NIR and Raman calibration. Raman is well suited to aqueous media because water interferes less than in infrared methods. *(affects: method_choice, calibration_strategy)*
Q5. What laboratory reference method is used for glucose and lactate, and how often are samples taken? *Why it matters:* The reference method defines the independent comparison for the feasibility study and the calibration target. Sampling frequency affects how well the pilot can be checked against existing measurements. *(affects: feasibility_plan, calibration_strategy)*

## Recommendation

- **REC-1 · Primary candidate: Raman + NIR + MIR (combination: a hypothesis to test), raman probe.** Raman is the strongest first candidate for glucose and lactate in an aqueous cell-culture medium. The sources state that Raman is particularly well suited for aqueous environments because water exhibits low absorbance compared with infrared methods, and that Raman can provide a molecular fingerprint for metabolites such as glucose and lactate in a reactor. A combination of Raman with NIR or MIR is a hypothesis to test against the best single method. *Conditions:* Requires confirmation that glucose and lactate are present at concentrations detectable by the selected Raman instrument and that fluorescence background from the medium or cells does not swamp the Raman signal. Combinations should be tested only after single-method feasibility has been established, with sampling location and timing aligned. [3: S01 p.16] [4: S01 p.16] [5: S01 p.7]
- **REC-2 · Conditional candidate: NIR, transmission transflection.** NIR transmission or transflection is a common online method for clear or semi-transparent liquids and can be implemented with robust silica fiber probes. It is worth testing if the medium remains sufficiently transparent and if glucose and lactate are major components rather than trace analytes. *Conditions:* Applies only if the medium is clear or only slightly turbid and if the target concentrations are high enough for NIR sensitivity. If the medium becomes highly turbid or opaque, transmission fails and this option is not suitable. [6: S01 p.18]
- **REC-3 · Conditional candidate: MIR, ATR.** MIR-ATR is a high-selectivity method for liquids and soft solids in contact with the ATR crystal. It could provide well-defined bands for glucose and lactate, but it samples only a surface layer a few micrometres deep and requires tight contact, which makes fouling and surface representativeness important risks in a cell-culture process. *Conditions:* Applies only if the probe can be kept clean and in tight contact with the medium, and if the surface layer is representative of the bulk. The usable MIR range and any remote fiber link length must be confirmed with AFS. [7: S01 p.9] [8: S01 p.10]

## Measurement concept

- **Probe and geometry:** For Raman, a contact Raman probe in the reactor or a flow cell. For NIR, transmission or transflection if the medium is clear, otherwise diffuse reflection. For MIR, an ATR probe in direct contact with the medium.
- **Location:** In situ in the reactor or in a bypass/flow cell, depending on the installation point and fouling conditions.
- **Fiber link:** Silica fibers for Raman and NIR. MIR requires chalcogenide, polycrystalline or hollow-waveguide fibers; the achievable MIR link length is unknown and must be confirmed with AFS. [9: S02 p.6] [10: S02 p.6] [11: S02 p.6]

## Spectral range

- **Raman:** Raman shift in cm-1, with the laser excitation wavelength stated separately. The nominal Raman range depends on the selected laser and spectrometer; no specific range is stated in the sources for this customer. [12: S01 p.11]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [13: S01 p.10]
- **MIR:** Nominal MIR range 4000-400 cm-1. The usable range depends on the instrument, fiber and probe actually selected. [14: S01 p.9]

## Risks and uncertainty

- Raman fluorescence background from the medium or cells could swamp the weak Raman signal. *(rules: R-RAM-1)* [15: S01 p.11]
- NIR may lack sensitivity for glucose and lactate if they are present at low concentrations. *(rules: R-NIR-4)* [16: S01 p.16]
- MIR-ATR samples only a surface layer a few micrometres deep, so fouling or surface deposits could make the measurement unrepresentative of the bulk medium. *(rules: R-MIR-3)* [17: S01 p.13]
- The changing cell population and medium composition may require frequent recalibration or model maintenance. *(rules: R-CAL-1)* *(no verified source: engineering judgement)*
- The achievable MIR fiber link length is unknown from the supplied sources, so a remote MIR installation cannot be assumed. *(rules: R-FIB-2)* [18: S02 p.9]

## First feasibility experiment

1. **Collect representative samples across the expected chemical and physical variation of the cell-culture run, including different glucose and lactate concentrations, cell densities and turbidity levels.** Ensure the calibration and validation data cover the range of conditions the pilot will encounter. *(no verified source: engineering judgement)*
2. **Measure each sample with the selected single methods first: Raman probe, NIR transmission/transflection or diffuse reflection depending on optical regime, and MIR-ATR if contact and fouling permit.** Establish which single method can detect glucose and lactate with sufficient signal quality before considering combinations. *(no verified source: engineering judgement)*
3. **Obtain independent reference measurements for glucose and lactate using the customer's existing laboratory method on the same samples.** Provide the reference values for calibration and validation. *(no verified source: engineering judgement)*
4. **Build chemometric calibration models for glucose and lactate from the spectral data and reference values, using appropriate preprocessing and validation.** Test whether the spectral data contain usable information for the target analytes. *(no verified source: engineering judgement)*
5. **Validate the models on held-out runs or batches that were not used for calibration.** Estimate prediction performance under conditions closer to routine use. *(no verified source: engineering judgement)*
6. **Compare the best single method against any proposed combination of methods only after single-method feasibility is established.** Test whether a combination provides a real gain over the best single method. *(no verified source: engineering judgement)*
7. **Define go/no-go criteria with the customer using numerical targets for accuracy, precision and response time based on their process requirements.** Provide an objective basis for deciding whether to proceed to a full pilot or sensor development. *(no verified source: engineering judgement)*

**Reference measurements:** Existing laboratory measurements of glucose and lactate on the same samples or process states.

**Decision basis:** Go/no-go criteria must be set by the customer from their required accuracy, precision and response time. The sources do not provide numerical criteria for this application.

## Assumptions

- The medium is liquid and aqueous, as stated.
- The cell population makes the medium at least somewhat heterogeneous and scattering.
- Glucose and lactate are present at concentrations that may be detectable by Raman or NIR, but this is unconfirmed.
- The pilot is for feasibility testing, not for immediate process control or clinical use.

## Not covered by the supplied sources

- Specific detection limits for glucose or lactate by any method in this customer's medium
- Achievable MIR fiber link length for a remote installation
- Numerical accuracy, precision or response-time targets for this application
- Product codes, prices or component ratings for a specific AFS configuration
- In vivo or production-ready evidence for this specific cell-culture application

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "Fiber optic probes and cells are being integrated into reactors and production lines of ongoing technological processes, enabling on-site online analysis and obtaining results in near real time."
2. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
3. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
4. ✓ **S01 p.16** (application precedent): "Raman spectroscopy can be used in the same reactor to provide a "molecular fingerprint" for direct detection of specific metabolites like glucose, acetate, or lactate."
5. ✓ **S01 p.7** (method gain): "The analysis of such systems may require a combination of two or even more spectral methods. This often provides a synergistic effect, allowing one to solve a problem that either method alone cannot handle or only partially."
6. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
7. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
8. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
9. ✓ **S02 p.6** (general): "Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
10. ✓ **S02 p.6** (general): "Chalcogenide As-S IR Fibers 6500 nm"
11. ✓ **S02 p.6** (general): "Polycrystalline Infrared Fibers 17 μm"
12. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
13. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
14. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
15. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
16. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
17. ✓ **S01 p.13** (general): "The MIR-ATR component captures the "chemical fingerprint" of the tissue's surface layer, typically at a depth of few microns, providing information on molecular composition and biochemical changes."
18. ✓ **S02 p.9** (general): "PIR-Fiber & HWG Cables for QCL, OPO, CO- & CO2-Lasers"

## Verification

- Citations verified: 18 of 23 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 6; soft warnings: 2; repair rounds: 2.
- Removed 5 citation(s) that failed verification:
  - ⚠ premise_checks[0].citations[0]: REF p.3 "A feasibility plan needs representative samples or process states, independent reference measurements, a defined compari"
  - ⚠ premise_checks[2].citations[1]: REF p.5 "NIR and Raman calibrations are specific to the matrix; after a change of sample matrix or composition the calibration mu"
  - ⚠ recommendations[0].citations[3]: REF p.5 "Combining methods can help for complex samples, but a gain is a hypothesis; compare with the best single method and alig"
  - ⚠ recommendations[1].citations[1]: S01 p.18 "Transmission fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
  - ⚠ risks[3].citations[0]: REF p.5 "NIR and Raman calibrations are specific to the matrix; after a change of sample matrix or composition the calibration mu"
- ⚠ numbers_uncited_text at clarification_questions[0]: figures in uncited text must come from the enquiry: ['0.1 percent']

*Run D04 · models deepseek/deepseek-v4-pro-0813 · cost $0.0575*
