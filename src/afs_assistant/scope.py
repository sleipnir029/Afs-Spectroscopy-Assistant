"""Evidence-scope check: what can this page support for this kind of claim? (rules R-EVI-*)

Result status:
  ok              the page can support the claim
  precedent_only  the page shows a related application: a reason to test, not proof (R-EVI-2)
  not_supported   the page cannot support the claim

Readiness claims (process or clinical) are never `ok`: no supplied page validates a
setup for a new customer. Pages carrying any tag listed in R-EVI-1's
`evidence_scope_not` cannot even serve as precedent for readiness.
"""

from __future__ import annotations

from functools import lru_cache

from afs_assistant import kb

CLAIM_KINDS = ("general", "application_precedent", "performance_figure", "method_gain",
               "readiness_process", "readiness_clinical")
_PRECEDENT_SCOPES = {"lab_example", "process_example", "research_study", "literature_map", "concept"}


@lru_cache(maxsize=1)
def readiness_forbidden_scopes() -> frozenset[str]:
    """Single source of truth: R-EVI-1 target.evidence_scope_not in knowledge/rules.yaml."""
    rule = next(r for r in kb.rules() if r["id"] == "R-EVI-1")
    return frozenset(rule["target"]["evidence_scope_not"])


def check(claim_kind: str, doc: str, page: int) -> tuple[str, str]:
    if claim_kind not in CLAIM_KINDS:
        raise ValueError(f"unknown claim kind {claim_kind!r}; expected one of {CLAIM_KINDS}")
    record = kb.page(doc, page)
    label = kb.citation_label(doc, page)
    if record is None:
        return "not_supported", f"{label} does not exist"
    scopes = set(record["scope"])

    if claim_kind == "general":
        if scopes <= {"business"}:
            return "not_supported", f"{label} is business context, not technical evidence"
        return "ok", "ok"
    if claim_kind == "application_precedent":
        if scopes & {"lab_example", "process_example", "research_study", "literature_map"}:
            return "ok", "ok"
        return "not_supported", f"{label} is {sorted(scopes)}: no application example on this page"
    if claim_kind == "performance_figure":
        forbidden = scopes & readiness_forbidden_scopes()
        if scopes & {"method", "component_spec", "guidance"} and not forbidden:
            return "ok", "ok"
        if scopes & _PRECEDENT_SCOPES:
            return "precedent_only", (f"{label} is {sorted(scopes)}: its figures come from a specific study, example "
                                      f"or literature and do not transfer to a new setup (R-EVI-2)")
        return "not_supported", f"{label} is {sorted(scopes)}: cannot support a performance figure"
    if claim_kind == "method_gain":
        if scopes & _PRECEDENT_SCOPES or "guidance" in scopes:
            return "precedent_only", f"a gain from combining methods is a hypothesis to test (R-CMB-1); {label} is precedent"
        return "not_supported", f"{label} is {sorted(scopes)}: no basis for a combination gain"
    if claim_kind == "readiness_clinical":
        return "not_supported", f"no supplied source validates clinical use; {label} is {sorted(scopes)} (R-EVI-1, R-EVI-3)"
    # readiness_process
    forbidden = scopes & readiness_forbidden_scopes()
    if forbidden:
        return "not_supported", f"{label} carries {sorted(forbidden)}, which cannot support readiness (R-EVI-1)"
    if "process_example" in scopes:
        return "precedent_only", f"{label} is a process example: a reason to test, not proof for this customer (R-EVI-2)"
    return "not_supported", f"{label} is {sorted(scopes)}: no process evidence"
