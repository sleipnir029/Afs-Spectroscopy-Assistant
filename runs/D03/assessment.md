# First technical assessment: A clear whey stream before concentration

**Customer enquiry**

> Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the reference. The stream can become more turbid under some operating conditions. We need a first measurement concept that handles this change rather than assuming the liquid always remains clear.

**Decision status:** Provisional feasibility assessment. A short method shortlist can be justified from the supplied sources, but it rests on assumptions the customer has not confirmed (protein range, turbidity range, installation, laboratory reference). The numerical criteria that would define success are missing, so no method can yet be called sufficient for this stream.

## Premise check

- **Not covered:** The stream is relatively clear.. This is a statement about the customer's own process. No supplied source describes this whey stream, its clarity or its variability. It is taken as a stated starting condition, not as a verified fact. *(no verified source: engineering judgement)*
- **Supported:** Spectroscopy is able to track protein concentration.. Supported only as an application precedent in dairy (milk), not as proof for this whey stream or this installation. The source describes in-line dairy NIR monitoring with PLS regression used to quantify fat and protein. [1: S01 p.17]
- **Not covered:** Laboratory results are suitable as the reference.. No supplied source evaluates the customer's laboratory protein method, its uncertainty, or its time alignment with an in-line measurement. The feasibility guidance only states that independent reference measurements are needed; it does not qualify this customer's reference method. *(no verified source: engineering judgement)*
- **Not covered:** A single first measurement concept can handle the change from clear to more turbid.. No source states that one technique covers both physical states for a stream of this kind. For dairy the source prefers transmission for clear liquids but notes it fails when the stream becomes too thick or fat-rich, that reflection is less representative for clear liquids, and that keeping both techniques gives the flexibility to cover the production chain; a transflection probe is described as a combined solution 'in some cases'. Single-concept coverage should therefore be treated as a hypothesis to test, not as an established capability. [2: S01 p.18] [3: S01 p.18]
- **Supported:** The liquid must not be assumed to always remain clear.. The source treats the physical state of the stream as a factor that decides the technique, so a fixed 'always clear' assumption is not safe. [4: S01 p.18]

## Requirements

**Stated by the customer**

- Track protein concentration in a whey stream before a concentration stage.
- Follow the stream as it changes over time.
- Use laboratory results as the reference.
- One first measurement concept should cope with the stream becoming more turbid under some operating conditions.

**Key unknowns**

- Protein concentration range and the accuracy, precision and response time that define success.
- Range, frequency and duration of the turbidity variation.
- Whether the measurement is in-line or at-line, and the available optical pathlength.
- Distance from the process point to a safe place for the spectrometer.
- Temperature, pressure and cleaning/fouling regime at the point.
- Presence of a fluorescent species at a useful concentration.
- Details of the laboratory reference method and its time alignment.

## Clarification questions (most decision-relevant first)

Q1. What protein concentration range must be covered, and what accuracy, precision and response time define success? *Why it matters:* These numbers decide the method and provide the go/no-go basis. No source supplies them, and without them no method can be judged sufficient. They also matter for NIR, which may lack sensitivity for trace components. *(affects: method choice, decision status, go/no-go criteria)*
Q2. How far and how fast does the turbidity change? What are the clearest and the most turbid states the point can see, and do both occur within one run? *Why it matters:* This decides whether one geometry is enough or whether the concept must switch between transmission and a contact technique, and whether the turbid state occurs often enough to be measured in a trial. *(affects: technique choice, measurement geometry, trial design)*
Q3. Does the stream contain a fluorescent species at a useful concentration (the source lists NADH, tryptophan and riboflavin as intrinsic fluorophores in bioprocesses)? *Why it matters:* Fluorescence is screened as 'unknown' because no fluorescent species or indicator has been identified. The answer decides whether a fluorescence channel is worth including at all. *(affects: method set)*
Q4. Is the measurement in-line in a pipe or flow cell, or at-line? What optical pathlength is available, and how far is a safe location for the spectrometer from the process point? *Why it matters:* In NIR transmission the pathlength must be controlled, and the fiber link depends on the distance and on the fiber family that matches the chosen method. *(affects: installation, measurement geometry, fiber link)*
Q5. What are the temperature, pressure and cleaning regime at the measurement point, and how much fouling or deposit is tolerated before cleaning? *Why it matters:* A contact technique such as ATR needs tight contact and is sensitive to deposits on the crystal, so this decides whether a contact option is practical at this point. *(affects: installation, technique choice)*
Q6. Which laboratory method is used for protein, what is its uncertainty, and how are samples taken and time-aligned with the spectral measurement? *Why it matters:* The laboratory result is the reference for the whole trial; its uncertainty and time alignment set the achievable agreement and could change how the trial is designed. *(affects: trial design, decision status)*

## Recommendation

- **R1 · Primary candidate: NIR + NIR + Raman (combination: a hypothesis to test), transmission transflection.** The measurement point is a relatively clear, semi-transparent aqueous stream, which is the case the source describes for NIR transmission/transflection in dairy, and whey is named explicitly. NIR also has an in-line dairy precedent for quantifying fat and protein with PLS regression. Transflection is included in the same technique family because the source notes it can in some cases serve both low-fat and high-fat products, which is relevant to the clear-to-turbid change, but this is a hypothesis to test. *Conditions:* Applies while the stream remains transparent to semi-transparent at the chosen pathlength. If the turbid state kills the transmitted signal, this option must be re-examined and the conditional MIR-ATR option becomes relevant. [5: S01 p.18] [6: S01 p.17] [7: S01 p.18] [8: S01 p.10] [9: S01 p.10]
- **R2 · Comparison candidate: Raman, raman probe.** Proposed by the customer. Raman is well suited to aqueous media and its spectra are complementary to infrared spectra, giving molecular-backbone information that NIR does not. It is included as a comparison against the NIR option on the same samples, not as a replacement for it. *Conditions:* Worth measuring in the trial in any case, but only useful if the Raman signal is not swamped by fluorescence background and if the protein level gives a usable signal. No laser excitation wavelength is assumed here; it must be selected separately from the Raman shift range. [10: S01 p.16] [11: S01 p.11] [12: S01 p.11] [13: S01 p.11] [14: S01 p.12]
- **R3 · Conditional candidate: MIR, ATR.** MIR-ATR samples only a few micrometres at the crystal, so bulk turbidity of the stream matters far less than in a transmission path, and MIR carries the well-defined protein amide bands. It is the natural fallback if the turbid state degrades the transmission measurement, or if protein-specific band information is needed for selectivity. *Conditions:* Applies only if the trial shows the more turbid state degrades the transmission option, or if protein-specific bands are required. ATR needs tight contact and suits liquids and soft solids. The MIR fiber family and the achievable link length are open questions, not assumptions. [15: S01 p.9] [16: S01 p.10] [17: S01 p.10] [18: S04 p.3] [19: S01 p.5]

## Measurement concept

- **Probe and geometry:** Start with NIR transmission or transflection through the whey stream with a controlled optical pathlength, and compare it on the same samples with a Raman probe. Hold MIR-ATR in reserve as the contact fallback for the turbid state. For a contact ATR head, the sample must be a liquid or soft solid that can make tight contact with the crystal.
- **Location:** At the point before the concentration stage. In-line (pipe or flow cell) is the target if a suitable interface exists; at-line sampling is an acceptable first-trial substitute.
- **Fiber link:** The source notes that probes allow analysis at a significant distance from the spectrometer, and states 100-300 m cables for low-OH silica fibers. No achievable length is stated for a MIR link, so the MIR fiber type (for example CIR or PIR) and its length remain open questions for AFS. See the fiber coverage notes from the earlier steps. [20: S01 p.10] [21: S04 p.4] [22: S02 p.7]

## Spectral range

- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected and is not fixed by this assessment. [23: S01 p.10]
- **Raman:** Raman is reported as a Raman shift (cm-1) with the laser excitation wavelength stated separately. No excitation wavelength is assumed here; it must be chosen for the application. [24: S01 p.11]
- **MIR:** Nominal MIR range 4000-400 cm-1. The usable range depends on the fiber (for example CIR or PIR) and ATR crystal actually selected, and on the MIR link length, which is not stated in the sources. [25: S01 p.9]

## Risks and uncertainty

- Matrix-specific calibration. *(rules: R-CAL-1)* [26: REF §5]
- The turbid state may break the primary transmission measurement. *(rules: R-GEO-2, R-GEO-4)* [27: S01 p.18] [28: S01 p.18]
- NIR may lack sensitivity for trace-level protein. *(rules: R-NIR-4)* [29: S01 p.16]
- Raman signal weakness and fluorescence background. *(rules: R-RAM-1)* [30: S01 p.11]
- ATR contact, shallow sampling and fouling. *(rules: R-MIR-2, R-MIR-3)* [31: S04 p.1] [32: S04 p.4]
- Fiber and link limitations, especially for MIR. *(rules: R-FIB-1, R-FIB-2)* [33: S02 p.7]
- Sample inhomogeneity and process turbulence can make the sampling point unrepresentative. *(rules: R-GEN-5)* [34: S01 p.7]
- The evidence base is dairy and other matrices, not this whey stream. *(rules: R-EVI-2)* [35: REF §3]

## First feasibility experiment

1. **Define the sample and process-state set.** Representative whey samples across the expected protein range and across both physical states (the clearest and the most turbid conditions the process shows), taken from several runs or days. [36: REF §3]
2. **Obtain independent laboratory reference values on the same samples.** Run the customer's laboratory protein method on the same samples with documented uncertainty and time alignment to the spectral measurements. *(no verified source: engineering judgement)*
3. **Measure each single method first, on the same samples and in both physical states.** NIR transmission/transflection at a controlled pathlength (test more than one pathlength), Raman with a probe, and, conditionally, MIR-ATR. [37: S01 p.18]
4. **Compare single methods against the reference.** Report prediction error per method, treating the turbid state as a separate group so that a method which only works when clear is visible as such. *(no verified source: engineering judgement)*
5. **Only after the single methods are compared, test the combination.** Test NIR + Raman data fusion against the best single method; a gain from combining methods is a hypothesis, not an established result. [38: S01 p.7] [39: S01 p.15] [40: S01 p.15]
6. **Validate on held-out runs or batches.** Split by run or batch, not by random points within a run, and check that the model holds in both the clear and the turbid state. *(no verified source: engineering judgement)*
7. **Set the go/no-go basis from the customer's numbers.** The customer supplies the required accuracy, precision, response time and range. Without those figures no method can be declared sufficient; the trial provides evidence for the choice, not process readiness. *(no verified source: engineering judgement)*

**Reference measurements:** Independent laboratory protein values on the same samples, with documented uncertainty and time alignment to the spectral measurements. No source states a suitable laboratory method for whey protein, so the customer's method is taken as given but must be described.

**Decision basis:** Go/no-go thresholds come from the customer. No numerical criteria are available from the enquiry or the sources, so they cannot be set here.

## Assumptions

- The stream is aqueous and its protein content lies in a range that NIR or Raman can see; the range is not stated by the customer.
- The measurement can be brought into contact with the liquid (flow cell, pipe interface or at-line sampling).
- The turbid state is still a liquid that light can enter at a short pathlength; this is not verified.
- The customer's laboratory protein result is available for the same samples with acceptable time alignment.
- No fluorescent species or indicator has been identified in the stream.

## Not covered by the supplied sources

- No whey-specific spectra, protein model or performance data. Whey is named only as an example of a stream suited to NIR transmission; the dairy examples given are milk.
- No accuracy, precision, detection limit, response time, temperature or pressure figures for this application.
- No achievable fiber or cable length for an MIR link (long cable figures are stated only for silica fibers).
- No AFS product codes, prices or component ratings.
- No data on the fluorescence of whey or on any specific fluorophore in this stream.
- No statement that any method is ready for production or clinical use.

## Evidence (verified quotes)

1. ✓ **S01 p.17** (application precedent): "before using Partial Least Squares (PLS) regression to quantify fat and protein"
2. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
3. ✓ **S01 p.18** (general): "having both fiber optic techniques available in a lab rather than relying on one provides the flexibility needed to monitor the entire production chain."
4. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
5. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
6. ✓ **S01 p.17** (application precedent): "before using Partial Least Squares (PLS) regression to quantify fat and protein"
7. ✓ **S01 p.18** (general): "The key experimental action is the precise control of the optical pathlength (usually 1 - 10 mm)"
8. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules"
9. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
10. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
11. ✓ **S01 p.11** (general): "This property makes mid-IR and Raman spectra complementary, that is, they complement each other."
12. ✓ **S01 p.11** (general): "measuring Raman spectra is hampered by the low intensity of Raman signals, which are several orders of magnitude weaker than IR absorption peaks in the IR range"
13. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
14. ✓ **S01 p.12** (general): "Therefore, Raman spectra (as well as IR absorption spectra) can be used to construct chemometric models-calibration or classification ones."
15. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
16. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
17. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples, such as biological tissue, using specialized probes utilizing high-transmission fiber optics in the Mid-IR region."
18. ✓ **S04 p.3** (general): "These are, respectively, the amide I and II bands, two major absorption peaks of the protein peptide group in the infrared region."
19. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR) by connecting appropriate attachments and probes."
20. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments, as well as in-situ measurements"
21. ✓ **S04 p.4** (general): "the suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
22. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
23. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules"
24. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
25. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
26. ✓ **REF §5** (general): "calibration specific to the matrix"
27. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
28. ✓ **S01 p.18** (general): "having both fiber optic techniques available in a lab rather than relying on one provides the flexibility needed to monitor the entire production chain."
29. ✓ **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
30. ✓ **S01 p.11** (general): "observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
31. ✓ **S04 p.1** (general): "ATR analysis with its penetration depth of a few micrometers acts as the single-cell level"
32. ✓ **S04 p.4** (general): "the suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
33. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
34. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
35. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer."
36. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
37. ✓ **S01 p.18** (general): "The key experimental action is the precise control of the optical pathlength (usually 1 - 10 mm)"
38. ✓ **S01 p.7** (general): "The analysis of such systems may require a combination of two or even more spectral methods."
39. ✓ **S01 p.15** (method gain): "By combining Raman and NIR, these models can predict API potency or coating thickness with higher accuracy and robustness than single-method models."
40. ✓ **S01 p.15** (method gain): "NIR detects hydrogen bonds and asymmetric polar groups, while Raman provides information on the molecular backbone and symmetrical non-polar groups."

## Verification

- Citations verified: 40 of 40 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 4; repair rounds: 1.

*Run D03 · models deepseek/deepseek-v4.1-flash · cost $0.0203*
