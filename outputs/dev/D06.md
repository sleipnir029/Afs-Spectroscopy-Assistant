# First technical assessment: Water content in a petroleum stream

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Provisional feasibility assessment. A shortlist can be justified from the supplied material: a laboratory example shows ATR probes used for measurement of water content in petroleum, and fiber probes are described as compatible with remote, in-line measurement. The choice between ATR, transmission and reflection, the fiber link length and any performance figure depend on facts the customer has not yet given, so this is a provisional shortlist with stated assumptions, not an equipment selection.

## Premise check

- **Supported:** A fiber based measurement closer to the process will notice changes sooner. The sources describe fiber probes in reactors and production lines with results in near real time. They do not quantify how much sooner for this stream, and no response time is given anywhere in the material. [1: S01 p.2]
- **Supported:** The analyzer can be outside the process area. Fiber probes are described as allowing analysis at a distance from the spectrometer. Caveat: no source states an achievable length for a mid-IR fiber link; the long cable figures in the material apply only to low-OH silica cables (NIR/Vis), and the mid-IR fiber and hollow-waveguide examples shown are laboratory pieces. The achievable distance for the intended configuration is an open question. [2: S01 p.10] [3: S02 p.7]
- **Supported:** A first comparison experiment should establish what is needed before selecting equipment. The material describes testing several methods on samples of incompletely known composition in order to select the most suitable method or combination, and an AFS pathway that starts with multi-method lab trials before choosing a solution. [4: S01 p.3] [5: S02 p.20]

## Requirements

**Stated by the customer**

- Water determination in a petroleum stream, currently by laboratory analysis of sent samples.
- Measurement closer to the process, with the analyzer outside the process area.
- Earlier notice of changes than the current laboratory route.
- Before equipment selection: what to clarify, and what a first comparison experiment should establish.

**Key unknowns**

- Water concentration range at the measurement point and the required detection limit and accuracy.
- Physical state and optical behaviour of the stream there: clear single-phase liquid, turbid, emulsion with free water, or gas.
- Form of the water: dissolved, emulsified or free.
- Temperature, pressure and flow at the measurement point, and the distance from that point to the intended analyzer location.
- Reference laboratory method used today and its repeatability on this stream.
- Fouling, coating and chemical compatibility of probe/crystal materials with this stream, and the cleaning that is possible.

## Clarification questions (most decision-relevant first)

Q1. What water concentration range must be measured at the measurement point, and what detection limit and accuracy does the process need? *Why it matters:* Decides whether a thin-layer ATR measurement or an NIR path-length measurement can reach the target at all. *(affects: method, technique, status)*
Q2. What is the stream at the proposed measurement point - a clear single-phase liquid, a turbid liquid or emulsion with free water, or a gas - and how much does this vary? *Why it matters:* Decides ATR contact versus transmission/transflection versus diffuse reflection, and whether a combination is worth testing later. *(affects: technique, installation, status)*
Q3. What are the temperature, pressure and flow at the measurement point, and what distance must the fiber link span from there to the analyzer location? *Why it matters:* Decides the fiber family and probe construction; no achievable mid-IR link length is stated in the material. *(affects: method, installation)*
Q4. Which laboratory method is used today for water determination, and what repeatability does it give on this stream? *Why it matters:* It is the independent reference for the comparison and for the go/no-go decision. *(affects: status)*
Q5. Must the new measurement replace the laboratory result, or is an early-warning trend sufficient? *Why it matters:* Decides whether a quantitative calibration with defined accuracy is needed or a trend model is acceptable. *(affects: method, status)*
Q6. Does the stream foul, coat or chemically attack a crystal or window, and what cleaning or maintenance is possible at the measurement point? *Why it matters:* ATR reads only the immediate surface layer, so contact, fouling and compatibility decide the technique and the installation. *(affects: technique, installation)*

## Recommendation

- **R1 · Primary candidate: MIR, ATR.** MIR is described as one of the most informative methods of chemical analysis, and strong mid-IR absorption (including by water) is handled by the very thin sampled layer of an ATR measurement. A supplied laboratory example shows ATR probes used for measurement of water content in petroleum. That example is a reason to test MIR-ATR on this stream, not proof that it works here. *Conditions:* Applies only if the stream at the measurement point is a liquid, paste or soft solid that can make tight contact with the ATR crystal, and if the water content lies inside the working range of the selected crystal and spectrometer (both unknown). [6: S02 p.13] [7: S01 p.9] [8: S01 p.5] [9: S04 p.4]
- **R2 · Comparison candidate: NIR, transmission transflection.** NIR is described as the most common online method performed with fiber probes, and low-OH silica cables are stated at 100-300 m, which fits an analyzer placed away from the process. Water absorbs in the NIR region, but the bands are broad and overlapping, so quantitative use needs a chemometric calibration. This is a second single-method option to compare with MIR-ATR, not a substitute decision. *Conditions:* Applies only if the stream is transparent or semi-transparent enough for transmission/transflection and the optical path length can be controlled; if the stream is too thick or opaque, the transmission signal is lost and a reflection geometry has to be considered instead. [10: S01 p.18] [11: S01 p.18] [12: S01 p.10] [13: S02 p.7]
- **R3 · Conditional candidate: NIR, diffuse reflection.** Conditional alternative to R2, to be tested only if the stream turns out opaque, highly concentrated or strongly scattering, where a transmission path would lose the signal. Reflection readings are sensitive to surface characteristics and particle/globule size, so scatter correction and a matrix-specific calibration are required. *Conditions:* Applies only if Q2 shows the stream is not suitable for transmission/transflection at a workable path length. [14: S01 p.17] [15: S01 p.17]

## Measurement concept

- **Probe and geometry:** Lead option: ATR fiber probe in contact with the stream. Alternative: NIR transmission/transflection probe across a defined path, or NIR reflection probe if the stream is opaque.
- **Location:** Probe at the process measurement point; analyzer and spectrometers located outside the process area on a fiber link.
- **Fiber link:** Mid-IR light needs chalcogenide (CIR) or polycrystalline (PIR) fibers or a hollow waveguide; NIR can use Vis-NIR silica fibers. No achievable mid-IR link length is stated in the material, so the distance must be confirmed with AFS. [16: S02 p.6] [17: S02 p.6] [18: REF §5]

## Spectral range

- **MIR:** Nominal method range 4000-400 cm-1. The usable range depends on the instrument, fiber and probe actually selected, and on the crystal used for ATR; it is not fixed by the method name. [19: S01 p.9]
- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [20: S01 p.10]

## Risks and uncertainty

- Contact and surface representativeness. An ATR measurement reads only a very thin surface layer, so deposits, an emulsion film or free water at the crystal can dominate the reading, and ATR needs tight contact with a suitable liquid or soft solid. If the stream is not such a medium at the measurement point, the MIR-ATR lead is wrong. *(rules: R-MIR-2, R-MIR-3)* [21: REF §5] [22: S01 p.13] [23: REF §5]
- Fiber link length. Long cables (100-300 m) are stated only for low-OH silica fibers; the mid-IR fiber and hollow-waveguide pieces shown are laboratory examples, and no achievable mid-IR link length is given. If the distance from the process point to the analyzer location is large, the mid-IR option may not be feasible as assumed and the analyzer position or method may have to change. *(rules: R-FIB-2)* [24: S02 p.7] [25: S02 p.9]
- Water level versus sensitivity. If the water content is very low, the required detection limit may be out of reach for the selected configuration; the material notes that NIR may lack sensitivity for trace compounds below 0.1 percent, but that statement comes from a bioprocess example, not from a petroleum measurement, and no detection limit for water in petroleum is supplied. If free water or a high water content is present, a short ATR path may saturate or may not be representative of the bulk stream. *(rules: R-NIR-4, R-GEN-3)* [26: S01 p.16]
- Matrix-specific calibration. Calibrations are specific to the matrix; if the stream grade, additives or water form change, a model built on one sample set must be re-validated on the new material. *(rules: R-CAL-1)* [27: REF §5]

## First feasibility experiment

1. **1** Build a representative sample set with independent reference values. [28: REF §3]
2. **2** Measure the same samples by MIR-ATR in the laboratory (single method first) and compare each result with the reference water value; check whether the water signal is measurable across the required range. *(no verified source: engineering judgement)*
3. **3** Measure the same samples by NIR transmission/transflection, and by NIR diffuse reflection if the samples are opaque; compare each single method with the best single method from step 2. [29: REF §5]
4. **4** Run the chosen single method at the process point with the analyzer at the intended remote location: check signal stability, repeatability and fouling behaviour, then validate the model on held-out runs or batches that were not used in the calibration. *(no verified source: engineering judgement)*
5. **5** Go/no-go against the customer's own numerical criteria (required accuracy, detection limit and response time), set by the customer before the trial; report any figure that cannot be met. *(no verified source: engineering judgement)*

**Reference measurements:** The current laboratory water determination, applied to the same samples, is the independent reference. Its method and repeatability are still to be confirmed (Q4).

**Decision basis:** Numeric acceptance limits must come from the customer; none are given in the enquiry and none may be assumed from the sources.

## Assumptions

- The stream at the measurement point is a liquid that can be presented to a probe.
- The analyzer can be placed at some distance from the process point on a fiber link; the achievable distance is not yet known.
- The water level of interest lies inside the working range of the configuration eventually chosen; no range has been stated.
- The current laboratory method is accurate enough to act as the reference.

## Not covered by the supplied sources

- No accuracy, detection limit or response time for water determination in a petroleum stream appears in the supplied material; the only related passage is a laboratory ATR spectra example.
- No achievable fiber or cable length for a mid-IR link between a process point and a remotely placed analyzer is stated; the long-cable figures in the material apply only to low-OH silica fibers, and the mid-IR fiber and hollow-waveguide pieces shown are laboratory examples.
- No source covers this customer's stream composition, water range or process conditions.

## Evidence (verified quotes)

1. ✓ **S01 p.2** (general): "enabling on-site online analysis and obtaining results in near real time"
2. ✓ **S01 p.10** (general): "allow analysis at a significant distance from the spectrometer, without the need for sampling"
3. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
4. ✓ **S01 p.3** (general): "samples of incompletely known composition, in order to select the most suitable method or combination of methods."
5. ✓ **S02 p.20** (general): "1. Multi-Method Lab Trials AFS tests your process using all key fiber optic spectroscopy methods."
6. ✓ **S02 p.13** (application precedent): "measurement of water content in petroleum"
7. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
8. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
9. ✓ **S04 p.4** (general): "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."
10. ✓ **S01 p.18** (general): "Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."
11. ✓ **S01 p.18** (general): "precise control of the optical pathlength (usually 1 - 10 mm)"
12. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
13. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
14. ✓ **S01 p.17** (general): "NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
15. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
16. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 µm"
17. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
18. ✓ **REF §5** (general): "actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
19. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
20. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
21. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
22. ✓ **S01 p.13** (general): "typically at a depth of few microns"
23. ✓ **REF §5** (general): "Liquids, pastes and soft solids in contact with the ATR crystal."
24. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
25. ✓ (precedent only) **S02 p.9** (performance figure): "HWG-750-2m PIR 600/700 -2m"
26. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
27. ✓ **REF §5** (general): "calibration specific to the matrix."
28. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
29. ✓ **REF §5** (general): "compare with the best single method."

## Verification

- Citations verified: 29 of 29 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 1; repair rounds: 1.

*Run D06-20261017T094535Z · models deepseek/deepseek-v4.1-flash · cost $0.0172*
