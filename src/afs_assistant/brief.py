"""Short brief view of a finished run: built by code from the saved run JSON, no model call.

It only selects, orders and copies what the run JSON already holds; it adds no fact. The
section order follows the organiser's answer structure (REF §3) and worked answers: decision
status, requirements, clarification questions, recommendation, measurement concept, spectral
range, risks and uncertainty, feasibility plan, sources. Length is cut by choosing fields and
list items, never by cutting a string mid-way.

- Citations: only those the run verified (`verification.citations`, matched on doc, page and
  quote) are shown, in the `S01 p.10` format; a citation not in that set is left out.
- Options: tier, methods, cost class (the run's `option_costs`) and confidence level (the run's
  `option_confidence`) only; the reasons stay in the full answer.
- An uncited risk tagged with a rule shows that rule's stored source quote as a related source,
  but only when the quote is verbatim on the cited page (`quotes.verify`); it never claims to
  verify the sentence.
- Secondary external literature: only verified items that support the proposed option (quote
  and URL kept, as for every external citation); nothing when there is none.
- Internal ids (option, recommendation, question, parameter ids) are not shown: a bracket that
  holds only ids is dropped and a remaining id is replaced by its label from the same run.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

from afs_assistant import kb, quotes
from afs_assistant.options import NOT_RATED, TABLE1_CITATION, method_label

QUESTIONS_SHOWN = 3
RISKS_SHOWN = 3
UNKNOWNS_SHOWN = 2
ASKED_SHARE = 0.5
EXTERNAL_SHOWN = 1
# Supplied documents that count as AFS material for a related rule source (REF is the organiser reference).
AFS_DOCS = ("S01", "S02", "S03", "S04", "S05")

# The run's own decision status is never relabelled: its plain label leads, then one short clause.
STATUS_LINE = {
    "provisional_assessment": ("Provisional feasibility assessment",
                               "methods worth testing under the stated conditions, not a final configuration."),
    "insufficient_information": ("Insufficient information",
                                 ("the known facts cannot yet justify a method choice; the next step below "
                                  "is meant to decide it.")),
    "premise_not_supported": ("Premise not supported",
                              ("the sources do not support the customer's premise as stated; the assessment "
                               "below is provisional.")),
    "outside_supported_scope": ("Outside the supported scope",
                                "the request goes beyond what the supplied sources cover."),
}


def status_line(status: str) -> str:
    label, clause = STATUS_LINE[status]
    return f"**{label}:** {clause}"
TIER_TEXT = {"simple": "Simple", "recommended": "Recommended", "extended": "Extended (multi-method)"}
TIER_WORD = {"simple": "simple", "recommended": "recommended", "extended": "extended"}
ROLE_TEXT = {"primary": "primary candidate", "comparison": "comparison candidate",
             "conditional": "conditional candidate", "not_recommended": "not recommended"}
BASIS_TEXT = {"supplied": "supplied AFS sources", "engineering_judgement": "engineering judgement"}
NOTE = "Short view built by code from the saved run JSON (no model call)."
CONFIDENCE_TEXT = ("Confidence rates the basis of the advice, not a predicted accuracy; cost class is relative, "
                   "not a price.")
_ID = re.compile(r"\b[A-Z]\d+\b")
_ID_PAIR = re.compile(r"\b[A-Z]\d+(?:/[A-Z]\d+)+\b")
_BRACKET = re.compile(r"\s*\(([^()]*)\)")
_WORD = re.compile(r"[A-Za-z0-9]")
_TERM = re.compile(r"[a-z]{4,}")   # content words (related-source choice, unknowns already asked)
_COMMON = {"that", "this", "with", "from", "what", "which", "whether", "there", "their", "your", "does", "will",
           "would", "could", "should", "have", "into", "over", "each", "they", "them", "than", "then", "when"}


def word_count(text: str) -> int:
    """Whitespace-separated tokens holding a letter or digit (table rules and bullets do not count)."""
    return sum(1 for token in text.split() if _WORD.search(token))


def verified_set(data: dict) -> set[tuple[str, int, str]]:
    """(doc, page, quote) of every citation the run verified."""
    return {(c["doc"], int(c["page"]), c["quote"]) for c in (data.get("verification") or {}).get("citations", [])
            if c.get("verified")}


def precedent_set(data: dict) -> set[tuple[str, int, str]]:
    """(doc, page, quote) of the verified citations whose page scope allows a precedent only."""
    return {(c["doc"], int(c["page"]), c["quote"]) for c in (data.get("verification") or {}).get("citations", [])
            if c.get("verified") and c.get("scope_status") == "precedent_only"}


class _Brief:
    """One run's brief: id labels, the verified-citation filter and the cited pages in order."""

    def __init__(self, data: dict) -> None:
        self.data = data
        self.a = data["assessment"]
        self.verified = verified_set(data)
        self.precedent_quotes = precedent_set(data)
        self.cited: list[tuple[str, int]] = []
        self.precedent: set[tuple[str, int]] = set()      # cited pages shown as precedent only
        self.recs = {r["id"]: r for r in self.a["recommendations"]}
        self.options = {o["id"]: o for o in self.a["solution_options"]}
        self.question_number: dict[str, int] = {}
        self.labels = self._id_labels()

    # ------------------------------------------------------------- ids
    def _rec_short(self, rec: dict) -> str:
        combo = f" + {' + '.join(rec['combined_with'])}" if rec["combined_with"] else ""
        same = [r for r in self.a["recommendations"]
                if r["method"] == rec["method"] and r["combined_with"] == rec["combined_with"]]
        base = rec["method"] if len(same) <= 1 else method_label(rec["method"], rec["technique"])
        return base + combo

    def _id_labels(self) -> dict[str, str]:
        labels = {o["id"]: f"the {TIER_WORD[o['tier']]} option" for o in self.a["solution_options"]}
        labels |= {r["id"]: self._rec_short(r) for r in self.a["recommendations"]}
        labels |= {p["id"]: p["name"] for p in self.a["parameters"]}
        labels |= {q["id"]: "an open clarification question" for q in self.a["clarification_questions"]}
        return labels

    def clean(self, text: str) -> str:
        """Model text without internal ids: an id-only bracket is dropped, any other known id gets its label."""
        def bracket(m: re.Match) -> str:
            tokens = [t for t in re.split(r"[\s,/;]+|\band\b", m.group(1)) if t]
            return "" if tokens and all(t in self.labels for t in tokens) else m.group(0)

        def name(token: str) -> str:
            if token in self.question_number:
                return f"question {self.question_number[token]}"
            return self.labels.get(token, token)

        def either(m: re.Match) -> str:          # "M2/M3" -> "Raman or NIR + Raman"
            ids = m.group(0).split("/")
            return " or ".join(map(name, ids)) if all(i in self.labels for i in ids) else m.group(0)

        text = _BRACKET.sub(bracket, " ".join(str(text).split()))
        text = _ID_PAIR.sub(either, text)
        return _ID.sub(lambda m: name(m.group(0)), text).strip()

    # ------------------------------------------------------------- citations
    def refs(self, citations: list[dict]) -> str:
        """' [S01 p.10; S02 p.7]' for the verified citations (repeats merged); '' when none is verified."""
        shown: list[tuple[str, int]] = []
        for c in citations:
            key = (c["doc"], int(c["page"]))
            full = (c["doc"], int(c["page"]), c["quote"])
            if full in self.verified and key not in shown:
                shown.append(key)
            if full in self.precedent_quotes:
                self.precedent.add(key)
        for key in shown:
            if key not in self.cited:
                self.cited.append(key)
        return f" [{'; '.join(kb.citation_label(d, p) for d, p in shown)}]" if shown else ""

    def related_source(self, risk: str, rule_ids: list[str]) -> str:
        """A stored AFS source quote of the risk's rules, verbatim on its page, shown as a related source.

        Of the rules' quotes, the one sharing the most words with the risk sentence is shown (the
        first one on a tie); it is never claimed to verify the sentence."""
        rules = {r["id"]: r for r in kb.rules()}
        words = _terms(risk)
        best, best_score = None, -1
        for rid in rule_ids:
            for s in (rules.get(rid) or {}).get("sources", []):
                if s["doc"] not in AFS_DOCS or not quotes.verify(s["doc"], int(s["page"]), s["quote"]).ok:
                    continue
                score = len(words & _terms(s["quote"]))
                if score > best_score:
                    best, best_score = s, score
        if best is None:
            return ""
        label = kb.citation_label(best["doc"], int(best["page"]))
        return f' (related AFS source: {label}, "{" ".join(best["quote"].split())}"; not checked against this sentence)'

    # ------------------------------------------------------------- sections
    def questions(self) -> list[dict]:
        """The top questions in the run's priority order; those that could change the method, the
        technique, the status or a recommendation come before installation-only ones."""
        qs = self.a["clarification_questions"]
        relevant = [q for q in qs if any(x != "installation" for x in q["affects"])]
        picked = (relevant + [q for q in qs if q not in relevant])[:QUESTIONS_SHOWN]
        top = [q for q in qs if q in picked]
        self.question_number = {q["id"]: k for k, q in enumerate(top, 1)}
        return top

    def stated(self) -> list[str]:
        """The customer's verbatim enquiry quotes (intake facts, then targets), repeats and substrings dropped."""
        intake = self.data["intake"]
        unique: list[str] = []
        for q in [f["enquiry_quote"] for f in intake["facts_stated"]] + [t["enquiry_quote"] for t in intake["targets"]]:
            q = " ".join(q.split())
            if q and q.casefold() not in {u.casefold() for u in unique}:
                unique.append(q)
        return [q for i, q in enumerate(unique)
                if not any(q.casefold() in o.casefold() for k, o in enumerate(unique) if k != i)]

    @staticmethod
    def rec_label(rec: dict) -> str:
        combo = f" + {', '.join(rec['combined_with'])} (combination)" if rec["combined_with"] else ""
        return method_label(rec["method"], rec["technique"]) + combo

    def option_methods(self, option: dict) -> str:
        parts = [self.rec_label(self.recs[rid]) for rid in option["recommendation_ids"] if rid in self.recs]
        return "; ".join(parts) or "none named"

    def cost_text(self, option_id: str) -> str:
        cost = (self.data.get("option_costs") or {}).get(option_id) or {}
        if not cost.get("cost_class"):
            return NOT_RATED
        return ("at least " if cost.get("unidentified") else "") + cost["cost_class"]

    def external(self, best_id: str) -> list[str]:
        ext = self.data.get("external") or {}
        sources = {s["id"]: s for s in ext.get("sources", [])}
        items = [it for it in ext.get("items", []) if it.get("option_id") == best_id][:EXTERNAL_SHOWN]
        out = []
        for it in items:
            c = it["citation"]
            src = sources.get(c["source_id"], {})
            link = src.get("url") or (f"https://doi.org/{src['doi']}" if src.get("doi") else "")
            out.append(f"- *{' '.join(str(src.get('title') or 'untitled').split())}* ({src.get('year') or 'n.d.'}), "
                       f"{link}: \"{' '.join(c['quote'].split())}\"")
        return out


def _terms(text: str) -> set[str]:
    return set(_TERM.findall(text.casefold())) - _COMMON


def unasked(unknowns: list[str], questions: list[dict]) -> list[str]:
    """The key unknowns a shown question does not already ask: an unknown sharing at least
    `ASKED_SHARE` of its content words with one shown question is left out (the questions come first)."""
    asked = [_terms(q["question"]) for q in questions]
    out = []
    for u in unknowns:
        words = _terms(u)
        if not words or not any(len(words & q) >= ASKED_SHARE * len(words) for q in asked):
            out.append(u)
    return out


def _cell(text: str) -> str:
    return " ".join(str(text).split()).replace("|", "\\|")


def off_topic_markdown(data: dict, title: str = "", full_answer: str = "") -> str:
    out = [f"# Short brief{': ' + title if title else ''}", ""]
    if full_answer:
        out += [f"*{NOTE} Full answer: {full_answer}.*", ""]
    out += [status_line("outside_supported_scope"), "", data["off_topic"]["message"], ""]
    return "\n".join(out)


def to_markdown(data: dict, title: str = "", full_answer: str = "") -> str:
    """The short brief of one run JSON (an `outputs/<set>/<case>.json` dict)."""
    if data.get("off_topic") is not None or data.get("assessment") is None:
        return off_topic_markdown(data, title, full_answer)
    b = _Brief(data)
    a = b.a
    top_questions = b.questions()           # numbers the questions before any text is cleaned
    out = [f"# Short brief{': ' + title if title else ''}", ""]
    if full_answer:
        out += [f"*{NOTE} Full answer: {full_answer}.*", ""]
    if data.get("still_open"):
        out += [f"⚠ {len(data['still_open'])} verification check(s) still open; see the full answer.", ""]
    if data.get("flagged"):
        out += [f"⚠ {len(data['flagged'])} item(s) flagged by the run's checks; see the full answer.", ""]

    out += [status_line(a["decision_status"]), "", b.clean(a["brief_answer"]), ""]

    out += ["## Requirements", ""]
    stated = b.stated() or [b.clean(s) for s in a["requirements_stated"]]
    if stated:
        out.append("**Stated by the customer:** " + "; ".join(f'"{s}"' for s in stated))
    unknowns = [b.clean(s).rstrip(".") for s in unasked(a["key_unknowns"], top_questions)][:UNKNOWNS_SHOWN]
    if unknowns:
        out += ["", "**Other key unknowns:** " + "; ".join(unknowns) + "."]
    out.append("")

    if top_questions:
        out += ["## Clarification questions", ""]
        out += [f"{k}. {b.clean(q['question'])}" for k, q in enumerate(top_questions, 1)] + [""]

    pr = a["proposal"]
    best = b.options.get(pr["best_current_option"])
    out += ["## Recommendation", ""]
    if best is not None:
        # Each method of the proposed option with its role and the run's verified citations for it;
        # the reasons are in the brief answer above and in full in the full answer.
        used = [b.recs[rid] for rid in best["recommendation_ids"] if rid in b.recs]
        roles = "; ".join(f"{b.rec_label(r)} as {ROLE_TEXT[r['role']]}{b.refs(r['citations'])}" for r in used)
        out += [f"**Proposed now:** the {TIER_WORD[best['tier']]} option (basis: {BASIS_TEXT[pr['basis']]})"
                + (f": {roles}." if roles else "."), ""]
    if a["solution_options"]:
        confidence = data.get("option_confidence") or {}
        out += [f"| Option | Methods | Cost class, {TABLE1_CITATION} | Confidence |", "|---|---|---|---|"]
        for o in a["solution_options"]:
            name = TIER_TEXT[o["tier"]] + (" (proposed)" if best is o else "")
            level = (confidence.get(o["id"]) or {}).get("level", "not rated")
            methods = b.option_methods(o)
            out.append(f"| {name} | {_cell(methods[:1].upper() + methods[1:])} | {b.cost_text(o['id'])} | {level} |")
        out += ["", f"*{CONFIDENCE_TEXT}*", ""]

    mc = a["measurement_concept"]
    out += ["## Measurement concept", "",
            (f"{b.clean(mc['probe_and_geometry'])} **Location:** {b.clean(mc['location'])} "
             f"**Fiber link:** {b.clean(mc['fiber_link'])}{b.refs(mc['citations'])}"), ""]

    methods = {b.recs[rid]["method"] for rid in (best or {}).get("recommendation_ids", []) if rid in b.recs}
    ranges = [s for s in a["spectral_ranges"] if s["method"] in methods] or a["spectral_ranges"]
    if ranges:
        out += ["## Spectral range", ""]
        out += [f"- **{s['method']}:** {b.clean(s['statement'])}{b.refs(s['citations'])}" for s in ranges] + [""]

    if a["risks"]:
        out += ["## Risks and uncertainty", ""]
        for k in a["risks"][:RISKS_SHOWN]:
            refs = b.refs(k["citations"])
            out.append(f"- {b.clean(k['risk'])}{refs or b.related_source(k['risk'], k['rule_ids'])}")
        out.append("")

    fp = a["feasibility_plan"]
    out += ["## Feasibility plan", "",
            f"- **Next step:** {b.clean(pr['next_step'])}",
            f"- **Reference measurements:** {b.clean(fp['reference_measurements'])}",
            f"- **Decision basis:** {b.clean(fp['decision_basis'])}", ""]

    if best is not None:
        lines = b.external(best["id"])
        if lines:
            out += ["## Secondary literature (external, not AFS material)", ""] + lines + [""]

    out += ["## Sources", ""]
    shown = [kb.citation_label(d, p) + (" (precedent only)" if (d, p) in b.precedent else "")
             for d, p in sorted(b.cited, key=lambda k: (k[0] == "REF", k))]
    if a["solution_options"]:
        shown.append(f"{TABLE1_CITATION} for the cost class")
    out += [f"{', '.join(shown) or 'none'}. The verified quotes are listed in the full answer.", ""]
    return "\n".join(out)


def title_from_markdown(path: Path) -> str:
    """The case title from the full answer's first heading ('# First technical assessment: <title>')."""
    if not path.exists():
        return ""
    first = path.read_text(encoding="utf-8").split("\n", 1)[0]
    return first.split(":", 1)[1].strip() if first.startswith("#") and ":" in first else ""


def is_run_json(data: dict) -> bool:
    return isinstance(data, dict) and "assessment" in data and "enquiry" in data


def brief_for(run: Path, out_dir: Path) -> str:
    """The brief of one saved run JSON, linking the full answer next to it relative to `out_dir`."""
    data = json.loads(run.read_text(encoding="utf-8"))
    full = run.with_suffix(".md")
    link = Path(os.path.relpath(full.resolve(), out_dir.resolve())).as_posix()
    return to_markdown(data, title_from_markdown(full), f"[{full.name}]({link})")


def write_briefs(src_dir: Path, out_dir: Path) -> list[tuple[Path, int]]:
    """A brief for every run JSON in `src_dir`, written to `out_dir/<stem>.md`; returns (path, words)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for run in sorted(src_dir.glob("*.json")):
        if not is_run_json(json.loads(run.read_text(encoding="utf-8"))):
            continue
        text = brief_for(run, out_dir)
        target = out_dir / f"{run.stem}.md"
        target.write_text(text, encoding="utf-8")
        written.append((target, word_count(text)))
    return written
