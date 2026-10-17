# First technical assessment: A clear whey stream before concentration

**Customer enquiry**

> Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the reference. The stream can become more turbid under some operating conditions. We need a first measurement concept that handles this change rather than assuming the liquid always remains clear.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified: the sources name whey as a transmission liquid and show NIR with PLS regression for fat and protein in dairy, so NIR transmission/transflection and NIR diffuse reflection are worth testing, with a conditional MIR-ATR route. The request for one concept that covers both the clear and the turbid state is not established by the sources (the closest statement is the dairy transflection example, 'in some cases', for low- and high-fat milk) and is carried here as a hypothesis, not as an approved configuration. Assumptions: this whey behaves like the dairy liquids in the sources; the protein to be tracked is a major component, not a trace one; the stream stays suitable for the chosen probe.

## Premise check

- **Supported:** Spectroscopy can track protein concentration in this whey stream as the stream changes. Supported as an application precedent only. The sources name whey as a transmission liquid and show NIR with PLS regression quantifying fat and protein in dairy. A published or shown example is a reason to test the method on this stream, not proof that it works here, and the source example does not cover a stream whose turbidity changes. [1: S01 p.18] [2: S01 p.17]
- **Not covered:** One measurement concept will cope with the stream changing from clear to turbid, without assuming it stays clear. No supplied source describes a single probe or geometry for a stream that moves between a clear and a turbid state. The closest statement is the dairy transflection example, and it is limited to low- and high-fat milk products and says 'in some cases'; it is a hypothesis to test on this stream, not support for the premise. [3: S01 p.18]
- **Not covered:** Laboratory results are an adequate reference for the spectroscopic measurement. No source states what makes a laboratory reference adequate for this application. The guidance only requires independent reference measurements in a feasibility plan; the reference method, its uncertainty, the sampling procedure and the turnaround time are open questions for the customer. [4: REF §3]

## Requirements

**Stated by the customer**

- The request is for a first measurement concept, not for a released in-line configuration.
- No method or fiber family is proposed by the customer, so nothing is listed as not_recommended.
- The customer's reference is laboratory protein results; no accuracy target, detection limit or response time was given.

**Key unknowns**

- Protein concentration range and which fraction must be tracked (total protein, whey protein, a specific component).
- Degree, cause and dynamics of the turbidity change (range of turbidity or optical density, how fast, how often).
- Available path length and line geometry at the measurement point (pipe size, insertion or bypass loop).
- Reference laboratory method for protein, its uncertainty, sampling procedure and turnaround time.
- Temperature, pressure and cleaning regime (e.g. CIP) at the measurement point, and expected fouling.
- Required accuracy, precision and response time for tracking the protein change.

## Clarification questions (most decision-relevant first)

Q1. What is the range of turbidity (or optical density) at the measurement point, how fast and how often does it change, and what causes it? *Why it matters:* This decides the measurement geometry (transmission/transflection versus reflection) and whether one probe can cover both states. *(affects: method, technique, status)*
Q2. What protein range must be tracked, which fraction is meant, and what accuracy, precision and response time are required? *Why it matters:* This decides whether NIR is sensitive enough for the target, or whether a MIR-ATR fallback and/or a method combination is needed. *(affects: method, technique, status)*
Q3. What path length and line geometry are available at the measurement point, and what are the temperature, pressure and cleaning (CIP) conditions? *Why it matters:* This decides the probe type and installation, and the achievable optical path length. *(affects: installation)*
Q4. Which laboratory method will be the reference for protein, with what uncertainty and turnaround, and can reference samples be taken at the same point and at the same time as the spectra? *Why it matters:* The feasibility comparison is only as good as the reference; the customer's statement that laboratory results are an adequate reference is not covered by the sources. *(affects: status, installation)*
Q5. How far from the measurement point will the instrument sit, and what is the environment there (vibration, dust, washdown)? *Why it matters:* This decides the fiber family and the link length; the sources state long cables only for low-OH silica fibers, and no source states an achievable length for a mid-IR link. *(affects: installation)*

## Recommendation

- **REC1 · Primary candidate: NIR, transmission transflection.** Whey is exactly the type of transparent or semi-transparent liquid the source names for NIR transmission, and NIR is the dairy method shown for quantifying fat and protein. Transflection is the geometry that could span the clear and the turbid state; the source presents it as 'in some cases' a combined solution for low- and high-fat milk, so on this stream it is a hypothesis to test. *Conditions:* Applies if the stream is at least semi-transparent at the measurement point and a fixed, controlled path length can be provided. [5: S01 p.18] [6: S01 p.17] [7: S01 p.18]
- **REC2 · Comparison candidate: NIR, diffuse reflection.** Covers the other end of the range: reflection is the source's technique for opaque or highly concentrated dairy liquids, so it is the natural comparison for the turbid state. It can be less representative for clear liquids and is sensitive to surface and particle size, so it is tested against REC1 rather than assumed better. *Conditions:* Test on the same samples and the same measurement point as REC1; most useful for the turbid operating states. [8: S01 p.17] [9: S01 p.18] [10: S01 p.17]
- **REC3 · Conditional candidate: MIR, ATR.** A fallback if the NIR tests cannot separate the protein change from the scattering change, or if the protein fraction of interest is too small for NIR. MIR-ATR probes analyse liquids in contact with a crystal and the MIR region carries the protein amide I and II bands; ATR samples only a few micrometres, which limits how much bulk turbidity contributes. Water absorbs strongly in the MIR, so the usable window is narrow and this route is not the first choice. *Conditions:* Applies only if the NIR trials show insufficient selectivity for the protein fraction, or if the target fraction is present at a level NIR cannot follow. [11: S04 p.3] [12: S01 p.5] [13: S01 p.10] [14: S01 p.13]

## Measurement concept

- **Probe and geometry:** One insertion or flow-through probe at the measurement point before the concentration stage, used in a transmission or transflection geometry first; a diffuse-reflection probe on the same point as the comparison for the turbid states. A MIR-ATR probe in contact with the stream is the conditional fallback. Contact, fouling and crystal cleaning are risks for the ATR option.
- **Location:** At the stated measurement point before the concentration stage; sampling location and timing must be the same for every method tested.
- **Fiber link:** An NIR link can be all-silica; the source states 100-300 m low-OH silica cables for remote industrial process control, so the instrument can sit away from the line. A mid-IR link needs chalcogenide or polycrystalline infrared fibers because silica fibers end near 2.4 µm. No source states an achievable length for a mid-IR link, so that length is an open question for AFS. [15: S02 p.7] [16: S02 p.6] [17: S02 p.6]

## Spectral range

- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected, and the water bands of the stream will cut into it. [18: S01 p.10] [19: REF §5]
- **MIR:** Nominal MIR range 4000-400 cm-1. The usable window in an aqueous stream is much narrower than the nominal range because water absorbs strongly. [20: S01 p.9] [21: REF §3]

## Risks and uncertainty

- Turbidity may be read as protein change. Reflection signals depend on surface and particle size, and the calibration is specific to the matrix, so a model built on clear samples may not hold when the stream turns turbid. *(rules: R-GEO-6, R-CAL-1)* [22: S01 p.17] [23: REF §5]
- The transmission option can lose signal or saturate when the stream becomes turbid, and one fixed path length may not serve both the clear and the turbid state. *(rules: R-GEO-2, R-GEN-4)* [24: S01 p.18] [25: S01 p.18]
- NIR may not be sensitive enough for the protein fraction of interest if it is a minor component. No source gives a detection limit for protein in whey. *(rules: R-NIR-4)* [26: S01 p.16]
- The customer's expectation that one concept covers both states may not hold. The source's combined transflection statement is limited to low- and high-fat milk products and says 'in some cases'; if it does not transfer to this stream, two probes (transmission and reflection) may be needed. *(rules: R-GEO-5, R-CMB-1)* [27: S01 p.18]

## First feasibility experiment

1. **Collect whey samples at the measurement point across the expected chemical and physical variation: the full protein range and the clear-to-turbid states, including the transition, over several runs or batches. Hold out complete runs for validation.** Representative samples and held-out runs. [28: REF §3]
2. **Measure protein on the same samples with the plant's laboratory method, with the sampling procedure, uncertainty and turnaround agreed in advance. Take the reference sample at the same point and the same time as the spectrum.** Independent reference measurement. [29: REF §3]
3. **Fix and record the transmission/transflection path length, then measure every sample with NIR transmission/transflection first and NIR diffuse reflection second (single methods before any combination). Record the sample's turbidity or optical density as a separate physical variable.** Single methods first; the physical variable is captured separately. [30: S01 p.18]
4. **Build a chemometric (e.g. PLS) model for protein with scatter correction (MSC or SNV) as in the dairy example, and validate it on the held-out runs, including turbid samples that were not used for calibration. Check whether the model tracks protein rather than turbidity.** Validation on held-out runs and a check against the confound. [31: S01 p.17]
5. **Go/no-go: compare predicted against reference protein separately for the clear and the turbid state, using accuracy, precision and response-time limits to be set by the customer. Test the MIR-ATR conditional, and only afterwards any method combination, only if the single-method tests fail those limits.** Go/no-go basis; combinations after single methods. [32: REF §3]

**Reference measurements:** Plant laboratory protein results, taken at the same point and time as the spectra, with the method, uncertainty and turnaround agreed before the trial.

**Decision basis:** Customer-set numerical limits on accuracy, precision and response time, assessed separately for the clear and the turbid state.

## Assumptions

- This whey behaves like the dairy liquids described in the sources (skim milk, whey, permeate).
- The protein to be tracked is a major component of the stream, not a trace component.
- The stream remains suitable for the chosen probe (contact for ATR, controlled path length for transmission).
- Reference laboratory results can be produced for the same point and time as the spectra.

## Not covered by the supplied sources

- No supplied source states an achievable accuracy, detection limit or response time for protein in whey.
- No supplied source gives a calibration or model for a whey stream whose turbidity changes, or covers cleaning (CIP) and fouling behaviour of an in-line probe on this stream.

## Evidence (verified quotes)

1. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
2. ✓ **S01 p.17** (application precedent): "using Partial Least Squares (PLS) regression to quantify fat and protein"
3. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
4. ✓ **REF §3** (general): "independent reference measurements"
5. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
6. ✓ **S01 p.17** (application precedent): "using Partial Least Squares (PLS) regression to quantify fat and protein"
7. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
8. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
9. ✓ **S01 p.18** (general): "reflection can work well in highly scattering environments but can be less representative for clear liquids."
10. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
11. ✓ **S04 p.3** (general): "the amide I and II bands, two major absorption peaks of the protein peptide group in the infrared region"
12. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
13. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
14. ✓ **S01 p.13** (general): "typically at a depth of few microns"
15. ✓ **S02 p.7** (general): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
16. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
17. ✓ **S02 p.6** (general): "1100 nm Chalcogenide As-S IR Fibers 6500 nm"
18. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
19. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
20. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
21. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
22. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
23. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
24. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
25. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
26. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
27. ✓ **S01 p.18** (general): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
28. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements"
29. ✓ **REF §3** (general): "independent reference measurements, what is compared"
30. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
31. ✓ **S01 p.17** (application precedent): "applying Multiplicative Scatter Correction (MSC) or Standard Normal Variate (SNV) transformations to remove physical interference caused by the scattering nature of the milk particles"
32. ✓ **REF §3** (general): "the basis for the go / no-go decision."

## Verification

- Citations verified: 32 of 32 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 0; repair rounds: 0.

*Run D03-20261017T093749Z · models deepseek/deepseek-v4.1-flash · cost $0.0139*
