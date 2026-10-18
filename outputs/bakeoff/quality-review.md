# 5.8 quality review, side by side (reviewer agent, 2026-10-18 ~10:00)

**Scope:** D03, A05 and A08. One run per arm, one judge, not blind. Each answer was scored 1–5 on technical correctness, usefulness, questions, honesty and readability, against the knowledge pages and S01 Table 1. Three citations per arm on A08 were spot-checked for whether they support their claim.

| Rank | Arm | Mean | Mean $/case | Mean / max wall time |
|---|---|---|---|---|
| 1 | gemini-3.8-flash | **4.53** | $0.066 (max $0.091) | 159 s / 238 s |
| 2 | mix-a | 4.47 | $0.046 (max $0.135) | 140 s / 425 s |
| 3 | baseline (v4.1-flash) | 3.87 | $0.030 | 763 s / 1254 s (1 runaway) |
| 4 | deepseek-1017 | 3.60 | $0.015 | 257 s / 297 s |
| 5 | mix-b | 3.47 | $0.040 | 93 s / 143 s |
| 6 | glm-5.3-flash | 3.33 | $0.006 | 332 s / 777 s |
| 7 | gemini-3.5-flash-lite | 2.67 | $0.020 | 34 s / 45 s |

## Serious defects
- **gemini-3.5-flash-lite, D03:** invented a customer premise and changed the decision status because of it.
- **glm-5.3-flash:** in A05 it gets the fluorescence physics backwards (it says fluorescence swamps MIR). In D03 it says Raman "tolerates scattering", which no source says.
- **mix-b and flash-lite, A08:** propose Raman for moisture because of its "low water absorbance", which is backwards.
- **baseline:** too slow for a live demo.

## A05 primary-method split
NIR diffuse reflection is right (Table 1 row 8: scattering media, average cost). MIR-ATR as the primary method is wrong: it sees 1–6 µm at a crystal in an abrasive stream, and it is high cost. Raman is the weakest choice.

## Pipeline issues seen in every arm (generic, need a plan)
1. "Best current option: O1" appears while O2 carries the "Recommended" tier label. The renderer, or the tier naming, must make the two agree.
2. Screening marks NIR diffuse reflection "not recommended" for a liquid whose turbidity varies, although S01 p.18 keeps both techniques. Proposed fix: demote it to "conditional" when scattering varies.
3. Smaller issues: duplicated step and reason text (GLM); uncited general knowledge (Kjeldahl, ICH Q2) in gemini-3.8-flash.

## Recommendation
Use gemini-3.8-flash for every role: best quality, no serious defects, about $0.07 per case, 2.5 minutes mean and 4 minutes worst case. mix-a is the cheaper fallback, but only after re-running its slow case to bound the tail.
