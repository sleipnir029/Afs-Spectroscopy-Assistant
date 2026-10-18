"""Turn a saved run JSON (`render.to_json`) into the display model of the web UI (one answer turn).

All labels come from the same code as the Markdown render (status, tier, role, basis, cost class,
confidence, measured-by wording, external source line), so the page and the .md never disagree.
Citations are collected into one registry: supplied ones (`S01 p.10`, ids s1, s2, ...) open the
verified quote in its page text; external ones (`E01 ¶12`, ids e1, e2, ...) open the stored quote and
source record only. The headline sentence is built by code from the proposed option, never by the model.
"""

from __future__ import annotations

import re
from types import SimpleNamespace

from afs_assistant import kb, quotes, scope
from afs_assistant.options import (
    CONFIDENCE_NOTE,
    TABLE1_CITATION,
    TECHNIQUE_LABEL,
    method_label,
    option_citations,
    option_parts,
)
from afs_assistant.pipeline import OFF_TOPIC_EXAMPLES, OFF_TOPIC_MESSAGE
from afs_assistant.render import (
    BASIS_LABEL,
    EXTERNAL_TITLE,
    GAP_LABEL,
    NOTE_LABEL,
    ROLE_LABEL,
    STATUS_LABEL,
    TIER_LABEL,
    basis_text,
    customer_quotes,
    external_verification,
    measured_by_text,
    request_label,
    request_line,
    shown_spectral_ranges,
    source_line,
)
from afs_assistant.schema import Assessment, Intake
from afs_assistant.ui import diagrams
from afs_assistant.verify import ANSWER_QUESTIONS

CONTEXT_CHARS = 700          # page text shown on each side of a verified quote
WIDE, NARROW = 720.0, 300.0  # native figure widths: wide from a 720 px container; narrow keeps >= 12 px text at 360 px
# Display steps of a run and the pipeline stages (`RunResult.timings`) each one covers.
STEPS = (("intake", "Reading enquiry", ("intake",)), ("screen", "Screening methods", ("screen",)),
         ("assess", "Assessing", ("assess", "repair")), ("verify", "Checking quotes", ("verify", "finalize")),
         ("external", "Searching literature", ("external",)))
TAB_SUB = {"simple": "least effort", "recommended": "best fit", "extended": "several methods"}
_TITLE = re.compile(r"^# First technical assessment(?::\s*(.*))?$")
_STEP_NUMBER = re.compile(r"^\s*\d+[.)](?!\d)\s*")
COST_NOTE = (f"Cost class is the relative rating in {TABLE1_CITATION} for the in-line method+technique rows "
             f"named (the highest one for a multi-method option); it is not a price.")
INCOMPLETE_MESSAGE = "This run stopped before an assessment was written; ask the question again to get one."


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
    """Off topic only when the pipeline says so (`off_topic` in the run JSON, Phase 5.0)."""
    return bool(data.get("off_topic"))


def is_incomplete(data: dict) -> bool:
    return not is_off_topic(data) and not data.get("assessment")


def off_topic(data: dict | None = None) -> dict:
    """The redirect line and example questions; the run's own wording wins when it carries one."""
    given = (data or {}).get("off_topic")
    given = given if isinstance(given, dict) else {"message": given} if isinstance(given, str) else {}
    return {"message": given.get("message") or OFF_TOPIC_MESSAGE,
            "examples": list(given.get("examples") or OFF_TOPIC_EXAMPLES)}


def status_label(data: dict) -> str:
    if is_off_topic(data):
        return "Off topic"
    if is_incomplete(data):
        return "Incomplete run"
    return STATUS_LABEL.get(data["assessment"].get("decision_status", ""), "")


def seconds_text(s: float | None) -> str:
    if s is None:
        return "—"
    if s < 0.1:
        return "<0.1 s"
    return f"{s:.0f} s" if s >= 100 else f"{s:.1f} s"


def safe_href(url: str | None) -> str | None:
    """Only http(s) links are rendered as links (a stored URL is data, never a script)."""
    return url if isinstance(url, str) and url.lower().startswith(("http://", "https://")) else None


_OPEN_Q = re.compile(r"^open question: (?P<ids>Q\d+(?:, Q\d+)*)(?: \(starts at Medium\))?$")


def plain_reasons(reasons: list[str], top_ids: list[str]) -> list[str]:
    """Confidence reasons in plain words; an open question points to its number under 'Help us sharpen this'."""
    out = []
    for r in reasons:
        m = _OPEN_Q.match(r)
        if not m:
            out.append(r)
            continue
        ids = m.group("ids").split(", ")
        nums = [str(top_ids.index(q) + 1) if q in top_ids else q for q in ids]
        joined = nums[0] if len(nums) == 1 else ", ".join(nums[:-1]) + " and " + nums[-1]
        out.append(f"question{'s' if len(nums) > 1 else ''} {joined} below {'are' if len(nums) > 1 else 'is'} still open")
    return out


def pin_reasons(reasons: list[str], top_ids: list[str]) -> list[dict]:
    """The pinned strip's short form of the confidence reasons: an open question reads 'Q1 open' (`open`: the
    strip links it to the current turn's questions); other reasons stay as they are."""
    out = []
    for r in reasons:
        m = _OPEN_Q.match(r)
        if not m:
            out.append({"text": r, "open": False})
            continue
        nums = [f"Q{top_ids.index(q) + 1}" if q in top_ids else q for q in m.group("ids").split(", ")]
        out.append({"text": ", ".join(nums) + " open", "open": True})
    return out


FOLLOW_DEFAULTS = ("What are the main risks?", "What would the first test look like?")


def follow_ups(v: dict, limit: int = 4) -> list[str]:
    """Suggested follow-up questions built from the run's own options and questions (generic wording)."""
    opts = v.get("options") or []
    best = next((o for o in opts if o["is_best"]), None)
    others = [o for o in opts if o is not best]
    out = []
    differing = [o for o in others if best and o["short"] != best["short"]]
    disjoint = [o for o in differing if not set(o["short"].split(" + ")) & set(best["short"].split(" + "))]
    alt = (disjoint or differing or [None])[0]
    if alt:
        out.append(f"Why {best['short']} and not {alt['short']}?")
    out += [f"Show the setup for the {o['tab']} option" for o in others]
    if v.get("top_questions"):
        out.append("How would the answer to question 1 change the recommendation?")
    out += [s for s in FOLLOW_DEFAULTS if s not in out]
    return out[:limit]


def headline(a: Assessment, option) -> str:
    """One sentence naming method and probe of the proposed option (code wording, not model text)."""
    if option is None:
        return STATUS_LABEL[a.decision_status] + "."
    recs = {r.id: r for r in a.recommendations}
    parts = option_parts(option, recs)
    if not parts:
        return STATUS_LABEL[a.decision_status] + "."

    def phrase(method: str, technique: str | None) -> str:
        if technique is None or technique == "to_be_determined":
            return f"{method} (probe type still to be chosen)"
        label = TECHNIQUE_LABEL.get(technique, technique.replace("_", " "))
        words = label if label.lower().startswith(method.lower()) else f"{method} {label}"
        if "probe" not in label:                       # e.g. diffuse reflection at a distance
            return words
        # spoken article: "an MIR", "an NIR", "an ATR"; "a Raman", "a UV-Vis"
        return ("an " if words[:1] in "AEIOUaeiou" or words.split()[0] in ("MIR", "NIR") else "a ") + words

    if len(parts) == 1:
        return f"Start with {phrase(*parts[0])}."
    return "Test " + " together with ".join(phrase(m, t) for m, t in parts) + ", one model per method first."


class _Registry:
    """Citation ids in order of appearance, per kind (s1.. supplied, e1.. external); a repeat keeps its id."""

    def __init__(self, data: dict) -> None:
        self.items: dict[str, dict] = {}
        self._ids: dict[tuple, str] = {}
        self._count = {"s": 0, "e": 0, "t": 0}
        self._checked = {(c["doc"], int(c["page"]), c["quote"]): c
                         for c in (data.get("verification") or {}).get("citations", [])}
        ext = data.get("external") or {}
        self._sources = {s["id"]: s for s in ext.get("sources", [])}
        self._external = {it["citation"]["label"]: it for it in ext.get("items", [])}

    def _new(self, kind: str, key: tuple) -> str:
        self._count[kind] += 1
        cid = f"{kind}{self._count[kind]}"
        self._ids[key] = cid
        return cid

    def supplied(self, citations) -> list[str]:
        out = []
        for c in citations or []:
            doc, page, quote, kind = c.doc, int(c.page), c.quote, c.claim_kind
            key = ("s", doc, page, quote)
            if key not in self._ids:
                cid = self._new("s", key)
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
            key = ("e", label)
            if key not in self._ids:
                cid = self._new("e", key)
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

    def table(self, cost: dict) -> list[str]:
        """The S01 Table 1 rows behind an option's cost class (transcribed table, not a text quote)."""
        rows = cost.get("rows") or []
        if not rows:
            return []
        key = ("t",) + tuple(r["row"] for r in rows)
        if key not in self._ids:
            cid = self._new("t", key)
            page = kb.page("S01", 6) or {}
            summary = "; ".join(f"row {r['row']}: {r['method']}, {r['table_technique']}, cost {r['cost']}" for r in rows)
            self.items[cid] = {
                "id": cid, "kind": "table", "label": TABLE1_CITATION, "doc": "S01", "page": 6, "quote": summary,
                "verified": False, "quote_status": "", "rows": rows, "title": page.get("title", ""),
                "page_text": str(page.get("text", ""))[:2 * CONTEXT_CHARS],
            }
        return [self._ids[key]]


_ID = re.compile(r"\b([OPQM])(\d+)\b")
_Q_RANGE = re.compile(r"\bQ(\d+)\s*(?:to|-|–)\s*Q(\d+)\b")


def id_words(a: Assessment):
    """Replace internal ids in model text with what the page shows: options by tier, questions by their
    number on the page, parameters and methods by name (the reader never sees O2, Q1, P3 or M1)."""
    names = {o.id: f"the {o.tier} option" for o in a.solution_options}
    names |= {q.id: f"question {i}" for i, q in enumerate(a.clarification_questions, 1)}
    names |= {p.id: p.name for p in a.parameters}
    names |= {r.id: method_label(r.method, r.technique) for r in a.recommendations}

    def sub(text: str) -> str:
        if not text:
            return text
        text = _Q_RANGE.sub(lambda m: f"questions {m.group(1)} to {m.group(2)}", text)
        return _ID.sub(lambda m: names.get(m.group(0), m.group(0)), text)
    return sub


def _source_record(src: dict) -> dict:
    """Display fields of an external source (our stored record; never the full text)."""
    doi = src.get("doi")
    return {"title": src.get("title") or "untitled", "year": src.get("year"), "venue": src.get("venue"),
            "authors": src.get("authors") or [], "doi": doi, "url": src.get("url"),
            "doi_href": f"https://doi.org/{doi}" if doi else None, "url_href": safe_href(src.get("url")),
            "access": "full text" if src.get("access") == "full_text" else "abstract only",
            "licence": src.get("licence") or "unknown",
            "retrieved": str(src.get("retrieved_at", ""))[:10] or "unknown",
            "origin": "curated library" if src.get("library_id") else src.get("api", "")}


def build(data: dict, markdown: str = "", key: str = "") -> dict:
    """The display model of one saved run."""
    manifest = data.get("manifest") or {}
    view = {"key": key, "run_id": data.get("run_id", ""), "title": title_of(markdown, data),
            "enquiry": data.get("enquiry", ""), "created": manifest.get("created_utc", ""),
            "models": manifest.get("models", []), "off_topic": None, "incomplete": None,
            "has_markdown": bool(markdown), "status_label": status_label(data)}
    if is_off_topic(data):
        view["off_topic"] = off_topic(data)
        view["reply"] = view["off_topic"]["message"] + "\n\n" + "\n".join(f"- {q}" for q in view["off_topic"]["examples"])
        return view
    if is_incomplete(data):
        view["incomplete"] = INCOMPLETE_MESSAGE
        view["reply"] = ""
        return view
    a = Assessment.model_validate(data["assessment"])
    intake = Intake.model_validate(data["intake"])
    ext = data.get("external")
    run = SimpleNamespace(assessment=a, intake=intake, enquiry=data.get("enquiry", ""), external=ext)
    flags = data.get("flagged") or {}
    reg = _Registry(data)
    recs = {r.id: r for r in a.recommendations}
    slots = data.get("slots") or {}

    view["request"] = {"label": request_label(run), "text": request_line(run)}
    view["status"] = {"code": a.decision_status, "label": STATUS_LABEL[a.decision_status],
                      "reason": a.status_reason, "flag": flags.get("status_reason")}
    view["still_open"] = data.get("still_open", [])

    pr = a.proposal
    best = next((o for o in a.solution_options if o.id == pr.best_current_option), None)
    support = (ext or {}).get("proposal_support", [])
    conf = data.get("option_confidence") or {}
    costs = data.get("option_costs") or {}

    top_ids = [q.id for q in a.clarification_questions[:ANSWER_QUESTIONS]]
    words = id_words(a)                    # main view: no internal ids (the expert rows keep and define them)
    drawn = a.model_copy(deep=True)        # the figures show model text too (location, names, sensors)
    drawn.measurement_concept.location = words(drawn.measurement_concept.location)
    for p in drawn.parameters:
        p.name = words(p.name)
        if p.measured_by.sensor:
            p.measured_by.sensor = words(p.measured_by.sensor)
    options = []
    for i, o in enumerate(a.solution_options):
        methods = []
        for rid in o.recommendation_ids:
            r = recs.get(rid)
            methods.append({"id": rid, "label": method_label(r.method, r.technique) if r else "missing",
                            "combined_with": list(r.combined_with) if r else []})
        c, cost = conf.get(o.id, {}), costs.get(o.id, {})
        short = " + ".join(dict.fromkeys(m for m, _ in option_parts(o, recs))) or "—"
        wide_svg, wide_notes = diagrams.schematic(drawn, o, slots, WIDE)
        narrow_svg, narrow_notes = diagrams.setup(drawn, o, slots, NARROW)
        options.append({
            "id": o.id, "tier": o.tier, "tier_label": TIER_LABEL[o.tier], "tab": o.tier.capitalize(),
            "tab_sub": f"{short} · {TAB_SUB.get(o.tier, '')}".rstrip(" ·"), "is_best": o is best, "short": short,
            "methods": methods, "confidence": {"level": c.get("level", ""), "reasons": c.get("reasons", []),
                                               "plain": plain_reasons(c.get("reasons", []), top_ids),
                                               "pin": pin_reasons(c.get("reasons", []), top_ids)},
            "cost": {"label": cost.get("label", ""), "class": cost.get("cost_class", ""), "cites": reg.table(cost)},
            "ease": words(o.ease_of_use), "maintenance": words(o.maintenance),
            "performance_fit": words(o.performance_fit), "parameters": list(o.parameter_ids),
            "cost_drivers": o.cost_drivers, "fusion_note": o.fusion_note,
            "cites": reg.supplied(option_citations(o, recs)), "flag": flags.get(f"solution_options[{i}]"),
            "figure": {"wide": wide_svg, "narrow": narrow_svg, "wide_notes": wide_notes,
                       "narrow_notes": narrow_notes},
        })
    if options and not any(o["is_best"] for o in options):
        options[0]["is_best"] = True       # a proposal pointing at a removed option still opens on one tab
    view["options"] = options
    best_view = next((o for o in options if o["is_best"]), None)
    view["recommendation"] = {
        "headline": headline(a, best), "text": words(a.brief_answer), "flag": flags.get("brief_answer"),
        "confidence": best_view["confidence"] if best_view else None,
        "cites": best_view["cites"] if best_view else [],
        "external_support": reg.external(support) if pr.basis == "engineering_judgement" else [],
    }
    view["proposal"] = {
        "best": {"id": best.id, "tier": TIER_LABEL[best.tier]} if best else None,
        "basis": basis_text(run), "basis_code": pr.basis, "basis_label": BASIS_LABEL[pr.basis],
        "what_would_change_it": words(pr.what_would_change_it), "next_step": words(pr.next_step),
        "tier": TIER_LABEL[best.tier] if best else None,
        "methods": best_view["methods"] if best_view else [],
        "confidence": best_view["confidence"] if best_view else None,
        "flags": {k: flags[f"proposal{s}"] for k, s in (("best", ""), ("change", ".what_would_change_it"),
                                                         ("next", ".next_step")) if f"proposal{s}" in flags},
    }
    view["confidence_note"] = CONFIDENCE_NOTE
    view["cost_note"] = COST_NOTE
    view["cost_citation"] = TABLE1_CITATION

    view["questions"] = [{"id": q.id, "question": words(q.question), "why": words(q.why_it_matters),
                          "affects": q.affects,
                          "flag": flags.get(f"clarification_questions[{i}]")}
                         for i, q in enumerate(a.clarification_questions)]
    view["top_questions"] = view["questions"][:ANSWER_QUESTIONS]

    # ---------------------------------------------------------------- folded rows
    view["parameters"] = [{"id": p.id, "name": p.name, "kind": p.kind, "necessity": p.necessity,
                           "measured_by": measured_by_text(p), "why": p.why, "cites": reg.supplied(p.citations),
                           "flag": flags.get(f"parameters[{i}]")} for i, p in enumerate(a.parameters)]
    view["risks"] = [{"text": k.risk, "rules": list(k.rule_ids), "cites": reg.supplied(k.citations),
                      "flag": flags.get(f"risks[{i}]")} for i, k in enumerate(a.risks)]
    fp = a.feasibility_plan
    view["plan"] = {"steps": [{"step": _STEP_NUMBER.sub("", s.step), "purpose": s.purpose,
                               "cites": reg.supplied(s.citations), "flag": flags.get(f"feasibility_plan.steps[{i}]")}
                              for i, s in enumerate(fp.steps)],
                    "reference": fp.reference_measurements, "decision_basis": fp.decision_basis}
    view["premises"] = [{"verdict": p.verdict, "verdict_label": p.verdict.replace("_", " ").capitalize(),
                         "premise": p.premise.rstrip().rstrip("."), "explanation": p.explanation,
                         "cites": reg.supplied(p.citations), "flag": flags.get(f"premise_checks[{i}]")}
                        for i, p in enumerate(a.premise_checks)]
    # Every de-duplicated customer quote, no cap: the web view may not show the full enquiry next to it.
    view["requirements"] = {"stated": list(a.requirements_stated) or [f'"{q}"' for q in customer_quotes(run)],
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
                         "flag": flags.get(f"spectral_ranges[{i}]")} for i, s in shown_spectral_ranges(a)]
    view["assumptions"] = list(a.assumptions)
    view["not_covered"] = list(a.not_in_sources)
    view["notes"] = [{"label": label, "text": getattr(a, n)} for n, label in NOTE_LABEL.items() if getattr(a, n)]
    proposed, others, fiber_ids = diagrams.option_highlights(a, best)
    view["figures"] = {
        "spectral": {"wide": diagrams.spectral(proposed, others, fiber_ids, WIDE - 40.0),
                     "narrow": diagrams.spectral(proposed, others, fiber_ids, NARROW)},
        "params": {"wide": diagrams.parameter_map(a, WIDE - 40), "narrow": diagrams.parameter_map(a, NARROW)},
        "proposed_methods": sorted(proposed), "other_methods": sorted(others),
    }
    view["external"] = _external_view(ext, reg)
    view["verification"] = _verification_view(data, run)
    view["made"] = made_strip(data)
    view["citations"] = reg.items
    view["reply"] = customer_reply(view)
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
            "mode": ext.get("mode", ""), "count": sum(len(g["cites"]) for g in gaps)}


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


def made_strip(data: dict) -> dict:
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
        seconds = round(sum(ran), 2) if ran else None
        steps.append({"key": key, "label": label, "seconds": seconds, "time": seconds_text(seconds),
                      "note": notes[key]})
    return {"steps": steps, "wall": seconds_text(timings.get("wall")) if timings.get("wall") else None,
            "calls": len(data.get("calls", [])), "models": (data.get("manifest") or {}).get("models", []),
            "verified": f"{s.get('citations_verified', 0)}/{s.get('citations_total', 0)}"}


def customer_reply(view: dict) -> str:
    """Plain-text reply for the hand-off: the brief answer, next step, open questions and source labels."""
    rec, pr = view["recommendation"], view["proposal"]
    labels = list(dict.fromkeys(view["citations"][c]["label"] for c in rec["cites"]))
    lines = ["Thank you for your enquiry.", "", rec["headline"], rec["text"], "", f"Proposed next step: {pr['next_step']}"]
    if view["top_questions"]:
        lines += ["", "To sharpen this assessment, could you tell us:"]
        lines += [f"{k}. {q['question']}" for k, q in enumerate(view["top_questions"], 1)]
    if labels:
        lines += ["", "Sources (AFS material): " + ", ".join(labels)]
    return "\n".join(lines)


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
    """Status, proposed option, its method and confidence: one side of 'What changed'."""
    if view.get("off_topic") or view.get("incomplete"):
        return {"status": view["status_label"], "best": None, "method": None, "confidence": None}
    best = view["proposal"]["best"]
    conf = view["proposal"]["confidence"] or {}
    methods = "; ".join(m["label"] for m in view["proposal"]["methods"]) or None
    return {"status": view["status"]["label"], "best": best["tier"] if best else None,
            "method": methods, "confidence": conf.get("level")}


def compare(before: dict, after: dict) -> list[dict]:
    """'What changed': each row old -> new, marked when it differs."""
    b, a = summary(before), summary(after)
    rows = [("Decision status", "status"), ("Proposed option", "best"), ("Method", "method"),
            ("Confidence", "confidence")]
    return [{"label": label, "before": b[k] or "—", "after": a[k] or "—", "changed": b[k] != a[k]}
            for label, k in rows]


def answers_to_facts(enquiry: str, answers: list[dict], follow_up: str = "") -> str:
    """The enquiry with the customer's answers and any added detail appended as stated facts."""
    lines = [f"- {' '.join(str(a['question']).split())} Answer: {' '.join(str(a['answer']).split())}"
             for a in answers if str(a.get("answer", "")).strip()]
    extra = " ".join(follow_up.split())
    if extra:
        lines.append(f"- Additional detail: {extra}")
    if not lines:
        return enquiry
    return (enquiry.rstrip() + "\n\nAdditional facts from the customer (answers and added details):\n"
            + "\n".join(lines))
