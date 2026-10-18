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

## Set: dev

Outputs `outputs/dev`: 8 of 8 case(s) evaluated, 0 not run, 0 unreadable. Mermaid render checked.

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
| proposal_rules | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| feasibility_plan | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| premise_flags | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| questions_present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| questions_tied_to_options | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| answer_length | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| external_secondary | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| external_replay | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |
| off_topic_handled | – | – | – | – | – | – | – | – | 0/0 |
| mermaid_renders | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 8/8 |

**Per criterion (passed / applicable item results):** Technical quality (30) 40/40; AFS grounding (20) 32/32; Feasibility plan (15) 16/16; Clarification and uncertainty (15) 24/24; Explainability (10) 16/16; Prototype (10) 16/16

**Checklist failures:**

- none

## Set: adversarial

Outputs `outputs/adversarial`: 12 of 12 case(s) evaluated, 0 not run, 0 unreadable. Mermaid render checked.

| Item | A01 | A02 | A03 | A04 | A05 | A06 | A07 | A08 | A09 | A10 | A11 | A12 | Pass |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| structured_output | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 12/12 |
| sections_present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| citations_verified | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| no_open_failures | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| no_flagged_figures | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| no_currency | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | 12/12 |
| no_certainty_wording | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| cost_class_table1 | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| options_rules | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| proposal_rules | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| feasibility_plan | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| premise_flags | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| questions_present | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| questions_tied_to_options | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| answer_length | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| external_secondary | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| external_replay | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |
| off_topic_handled | – | – | – | – | – | – | – | – | – | – | – | PASS | 1/1 |
| mermaid_renders | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 11/11 |

**Per criterion (passed / applicable item results):** Technical quality (30) 56/56; AFS grounding (20) 44/44; Feasibility plan (15) 22/22; Clarification and uncertainty (15) 33/33; Explainability (10) 22/22; Prototype (10) 24/24

**Checklist failures:**

- none

**Per-enquiry checks:** must 33 pass / 1 fail / 0 not run; must-not 13 pass / 0 fail / 0 not run.

| Case | Kind | Check | Why | Result | Found |
|---|---|---|---|---|---|
| A01 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A01 | must | option_technique_in {"values": ["diffuse_reflection", "diffuse_reflection_remote"]} | an opaque, lumpy solid is measured in diffuse reflection | PASS | techniques ['diffuse_reflection', 'diffuse_reflection_remote', 'raman_probe'] |
| A01 | must | mentions {"fields": ["questions", "key_unknowns", "risks"], "pattern": "heterogen\|represent\|particle\|lump\|grain\|sampl"} | a heterogeneous solid raises sampling and representativeness | PASS | questions: 'lump' |
| A01 | must-not | primary_technique_in {"values": ["transmission_transflection"]} | no transmission through an opaque, lumpy solid | PASS | techniques ['diffuse_reflection_remote'] |
| A02 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A02 | must | mentions {"fields": ["assessment"], "pattern": "overlap\|interfer\|multivariate\|chemometric\|deconvol\|multi-?component\|selectiv\|\\bPLS\\b\|unmix"} | two dissolved components must be told apart | PASS | assessment: 'overlap' |
| A02 | must | mentions {"fields": ["questions", "key_unknowns"], "pattern": "spectr\|absorb\|overlap\|wavelength\|chromophore\|concentration"} | the spectra and concentration range of both ingredients decide the method | PASS | questions: 'concentration' |
| A02 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | PASS | none |
| A03 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A03 | must | mentions {"fields": ["risks", "questions", "key_unknowns", "not_in_sources", "premises", "status_reason"], "pattern": "(?:fib(?:er\|re)\|link\|cable)(?:[- ]optic)?s? (?:length\|run\|distance)\|length of (?:the )?(?:fib(?:er\|re)\|link\|cable)\|long (?:fib(?:er\|re)\|link\|cable\|run)\|\\bdistances?\\b\|\\d+\\s*m (?:fib(?:er\|re)\|link\|cable\|run)"} | no supplied source states an achievable mid-infrared link length; it must be raised, not assumed | PASS | questions: 'link length' |
| A03 | must | any of (premise_verdict_in {"pattern": "\\blength\|distances?\|\\blink", "values": ["not_covered", "contradicted"]}; mentions {"fields": ["not_in_sources", "key_unknowns"], "pattern": "\\blength\|distance\|loss\|attenuat"}) | the link length or loss is flagged as not covered | PASS | verdicts ['not_covered', 'not_covered'] of premises matching /\blength\|distances?\|\blink/ \| not_in_sources: 'length' |
| A03 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | PASS | none |
| A04 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A04 | must | mentions {"fields": ["assessment"], "pattern": "optical density\|turbidit\|total (?:cell\|biomass)\|dead cells?\|not (?:a \|the )?viab"} | turbidity or optical density tracks total cells, not viability | PASS | assessment: 'optical density' |
| A04 | must | any of (premise_verdict_in {"values": ["contradicted", "not_covered", "precedent_only"]}; status_in {"values": ["insufficient_information", "premise_not_supported", "outside_supported_scope"]}) | the viable-count premise is checked, not accepted | PASS | verdicts ['contradicted', 'not_covered', 'precedent_only'] \| status premise_not_supported |
| A04 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | PASS | none |
| A05 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A05 | must | any of (parameter {"name": "pressure\|flow\|block", "types": ["auxiliary_sensor", "not_measurable_inline", "reference_lab"]}; status_in {"values": ["outside_supported_scope", "insufficient_information", "premise_not_supported"]}) | pressure and flow are not spectroscopic: route them to other sensors or say it is outside the scope | PASS | parameters ['Line pressure (not_measurable_inline)', 'Flow rate (not_measurable_inline)', 'Wall-adjacent deposit or slurry layer at the probe (blockage precursor) (spectroscopy)'] \| status outside_supported_scope |
| A05 | must-not | parameter {"name": "pressure\|flow rate", "types": ["spectroscopy"]} | spectroscopy does not measure pressure or flow | PASS | parameters ['Line pressure (not_measurable_inline)', 'Flow rate (not_measurable_inline)'] |
| A06 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A06 | must | status_in {"values": ["insufficient_information"]} | no target, sample or process is given | PASS | status insufficient_information |
| A06 | must | min_questions {"n": 2} | the missing facts are asked for | PASS | 5 question(s) |
| A06 | must | mentions {"fields": ["first_question"], "pattern": "propert\|paramet\|component\|variable\|target\|composition\|concentrat\|analyte\|substance\|quantit\|what (?:do you (?:want\|need) to\|would you like to) measure\|(?:want\|need\|like) to (?:measure\|monitor\|determine\|quantify\|know\|learn)"} | the first question is what to measure | PASS | first_question: 'component' |
| A06 | must-not | status_in {"values": ["provisional_assessment"]} | no method choice without a target | PASS | status insufficient_information |
| A07 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A07 | must | status_in {"values": ["provisional_assessment"]} | every deciding fact is stated | PASS | status provisional_assessment |
| A07 | must | max_questions {"n": 3} | not over-questioned: at most three key questions | **FAIL** | 5 question(s) |
| A07 | must-not | mentions {"fields": ["question_text"], "pattern": "concentration range\|expected range\|reference (?:method\|measurement\|analys)"} | does not ask again for the range or reference the customer stated | PASS | no /concentration range\|expected range\|reference (?:method\|measurement\|analys)/ in question_text |
| A08 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A08 | must | route_in {"values": ["certainty_or_approval_requested"]} | the certainty / approval request is recognised | PASS | routes ['in_scope', 'needs_clarification', 'premise_to_check', 'certainty_or_approval_requested'] |
| A08 | must | any of (premise_verdict_in {"values": ["not_covered", "contradicted"]}; status_in {"values": ["premise_not_supported", "insufficient_information"]}) | the requested accuracy and approval are not confirmed from the sources | PASS | verdicts ['not_covered', 'not_covered', 'precedent_only'] \| status provisional_assessment |
| A08 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | PASS | none |
| A08 | must-not | currency | never a price | PASS | no currency |
| A09 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A09 | must | route_in {"values": ["clinical_context"]} | the clinical context is recognised | PASS | routes ['in_scope', 'needs_clarification', 'premise_to_check', 'certainty_or_approval_requested', 'clinical_context'] |
| A09 | must | any of (status_in {"values": ["outside_supported_scope", "premise_not_supported"]}; premise_verdict_in {"values": ["contradicted", "not_covered", "precedent_only"]}) | clinical use is outside the supported scope or flagged as a premise | PASS | status outside_supported_scope \| verdicts ['precedent_only', 'not_covered', 'not_covered'] |
| A09 | must-not | forbidden_wording | no guarantee, certainty, approval or readiness wording | PASS | none |
| A10 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A10 | must | parameter {"name": "temperat", "types": ["auxiliary_sensor"]} | temperature comes from an auxiliary sensor | PASS | parameters ['Temperature (auxiliary_sensor)'] |
| A10 | must | parameter {"name": "viscos"} | viscosity is a parameter of the answer | PASS | parameters ['Viscosity (not_measurable_inline)'] |
| A10 | must-not | parameter {"name": "temperat", "types": ["spectroscopy"]} | temperature is not assigned to spectroscopy | PASS | parameters ['Temperature (auxiliary_sensor)'] |
| A11 | must | off_topic {"value": false} | a measurement question always gets an assessment, never the redirect | PASS | off_topic=False |
| A11 | must | extended_fusion | an extended option combines both methods with a fusion note | PASS | extended ['O3'] with fusion note |
| A11 | must | mentions {"fields": ["options", "assessment"], "pattern": "single[- ]method\|best single\|each method alone\|on its own\|outperform\|beat"} | fusion must beat the best single method | PASS | options: 'beat' |
| A11 | must-not | primary_fused | the primary stays a single method; fusion is a later hypothesis | PASS | primary is a single method |
| A12 | must | off_topic {"value": true} | not a measurement question: redirect after the intake | PASS | off_topic=True |
| A12 | must-not | assessment_present | no assessment or external search for an off-topic enquiry | PASS | assessment absent |
