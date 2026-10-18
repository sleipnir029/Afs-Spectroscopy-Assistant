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

Outputs `outputs/bakeoff-dev/mix-a/dev`: 8 of 8 case(s) evaluated, 0 not run, 0 unreadable. Mermaid render not checked.

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
| external_secondary | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 7/7 |
| external_replay | PASS | PASS | PASS | PASS | PASS | PASS | PASS | – | 7/7 |
| off_topic_handled | – | – | – | – | – | – | – | – | 0/0 |
| mermaid_renders | – | – | – | – | – | – | – | – | 0/0 |

**Per criterion (passed / applicable item results):** Technical quality (30) 40/40; AFS grounding (20) 30/30; Feasibility plan (15) 16/16; Clarification and uncertainty (15) 24/24; Explainability (10) 16/16; Prototype (10) 8/8

**Checklist failures:**

- none
