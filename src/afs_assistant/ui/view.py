"""Turn a saved run JSON (`render.to_json`) into the display model of the web UI.

All labels come from the same code as the Markdown render (status, tier, role, basis, cost class,
confidence, measured-by wording, external source line), so the page and the .md never disagree.
Citations are collected into one registry: supplied ones (`S01 p.10`) open the verified quote and
the surrounding page text; external ones (`E01 ¶12`) open the stored quote and source record only.
"""

from __future__ import annotations

import re
from types import SimpleNamespace

from afs_assistant import kb, quotes, scope
from afs_assistant.options import (
    CONFIDENCE_NOTE,
    TABLE1_CITATION,
    method_label,
    option_citations,
)
from afs_assistant.render import (
    BASIS_LABEL,
    EXTERNAL_TITLE,
    GAP_LABEL,
    NOTE_LABEL,
    ROLE_LABEL,
    STATUS_LABEL,
    TIER_LABEL,
    basis_text,
    external_verification,
    measured_by_text,
    request_label,
    request_line,
    source_line,
    stated_from_intake,
)
from afs_assistant.schema import Assessment, Intake
from afs_assistant.ui import diagrams
from afs_assistant.verify import ANSWER_QUESTIONS

CONTEXT_CHARS = 700          # page text shown on each side of a verified quote
FIG_WIDTHS = {"wide": 560.0, "narrow": 340.0}      # side-by-side figures on desktop / one column on phone
MAP_WIDTHS = {"wide": 900.0, "narrow": 340.0}
# Display steps of a run and the pipeline stages (`RunResult.timings`) each one covers.
STEPS = (("intake", "Reading enquiry", ("intake",)), ("screen", "Screening methods", ("screen",)),
         ("assess", "Assessing", ("assess", "repair")), ("verify", "Checking quotes", ("verify", "finalize")),
         ("external", "Searching literature", ("external",)))
_TITLE = re.compile(r"^# First technical assessment(?::\s*(.*))?$")
_STEP_NUMBER = re.compile(r"^\s*\d+[.)](?!\d)\s*")
COST_NOTE = (f"Cost class is the relative rating in {TABLE1_CITATION} for the in-line method+technique rows "
             f"named (the highest one for a multi-method option); it is not a price.")
OFF_TOPIC_MESSAGE = ("This assistant gives first technical assessments for in-line process spectroscopy with "
                     "fiber-optic probes (NIR, MIR, Raman, fluorescence, UV-Vis); this enquiry seems to be about "
                     "something else.")
# Generic examples written for the UI; none is taken from a test or development case.
OFF_TOPIC_EXAMPLES = (
    "Can NIR follow the moisture of a granulate in-line while it dries in a fluid-bed dryer?",
    "Which probe and fiber would suit monitoring solvent composition at the top of a distillation column?",
    "Is UV-Vis or fluorescence the better first test for a dissolved dye in a clear rinse-water stream?",
)


def title_of(markdown: str, data: dict) -> str:
    """The run title from the Markdown heading, else the intake summary, else the enquiry's first line."""
    first = markdown.splitlines()[0] if markdown else ""
    m = _TITLE.match(first)
    if m and m.group(1):
        return m.group(1).strip()
    summary = " ".join(str((data.get("intake") or {}).get("summary", "")).split())
    if summary:
        return summary
    lines = str(data.get("enquiry", "")).strip().splitlines()
    return lines[0][:120] if lines else "Untitled run"


def is_off_topic(data: dict) -> bool:
    """An off-topic run: marked by the pipeline, intake routed only out_of_scope, or no assessment at all."""
    routes = set((data.get("intake") or {}).get("routes") or [])
    return bool(data.get("off_topic")) or routes == {"out_of_scope"} or not data.get("assessment")


def off_topic(data: dict | None = None) -> dict:
    """The redirect line and example questions; the pipeline's own wording wins when the run carries it."""
    given = (data or {}).get("off_topic")
    given = given if isinstance(given, dict) else {"message": given} if isinstance(given, str) else {}
    return {"message": given.get("message") or OFF_TOPIC_MESSAGE,
            "examples": list(given.get("examples") or OFF_TOPIC_EXAMPLES)}


def status_label(data: dict) -> str:
    if is_off_topic(data):
        return "Off topic"
    return STATUS_LABEL.get(data["assessment"].get("decision_status", ""), "")


class _Registry:
    """Citation ids in order of appearance; an identical quote keeps its first id."""

    def __init__(self, data: dict) -> None:
        self.items: dict[str, dict] = {}
        self._ids: dict[tuple, str] = {}
        self._checked = {(c["doc"], int(c["page"]), c["quote"]): c
                         for c in (data.get("verification") or {}).get("citations", [])}
        ext = data.get("external") or {}
        self._sources = {s["id"]: s for s in ext.get("sources", [])}
        self._external = {it["citation"]["label"]: it for it in ext.get("items", [])}

    def supplied(self, citations) -> list[str]:
        out = []
        for c in citations or []:
            doc, page, quote, kind = c.doc, int(c.page), c.quote, c.claim_kind
            key = ("s", doc, page, quote)
            if key not in self._ids:
                cid = f"s{len(self._ids) + 1}"
                self._ids[key] = cid
                checked = self._checked.get((doc, page, quote), {})
                self.items[cid] = {
                    "id": cid, "kind": "supplied", "label": kb.citation_label(doc, page), "doc": doc,
                    "page": page, "quote": quote, "claim_kind": kind.replace("_", " "),
                    "verified": bool(checked.get("verified")), "quote_status": checked.get("quote_status", ""),
                    "precedent": scope.check(kind, doc, page)[0] == "precedent_only",
                }
            out.append(self._ids[key])
        return out

    def external(self, labels) -> list[str]:
        out = []
        for label in labels or []:
            item = self._external.get(label)
            if item is None:
                continue
            key = ("x", label)
            if key not in self._ids:
                cid = f"x{len(self._ids) + 1}"
                self._ids[key] = cid
                c = item["citation"]
                src = self._sources.get(c["source_id"], {})
                self.items[cid] = {
                    "id": cid, "kind": "external", "label": label, "quote": c["quote"],
                    "quote_status": item.get("quote_status", ""), "verified": True,
                    "finding": item.get("finding", ""), "how_it_applies": item.get("how_it_applies", ""),
                    "limits": item.get("limits_and_transfer_risks", ""), "option_id": item.get("option_id"),
                    "source": _source_record(src), "source_line": source_line(src),
                }
            out.append(self._ids[key])
        return out


def _source_record(src: dict) -> dict:
    """Display fields of an external source (our stored record; never the full text)."""
    return {"title": src.get("title") or "untitled", "year": src.get("year"), "venue": src.get("venue"),
            "authors": src.get("authors") or [], "doi": src.get("doi"), "url": src.get("url"),
            "access": "full text" if src.get("access") == "full_text" else "abstract only",
            "licence": src.get("licence") or "unknown",
            "retrieved": str(src.get("retrieved_at", ""))[:10] or "unknown",
            "origin": "curated library" if src.get("library_id") else src.get("api", "")}


def build(data: dict, markdown: str = "", key: str = "") -> dict:
    """The display model of one saved run."""
    manifest = data.get("manifest") or {}
    view = {"key": key, "run_id": data.get("run_id", ""), "title": title_of(markdown, data),
            "enquiry": data.get("enquiry", ""), "created": manifest.get("created_utc", ""),
            "models": manifest.get("models", []), "off_topic": None, "has_markdown": bool(markdown)}
    if is_off_topic(data):
        view["off_topic"] = off_topic(data)
        return view
    a = Assessment.model_validate(data["assessment"])
    intake = Intake.model_validate(data["intake"])
    ext = data.get("external")
    run = SimpleNamespace(assessment=a, intake=intake, enquiry=data.get("enquiry", ""), external=ext)
    flags = data.get("flagged") or {}
    reg = _Registry(data)
    recs = {r.id: r for r in a.recommendations}

    view["request"] = {"label": request_label(run), "text": request_line(run)}
    view["status"] = {"code": a.decision_status, "label": STATUS_LABEL[a.decision_status],
                      "reason": a.status_reason, "flag": flags.get("status_reason")}
    view["still_open"] = data.get("still_open", [])
    view["brief_answer"] = {"text": a.brief_answer, "flag": flags.get("brief_answer")}

    pr = a.proposal
    best = next((o for o in a.solution_options if o.id == pr.best_current_option), None)
    support = (ext or {}).get("proposal_support", [])
    view["proposal"] = {
        "best": {"id": best.id, "tier": TIER_LABEL[best.tier]} if best else None,
        "basis": basis_text(run), "basis_code": pr.basis, "basis_label": BASIS_LABEL[pr.basis],
        "external_support": reg.external(support) if pr.basis == "engineering_judgement" else [],
        "what_would_change_it": pr.what_would_change_it, "next_step": pr.next_step,
        "flags": {k: flags[f"proposal{s}"] for k, s in (("best", ""), ("change", ".what_would_change_it"),
                                                         ("next", ".next_step")) if f"proposal{s}" in flags},
    }

    conf = data.get("option_confidence") or {}
    costs = data.get("option_costs") or {}
    view["options"] = []
    for i, o in enumerate(a.solution_options):
        methods = []
        for rid in o.recommendation_ids:
            r = recs.get(rid)
            methods.append({"id": rid, "label": method_label(r.method, r.technique) if r else "missing",
                            "combined_with": list(r.combined_with) if r else []})
        c = conf.get(o.id, {})
        cost = costs.get(o.id, {})
        view["options"].append({
            "id": o.id, "tier": o.tier, "tier_label": TIER_LABEL[o.tier], "is_best": best is not None and o is best,
            "methods": methods, "confidence": {"level": c.get("level", ""), "reasons": c.get("reasons", [])},
            "cost": {"label": cost.get("label", ""), "class": cost.get("cost_class", "")},
            "ease": o.ease_of_use, "maintenance": o.maintenance, "performance_fit": o.performance_fit,
            "parameters": list(o.parameter_ids), "cost_drivers": o.cost_drivers, "fusion_note": o.fusion_note,
            "cites": reg.supplied(option_citations(o, recs)), "flag": flags.get(f"solution_options[{i}]"),
        })
    view["proposal"]["methods"] = next((o["methods"] for o in view["options"] if o["is_best"]), [])
    view["proposal"]["confidence"] = next((o["confidence"] for o in view["options"] if o["is_best"]), None)
    view["confidence_note"] = CONFIDENCE_NOTE
    view["cost_note"] = COST_NOTE
    view["cost_citation"] = TABLE1_CITATION

    proposed, others, fiber_ids = diagrams.option_highlights(a, best)
    slots = data.get("slots") or {}
    view["figures"] = {
        "setup": {w: diagrams.setup(a, best, slots, px) for w, px in FIG_WIDTHS.items()} if best else None,
        "spectral": {w: diagrams.spectral(proposed, others, fiber_ids, px) for w, px in FIG_WIDTHS.items()},
        "params": {w: diagrams.parameter_map(a, px) for w, px in MAP_WIDTHS.items()},
        "proposed_methods": sorted(proposed), "other_methods": sorted(others),
    }

    view["questions"] = [{"id": q.id, "question": q.question, "why": q.why_it_matters, "affects": q.affects,
                          "flag": flags.get(f"clarification_questions[{i}]")}
                         for i, q in enumerate(a.clarification_questions)]
    view["top_questions"] = ANSWER_QUESTIONS

    # ---------------------------------------------------------------- expert detail
    view["parameters"] = [{"id": p.id, "name": p.name, "kind": p.kind, "necessity": p.necessity,
                           "measured_by": measured_by_text(p), "why": p.why, "cites": reg.supplied(p.citations),
                           "flag": flags.get(f"parameters[{i}]")} for i, p in enumerate(a.parameters)]
    view["premises"] = [{"verdict": p.verdict, "verdict_label": p.verdict.replace("_", " ").capitalize(),
                         "premise": p.premise.rstrip().rstrip("."), "explanation": p.explanation,
                         "cites": reg.supplied(p.citations), "flag": flags.get(f"premise_checks[{i}]")}
                        for i, p in enumerate(a.premise_checks)]
    view["requirements"] = {"stated": list(a.requirements_stated) or stated_from_intake(run),
                            "unknowns": list(a.key_unknowns)}
    view["recommendations"] = [{
        "id": m.id, "role": m.role, "role_label": ROLE_LABEL[m.role], "method": method_label(m.method, m.technique),
        "combined_with": list(m.combined_with), "rationale": m.rationale,
        "conditions": "" if m.conditions.strip().lower() in ("", "none") else m.conditions,
        "cites": reg.supplied(m.citations), "flag": flags.get(f"recommendations[{i}]"),
    } for i, m in enumerate(a.recommendations)]
    mc = a.measurement_concept
    view["measurement"] = {"probe": mc.probe_and_geometry, "location": mc.location, "fiber_link": mc.fiber_link,
                           "cites": reg.supplied(mc.citations), "flag": flags.get("measurement_concept")}
    view["spectral"] = [{"method": s.method, "statement": s.statement, "cites": reg.supplied(s.citations),
                         "flag": flags.get(f"spectral_ranges[{i}]")} for i, s in enumerate(a.spectral_ranges)]
    view["risks"] = [{"text": k.risk, "rules": list(k.rule_ids), "cites": reg.supplied(k.citations),
                      "flag": flags.get(f"risks[{i}]")} for i, k in enumerate(a.risks)]
    fp = a.feasibility_plan
    view["plan"] = {"steps": [{"step": _STEP_NUMBER.sub("", s.step), "purpose": s.purpose,
                               "cites": reg.supplied(s.citations), "flag": flags.get(f"feasibility_plan.steps[{i}]")}
                              for i, s in enumerate(fp.steps)],
                    "reference": fp.reference_measurements, "decision_basis": fp.decision_basis}
    view["assumptions"] = list(a.assumptions)
    view["not_covered"] = list(a.not_in_sources)
    view["notes"] = [{"label": label, "text": getattr(a, n)} for n, label in NOTE_LABEL.items() if getattr(a, n)]
    view["external"] = _external_view(ext, reg)
    view["verification"] = _verification_view(data, run)
    view["made"] = made_strip(data, len(reg.items))
    view["citations"] = reg.items
    return view


def _external_view(ext: dict | None, reg: _Registry) -> dict | None:
    if not ext or not ext.get("gaps"):
        return None
    gaps = []
    for g in ext["gaps"]:
        labels = [it["citation"]["label"] for it in ext.get("items", []) if it["gap_id"] == g["id"]]
        gaps.append({"id": g["id"], "kind": GAP_LABEL.get(g["kind"], g["kind"]), "text": g["text"],
                     "cites": reg.external(labels)})
    return {"title": EXTERNAL_TITLE, "fallback": ext.get("fallback"), "error": ext.get("error"), "gaps": gaps,
            "mode": ext.get("mode", "")}


def _verification_view(data: dict, run) -> dict:
    s = (data.get("verification") or {}).get("summary", {})
    return {
        "summary": s,
        "still_open": data.get("still_open", []),
        "removed_citations": [{"location": x["location"],
                               "label": kb.citation_label(x["citation"]["doc"], x["citation"]["page"]),
                               "quote": x["citation"]["quote"]} for x in data.get("removed_citations", [])],
        "changes": [{"location": x["location"], "reason": x["reason"]} for x in data.get("finalize_changes", [])],
        "repair_rounds": len(data.get("repairs", [])),
        "external_lines": [line.lstrip("- ").strip() for line in external_verification(run)],
    }


def made_strip(data: dict, n_citations: int) -> dict:
    """'How this answer was made': the display steps with their recorded times and counts."""
    timings = data.get("timings_s") or {}
    s = (data.get("verification") or {}).get("summary", {})
    ext = data.get("external")
    notes = {"intake": f"{len((data.get('intake') or {}).get('facts_stated', []))} stated fact(s)",
             "screen": f"{len(data.get('screening', []))} method/technique pairs",
             "assess": f"{len(data.get('repairs', []))} repair round(s)",
             "verify": f"{s.get('citations_verified', 0)} of {s.get('citations_total', 0)} quotes verified",
             "external": ("off" if ext is None else
                          f"{len(ext.get('items', []))} external quote(s) verified" if ext.get("gaps")
                          else "no gap to search")}
    steps = []
    for key, label, stages in STEPS:
        ran = [timings[x] for x in stages if x in timings]
        steps.append({"key": key, "label": label, "seconds": round(sum(ran), 1) if ran else None,
                      "note": notes[key]})
    return {"steps": steps, "wall": timings.get("wall"), "calls": len(data.get("calls", [])),
            "models": (data.get("manifest") or {}).get("models", []), "citations": n_citations}


def source(doc: str, page: int, quote: str) -> dict | None:
    """The supplied page text around a quote, located the same way verification does."""
    record = kb.page(doc, page)
    if record is None:
        return None
    text = record["text"]
    check = quotes.verify(doc, page, quote)
    out = {"label": kb.citation_label(doc, page), "doc": doc, "page": int(page), "title": record.get("title", ""),
           "status": check.status, "verified": check.ok}
    if check.start is None:
        out.update(before="", match="", after=text[:2 * CONTEXT_CHARS], cut_before=False,
                   cut_after=len(text) > 2 * CONTEXT_CHARS)
        return out
    lo, hi = max(0, check.start - CONTEXT_CHARS), min(len(text), check.end + CONTEXT_CHARS)
    if lo > 0:                                   # start and end on a word boundary
        space = text.find(" ", lo)
        lo = space + 1 if 0 <= space < check.start else lo
    if hi < len(text):
        space = text.rfind(" ", check.end, hi)
        hi = space if space > check.end else hi
    out.update(before=text[lo:check.start], match=text[check.start:check.end], after=text[check.end:hi],
               cut_before=lo > 0, cut_after=hi < len(text))
    return out


def summary(view: dict) -> dict:
    """Status, proposed option and its confidence, per-option confidence: the before/after comparison."""
    if view.get("off_topic"):
        return {"status": "Off topic", "best": None, "confidence": None, "options": []}
    best = view["proposal"]["best"]
    conf = view["proposal"]["confidence"] or {}
    return {"status": view["status"]["label"], "best": f"{best['id']} ({best['tier']})" if best else None,
            "confidence": conf.get("level"),
            "options": [{"id": o["id"], "tier": o["tier_label"], "confidence": o["confidence"]["level"]}
                        for o in view["options"]]}


def compare(before: dict, after: dict) -> dict:
    return {"before": summary(before), "after": summary(after)}


def answers_to_facts(enquiry: str, answers: list[dict]) -> str:
    """The enquiry with the customer's answers to clarification questions appended as stated facts."""
    lines = [f"- {' '.join(str(a['question']).split())} Answer: {' '.join(str(a['answer']).split())}"
             for a in answers if str(a.get("answer", "")).strip()]
    if not lines:
        return enquiry
    return (enquiry.rstrip() + "\n\nAdditional facts from the customer (answers to clarification questions):\n"
            + "\n".join(lines))
