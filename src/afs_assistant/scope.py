"""Evidence-scope check: may this page support this kind of claim? (rules R-EVI-*)"""

from __future__ import annotations

from afs_assistant import kb

# Claim kinds the assessment can make, and the page scopes allowed to support them.
# A readiness claim needs evidence from the same setting; no supplied page shows
# validated clinical use, so clinical readiness can never be supported.
ALLOWED_SCOPES = {
    "general": {"method", "component_spec", "concept", "lab_example", "process_example",
                "literature_map", "research_study", "clinical_aspiration", "guidance"},
    "application_precedent": {"lab_example", "process_example", "research_study", "literature_map"},
    "readiness_process": {"process_example"},
    "readiness_clinical": set(),
    "performance_figure": {"component_spec", "method", "lab_example", "process_example", "research_study"},
}


def check(claim_kind: str, doc: str, page: int) -> tuple[bool, str]:
    record = kb.page(doc, page)
    if record is None:
        return False, f"{kb.citation_label(doc, page)} does not exist"
    allowed = ALLOWED_SCOPES.get(claim_kind)
    if allowed is None:
        return False, f"unknown claim kind {claim_kind!r}"
    scopes = set(record["scope"])
    if scopes & allowed:
        return True, "ok"
    label = kb.citation_label(doc, page)
    if claim_kind == "readiness_clinical":
        return False, f"no supplied source validates clinical use; {label} is {sorted(scopes)} (R-EVI-1, R-EVI-3)"
    return False, f"{label} is {sorted(scopes)}, which cannot support a {claim_kind} claim (R-EVI-1)"
