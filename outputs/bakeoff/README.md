# 5.8 model bake-off (2026-10-18)

Plan: PHASES.md "5.8 plan" (v2, approved 09:00); deviations D-054, D-056, D-057.
Arms: v4.1-flash baseline (config/models.yaml), glm-5.3-flash, deepseek-v4.1-flash-1017 (config/bakeoff/*.yaml).
Cases: D02, D03, D04 (dev) and A05, A07, A08 (adversarial); `--external cache`; arms in parallel, 3 workers per set.

## Dropped at the first call (schema rejected; plan step 3: no per-model schema rewrites in 5.8)
- **anthropic/claude-haiku-5.5**: every endpoint (Anthropic, Google Vertex, Azure) returned 400 on the intake call: "The compiled grammar is too large, which would cause performance issues. Simplify your tool schemas or reduce the number of strict tools." All 6 cases failed; cost $0.010.
- **openai/gpt-6-luna**: OpenAI and Azure returned 400 on the intake call: "Invalid schema for response_format 'intake': context=('properties', 'optical_regime'), $ref cannot have keywords {'description'}." All 6 cases failed; cost $0.000. (A generic fix would inline $ref targets that carry a description; not done in 5.8.)

## Results
(filled when the runs finish)
