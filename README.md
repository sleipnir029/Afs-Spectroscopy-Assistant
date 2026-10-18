# AFS Spectroscopy Assistant (Team Helios)

The assistant reads a customer enquiry about in-line spectroscopy, the kind Art Fiber Systems (AFS) gets: "we want to follow X in our process, which method and probe should we test first?". It writes a cited first technical assessment. It screens the methods against rules taken from the supplied AFS materials. A model writes the assessment, and code then checks every quote word for word against the page it cites. Anything that fails the checks is repaired, removed or labelled before the answer is shown. External literature is used only for gaps the AFS materials leave open, and it is marked as secondary.

Hackathon deliverable. Deadline: Sun 18 Oct 2026, 23:59 Berlin.

## What it produces

- **A first technical assessment** for each enquiry, as JSON and Markdown:
  - a short answer and a proposal (which option to test first, what would change the choice, the next step);
  - two or three solution options (simple / recommended / extended multi-method), each with a cost class taken from S01 Table 1 (p.6) and a confidence level computed by code;
  - premise checks, open questions linked to the options they affect, risks, a feasibility plan, a setup diagram and parameter tables.
  - Citations use the form `S01 p.10` (1-based PDF page; S02 uses slide numbers). External items use `E01 ¶12`, each with its quoted passage and URL.
- **A web chat** (`uv run afs-assist ui`). The first message runs the assessment. After that you can:
  - ask follow-up questions, and every claim in the answer is checked against its sources;
  - re-assess with new facts. The new turn opens with "What changed";
  - see live result blocks (recommendation, options table, setup diagram, parameters, questions, risks, plan, sources, what changed). The server renders these blocks from the verified run data. The model only picks which blocks to show and never writes HTML.

Screenshots: `docs/ui/brief-*.png` (chat UI), `docs/ui/chat-*.png` (chat answers with blocks).

Example output: `outputs/final/H04.md` (held-out case, unedited). Demo video: `docs/video/demo.mp4` (2:25, the real app with live model calls). Slides: `docs/slides/slides.pdf`.

Without an API key you can still browse saved runs (`uv run afs-assist ui`), and run `uv run pytest` and `uv run afs-assist eval`.

## Quick start (uv only)

```bash
uv sync
```

Create a `.env` in the repo root with your own keys. **Never commit `.env`** (it is in `.gitignore`).

```
OPENROUTER_API_KEY=sk-or-...        # required for any model call
CONTACT_EMAIL=you@example.org       # Unpaywall needs it; also sent as OpenAlex `mailto` (polite pool)
# OPENALEX_API_KEY=...              # optional; the keyless OpenAlex budget is about 100 searches/day per IP
# AFS_MODELS_CONFIG=config/bakeoff/baseline-v4.1-flash.yaml   # optional: another models config
```

Without `CONTACT_EMAIL` the Unpaywall lookup is skipped. The pipeline never calls Crossref.

### Knowledge base and organiser files

The organiser files (AFS / SchubKI materials, S01–S06 and the reference docx) are **not in this repository**, and neither is their extracted full page text, `knowledge/pages.jsonl` (both are gitignored; see `NOTICE`). What is committed is our own derived knowledge: page scopes, rules (each with a short verbatim source quote), S01 Table 1, fiber data, the graph and our S02 notes.

The assistant needs the page text to assess or to open a run. Recreate it from the organiser archive:

```bash
unzip materials.zip -d resources/      # gives resources/materials/S01_….pdf … (organiser archive)
uv run afs-assist kb build             # writes knowledge/pages.jsonl (and rebuilds the other knowledge files)
uv run afs-assist kb check             # validate knowledge/ (every rule quote verbatim on its page, etc.)
```

The rebuilt `knowledge/pages.jsonl` is byte-identical to the one the runs used: its sha256 equals `pages_sha256` in every run manifest (`7e23c2ae…` in `outputs/final/H01.json`; checked by rebuilding in a fresh clone, 2026-10-18). Without it, `assess`, `run` and `ui` stop with a message that says to run `kb build`, `kb check` reports `pages_present` as failing, and the tests that need the page text are skipped with the same hint. The saved outputs, `afs-assist eval` and `afs-assist external replay` work without it.

## Commands

| Command | What it does |
|---|---|
| `uv run afs-assist ui [--port 8765] [--external live\|cache\|off]` | Local web chat at http://127.0.0.1:8765. Opens saved runs, assesses a new enquiry, answers follow-ups, re-assesses. |
| `uv run afs-assist assess --text "..."` or `--file enquiry.txt [--out DIR]` | Assesses one enquiry and prints the Markdown. With `--out`, also writes `.json`/`.md`. |
| `uv run afs-assist run --set dev\|adversarial [--only D01,D02] [--workers 4] [--outputs DIR]` | Assesses a scenario set in parallel. Writes `outputs/<set>/<id>.json\|.md`. |
| `uv run afs-assist run --set final --i-know-this-is-the-final-run` | The held-out H01–H06 set. It refuses to run without the flag. It was run once on tag `freeze-1`. |
| `--external live\|cache\|off` (on `assess`, `run`, `ui`) | `live` searches the scholarly APIs and falls back to the curated library on a network error or rate limit. `cache` makes no literature-API calls and answers them from recorded responses only (model calls still run; a query that differs from the recording falls back to the library). `off` skips the literature step. |
| `uv run afs-assist external replay outputs/final/H01.json` | Re-checks a run's external items offline against the cached text (exact re-check, no model call). |
| `uv run afs-assist eval [--set dev\|adversarial]` | Deterministic checklist over the saved runs (no model or API call). Writes `outputs/eval/summary.md\|json`. |
| `uv run afs-assist kb build\|check` | Rebuilds or validates `knowledge/` (see above). |
| `uv run pytest` | Offline test suite. It uses fake model clients, so it needs no API key and no `resources/`. |

Every run is also written as a commit on the `provenance` branch (see ARCHITECTURE.md). Local copies go to `runs/` (gitignored).

## Models

The production config is `config/models.yaml`, the combined arm **mix-a** (D-063, chosen by the user after the bake-off). All models are called through OpenRouter, pinned, with strict JSON output and temperature 0:

| Role | Model | Fallback model |
|---|---|---|
| intake, external_queries, external_evidence | `google/gemini-3.5-flash-lite` (flex tier) | `z-ai/glm-5.3-flash` |
| assess (writes the assessment) | `z-ai/glm-5.3-flash` | `google/gemini-3.8-flash` |
| repair (only when the checks find hard failures) | `google/gemini-3.8-flash` (flex tier) | `z-ai/glm-5.3-flash` |
| chat_answer (follow-up questions) | `z-ai/glm-5.3-flash` | `google/gemini-3.8-flash` |

- **Per-role models:** a fast, cheap model does the short structured jobs, and a cheap reasoning model writes the assessment.
- **Escalating repair:** when the deterministic checks fail, the repair goes to a different, stronger model. This is a cascade in the style of FrugalGPT, with the verifier as the scorer (docs/model-research.md §9).
- **Cross-model retry:** a reply that is cut off, is invalid JSON or times out is retried on the fallback model instead of the same one (D-059).
- **Spend caps:** $1.00 per run and $10.00 per session (`spend_cap_usd`).
- **Switching models:** set `AFS_MODELS_CONFIG=config/bakeoff/<arm>.yaml`. The arm configs from the bake-off are in `config/bakeoff/`, including the previous single-model config `baseline-v4.1-flash.yaml`. Each run's manifest records the config path and its sha256.

**Cost and time per case on mix-a:**
- H01–H06 freeze run: 97–184 s and $0.032–0.064 per case, $0.288 in total (`outputs/final/*.json` manifests).
- 19-case dev + adversarial gate run: 35–247 s per case (mean about 105 s), $0.013–0.070 per case (STATUS.md 11:52).
- A chat follow-up: 1.4–6.3 s, about $0.004 per question (10 questions for $0.038, `docs/chat/live-check-20261018.json`).

## Results

### Final set H01–H06 (held out, run once on tag `freeze-1`)

Outputs are in `outputs/final/H01.json|.md` … `H06.json|.md`. They are generated by the assistant with no manual edits. The run used `--external live` with code 1b3a7b9 (clean tree) and `config/models.yaml` (mix-a).

| Case | Status | Citations verified | Hard failures | Wall time | Cost |
|---|---|---|---|---|---|
| H01 | premise_not_supported | 14/14 | 0 | 97 s | $0.032 |
| H02 | provisional_assessment | 16/16 | 0 | 98 s | $0.043 |
| H03 | premise_not_supported | 21/21 | 0 | 184 s | $0.054 |
| H04 | premise_not_supported | 25/25 | 0 | 180 s | $0.064 |
| H05 | insufficient_information | 22/22 | 0 | 148 s | $0.045 |
| H06 | premise_not_supported | 22/22 | 0 | 180 s | $0.050 |
| **Total** | | **120/120** | **0** | | **$0.288** |

- 0 runaway replies and 0 timeouts.
- The cost class matched S01 Table 1 in 6 of 6 cases (`scripts/check_cost_class.py`).
- External replay: 13/13 rows equal (6 kept items, 1 dropped item, 6 library-file hash checks) on the machine that ran the set.
- **Rule-compliance review** by an independent reviewer agent (`outputs/final/REVIEW.md`): PASS WITH CAVEATS, no blocking violation.
  - Each status is justified by a cited source.
  - External items appear only in the secondary section.
  - Cost is given only as a Table 1 class, never a price.
  - No invented accuracy, detection limit, response time or fiber length.
  - Every case has a proposal, a change trigger, a next step, and 4–5 questions.

### Evaluation on dev (D01–D08) and adversarial (A01–A12)

Source: `outputs/eval/summary.md`, the gate run on mix-a with `--external live`.
- **Checklist:** 0 failures in both sets. It has 19 binary items mapped to the six judging criteria: structure, citations verified, no open failures, no flagged figures, no currency, no certainty wording, cost class vs Table 1, option and proposal rules, feasibility plan, premise flags, questions, length, external items secondary and replayable, off-topic handling.
- **Per-enquiry checks (adversarial):** must 33/34 and must-not 12/13. Both failures are A07, a complete enquiry:
  - it got 4 questions where at most 3 are allowed;
  - the must-not pattern `reference (method|measurement|analys)` matched a legitimate question about the reference's reproducibility.
  - Both are recorded as they are. The eval was not changed after seeing the outputs (D-051; STATUS 11:52).
- Citations verified 100 % in every case. External replay 19/19 equal.

### Model bake-off

7 arms ran on D01–D08 with `--external cache`. Four blind judge agents (LLM reviewers) scored them against the AFS eval data (facts stated and useful sources in `scenarios/dev.jsonl`, and the worked answers for D01–D02). Arms were shown as anonymous letters.

Source: `outputs/bakeoff-dev/blind/summary.md`, with recall from `outputs/bakeoff-dev/afs-score.md`.

| Arm | Blind quality (1–5) | Mean s/case | Mean $/case | AFS useful-source recall |
|---|---|---|---|---|
| deepseek-v4.1-flash-1017 | 4.15 | 259 | $0.013 | 78 % |
| baseline (deepseek-v4.1-flash) | 4.08 | 504 | $0.022 | 82 % |
| **mix-a (chosen)** | **4.06** | **84** | **$0.030** | **85 %** |
| glm-5.3-flash | 3.96 | 322 | $0.006 | 85 % |
| gemini-3.8-flash | 3.75 | 173 | $0.059 | 82 % |
| mix-b | 3.38 | 69 | $0.030 | 75 % |
| gemini-3.5-flash-lite | 3.23 | 29 | $0.015 | 65 % |

All arms had 0 hard failures and 0 checklist failures. The top three are close on quality. mix-a was chosen because it is 3–6× faster than the other two and was also in the top group of an earlier 3-case review (D-063).

An earlier 6-case bake-off is in `outputs/bakeoff/compare.md`. In it, two arms (Haiku 5.5 and GPT-6 Luna) were dropped because their APIs rejected our strict JSON schema on the first call (`outputs/bakeoff/README.md`).

### Reproducibility

Fresh-clone test, 2026-10-18 about 12:35:
- A fresh `git clone` + `uv sync`, with no `resources/` folder, passes `uv run pytest -q` (758 passed, 2 skipped).
- It also passes `uv run afs-assist kb check`: all PASS. The S02 PDF text-layer comparison is skipped without the PDF.
- One live `afs-assist assess --text ... --external off` in the clone took 92 s and $0.031, with 0 hard failures and 25/25 citations verified.

Replay in a fresh clone:
- `afs-assist external replay outputs/final/<H>.json` re-checks the items from the curated library.
- It reports the full-text items as "source text not in the local cache". This is by design (user decision 2026-10-17 12:31):
  - git holds the metadata, the verified quotes and the sha256 of each fetched source;
  - the full fetched text stays in the local, gitignored cache `runs/external_cache/`.
- On the machine that ran H01–H06, the replay is 13/13 equal.

Every run's manifest records the code sha, a dirty flag, the models config and its sha256, and the prompt, skill, knowledge, pages and rules sha256. It also records the cost, the tokens and the provenance commit.

## Known limitations

From STATUS.md, the G5 review (PHASES.md "Review (G5)") and the H01–H06 rule-compliance review (`outputs/final/REVIEW.md`, generic patterns only):

- **Answers are long.** The H01–H06 Markdown files are 3,058–3,455 words each, including the expert detail. The AFS worked answers for D01–D02 are 303–400 words (`scenarios/dev_reference.jsonl`). The short answer and the tables carry the reader, but the full report is far longer than what AFS writes.
- **"Verified" means the quote is on the cited page and in scope, not that it supports the claim.** A page-scope check (`scope.py`) limits what kind of claim a page can back, and precedents are labelled. Still, a claim can go beyond its valid quote, and a citation is sometimes used for a point the page does not really make (seen in four of the six H outputs). The planned entailment critic (PHASES 5.5) was not built.
- **Gaps in the checks:**
  - Short table cells (performance fit, future direction) are not screened for overclaiming.
  - A page reference typed inline in prose, rather than as a citation, skips verification.
  - A cited quote can carry the source's own certainty wording.
  - No check compares fields with each other, for example contact vs non-contact in two sections.
- **Literature tagging:** an external item can be tagged to the wrong option, or be only weakly relevant.
- **Lab reference methods** (for example Kjeldahl or Karl Fischer) are engineering judgement. They are marked "e.g." and flagged as unsourced.
- **Setup sketch:** the NIR fiber label lists every fiber family that overlaps the range.
- **Over-questioning:** a complete enquiry can still get 4–5 questions (A07, D-051). The questions are relevant, not re-asks of stated facts.
- **Confidence rarely varies.** It is computed by code from open questions and named weaknesses. In the G5 review it was Low for 45 of 55 options, Medium for 10 and High for none. It rates the basis of the advice, never a predicted accuracy.
- **A follow-up can flip the method** without a clear reason (seen in the G5 live loop: Raman to MIR-ATR; and in the demo video: NIR alone to NIR + Raman after only a temperature answer). A re-assessment is a fresh model run, so it can differ for reasons other than the new fact.
- **Margin note numbers restart per turn,** so in a long thread the same number can point to different quotes in different turns.
- **Latency:** a full assessment takes about 1.5–3 minutes. The Gemini roles use the flex tier, which can queue or rate-limit. The fallback models cover that, but runs may be slower.
- **External literature** comes from keyless APIs with small shared quotas (OpenAlex keyless is about 100 searches per day per IP). When those fail, the step falls back to the 9-entry curated library.
- **Windows:** parallel set runs inside one process are serialised by a thread lock. The cross-process provenance lock uses `fcntl` (POSIX only), so on Windows do not run two `afs-assist` processes at once.
- **Reruns differ.** Live model calls do not give byte-identical reruns. The frozen H outputs are stored once and are not regenerated.

## Licences and materials

- **Our code and docs:** MIT (`LICENSE`). `NOTICE` lists what the licence does not cover.
- **Organiser and publisher materials** (S01–S05, S06, the reference docx and the method table, AFS / SchubKI and the publishers) are not in the repository and belong to their holders. Their full page text (`knowledge/pages.jsonl`) is rebuilt locally with `kb build`. The short verbatim quotes in `knowledge/` (rules, page scopes, S02 notes, Table 1) and in `outputs/` are citations for the challenge. S03 is open access under CC BY 4.0 (attribution in `NOTICE`).
- **Fonts:** IBM Plex Sans and Mono (Copyright 2017 IBM Corp.) and Newsreader (Copyright 2020 The Newsreader Project Authors). All are under the SIL Open Font License 1.1 and self-hosted in `src/afs_assistant/ui/static/fonts/` (see `OFL.txt` and `OFL-Newsreader.txt`).
- **htmx 2.0.4** (0BSD) is vendored in `src/afs_assistant/ui/static/vendor/`.
- **External literature:** only short verified quotes, each with its URL or DOI, and metadata are stored. The curated library holds open-access (CC BY) passages.

More detail: `ARCHITECTURE.md`, `PHASES.md` (plans), `DEVIATIONS.md` (every change from plan), `STATUS.md` (log), `docs/model-research.md`, `docs/slides/slides.pdf`.
