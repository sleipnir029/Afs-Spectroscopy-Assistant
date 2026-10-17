# First technical assessment: Glucose and lactate trends in an aqueous bioprocess

**Customer enquiry**

> We run a cell culture process in an aqueous medium. Glucose and lactate are measured from samples, and the delay makes it difficult to see changes promptly. We are exploring an in situ spectroscopy pilot that can be checked against those existing laboratory measurements. The medium and cell population change during the run; we have not yet selected a probe or a calibration strategy.

**Decision status:** Provisional feasibility assessment. A shortlist of single methods can be justified for laboratory testing (Raman and MIR-ATR pass the screening; NIR is conditional on the medium's optical density). No probe, geometry, fiber link, accuracy or calibration strategy can be fixed from the stated facts. The published examples cited below are reasons to test, not evidence that any method works for this process.

## Premise check

- **Supported:** The existing laboratory measurements can serve as a reference for the in situ spectroscopy pilot. A feasibility plan is expected to include independent reference measurements. Whether these particular measurements are accurate, traceable and frequent enough to be that reference is not addressed by the sources. [1: REF §3]
- **Supported:** The in situ spectroscopy pilot can be checked against those existing laboratory measurements. Same check as above: the sources expect a defined reference measurement and a defined comparison in a feasibility plan; they do not confirm that the customer's current method meets that requirement. [2: REF §3]
- **Not covered:** The existing laboratory measurements are adequate to detect the changes promptly. No supplied source addresses the accuracy, precision or timeliness of the customer's laboratory measurements. The enquiry itself says the delay makes it difficult to see changes promptly, so this premise is the opposite of what the customer stated. This is a question to put back to the customer, not an assumption to carry forward. *(no verified source: engineering judgement)*

## Requirements

**Stated by the customer**


**Key unknowns**

- Glucose and lactate concentration ranges over a run, and the required accuracy, precision and time to result
- Optical density / turbidity of the medium and how strongly it changes with the cell population
- Installation point (reactor, loop, pipe), temperature and pressure there, cleaning/sterilisation the probe must survive, and distance from the spectrometer
- Fluorescence background of the medium and cells (decisive for Raman)
- Which exact laboratory method provides the current glucose/lactate values, at what accuracy and frequency
- Achievable length of a mid-IR fiber link for an in-situ installation (no source states one)

## Clarification questions (most decision-relevant first)

Q1. What are the glucose and lactate concentration ranges during a run, and what accuracy, precision and time-to-result do you need? These numbers decide whether NIR or Raman can reach the analytes and they become the go/no-go criteria. *Why it matters:* Method, technique and the whole go/no-go basis depend on this. No source supplies detection limits or accuracy for these analytes. *(affects: method, technique, status)*
Q2. How does the medium's optical density / turbidity behave over the run (for example clear at start, turbid at the end), and how much of the change is caused by the cell population? *Why it matters:* This decides NIR transmission/transflection versus diffuse reflection versus ATR, and whether a UV-ATR type short-path probe is needed instead of transmission. *(affects: technique, probe)*
Q3. Where would the probe be installed (reactor, recirculation loop, pipe), what are the temperature and pressure there, what cleaning/sterilisation must it survive, and how far is the spectrometer from the process point? *Why it matters:* ATR needs tight contact with the sample; installation, fouling and cleaning constraints can rule an immersion crystal in or out, and the distance sets the fiber link, for which no mid-IR length is stated in the supplied material. *(affects: installation, technique)*
Q4. Which laboratory method produces your current glucose and lactate values, how often are samples taken, and what is its accuracy? *Why it matters:* The reference measurement has to be good enough to act as the reference; the enquiry gives no detail on it. *(affects: status, validation)*
Q5. Do the medium components or the cells fluoresce strongly (media, NADH-type cofactors, other fluorophores)? *Why it matters:* Raman bands can be hidden by luminescence; this has to be checked on the real medium before Raman is relied on. *(affects: method)*

## Recommendation

- **R1 · Primary candidate: Raman, raman probe.** Passes the screening. Raman is the single method the supplied sources name for the customer's analytes in a reactor: it is described as giving a molecular fingerprint for direct detection of specific metabolites such as glucose and lactate, and as well suited to aqueous media because water absorbs less than in infrared methods. This is the best-supported single method to test first. *Conditions:* Depends on the real fluorescence background and on the analyte levels; Raman signals are weak. The laser excitation wavelength is a separate choice and is not fixed by the supplied material. [3: S01 p.16] [4: S01 p.16] [5: S01 p.11] [6: S01 p.11]
- **R2 · Primary candidate: MIR, ATR.** Passes the screening. Strong mid-IR absorption makes transmission impractical for a liquid layer, and ATR is the stated route for that; mid-IR is described as highly informative, ATR probes are described for liquids and for in-line, in-process biotechnological environments, and in-line MIR-ATR is shown in a process example. These are reasons to test, not evidence for this medium. *Conditions:* Requires tight contact with the sample and reads only a very thin surface layer, so fouling and surface representativeness are open risks. The usable range is set by the fiber and the ATR crystal, not by the method range. [7: S01 p.5] [8: S01 p.9] [9: S01 p.10] [10: S01 p.10] [11: S02 p.14] [12: S01 p.13] [13: REF §5]
- **R3 · Conditional candidate: NIR, diffuse reflection.** Screening is 'unknown' because the medium's optical regime is not known, so this entry applies only if the medium is opaque/scattering enough that transmission is not usable. NIR is described as the most common online fiber-probe method and as effective for major components like glucose in the millimolar range, but it may lack sensitivity below 0.1 percent. If the medium is transparent and low-OD, the transmission/transflection geometry would be the one to test instead. *Conditions:* Decided by Q2. Requires controlled optical pathlength if transmission is used, and scatter correction if reflection is used. NIR calibrations are matrix-specific. [14: S01 p.10] [15: S01 p.16] [16: S01 p.17] [17: S01 p.18] [18: S01 p.18]
- **R4 · Not recommended: Fluorescence, fluorescence probe.** Fluorescence is a key online method in biotechnology, so a reader would expect it to be considered. It is not recommended for the stated targets: it reports species that fluoresce, most chemicals do not, and no fluorescent species or justified indicator for glucose or lactate has been identified. It is high-sensitivity but low-selectivity and not a direct measurement of every analyte. *Conditions:* Could only become relevant if a defined fluorescent species or a justified indicator for this process is named. [19: S01 p.5] [20: S01 p.12] [21: REF §5]

## Measurement concept

- **Probe and geometry:** Immersion or flow-through probe at the process point, without sampling: MIR-ATR crystal in contact with the liquid; Raman probe (contact or through a window); NIR reflection for scattering media or transmission/transflection for clear media. Which of these is installed depends on Q2 and Q3.
- **Location:** Directly in the process flow or reactor rather than by sampling.
- **Fiber link:** NIR and Raman can use silica fibers (the visible-to-near-IR silica fiber family is shown in the fiber-range figure on S02 p.6); metal-coated silica avoids polymer-jacket fluorescence, which matters for Raman. MIR cannot use silica and needs chalcogenide (CIR) or polycrystalline (PIR) fibers; hollow waveguides couple poorly to FTIR spectrometers. The achievable length of a mid-IR link is not stated in the supplied material and is an open question for AFS. [22: S01 p.3] [23: S02 p.6] [24: S02 p.6] [25: S02 p.7] [26: S02 p.10]

## Spectral range

- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the spectrometer, fiber and probe actually selected. [27: S01 p.10] [28: REF §3]
- **MIR:** Nominal method range 4000-400 cm-1 (2.5-25 µm). In a fiber-probe setup the usable range is set by the fiber and the ATR crystal, not by the method range. [29: S01 p.9] [30: REF §5]
- **Raman:** Raman is reported on the Raman shift axis in cm-1; the laser excitation wavelength is a separate choice and is not fixed by the supplied material (785 nm appears only in a pharmaceutical example). [31: S01 p.11] [32: S01 p.15]

## Risks and uncertainty

- The Raman signal may be swamped by fluorescence from the medium or cells; this can only be judged on the real medium. *(rules: R-RAM-1)* [33: S01 p.11]
- The medium and cell population change during the run, so a calibration built on one process state may not hold across the run or across batches; NIR and Raman calibrations are matrix-specific. *(rules: R-CAL-1)* [34: REF §5] [35: REF §5]
- If the optical density rises strongly during the run, a transmission geometry can saturate and stop measuring; the geometry choice then changes. The pathlength in transmission must be controlled. *(rules: R-GEO-2, R-GEN-3, R-GEN-4)* [36: S01 p.16] [37: S01 p.18]
- Installation and contact: an ATR probe needs tight contact and reads only a surface layer, so fouling, cleaning/sterilisation and sample representativeness are open; the achievable length of a mid-IR fiber link for this installation is not stated anywhere in the supplied material. *(rules: R-MIR-2, R-MIR-3, R-FIB-2)* [38: REF §5] [39: S01 p.13]

## First feasibility experiment

1. **Build a representative sample set from real process states: early, mid and late in the run, covering the observed glucose and lactate range, the cell-density/viability range and any medium changes. Include at least two independent runs or batches so that one can be held out.** Representative coverage before any method is chosen. [40: REF §3]
2. **Measure every sample in the laboratory with each single candidate method first (Raman probe; MIR-ATR; NIR in the geometry that matches the sample's optical density), plus spiked samples to cover the required concentration range, and keep the existing laboratory values alongside as the reference.** Single methods first; no combination before this. [41: S01 p.3]
3. **Compare the single methods against the reference and against each other. Only then test a combination (for example NIR + Raman, or MIR-ATR + Raman) as a hypothesis to be measured against the best single method, with sampling location and timing aligned.** Keep any combination claim as a hypothesis. [42: REF §5] [43: REF §5]
4. **Validate the models on held-out runs or batches, not only on further samples from the same run, and check whether the medium and cell changes during a run break the calibration.** Independent validation on limited data. [44: S03 p.14]
5. **Fix the go/no-go basis before starting. The numerical criteria (accuracy, precision, time to result, allowed drift over a run) must come from the customer; they are not in the supplied material, so until they are given the pilot has no defined decision basis.** Go/no-go criteria come from the customer. [45: REF §3]

**Reference measurements:** The existing laboratory glucose and lactate values, provided their accuracy and sampling frequency are adequate (Q4).

**Decision basis:** Not defined yet: no detection limit, accuracy, precision or response time for glucose or lactate appears in the supplied sources or in the enquiry. These numbers must be set by the customer before the experiment can pass or fail.

## Assumptions

- The customer's existing laboratory measurements are accurate and frequent enough to act as the reference; this is assumed, not confirmed.
- The process allows a probe to be brought into contact with, or immersed in, the medium (contact, sterilisation and cleaning constraints are unknown).
- Glucose and lactate sit in a concentration range where at least one of the shortlisted methods has a chance; no source states a detection limit for either analyte in this medium.

## Not covered by the supplied sources

- Detection limits, accuracy, precision or response time for glucose or lactate in a cell-culture medium: no supplied source states these for any configuration.
- An achievable length for a mid-IR fiber link in an in-situ installation: no supplied source states one; the mid-IR fiber and hollow-waveguide examples shown are laboratory lengths only.

## Evidence (verified quotes)

1. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
2. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
3. ✓ **S01 p.16** (application precedent): "direct detection of specific metabolites like glucose, acetate, or lactate."
4. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
5. ✓ **S01 p.11** (general): "signals, which are several orders of magnitude weaker than IR absorption peaks"
6. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
7. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
8. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
9. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
10. ✓ **S01 p.10** (general): "Probe-based analysis is gaining widespread use in online analysis, such as in-line, in-process (chemical, biotechnological, natural) environments"
11. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
12. ✓ **S01 p.13** (general): "typically at a depth of few microns"
13. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
14. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
15. ✓ **S01 p.16** (general): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
16. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
17. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
18. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
19. ✓ **S01 p.5** (general): "However, most chemicals do not exhibit this property."
20. ✓ **S01 p.12** (general): "Recently, it has become a key method for online analysis of biotechnological processes."
21. ✓ **REF §5** (general): "High sensitivity, low selectivity; not a direct measurement of every analyte."
22. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
23. ✓ **S02 p.6** (general): "1100 nm Chalcogenide As-S IR Fibers 6500 nm"
24. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
25. ✓ **S02 p.7** (general): "Free of Polymer jacket fluorescence for Raman and Fluo- Spectroscopy"
26. ✓ **S02 p.10** (general): "too low NA>0.1 - which results in very poor coupling efficiency with FTIR-spectrometers"
27. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations of molecules and atomic groups"
28. ✓ **REF §3** (general): "A nominal method range is not the range of a specific instrument, fiber or probe."
29. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
30. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
31. ✓ **S01 p.11** (general): "The Raman shift is used as the horizontal (spectral) axis in Raman spectroscopy"
32. ✓ **S01 p.15** (application precedent): "Raman spectrometer and Raman fiber probe for contact measurements with 785 nm excitation wavelength"
33. ✓ **S01 p.11** (general): "superposition of luminescence (fluorescence), which has a significantly higher intensity."
34. ✓ **REF §5** (general): "Weak signal, fluorescence background; calibration specific to the matrix."
35. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
36. ✓ **S01 p.16** (general): "transmission setup becomes saturated because the light cannot penetrate the bulk of the sample."
37. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
38. ✓ **REF §5** (general): "Liquids, pastes and soft solids in contact with the ATR crystal."
39. ✓ **S01 p.13** (general): "typically at a depth of few microns"
40. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
41. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
42. ✓ **REF §5** (general): "compare with the best single method."
43. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."
44. ✓ **S03 p.14** (general): "A thorough validation, including full, segmented and random-subset CVs, as well as randomization tests, are recommended in any cases for which important conclusions depend on calibration or discrimination models built on limited experimental material."
45. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 45 of 45 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 1; repair rounds: 1.

*Run D04-20261017T085117Z · models deepseek/deepseek-v4.1-flash · cost $0.0359*
