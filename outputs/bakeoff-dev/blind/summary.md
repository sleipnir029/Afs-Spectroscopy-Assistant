# D01–D08 blind quality summary (2026-10-18 ~10:42)

Four blind judges, 2 cases each. Arms were shown as letters P–V; the mapping was applied only after all four finished. Each judge scored against the AFS eval data (dev.jsonl eval_facts_stated / eval_useful_sources, dev_reference worked answers D01–D02). Criteria a–f, 1–5. Pipeline e3da219, `--external cache`.

| Rank | Arm (letter) | D01–02 | D03–04 | D05–06 | D07–08 | **Mean** | Mean s/case | Mean $/case | AFS source recall | Earlier 3-case judge |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | deepseek-1017 (S) | 4.42 | 3.75 | 4.50 | 3.92 | **4.15** | 259 | $0.013 | 78% | 3.60 |
| 2 | baseline (T) | 4.33 | 4.08 | 4.33 | 3.58 | **4.08** | 504 | $0.022 | 82% | 3.87 |
| 3 | mix-a (Q) | 4.58 | 4.33 | 3.42 | 3.92 | **4.06** | 84 | $0.030 | 85% | 4.47 |
| 4 | glm-5.3-flash (R) | 4.08 | 3.75 | 4.00 | 4.00 | **3.96** | 322 | $0.006 | 85% | 3.33 |
| 5 | gemini-3.8-flash (P) | 3.58 | 4.00 | 3.67 | 3.75 | **3.75** | 173 | $0.059 | 82% | 4.53 |
| 6 | mix-b (V) | 3.17 | 3.50 | 3.17 | 3.67 | **3.38** | 69 | $0.030 | 75% | 3.47 |
| 7 | gemini-3.5-flash-lite (U) | 3.08 | 3.08 | 3.25 | 3.50 | **3.23** | 29 | $0.015 | 65% | 2.67 |
