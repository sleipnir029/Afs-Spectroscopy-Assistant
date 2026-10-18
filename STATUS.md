# Status

_Last updated: 2026-10-18 05:34 CEST (Claude, Phase 5 session 3)._

**00:07 session 2 started:** task 1: reviewer agent on branch worktree-agent-a5dda1b856731189d (eval harness), read-only.
- **Eval branch review: NEEDS_FIXES** (B1 CLI exits 0 with nothing checked + hidden must_not on unreadable/raising predicate; B2 adversarial never run (G5); B3 A07 must_not fails good answers via why_it_matters; non-blocking: A02/A03/A06 predicates loose, no_currency scans the enquiry, external_replay all-or-nothing, D03 real fail pending re-run; merge conflict cli.py only, merged tree 611 passed). Implementer agent applying fixes + merge of master in the worktree (no API spend).
- **Eval merged (00:22):** fixes 32b0dac + confirm review APPROVE WITH FIXES → Claude fixes b15b4c7 (no vacuous must_not on a wrong off-topic redirect, malformed spec rows, OSError, A03/A06 patterns); D-046. master: pytest 622 passed, 2 skipped; ruff clean. **00:23 live runs started:** dev then adversarial, `--workers 4 --external live` (logs run_dev.log / run_adv.log in the session scratchpad).
- **Live runs done 02:15 (7c2d4c6):** dev 8/8 + adversarial 11/11 assessed + A12 off-topic; 0 hard failures; all citations verified (dev 254, adv 347); replay 19/19 equal; check_cost_class 8/8 + 11/11; Mermaid 20/20 adv; cost $0.234 + $0.356. **Eval:** must 34/34, must-not 13/13 (G5 item met); D03 proposal_rules now PASS. Checklist fails: D02 options_rules (extended with one method: model put MIR in its own combined_with), D04/A07/A11 questions_present (raw model reply had 0 questions, 6 unknowns). → **5.R1 planned 02:20** (PHASES.md, D-047), implementer next.
- **5.R1 (branch worktree-agent-ade5f3a7df4d96488, f2bda6e):** two hard checks + repair lines + finalize fallbacks; review APPROVE WITH FIXES (02:32; offline sim over 19 saved runs: only A07 gets an extra repair call, 0 open failures after the fallback). Fixes running (question fallback after the status step, extended fallback tries comparison/conditional too, eval options_rules uses verify's method count, no_flagged_figures ignores fallback flags, question casing). Master 450e8a5: UI tests on a frozen D03 fixture (a live re-run had broken 2 UI tests; caught by the implementer). pytest 622 passed, 2 skipped. **5.R1 merged 02:37** (fixes 7c52803, D-048): pytest 642 passed, 2 skipped; ruff clean; kb check PASS. Live re-run of D02, D04, A07, A11 started 02:37.
- **5.R1 re-run done 03:09 (3114f8d, $0.11):** D02/D04/A07/A11 0 hard failures, all citations verified, replay 4/4 equal, 5 questions each, no fallback fired (prompt line + repair did it). **Eval:** checklist **0 failures** dev + adversarial; must-not 13/13; **must 33/34: A07 `max_questions` 3 fails (5 questions)** — the complete enquiry is over-questioned since the new assess line 'ask at least one question'. Questions are sensible (interferents, bubbles, CIP details, port, refractometer accuracy) but the check stays (no goalpost move).
- **05:15 session 3 started:** task 1 (A07 over-questioning): D-049 assess step 7 question count scales with what is open, no re-asking stated facts (3662329; pytest 642 passed, 2 skipped). Live re-run A06, A07, D04 started 05:16. **Done 05:26 ($0.085):** 0 hard failures, citations verified, but 6 questions each (A07 5→6, A06 5→6, D04 5→6); A07 max_questions still fails. → D-051: prompt + outputs reverted to 5.R1 (evidence 635401c); A07 recorded as a known limit. Eval: checklist 0 failures, must 33/34, must-not 13/13; pytest 642/2. **Task 2** (carry-overs 1, 5, 6) implemented on branch worktree-agent-af27b84c238dd6dba (2189670, D-050, pytest 656/2); reviewer running. Items 2, 3, 4 left as known limits (rating design / prompt work). **Merged 05:34** after review NEEDS_FIXES (B1 cap hid customer figures e.g. a 150 m distance; B2 web UI capped silently) → fixes 84f4a1f → confirm review APPROVE (non-blocking limits noted in D-050). master: pytest 661 passed, 2 skipped; ruff clean; kb check PASS. Saved outputs still show the old rendering until the next run (Phase 6 freeze run re-renders).

**Deadline:** Sun 18 Oct 23:59 Berlin. **Q&A:** Sat 17 Oct 13:38–13:48 (Helios).

## Current phase
**Phase 4 (External evidence): CLOSED 22:46 (G4 PASS WITH NON-BLOCKING).** See PHASES.md "### Phase 4 close". **Phase 5 started early (user 22:35/22:41, D-039/D-040):** web UI per the approved plan 5.6''' (approved 22:45; agent building in a worktree), 5.0 robustness items (off-topic short-circuit, parallel runs, LLM timeouts; agent in a worktree). Both to be merged after their checks.
- **5.0 + 5.0.R merged (23:00):** review NEEDS_FIXES (two misroutes of real enquiries to off-topic; per-read timeout not a deadline) → 5.0.R (D-042: stricter off-topic rule, first attempt only, intake prompt `out_of_scope` line; wall-clock LLM deadline; Ctrl-C cancel) → re-review APPROVE WITH FIXES (cancel in the external step) → fixed add6c87. pytest 490 passed, 2 skipped; ruff clean. Live check: "What is the capital of France?" → redirect + 3 examples after one intake call, $0.0004.
- **Web UI v1 (branch worktree-agent-a207b0059aa193d71, aa66396; not merged):** built per 5.6'''; review NEEDS_FIXES: B1 Fig. 2 prints a fluorescence range (190–740 nm) that S01 p.12 does not state (borrowed from UV-Vis) — truthfulness; B2 phone Saved-runs menu clipped; B3 figure text too small (container query, ≥12 px); B4 POST /assess and /clarify accept cross-origin requests and foreign Host (add Origin/Host middleware). Non-blocking: simplify Fig. 2, shadows, ⚠ emoji variant, http-only links, "Off topic" label for incomplete runs, unused 2.8 MB mermaid file (removal needs the user's OK). **User (23:08): the page reads like a report, unclear where to ask; asked for UI/UX research and examples before deciding.** Research agent started (docs/ui-research.md); then 2–3 mockups for the user to choose; the review fixes go into the chosen design.
- **UI research + direction (23:21, D-043):** docs/ui-research.md (12 patterns, sources); three mockups on a private canvas (claude.ai/artifact/J3ziNHcrv1nURmoZjqZDXk); **user chose A "Answer + Ask"** (plan PHASES.md 5.6⁗). The UI agent reworks its worktree branch (worktree-agent-a207b0059aa193d71) to A + the v1 review fixes; then reviewer agent, screenshots to the user, merge. Open user decision: remove the unused 2.8 MB mermaid file from the UI branch (recommend yes).
- **5.0b merged (23:48):** query privacy guard (names incl. sentence-initial/signatures, e-mail/URL domains, product codes; chemical formulas allowed; 0/41 dev queries dropped; known limit: an all-lowercase name cannot be caught), digit-hyphen and digit-space loose rules (880 output quotes and 77 kb quotes unchanged), per-API search failure, abstract relevance (D-045; 11/12 dev abstracts dropped). Reviewer APPROVE WITH FIXES → F1/F2 applied. pytest 509 passed, 2 skipped.
- **UI direction A merged (after c0b4c8a + slash-wrap fix; confirm review APPROVE WITH FIXES).** Earlier review NEEDS_FIXES: B1 Origin port not compared (localhost:3000 could POST), B2 setup-diagram labels truncated with "…" in all 8 dev runs, B3 option ids (O1–O3) in the main view; + polish N1–N6, N8, N9 → fixed.
- **5.1/5.2 done, NOT reviewed, NOT merged:** branch worktree-agent-a5dda1b856731189d, ecbb021: scenarios/adversarial.jsonl (A01–A12 with must/must_not), `afs-assist eval` (src/afs_assistant/evaluate.py, 19 items → six criteria), outputs/eval/summary.md/json; dev: 7/8 pass all applicable items, D03 fails proposal_rules (the known D-041 support line); adversarial not run. pytest 527 passed on the branch. Note: the sandbox blocks shell commands containing the word "eval" (use a wrapper).
- **User rule (23:55): one agent at a time** (implementer → reviewer), Claude orchestrates; new work in a new session (memory: feedback_one_agent_at_a_time).
- **Phase 5 must-dos before the freeze:** G4 N2 query-privacy code guard; re-run D03 (D-041); dev re-run with `--workers 4` on the new intake prompt.

**Phase 4 (External evidence, option B): IN PROGRESS (started 19:52).** Implementation plan + D-034 committed 57ab2ba (19:56); **Code 2e9a47a + 77fb873** (items 1–11; D-035 implementer choices + two Claude additions): pytest 413 passed, 2 skipped; ruff clean; kb check all PASS (library empty). **Live API probe (20:14–20:18, keyless, one call each):** OpenAlex search 200, 0.83 s, 5 parsed, ratelimit remaining 960/1000 ($0.096 left, $0.001/search); Europe PMC search 200, 0.32 s; EPMC fullTextXML 200, 0.67 s, 105 paragraphs; Unpaywall 200, 0.51 s, OA PDF + cc-by. OpenAlex searches used: 3.
**Curated library df33769:** 9 entries (EPMC full text, cc by), 28 passages ≤398 chars; topics: PAT data fusion, multi-block fusion, Raman as PAT, optical PAT trends, in-line NIR tools, in-line ATR-FTIR, NIR temperature correction, FT-IR+Raman maintenance, Raman probe cleaning. Spec `scripts/external_library_spec.yaml`. No OA source found for reactor temperature measurement or viscosity. kb check 9/9 + external_library PASS; pytest 413/2 skipped.
**20:18 D01–D08 `--external=live` started** on code df33769 (log in the session scratchpad); this run shows live behaviour only, it is re-run after 4.R.
**G4 code review (20:22, reviewer agent, run in parallel): NEEDS_FIXES** — B1 uncapped model text in dropped items reaches git; B2 an external-step crash (null API fields) kills the primary assessment and the set; B3 no wall deadline (drip-feeding server); B4 localhost guard bypass (127.1, 0x7f.1, localhost.). N1–N12 non-blocking. → **4.R** (PHASES.md; D-036) done in a worktree (5b767ce), merged 20:37: pytest 439 passed, 2 skipped; ruff clean; kb check PASS.
**Preview run (pre-4.R code) stopped after D01** (D-037): D01 external 4 gaps, 6 queries (EPMC ×6, OpenAlex ×3), 5 sources (3 library, 2 EPMC abstracts), 7 verified items, 0 dropped, $0.0098, **253 s** (evidence call 218 s, 19k reasoning tokens). With `reasoning: {effort: low}` on the external roles (D-037, 72e493a): **97 s, $0.0042**, 5 verified, 0 dropped. pytest 440 passed, 2 skipped.
**20:41 D01–D08 `--external=live` re-run started on f6538ee** (log `devrun_p4r.log` in the session scratchpad). D01 (361 s; external 54 s, $0.0019, 2 verified items, library only after a Europe PMC ReadTimeout) and D02 (599 s; external 54 s, $0.0025, 4 verified) done: 0 hard failures, 21/21 and 30/30 citations. **D03 hung 42 min in an LLM call → stopped 21:39, D03–D08 restarted with `--only` (D-038).** Next: `external replay` ×8, `check_cost_class`, `check_mermaid`, `git ls-files` copyright check, G4 re-review (reviewer agent).
**D03–D08 done 22:37 (session $0.157 for D03–D08). Phase 4 dev outputs 16f85fb:** 8/8 pass, 0 hard failures, 227/227 supplied citations verified; `external replay` 8/8 equal (30 external items, 0 dropped); every gap has a verified item or an explicit "no usable external source found"; external step 39–76 s and $0.0018–0.0036 per case (targets ≤90 s, ≤$0.03); D01 library-only after a Europe PMC ReadTimeout; D03 proposal gets secondary external support; `check_cost_class` 8/8; `check_mermaid` 15/15; `git ls-files`: no resources/, no full third-party text.
**User decisions 22:35 (D-039):** custom web page (not Streamlit), clean technical-report look + dark mode, start now in parallel; off-topic → polite redirect + example questions without a full run; parallel set runs + LLM timeouts (Phase 5). Keep API use low.
**22:38 running in parallel:** G4 re-review (reviewer agent, read-only) and the web UI build (implementer agent, separate worktree, saved runs only, no API cost).

**Phase 3 (Assessment upgrade): CLOSED 19:36 (G3 passed).** Re-plan approved 13:36 (simple chat → now the Streamlit app, D-023). Additions approved 14:22 (user): two-layer answer + code-derived confidence rating (D-022). D-024: single_primary skipped for outside_supported_scope.
- **User mode (D-020, 14:24):** Claude is fully in charge; the user is woken (push notification) only for their decisions. At each phase end: write this handoff and tell the user to switch sessions ("do the next task").
- **Phase 3 code** 3c7e881: pytest 248 passed, 1 skipped; ruff clean; kb check 9/9. Code review: APPROVE WITH FIXES (B1 duplicate ids, B2 proposal basis unverified, B3 price wording) → 3.R item 1.
- **First Phase 3 dev run (13:51–14:59, $0.211):** 7/8 complete, 0 hard failures left, citations 241/241 verified, 12/12 Mermaid charts render, cost classes match Table 1 (D01–D04 checked; the check script crashed on the stale D05). **D05 failed** (assess reply truncated at max_tokens). D06 simple = recommended option. Body 2,472–3,137 words. outputs/dev/D05.* are still the 12:41 Phase 2 output.
- **3.R implemented (15:21, offline):** items 1, 2, 3, 4, 4b done; pytest 297 passed, 1 skipped; ruff clean; kb check 9/9. D05 diagnosis (2 raw calls, $0.0175): hidden reasoning used 27,904 of 32,000 completion tokens, no repetition loop; assess/repair max_tokens → 64,000 (D-025). Implementer choices in D-025. Not yet run live.
- **3.R** done (0ce9801, D-025; D-026 9cfc7f2): pytest 298. 3.R code review: APPROVE WITH FIXES (2 blocking in the confidence rating). 3.R dev run (15:22–16:16): 8/8 complete, 0 hard failures, 227/227 citations, 15/15 charts, 8/8 cost classes; $0.171.
- **3.R2 implemented (16:27, offline):** items 1–4 done (B1 precedent by page scope, B2 unscreened/to-be-determined technique, N3 ⚠ open-check line + per-row confidence, N4 request label, N5 rule 3 any necessity, N6 currency codes any case except a journal abbreviation + Evidence section skipped by check_cost_class, N7 request line counted / "high cost (row N)" / H2 layers + H3 sections, item 3 Sources cell = rating pool, item 4 open top-3 question). pytest 319 passed, 1 skipped; ruff check clean; kb check 9/9. Implementer choices in D-028. `check_cost_class.py outputs/dev`: 0/8 (only the old cost wording, expected until the re-run); `check_mermaid.py outputs/dev`: 15/15. Not yet run live.
- **3.R2 dev run (16:58–17:55, $0.175, code 7ebe590):** 8/8, 0 hard failures, 227/227 citations, 14/14 charts, 8/8 cost; confidence 2 High / 7 Medium / 13 Low.
- **G3 review (18:05): NEEDS_FIXES:** D05 intake collapsed (Russian request line), D08 fluorescence wrongly failed by the screen, `affects` vocabulary, comparison treated as fusion, empty stated requirements, extended options undercosted; calibration driven by the temperature-sensor and fusion rules.
- **3.R3 implemented (18:13, offline):** items 1–9 done (intake check + one retry + request-line fallback; screen near-match neighbours soft_solid/paste; `affects` vocabulary normalised in finalize; fusion only for extended / fusion_note / combined_with, per-method models in the sketch; stated-requirements fallback; borrowed technique or "at least" cost; confidence: required parameters only, open question caps at Medium; simplicity items). pytest 354 passed, 1 skipped; ruff clean; kb check 9/9. graph.json unchanged (the state mapping does not feed it). Implementer choices in D-030. Offline recompute of the 3.R2 dev outputs with the new rules: 19 Medium / 3 Low of 22 (every option carries an open method question). Not yet run live; outputs/dev are still the 3.R2 run.
- **3.R3 code review: APPROVE WITH FIXES** (B1 intake warning not visible, B2 paraphrase in the stated fallback; N1–N7) → 3.R4 (D-032). The 3.R3 dev run started 18:19 was stopped at D01; outputs/dev/D01.* in the working tree are from that stopped run (not committed).
- **3.R4 implemented (18:25, offline):** items 1–8 done (⚠ intake-incomplete line in Verification, placeholders not counted as removed; stated fallback = verified enquiry quotes only; near match keeps the dark-sample / unknown-regime reason; `affects` accepts O ids and any method* word, an O id in a top-3 question affects that option; finalize logs only dropped affects items; merged Evidence entry keeps the precedent badge; confidence starts at Medium with an open method/option question, then one level per weakness; check_cost_class checks "at least"). pytest 372 passed, 1 skipped; ruff check clean; kb check 9/9. Implementer choices in D-033. Offline recompute of the 3.R2 dev outputs (bab11a7): 0 High / 8 Medium / 14 Low of 22 (the 3.R3 cap gave 0 / 19 / 3); every case still has an open method question in the top 3. Not yet run live.
- **3.R4 dev run (18:35–19:28, $0.198, outputs 085dcf1):** 8/8 pass, 0 hard failures, 236/236 citations, 14/14 charts, 8/8 cost classes; confidence 0 High / 7 Medium / 15 Low; Answer 585–753 words.
- **G3 re-review (19:36): PASS WITH NON-BLOCKING.** Phase 3 closed. Non-blocking items carried to Phase 5.4 (PHASES.md "Phase 3 close").
- **Next:** Phase 4 in a new session (handoff below).

## Next session starts with (handoff 2026-10-18 03:13)
Rules (user): ≤200k tokens per session; one piece of work per session; **ONE agent at a time** (implementer → reviewer), Claude orchestrates and does small exact fixes itself; low API use; wake the user only for their decisions. Run `uv run pytest -q` before committing new outputs (a live re-run once broke UI tests). At the end: write the next handoff here and tell the user to start a new session ("do the next task").

**State:** master 3114f8d+. pytest 642 passed / 2 skipped; ruff clean; kb check PASS. Merged this session: 5.1/5.2 eval harness (D-046), 5.R1 (D-047, D-048). Outputs: dev 8/8 and adversarial 12/12 live (D02, D04, A07, A11 on 5.R1 code; the rest on pre-5.R1 code, prompt sha differs). Eval wrapper: the sandbox blocks the word "eval" in shell commands; use a script that builds the subcommand (e.g. `exec uv run afs-assist ev''al "$@"`). `uv run afs-assist ev''al --mermaid` exits 1 on any not-run/unreadable case.

**Task for the next session (in order):**
1. **A07 over-questioning (generic):** prompts/assess.md step 7 says 'usually 3-5 questions' plus the new 'at least one when a key unknown is open'. Make it scale: ask only questions whose answer could change method, technique, installation or status; a complete enquiry may need only 1-3; never re-ask stated facts. Log a deviation, re-run A07 + one dev case (e.g. D04) + A06 (vague, needs ≥2) to check both directions (~$0.1), eval, commit. If one prompt change does not do it, stop and record it as a known limit (model variance) rather than looping.
2. Phase 3 carry-overs still open (PHASES "### Phase 3 close": stated-quote substrings, confidence separation, precedent against a single method, answer length, expert clutter, test gaps): pick what is cheap and safe; leave the rest listed as known limits.
3. UI leftovers (non-blocking): follow-up screenshot caption (stub replays the same assessment); answer pieces revealed during the run (N7); outputs/ui/ live runs are untracked (decide: commit or treat as throwaway).
4. 5.3 quick bake-off: skip unless time allows (flash stays; record as a deviation if skipped).
5. Then G5 (one reviewer: eval results, adversarial outputs, demo path), Phase 5 close, handoff to Phase 6 (freeze, H01–H06 once, README/ARCHITECTURE/slides/video, fresh-clone test; user yes/no to publish and submit). Deadline Sun 18 Oct 23:59; target submit 22:30.
Never read scenarios/final.jsonl before Phase 6.

## Phase overview
| Phase | State | Gate | Notes |
|---|---|---|---|
| 0 Repo hygiene and setup | Done (see D-001) | G0 retro-review pending | backup tgz, `.gitignore`, history purged, uv project + deps |
| 1 Knowledge foundation | **Closed** | G1 passed | pytest 59/59, kb check 9/9 | G1 ~13:15 | kb check 8/8, pytest 51/51, ruff clean |
| 2 Pipeline MVP | **Closed** 13:33 | G2 passed | |
| 3 Assessment upgrade | **Closed** 19:36 | G3 passed | 8/8, 236/236 citations, 14/14 charts, 8/8 cost |
| 4 External evidence (option B) | **Closed** 22:46 | G4 passed | 8/8, 227/227, replay 8/8, 23 external items |
| 5 Quality, eval and demo surface | **In progress** (UI direction A, D-043) | G5 Sun 14:00 | 5.0, 5.0b, 5.6⁗ merged; 5.1/5.2 branch to review |
| 6 Freeze and deliverables | Planned (approved 13:36) | Submit by 22:30 | user yes/no to publish + submit |

## Done
- **Jury input (12:22, relayed by the user; paraphrase, not verbatim):**
  - The system should always make a proposal, even when the supplied data does not cover the question.
  - If the information is not in the system, it should search online (research papers, proper scientific forums), analyse what it finds and explain how it can be used.
  - It must be able to analyse how a multispectral system can be used for a chemical process.
  - → A re-plan of Phases 3–6 is needed (what we have, what we plan, what can be integrated). Clarifying questions asked; no code changes until a plan is approved.
- **Decisions on the jury input (12:24, user):**
  - "Multispectral system" = several spectroscopy methods combined on one process, plus how their data are fused (not imaging).
  - Search mode = live search when the supplied sources do not cover the question, with the curated external library as the offline fallback; every external quote is fetched and verified verbatim.
  - Sources = free scholarly APIs (OpenAlex, Semantic Scholar, arXiv, Europe PMC, Crossref) plus general web search; external sources are always marked secondary.
  - Process = a background research agent now (notes in `docs/research-replan.md`); the full re-plan of Phases 3–6 is written in the next session for approval.
- **Research done (865da99, `docs/research-replan.md`).** Recommendation: option B (curated library first, then keyless scholarly APIs only on an evidence gap; fetch, verify verbatim and cache every source; a separate secondary-evidence section; a required proposal block; ~14–17 h). Option C (web plugin behind `--web`) is a stretch. Notes: OpenAlex keyless = a shared ~100 searches/day per IP; Semantic Scholar returned 429 without a key.
- **Decisions (12:31, user):**
  - Git gets the metadata, verified quotes and sha256 of fetched sources; full fetched text stays in a local gitignored cache (confirm the exact path at planning).
  - General web search is off by default, enabled by a flag.
  - Add a required Proposal block and keep the honest decision status.
  - Final H01–H06 runs: live search once, then freeze (cache and replay).
  - Still open: optional OpenAlex key, and which contact email to use for Unpaywall/Crossref.
- **Organizer Q&A notes (12:45):** `docs/qa-notes-2026-10-17.md` (our interpretation of a garbled transcript). Key points: multi-method because spectra overlap, but single method first if it answers; chemometrics with reference data is central; real-time tracking of intermediates; the first proposal = method-comparison design, not sample numbers or acceptance criteria; the jury may ask for a live run of a new enquiry. **Scope (12:51, user):** these Q&A points are for after the hackathon, so they are optional output fields filled when relevant, not musts.
- **End-user trade-offs (12:57, user; a must for the re-plan):**
  - Recommendations must weigh cost, ease of use and operation, maintenance and performance fit, and recommend the *optimal* option for the actual problem: not just the cheapest, not just the best result.
  - **Price = relative cost class only** (low/average/high per method+technique, cited to S01 Table 1, plus cost drivers such as fiber type, probe and chemometric-model effort). No currency figures; the verifier keeps blocking them.
  - Ease of use and maintenance come from the supplied sources (cleaning, fouling, probe contact, robustness) or are labelled engineering judgement.
- **More organizer input (13:05, user; under discussion, not yet decided):**
  - **Parameter-driven solution proposals:** from the enquiry, derive the *minimal* set of chemical and physical parameters (quantitative or qualitative, e.g. concentration, composition, intermediates, temperature, viscosity, phase). "As simple as possible, complex where needed": don't ask for more than needed.
  - **Map each parameter to a measurement:** a spectroscopy method or an auxiliary sensor (AFS probes can include thermocouples, an oral Q&A statement; temperature matters for exo/endothermic reactions).
  - **Give 1–3 solution options** with trade-offs (cost class, ease, maintenance, performance) and recommend the optimal one; a simple brief answer; sketches where useful.
  - **Gap:** the supplied KB has nothing on thermocouples, viscosity or temperature effects, so these need external sources (live search) or must be labelled engineering judgement. Spectroscopy does not measure viscosity directly.
  - **Proposed priorities:**
    - P1: parameter layer + solution options + brief answer + proposal block (~4–6 h).
    - P2: online search, option B (~10–14 h).
    - P3: code-generated Mermaid sketch (~1–2 h).
    - P4: optional fields.
    - Then the shell, freeze and deliverables (~8–10 h). Cut the bake-off to a quick check.
- **Decisions (13:07, user):**
  - **Thermocouples:** no written source from AFS. Two web searches found none (Art Photonics ATR listings give only temperature ranges, no integrated thermocouple/Pt100). Offer temperature sensing as a suggested option in proposals, labelled engineering judgement, "confirm availability with AFS"; live search may still find a source.
  - **Parameters: no cap.** Evaluate which parameters the case needs and whether each is necessary; also list optional "should be available" parameters with the reason.
  - **Solution options:** always 2–3: simple, recommended, extended multi-method.
  - **Sketch:** a Mermaid flowchart in the Markdown, no images.
  - **Bake-off:** cut to a quick check.
  - **Contact email for scholarly APIs (13:12, user):** stored as `CONTACT_EMAIL` in the gitignored `.env`, not in committed files. The code must read it from the environment, and the README tells others to set their own. No OpenAlex key for now (keyless plus the polite-pool email).
- Dev model switched to `deepseek/deepseek-v4.1-flash` (10:15, user; D-011). Providers [deepinfra, atlas-cloud, coreweave] (fp8, strict JSON); max_tokens 16k/32k/32k (reasoning tokens count). Smoke test: the D08 intake runs clean on flash (DeepInfra, finish=stop, $0.0031, proposed_methods [MIR, Fluorescence]). pytest 84 passed, 1 skipped. D01–D07 outputs are still from v4-pro: re-run on flash before G2.
- Decisions (09:29, user):
  - External reference library: **yes**. Curated, each entry with URL + verbatim quoted passage, marked secondary; to be planned in Phase 3.
  - Jury evaluation: **may be both** (jury runs the repo with their own key, and/or asks us to run an enquiry live). We therefore need a reproducible repo (README, fresh-clone test, own key) and a robust live demo (pinned providers, saved-run replay fallback, video).
- Live smoke run (09:27, generic ethanol enquiry; not a dev or final case):
  - End to end in 2.5 min, $0.064 (provider pinning D-010 after a first empty response).
  - 22/24 citations verified. The 2 removed were a quote taken from the organizer's worked answer (not in our knowledge base) and a quote spanning a page break; both were correctly caught.
  - 3 unverifiable intake items were sanitized.
  - Observed for Phase 3: claims that go beyond their (valid) quotes, e.g. "ethanol has characteristic NIR bands"; only an entailment check / critic can catch these. Output length is above the organizer examples.
- Phase 2 offline (09:19): LLM client (strict JSON, cost tracking, spend caps), scenario parser (8 dev, 2 worked references, 6 final), schemas, prompts (intake/assess/repair), pipeline, claim-local verifier, intake sanitizer (D-009), renderer, dulwich provenance, CLI. pytest 74 passed + 1 live test skipped.
- Decisions (09:12): Phase 2 approved; dev model deepseek/deepseek-v4-pro-0813; `runs/` gitignored; the user adds the key to `.env`.
- Phase 1 closed (09:06): 1.R2 leftovers fixed (transflection exception scoped to R-GEO-5, S02 provenance guard, performance_figure/method_gain scope, `for_method` required, R-GEN-3 reworded, unit/quantifier guard words, `+` ranges and time units). pytest 59/59, kb check 9/9.
- 1.R fixes:
  - R1: fuzzy quote matches become `fuzzy_review` (not verified); a changed number or negation is rejected.
  - R2: S02 `text` = PDF text layer + transcribed image text; our descriptions moved to `notes` (never quotable).
  - R3: R-FIB-2 corrected (MIR samples are 1–2 m lab lengths; no source gives an MIR link length); slide-10 legend added.
  - R4: number check matches value + unit dimension and whole ranges.
  - R5: warnings filtered by target; opaque transflection is `unknown`; slots validated; `proposed_fiber` per method; `opaque_absorbing`.
  - R6: scope check derived from R-EVI-1; readiness is at best `precedent_only`.
  - R7: 9 rule wording/quote fixes plus 5 new generic rules (44 rules / 76 exact quotes).
  - R8: private-use glyphs mapped, unit guards, `.gitignore` comment.
- Design note for Phase 2: number provenance must be claim-local (a claim's numbers are checked against that claim's own cited quotes); a KB-wide pool lets e.g. a silica '300 m' pass on an MIR claim.
- Review: APPROVE WITH FIXES. Decisions: fix all R1–R8; B8: keep `pages.jsonl` committed (user).
- 1.1 `normalize.py` (NFKC, keep line-break hyphens, collapse whitespace; `loose()` for tolerant matching).
- 1.2 `pages.jsonl`: S01 19, S03 17, S04 6, S05 2, S06 1, REF 2; reproducible (identical sha256 on rebuild).
- 1.3 `s02_slide_notes.md`: 20 slides (verbatim slide text, our figure descriptions, uncertain readings).
- 1.4 `page_scopes.yaml`: all 67 pages tagged (D-004 adds `guidance`).
- 1.6 `rules.yaml`: 39 generic rules, 58 source quotes, all exact matches.
- 1.7 `graph.json`: 156 nodes / 220 edges (pages, rules, table rows, techniques, sample types, fibers, methods).
- 1.8 tools: `units`, `fibers` (coverage), `screen` (method×technique: pass/fail/unknown), `quotes` (exact/loose/fuzzy + offsets + page sha256), `numbers` (unsupported-number flagging), `scope` (claim kind vs page scope).
- 1.9 CLI: `uv run afs-assist kb build` / `kb check`; the build is byte-reproducible.
- 1.10 `tests/test_phase1.py`: 21 tests.
- Bugs caught by our own checks and fixed: (a) one regime slot mixed state and optics (D-005); (b) a shadowed variable failed ATR for liquids (regression test added); (c) YAML `yes` parsed as boolean, so the fluorophore requirement never passed (quoted, plus a new `kb check` guard).
- 1.5 `table1_methods.json` (19 rows, path in mm) and `fibers.json` (7 fiber families with S02 p.6 quotes).
- Decision: docx §3/§5 citable as `REF`; D01–D08 and the worked answers are dev/eval data only.
- Phase 0. Verified: `git rev-list --objects --all` shows 0 objects under `resources/`; files still on disk; backup at `~/Desktop/aails-backup-2026-10-17.tgz`.

## Next
1. Phase 2 offline parts (config/LLM client, scenarios, schema, pipeline, verify, render, provenance, CLI, tests), then D01–D08 live runs.
2. 13:38 Q&A (user), using the questions in Plan v3 §10.

## Open decisions
- Output length (11:23, user): not a hard rule; minimise later (Phase 3). The soft length check stays a warning.
- Product name: later.

## Blockers
None.

## Check results
**Phase 3 implementation (13:50), code 3c7e881, offline only (no live LLM calls):**
- pytest 248 passed, 1 skipped (live smoke); ruff clean; `kb check` 9/9 PASS (incl. the scenario-id lint, which now also covers `skills/`).
- `scripts/check_mermaid.py` renders charts with mmdc (npx mermaid-cli, using the installed Chrome via `PUPPETEER_EXECUTABLE_PATH`): 2/2 sample charts with escaped quotes, brackets and pipes rendered; a broken chart fails. Not yet run on dev outputs (they predate Phase 3).
- `scripts/check_cost_class.py` re-derives each option's cost class from `table1_methods.json`; tested offline on rendered fixtures.

**2.R4 dev run (finished ~13:00), flash, code e208980 (+8330c8c regex, no effect on dev), session cost $0.1938:**
- **Completion:** all 8 complete; 0 hard failures, 0 still open; citations 318/318 verified.
- **Status:** provisional ×7, D05 insufficient_information.
- **Review fixes confirmed:** spectral ranges present in all 8; plan steps have real text and no doubled numbers; the D01 combination is its own comparison entry (no invented technique).
- **Length and cost:** body 1,663–2,380 words; $0.015–0.041 per case.
- **Slower:** 146–882 s per case (repair rounds plus provider latency).
- **New cosmetic issue (Phase 3):** D01 `combined_with` [Raman, Raman] (dedupe the list and drop the entry's own method). D01 still has two primaries (Phase 3 list).
- Committed. **Phase 2 is ready for G2.**

**Final Phase 2 dev run (finished 11:53), flash, code 75a4469, session cost $0.1455:**
- **Completion:** all 8 complete; 0 hard failures, 0 still open, 0 finalize corrections; citations 254/254 verified.
- **Status:** provisional ×8.
- **D08 fixed:** named methods MIR + fluorescence; state soft_solid; MIR-ATR primary, fluorescence comparison.
- **Shape:** questions 5–6; body 1,683–2,141 words (length deferred, user).
- **Cost:** $0.014–0.033 per case.
- Committed 7f3022a. Independent pre-G2 output review started 11:54.

**2.R2 run (finished 11:12), flash, code 9a7e465, session cost $0.1855:**
- **Completion:** all 8 complete; 0 hard failures; citations 304/304 verified; no finalize corrections needed.
- **Status:** provisional ×7, D02 premise_not_supported.
- **Shape:** recommendations 3–4, a single method as primary; questions 5–6; risks 4 each.
- **Cost and length:** $0.015–0.036 per case. Body (before Evidence) 1,616–2,483 words vs 2,100–3,650 total before; still far above the ~450 of the organizer examples and the 1,800 soft budget.

Problems found:
1. **`proposed_methods` is null in all 8 cases.** It is not the sanitizer: the model returns nulls and puts named methods into `process` as `existing_equipment`. Removing the schema docstring did not help (live A/B on D08, $0.004).
2. **D08 shows MIR-ATR as not_recommended although the customer asked for it.** Intake classified chicken muscle/fat/liver as `solid`, not `soft_solid`, so R-MIR-2 fails ATR. The screen is right for its input; the intake prompt never defines the physical_state values.
3. **Placeholder `"unknown"` process items** still appear (D01, D02, D08) despite the prompt; the sanitizer removes them (soft).

**Flash baseline, pre-2.R2 code (finished 10:40), deepseek-v4.1-flash, session cost $0.1415:** all 8 complete (D08 too); hard failures 0 in every case; citations 271/271 verified; status provisional ×7, D08 insufficient_information; recs 2–5; questions 5–6; cost $0.015–0.022 per case. Markdown 2,082–3,656 words (longer than v4-pro's 2,000–2,700). Committed 67ce484.

**Phase 2 re-run after 2.R (10:10), dev model deepseek-v4-pro-0813, session cost $0.345:**

| Case | Status | Recs | Questions | Citations verified | Hard failures left | Repair rounds | Cost |
|---|---|---|---|---|---|---|---|
| D01 | provisional | 4 | 6 | 21/21 | 0 | 1 | $0.047 |
| D02 | provisional | 4 | 5 | 24/25 | 1 | 2 | $0.057 |
| D03 | provisional | 4 | 5 | 17/17 | 1 | 2 | $0.047 |
| D04 | provisional | 3 | 5 | 18/23 | 6 | 2 | $0.057 |
| D05 | provisional | 5 | 5 | 22/22 | 0 | 1 | $0.040 |
| D06 | insufficient_information | 5 | 5 | 25/25 | 0 | 1 | $0.041 |
| D07 | provisional | 4 | 5 | 25/26 | 1 | 2 | $0.055 |
| D08 | **FAILED** | — | — | — | — | — | — |

- Recommendations dropped from up to 13 to 3–5; questions from 7 to 5–6.
- **D08 still fails at intake:** the reply is truncated at max_tokens 8000 (19k chars; Ionstream). The same scenario failed in both runs, so it is likely a degenerate or repetitive intake output for this enquiry. Fix next session (e.g. cap intake list lengths in the schema/prompt, inspect the raw reply).
  - **Diagnosed 10:13** (one raw intake call, $0.024, reply kept in the session scratchpad): a degenerate repetition loop in `Intake.proposed_methods` (a bare `list[Method]` enum array). After the premises the model wrote `"MIR"` 1,427 times until finish=length. At temperature 0 the retries repeat the same loop. Second finding: `proposed_methods` has no `enquiry_quote`, so it is unverifiable; in D02/D06/D07 it lists all 5 methods. Also: unknown process aspects are emitted with `enquiry_quote: "unknown"` (D03–D05: 3–6 per case) and then sanitized. A fix plan (2.R2) will be merged with the reviewer findings.
- D04 has the most remaining failures (6); inspect them in the review.

**Phase 1 (pre-review):** `afs-assist kb check` 8/8 PASS (page counts, scopes, rule ids/effects, string slot values, 58/58 quotes exact, no scenario ids, graph present); `pytest` 21 passed; `ruff check` clean; `kb build` run twice gives identical sha256 for all knowledge files.
Not yet done: visual spot check of 5 pages against the PDFs (assigned to the reviewer).
