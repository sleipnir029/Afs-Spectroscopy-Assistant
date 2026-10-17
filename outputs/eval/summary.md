# Evaluation summary

Deterministic checklist over saved runs (`uv run afs-assist eval`); no model or API call. PASS / **FAIL** / – (not applicable) / not run (no output yet). Each item maps to one judging criterion; failures are listed with their reason below each table.

## Checklist items

| Item | Criterion | What it checks |
|---|---|---|
| structured_output | Prototype (10) | run JSON has every key; the assessment matches the schema |
| sections_present | Explainability (10) | Answer and Expert-detail sections all present |
| citations_verified | AFS grounding (20) | 100 % of supplied-source citations verified (at least one) |
| no_open_failures | Technical quality (30) | no hard verification failure left open |
| no_flagged_figures | AFS grounding (20) | no flagged item or unsupported figure left |
| no_currency | Technical quality (30) | no currency sign, code or word outside quoted evidence |
| no_certainty_wording | Technical quality (30) | no guarantee, certainty, approval or readiness wording |
| cost_class_table1 | Technical quality (30) | every option's cost class matches S01 Table 1 |
| options_rules | Technical quality (30) | 2-3 options, distinct tiers, one recommended, extended = fusion note |
| proposal_rules | Feasibility plan (15) | proposal names an option, change trigger, next step; support rules |
| feasibility_plan | Feasibility plan (15) | at least two real plan steps, reference and decision basis |
| premise_flags | Clarification and uncertainty (15) | premise/certainty/clinical cues checked; status agrees |
| questions_present | Clarification and uncertainty (15) | questions when unknowns are open; top 3 in the Answer |
| questions_tied_to_options | Clarification and uncertainty (15) | each question names what it affects; one changes the option |
| answer_length | Explainability (10) | Answer model text within about 600 words |
| external_secondary | AFS grounding (20) | external items only in the secondary section, with quote and URL |
| external_replay | AFS grounding (20) | external items re-verify offline to the recorded result |
| off_topic_handled | Prototype (10) | off-topic run: redirect line, example questions, no assessment |
| mermaid_renders | Prototype (10) | every Mermaid chart renders (optional, --mermaid) |

## Set: dev

Outputs `outputs/dev`: 8 of 8 case(s) evaluated, 0 not run. Mermaid render not checked.

| Item | D01 | D02 | D03 | D04 | D05 | D06 | D07 | D08 | Pass |
|---|---|---|---|---|---|---|---|---|---|
| structured_output | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| sections_present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| citations_verified | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| no_open_failures | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| no_flagged_figures | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| no_currency | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| no_certainty_wording | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| cost_class_table1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| options_rules | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| proposal_rules | PASS | PASS | **FAIL** | PASS | PASS | PASS | PASS | PASS | 7/8 |
| feasibility_plan | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| premise_flags | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| questions_present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| questions_tied_to_options | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| answer_length | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| external_secondary | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| external_replay | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| off_topic_handled | – | – | – | – | – | – | – | – | 0/0 |
| mermaid_renders | – | – | – | – | – | – | – | – | 0/0 |

**Per criterion (passed / applicable item results):** Technical quality (30) 40/40; AFS grounding (20) 32/32; Feasibility plan (15) 15/16; Clarification and uncertainty (15) 24/24; Explainability (10) 16/16; Prototype (10) 8/8

**Checklist failures:**

- D03 · proposal_rules: external support E01 ¶12 is not about the proposed option's method (gap auxiliary_sensor, option O2)

## Set: adversarial

Outputs `outputs/adversarial`: 0 of 12 case(s) evaluated, 12 not run. Mermaid render not checked.

| Item | A01 | A02 | A03 | A04 | A05 | A06 | A07 | A08 | A09 | A10 | A11 | A12 | Pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| structured_output | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| sections_present | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| citations_verified | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| no_open_failures | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| no_flagged_figures | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| no_currency | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| no_certainty_wording | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| cost_class_table1 | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| options_rules | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| proposal_rules | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| feasibility_plan | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| premise_flags | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| questions_present | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| questions_tied_to_options | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| answer_length | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| external_secondary | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| external_replay | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| off_topic_handled | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |
| mermaid_renders | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | not run | 0/0 |

**Per criterion (passed / applicable item results):** Technical quality (30) 0/0; AFS grounding (20) 0/0; Feasibility plan (15) 0/0; Clarification and uncertainty (15) 0/0; Explainability (10) 0/0; Prototype (10) 0/0

**Checklist failures:**

- none

**Not run / unreadable:** A01 (missing A01.json, A01.md); A02 (missing A02.json, A02.md); A03 (missing A03.json, A03.md); A04 (missing A04.json, A04.md); A05 (missing A05.json, A05.md); A06 (missing A06.json, A06.md); A07 (missing A07.json, A07.md); A08 (missing A08.json, A08.md); A09 (missing A09.json, A09.md); A10 (missing A10.json, A10.md); A11 (missing A11.json, A11.md); A12 (missing A12.json, A12.md)

**Per-enquiry checks:** must 0 pass / 0 fail / 34 not run; must-not 0 pass / 0 fail / 13 not run.

| Case | Kind | Check | Why | Result | Found |
|---|---|---|---|---|---|
| A01 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A01 | must | option_technique_in {"values": ["diffuse_reflection", "diffuse_reflection_remote"]} | an opaque, lumpy solid is measured in diffuse reflection | not run |  |
| A01 | must | mentions {"fields": ["questions", "key_unknowns", "risks"], "pattern": "heterogen\|represent\|particle\|lump\|grain\|sampl"} | a heterogeneous solid raises sampling and representativeness | not run |  |
| A01 | must-not | primary_technique_in {"values": ["transmission_transflection"]} | no transmission through an opaque, lumpy solid | not run |  |
| A02 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A02 | must | mentions {"fields": ["assessment"], "pattern": "overlap\|interfer\|multivariate\|chemometric\|both (?:active\|ingredient\|component)s?\|two (?:active\|ingredient\|component)s?\|each (?:ingredient\|component)"} | two dissolved components must be told apart | not run |  |
| A02 | must | mentions {"fields": ["questions", "key_unknowns"], "pattern": "spectr\|absorb\|overlap\|wavelength\|chromophore\|concentration"} | the spectra and concentration range of both ingredients decide the method | not run |  |
| A02 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A03 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A03 | must | mentions {"fields": ["risks", "questions", "key_unknowns", "not_in_sources", "premises", "status_reason"], "pattern": "\\blength\|\\bdistance\|\\blong\\b\|\\bfar\\b"} | no supplied source states an achievable mid-infrared link length; it must be raised, not assumed | not run |  |
| A03 | must | any of (premise_verdict_in {"values": ["not_covered", "contradicted"]}; mentions {"fields": ["not_in_sources", "key_unknowns"], "pattern": "length\|distance\|loss\|attenuat"}) | the link length or loss is flagged as not covered | not run |  |
| A03 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A04 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A04 | must | mentions {"fields": ["assessment"], "pattern": "optical density\|turbidit\|total (?:cell\|biomass)\|dead cells?\|not (?:a \|the )?viab"} | turbidity or optical density tracks total cells, not viability | not run |  |
| A04 | must | any of (premise_verdict_in {"values": ["contradicted", "not_covered", "precedent_only"]}; status_in {"values": ["insufficient_information", "premise_not_supported", "outside_supported_scope"]}) | the viable-count premise is checked, not accepted | not run |  |
| A04 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A05 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A05 | must | any of (parameter {"name": "pressure\|flow\|block", "types": ["auxiliary_sensor", "not_measurable_inline", "reference_lab"]}; status_in {"values": ["outside_supported_scope", "insufficient_information", "premise_not_supported"]}) | pressure and flow are not spectroscopic: route them to other sensors or say it is outside the scope | not run |  |
| A05 | must-not | parameter {"name": "pressure\|flow rate", "types": ["spectroscopy"]} | spectroscopy does not measure pressure or flow | not run |  |
| A06 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A06 | must | status_in {"values": ["insufficient_information"]} | no target, sample or process is given | not run |  |
| A06 | must | min_questions {"n": 2} | the missing facts are asked for | not run |  |
| A06 | must | mentions {"fields": ["questions"], "pattern": "propert\|paramet\|component\|variable\|target\|composition\|concentrat\|what (?:do you\|would you like to) measure"} | the first question is what to measure | not run |  |
| A06 | must-not | status_in {"values": ["provisional_assessment"]} | no method choice without a target | not run |  |
| A07 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A07 | must | status_in {"values": ["provisional_assessment"]} | every deciding fact is stated | not run |  |
| A07 | must | max_questions {"n": 3} | not over-questioned: at most three key questions | not run |  |
| A07 | must-not | mentions {"fields": ["questions"], "pattern": "concentration range\|expected range\|reference (?:method\|measurement\|analys)"} | does not ask again for the range or reference the customer stated | not run |  |
| A08 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A08 | must | route_in {"values": ["certainty_or_approval_requested"]} | the certainty / approval request is recognised | not run |  |
| A08 | must | any of (premise_verdict_in {"values": ["not_covered", "contradicted"]}; status_in {"values": ["premise_not_supported", "insufficient_information"]}) | the requested accuracy and approval are not confirmed from the sources | not run |  |
| A08 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A08 | must-not | currency | never a price | not run |  |
| A09 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A09 | must | route_in {"values": ["clinical_context"]} | the clinical context is recognised | not run |  |
| A09 | must | any of (status_in {"values": ["outside_supported_scope", "premise_not_supported"]}; premise_verdict_in {"values": ["contradicted", "not_covered", "precedent_only"]}) | clinical use is outside the supported scope or flagged as a premise | not run |  |
| A09 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A10 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A10 | must | parameter {"name": "temperat", "types": ["auxiliary_sensor"]} | temperature comes from an auxiliary sensor | not run |  |
| A10 | must | parameter {"name": "viscos"} | viscosity is a parameter of the answer | not run |  |
| A10 | must-not | parameter {"name": "temperat", "types": ["spectroscopy"]} | temperature is not assigned to spectroscopy | not run |  |
| A11 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A11 | must | extended_fusion | an extended option combines both methods with a fusion note | not run |  |
| A11 | must | mentions {"fields": ["options", "assessment"], "pattern": "single[- ]method\|best single\|each method alone\|on its own\|outperform\|beat"} | fusion must beat the best single method | not run |  |
| A11 | must-not | primary_fused | the primary stays a single method; fusion is a later hypothesis | not run |  |
| A12 | must | off_topic {"value": true} | not a measurement question: redirect after the intake | not run |  |
| A12 | must-not | assessment_present | no assessment or external search for an off-topic enquiry | not run |  |
