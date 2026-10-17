"""Deterministic verification of an assessment (AFS-Ashby post-checks; no LLM).

Pattern from MatSage's verifier: a report of named checks with hard/soft severity.
All checks run against the exact texts the model was shown (normalised page text,
the enquiry). Number checks are claim-local: an item's numbers must come from that
item's own verified quotes or from the enquiry.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field

from afs_assistant import quotes, scope
from afs_assistant.normalize import normalize
from afs_assistant.numbers import unsupported_numbers
from afs_assistant.schema import Assessment, Citation, Intake
from afs_assistant.screen import Candidate

MAX_QUESTIONS = 7
MAX_WORDS = 1800
# Wording that asserts certainty or commercial facts the sources cannot support (REF §3 "Do not invent").
FORBIDDEN = [
    (re.compile(r"[€$£]\s*\d|\b\d+(?:[.,]\d+)?\s*(?:EUR|USD|euro|dollars?)\b", re.IGNORECASE), "price"),
    (re.compile(r"\bguarantee[sd]?\b", re.IGNORECASE), "guarantee"),
    (re.compile(r"\bwill (?:definitely |certainly )?work\b", re.IGNORECASE), "certainty"),
    (re.compile(r"\b(?:is|are) (?:approved|validated|certified|proven) (?:for|to)\b", re.IGNORECASE), "approval claim"),
    (re.compile(r"\bproven to\b|\bready for (?:clinical|surgical|in vivo|production)\b", re.IGNORECASE), "readiness claim"),
    (re.compile(r"\b[A-Z]{2,5}-\d{3,}[A-Z0-9-]*\b"), "product-code-like token"),
]
# Which question wording counts as covering an unknown deciding slot.
SLOT_WORDS = {
    "physical_state": ("state", "liquid", "solid", "powder", "paste", "form"),
    "optical_regime": ("clear", "turbid", "opaque", "optical", "scatter", "transparen", "colour", "color", "dark"),
    "fluorophore": ("fluoresc", "fluorophore", "marker", "indicator"),
}


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
    return items


def _all_text(a: Assessment) -> str:
    parts = [a.status_reason, *a.requirements_stated, *a.key_unknowns, *a.assumptions, *a.not_in_sources,
             a.feasibility_plan.reference_measurements, a.feasibility_plan.decision_basis]
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
            report.add("quote_verified", q.ok, "hard", where,
                       f"{c.doc} p.{c.page}: quote {q.status} (score {q.score})")
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
    for loc, text in loose_texts:
        missing = unsupported_numbers(text, [enquiry])
        report.add("numbers_uncited_text", not missing, "hard", loc,
                   f"figures in uncited text must come from the enquiry: {[n.text for n in missing]}")


def sanitize_intake(intake: Intake, enquiry: str) -> tuple[Intake, list[dict]]:
    """Remove intake items whose quote is not verbatim in the enquiry (no invented client facts).

    Facts, targets, process details and premises with a bad quote are dropped; a sample
    slot with a bad or missing quote is reset to unknown. Returns the cleaned intake and
    a record of every removal.
    """
    text = normalize(enquiry).lower()

    def ok(span: str | None) -> bool:
        return span is not None and normalize(span).lower() in text

    data = intake.model_dump()
    removed: list[dict] = []
    for key in ("facts_stated", "targets", "process", "customer_premises"):
        kept = []
        for i, item in enumerate(data[key]):
            if ok(item["enquiry_quote"]):
                kept.append(item)
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
    asked = " ".join(f"{q.question} {q.why_it_matters}" for q in a.clarification_questions).lower()
    assumed = " ".join(a.assumptions).lower()
    for slot, words in SLOT_WORDS.items():
        if slots.get(slot, "unknown") != "unknown":
            continue
        deciding = [c for c in candidates if (c.method, c.technique) in recommended and c.status == "unknown"
                    and any(slot.replace("_", " ") in x["message"] or _slot_rule(slot, x["rule"]) for x in c.reasons)]
        if deciding:
            covered = any(w in asked or w in assumed for w in words)
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


def check_style(a: Assessment, report: Report) -> None:
    text = _all_text(a)
    for rx, label in FORBIDDEN:
        m = rx.search(text)
        report.add("forbidden_wording", m is None, "hard", "assessment", f"{label}: {m.group(0)!r}" if m else "")
    report.add("question_count", len(a.clarification_questions) <= MAX_QUESTIONS, "soft", "clarification_questions",
               f"{len(a.clarification_questions)} questions (max {MAX_QUESTIONS})")
    for i, q in enumerate(a.clarification_questions):
        report.add("question_affects", bool(q.affects), "soft", f"clarification_questions[{i}]",
                   "a question should say what decision it affects")
    words = len(text.split())
    report.add("length_budget", words <= MAX_WORDS, "soft", "assessment", f"{words} words (budget {MAX_WORDS})")


def verify(enquiry: str, intake: Intake, a: Assessment, candidates: list[Candidate], slots: dict,
           intake_removed: list[dict] | None = None) -> Report:
    """`intake` must already be sanitized; `intake_removed` records what sanitizing dropped."""
    report = Report()
    for r in intake_removed or []:
        report.add("intake_sanitized", False, "soft", r["location"], r["reason"])
    verified = check_citations(a, report)
    check_numbers(a, enquiry, verified, report)
    check_against_screen(a, candidates, slots, report)
    check_status(a, report)
    check_style(a, report)
    return report
