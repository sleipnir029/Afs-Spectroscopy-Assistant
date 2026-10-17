# First technical assessment: Fat and protein monitoring in opaque dairy product

**Customer enquiry**

> We produce an opaque, concentrated milk product that flows through a processing line. We currently sample it for fat and protein analysis and would like earlier information about composition changes. Product temperature and texture vary during production. We want an initial spectroscopy concept and a practical comparison experiment, while retaining our laboratory checks.

**Decision status:** Provisional feasibility assessment. A shortlist is defensible because one candidate passed the deterministic screening (NIR diffuse reflection) and the dairy example in the sources supports in-line NIR on opaque, concentrated products. The shortlist rests on stated assumptions: the product can be measured at a point where it is a flowing liquid or soft solid, and the composition changes of interest are large enough for NIR. Accuracy, detection limits, response time and fiber-link length for this product are not in the supplied sources and must come from the customer and from the trial.

## Premise check

- **Supported:** Earlier information about composition changes is achievable with an in-line fiber measurement. Supported as a published application precedent for in-line NIR monitoring of milk, not as proof for this product, and it says nothing about how much earlier the information would arrive. [1: S01 p.17] [2: S01 p.10]
- **Supported:** An initial concept and a practical comparison experiment can be provided before all method-selection facts are known. Guidance for this kind of assessment explicitly allows a provisional plan on incomplete facts. [3: REF §3]
- **Not covered:** Laboratory checks can be retained alongside the new measurement. No supplied source addresses keeping routine reference laboratory checks alongside an in-line measurement in production. The sources only require independent reference measurements inside a feasibility plan. [4: REF §3]

## Requirements

**Stated by the customer**

- Opaque, concentrated milk product flowing through a processing line (customer facts).
- Targets: fat content and protein content, plus earlier information about composition changes.
- Product temperature and texture vary during production.
- Wanted: an initial spectroscopy concept and a practical comparison experiment, while keeping the existing laboratory checks.

**Key unknowns**

- Physical state and rheology at the intended measurement point (pumpable liquid vs paste, and how the texture varies).
- Fat and protein ranges, the size of the composition change to be detected, and the accuracy of the current laboratory method.
- Optical density / turbidity of the product at the measurement point, and how much it changes during production.
- Temperature range and pressure at the measurement point (spectral effects of temperature are not covered by the supplied sources).
- Installation point, distance from the measurement point to a safe instrument location, and required update time.
- Cleaning, fouling and CIP regime at the measurement point.

## Clarification questions (most decision-relevant first)

Q1. What is the physical state of the product at the intended measurement point - a pumpable liquid, a viscous paste, or does it change between these states during production - and can it make tight contact with a flat probe face? *Why it matters:* Decides whether MIR-ATR is usable at all (ATR needs tight contact) and how the reflection probe must be mounted. *(affects: MIR ATR status, probe geometry, installation)*
Q2. Which laboratory method do you use for fat and protein, what accuracy does it give, what ranges do you expect in the line, and how large is the composition change you must detect? *Why it matters:* Sets the go/no-go numbers and decides whether NIR sensitivity is sufficient for the change of interest. *(affects: method choice, feasibility criteria)*
Q3. How opaque or turbid is the product at the measurement point, and does this change during production? *Why it matters:* Decides diffuse reflection versus transmission/transflection geometry, and whether a transflection probe is worth testing. *(affects: technique, probe geometry)*
Q4. Where on the line should the measurement be made, how far is the nearest safe place for a spectrometer, and how fast must a result be available? *Why it matters:* Decides the fiber link; no source states an achievable MIR link length, so it stays an open question for AFS. *(affects: installation, fiber family, response time)*
Q5. What are the temperature range and pressure at the measurement point, and what cleaning/CIP and fouling regime applies there? *Why it matters:* Decides probe construction, materials and maintenance interval; the sources give no temperature or pressure ratings for a probe. *(affects: installation, probe design, maintenance)*

## Recommendation

- **R1 · Primary candidate: NIR, diffuse reflection.** The only candidate that passed the screening for this product. In-line NIR reflection is the documented route for opaque or highly concentrated dairy products, and NIR is the most common online method run through fiber probes. The probe is a backscatter head mounted into the pipe or vessel wall. A chemometric calibration specific to this matrix is required, with scatter correction for the changing texture. *Conditions:* Applies if the product at the measurement point is an opaque, flowing medium (liquid or soft solid) that can be presented to the probe window. [5: S01 p.17] [6: S01 p.17] [7: S02 p.6] [8: REF §5]
- **R2 · Comparison candidate: NIR, transmission transflection.** Same method, different geometry, worth testing against R1 in the same trial. A transflection probe has been described as, in some cases, working for both low-fat and high-fat milk products, which matches a product whose texture varies. Plain transmission is expected to fail for a thick or fat-rich product, so treat this as a geometry comparison, not as a stand-alone recommendation. Pathlength must be controlled (1-10 mm in the dairy example). *Conditions:* Applies where the product at the measurement point is transparent or semi-transparent enough at the chosen pathlength; the deciding fact is the optical density (Q3). [9: S01 p.18] [10: S01 p.18] [11: S01 p.18]
- **R3 · Conditional candidate: MIR, ATR.** Complementary vibrational information from a different sampling depth (a few micrometres at the crystal) and the usual in-line route for liquids and soft solids in contact with the crystal. MIR-ATR with a ZrO2 tip has been shown for water in petroleum, and NIR reflection plus MIR-ATR has been shown for in-line polymer extrusion. MIR needs chalcogenide or polycrystalline fibers, not silica; the achievable MIR link length is an open question (Q4). *Conditions:* Applies only if Q1 shows the product at the measurement point is a pumpable liquid or soft solid that can make tight contact with the ATR crystal. Screening status is unknown until then. [12: S01 p.10] [13: S01 p.5] [14: S02 p.13] [15: S02 p.14] [16: REF §5]
- **NR1 · Not recommended: UV-Vis, transmission transflection.** Failed the deterministic screening: transmission fails when the sample is too thick or fat-rich because light cannot penetrate it, which is the customer's stated case. A UV-Vis option could only be reconsidered later with an ATR or reflection geometry, which is not what was asked for here. *Conditions:* None in the current concept. [17: S01 p.18]

## Measurement concept

- **Probe and geometry:** NIR backscatter (diffuse reflection) head, flush-mounted into the pipe or vessel wall at the point of interest; one fiber set delivers light to the sample, the other collects the backscattered light. A transflection probe is the alternative geometry to compare. For the conditional MIR option, an ATR probe in contact with the product.
- **Location:** At the point in the line where the composition information is needed; probes are inserted directly into the process environment.
- **Fiber link:** Vis-NIR silica fibers for NIR; long 100-300 m cables are stated only for low-OH silica fibers. MIR needs chalcogenide or polycrystalline fibers; no achievable MIR link length is stated in the sources. [18: S01 p.15] [19: S02 p.7] [20: S02 p.6]

## Spectral range

- **NIR:** Nominal method range 780-2500 nm. The usable range depends on the instrument, fiber and probe actually selected. [21: S01 p.10] [22: REF §5]
- **MIR:** Nominal method range 4000-400 cm-1 (2.5-25 µm). Again, the usable range depends on the instrument, fiber and crystal actually selected. [23: S01 p.9]

## Risks and uncertainty

- Texture and optical-density variation can look like a composition change: the reflection signal is sensitive to surface characteristics and particle size, and a calibration is specific to the matrix. A calibration built at one texture or temperature may not transfer to the full production range. *(rules: R-GEO-6, R-CAL-1)* [24: S01 p.17] [25: REF §5]
- The composition changes of interest may be too small for NIR. If the change to be detected is at trace level, a single NIR measurement may not see it, and the customer's target size of change must be stated before the trial. *(rules: R-NIR-4)* [26: S01 p.16]
- The MIR-ATR option depends on tight contact and samples only a surface layer a few micrometres deep, so deposits on the crystal and surface representativeness are risks; the usable range is limited by the fiber and crystal. *(rules: R-MIR-3, R-FIB-2)* [27: S01 p.13] [28: REF §5]
- The dairy and process examples in the sources are reasons to test the methods, not evidence that they will meet this customer's targets. No source gives accuracy, detection limits, response time or fiber length for this application. *(rules: R-EVI-2, R-PRO-3)* [29: REF §3]

## First feasibility experiment

1. **1** Representative sample and process-state set [30: REF §3]
2. **2** Independent reference values [31: REF §3]
3. **3** Single-method comparison [32: S01 p.17] [33: REF §5]
4. **4** Validation on held-out runs or batches [34: S03 p.14]
5. **5** Go/no-go and next step [35: REF §5]

**Reference measurements:** The customer's existing laboratory fat and protein method, run on split samples taken at the same time as the spectral measurements, with the sampling frequency the customer already uses.

**Decision basis:** The numerical go/no-go criteria must come from the customer: agreement with the laboratory fat and protein method within the customer's stated limits, across the full temperature and texture range, at the update time the customer specifies. No numerical criterion can be taken from the supplied sources.

## Assumptions

- The product can be presented to a probe at the chosen line position as a flowing liquid or soft solid.
- The composition change to be detected is large enough to produce a measurable spectral change.
- The customer's laboratory fat and protein method can serve as the independent reference.
- The process environment allows a probe to be mounted and cleaned without stopping production.

## Not covered by the supplied sources

- Any accuracy, limit of detection or response-time figure for fat or protein measurement in this product; the sources give no such numbers for this application.
- Any usable MIR fiber-link length; the sources show only laboratory-scale lengths and state no achievable length for an MIR link.
- Any statement about retaining routine reference laboratory checks alongside an in-line measurement in production.

## Evidence (verified quotes)

1. ✓ **S01 p.17** (application precedent): "The use of Near-Infrared (NIR) spectroscopy for the inline monitoring of milk is a cornerstone of modern dairy "Process Analytical Technology" (PAT)."
2. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
3. ✓ **REF §3** (general): "An honest provisional plan is more useful than a final configuration built on missing facts."
4. ✓ **REF §3** (general): "independent reference measurements"
5. ✓ **S01 p.17** (application precedent): "Inline NIR Reflection is primarily used for opaque or highly concentrated dairy products, such as yogurt, butter, or whole milk concentrates."
6. ✓ **S01 p.17** (general): "a fiber optic probe where one set of fibers delivers light to the sample and the other collects the "backscattered" light."
7. ✓ **S02 p.6** (general): "350 nm Standard VIS-NIR Silica Fibers Al/Cu-coated VIS-NIR Silica Fibers 2400 nm"
8. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
9. ✓ **S01 p.18** (application precedent): "In some cases, a Transflection probe can already be a combined solution working well for low-fat and high-fat containing milk products."
10. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
11. ✓ **S01 p.18** (general): "the precise control of the optical pathlength (usually 1 - 10 mm); if the pathlength is too wide, the signal is lost to absorption; if too narrow, the sample represents a negligible volume."
12. ✓ **S01 p.10** (general): "ATR fiber probes (Fig.1) enable the analysis of liquids and solid elastic samples"
13. ✓ **S01 p.5** (general): "strong absorption in the mid-IR region limits the corresponding spectral method to the analysis of very thin samples (usually less than 50 μm), but it opens up the possibility of using attenuated total reflectance (ATR)"
14. ✓ **S02 p.13** (application precedent): "measurement of water content in petroleum"
15. ✓ **S02 p.14** (application precedent): "NIR-Reflex & MIR-ATR-spectroscopy to control polymer extrusion in-line"
16. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
17. ✓ **S01 p.18** (general): "it fails when the milk becomes too "thick" or fat-rich, as the light cannot penetrate the sample."
18. ✓ **S01 p.15** (general): "the probes are inserted directly into the process environment"
19. ✓ **S02 p.7** (general): "Robust 100-300m cables made with Silica fibers of low OH-content (<0.1ppm OH) enable remote industrial process-control"
20. ✓ **S02 p.6** (general): "3000 nm Polycrystalline Infrared Fibers 17 μm"
21. ✓ **S01 p.10** (general): "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
22. ✓ **REF §5** (general): "It is not a product specification: actual spectral coverage, fiber length, component ratings, detection limits and accuracy depend on the configuration and the sample."
23. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
24. ✓ **S01 p.17** (general): "the method is sensitive to the surface characteristics and fat globule size."
25. ✓ **REF §5** (general): "physical variation; calibration specific to the matrix."
26. ✓ **S01 p.16** (general): "may lack the sensitivity to detect trace compounds below 0.1 percent."
27. ✓ **S01 p.13** (general): "typically at a depth of few microns"
28. ✓ **REF §5** (general): "Usable range limited by fiber and crystal; contact, fouling, compatibility."
29. ✓ **REF §3** (general): "a published application is a reason to test a method, not proof that it will work for a new customer."
30. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."
31. ✓ **REF §3** (general): "independent reference measurements"
32. ✓ **S01 p.17** (general): "to remove physical interference caused by the scattering nature of the milk particles"
33. ✓ **REF §5** (general): "compare with the best single method."
34. ✓ **S03 p.14** (general): "A thorough validation, including full, segmented and random-subset CVs, as well as randomization tests, are recommended in any cases for which important conclusions depend on calibration or discrimination models built on limited experimental material."
35. ✓ (precedent only) **REF §5** (method gain): "Sampling location and timing must be aligned; a gain is a hypothesis to test."

## Verification

- Citations verified: 35 of 35 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 1; repair rounds: 1.

*Run D02-20261017T093510Z · models deepseek/deepseek-v4.1-flash · cost $0.0166*
