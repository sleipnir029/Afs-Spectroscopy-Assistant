"""The assessment pipeline: intake -> screen -> assess -> verify -> repair -> finalize.

AFS-Ashby steps 0-2 (LLM intake), 3-4 (deterministic screening and fiber coverage),
5-8 (LLM assessment over the full page-tagged knowledge base), then deterministic
verification with at most MAX_REPAIR_ROUNDS repair calls; the round with the fewest
hard failures is kept. Finalize never shows an unverified citation as verified: failing
citations are removed, items that lost one or failed a number check are flagged, and
duplicates, screen violations and inconsistent status are fixed deterministically.
With `external` set to live or cache, the external-evidence step (Phase 4) runs after
finalize; it adds a separate secondary block and never changes the assessment.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cache, lru_cache

from afs_assistant import kb, paths, quotes
from afs_assistant.external import step as external_step
from afs_assistant.methods import named_methods
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import UNKNOWN, Candidate, screen
from afs_assistant.verify import (
    Report,
    check_status,
    intake_problems,
    normalize_affects,
    normalized_combined_with,
    recheck,
    recommendation_key,
    sanitize_intake,
    verify,
)

MAX_REPAIR_ROUNDS = 2
MAX_INTAKE_ATTEMPTS = 2      # a collapsed intake is retried once, then the case fails (3.R3 B1)
# Highest role first: a duplicate method+technique (+combination) keeps the entry with the best role.
ROLE_RANK = {"primary": 0, "comparison": 1, "conditional": 2, "not_recommended": 3}
PROMPTS = paths.ROOT / "prompts"
SKILLS = paths.ROOT / "skills"
# Skills loaded into the assess context (progressive guidance, our words with source page refs).
ASSESS_SKILLS = ("multi-method-fusion",)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@cache
def prompt(name: str) -> str:
    return (PROMPTS / f"{name}.md").read_text(encoding="utf-8")


@cache
def skill(name: str) -> str:
    return (SKILLS / f"{name}.md").read_text(encoding="utf-8")


def assess_system() -> str:
    """Assess prompt + skills + the knowledge block (stable prefix, cacheable)."""
    skills = "\n\n".join(f"# SKILL: {name}\n{skill(name)}" for name in ASSESS_SKILLS)
    return prompt("assess") + "\n\n" + skills + "\n\n" + knowledge_block()


@lru_cache(maxsize=1)
def knowledge_block() -> str:
    """All source pages (quotable text only) and the rule list, as one stable, cacheable block."""
    lines = ["# SOURCE PAGES",
             "Each page starts with a header line [DOC p.N | scope | title]. Quote only from the text after the header."]
    for (doc, number), rec in kb.pages().items():
        label = kb.citation_label(doc, number)
        lines.append(f"\n[{label} | scope: {', '.join(rec['scope'])} | {rec['title']}]\n{rec['text']}")
    lines.append("\n# RULES (curated from the sources; cite the underlying page, not the rule)\n"
                 "Each rule statement is our paraphrase: never quote it. To cite a rule, quote one of its "
                 "verbatim source passages listed below it, with that passage's label.")
    for r in kb.rules():
        lines.append(f"[{r['id']}] ({r['effect']}) paraphrase, never quote this: {r['statement']}")
        lines += [f'  source [{kb.citation_label(s["doc"], s["page"])}]: "{s["quote"]}"' for s in r["sources"]]
    return "\n".join(lines)


def slots_from_intake(intake: Intake) -> dict:
    slots: dict = {}
    for name in ("physical_state", "optical_regime", "aqueous", "heterogeneous", "fluorophore"):
        value = getattr(intake.sample, name).value
        slots[name] = value if value != "unknown" else UNKNOWN
    f = intake.proposed_fiber
    if f.family != "none" and f.for_method != "none":
        slots["proposed_fiber"] = {"family": f.family, "for_method": f.for_method}
    # A distance or remote analyzer stated or asked about makes link-length limits relevant (R-FIB-2).
    if any(p.aspect == "distance_or_remote_analyzer" for p in intake.process):
        slots["remote_distance"] = "yes"
    return slots


def screening_table(candidates: list[Candidate]) -> str:
    rows = ["# SCREENING (deterministic; method x in-line technique)",
            "status | method | technique | reasons | warnings (rule ids) | notes"]
    for c in candidates:
        reasons = "; ".join(f"{r['rule']}: {r['message']}" for r in c.reasons) or "-"
        rows.append(f"{c.status} | {c.method} | {c.technique} | {reasons} | {', '.join(c.warnings) or '-'} | "
                    f"{' '.join(c.notes) or '-'}")
    return "\n".join(rows)


@dataclass
class RunResult:
    run_id: str
    enquiry: str
    intake: Intake
    slots: dict
    candidates: list[Candidate]
    assessment_raw: Assessment
    assessment: Assessment
    report: Report
    repairs: list[dict] = field(default_factory=list)
    removed: list[dict] = field(default_factory=list)
    intake_removed: list[dict] = field(default_factory=list)
    calls: list[dict] = field(default_factory=list)
    manifest: dict = field(default_factory=dict)
    flagged: dict[str, str] = field(default_factory=dict)    # item path -> why it is shown with a warning
    timings: dict[str, float] = field(default_factory=dict)  # seconds per stage, plus wall
    named_methods: dict[str, str] = field(default_factory=dict)  # method -> enquiry span naming it
    recheck: list = field(default_factory=list)  # option/proposal/premise checks failing on the final assessment
    external: dict | None = None  # secondary external evidence (Phase 4); None when the step is off


def _assess_user(enquiry: str, intake: Intake, candidates: list[Candidate]) -> str:
    named = named_methods(enquiry)
    return "\n\n".join([
        "# CUSTOMER ENQUIRY (everything the customer said)\n" + enquiry,
        "# INTAKE (steps 0-2)\n" + intake.model_dump_json(indent=1),
        "# METHODS NAMED IN THE ENQUIRY (found by word list; judge whether the customer proposes them)\n"
        + (", ".join(f'{m} ("{q}")' for m, q in named.items()) or "none"),
        screening_table(candidates),
    ])


def _repair_user(previous: Assessment, report: Report, base_user: str) -> str:
    # For near-miss quotes, show the closest page passage (repair prompt only, never the user output).
    hints = {}
    for c in report.citations:
        if c["quote_status"] == "fuzzy_review":
            q = quotes.verify(c["doc"], c["page"], c["quote"])
            if q.start is not None:
                text = kb.page(c["doc"], c["page"])["text"]
                hints[c["location"]] = f'; closest passage on that page: "{text[q.start:q.end]}"'
    failures = "\n".join(f"- [{c.name}] {c.location}: {c.message}"
                         f"{hints.get(c.location, '') if c.name == 'quote_verified' else ''}"
                         for c in report.hard_failures)
    return "\n\n".join([base_user, "# YOUR PREVIOUS ASSESSMENT\n" + previous.model_dump_json(indent=1),
                        "# VERIFICATION FAILURES TO FIX\n" + failures])


def finalize(a: Assessment, report: Report,
             candidates: list[Candidate]) -> tuple[Assessment, list[dict], dict[str, str]]:
    """Make the kept round safe to show. Every change is recorded in `removed` with a reason.

    1. Remove citations that failed verification.
    2. A recommended entry whose candidate failed screening becomes not_recommended.
    3. Same method+technique (and same combined_with) listed twice: keep the highest role, drop the others.
    4. A `supported` or `contradicted` premise with no citation left becomes `not_covered`.
    5. Status inconsistent with premises -> premise_not_supported; with recommendations
       -> insufficient_information (re-checked on the result of steps 1-4).
    6. Question `affects` items are normalised to the fixed vocabulary; other words are dropped (logged).
    Locations in the change log use the numbering of `a`. Returns the assessment, the
    change log and the flagged items (path in the returned assessment -> reason) that
    render marks with a warning: items that lost a citation or failed a number check.
    """
    bad = {c["location"] for c in report.citations if not c["verified"]}
    removed: list[dict] = []
    flagged: dict[str, str] = {}
    data = json.loads(a.model_dump_json())

    def strip(container: dict, loc: str) -> None:
        kept = []
        for j, cit in enumerate(container.get("citations", [])):
            if f"{loc}.citations[{j}]" in bad:
                removed.append({"location": f"{loc}.citations[{j}]", "citation": cit,
                                "reason": "citation failed verification; removed"})
                flagged[loc] = "a citation failed verification and was removed"
            else:
                kept.append(cit)
        container["citations"] = kept

    for key in ("premise_checks", "recommendations", "spectral_ranges", "risks", "parameters", "solution_options"):
        for i, item in enumerate(data[key]):
            strip(item, f"{key}[{i}]")
    strip(data["measurement_concept"], "measurement_concept")
    for i, step in enumerate(data["feasibility_plan"]["steps"]):
        strip(step, f"feasibility_plan.steps[{i}]")
    for c in report.hard_failures:
        if c.name in ("numbers_claim_local", "numbers_uncited_text"):
            flagged[c.location] = "contains a figure not found in its sources or the enquiry"

    for i, r in enumerate(data["recommendations"]):
        clean = normalized_combined_with(r["method"], r["combined_with"])
        if clean != r["combined_with"]:
            removed.append({"location": f"recommendations[{i}].combined_with", "item": list(r["combined_with"]),
                            "reason": f"combined_with normalised to {clean} (duplicates and the entry's own method "
                                      f"removed)"})
            r["combined_with"] = clean

    status = {(c.method, c.technique): c.status for c in candidates}
    for i, r in enumerate(data["recommendations"]):
        if r["role"] != "not_recommended" and status.get((r["method"], r["technique"])) == "fail":
            removed.append({"location": f"recommendations[{i}]", "item": dict(r),
                            "reason": f"{r['method']} {r['technique']} failed screening; "
                                      f"role {r['role']} changed to not_recommended",
                            "corrects": "respects_screen"})
            flagged[f"recommendations[{i}]"] = "failed screening; changed to not recommended by verification"
            r["role"] = "not_recommended"

    # Dedupe method+technique+combination (stable: on equal role the earlier entry wins), then renumber flags.
    recs = data["recommendations"]
    best: dict[tuple[str, str, tuple[str, ...]], int] = {}
    for i, r in enumerate(recs):
        key = recommendation_key(r["method"], r["technique"], r["combined_with"])
        if key not in best or ROLE_RANK[r["role"]] < ROLE_RANK[recs[best[key]]["role"]]:
            best[key] = i
    keep = sorted(best.values())
    for i, r in enumerate(recs):
        if i not in keep:
            winner = best[recommendation_key(r["method"], r["technique"], r["combined_with"])]
            removed.append({"location": f"recommendations[{i}]", "item": r,
                            "reason": f"duplicate method+technique (and combination); kept recommendations[{winner}] "
                                      f"(role {recs[winner]['role']})",
                            "corrects": "recommendations_unique"})
    new_index = {old: new for new, old in enumerate(keep)}
    renumbered = {}
    for path, why in flagged.items():
        if path.startswith("recommendations["):
            old = int(path[len("recommendations["):path.index("]")])
            if old in new_index:
                renumbered[f"recommendations[{new_index[old]}]{path[path.index(']') + 1:]}"] = why
        else:
            renumbered[path] = why
    flagged = renumbered
    # Option references follow the dedupe: a dropped duplicate's id maps to the kept entry's id.
    id_map = {recs[i]["id"]: recs[best[recommendation_key(recs[i]["method"], recs[i]["technique"],
                                                          recs[i]["combined_with"])]]["id"]
              for i in range(len(recs))}
    for i in keep:                      # a kept entry always keeps its own id (also with duplicate ids)
        id_map[recs[i]["id"]] = recs[i]["id"]
    dropped_roles = {recs[i]["id"]: recs[i]["role"] for i in range(len(recs)) if i not in keep}
    data["recommendations"] = [recs[i] for i in keep]
    _finalize_options(data, id_map, removed, flagged, dropped_roles)
    _finalize_proposal_basis(data, removed, flagged)

    demoted_contradiction = False
    for i, p in enumerate(data["premise_checks"]):
        if p["verdict"] in ("supported", "contradicted", "precedent_only") and not p["citations"]:
            change = {"location": f"premise_checks[{i}]", "item": dict(p),
                      "reason": f"verdict {p['verdict']} without a verified citation; changed to not_covered"}
            if p["verdict"] == "contradicted":
                change["corrects"] = "status_vs_premises"
                flagged[f"premise_checks[{i}]"] = ("contradiction not verified; changed to not covered, "
                                                   "explanation is the model's original")
                demoted_contradiction = True
            removed.append(change)
            p["verdict"] = "not_covered"

    for i, q in enumerate(data["clarification_questions"]):
        kept, dropped = normalize_affects(q["affects"])
        if dropped:      # case and synonym normalisation is silent; only a dropped item is a change (3.R4 N3)
            removed.append({"location": f"clarification_questions[{i}].affects", "item": list(q["affects"]),
                            "reason": f"affects normalised to {kept}; dropped {dropped} (not method, technique, "
                                      f"installation, status, an M id or an O id)"})
        q["affects"] = kept

    interim = Report()
    check_status(Assessment.model_validate(data), interim)
    failed = {c.name for c in interim.hard_failures}
    for name, new_status in (("status_vs_premises", "premise_not_supported"),
                             ("status_vs_recommendations", "insufficient_information")):
        if name in failed and data["decision_status"] == "provisional_assessment":
            removed.append({"location": "decision_status", "item": data["decision_status"],
                            "reason": f"{name} failed; status changed to {new_status}", "corrects": name})
            data["decision_status"] = new_status
            flagged["status_reason"] = "status changed by verification; this reason text is the model's original"
    # The model's own premise_not_supported may rest on a contradiction that failed verification.
    if (demoted_contradiction and data["decision_status"] == "premise_not_supported"
            and not any(p["verdict"] == "contradicted" for p in data["premise_checks"])):
        flagged.setdefault("status_reason", "the contradiction behind this status failed verification")
    return Assessment.model_validate(data), removed, flagged


def _finalize_options(data: dict, id_map: dict[str, str], removed: list[dict], flagged: dict[str, str],
                      dropped_roles: dict[str, str] | None = None) -> None:
    """Keep option references consistent with the finalized recommendations.

    A reference to a deduplicated entry is remapped to the kept entry; a reference to an
    unknown or not_recommended entry is dropped; an option left without references is
    dropped. Fewer than two options, or no recommended tier, stays a visible check failure
    (re-checked on the result). Flags on options are renumbered.
    """
    roles = {r["id"]: r["role"] for r in data["recommendations"]}
    kept_options, new_index = [], {}
    for i, o in enumerate(data["solution_options"]):
        refs = []
        for ref in o["recommendation_ids"]:
            target = id_map.get(ref, ref)
            if roles.get(target, "not_recommended") == "not_recommended":
                why = "not an existing recommendation" if target not in roles else "recommendation is not_recommended"
                removed.append({"location": f"solution_options[{i}].recommendation_ids", "item": ref,
                                "reason": f"reference {ref} dropped ({why})", "corrects": "option_recommendation_refs"})
                continue
            if target != ref:
                old_role = (dropped_roles or {}).get(ref)
                role_note = (f" (role changed from {old_role} to {roles[target]})"
                             if old_role and old_role != roles[target] else "")
                removed.append({"location": f"solution_options[{i}].recommendation_ids", "item": ref,
                                "reason": f"reference {ref} pointed to a removed duplicate; now {target}{role_note}"})
            if target not in refs:
                refs.append(target)
        if not refs:
            removed.append({"location": f"solution_options[{i}]", "item": dict(o),
                            "reason": f"option {o['id']} has no valid recommendation left; dropped",
                            "corrects": "option_has_methods"})
            continue
        if refs != o["recommendation_ids"]:
            flagged[f"solution_options[{i}]"] = "methods changed by verification"
        o["recommendation_ids"] = refs
        new_index[i] = len(kept_options)
        kept_options.append(o)
    renumbered = {}
    for path, why in flagged.items():
        if path.startswith("solution_options["):
            old = int(path[len("solution_options["):path.index("]")])
            if old in new_index:
                renumbered[f"solution_options[{new_index[old]}]{path[path.index(']') + 1:]}"] = why
        else:
            renumbered[path] = why
    flagged.clear()
    flagged.update(renumbered)
    data["solution_options"] = kept_options
    if data["proposal"]["best_current_option"] not in {o["id"] for o in kept_options}:
        flagged["proposal"] = "the proposed option was removed by verification"


def _finalize_proposal_basis(data: dict, removed: list[dict], flagged: dict[str, str]) -> None:
    """`supplied` needs a verified citation behind the proposed option (its own or its recommendations');
    otherwise the basis becomes engineering_judgement (3.R B2). Runs after the citations were stripped."""
    proposal = data["proposal"]
    if proposal["basis"] != "supplied":
        return
    option = next((o for o in data["solution_options"] if o["id"] == proposal["best_current_option"]), None)
    recs = {r["id"]: r for r in data["recommendations"]}
    cited = option is not None and (bool(option["citations"]) or any(
        recs[x]["citations"] for x in option["recommendation_ids"] if x in recs))
    if cited:
        return
    removed.append({"location": "proposal.basis", "item": "supplied", "corrects": "proposal_basis",
                    "reason": "no verified citation behind the proposed option; basis changed to engineering_judgement"})
    proposal["basis"] = "engineering_judgement"
    why = "basis changed to engineering judgement: no verified source behind the proposed option"
    flagged["proposal"] = f"{flagged['proposal']}; {why}" if "proposal" in flagged else why


def run(enquiry: str, client, run_id: str | None = None, external: str = "off", fetcher=None) -> RunResult:
    """One assessment. `external`: off (default) | live | cache; `fetcher` overrides the HTTP fetcher (tests)."""
    run_id = run_id or datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]
    tracker = getattr(client, "tracker", None)
    if tracker is not None:
        tracker.start_run()
        first_call = len(tracker.calls)
    timings: dict[str, float] = {}
    wall = clock = time.monotonic()

    def lap(stage: str) -> None:
        nonlocal clock
        now = time.monotonic()
        timings[stage] = round(timings.get(stage, 0.0) + now - clock, 3)
        clock = now

    # A collapsed intake is retried once; if it still has problems, the attempt with the fewest is kept and
    # the case goes on (a vague enquiry still gets questions and a proposal; verify reports `intake_complete`).
    best_intake = None
    for attempt in range(1, MAX_INTAKE_ATTEMPTS + 1):
        intake_res = client.complete_json("intake", prompt("intake"), "# CUSTOMER ENQUIRY\n" + enquiry,
                                          "intake", Intake.model_json_schema())
        intake, intake_removed = sanitize_intake(Intake.model_validate(intake_res.data), enquiry)
        problems = intake_problems(intake, intake_removed)
        if best_intake is None or len(problems) < len(best_intake[2]):
            best_intake = (intake, intake_removed, problems)
        if not problems:
            break
    intake, intake_removed, problems = best_intake
    lap("intake")
    slots = slots_from_intake(intake)
    candidates = screen(slots)
    lap("screen")

    system = assess_system()
    base_user = _assess_user(enquiry, intake, candidates)
    res = client.complete_json("assess", system, base_user, "assessment", Assessment.model_json_schema())
    raw = Assessment.model_validate(res.data)
    lap("assess")
    current, report = raw, verify(enquiry, intake, raw, candidates, slots, intake_removed)
    lap("verify")
    best, best_report, best_round = current, report, 0

    repairs = []
    for round_no in range(1, MAX_REPAIR_ROUNDS + 1):
        if report.passed:
            break
        res = client.complete_json("repair", system + "\n\n" + prompt("repair"),
                                   _repair_user(current, report, base_user), "assessment",
                                   Assessment.model_json_schema())
        repairs.append({"round": round_no, "hard_failures_before": len(report.hard_failures)})
        current = Assessment.model_validate(res.data)
        lap("repair")
        report = verify(enquiry, intake, current, candidates, slots, intake_removed)
        lap("verify")
        repairs[-1]["hard_failures_after"] = len(report.hard_failures)
        repairs[-1]["assessment"] = json.loads(current.model_dump_json())
        if len(report.hard_failures) <= len(best_report.hard_failures):   # ties: the later round
            best, best_report, best_round = current, report, round_no

    final, removed, flagged = finalize(best, best_report, candidates)
    still_failing = recheck(final, candidates).hard_failures
    lap("finalize")
    ext = None
    if external != "off":
        ext = external_step.run(intake, final, client, external, fetcher=fetcher)
        lap("external")
    timings["wall"] = round(time.monotonic() - wall, 3)
    calls = tracker.calls[first_call:] if tracker is not None else []
    manifest = {
        "run_id": run_id,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "models": sorted({c["model"] for c in calls}),
        "prompt_sha256": {n: sha(prompt(n)) for n in ("intake", "assess", "repair")},
        "skills_sha256": {n: sha(skill(n)) for n in ASSESS_SKILLS},
        "knowledge_sha256": sha(knowledge_block()),
        "pages_sha256": sha(paths.PAGES_FILE.read_text(encoding="utf-8")),
        "rules_sha256": sha(paths.RULES_FILE.read_text(encoding="utf-8")),
        "cost_usd": round(sum(c["cost_usd"] for c in calls), 6),
        "tokens": {"prompt": sum(c["prompt_tokens"] for c in calls),
                   "completion": sum(c["completion_tokens"] for c in calls),
                   "cached": sum(c["cached_tokens"] for c in calls)},
        "calls": len(calls),
        "intake_attempts": attempt,
        "intake_problems": problems,
        "repair_rounds": len(repairs),
        "kept_round": best_round,
        "timings_s": timings,
        "verification": best_report.summary(),
    }
    if ext is not None:
        manifest["prompt_sha256"].update(ext["prompt_sha256"])
        manifest["external_mode"] = external
        manifest["external_library_sha256"] = ext["library_sha256"]
    return RunResult(run_id, enquiry, intake, slots, candidates, raw, final, best_report, repairs, removed,
                     intake_removed, calls, manifest, flagged, timings, named_methods(enquiry), still_failing,
                     ext)
