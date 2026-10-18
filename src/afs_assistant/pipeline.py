"""The assessment pipeline: intake -> screen -> assess -> verify -> repair -> finalize.

AFS-Ashby steps 0-2 (LLM intake), 3-4 (deterministic screening and fiber coverage),
5-8 (LLM assessment over the full page-tagged knowledge base), then deterministic
verification with at most MAX_REPAIR_ROUNDS repair calls; the round with the fewest
hard failures is kept. Finalize never shows an unverified citation as verified: failing
citations are removed, items that lost one or failed a number check are flagged, and
duplicates, screen violations and inconsistent status are fixed deterministically.
With `external` set to live or cache, the external-evidence step (Phase 4) runs after
finalize; it adds a separate secondary block and never changes the assessment.
An off-topic enquiry (intake route only `out_of_scope` and no measurement target) stops
after the intake with a short redirect and example questions (no screen/assess/external).
"""

from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from functools import cache, lru_cache

from afs_assistant import activity, kb, paths, quotes
from afs_assistant.external import step as external_step
from afs_assistant.llm import RunCancelled, config_provenance
from afs_assistant.methods import named_methods
from afs_assistant.options import method_label
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import UNKNOWN, Candidate, screen
from afs_assistant.verify import (
    METHOD_ADDED_FLAG,
    PROPOSAL_CHANGED_FLAG,
    QUESTION_ADDED_FLAG,
    RECOMMENDED_ROLES,
    TEXT_FOR_OTHER_OPTION_FLAG,
    TIER_SWAPPED_FLAG,
    Report,
    check_questions,
    check_status,
    extended_methods,
    intake_problems,
    normalize_affects,
    normalized_combined_with,
    recheck,
    recommendation_key,
    sanitize_intake,
    verify,
)

MAX_REPAIR_ROUNDS = 2
# Finalize fallbacks (5.R1, D-047, D-061) for structure failures a repair may leave open.
FALLBACK_CHECKS = ("questions_for_unknowns", "extended_two_methods", "proposal_is_recommended")
FALLBACK_QUESTIONS = 3
FALLBACK_WHY = "Listed as a key unknown in this assessment; the answer may change the status."
MAX_INTAKE_ATTEMPTS = 2      # a collapsed intake is retried once, then the case fails (3.R3 B1)
# Highest role first: a duplicate method+technique (+combination) keeps the entry with the best role.
ROLE_RANK = {"primary": 0, "comparison": 1, "conditional": 2, "not_recommended": 3}
PROMPTS = paths.ROOT / "prompts"
SKILLS = paths.ROOT / "skills"
# Skills loaded into the assess context (progressive guidance, our words with source page refs).
ASSESS_SKILLS = ("multi-method-fusion",)
# Off-topic redirect (D-039, D-040): one polite line and generic example questions, our own words.
OFF_TOPIC_MESSAGE = ("Thank you for your message; this assistant answers in-line spectroscopy and process-measurement "
                     "enquiries, such as which optical method, probe and fiber link could measure a property of a "
                     "material in a running process.")
OFF_TOPIC_EXAMPLES = (
    ("Could we follow the concentration of a dissolved component in a liquid flowing through a pipe, and which "
     "spectroscopic method should we test first?"),
    "Is NIR or Raman spectroscopy better suited to monitor a reaction in a stirred vessel at elevated temperature?",
    "Which probe and fiber setup suits an in-line measurement when the analyzer must stand far from the process point?",
)


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


# Generic measurement words (5.0.R): an enquiry using any of them is never treated as off-topic.
MEASUREMENT_CUE = re.compile(r"measur|monitor|spectr|analy[sz]|sensor|probe|fib(?:er|re)|in-?line|concentrat|"
                             r"calibrat|absorb|wavelength|reactor|pipe|process|\bNIR|\bRaman\b|FT-?IR|\bUV",
                             re.IGNORECASE)
_SAMPLE_SLOTS = ("physical_state", "optical_regime", "aqueous", "heterogeneous", "fluorophore")


def is_off_topic(intake: Intake, removed: list[dict], enquiry: str) -> bool:
    """Off-topic only on strict evidence (5.0.R): the model routed it only `out_of_scope`, and nothing in
    the intake or the enquiry hints at a measurement. Any target, process detail, premise, sample slot or
    proposed fiber (kept, or removed by the quote check), a named method or a generic measurement word
    sends the enquiry through the full assessment. Stated facts alone do not count."""
    return (set(intake.routes) == {"out_of_scope"}
            and not intake.targets and not intake.process and not intake.customer_premises
            and all(getattr(intake.sample, name).value == "unknown" for name in _SAMPLE_SLOTS)
            and intake.proposed_fiber.family == "none"
            and not any(not r["location"].startswith("intake.facts_stated") for r in removed)
            and not named_methods(enquiry)
            and not MEASUREMENT_CUE.search(enquiry))


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
    assessment_raw: Assessment | None       # None only for an off-topic run (no assessment made)
    assessment: Assessment | None
    report: Report | None
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
    off_topic: dict | None = None  # {"message", "examples"} when the run stopped after the intake


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
    Deterministic fallbacks (5.R1): before step 1, a second method for a one-method extended option
    (`_fallback_extended`); after the options are finalized, the proposal follows the recommended
    tier (`_fallback_proposal`, D-061); after step 5, questions from the key unknowns (`_fallback_questions`).
    Locations in the change log use the numbering of `a`. Returns the assessment, the
    change log and the flagged items (path in the returned assessment -> reason) that
    render marks with a warning: items that lost a citation or failed a number check.
    """
    bad = {c["location"] for c in report.citations if not c["verified"]}
    removed: list[dict] = []
    flagged: dict[str, str] = {}
    data = json.loads(a.model_dump_json())
    _fallback_extended(a, data, candidates, removed, flagged)

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
    _fallback_proposal(data, removed, flagged)
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
    _fallback_questions(data, report, removed, flagged)
    return Assessment.model_validate(data), removed, flagged


def _question_text(unknown: str) -> str:
    """A fallback question from a key unknown: its first letter lower-cased unless the first word is an
    acronym (two or more capitals), its end punctuation replaced by a question mark."""
    text = unknown.strip().rstrip(".;:!? ")
    first = text.split()[0] if text else ""
    if sum(ch.isupper() for ch in first) < 2:
        text = text[:1].lower() + text[1:]
    return f"Could you tell us more about this open point: {text}?"


def _fallback_questions(data: dict, report: Report, removed: list[dict], flagged: dict[str, str]) -> None:
    """Fallback (5.R1 a), on the final data after the status step: no clarification question while key
    unknowns are open or the status is not provisional -> up to FALLBACK_QUESTIONS questions from the
    first key unknowns (skipping one with an unsupported figure), `affects` ["status"]. Logged in
    `removed` (`corrects`: questions_for_unknowns) and flagged. Without a usable unknown nothing changes."""
    probe = Report()
    check_questions(Assessment.model_validate(data), probe)
    if not probe.hard_failures:
        return
    bad = {c.location for c in report.hard_failures if c.name == "numbers_uncited_text"}
    usable = [(i, t) for i, t in enumerate(data["key_unknowns"])
              if t.strip() and f"key_unknowns[{i}]" not in bad][:FALLBACK_QUESTIONS]
    for n, (i, text) in enumerate(usable):
        q = {"id": f"Q{n + 1}", "question": _question_text(text), "why_it_matters": FALLBACK_WHY,
             "affects": ["status"]}
        data["clarification_questions"].append(q)
        removed.append({"location": f"clarification_questions[{n}]", "item": q,
                        "reason": f"no clarification question while key unknowns are open or the status is not "
                                  f"provisional; question added from key_unknowns[{i}]",
                        "corrects": "questions_for_unknowns"})
        flagged[f"clarification_questions[{n}]"] = QUESTION_ADDED_FLAG


def _fallback_extended(a: Assessment, data: dict, candidates: list[Candidate], removed: list[dict],
                       flagged: dict[str, str]) -> None:
    """Fallback (5.R1 b), before any removal: an extended option with fewer than two different methods
    gets the first recommendation, in role order (primary, comparison, conditional), that survives the
    screen, brings a method the option does not use yet, and keeps the option's set of recommendations
    distinct from the other options'. Otherwise nothing changes. Logged (`corrects`:
    extended_two_methods) and flagged; finalize's later steps treat the added reference like the model's."""
    status = {(c.method, c.technique): c.status for c in candidates}
    # Entries that finalize keeps recommended (the screen step demotes a failed candidate).
    kept = {r.id: r for r in a.recommendations
            if r.role in RECOMMENDED_ROLES and status.get((r.method, r.technique)) != "fail"}
    ordered = sorted(kept.values(), key=lambda r: ROLE_RANK[r.role])     # stable: list order within a role
    others = [frozenset(o.recommendation_ids) for o in a.solution_options]
    for i, o in enumerate(a.solution_options):
        if o.tier != "extended":
            continue
        methods = extended_methods(o, kept)
        if len(methods) >= 2:
            continue
        pick = next((r for r in ordered if r.method not in methods and r.id not in o.recommendation_ids
                     and frozenset([*o.recommendation_ids, r.id]) not in others[:i] + others[i + 1:]), None)
        if pick is None:
            continue
        refs = [*o.recommendation_ids, pick.id]
        data["solution_options"][i]["recommendation_ids"] = refs
        removed.append({"location": f"solution_options[{i}].recommendation_ids", "item": list(o.recommendation_ids),
                        "reason": f"extended option {o.id} used {methods} only; {pick.role} {pick.id} "
                                  f"({pick.method}) added as a second method", "corrects": "extended_two_methods"})
        flagged[f"solution_options[{i}]"] = METHOD_ADDED_FLAG


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


def _fallback_proposal(data: dict, removed: list[dict], flagged: dict[str, str]) -> None:
    """Fallback (D-061a), on the finalized options: the proposal and the single `recommended` tier must name
    the same option. The brief answer and next step argue for the proposed option, so the tier follows the
    proposal: a proposed `simple` option swaps tiers with the recommended one. A proposed `extended` option
    keeps its tier (it carries the fusion note); the proposal then moves to the recommended option and the
    brief answer and next step are flagged as written for the other option. A missing proposed option or no
    single recommended option stays a visible check failure. Logged (`corrects`: proposal_is_recommended)."""
    proposal, options = data["proposal"], data["solution_options"]
    by_id = {o["id"]: (i, o) for i, o in enumerate(options)}
    recommended = [o["id"] for o in options if o["tier"] == "recommended"]
    best = proposal["best_current_option"]
    if best not in by_id or len(recommended) != 1 or best in recommended:
        return
    (i, chosen), (j, old) = by_id[best], by_id[recommended[0]]
    if chosen["tier"] == "simple":
        removed.append({"location": f"solution_options[{i}].tier", "item": "simple",
                        "reason": f"proposed option {best} had tier simple; tiers swapped with {old['id']} so the "
                                  f"recommended option is the proposed one", "corrects": "proposal_is_recommended"})
        chosen["tier"], old["tier"] = "recommended", "simple"
        flagged[f"solution_options[{i}]"] = flagged[f"solution_options[{j}]"] = TIER_SWAPPED_FLAG
        return
    removed.append({"location": "proposal.best_current_option", "item": best,
                    "reason": f"proposed option {best} is the extended option; changed to the recommended option "
                              f"{old['id']}", "corrects": "proposal_is_recommended"})
    proposal["best_current_option"] = old["id"]
    flagged["proposal"] = PROPOSAL_CHANGED_FLAG
    flagged["brief_answer"] = flagged["proposal.next_step"] = TEXT_FOR_OTHER_OPTION_FLAG


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
        first_call = len(tracker.run_calls)
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
        # Only the first attempt may stop the run as off-topic (it has no target by design: no retry). A
        # retry follows an attempt that was not off-topic, so the enquiry is assessed whatever it says (5.0.R).
        off_topic = attempt == 1 and is_off_topic(intake, intake_removed, enquiry)
        if not problems or off_topic:
            break
    intake, intake_removed, problems = best_intake
    lap("intake")
    _note_intake(intake, enquiry)
    if off_topic:
        timings["wall"] = round(time.monotonic() - wall, 3)
        calls = tracker.run_calls[first_call:] if tracker is not None else []
        manifest = _manifest(run_id, calls, attempt, problems, [], None, timings, None)
        manifest["off_topic"] = True
        return RunResult(run_id, enquiry, intake, {}, [], None, None, None, [], [], intake_removed, calls,
                         manifest, {}, timings, named_methods(enquiry), [], None,
                         {"message": OFF_TOPIC_MESSAGE, "examples": list(OFF_TOPIC_EXAMPLES)})
    slots = slots_from_intake(intake)
    candidates = screen(slots)
    lap("screen")
    _note_screen(candidates)

    system = assess_system()
    base_user = _assess_user(enquiry, intake, candidates)
    res = client.complete_json("assess", system, base_user, "assessment", Assessment.model_json_schema())
    raw = Assessment.model_validate(res.data)
    lap("assess")
    current, report = raw, verify(enquiry, intake, raw, candidates, slots, intake_removed)
    lap("verify")
    _note_verify(report)
    best, best_report, best_round = current, report, 0

    repairs = []
    for round_no in range(1, MAX_REPAIR_ROUNDS + 1):
        if report.passed:
            break
        activity.note(f"Repair round {round_no}: sending the failed checks back to the model.")
        res = client.complete_json("repair", system + "\n\n" + prompt("repair"),
                                   _repair_user(current, report, base_user), "assessment",
                                   Assessment.model_json_schema())
        repairs.append({"round": round_no, "hard_failures_before": len(report.hard_failures)})
        current = Assessment.model_validate(res.data)
        lap("repair")
        report = verify(enquiry, intake, current, candidates, slots, intake_removed)
        lap("verify")
        _note_verify(report)
        repairs[-1]["hard_failures_after"] = len(report.hard_failures)
        repairs[-1]["assessment"] = json.loads(current.model_dump_json())
        if len(report.hard_failures) <= len(best_report.hard_failures):   # ties: the later round
            best, best_report, best_round = current, report, round_no

    final, removed, flagged = finalize(best, best_report, candidates)
    still_failing = recheck(final, candidates).hard_failures
    lap("finalize")
    if removed:
        activity.note(f"Final check: {activity.plural(len(removed), 'unsupported item')} removed or corrected.")
    ext = None
    if external != "off":      # the primary result is complete here; no failure of the step may discard it
        try:
            ext = external_step.run(intake, final, client, external, fetcher=fetcher, enquiry=enquiry)
        except RunCancelled:            # Ctrl-C on a set run: stop the case, write nothing
            raise
        except Exception as exc:        # noqa: BLE001 - malformed API data, cache I/O, extractor bugs, ...
            ext = external_step.failed_block(final, external, f"external step failed: {type(exc).__name__}")
        lap("external")
    timings["wall"] = round(time.monotonic() - wall, 3)
    calls = tracker.run_calls[first_call:] if tracker is not None else []
    manifest = _manifest(run_id, calls, attempt, problems, repairs, best_round, timings, best_report)
    manifest["finalize_fallbacks"] = list(dict.fromkeys(x["corrects"] for x in removed
                                                        if x.get("corrects") in FALLBACK_CHECKS))
    if ext is not None:
        manifest["prompt_sha256"].update(ext["prompt_sha256"])
        manifest["external_mode"] = external
        manifest["external_library_sha256"] = ext["library_sha256"]
    return RunResult(run_id, enquiry, intake, slots, candidates, raw, final, best_report, repairs, removed,
                     intake_removed, calls, manifest, flagged, timings, named_methods(enquiry), still_failing,
                     ext)


@activity.quiet
def _note_intake(intake: Intake, enquiry: str) -> None:
    targets = ", ".join(t.variable for t in intake.targets[:3]) or "no clear target yet"
    sample = [v.replace("_", " ") for v in (intake.sample.physical_state.value, intake.sample.optical_regime.value)
              if v != "unknown"]
    activity.note(f"Understood: target {targets}" + (f"; sample {', '.join(sample)}." if sample else "."))
    named = named_methods(enquiry)
    if named:
        activity.note("Methods named in the enquiry: " + ", ".join(sorted(named)) + ".")
    if intake.unknowns:
        activity.note(f"{activity.plural(len(intake.unknowns), 'open point')} to ask about or assume.")


@activity.quiet
def _note_screen(candidates: list[Candidate]) -> None:
    counts = {k: sum(1 for c in candidates if c.status == k) for k in ("pass", "unknown", "fail")}
    activity.note(f"Screened {activity.plural(len(candidates), 'method and probe option')} against the AFS rules: "
                  f"{counts['pass']} feasible, {counts['unknown']} uncertain, {counts['fail']} ruled out.")
    for c in [c for c in candidates if c.status == "fail"][:2]:
        why = next((r["message"] for r in c.reasons if r["status"] == "fail"), "a rule failed")
        why = re.sub(r"\[([^\]]*)\]", lambda m: m.group(1).replace("'", ""), why)     # "['a', 'b']" -> "a, b"
        activity.note(f"Ruled out {method_label(c.method, c.technique)}: {why[:120]}")


@activity.quiet
def _note_verify(report) -> None:
    total = len(report.citations)
    ok = sum(1 for c in report.citations if c["verified"])
    hard = len(report.hard_failures)
    activity.note(f"Checked {activity.plural(total, 'citation')} against the AFS documents: {ok} verified "
                  "(quote and page scope); "
                  + (f"{activity.plural(hard, 'hard check')} failing." if hard else "no hard failures."))


def _manifest(run_id: str, calls: list[dict], attempts: int, problems: list[str], repairs: list[dict],
              best_round: int | None, timings: dict[str, float], report: Report | None) -> dict:
    """Run metadata; `report` is None (verification null) for an off-topic run."""
    return {
        "run_id": run_id,
        "created_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        "models": sorted({c["model"] for c in calls}),
        "models_config": config_provenance(),
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
        "intake_attempts": attempts,
        "intake_problems": problems,
        "repair_rounds": len(repairs),
        "kept_round": best_round,
        "timings_s": timings,
        "verification": report.summary() if report is not None else None,
    }
