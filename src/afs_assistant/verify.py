"""Deterministic verification of an assessment (AFS-Ashby post-checks; no LLM).

Pattern from MatSage's verifier: a report of named checks with hard/soft severity.
All checks run against the exact texts the model was shown (normalised page text,
the enquiry). Number checks are claim-local: an item's numbers must come from that
item's own verified quotes or from the enquiry.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from rapidfuzz import fuzz

from afs_assistant import kb, quotes, scope
from afs_assistant.normalize import normalize
from afs_assistant.numbers import unsupported_numbers
from afs_assistant.options import option_methods
from afs_assistant.schema import Assessment, Citation, Intake
from afs_assistant.screen import Candidate

MAX_QUESTIONS = 7
MAX_RECOMMENDATIONS = 5
MAX_WORDS = 1800
RECOMMENDED_ROLES = ("primary", "comparison", "conditional")
MIN_STEP_WORDS = 3
MAX_BRIEF_WORDS = 80
MAX_ANSWER_WORDS = 600       # model-written text shown in the Answer part (two layers, D-022)
ANSWER_QUESTIONS = 3         # the Answer part shows the top questions only
MAX_PREMISES = 3
MIN_OPTIONS, MAX_OPTIONS = 2, 3
# Values a model writes instead of leaving an intake item out; not client facts.
PLACEHOLDERS = {"", "unknown", "n/a", "na", "none", "not stated", "not given", "not specified", "null", "-"}
_BARE_NUMBER = re.compile(r"^\s*\d+[.)]?\s*$")
# A forbidden phrase preceded (within a few words, same clause) by one of these is a cautious negation,
# not a claim. The clause ends at ; , : a dash, a line break, a sentence end, "but", "however" or
# "because". A comma aside directly after an auxiliary negation ("cannot, at this stage, guarantee")
# stays in the clause, as does a dash aside ("cannot - at this stage - guarantee", also with en/em dashes);
# after "no"/"never" neither does ("No, honestly, it will work" is a claim).
# Emphatic idioms ("no doubt") are not negations.
_NEGATION_WORDS = r"(?:not|no|never|cannot|can't|without|nor|neither|isn't|doesn't|don't|won't)"
_ASIDE_WORDS = r"(?:not|cannot|can't|isn't|doesn't|don't|won't)"
_NEGATION_BEFORE = re.compile(rf"\b{_NEGATION_WORDS}\b(?:\W+\w+){{0,6}}\W*$", re.IGNORECASE)
_NEGATION_ASIDE = re.compile(rf"\b({_ASIDE_WORDS})(?:\s*,[^,;.!?]{{1,40}},|\s+[-\u2013\u2014]\s"
                             rf"[^,;.!?\-\u2013\u2014]{{1,40}}\s[-\u2013\u2014](?=\s))", re.IGNORECASE)
_EMPHATIC = re.compile(r"\b(?:no doubt|without (?:a |any )?doubt|no question)\b", re.IGNORECASE)
_CLAUSE_BREAK = re.compile(r"[;,:\n\u2013\u2014]|\s-\s|[.!?](?=[\s\"'\u201d\u2019)\]]|$)|\b(?:but|however|because)\b",
                           re.IGNORECASE)
# A verbatim enquiry quote needs at least this many normalised characters (and a word character).
MIN_ENQUIRY_QUOTE_CHARS = 4
# Any currency sign, code or word: the assistant never states a price (3.R B3). Codes in any case,
# except before a journal abbreviation ("Eur. Urol."): a dot and a capital letter (3.R2 N6, D-028).
PRICE_PATTERN = r"[€$£]|\b(?:eur|usd|gbp|chf)\b(?!\.\s?(?-i:[A-Z]))|\beuros?\b|\bdollars?\b"
# Wording that asserts certainty or commercial facts the sources cannot support (REF §3 "Do not invent").
FORBIDDEN = [
    (re.compile(PRICE_PATTERN, re.IGNORECASE), "price"),
    (re.compile(r"\bguarantee[sd]?\b", re.IGNORECASE), "guarantee"),
    (re.compile(r"\bwill (?:definitely |certainly )?work\b", re.IGNORECASE), "certainty"),
    (re.compile(r"\b(?:is|are) (?:approved|validated|certified|proven) (?:for|to)\b", re.IGNORECASE), "approval claim"),
    (re.compile(r"\bproven to\b|\bready for (?:clinical|surgical|in vivo|production)\b", re.IGNORECASE), "readiness claim"),
    (re.compile(r"\b[A-Z]{2,5}-\d{3,}[A-Z0-9-]*\b"), "product-code-like token"),
]
# Which question wording counts as covering an unknown deciding slot (whole words; \w* marks a stem).
SLOT_WORDS = {
    "physical_state": (r"states?", r"liquids?", r"solids?", r"powders?", r"pastes?", r"form"),
    "optical_regime": (r"clear", r"turbid\w*", r"opaque", r"opacity", r"optical\w*", r"scatter\w*",
                       r"transparen\w*", r"colou?rs?", r"dark\w*"),
    "fluorophore": (r"fluoresc\w*", r"fluorophores?", r"markers?", r"indicators?"),
}
SLOT_PATTERNS = {slot: re.compile(r"\b(?:" + "|".join(words) + r")\b", re.IGNORECASE)
                 for slot, words in SLOT_WORDS.items()}


@dataclass
class Check:
    name: str
    passed: bool
    severity: str          # hard | soft
    location: str          # e.g. recommendations[1].citations[0]
    message: str


@dataclass
class Report:
    checks: list[Check] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)   # per-citation verification (quote + scope)

    @property
    def hard_failures(self) -> list[Check]:
        return [c for c in self.checks if not c.passed and c.severity == "hard"]

    @property
    def soft_failures(self) -> list[Check]:
        return [c for c in self.checks if not c.passed and c.severity == "soft"]

    @property
    def passed(self) -> bool:
        return not self.hard_failures

    def add(self, name: str, ok: bool, severity: str, location: str, message: str = "") -> None:
        self.checks.append(Check(name, ok, severity, location, message if not ok else "ok"))

    def summary(self) -> dict:
        return {"passed": self.passed, "hard_failures": len(self.hard_failures),
                "soft_failures": len(self.soft_failures), "checks": len(self.checks),
                "citations_total": len(self.citations),
                "citations_verified": sum(1 for c in self.citations if c["verified"])}

    def to_dict(self) -> dict:
        return {"summary": self.summary(), "checks": [asdict(c) for c in self.checks], "citations": self.citations}


def _items_with_citations(a: Assessment) -> list[tuple[str, str, list[Citation]]]:
    """(location, item text, citations) for every citation-bearing item."""
    items = []
    for i, p in enumerate(a.premise_checks):
        items.append((f"premise_checks[{i}]", f"{p.premise} {p.explanation}", p.citations))
    for i, r in enumerate(a.recommendations):
        items.append((f"recommendations[{i}]", f"{r.rationale} {r.conditions}", r.citations))
    mc = a.measurement_concept
    items.append(("measurement_concept", f"{mc.probe_and_geometry} {mc.location} {mc.fiber_link}", mc.citations))
    for i, s in enumerate(a.spectral_ranges):
        items.append((f"spectral_ranges[{i}]", s.statement, s.citations))
    for i, r in enumerate(a.risks):
        items.append((f"risks[{i}]", r.risk, r.citations))
    for i, s in enumerate(a.feasibility_plan.steps):
        items.append((f"feasibility_plan.steps[{i}]", f"{s.step} {s.purpose}", s.citations))
    for i, p in enumerate(a.parameters):
        mb = p.measured_by
        items.append((f"parameters[{i}]", " ".join(x for x in (p.name, p.why, mb.sensor, mb.alternative) if x),
                      p.citations))
    for i, o in enumerate(a.solution_options):
        items.append((f"solution_options[{i}]",
                      " ".join(x for x in (o.ease_of_use, o.maintenance, o.performance_fit, o.cost_drivers,
                                           o.fusion_note) if x), o.citations))
    return items


def _new_uncited_texts(a: Assessment) -> list[tuple[str, str]]:
    """Phase 3 text fields without citations: (location, text); null notes are skipped."""
    texts = [("brief_answer", a.brief_answer),
             ("proposal.what_would_change_it", a.proposal.what_would_change_it),
             ("proposal.next_step", a.proposal.next_step)]
    texts += [(name, getattr(a, name)) for name in ("chemometrics_note", "realtime_tracking_note", "future_direction")
              if getattr(a, name)]
    return texts


def _all_text(a: Assessment) -> str:
    parts = [a.status_reason, *a.requirements_stated, *a.key_unknowns, *a.assumptions, *a.not_in_sources,
             a.feasibility_plan.reference_measurements, a.feasibility_plan.decision_basis]
    parts += [text for _, text in _new_uncited_texts(a)]
    parts += [f"{q.question} {q.why_it_matters}" for q in a.clarification_questions]
    parts += [text for _, text, _ in _items_with_citations(a)]
    return "\n".join(parts)


def check_citations(a: Assessment, report: Report) -> dict[str, list[str]]:
    """Quote + scope per citation. Returns verified quote texts per item location."""
    verified: dict[str, list[str]] = {}
    for loc, _text, cits in _items_with_citations(a):
        verified[loc] = []
        for j, c in enumerate(cits):
            where = f"{loc}.citations[{j}]"
            q = quotes.verify(c.doc, c.page, c.quote)
            message = f"{c.doc} p.{c.page}: quote {q.status} (score {q.score})"
            rule = None if q.ok else rule_paraphrased(c.quote)
            if rule is not None:
                sources = "; ".join(f'[{kb.citation_label(x["doc"], x["page"])}] "{x["quote"]}"' for x in rule["sources"])
                message += (f"; this is rule {rule['id']}'s paraphrase, not source text. "
                            f"Quote the source instead: {sources}")
            report.add("quote_verified", q.ok, "hard", where, message)
            sc_status, sc_msg = scope.check(c.claim_kind, c.doc, c.page)
            scope_ok = sc_status != "not_supported"
            report.add("citation_scope", scope_ok, "hard", where, sc_msg)
            if sc_status == "precedent_only":
                report.add("citation_precedent_only", False, "soft", where, sc_msg)
            ok = q.ok and scope_ok
            report.citations.append({"location": where, "doc": c.doc, "page": c.page, "quote": c.quote,
                                     "claim_kind": c.claim_kind, "quote_status": q.status,
                                     "start": q.start if q.ok else None, "end": q.end if q.ok else None,
                                     "page_sha256": q.page_sha256, "scope_status": sc_status, "verified": ok})
            if ok:
                verified[loc].append(c.quote)
    return verified


def _loose(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", normalize(text).lower())


def rule_paraphrased(quote: str) -> dict | None:
    """The rule whose (our-words) statement this quote copies, if any."""
    q = _loose(quote)
    if len(q) < 25:          # a few words; shorter spans match rule wording by chance
        return None
    for rule in kb.rules():
        statement = _loose(rule["statement"])
        if q in statement or fuzz.partial_ratio(q, statement) >= quotes.FUZZY_MIN:
            return rule
    return None


def check_numbers(a: Assessment, enquiry: str, verified: dict[str, list[str]], report: Report) -> None:
    for loc, text, _ in _items_with_citations(a):
        missing = unsupported_numbers(text, verified.get(loc, []) + [enquiry])
        report.add("numbers_claim_local", not missing, "hard", loc,
                   f"figures not in this item's verified quotes or the enquiry: {[n.text for n in missing]}")
    loose_texts = [("status_reason", a.status_reason), ("feasibility_plan.decision_basis", a.feasibility_plan.decision_basis),
                   ("feasibility_plan.reference_measurements", a.feasibility_plan.reference_measurements)]
    loose_texts += [(f"clarification_questions[{i}]", f"{q.question} {q.why_it_matters}")
                    for i, q in enumerate(a.clarification_questions)]
    loose_texts += [(f"assumptions[{i}]", t) for i, t in enumerate(a.assumptions)]
    loose_texts += [(f"requirements_stated[{i}]", t) for i, t in enumerate(a.requirements_stated)]
    loose_texts += [(f"key_unknowns[{i}]", t) for i, t in enumerate(a.key_unknowns)]
    loose_texts += [(f"not_in_sources[{i}]", t) for i, t in enumerate(a.not_in_sources)]
    loose_texts += _new_uncited_texts(a)
    for loc, text in loose_texts:
        missing = unsupported_numbers(text, [enquiry])
        report.add("numbers_uncited_text", not missing, "hard", loc,
                   f"figures in uncited text must come from the enquiry: {[n.text for n in missing]}")


# The field that carries each intake item's content; a placeholder item has a placeholder quote AND value.
INTAKE_VALUE_FIELDS = {"facts_stated": "text", "targets": "variable", "process": "value", "customer_premises": "claim"}


def sanitize_intake(intake: Intake, enquiry: str) -> tuple[Intake, list[dict]]:
    """Remove intake items whose quote is not verbatim in the enquiry (no invented client facts).

    Facts, targets, process details and premises with a bad quote are dropped; a sample
    slot with a bad or missing quote is reset to unknown; a proposed method with a bad
    quote is set to null. A quote must be a real span: at least MIN_ENQUIRY_QUOTE_CHARS
    normalised characters with a word character. Returns the cleaned intake and a record
    of every removal.
    """
    text = normalize(enquiry).lower()

    def ok(span: str | None) -> bool:
        if span is None:
            return False
        span = normalize(span).strip().lower()
        return len(span) >= MIN_ENQUIRY_QUOTE_CHARS and re.search(r"\w", span) is not None and span in text

    data = intake.model_dump()
    removed: list[dict] = []
    for key, value_field in INTAKE_VALUE_FIELDS.items():
        kept = []
        for i, item in enumerate(data[key]):
            if ok(item["enquiry_quote"]):
                kept.append(item)
            elif is_placeholder(item["enquiry_quote"]) and is_placeholder(item[value_field]):
                removed.append({"location": f"intake.{key}[{i}]", "item": item, "placeholder": True,
                                "reason": "placeholder quote (no information given); dropped"})
            else:
                removed.append({"location": f"intake.{key}[{i}]", "item": item,
                                "reason": "enquiry_quote not found verbatim in the enquiry"})
        data[key] = kept
    for name in ("physical_state", "optical_regime", "aqueous", "heterogeneous", "fluorophore"):
        s = data["sample"][name]
        if s["value"] != "unknown" and not ok(s["enquiry_quote"]):
            removed.append({"location": f"intake.sample.{name}", "item": dict(s),
                            "reason": "slot value without a verbatim enquiry quote; reset to unknown"})
            data["sample"][name] = {"value": "unknown", "basis": "unknown", "enquiry_quote": None}
    fiber = data["proposed_fiber"]
    if fiber["family"] != "none" and not ok(fiber["enquiry_quote"]):
        removed.append({"location": "intake.proposed_fiber", "item": dict(fiber),
                        "reason": "proposed fiber without a verbatim enquiry quote; ignored"})
        data["proposed_fiber"] = {"family": "none", "for_method": "none", "enquiry_quote": None}
    return Intake.model_validate(data), removed


def is_placeholder(span: str | None) -> bool:
    """A quote such as "unknown" or "n/a" that stands for missing information."""
    return span is None or re.sub(r"[^a-z/ -]", "", normalize(span).strip().lower()).strip() in PLACEHOLDERS


def check_against_screen(a: Assessment, candidates: list[Candidate], slots: dict, report: Report) -> None:
    status = {(c.method, c.technique): c for c in candidates}
    for i, r in enumerate(a.recommendations):
        cand = status.get((r.method, r.technique))
        if r.role != "not_recommended" and cand is not None and cand.status == "fail":
            reasons = "; ".join(x["rule"] for x in cand.reasons if x["status"] == "fail")
            report.add("respects_screen", False, "hard", f"recommendations[{i}]",
                       f"{r.method} {r.technique} failed screening ({reasons}); use role not_recommended or drop it")
        else:
            report.add("respects_screen", True, "hard", f"recommendations[{i}]")

    # Unknown deciding slots of recommended candidates must be asked about or assumed.
    recommended = {(r.method, r.technique) for r in a.recommendations if r.role != "not_recommended"}
    asked = " ".join(f"{q.question} {q.why_it_matters}" for q in a.clarification_questions)
    assumed = " ".join(a.assumptions)
    for slot, pattern in SLOT_PATTERNS.items():
        if slots.get(slot, "unknown") != "unknown":
            continue
        deciding = [c for c in candidates if (c.method, c.technique) in recommended and c.status == "unknown"
                    and any(slot.replace("_", " ") in x["message"] or _slot_rule(slot, x["rule"]) for x in c.reasons)]
        if deciding:
            covered = bool(pattern.search(asked) or pattern.search(assumed))
            report.add("unknown_slot_addressed", covered, "hard", f"slot.{slot}",
                       f"{slot} is unknown and decides {[(c.method, c.technique) for c in deciding]}: "
                       f"ask about it or state an assumption")


def _slot_rule(slot: str, rule_id: str) -> bool:
    return {"fluorophore": rule_id == "R-FLU-1",
            "physical_state": rule_id in ("R-MIR-2", "S01 Table 1 (p.6)"),
            "optical_regime": rule_id in ("R-GEO-2", "S01 Table 1 (p.6)")}.get(slot, False)


def check_status(a: Assessment, report: Report) -> None:
    contradicted = [p.premise for p in a.premise_checks if p.verdict == "contradicted"]
    report.add("status_vs_premises", not (contradicted and a.decision_status == "provisional_assessment"), "hard",
               "decision_status", f"premise(s) contradicted by sources {contradicted} but status is provisional_assessment")
    has_primary = any(r.role in ("primary", "comparison", "conditional") for r in a.recommendations)
    report.add("status_vs_recommendations",
               has_primary or a.decision_status != "provisional_assessment", "hard", "decision_status",
               "provisional_assessment needs at least one method worth testing")


def check_premise_basis(a: Assessment, report: Report) -> None:
    """Reverse check: premise_not_supported needs a premise the sources contradict."""
    contradicted = any(p.verdict == "contradicted" for p in a.premise_checks)
    report.add("status_needs_contradiction", contradicted or a.decision_status != "premise_not_supported", "hard",
               "decision_status", "premise_not_supported needs at least one premise check with verdict contradicted; "
               "otherwise use another status and keep the premise as not_covered or precedent_only")


def check_options(a: Assessment, candidates: list[Candidate], report: Report) -> None:
    """Brief answer, proposal, solution options, parameters and the single primary (Phase 3)."""
    report.add("brief_answer_present", bool(a.brief_answer.strip()), "hard", "brief_answer",
               "brief_answer is empty: give 2-4 plain sentences")
    p = a.proposal
    empty = [n for n in ("best_current_option", "what_would_change_it", "next_step") if not getattr(p, n).strip()]
    report.add("proposal_present", not empty, "hard", "proposal", f"proposal fields empty: {empty}")
    ids = [o.id for o in a.solution_options]
    report.add("proposal_option_exists", p.best_current_option in ids, "hard", "proposal.best_current_option",
               f"best_current_option {p.best_current_option!r} is not an option id {ids}")

    for key in ("recommendations", "solution_options", "parameters"):
        item_ids = [x.id for x in getattr(a, key)]
        dupes = sorted({x for x in item_ids if item_ids.count(x) > 1})
        report.add("ids_unique", not dupes, "hard", key, f"ids used more than once in {key}: {dupes}; "
                   f"give every entry its own id")

    n = len(a.solution_options)
    report.add("option_count", MIN_OPTIONS <= n <= MAX_OPTIONS, "hard", "solution_options",
               f"{n} options; give {MIN_OPTIONS}-{MAX_OPTIONS} (simple / recommended / extended)")
    tiers = [o.tier for o in a.solution_options]
    report.add("option_tiers_distinct", len(tiers) == len(set(tiers)), "hard", "solution_options",
               f"tiers repeat: {tiers}; each option has its own tier")
    report.add("option_recommended_tier", tiers.count("recommended") == 1, "hard", "solution_options",
               f"{tiers.count('recommended')} options with tier recommended; exactly one is needed")

    recs = {r.id: r for r in a.recommendations}
    param_ids = {p.id for p in a.parameters}
    status = {(c.method, c.technique): c.status for c in candidates}
    method_status: dict[str, set[str]] = {}
    for c in candidates:
        method_status.setdefault(c.method, set()).add(c.status)
    for i, o in enumerate(a.solution_options):
        loc = f"solution_options[{i}]"
        report.add("option_has_methods", bool(o.recommendation_ids), "hard", loc,
                   f"option {o.id} references no recommendation")
        bad = [x for x in o.recommendation_ids if x not in recs or recs[x].role == "not_recommended"]
        report.add("option_recommendation_refs", not bad, "hard", loc,
                   f"option {o.id} references {bad}: not an existing recommendation, or not_recommended")
        failed = [f"{recs[x].method} {recs[x].technique}" for x in o.recommendation_ids
                  if x in recs and status.get((recs[x].method, recs[x].technique)) == "fail"]
        failed += [f"{m} (combined)" for x in o.recommendation_ids if x in recs for m in recs[x].combined_with
                   if method_status.get(m) == {"fail"}]
        report.add("option_screen", not failed, "hard", loc, f"option {o.id} uses candidates that failed: {failed}")
        missing = [x for x in o.parameter_ids if x not in param_ids]
        report.add("option_parameter_refs", not missing, "hard", loc,
                   f"option {o.id} references parameters {missing} that do not exist")
        if o.tier == "extended":
            report.add("extended_fusion_note", bool(o.fusion_note and o.fusion_note.strip()), "hard", loc,
                       f"extended option {o.id} needs a fusion_note (fusion level, same sampling spot, "
                       f"synchronisation, per-block calibration, must beat the best single method)")
            methods = option_methods(o, recs)
            report.add("extended_multi_method", len(methods) >= 2, "soft", loc,
                       f"extended option {o.id} uses {methods}; the extended tier combines two or more methods")

    sets = [frozenset(o.recommendation_ids) for o in a.solution_options]
    same = sorted({" = ".join(o.id for o, s in zip(a.solution_options, sets, strict=True) if s == key)
                   for key in sets if sets.count(key) > 1})
    report.add("options_distinct", not same, "hard", "solution_options",
               f"options use the same recommendations: {same}; each option must differ in its methods")

    in_options = {m for o in a.solution_options for m in option_methods(o, recs)}
    for i, prm in enumerate(a.parameters):
        mb = prm.measured_by
        if mb.type != "spectroscopy":
            continue
        report.add("parameter_method_in_option", mb.method is not None and mb.method in in_options, "hard",
                   f"parameters[{i}]", f"parameter {prm.id} is measured by spectroscopy method {mb.method}, "
                   f"which no solution option uses {sorted(in_options)}")

    # An out-of-scope case may end without any recommendable method, so no primary (D-024).
    if a.decision_status != "outside_supported_scope":
        primaries = [r.id for r in a.recommendations if r.role == "primary"]
        report.add("single_primary", len(primaries) == 1, "hard", "recommendations",
                   f"{len(primaries)} primary recommendations {primaries}; exactly one is needed "
                   f"(others are comparison or conditional)")


# Hard checks that are re-run on the finalized assessment; their open state comes from that re-run.
RECHECK_NAMES = frozenset({"brief_answer_present", "proposal_present", "proposal_option_exists", "option_count",
                           "option_tiers_distinct", "option_recommended_tier", "option_has_methods",
                           "option_recommendation_refs", "option_screen", "extended_fusion_note",
                           "parameter_method_in_option", "single_primary", "status_needs_contradiction",
                           "ids_unique", "option_parameter_refs", "options_distinct"})


def recheck(a: Assessment, candidates: list[Candidate]) -> Report:
    """Checks re-run on the finalized assessment: what finalize may break or leave open."""
    report = Report()
    check_options(a, candidates, report)
    check_premise_basis(a, report)
    return report


def forbidden_hits(text: str) -> list[str]:
    """Forbidden phrases that are asserted, i.e. not preceded by a nearby negation."""
    hits = []
    for rx, label in FORBIDDEN:
        for m in rx.finditer(text):
            window = _NEGATION_ASIDE.sub(r"\1", _EMPHATIC.sub(" ", text[max(0, m.start() - 80):m.start()]))
            breaks = list(_CLAUSE_BREAK.finditer(window))
            if breaks:
                window = window[breaks[-1].end():]
            if not _NEGATION_BEFORE.search(window):
                hits.append(f"{label}: {m.group(0)!r}")
    return hits


def check_style(a: Assessment, report: Report) -> None:
    text = _all_text(a)
    hits = forbidden_hits(text)
    report.add("forbidden_wording", not hits, "hard", "assessment", "; ".join(hits))
    keys = [recommendation_key(r.method, r.technique, r.combined_with) for r in a.recommendations]
    dupes = sorted({" ".join([m, tq, *(["+ " + "+".join(cw)] if cw else [])])
                    for m, tq, cw in keys if keys.count((m, tq, cw)) > 1})
    report.add("recommendations_unique", not dupes, "hard", "recommendations",
               f"same method+technique (and combination) listed more than once: {dupes}")
    fused = [r.id for r in a.recommendations if r.role == "primary" and r.combined_with]
    report.add("primary_single_method", not fused, "soft", "recommendations",
               f"primary entries {fused} carry combined_with; the primary is a single method, "
               f"a combination is a later hypothesis")
    report.add("recommendation_count", len(a.recommendations) <= MAX_RECOMMENDATIONS, "soft", "recommendations",
               f"{len(a.recommendations)} entries (max {MAX_RECOMMENDATIONS}); list only options worth testing")
    report.add("question_count", len(a.clarification_questions) <= MAX_QUESTIONS, "soft", "clarification_questions",
               f"{len(a.clarification_questions)} questions (max {MAX_QUESTIONS})")
    for i, q in enumerate(a.clarification_questions):
        report.add("question_affects", bool(q.affects), "soft", f"clarification_questions[{i}]",
                   "a question should say what decision it affects")
    words = len(text.split())
    report.add("length_budget", words <= MAX_WORDS, "soft", "assessment", f"{words} words (budget {MAX_WORDS})")
    brief = len(a.brief_answer.split())
    report.add("brief_answer_length", brief <= MAX_BRIEF_WORDS, "soft", "brief_answer",
               f"{brief} words (max {MAX_BRIEF_WORDS})")
    report.add("premise_count", len(a.premise_checks) <= MAX_PREMISES, "soft", "premise_checks",
               f"{len(a.premise_checks)} premises (max {MAX_PREMISES}); keep the central ones")


def request_text(summary: str, enquiry: str) -> str:
    """The customer request line of the Answer: the intake summary, unless it carries a figure that is
    not in the enquiry or forbidden wording; then the enquiry itself."""
    summary = " ".join(summary.split())
    if not summary or unsupported_numbers(summary, [enquiry]) or forbidden_hits(summary):
        return " ".join(enquiry.split())
    return summary


def check_answer_length(a: Assessment, request: str, report: Report) -> None:
    """Soft: the Answer part stays short (about MAX_ANSWER_WORDS words of model text).

    `request` is the rendered request line (`request_text`), the summary or the enquiry itself."""
    words = sum(len(t.split()) for t in answer_texts(a, request))
    report.add("answer_length", words <= MAX_ANSWER_WORDS, "soft", "assessment",
               f"{words} words of model text in the Answer part (budget about {MAX_ANSWER_WORDS})")


def answer_texts(a: Assessment, request: str = "") -> list[str]:
    """Text shown in the Answer part: the request line, brief answer, status reason, proposal,
    option table cells and the top questions (code labels and the sketch are not counted)."""
    texts = [request, a.brief_answer, a.status_reason, a.proposal.what_would_change_it, a.proposal.next_step]
    texts += [x for o in a.solution_options for x in (o.ease_of_use, o.maintenance, o.performance_fit)]
    texts += [q.question for q in a.clarification_questions[:ANSWER_QUESTIONS]]
    return texts


def recommendation_key(method: str, technique: str, combined_with: list[str]) -> tuple[str, str, tuple[str, ...]]:
    """Identity of a recommendation: a combination is its own entry beside the single method.

    combined_with is normalised: duplicates and the entry's own method do not count.
    """
    return method, technique, tuple(sorted(set(combined_with) - {method}))


def normalized_combined_with(method: str, combined_with: list[str]) -> list[str]:
    """combined_with without duplicates and without the entry's own method, order kept."""
    return [m for m in dict.fromkeys(combined_with) if m != method]


def check_sections(a: Assessment, report: Report) -> None:
    """Sections the reader needs must have content: spectral ranges and real plan steps."""
    recommended = list(dict.fromkeys(r.method for r in a.recommendations if r.role in RECOMMENDED_ROLES))
    report.add("spectral_ranges_present", not (recommended and not a.spectral_ranges), "hard", "spectral_ranges",
               f"no spectral range given; state the nominal range for each recommended method {recommended}")
    covered = {s.method for s in a.spectral_ranges}
    for m in recommended:
        report.add("spectral_range_per_method", m in covered, "soft", "spectral_ranges",
                   f"recommended method {m} has no spectral_ranges entry")
    for i, s in enumerate(a.feasibility_plan.steps):
        bare = bool(_BARE_NUMBER.match(s.step)) or len(s.step.split()) < MIN_STEP_WORDS
        report.add("plan_step_text", not bare, "hard", f"feasibility_plan.steps[{i}]",
                   f"step text {s.step!r} is a bare number or under {MIN_STEP_WORDS} words; "
                   f"write the action itself (no numbering)")


def verify(enquiry: str, intake: Intake, a: Assessment, candidates: list[Candidate], slots: dict,
           intake_removed: list[dict] | None = None) -> Report:
    """`intake` must already be sanitized; `intake_removed` records what sanitizing dropped."""
    report = Report()
    for r in intake_removed or []:
        if not r.get("placeholder"):
            report.add("intake_sanitized", False, "soft", r["location"], r["reason"])
    verified = check_citations(a, report)
    check_numbers(a, enquiry, verified, report)
    check_against_screen(a, candidates, slots, report)
    check_status(a, report)
    check_premise_basis(a, report)
    check_style(a, report)
    check_answer_length(a, request_text(intake.summary, enquiry), report)
    check_sections(a, report)
    check_options(a, candidates, report)
    return report
