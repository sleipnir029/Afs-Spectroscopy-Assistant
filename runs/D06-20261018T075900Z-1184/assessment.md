# First technical assessment: Water content in a petroleum stream

## Answer

**Customer request (our summary):** The customer wants to investigate an in-line fiber-based measurement to determine water in a petroleum stream closer to the process.

### Brief answer

We recommend testing mid-infrared ATR spectroscopy first, as it is documented for water determination in petroleum streams. The analyzer can be placed outside the process area using fiber-optic links. Key unknowns such as stream optical regime, water concentration range, and process conditions must be clarified before finalizing equipment.

### Proposal

- **Best current option:** O1 (recommended)
- **Basis:** supplied AFS sources
- **What would change it:** If water concentrations fall below detection limits or petroleum properties prevent ATR contact, alternative methods like NIR or laboratory cross-checks would be needed.
- **Next step:** Conduct laboratory trials on representative petroleum samples using an MIR-ATR probe to establish calibration feasibility.

**Secondary evidence (external, not AFS material):** G1: no usable external source found. See Expert detail.

**Decision status:** Provisional feasibility assessment

### Solution options

| ID | Tier | Methods | Confidence | Cost class, S01 Table 1 (p.6) | Ease of use | Maintenance | Performance fit | Sources |
|---|---|---|---|---|---|---|---|---|
| O1 | Recommended | M1 MIR, ATR probe | Low: open question: Q1 (starts at Medium); precedent only | high cost (row 2) | Direct immersion probe in stream | Periodic cleaning of ATR crystal | Directly detects water via documented petroleum precedent | [1: S02 p.13] |
| O2 | Simple | M2 NIR, diffuse reflection probe | Low: open question: Q1, Q2 (starts at Medium); sample clarity unknown | average cost (row 8) | Standard silica fiber reflection probe | Probe window cleaning and inspection | Fast screening using standard NIR optics | [2: S01 p.10] |

*Confidence rates the basis of the advice (how much is known and cited), not a predicted accuracy or probability of success. It starts at High, or at Medium when a key question on the method or the option is open, and drops one level per weakness listed (floor Low).*

*Cost class is the relative rating in S01 Table 1 (p.6) for the in-line method+technique rows named (the highest one for a multi-method option); it is not a price.*

### Setup sketch

*Recommended option O1; drawn by code from the option, a schematic, not a configuration.*

```mermaid
flowchart LR
    proc["Process point: In-line in the petroleum stream closer to…"]
    probe1["MIR, ATR probe"]
    fiber1["Fiber: chalcogenide or polycrystalline or hollow waveguide…"]
    spec1["MIR spectrometer"]
    model["Chemometric model"]
    result["Result: Water content"]
    proc --> probe1
    probe1 --> fiber1
    fiber1 --> spec1
    spec1 --> model
    model --> result
```

### Key questions

1. What is the expected water concentration range in the petroleum stream?
2. What is the optical regime and turbidity of the petroleum stream (for instance clear, translucent, or opaque/scattering)?
3. What are the operating temperature, pressure, and flow velocity at the measurement point?

## Expert detail

**Customer enquiry**

> We handle a petroleum stream and currently send samples to a laboratory for water determination. We want to investigate a fiber based measurement closer to the process so that changes can be noticed sooner. The analyzer would be outside the process area. Before selecting equipment, we need to know what to clarify and what a first comparison experiment should establish.

**Decision status:** Provisional feasibility assessment. Mid-infrared attenuated total reflectance (MIR-ATR) spectroscopy is documented for measuring water in petroleum streams, providing a solid basis for a provisional recommendation pending clarification of concentration ranges and operating conditions.

### Parameters

| ID | Parameter | Kind | Need | Measured by | Why | Sources |
|---|---|---|---|---|---|---|
| P1 | Water content | quantitative | required | Spectroscopy: MIR | Core target parameter for process control. | [1: S02 p.13] |

### Solution option details

- **O1 cost drivers:** MIR spectrometer and ATR immersion probe
- **O2 cost drivers:** NIR spectrometer and reflection probe

### Premise check

- **Supported:** Fiber-based measurement can place the analyzer outside the process area for petroleum streams. Sources confirm that fiber optic probes allow remote measurements and online analysis without sampling while keeping spectrometers away from the process. [3: S01 p.10]

### Requirements

**Stated by the customer**

- Handle a petroleum stream
- Water determination
- Fiber-based measurement closer to the process
- Analyzer outside the process area

**Key unknowns**

- Water concentration range
- Optical regime and turbidity of the petroleum stream
- Exact petroleum matrix composition and variability
- Process temperature and pressure
- Required response time and measurement accuracy

### Clarification questions (most decision-relevant first)

Q1. What is the expected water concentration range in the petroleum stream? *Why it matters:* Determines whether MIR-ATR or an alternative method is best suited for the target concentration levels. *(affects: method, M1)*
Q2. What is the optical regime and turbidity of the petroleum stream (for instance clear, translucent, or opaque/scattering)? *Why it matters:* Determines whether diffuse reflection or transmission is applicable for NIR measurements. *(affects: technique, M2)*
Q3. What are the operating temperature, pressure, and flow velocity at the measurement point? *Why it matters:* Defines the mechanical and thermal specifications required for probe materials and seals. *(affects: installation)*
Q4. What is the required response time and measurement accuracy for process control? *Why it matters:* Influences spectrometer acquisition parameters and chemometric model complexity. *(affects: technique)*
Q5. What is the exact chemical composition and variability of the petroleum matrix? *Why it matters:* Impacts background absorption and calibration robustness. *(affects: method)*

### Recommendation

- **M1 · Primary candidate: MIR, ATR probe.** Mid-infrared ATR spectroscopy is established for water determination in petroleum streams using durable ATR tips. [1: S02 p.13]
- **M2 · Comparison candidate: NIR, diffuse reflection probe.** NIR spectroscopy can serve as an alternative online method for hydrocarbon and water monitoring if optical scattering permits. *Conditions:* If water concentrations and optical scattering properties permit reflection measurements. [2: S01 p.10]

### Measurement concept

- **Probe and geometry:** MIR-ATR immersion probe with a Zirconia or diamond ATR tip sealed in a PEEK shaft.
- **Location:** In-line in the petroleum stream closer to the process.
- **Fiber link:** Chalcogenide (CIR) or polycrystalline infrared (PIR) fiber cables connecting the immersion probe to the spectrometer located outside the process area. [4: S02 p.13] [3: S01 p.10]

### Spectral range

- **MIR:** The nominal mid-IR range is 4000-400 cm-1; the usable range depends on the instrument, fiber, and ATR crystal selected. [5: S01 p.9]

### Risks and uncertainty

- Fouling or coating on the ATR crystal by heavy petroleum fractions can degrade the signal over time. *(rules: R-MIR-3)* [6: S01 p.13]
- Fiber transmission limits or coupling efficiency for mid-IR radiation over longer distances outside the process area. *(rules: R-FIB-2, R-FIB-3)* [7: S02 p.10]

### First feasibility experiment

1. **Collect representative petroleum samples spanning the expected water concentration range.** Ensure samples cover expected chemical and physical variation. [8: REF §3]
2. **Perform reference laboratory water determinations for all collected samples.** Establish independent reference measurements for model calibration. [8: REF §3]
3. **Test MIR-ATR probe response across the samples and build an initial partial least squares calibration model.** Evaluate feasibility and correlation between spectra and water content. [1: S02 p.13]

**Reference measurements:** Standard laboratory water determination methods currently used by the customer.

**Decision basis:** Proceed based on customer-defined accuracy and response time criteria matching laboratory reference values.

### Assumptions

- The petroleum stream is fluid enough to maintain contact with an ATR probe tip.
- The optical regime of the petroleum stream allows optical probing, assumed opaque or scattering for diffuse reflection or clear for transmission.
- The spectrometer can be housed outside the process area with an appropriate fiber optic link.

### Not covered by the supplied sources

- Exact distance from the process point to the analyzer outside the process area.

### Further notes

- **Chemometrics:** Multivariate calibration using PLS regression is necessary to relate MIR or NIR spectra to water concentration.
- **Real-time tracking:** In-line probe placement enables continuous real-time tracking of water content changes closer to the process.
- **Future direction:** Transition from laboratory trials to a dedicated optical multisensor system or IoT sensor once calibration is validated.

### Secondary evidence (external, not AFS material)

*Found by a literature search for gaps the supplied AFS sources leave open. Not AFS material and not proof for this case; every quote below was verified verbatim against the fetched text.*

**G1 · not in the supplied sources:** Exact distance from the process point to the analyzer outside the process area.

- No usable external source found.

### Evidence (verified quotes)

1. ✓ **S02 p.13** (application precedent): "Application: measurement of water content in petroleum ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"
2. ✓ **S01 p.10** (general): "Near-IR vibrational spectroscopy (NIR) is the most common online analysis method performed using fiber optic probes."
3. ✓ **S01 p.10** (general): "These immersion probes operate on the ATR principle but allow analysis at a significant distance from the spectrometer, without the need for sampling."
4. ✓ **S02 p.13** (application precedent): "ATR-Probes with ATR-tips from ZrO2 (& Diamond, etc.) sealed in PEEK-shaft and protected by PEEK-tubing can be used in microwave furnaces"
5. ✓ **S01 p.9** (general): "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis."
6. ✓ **S01 p.13** (general): "typically at a depth of few microns"
7. ✓ **S02 p.10** (general): "too low NA>0.1 - which results in very poor coupling efficiency with FTIR-spectrometers"
8. ✓ **REF §3** (general): "Representative samples or process states, independent reference measurements, what is compared, and the basis for the go / no-go decision."

### Verification

- Citations verified: 14 of 14 (exact or whitespace/hyphen-tolerant match on the cited page, scope checked).
- Hard check failures before deterministic corrections: 0; still open: 0; soft warnings: 1; repair rounds: 1.
- External evidence (cache): 0 quote(s) verified verbatim (exact or whitespace/hyphen-tolerant, at most 400 characters and 2 sentences, against the cited paragraph); 0 item(s) dropped.
- External search: 0 query(ies), 0 hit(s), 0 source(s) (0 from the curated library).
- External step: 1 model call(s), 0.7 s extra (cost in the run JSON).

*Run D06-20261018T075900Z-1184 · models google/gemini-3.5-flash-lite, google/gemini-3.8-flash*
