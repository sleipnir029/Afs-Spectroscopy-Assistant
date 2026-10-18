# Model research for the final frozen run (task 5.8)

Written 2026-10-18 08:50 CEST. Research only: no paid LLM calls were made. All prices and parameters come from live OpenRouter data read on 2026-10-18 between 08:41 and 08:49 CEST. Prices change, and several providers show temporary discounts.

## 1. Question and constraints

Question: which OpenRouter model should the pipeline use for the final frozen run?

Constraints, from `config/models.yaml`, `src/afs_assistant/llm.py`, DEVIATIONS D-053/D-053a/D-053b and the user's budget:

- Strict `response_format: json_schema` must work. `llm.py` always sends `strict: true` with `provider.require_parameters: true`, and always sends `temperature`.
- A `reasoning` control is needed: `external_*` roles send `reasoning: {effort: low}`.
- Output headroom: assess needs at least 64k max completion tokens (hidden reasoning plus JSON). 32k already truncated replies (D-025).
- Context of at least 128k. The largest single call seen is ~50k prompt tokens (repair).
- Budget: about $0.15 or less per run, where one run is one case.
- Main problem to solve: v4.1-flash produces runaway, looping replies on four providers. In committed runs, 13 of about 111 assess calls were discarded at max_tokens (32k or 64k), plus 2 intake discards and 1 assess timeout. Runs take 5–20 minutes.

### Our schema (it decides strict-mode compatibility)

I measured this from `afs_assistant.schema` passed through `llm.strict_schema`.

- Keywords used: `$defs`/`$ref`, `anyOf` (nullable fields), string `enum`, `additionalProperties: false`, and every property required.
- Keywords not used: `maxItems`, `minItems`, `pattern`, numeric bounds, recursion.
- `Assessment` has 7 `anyOf` nodes and `Intake` has 4, with each `$defs` entry counted once.
- `Assessment` has content fields named `why`, `explanation`, `rationale` and `status_reason`.

### Measured token profile (v4.1-flash, 51 full runs in `runs/*/calls.json`)

| Role | Prompt tokens (median / max) | Completion tokens (median / max) | Latency median |
|---|---|---|---|
| intake | 934 / 2,366 | 9,851 / 13,678 | 70 s |
| assess | 42,352 / 46,157 | 29,597 / 63,209 (plus 13 discards at 32k/64k) | 231 s |
| repair | 47,948 / 49,930 | 6,536 / 33,079 | 41 s |
| external_queries | 513 / 631 | 1,231 / 3,241 | 13 s |
| external_evidence | 2,895 / 3,492 | 4,302 / 19,079 | 40 s |

Per case, median: prompt 95.3k tokens, of which 83.6k were served from cache (88%); completion 63.7k; cost $0.030 (max $0.156); summed latency 491 s (max 1,304 s). Completion is mostly hidden reasoning, so a model that reasons less is both cheaper and faster.

## 2. Method

- `GET https://openrouter.ai/api/v1/models` (keyless) returned 471 models. I filtered to models whose `supported_parameters` include both `structured_outputs` and `reasoning`, with context ≥ 128k.
- `GET https://openrouter.ai/api/v1/models/<id>/endpoints` for 24 candidates gave per-provider price, cache price, max completion tokens, quantization, `supported_parameters` and 1-day uptime. Raw JSON is in the session scratchpad and is not committed.
- The API returns `throughput_last_30m` and `latency_last_30m` as null. I read throughput, latency and the "structured output error rate" from the rendered OpenRouter model pages in a headless browser.
- Quality signals:
  - Artificial Analysis (AA) Intelligence Index and verbosity, i.e. output tokens AA used to run its index, which is a proxy for how much a model reasons.
  - OpenRouter "AutoExacto" GPQA Diamond / TAU-Bench, measured per provider.
- Docs: OpenRouter structured outputs, reasoning tokens, prompt caching, provider routing and streaming; Anthropic structured-outputs limits and models overview; OpenAI structured-outputs supported schemas.
- Known-issue search: Google AI dev forum, OpenAI community, GitHub and web search.

### Estimate formulas

- Cost per case = 11.7k uncached input × input price + 83.6k cached input × cache price (scaled by the model's realistic cache-hit rate) + O × output price.
- O = 40k / 64k / 100k completion tokens: a model that reasons less, our median, and a bad case with one runaway.
- Wall time per case ≈ 491 s × (68 / provider tok/s) × (O / 64k). The constant 491 s is anchored to our measured median on DeepInfra, whose OpenRouter p50 is 68 tok/s.
- These are rough estimates. Tokenizers differ: Anthropic's current tokenizer counts about 30% more tokens than Haiku 4.5's (VKTR), so treat the Haiku figures as +30%.

## 3. Candidate table

Prices are USD per 1M tokens: standard tier, cheapest endpoint that is strict-JSON capable and not fp4, unless noted. "Temp" means the endpoint accepts `temperature`. Our code always sends it and requires it (`require_parameters: true`).

| Model id | $/M in | $/M out | Cache read | Ctx | Max out | Strict JSON | Temp | Reasoning control | Providers (quant) | tok/s (OR p50) | Est. $/case (40k/64k/100k out) | Est. wall/case at 64k |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **deepseek/deepseek-v4.1-flash** (baseline) | 0.14 (30% off; list 0.20) | 0.42 (list 0.60) | 0.0042 | 1.05M | 131k on DeepInfra | y (28 of 34 endpoints) | y | effort | DeepInfra fp8, AtlasCloud fp8, CoreWeave fp8; 34 endpoints | DeepInfra 68, AtlasCloud 50, CoreWeave 221 | 0.019 / 0.029 / 0.044 (list 0.027 / 0.041 / 0.063) | 491 s (measured) |
| deepseek/deepseek-v4.1-flash-1017 (Baseten not usable: its endpoint lists no structured_outputs/response_format, reviewer check 08:53) | 0.098 (51% off; list 0.20) | 0.294 (list 0.60) | 0.0029 | 1.05M | 131k (DeepInfra), 943k (Fireworks/Parasail) | y (9 of 11) | y | effort | DeepInfra fp8, DeepSeek (first party, peak-hour prices 2×), Baseten/Fireworks/Parasail at 0.30/1.20 | DeepInfra 105, Baseten 296, Fireworks 153, DeepSeek 51 | 0.013 / 0.020 / 0.031 (DeepInfra); 0.052 / 0.081 / 0.124 (Baseten/Fireworks) | ~320 s (DeepInfra), ~220 s (Fireworks) |
| deepseek/deepseek-v4-pro-0813 | 0.133 (Baidu); 1.31 (others) | 0.40 (Baidu); 3.96 (others) | 0.0042 | 1.02M | 393k | y | y | effort | Baidu fp8 cheap but without penalty params; CoreWeave/Parasail/AtlasCloud fp8 at 10× | ~85 | 0.018 / 0.027 / 0.042 (Baidu only); 0.18 / 0.27 / 0.42 (others) | ~390 s |
| **anthropic/claude-haiku-5.5** | 0.10 (0.50 above 100k prompt) | 0.50 (2.50 above 100k) | 0.01 (write 0.125) | 1M | 128k | y on Anthropic, Vertex, Azure; **n on Bedrock / Claude Platform on AWS** | **n** | effort (low…max, adaptive) | Anthropic, Google Vertex, Azure | 166–171 (Vertex) | 0.029 / 0.042 / 0.059 without cache_control; about +30% for the tokenizer | ~200 s |
| **openai/gpt-6-luna** | 0.10 (flex 0.05; priority 0.20) | 0.50 (flex 0.25; priority 1.00) | 0.01 | 1.05M | 128k | y | **n** | effort (none…max) | OpenAI, Azure, Bedrock | OpenAI 69, OpenAI priority 112, Bedrock 80 | 0.024 / 0.036 / 0.054 (std); 0.048 / 0.072 / 0.108 (priority) | ~480 s std, ~300 s priority |
| **z-ai/glm-5.3-flash** | 0.15 (fp8: Baseten, Inceptron 0.10) | 0.50 (Inceptron 0.69) | 0.03 | 1.05M | 131k (Baseten), 943k (others) | y (29 of 35) | y | effort | 35 endpoints. fp8: Baseten, Inceptron, StreamLake, Near AI, Morph. Unknown quant: Together, Fireworks, Friendli | Baseten 142–160, Inceptron 110, Together 165, Friendli 207, Z.ai 43 | 0.024 / 0.036 / 0.054 | ~270 s |
| google/gemini-3.5-flash-lite | 0.30 (flex 0.15) | 2.50 (flex 1.25) | 0.03 | 1.05M | **65.5k** | y | AI Studio y, Vertex n | effort maps to thinkingLevel | Google only | 206–245 | 0.12 / 0.18 / 0.27 | ~150 s |
| google/gemini-3.8-flash | 0.75 (flex 0.375) | 3.75 (flex 1.875) | 0.075 | 1.05M | **65.5k** | y | AI Studio y, Vertex n | effort maps to thinkingLevel | Google only | 94–112 | 0.20 / 0.29 / 0.42 (over budget except flex) | ~320 s |
| qwen/qwen3.8-flash | 0.15 | 0.47 | 0.016 | 1M | 131k | y | y | `reasoning` only (no `reasoning_effort` listed) | Alibaba only | 44–52 | 0.022 / 0.034 / 0.050 | ~700 s |
| xiaomi/mimo-v2.6-flash | 0.133 | 0.266 | 0.0027 | 1.05M | 131k (943k DeepInfra) | y | y | `reasoning` only | DeepInfra fp8, Xiaomi fp8, Makora fp8 and others | 28–71 | 0.012 / 0.019 / 0.028 | ~560 s |
| minimax/minimax-m3 | 0.30 | 1.20 | 0.06 | 1.05M | 472k+ | y on only 3 of 14 endpoints | y | `reasoning` only | CoreWeave fp4, Together, ModelRun fp8 | 98–119 | 0.057 / 0.086 / 0.129 | ~330 s |
| mistralai/mistral-small-2603 | 0.15 | 0.60 | 0.015 | 262k | 210k | y | y | effort | Mistral only | 115–132 | ~0.03 | ~260 s |

Quality and reliability signals for the same models:

| Model | AA Intelligence Index | AA verbosity (output tokens to run index; median of class) | OR GPQA / TAU (range across providers) | OR structured-output error rate (3 lowest providers shown) |
|---|---|---|---|---|
| v4.1-flash | 39 (max) | 250M (median 130M), "very verbose" | 90.1–91.0% / 76.2–77.9% | 0.62–0.76% |
| v4.1-flash-1017 | not listed | not listed | 89.7–90.7% / 76.7–79.3% | 0.97–1.61% |
| v4-pro-0813 | 36 (max) | not read | 90.1–92.1% / 78.0–80.7% | 1.85–3.65% |
| claude-haiku-5.5 | **43** (max) | **440M** at max (median 96M) | 86.4–87.6% / 73.7–76.1% | **2.18–3.24%** |
| gpt-6-luna | 38 (max) | **140M** at max (median 96M) | 87.1–88.4% / 65.3–68.6% | 0.50–0.84% |
| glm-5.3-flash | **42** | 180M (median 130M) | 82.4–88.9% / 76.1–78.0% | 0.46–0.72% |
| gemini-3.5-flash-lite | 22 | not read | 82.7–85.4% / 73.3–79.3% | 0.08–0.25% |
| gemini-3.8-flash | 41 (high) | 170M (median 85M) | 94.7–95.6% / 71.3–78.0% | 0.43–0.55% |
| qwen3.8-flash | ~40 ("Qwen3.8-Flash-Next"; not the same id, unverified) | not read | 88.6–89.8% / 70.0–71.3% | 2.51–2.62% |
| mimo-v2.6-flash | 38 | 240M | 75.5–85.3% / 75.1–78.6% | 0.20–4.04% |
| minimax-m3 | 29 | not read | 91.3–93.3% / 76.5–78.0% | 1.01–4.18% |
| mistral-small-2603 | 11 | not read | 74.6–75.3% / 40–44% | 0.14–0.55% |

Excluded on price: Kimi K3 (output ≥ $8/M), Grok 4.3 ($2.50/M output; ~$0.19 per case at 64k), and GLM-5.3 non-flash (output ≥ $1.5–4.8/M). Bigger tiers (Claude Sonnet 5.5, GPT-6 Sol, Gemini Pro) are $10+/M output and far over budget.

## 4. Known issues per candidate

**deepseek/deepseek-v4.1-flash (baseline)**

- Our own evidence (D-053a, D-053b): runaway replies to max_tokens on DeepInfra, Together, Parasail and AtlasCloud. Examples: assess at 64,000 tokens, intake at 16,000, and an enum value repeated 1,427×.
- I found no public report of this loop. A web search found only a third-party note that some hosts treat its JSON as soft rather than strict (LLM Gateway), and Sarvam's note that reasoning can consume all of max_tokens and return `content: null`.
- AA calls it "very verbose" (250M tokens against a 130M median). That fits our 23–64k assess completions.

**deepseek/deepseek-v4.1-flash-1017**

- A one-day-old snapshot, listed 2026-10-17, "served by DeepSeek under the `deepseek-flash` API model name".
- I found no release notes, so it is unknown whether the loop behaviour changed. Its structured-output error rate (0.97–1.61%) is no better than the baseline's.
- DeepSeek's own endpoint has peak-hour prices on weekdays (2× during UTC 01:00–04:00 and 06:00–10:00). DeepInfra's 51% discount may be temporary.

**deepseek/deepseek-v4-pro-0813**

- Cheap only on Baidu, a single provider without `frequency_penalty`/`repetition_penalty`. Elsewhere it is about 10× and over budget.
- AA index 36 is below V4.1 Flash, and its structured-output error rate is the highest of the DeepSeek models (1.85–3.65%). Not worth the integration risk.

**anthropic/claude-haiku-5.5**

- **It rejects non-default `temperature`.** OpenRouter lists no `temperature` on any of its endpoints, and VKTR reports that "non-default temperature, top_p, or top_k values return an error". Because `llm.py` always sends `temperature` with `require_parameters: true`, OpenRouter would find no endpoint. **This needs a generic code change** (omit temperature for such models) before any test. It also removes the deterministic setting and has no `seed`.
- Structured outputs are not supported on Bedrock or Claude Platform on AWS (OpenRouter endpoint data; Anthropic docs). Routing must be limited to `anthropic`, `google-vertex` and `azure`.
- Anthropic's schema limits:
  - At most 16 parameters with union types and 24 optional parameters across the request.
  - A "Schema is too complex for compilation" 400 error, and a 180 s compilation timeout.
  - Our Assessment has 7 `anyOf` nodes counted per `$defs` entry. **It is unverified whether Anthropic counts each `$ref` use separately.** If it does, Assessment may exceed 16. One intake/assess smoke call will show this immediately (a 400 error, not a cost).
- A property that asks for the model's reasoning may trigger a `reasoning_extraction` refusal. Our `rationale`/`why` fields are content, not chain-of-thought, so the risk is low but untested.
- Refusals (`stop_reason: refusal`) may not match the schema.
- AA verbosity at max effort is the highest in the table (440M). Use effort `low` or `medium` (default `medium`).
- Its OpenRouter structured-output error rate (2.2–3.2%) is the worst of the shortlist.
- Prompt caching needs `cache_control`, which we do not send. Without it there is no cache discount, and the estimate above already assumes none.
- Tokenizer is about +30% tokens against Haiku 4.5. The per-call prompt stays far below the 100k price step (our maximum is ~50k, ~65k after +30%).

**openai/gpt-6-luna**

- **It does not accept `temperature`** (absent from all 7 endpoints), so it needs the same code change as Haiku. It does accept `seed`.
- Strict mode supports all our keywords and also `maxItems` and recursion. Limits are 5,000 properties, 10 nesting levels and 1,000 enum values (OpenAI docs). The root must be an object, not `anyOf`; ours is an object.
- Slowest of the shortlist on the standard tier (69 tok/s). Priority ("OpenAI Fast") is 112 tok/s at 2× price.
- Third-party benchmark write-ups conflict, and BenchLM says the model is not yet publicly ranked (search summary). TAU-Bench is clearly lower than the others (65–69%).
- I found no Luna-specific loop reports. OpenAI community threads report structured outputs repeating the same object in GPT-family models, and lowering temperature did not stop it.

**z-ai/glm-5.3-flash**

- I found no public loop or structured-output reports (search returned nothing specific). Absence of reports is not evidence of absence.
- AutoExacto GPQA varies by provider (82.4–88.9%), which suggests serving or quantization differences. Restrict routing to named fp8/bf16 endpoints: Baseten fp8 (142–160 tok/s), Inceptron fp8 (110 tok/s), with Together/Fireworks (quantization unknown) only as fallback. D-053a saw runaways on Together, though D-053b later attributed them to the model.
- Z.ai's own endpoint is slow (43 tok/s, 4.6 s latency).
- Drop-in: it supports `temperature`, `frequency_penalty`, `repetition_penalty` and effort.

**Gemini Flash family (3.5 Flash-Lite, 3.8 Flash)**

- Documented schema-constrained loops in the Flash line:
  - Gemini 2.5 Flash: repeating until max tokens in structured output, ~30% of requests in one report.
  - Gemini 3.7 Flash, 2026-08-17: digits repeating in an integer field until the cap, ~1 in 3 runs on the repro. "`temperature: 0` does NOT avoid it", retries "re-entered the loop on the same content", maxItems was set in the schema, and there is no Google response.
  - A Vertex report of a loop inside a JSON number literal.
- I did not verify these for 3.8 or 3.5 Flash-Lite.
- Max output is 65,536, at our assess ceiling. 3.8 Flash is over budget at standard prices. 3.5 Flash-Lite is weak (AA 22).

**Others**

- Qwen3.8 Flash: Alibaba is the only provider; 44–52 tok/s; 2.5% structured-output errors; tool-call errors of 2.4–7.6%.
- MiMo-V2.6-Flash: slow (28–71 tok/s), verbose (240M), and provider-dependent errors up to 4%.
- MiniMax-M3: only 3 strict endpoints, one of them fp4, and up to 4.2% errors.
- Mistral Small 4: weak (AA 11, TAU 40–44%).

## 5. Generic mitigations

These apply whatever model is chosen. They are ordered by how directly they address the runaway problem.

1. **Streaming with a repetition guard, then abort.** OpenRouter: "Streaming requests can be cancelled by aborting the connection. For supported providers, this immediately stops model processing and billing." The supported list includes DeepInfra, Together, Fireworks, OpenAI, Azure, Anthropic, Cloudflare and DeepSeek. Not supported: Bedrock, Google and Mistral, among others. A guard that detects the same n-gram or JSON value repeated N times, aborts, and retries once would turn a 64k-token, 5-minute failure into a few seconds.
   - Limits: OpenRouter "Response Healing" only applies to non-streaming requests. With hidden reasoning, the visible stream may be empty for a long time, so the guard must also watch `reasoning` deltas where the provider streams them.
   - This is a code change and needs a DEVIATIONS entry.
2. **Lower reasoning effort on assess/intake.** OpenRouter maps `effort` to roughly a share of max_tokens: `low` about 20%, `medium` about 50%. Reasoning tokens "are considered output tokens and charged accordingly". This cuts cost and time for every candidate. Its quality effect must be measured. Secondary reports put Haiku 5.5's Terminal-Bench at 39.2% at max effort and about 20% at medium (aiweekly.co summary of The Decoder and VentureBeat; search summary only, https://aiweekly.co/alerts/introducing-claude-haiku-55).
3. **Raise intake max_tokens to ~32k.** Intake median completion is already 9.9k, max 13.7k, with 2 discards at 16k. This only helps if the truncations were legitimate long reasoning. A loop will still run to the cap, now at 2× cost. Pair it with mitigation 1.
4. **`maxItems` on arrays.** OpenAI strict supports it. Anthropic does not support array constraints beyond `minItems` of 0 or 1 (a 400 error). Open-weight hosts vary. The Gemini 3.7 loop report had maxItems set and still looped, inside a scalar. It bounds array-level loops like our 1,427× enum repeat, but not loops inside strings or reasoning.
5. **`frequency_penalty` / `repetition_penalty`.** Most DeepSeek/GLM endpoints support them; OpenAI, Anthropic and Gemini do not on OpenRouter. With strict JSON they are risky: JSON's repeated structural tokens and field names absorb most of the penalty (a single-author DEV post, not measured). `repetition_penalty` also counts prompt tokens (NVIDIA NIM docs). Only consider a small `frequency_penalty` (≤ 0.2), and only after a measured test.
6. **Provider pinning with `quantizations: ["fp8","bf16"]`** avoids fp4 serving differences (OpenRouter provider-routing docs). D-053b showed this does not fix v4.1-flash's loops.

## 6. Shortlist

`openai/gpt-6-luna-pro` (same $0.10/$0.50) is excluded: the same model in a pro mode that spends far more tokens. `nvidia/nemotron-3.5-super-vl` was fetched but not assessed.

| Rank | Model | Why it fits our constraints | Main risk |
|---|---|---|---|
| 1 | **z-ai/glm-5.3-flash** (Baseten fp8, then Inceptron fp8) | Drop-in: supports temperature 0, strict JSON, effort and penalties, so no code change. AA 42 against 39 for the baseline. Low structured-output error (0.46–0.72%). ~110–160 tok/s on fp8, about 2× DeepInfra v4.1-flash. ~$0.036 per case at our median, ~$0.054 in a bad case, well under $0.15. | No public evidence on loops either way. Quality varies by provider, so pin fp8. |
| 2 | **anthropic/claude-haiku-5.5** (Anthropic / Vertex / Azure, effort low or medium) | Highest AA index of the affordable models (43). Fastest (166–171 tok/s), so ~3–4 min per case. 128k output. ~$0.04–0.08 per case including the tokenizer uplift. A different model family from DeepSeek, so the loops are unlikely to be shared. | Needs the generic "omit temperature" code change. Highest structured-output error rate (2.2–3.2%). Anthropic union-type complexity limit unverified for Assessment. Verbose at high effort. |
| 3 | **openai/gpt-6-luna** (OpenAI standard, effort medium) | Cheapest frontier-lab model ($0.10/$0.50). Least verbose (140M), so it likely reasons less. Low structured-output error (0.5–0.8%). The fullest strict-schema support, including maxItems, and accepts `seed`. | Needs the same temperature change. Slow on the standard tier (69 tok/s, about the same as now); priority doubles the price. Lowest TAU-Bench (65–69%). |
| ref | deepseek/deepseek-v4.1-flash (current) | Known quality on our eval. ~$0.03 per case. | Runaway replies (~12% of assess calls discarded). Slow. |
| optional | deepseek/deepseek-v4.1-flash-1017 | Zero-cost switch (same family, drop-in), cheaper on DeepInfra right now, and 105 tok/s. | No release notes; likely the same loop behaviour. Include only as a cheap control. |

Gemini was left out of the shortlist: the 65.5k output cap, documented schema-constrained loops in the Flash line, and 3.8 Flash's price.

## 7. Proposed bake-off

**Arms**

- Run GLM-5.3-Flash, Haiku 5.5 and GPT-6 Luna, plus v4.1-flash-1017 if the user wants a cheap control.
- Reuse the committed v4.1-flash baseline runs for the same cases (no re-spend). Re-run baseline only if the prompts changed since those runs.

**Cases (6)**

- Dev: **D03** (looped twice at 64k), **D04** (looped on Parasail/Together; the usual smoke case), **D02** (a typical case).
- Adversarial: **A07** (assess loop, a timeout, and a $0.153 run), **A08** (assess discarded at 64k; 146k completion tokens), **A05** (highest completion of the other A cases, 81.8k).

**Before the bake-off**

- Make the generic code change: omit `temperature` for models that do not list it. Log it in DEVIATIONS.
- Add per-model `provider_routing` and fallback price rows in `config/models.yaml`.
- Make one intake call and one assess call per new model on D04 to catch schema rejection (Anthropic complexity limit, OpenAI strict-subset errors) before a full run. About $0.01–0.03 each.

**Measures per run**

All are already produced by the pipeline and eval:

- cost (OpenRouter `usage.cost`), wall time, and per-role latency;
- eval checklist pass count, citation verification result, and hard failures (failed case, invalid JSON after retries, schema 400);
- **runaway replies**: count of `*:discarded` at max_tokens and timeouts;
- completion tokens per role, to compare reasoning volume.

**Decision rule (proposal)**

Pick the model with zero hard failures and zero runaway replies on the 6 cases, and eval and citation results at least equal to the baseline. Break ties on wall time, then cost.

If no model is clean, keep v4.1-flash and add the streaming repetition guard (mitigation 1).

**Spend estimate**

| Item | Calculation | Cost |
|---|---|---|
| GLM-5.3-Flash | 6 cases × $0.036–0.054 | $0.22–0.32 |
| Haiku 5.5 | 6 cases × $0.055–0.077 (with +30% tokenizer) | $0.33–0.46 |
| GPT-6 Luna (standard) | 6 cases × $0.036–0.054 | $0.22–0.32 |
| Smoke calls | | ~$0.10 |
| Subtotal | | **~$0.9–1.2** |
| Optional v4.1-flash-1017 control | 6 cases × $0.020–0.031 | +$0.12–0.19 |
| Optional repeat of D03/A07/A08 for the top 2 models (loops are stochastic) | | +$0.25–0.40 |
| **Worst case, everything included** | | **~$1.8**, inside the $10 session cap |

A runaway is capped by max_tokens: a 64k assess loop costs about $0.03 on GLM/Luna and about $0.04 on Haiku.

Wall time: about 18–24 runs at 3–8 minutes each. Arms use different providers, so they can run in parallel (about 30–60 minutes) if spend tracking stays per run.

## 8. Open questions and uncertainty

- **Loop behaviour on our prompts is unknown for every candidate.** No public source tests long strict-JSON technical outputs like ours. The bake-off is the only real evidence, and 6 cases is a small sample: a 12% runaway rate can produce zero runaways in 6 runs about 46% of the time. Repeating the loop-prone cases helps.
- Quality evidence is generic. AA Intelligence Index, GPQA and TAU-Bench measure reasoning and agentic tasks, not cited spectroscopy assessments. No IFBench or AA-Omniscience number was retrievable for the candidates; the pages showed no per-model values. Our own eval is the deciding signal.
- Haiku 5.5 and GPT-6 Luna cannot run at temperature 0, so reruns will vary. Is that acceptable for a "frozen" run? The final outputs are generated once and stored, so it probably is, but this is the user's call.
- Unverified: whether Anthropic counts `$ref` re-uses toward the 16 union-type limit; whether DeepInfra's 51% (1017) and 30% (v4.1-flash) discounts last until tonight; whether v4.1-flash-1017 changes loop behaviour.
- The OpenRouter p50 throughput (68 tok/s on DeepInfra) is lower than the effective rate our runs imply (~130 completion tokens/s summed over calls). The wall-time estimates are therefore relative rankings, not promises.
- Cache-hit rates for Gemini, OpenAI and Anthropic on our prompts are assumed (0–75%), not measured. Haiku gets no cache discount unless we add `cache_control` (another code change).
- Any model change after the H outputs exist must stay generic and be logged (CLAUDE.md). This research did not look at `scenarios/final.jsonl`.

## Sources

All accessed 2026-10-18 between 08:41 and 08:49 CEST.

1. OpenRouter models API: https://openrouter.ai/api/v1/models (prices, supported_parameters, context, max completion, pricing overrides such as Haiku's 100k tier and DeepSeek-1017's peak hours).
2. OpenRouter endpoints API, per model: `https://openrouter.ai/api/v1/models/<id>/endpoints` for deepseek/deepseek-v4.1-flash, deepseek/deepseek-v4.1-flash-1017, deepseek/deepseek-v4-pro(-0813), deepseek/deepseek-v4-flash-0731, anthropic/claude-haiku-5.5, openai/gpt-6-luna, openai/gpt-5.6-luna, google/gemini-3.5-flash-lite, google/gemini-3.1-flash-lite, google/gemini-3.8-flash, qwen/qwen3.8-flash, qwen/qwen3.7-plus, z-ai/glm-5.3-flash, z-ai/glm-5.3, minimax/minimax-m3, mistralai/mistral-small-2603, mistralai/mistral-large-4-0, xiaomi/mimo-v2.6-flash, xiaomi/mimo-v2.6-pro, x-ai/grok-4.3, nvidia/nemotron-3.5-super-vl, tencent/hy3, moonshotai/kimi-k3 (per-provider price, quantization, max out, temperature/penalty support, uptime).
3. OpenRouter model pages (throughput, latency, AutoExacto GPQA/TAU, structured-output error rate): https://openrouter.ai/deepseek/deepseek-v4.1-flash, https://openrouter.ai/deepseek/deepseek-v4.1-flash-1017, https://openrouter.ai/deepseek/deepseek-v4-pro-0813, https://openrouter.ai/anthropic/claude-haiku-5.5, https://openrouter.ai/openai/gpt-6-luna, https://openrouter.ai/google/gemini-3.5-flash-lite, https://openrouter.ai/google/gemini-3.8-flash, https://openrouter.ai/qwen/qwen3.8-flash, https://openrouter.ai/z-ai/glm-5.3-flash, https://openrouter.ai/xiaomi/mimo-v2.6-flash, https://openrouter.ai/minimax/minimax-m3, https://openrouter.ai/mistralai/mistral-small-2603, https://openrouter.ai/tencent/hy3.
4. OpenRouter docs, structured outputs: https://openrouter.ai/docs/features/structured-outputs ("Support is determined per endpoint"; "exact compliance is not guaranteed on every endpoint").
5. OpenRouter docs, reasoning tokens: https://openrouter.ai/docs/use-cases/reasoning-tokens (effort shares; "Reasoning tokens are considered output tokens and charged accordingly").
6. OpenRouter docs, prompt caching: https://openrouter.ai/docs/features/prompt-caching (OpenAI and DeepSeek automatic; Anthropic needs `cache_control`; Gemini implicit).
7. OpenRouter docs, provider routing: https://openrouter.ai/docs/features/provider-routing (`require_parameters`, `quantizations`, `sort`, `max_price`).
8. OpenRouter docs, streaming and cancellation: https://openrouter.ai/docs/api/reference/streaming ("For supported providers, this immediately stops model processing and billing").
9. Anthropic structured outputs (schema limits, complexity limits, invalid outputs): https://platform.claude.com/docs/en/build-with-claude/structured-outputs
10. Anthropic models overview (Haiku 5.5 id, adaptive thinking, default effort medium, 128K output): https://platform.claude.com/docs/en/about-claude/models/overview
11. OpenAI structured outputs, supported schemas: https://developers.openai.com/api/docs/guides/structured-outputs
12. VKTR, "Anthropic cuts small-model pricing … Claude Haiku 5.5" (2026-10-07; tokenizer about +30%; non-default temperature errors): https://www.vktr.com/ai-platforms/anthropic-cuts-smallmodel-pricing-90-with-claude-haiku-55/
13. Artificial Analysis leaderboard: https://artificialanalysis.ai/leaderboards/models. Model pages: https://artificialanalysis.ai/models/claude-haiku-5-5, https://artificialanalysis.ai/models/gpt-6-luna, https://artificialanalysis.ai/models/deepseek-v4-1-flash, https://artificialanalysis.ai/models/glm-5-3-flash, https://artificialanalysis.ai/models/gemini-3-8-flash, https://artificialanalysis.ai/models/mimo-v2-6-flash
14. Google AI dev forum, Gemini 3.7 Flash schema-constrained loop (2026-08-17): https://discuss.ai.google.dev/t/gemini-3-7-flash-schema-constrained-json-output-degenerates-into-repeated-0-until-maxoutputtokens-regression-vs-gemini-3-flash-preview/178681
15. Google AI dev forum, Gemini 2.5 Flash repeats tokens in structured output: https://discuss.ai.google.dev/t/gemini-2-5-flash-repeats-tokens-until-max-tokens-reached-in-structured-output/107176 and https://discuss.ai.google.dev/t/structured-output-repetition-loop-inside-a-json-number-literal-runs-to-max-tokens-flash-vertex/175138 (search summaries only, not opened).
16. OpenAI community, structured outputs repeating objects: https://community.openai.com/t/issue-with-structured-outputs-model-generates-repetitive-concatenated-json-objects-instead-of-a-single-response/1368498 (search summary only, not opened).
17. DEV Community, "Why repetition penalty breaks JSON and code generation": https://dev.to/ji_ai/why-repetition-penalty-breaks-json-and-code-generation-4bbk (search summary only; one author, not measured).
18. NVIDIA NIM sampling parameters (repetition_penalty covers prompt and output): https://docs.nvidia.com/nim/vision-language-models/1.7.0/sampling-params.html (search summary only).
19. Sarvam docs, DeepSeek V4.1 Flash (reasoning can consume max_tokens and return null content): https://docs.sarvam.ai/api/getting-started/models/openweight/deepseek-v4.1-flash (search summary only).
20. LLM Gateway, DeepSeek V4.1 Flash (soft vs strict JSON on its upstream): https://llmgateway.io/models/deepseek-v4-1-flash (search summary only).
21. GPT-6 Luna third-party guides (effort levels none…max; AA index about 38): https://codersera.com/blog/gpt-6-luna-complete-guide-2026/, https://benchlm.ai/models/jevbench-gpt-6-luna (search summaries only; conflicting figures).
22. Internal evidence: `runs/*/calls.json` (51 full runs, measured 2026-10-18 08:45), DEVIATIONS.md D-025, D-053, D-053a, D-053b, `config/models.yaml`, `src/afs_assistant/llm.py`, `src/afs_assistant/schema.py`.

## 9. Combining models (added 2026-10-18 09:30, user: "combining data from different models so we can make better results at cheaper costs")

Known approaches:

- **Cascades (FrugalGPT).** Send each query to a cheap model first. A scorer judges the answer. Only answers that fail go to a dearer model. The paper reports matching the best single model's quality at a large cost reduction on its benchmarks. Chen, Zaharia, Zou, "FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance", arXiv:2305.05176, https://arxiv.org/abs/2305.05176.
- **Routers (RouteLLM).** A learned router picks the strong or weak model per query before answering. Ong et al., "RouteLLM: Learning to Route LLMs with Preference Data", arXiv:2406.18665, https://arxiv.org/abs/2406.18665.
- **Mixture-of-Agents.** Several models answer, then an aggregator model merges the answers. This raises quality on chat benchmarks, but every query pays for all the models plus the aggregator. Wang et al., "Mixture-of-Agents Enhances Large Language Model Capabilities", arXiv:2406.04692, https://arxiv.org/abs/2406.04692.

How this maps onto our pipeline:

- Our pipeline already has the scorer a cascade needs: the deterministic verifier. It checks quotes verbatim on the cited page, the scope, numbers and rules, and records hard failures. This is stronger than FrugalGPT's learned scorer, because a failure is a checked fact, not a prediction.

| # | Combination | How | Cost effect | Code |
|---|---|---|---|---|
| C1 | **Per-role models** | A fast, cheap model for intake and the two external roles (short structured jobs); the best-value model for assess. | Pays for strength only where the long reasoning happens. | None (roles already name their own model). |
| C2 | **Escalating repair (cascade)** | Assess on the cheap model. Only when the verifier finds hard failures does the repair call go to a different, stronger model. It sees the failed checks and fixes them. | The dearer model runs only on failing cases (about 0–1 repair calls per case today). | None (the repair role names its own model). |
| C3 | **Cross-model retry on a runaway** | When a reply is discarded (cut at max_tokens, invalid JSON) or times out, retry on a fallback model instead of the same one. At temperature 0 the same model "re-entered the loop on the same content" (§4). | Removes the 64k-token loops that cost the most and take the longest. | Small: a per-role `fallback_model` in `llm.py`, used only for the retry after a discard or timeout. |
| C4 | Mixture-of-Agents (two assessments merged) | Two models assess; a third merges. | About 2–3× the cost per case, plus a merge step and its own verification. | Large. **Not proposed** for today. |

**Proposal:** run the single-model arms first; the measurements per role are in `calls.json`. Then build one combined arm from the per-role results: C1 + C2, plus C3 if the code change passes review. Measure it on the same 6 cases against the best single model.

## 10. Decision models such as TypeSafe "Jev" (added 2026-10-18, user: "can try jev type models?")

What it is (search 2026-10-18; mostly secondary sources, vendor figures unverified):

- **A non-generative decision model.** You send text plus typed questions and get structured answers back. There are three question types:
  - Choice: a winning label.
  - Score: an expected value with probabilities per level.
  - "Noul": P(yes).
- **It cannot write, summarise or explain.**
- Launched in early access on 14 or 15 Sep 2026; sources differ. There is a waitlist, and no dedicated pricing page was found.
- Reported price: $0.042 per 1M input tokens, output free. Vendor latency claim: 70–500 ms. Vendor speed and cost multipliers come from their own workflows.
- Sources:
  - https://www.gigazine.net/news/20260916-system-one-jev/
  - https://www.gradually.ai/en/ai-models/jev/
  - https://innfactory.ai/en/ai-models/typesafe-jev/
  - https://pub.towardsai.net/meet-jev-the-ai-model-that-doesnt-write-and-why-data-engineers-should-care-f3ebfa2aab55
  - Aggregator: https://aiweekly.co/alerts/jev-judge-model-matches-llm-accuracy-at-036-of-the-cost
- **As a judge:** "JEV vs. LLMs as Rubric Judges: Cheaper, Faster, and Wrong in the Same Places", https://arxiv.org/pdf/2609.29769. A search summary reports RewardBench 92.2% vs 93.5% for an LLM judge, and 14.6 points behind on JudgeBench (not read in full).
- Related, but different: JEPA-style LLM training (LLM-JEPA, Huang, LeCun, Balestriero, arXiv:2509.14252, https://arxiv.org/abs/2509.14252). It is a training objective, not a model we can call, so it does not apply to us.

Fit for this pipeline:

| Step | Kind of work | Could a decision model do it? |
|---|---|---|
| Assess and repair (~75–90% of tokens and time) | Writes the cited assessment, options and questions | **No.** This needs generated text, and it is where the cost is. |
| Intake | Extracts facts, quotes, slots and unknowns | Mostly no: it must copy enquiry quotes. Only the route or off-topic decision is a Choice. |
| Screening, verification, cost class | Already deterministic code (rules, verbatim quote checks) | Not needed: code is free, exact and auditable. |
| External step | Query plan (text) and quote selection (text and verbatim quotes) | No. Source relevance is a deterministic check today. |
| Eval / bake-off quality judging | Rubric scores | Possible, as a cheap second judge. The paper above says it fails where LLM judges fail. |

**Verdict:** it would not lower our cost or time today. Our cost sits in the generative assess step, which Jev cannot do. Every bounded decision in the pipeline is already deterministic code. Access is early-access with a waitlist and no OpenRouter route, so integrating it today would be an untested dependency right before the freeze. A possible use after the hackathon: a cheap route or off-topic pre-check, or a second rubric judge in the eval.
