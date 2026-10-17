# First technical assessment: Water content in a petroleum stream

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Provisional feasibility assessment. A shortlist for a first laboratory comparison can be justified, but the physical/optical state of the stream at the measurement point, the water level and the required accuracy are not known. The method choice therefore stays conditional and the decisive questions are asked below.

## Premise check

- **Not covered:** A fiber-based measurement closer to the process can be used for this petroleum stream.. No supplied source addresses this customer's stream. The closest material is a laboratory application of ATR probes to water content in petroleum and the general statement that ATR fiber probes allow in-line, in-process analysis of liquids. A laboratory example is a reason to test, not proof for this stream. [1: S02 p.13] [2: S01 p.10]
- **Supported:** A fiber-based measurement closer to the process will make changes noticeable sooner.. Supported for online/in-process analysis in general: it removes the sampling and transport step that a send-to-laboratory workflow contains. The actual response time of any configuration is not stated in the sources and must be set by the customer. [3: S01 p.3]
- **Supported:** The analyzer can remain outside the process area while measuring the stream.. Fiber probes are explicitly described as letting the spectrometer sit away from the process point. How far the analyzer can be placed depends on the fiber family; for a mid-IR link no achievable length is stated in the sources. [4: S01 p.10] [5: S01 p.15]
- **Supported:** A first comparison experiment is the right next step before selecting equipment.. The sources describe multi-method trials on the customer process as the first step, and testing several optical approaches is described as the way to select the most suitable method or combination when the sample composition is not fully known. [6: S02 p.20] [7: S01 p.3]

## Requirements

**Stated by the customer**

- The customer asks what to clarify before selecting equipment and what a first comparison experiment should establish. No approval, proof of readiness or exact configuration is given or implied.

**Key unknowns**

- Physical state and optical behaviour of the stream at the measurement point (single-phase liquid, emulsion with dispersed water, wet gas, turbid, opaque).
- Water concentration range and required detection limit / accuracy / response time.
- Petroleum matrix and its spectral background, including fluorescent components.
- Distance from measurement point to analyzer, area classification, ambient conditions.
- Process temperature, pressure, flow and deposit/fouling tendency.
- Reference laboratory water method and whether paired samples can be taken at the probe location.

## Clarification questions (most decision-relevant first)

Q1. What is the physical state and optical behaviour of the stream at the intended measurement point: single-phase clear liquid, liquid with dispersed/emulsified water, wet gas, or slurry — and will it wet a probe surface? *Why it matters:* This decides ATR (needs tight contact with a liquid, paste or soft solid) versus a transmission/transflection or reflection geometry, and therefore the whole shortlist. It is the single most decisive question. *(affects: method, technique, installation)*
Q2. What water concentration range must be covered, what detection limit and accuracy are required, and what is your current laboratory water method? *Why it matters:* It sets whether a mid-IR method is needed or a NIR method is sufficient, and it provides the numbers for the go/no-go basis of the first experiment (which must come from the customer, not from the sources). *(affects: method, technique, go_no_go)*
Q3. What is the distance from the intended measurement point to the analyzer location, and what are the area classification and ambient conditions there? *Why it matters:* Fiber family follows from the method, but no source states an achievable length for a mid-IR fiber link. A long mid-IR run is an open engineering question for AFS, not a value to assume. *(affects: installation, method, status)*
Q4. What are the process temperature, pressure and flow at the measurement point, and is there any tendency to deposit wax, asphaltenes or other films on a window or crystal? *Why it matters:* ATR probes only a surface layer, so a deposit biases the reading; contact, probe compatibility and cleaning strategy depend on these answers. *(affects: technique, installation)*
Q5. Can paired samples be drawn at the probe location and measured with your existing laboratory method, blind to the spectral result, and how are they currently handled and stored? *Why it matters:* An independent reference measurement is required for a meaningful comparison; without it the first experiment cannot be evaluated. *(affects: feasibility_experiment, status)*
Q6. Does the stream contain fluorescent components (for example aromatics), and can you say roughly how strongly it absorbs in the visible? *Why it matters:* This decides whether the conditional Raman option is worth including at all, since a strong fluorescence background can swamp the weak Raman signal. *(affects: method, status)*

## Recommendation

- **R1 · Primary candidate: MIR + MIR + NIR (combination: a hypothesis to test), ATR.** The only supplied application note that directly names water in petroleum uses ATR probes, and mid-IR is described as highly informative and highly sensitive because of high extinction coefficients. ATR fiber probes are described as usable for in-line, in-process analysis of liquids. The combination of MIR-ATR with NIR is put forward only as a hypothesis, to be compared against the best single method, because a combined gain must be tested and is not established for this stream. *Conditions:* Applies only if the stream at the measurement point is a liquid or a soft/pumpable fluid that wets the ATR crystal, and if a workable mid-IR fiber link between probe and analyzer can be provided. If the stream is a dry gas or a non-wetting medium, this option falls away. [8: S02 p.13] [9: S01 p.9] [10: S01 p.9] [11: S01 p.10] [12: S02 p.8] [13: S01 p.7]
- **R2 · Comparison candidate: NIR, transmission transflection.** NIR is the most common online fiber-probe method and suits remote measurement with standard optics. Transmission/transflection is the preferred geometry for transparent or semi-transparent liquids and gives a representative volume signal. It is included as a comparison against MIR-ATR, because a mid-IR method is more selective for water while NIR may be simpler to install. *Conditions:* Applies if the stream is transparent or semi-transparent and a short, controlled optical pathlength can be provided. If the stream is opaque, scattering or highly absorbing, a diffuse-reflection geometry would be the alternative to test instead. Whether NIR can reach the required low water levels is a question for the trial, not an assumption. [14: S01 p.10] [15: S01 p.18] [16: S01 p.18] [17: S01 p.16]
- **R3 · Conditional candidate: Raman, raman probe.** Raman tolerates water better than infrared methods, which is relevant for a water-in-hydrocarbon target, but the Raman signal is weak and can be swamped by fluorescence. This option is listed as conditional on the customer's answer about fluorescent components and on trial spectra showing a usable signal. *Conditions:* Applies only if the stream shows a usable Raman signal above its fluorescence background, and only if a laser excitation wavelength appropriate to the stream is chosen. Raman shift (cm-1) and the excitation wavelength must be reported separately. [18: S01 p.16] [19: S01 p.11]

## Measurement concept

- **Probe and geometry:** High level only, pending the answers above. If the stream is a wetting liquid: an immersion ATR probe (zirconia or diamond crystal in a chemically compatible shaft) for mid-IR, and/or a transmission or transflection probe for NIR. If the stream is opaque or scattering: a diffuse-reflection probe. No probe or crystal material is selected at this stage.
- **Location:** At or close to the process line, with the spectrometers in the analyzer area outside the process area, connected by fiber. The achievable distance depends on the fiber family and is an open question for a mid-IR link.
- **Fiber link:** Silica fibers cover the visible and near-infrared (the fiber figure lists standard VIS-NIR silica fibers). A mid-IR link requires chalcogenide (CIR), polycrystalline (PIR) fibers or hollow waveguides; the fiber figure lists polycrystalline infrared fibers among the mid-IR options, and the usable range depends on the fiber actually selected. Long cables (100-300 m) are stated only for low-OH silica fibers; no achievable length is stated for a mid-IR link. [20: S02 p.6] [21: S02 p.6] [22: S02 p.7]

## Spectral range

- **MIR:** Nominal mid-IR range 4000-400 cm-1. The usable range depends on the instrument, the fiber and the probe actually selected; no instrument or probe is chosen yet. [23: S01 p.9]
- **NIR:** Nominal NIR range 780-2500 nm. The usable range depends on the instrument, the fiber and the probe actually selected. [24: S01 p.10]
- **Raman:** Raman is reported as a shift in cm-1; the laser excitation wavelength is a separate parameter and is not selected yet. [25: S01 p.11]

## Risks and uncertainty

- The mid-IR water-in-petroleum precedent is a laboratory application note, not evidence that the method works in-line on this stream. *(rules: R-EVI-1, R-EVI-2)* [26: REF §3]
- ATR analyses only a very thin surface layer, so a wax, asphaltene or other film on the crystal can bias the reading and make the measurement unrepresentative. *(rules: R-MIR-3)* [27: S01 p.13]
- No source states an achievable length for a mid-IR fiber link. If the analyzer must be far from the process point, the mid-IR option may not be installable as assumed; this must be confirmed with AFS. *(rules: R-FIB-2, R-FIB-1)* [28: S02 p.7]
- Raman: the weak Raman signal can be overwhelmed by fluorescence from organic components, so the Raman option may not survive a trial on the real stream. *(rules: R-RAM-1)* [29: S01 p.11]
- NIR: bands are broad and overlapping, so quantitative use needs a chemometric calibration, and sensitivity for low water levels is uncertain; in IR methods water absorbs strongly, so a NIR transmission path must be short and controlled. *(rules: R-NIR-2, R-NIR-4, R-GEN-3, R-GEN-4)* [30: S01 p.10] [31: S01 p.16]
- Calibration is specific to the matrix. A change of crude, feed or additive package invalidates the model and requires re-validation on the new material. *(rules: R-CAL-1)* [32: REF §5]
- Water is present in the hydrocarbon in more than one form (dissolved, dispersed droplets, free water). The physical form changes the optical signal, and the sources do not cover this speciation for petroleum. *(rules: R-GEN-5)* [33: S01 p.7]
- The combination MIR-ATR + NIR is a hypothesis only. A combined gain must be demonstrated against the best single method and requires the two measurements to be aligned in location and time. *(rules: R-CMB-1, R-CMB-2, R-CMB-3)* [34: S01 p.8]

## First feasibility experiment

1. **1. Sample set** Cover the expected chemical and physical variation, not a single convenient sample. [35: REF §3]
2. **2. Reference measurements** Measure every sample with the customer's existing laboratory water determination method, on split samples, blind to the spectral result. Without this the comparison cannot be evaluated. [36: REF §3]
3. **3. Single methods first** Acquire spectra with each candidate method separately (MIR-ATR, NIR, Raman) on the same sample set, using the same measurement point and conditions. Only after single-method results are in hand, test the MIR-ATR + NIR combination against the best single method. [37: S02 p.20]
4. **4. Validation** Split the data by run or batch, not by spectrum, and validate the model on held-out runs. Repeated measurements in the same position must be kept together in the same split. [38: REF §3]
5. **5. Go / no-go basis** Numerical acceptance criteria (required detection limit, accuracy, precision, response time) must come from the customer. They are not in the sources and are not set here. The go/no-go is decided by whether the best single method, and then the combination, meets those numbers on held-out runs. [39: REF §3]

**Reference measurements:** The customer's own laboratory water determination on split samples, blind to the spectral result.

**Decision basis:** Customer-defined numerical criteria (unknown at this time). No accuracy, detection limit or response time is claimed or assumed here.

## Assumptions

- The stream at the measurement point can be presented to a probe (a bypass, a window or an immersion position exists or can be created).
- A liquid or soft/pumpable medium is present at the measurement point; this is assumed, not confirmed.
- The analyzer can be placed outside the process area with a fiber link of a length that AFS confirms to be feasible for the chosen fiber family.
- A paired-sample reference protocol with the existing laboratory method is possible.

## Not covered by the supplied sources

- No source states the achievable fiber length for a mid-IR (CIR/PIR) or hollow-waveguide link between probe and analyzer.
- No source states accuracy, detection limit, precision or response time for water in petroleum.
- No source states probe or fiber temperature, pressure or area-classification ratings.
- No source covers cleaning, fouling or maintenance strategy for petroleum streams.
- No source addresses this customer's specific stream, its water speciation or its required detection limit.
- No source covers the customer's current laboratory water method or sampling procedure.
- No AFS product codes or prices appear in the supplied material.

## Evidence (verified quotes)

1. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum"
2. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
3. ✓ **S01 p.3** (general): "It allows for in-process analysis, i.e., directly in the process flow or reactor without sampling, eliminating delays and the risk of sample contamination."
4. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
5. ✓ **S01 p.15** (general): "The use of fiber optics is critical here, as it allows the sensitive spectrometers to be located safely away from the vibration and dust of the manufacturing floor."
6. ✓ **S02 p.20** (general): "AFS tests your process using all key fiber optic spectroscopy methods."
7. ✓ **S01 p.3** (general): "The ability to test various optical spectroscopy approaches is crucial for solving complex analytical problems, such as analyzing natural and industrial samples of incompletely known composition, in order to select the most suitable method or combination of methods."
8. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum"
9. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
10. ✓ **S01 p.9** (general): "Due to the high extinction coefficients of various molecules in this region, the method is highly sensitive and can be used to analyze a wide variety of samples: solids, liquids, and gases."
11. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
12. ✓ **S02 p.8** (general): "PIR-fiber transmission range 3-16μm is in the perfect match with Black Body Spectral Radiance at 0-100°C and Finger-Print Region of Molecular Vibrations"
13. ✓ **S01 p.7** (method gain): "The analysis of such systems may require a combination of two or even more spectral methods."
14. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
15. ✓ **S01 p.18** (general): "NIR Transmission is the preferred method for transparent or semi-transparent liquids"
16. ✓ **S01 p.18** (general): "The key experimental action is the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
17. ✓ **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
18. ✓ **S01 p.16** (general): "Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance for water molecules compared to infrared methods."
19. ✓ **S01 p.11** (general): "Furthermore, observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
20. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers"
21. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
22. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
23. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
24. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm)"
25. ✓ **S01 p.11** (general): "The difference between the observed frequencies and the laser frequency is called the Raman shift, expressed in units of frequency-wavenumbers (cm-1)."
26. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer"
27. ✓ **S01 p.13** (general): "typically at a depth of few microns"
28. ✓ **S02 p.7** (performance figure): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
29. ✓ **S01 p.11** (general): "Furthermore, observing Raman bands is often complicated by light scattering from the illuminating laser, and for many organic compounds, by the superposition of luminescence (fluorescence), which has a significantly higher intensity."
30. ✓ **S01 p.10** (general): "The broad absorption bands observed in this region overlap, suggesting the use of chemometrics for quantitative and qualitative analysis of spectral data."
31. ✓ **S01 p.16** (performance figure): "NIR spectroscopy is effective for tracking major components like glucose or glycerol in the millimolar range but may lack the sensitivity to detect trace compounds below 0.1 percent."
32. ✓ **REF §5** (general): "calibration specific to the matrix"
33. ✓ **S01 p.7** (general): "Morphological factors, such as sample inhomogeneity (e.g., biological tissue) or process turbulence, must also be considered when selecting a measurement technique."
34. ✓ **S01 p.8** (method gain): "Ultimately, the measurement data must be normalized to a common time step."
35. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
36. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
37. ✓ **S02 p.20** (general): "AFS tests your process using all key fiber optic spectroscopy methods."
38. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
39. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

## Verification

- Citations verified: 39 of 39 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Remaining hard check failures: 0; soft warnings: 5; repair rounds: 2.

*Run D06 · models deepseek/deepseek-v4.1-flash · cost $0.0177*
