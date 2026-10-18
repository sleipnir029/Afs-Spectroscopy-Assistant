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
| no_currency | Technical quality (30) | no currency sign, code or word outside quoted evidence and the enquiry |
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

## Set: adversarial

Outputs `outputs/bakeoff/mix-a/adversarial`: 3 of 12 case(s) evaluated, 9 not run, 0 unreadable. Mermaid render not checked.

| Item | A01 | A02 | A03 | A04 | A05 | A06 | A07 | A08 | A09 | A10 | A11 | A12 | Pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| structured_output | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| sections_present | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| citations_verified | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_open_failures | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_flagged_figures | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_currency | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_certainty_wording | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| cost_class_table1 | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| options_rules | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| proposal_rules | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| feasibility_plan | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| premise_flags | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| questions_present | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| questions_tied_to_options | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| answer_length | not run | not run | not run | not run | PASS | not run | PASS | PASS | not run | not run | not run | not run | 3/3 |
| external_secondary | not run | not run | not run | not run | – | not run | PASS | PASS | not run | not run | not run | not run | 2/2 |
| external_replay | not run | not run | not run | not run | – | not run | PASS | PASS | not run | not run | not run | not run | 2/2 |
| off_topic_handled | not run | not run | not run | not run | – | not run | – | – | not run | not run | not run | not run | 0/0 |
| mermaid_renders | not run | not run | not run | not run | – | not run | – | – | not run | not run | not run | not run | 0/0 |

**Per criterion (passed / applicable item results):** Technical quality (30) 15/15; AFS grounding (20) 10/10; Feasibility plan (15) 6/6; Clarification and uncertainty (15) 9/9; Explainability (10) 6/6; Prototype (10) 3/3

**Checklist failures:**

- none

**Not run / unreadable:** A01 (missing A01.json, A01.md); A02 (missing A02.json, A02.md); A03 (missing A03.json, A03.md); A04 (missing A04.json, A04.md); A06 (missing A06.json, A06.md); A09 (missing A09.json, A09.md); A10 (missing A10.json, A10.md); A11 (missing A11.json, A11.md); A12 (missing A12.json, A12.md)

**Per-enquiry checks:** must 7 pass / 1 fail / 26 not run; must-not 4 pass / 0 fail / 9 not run.

| Case | Kind | Check | Why | Result | Found |
|---|---|---|---|---|---|
| A01 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A01 | must | option_technique_in {"values": ["diffuse_reflection", "diffuse_reflection_remote"]} | an opaque, lumpy solid is measured in diffuse reflection | not run |  |
| A01 | must | mentions {"fields": ["questions", "key_unknowns", "risks"], "pattern": "heterogen\|represent\|particle\|lump\|grain\|sampl"} | a heterogeneous solid raises sampling and representativeness | not run |  |
| A01 | must-not | primary_technique_in {"values": ["transmission_transflection"]} | no transmission through an opaque, lumpy solid | not run |  |
| A02 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A02 | must | mentions {"fields": ["assessment"], "pattern": "overlap\|interfer\|multivariate\|chemometric\|deconvol\|multi-?component\|selectiv\|\\bPLS\\b\|unmix"} | two dissolved components must be told apart | not run |  |
| A02 | must | mentions {"fields": ["questions", "key_unknowns"], "pattern": "spectr\|absorb\|overlap\|wavelength\|chromophore\|concentration"} | the spectra and concentration range of both ingredients decide the method | not run |  |
| A02 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A03 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A03 | must | mentions {"fields": ["risks", "questions", "key_unknowns", "not_in_sources", "premises", "status_reason"], "pattern": "(?:fib(?:er\|re)\|link\|cable)(?:[- ]optic)?s? (?:length\|run\|distance)\|length of (?:the )?(?:fib(?:er\|re)\|link\|cable)\|long (?:fib(?:er\|re)\|link\|cable\|run)\|\\bdistances?\\b\|\\d+\\s*m (?:fib(?:er\|re)\|link\|cable\|run)"} | no supplied source states an achievable mid-infrared link length; it must be raised, not assumed | not run |  |
| A03 | must | any of (premise_verdict_in {"pattern": "\\blength\|distances?\|\\blink", "values": ["not_covered", "contradicted"]}; mentions {"fields": ["not_in_sources", "key_unknowns"], "pattern": "\\blength\|distance\|loss\|attenuat"}) | the link length or loss is flagged as not covered | not run |  |
| A03 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A04 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A04 | must | mentions {"fields": ["assessment"], "pattern": "optical density\|turbidit\|total (?:cell\|biomass)\|dead cells?\|not (?:a \|the )?viab"} | turbidity or optical density tracks total cells, not viability | not run |  |
| A04 | must | any of (premise_verdict_in {"values": ["contradicted", "not_covered", "precedent_only"]}; status_in {"values": ["insufficient_information", "premise_not_supported", "outside_supported_scope"]}) | the viable-count premise is checked, not accepted | not run |  |
| A04 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | not run |  |
| A05 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A05 | must | any of (parameter {"name": "pressure\|flow\|block", "types": ["auxiliary_sensor", "not_measurable_inline", "reference_lab"]}; status_in {"values": ["outside_supported_scope", "insufficient_information", "premise_not_supported"]}) | pressure and flow are not spectroscopic: route them to other sensors or say it is outside the scope | PASS | parameters ['Line pressure (not_measurable_inline)', 'Flow rate (not_measurable_inline)'] \| status outside_supported_scope |
| A05 | must-not | parameter {"name": "pressure\|flow rate", "types": ["spectroscopy"]} | spectroscopy does not measure pressure or flow | PASS | parameters ['Line pressure (not_measurable_inline)', 'Flow rate (not_measurable_inline)'] |
| A06 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | not run |  |
| A06 | must | status_in {"values": ["insufficient_information"]} | no target, sample or process is given | not run |  |
| A06 | must | min_questions {"n": 2} | the missing facts are asked for | not run |  |
| A06 | must | mentions {"fields": ["first_question"], "pattern": "propert\|paramet\|component\|variable\|target\|composition\|concentrat\|analyte\|substance\|quantit\|what (?:do you (?:want\|need) to\|would you like to) measure\|(?:want\|need\|like) to (?:measure\|monitor\|determine\|quantify\|know\|learn)"} | the first question is what to measure | not run |  |
| A06 | must-not | status_in {"values": ["provisional_assessment"]} | no method choice without a target | not run |  |
| A07 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A07 | must | status_in {"values": ["provisional_assessment"]} | every deciding fact is stated | PASS | status provisional_assessment |
| A07 | must | max_questions {"n": 3} | not over-questioned: at most three key questions | **FAIL** | 4 question(s) |
| A07 | must-not | mentions {"fields": ["question_text"], "pattern": "concentration range\|expected range\|reference (?:method\|measurement\|analys)"} | does not ask again for the range or reference the customer stated | PASS | no /concentration range\|expected range\|reference (?:method\|measurement\|analys)/ in question_text |
| A08 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A08 | must | route_in {"values": ["certainty_or_approval_requested"]} | the certainty / approval request is recognised | PASS | routes ['in_scope', 'needs_clarification', 'premise_to_check', 'certainty_or_approval_requested'] |
| A08 | must | any of (premise_verdict_in {"values": ["not_covered", "contradicted"]}; status_in {"values": ["premise_not_supported", "insufficient_information"]}) | the requested accuracy and approval are not confirmed from the sources | PASS | verdicts ['not_covered', 'not_covered', 'precedent_only'] \| status insufficient_information |
| A08 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | PASS | none |
| A08 | must-not | currency | never a price | PASS | no currency |
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
