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

Outputs `outputs/bakeoff/glm-5.3-flash/dev`: 3 of 8 case(s) evaluated, 5 not run, 0 unreadable. Mermaid render not checked.

| Item | D01 | D02 | D03 | D04 | D05 | D06 | D07 | D08 | Pass |
|---|---|---|---|---|---|---|---|---|---|
| structured_output | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| sections_present | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| citations_verified | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_open_failures | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_flagged_figures | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_currency | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| no_certainty_wording | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| cost_class_table1 | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| options_rules | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| proposal_rules | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| feasibility_plan | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| premise_flags | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| questions_present | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| questions_tied_to_options | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| answer_length | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| external_secondary | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| external_replay | not run | PASS | PASS | PASS | not run | not run | not run | not run | 3/3 |
| off_topic_handled | not run | – | – | – | not run | not run | not run | not run | 0/0 |
| mermaid_renders | not run | – | – | – | not run | not run | not run | not run | 0/0 |

**Per criterion (passed / applicable item results):** Technical quality (30) 15/15; AFS grounding (20) 12/12; Feasibility plan (15) 6/6; Clarification and uncertainty (15) 9/9; Explainability (10) 6/6; Prototype (10) 3/3

**Checklist failures:**

- none

**Not run / unreadable:** D01 (missing D01.json, D01.md); D05 (missing D05.json, D05.md); D06 (missing D06.json, D06.md); D07 (missing D07.json, D07.md); D08 (missing D08.json, D08.md)
