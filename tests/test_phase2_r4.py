"""Phase 2 fixes 2.R4 (offline): section checks, plan-step text, combination key, prompt lines, regressions.

Same made-up generic enquiry and fixtures as test_phase2 (no dev or final scenario text).
"""

from __future__ import annotations

import copy

import pytest
from test_phase2 import ASSESSMENT, failures, run_with

from afs_assistant import pipeline, render
from afs_assistant.methods import named_methods
from afs_assistant.schema import Assessment
from afs_assistant.verify import Report, check_style, forbidden_hits


# ----------------------------------------------------------------- 1. spectral ranges present
def test_clean_fixture_has_no_section_failures():
    result, _ = run_with()
    names = {c.name for c in result.report.checks if not c.passed}
    assert not names & {"spectral_ranges_present", "spectral_range_per_method", "plan_step_text"}


def test_empty_spectral_ranges_with_a_recommended_method_is_a_hard_failure():
    a = copy.deepcopy(ASSESSMENT)
    a["spectral_ranges"] = []
    result, client = run_with(assess=a, repairs=[a, a])
    fail = failures(result, "spectral_ranges_present")
    assert fail and fail[0].location == "spectral_ranges"
    repair_user = next(s["user"] for s in client.seen if s["role"] == "repair")
    assert "[spectral_ranges_present] spectral_ranges:" in repair_user


def test_empty_spectral_ranges_without_a_recommended_method_passes_that_check():
    a = copy.deepcopy(ASSESSMENT)
    a["spectral_ranges"] = []
    for r in a["recommendations"]:
        r["role"] = "not_recommended"
    a["decision_status"] = "insufficient_information"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert not failures(result, "spectral_ranges_present")


def test_recommended_method_without_its_range_is_a_soft_warning():
    a = copy.deepcopy(ASSESSMENT)
    a["spectral_ranges"] = [s for s in a["spectral_ranges"] if s["method"] != "Raman"]
    result, _ = run_with(assess=a)
    assert result.report.passed
    soft = [c for c in result.report.soft_failures if c.name == "spectral_range_per_method"]
    assert len(soft) == 1 and "Raman" in soft[0].message


# ----------------------------------------------------------------- 2. plan-step text
@pytest.mark.parametrize("step", ["1", "2.", " 3) ", "Collect samples", "Step"])
def test_bare_number_or_short_plan_step_is_a_hard_failure(step):
    a = copy.deepcopy(ASSESSMENT)
    a["feasibility_plan"]["steps"][0]["step"] = step
    result, _ = run_with(assess=a, repairs=[a, a])
    assert any(c.location == "feasibility_plan.steps[0]" for c in failures(result, "plan_step_text"))


def test_render_strips_a_leading_step_number():
    a = copy.deepcopy(ASSESSMENT)
    a["feasibility_plan"]["steps"][0]["step"] = "1. Collect samples from the line."
    a["feasibility_plan"]["steps"].append({"step": "2) Measure GC references on them.",
                                           "purpose": "Reference values.", "citations": []})
    a["feasibility_plan"]["steps"].append({"step": "1.5 mm probe gap: test it on the samples.",
                                           "purpose": "Path length.", "citations": []})
    result, _ = run_with(assess=a, repairs=[a, a])          # "1.5 mm" is not in the enquiry: flagged, still shown
    md = render.to_markdown(result)
    assert "1. **Collect samples from the line.**" in md and "1. **1." not in md
    assert "2. **Measure GC references on them.**" in md and "2) " not in md
    assert "3. **1.5 mm probe gap" in md


# ----------------------------------------------------------------- 3. combination is its own entry
def _combo_assessment() -> Assessment:
    a = copy.deepcopy(ASSESSMENT)
    base = {"technique": "diffuse_reflection", "rationale": "Diffuse reflection for comparison.",
            "conditions": "none", "citations": []}
    a["recommendations"] = [
        {**base, "id": "M1", "method": "NIR", "role": "primary", "combined_with": []},
        {**base, "id": "M2", "method": "NIR", "role": "conditional", "combined_with": ["Raman"]},
    ]
    return Assessment.model_validate(a)


def test_combination_beside_its_single_method_is_not_a_duplicate():
    report = Report()
    check_style(_combo_assessment(), report)
    assert next(c for c in report.checks if c.name == "recommendations_unique").passed


def test_combination_order_does_not_matter_for_uniqueness_or_dedupe():
    a = _combo_assessment().model_dump()
    a["recommendations"][0]["combined_with"] = ["MIR", "Raman"]
    a["recommendations"][1]["combined_with"] = ["Raman", "MIR"]
    a = Assessment.model_validate(a)
    report = Report()
    check_style(a, report)
    assert not next(c for c in report.checks if c.name == "recommendations_unique").passed
    final, removed, _ = pipeline.finalize(a, Report(), [])
    assert [r.id for r in final.recommendations] == ["M1"]
    assert any("duplicate" in x.get("reason", "") for x in removed)


def test_finalize_keeps_a_combination_beside_its_single_method():
    final, removed, _ = pipeline.finalize(_combo_assessment(), Report(), [])
    assert [(r.id, r.combined_with) for r in final.recommendations] == [("M1", []), ("M2", ["Raman"])]
    assert not any("duplicate" in x.get("reason", "") for x in removed)


def test_same_combination_twice_is_still_a_duplicate():
    a = _combo_assessment().model_dump()
    a["recommendations"].append({**a["recommendations"][1], "id": "M3", "role": "not_recommended"})
    report = Report()
    check_style(Assessment.model_validate(a), report)
    assert not next(c for c in report.checks if c.name == "recommendations_unique").passed


# ----------------------------------------------------------------- 3-4. assess prompt lines
def test_assess_prompt_has_the_2r4_lines():
    text = pipeline.prompt("assess")
    assert ("a combination (non-empty `combined_with`) is its own `comparison` or `conditional` entry" in text
            and "never a `primary`, and never a reason to invent another technique" in text)
    assert 'must not use pipeline jargon such as "deterministic screening"' in text
    assert "A fact the customer stated is never a premise" in text


# ----------------------------------------------------------------- 5. small regressions
@pytest.mark.parametrize("text", [
    "We cannot - at this stage - guarantee the result.",
    "We cannot – at this stage – guarantee the result.",
    "We cannot — at this stage — guarantee the result.",
])
def test_dash_aside_after_auxiliary_negation_is_not_flagged(text):
    assert forbidden_hits(text) == []


@pytest.mark.parametrize("text", [
    "No further testing needed - it will work.",
    "No further testing needed — it will work.",
    "It is not cheap - it will work.",
])
def test_dash_after_no_or_closing_clause_is_still_flagged(text):
    assert forbidden_hits(text)


@pytest.mark.parametrize("text, expected", [
    ("Fluorimetry is used in the lab.", {"Fluorescence": "Fluorimetry"}),
    ("A fluorometer gives the reference.", {"Fluorescence": "fluorometer"}),
    ("We rely on fluorometry today.", {"Fluorescence": "fluorometry"}),
    ("The resin is non fluorescent.", {}),
    ("The resin is non-fluorescent and nonfluorescent.", {}),
    ("Autofluorescence is a background.", {"Fluorescence": "Autofluorescence"}),
    ("Fluorine and fluoride content.", {}),
    ("A trifluoromethyl group and tetrafluoromethane.", {}),
    ("A fluorometric assay.", {"Fluorescence": "fluorometric"}),
])
def test_fluorescence_method_words(text, expected):
    assert named_methods(text) == expected
