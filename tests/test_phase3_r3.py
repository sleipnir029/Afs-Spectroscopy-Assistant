"""Phase 3 fix round 3.R3 offline tests (G3 review): collapsed intake, near-match sample types,
the `affects` vocabulary, comparison vs fusion, stated-requirements fallback, combined-method
cost, the calibrated confidence rating and the simplicity items.

Same made-up generic enquiry and fixtures as test_phase2 (no dev or final scenario text).
"""

from __future__ import annotations

import copy
import json

import pytest
from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE, RAMAN_QUOTE, cit, run_with
from test_phase3 import EXTENDED, _load_script, soft, with_
from test_phase3_r import _clean, _conf

from afs_assistant import kb, pipeline, render
from afs_assistant.llm import FakeClient
from afs_assistant.options import cost_class, is_fusion, option_costs
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import screen
from afs_assistant.verify import (
    AFFECTS_WORDS,
    answer_texts,
    intake_problems,
    normalize_affects,
    request_text,
    sanitize_intake,
)


def _client(intakes, assess=ASSESSMENT):
    return FakeClient({"intake": list(intakes), "assess": [assess], "repair": []})


def _collapsed_intake() -> dict:
    """Most items carry a quote that is not in the enquiry, and the only target is lost."""
    bad = copy.deepcopy(INTAKE)
    bad["facts_stated"] += [{"text": f"Invented fact {i}", "enquiry_quote": f"words never written {i}"}
                            for i in range(3)]
    bad["targets"] = [{"variable": "ethanol", "purpose": "follow", "enquiry_quote": "a quote that is not there"}]
    return bad


# ----------------------------------------------------------------- B1 collapsed intake
def test_collapsed_intake_fails_the_intake_check():
    intake, removed = sanitize_intake(Intake.model_validate(_collapsed_intake()), ENQUIRY)
    problems = intake_problems(intake, removed)
    assert any("no target" in p for p in problems) and any("4 of 6 intake items removed" in p for p in problems)
    assert intake_problems(*sanitize_intake(Intake.model_validate(INTAKE), ENQUIRY)) == []


def test_half_of_the_intake_items_removed_fails_even_with_a_target():
    bad = copy.deepcopy(INTAKE)
    bad["facts_stated"] += [{"text": f"Invented {i}", "enquiry_quote": f"never written {i}"} for i in range(3)]
    problems = intake_problems(*sanitize_intake(Intake.model_validate(bad), ENQUIRY))
    assert problems == ["3 of 6 intake items removed (quote not verbatim in the enquiry, or a placeholder)"]


def test_collapsed_intake_is_retried_once_and_the_retry_is_used():
    client = _client([_collapsed_intake(), INTAKE])
    result = pipeline.run(ENQUIRY, client, run_id="t")
    assert [c["role"] for c in client.seen].count("intake") == 2
    assert result.manifest["intake_attempts"] == 2
    assert result.intake.targets and result.intake_removed == []


def test_intake_that_collapses_twice_fails_the_case():
    with pytest.raises(RuntimeError, match="intake failed after 2 attempts"):
        pipeline.run(ENQUIRY, _client([_collapsed_intake(), _collapsed_intake()]), run_id="t")


def test_clean_intake_is_not_retried():
    assert run_with()[0].manifest["intake_attempts"] == 1


@pytest.mark.parametrize("summary", [
    "Самая распространенная ошибка в производстве.",            # not Latin script
    "Customer asks about a measurement problem.",                 # fewer than 3 content words shared
])
def test_request_line_falls_back_to_the_enquiry(summary):
    assert request_text(summary, ENQUIRY) == ENQUIRY
    intake = copy.deepcopy(INTAKE)
    intake["summary"] = summary
    md = render.to_markdown(run_with(intake=intake)[0])
    assert f"**Customer request:** {ENQUIRY}" in md and summary not in md


def test_request_line_keeps_a_summary_in_the_enquirys_words():
    assert request_text(INTAKE["summary"], ENQUIRY) == INTAKE["summary"]


# ----------------------------------------------------------------- B2 near-match sample types
def _cand(slots, method, technique):
    return next(c for c in screen(slots) if (c.method, c.technique) == (method, technique))


def test_soft_solid_against_a_solid_row_is_to_be_tested_not_failed():
    slots = {"physical_state": "soft_solid", "optical_regime": "turbid", "fluorophore": "yes"}
    c = _cand(slots, "Fluorescence", "fluorescence_probe")              # Table 1: liquid, solid
    assert c.status == "unknown"
    assert c.reasons == [{"status": "unknown", "rule": "S01 Table 1 (p.6)",
                          "message": "Table 1 lists ['liquid', 'solid'] for this technique; "
                                     "fit for soft solid to be tested"}]
    assert _cand(slots, "UV-Vis", "transmission_transflection").status == "fail"     # liquid only


def test_paste_against_a_liquid_row_is_to_be_tested():
    c = _cand({"physical_state": "paste", "optical_regime": "turbid"}, "UV-Vis", "ATR")   # Table 1: liquid
    table = [r for r in c.reasons if r["rule"] == "S01 Table 1 (p.6)"]
    assert table and table[0]["status"] == "unknown" and table[0]["message"].endswith("fit for paste to be tested")


def test_far_apart_states_still_fail():
    c = _cand({"physical_state": "powder", "optical_regime": "opaque"}, "UV-Vis", "ATR")    # liquid only
    assert c.status == "fail"
    assert _cand({"physical_state": "liquid", "optical_regime": "clear"}, "NIR", "diffuse_reflection_remote").status \
        == "fail"                                                                              # powder, solid


def test_near_match_reason_is_the_confidence_phrase():
    a = _clean()
    a.recommendations[0].method, a.recommendations[0].technique = "Raman", "raman_probe"
    slots = {"physical_state": "soft_solid", "optical_regime": "clear", "aqueous": "yes"}
    assert _conf(a, "O2", slots) == {"level": "Medium", "reasons": ["fit for soft solid to be tested"]}


# ----------------------------------------------------------------- B3 affects vocabulary
def test_affects_vocabulary_is_in_the_schema_and_the_prompt():
    desc = Assessment.model_json_schema()["$defs"]["Question"]["properties"]["affects"]["description"]
    assert all(f"'{w}'" in desc for w in AFFECTS_WORDS) and "M1" in desc
    assert "`affects`: each item is exactly one of `method`" in pipeline.prompt("assess")


def test_normalize_affects_maps_synonyms_and_drops_other_words():
    assert normalize_affects(["method", "Method choice", "method_choice", "m2", "status"]) == (
        ["method", "M2", "status"], [])
    assert normalize_affects(["O1", "installation", "the budget"]) == (["installation"], ["O1", "the budget"])


def test_finalize_normalises_affects_and_logs_the_change():
    a = with_()
    a["clarification_questions"][0]["affects"] = ["method_choice", "O2", "M2"]
    result, _ = run_with(assess=a)
    assert result.assessment.clarification_questions[0].affects == ["method", "M2"]
    change = next(x for x in result.removed if x["location"] == "clarification_questions[0].affects")
    assert change["item"] == ["method_choice", "O2", "M2"] and "dropped ['O2']" in change["reason"]
    assert result.report.passed and not render.open_failures(result)


def test_the_models_real_method_spelling_caps_every_option():
    a = _clean()
    a.clarification_questions[0].affects = ["method"]
    assert _conf(a, "O1")["level"] == _conf(a, "O2")["level"] == "Medium"


# ----------------------------------------------------------------- B4 comparison is not fusion
TWO_METHODS = {**EXTENDED, "id": "O3", "tier": "simple", "fusion_note": None}


def _with_options(*options) -> Assessment:
    a = _clean()
    a.solution_options = [type(a.solution_options[0]).model_validate(o) for o in options]
    return a


def test_two_methods_side_by_side_are_not_fusion():
    a = _with_options(ASSESSMENT["solution_options"][1], TWO_METHODS)
    recs = {r.id: r for r in a.recommendations}
    assert not is_fusion(a.solution_options[1], recs)
    assert _conf(a, "O3")["reasons"] == []
    chart = render.mermaid_chart(a, a.solution_options[1], {})
    assert "fusion" not in chart.lower()
    assert 'model1["Chemometric model (Raman)"]' in chart and 'model2["Chemometric model (NIR)"]' in chart
    assert "spec1 --> model1" in chart and "spec2 --> model2" in chart
    assert "model1 --> result" in chart and "model2 --> result" in chart
    assert "aux1 -.-> model1" in chart and "aux1 -.-> model2" in chart


@pytest.mark.parametrize("change", ["extended", "fusion_note", "combined_with"])
def test_fusion_needs_the_extended_tier_a_fusion_note_or_a_combination(change):
    option = copy.deepcopy(TWO_METHODS)
    if change == "extended":
        option["tier"] = "extended"
    elif change == "fusion_note":
        option["fusion_note"] = "Same spot, synchronised; must beat the best single method."
    a = _with_options(ASSESSMENT["solution_options"][1], option)
    if change == "combined_with":
        a.recommendations[0].combined_with = ["NIR"]
        a.solution_options[1].recommendation_ids = ["M1"]
    recs = {r.id: r for r in a.recommendations}
    assert is_fusion(a.solution_options[1], recs)
    assert _conf(a, "O3")["reasons"] == ["multi-method, fusion benefit not yet shown"]
    assert 'model["Data fusion model (per-method calibration)"]' in render.mermaid_chart(a, a.solution_options[1], {})


# ----------------------------------------------------------------- B5 stated requirements
def test_empty_stated_requirements_show_the_intake_facts_and_targets():
    md = render.to_markdown(run_with(assess=with_(requirements_stated=[]))[0])
    block = md.split("**Stated by the customer**\n\n", 1)[1].split("\n\n", 1)[0]
    assert block == "- Broth is clear and aqueous\n- Target: ethanol (follow during fermentation)"


def test_intake_item_with_an_unsupported_figure_shows_its_quote():
    intake = copy.deepcopy(INTAKE)
    intake["facts_stated"][0]["text"] = "Broth is clear, about 5 % ethanol"
    md = render.to_markdown(run_with(intake=intake, assess=with_(requirements_stated=[]))[0])
    assert "- clear aqueous fermentation broth\n" in md and "5 %" not in md


def test_stated_requirements_are_used_when_present():
    md = render.to_markdown(run_with()[0])
    assert "- Ethanol in a clear aqueous broth\n" in md and "Target: ethanol" not in md


# ----------------------------------------------------------------- B6 combined-method cost
def test_combined_method_takes_the_technique_of_another_recommendation():
    a = Assessment.model_validate(with_())
    a.recommendations[0].combined_with = ["NIR"]                 # M2 is NIR transmission (row 7)
    a.solution_options[1].recommendation_ids = ["M1"]
    c = cost_class(a.solution_options[1], {r.id: r for r in a.recommendations})
    assert [r["row"] for r in c.rows] == [7, 12] and c.unidentified == [] and c.label() == "high cost (rows 7, 12)"


def test_combined_method_without_any_technique_is_a_lower_bound():
    a = Assessment.model_validate(with_())
    a.recommendations[0].combined_with = ["MIR"]
    c = cost_class(a.solution_options[1], {r.id: r for r in a.recommendations})
    assert c.label() == "at least high cost (row 12); MIR row not identified"
    assert option_costs(a)["O2"]["unidentified"] == ["MIR"]


def test_not_recommended_technique_is_not_borrowed():
    a = Assessment.model_validate(with_())
    a.recommendations[1].role = "not_recommended"
    a.recommendations[0].combined_with = ["NIR"]
    c = cost_class(a.solution_options[1], {r.id: r for r in a.recommendations})
    assert c.label() == "at least high cost (row 12); NIR row not identified"


def test_cost_script_agrees_with_borrowed_and_lower_bound_costs(tmp_path):
    script = _load_script("check_cost_class")
    for combined in (["NIR"], ["MIR"]):
        a = with_(solution_options=ASSESSMENT["solution_options"] + [
            {**EXTENDED, "recommendation_ids": ["M1"]}])
        a["recommendations"][0]["combined_with"] = combined
        a["recommendations"][0]["role"] = "comparison"
        a["recommendations"][1]["role"] = "primary"
        a["solution_options"][1]["recommendation_ids"] = ["M1", "M2"]
        result, _ = run_with(assess=a)
        (tmp_path / "X.json").write_text(json.dumps(render.to_json(result)), encoding="utf-8")
        (tmp_path / "X.md").write_text(render.to_markdown(result), encoding="utf-8")
        assert script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1()) == [], combined


# ----------------------------------------------------------------- item 7 calibration
def test_open_question_caps_at_medium_and_does_not_stack():
    a = _clean()
    a.clarification_questions[0].affects = ["M1"]
    a.solution_options[1].citations = []
    a.recommendations[0].citations = [cit_precedent()]
    conf = _conf(a, "O2")
    assert conf == {"level": "Medium", "reasons": ["precedent only", "open question: Q1 (at most Medium)"]}


def test_cap_reason_is_listed_when_the_level_is_already_low():
    a = _clean(decision_status="insufficient_information")
    a.clarification_questions[0].affects = ["method"]
    a.solution_options[1].citations = []
    a.recommendations[0].citations = []
    conf = _conf(a, "O2")
    assert conf["level"] == "Low"
    assert conf["reasons"] == ["no verified source citation", "status: insufficient information",
                               "open question: Q1 (at most Medium)"]


def cit_precedent():
    from afs_assistant.schema import Citation

    return Citation.model_validate(cit("S01", 16, RAMAN_QUOTE, "application_precedent"))


# ----------------------------------------------------------------- item 8 simplicity
def _layers(md: str) -> tuple[str, str]:
    return tuple(md.split("\n## Expert detail\n", 1))


def test_decision_status_is_a_label_in_the_answer_and_prose_in_the_expert_detail():
    result, _ = run_with()
    answer, expert = _layers(render.to_markdown(result))
    reason = ASSESSMENT["status_reason"]
    assert "**Decision status:** Provisional feasibility assessment\n" in answer and reason not in answer
    assert f"**Decision status:** Provisional feasibility assessment. {reason}" in expert
    assert reason not in answer_texts(result.assessment, "")


def test_extended_sketch_moves_to_the_expert_detail():
    result, _ = run_with(assess=with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))
    answer, expert = _layers(render.to_markdown(result))
    assert answer.count("```mermaid") == 1 and "*Recommended option O2;" in answer
    assert expert.count("```mermaid") == 1 and "*Extended (multi-method) option O3;" in expert
    assert set(render.to_json(result)["setup_sketches"]) == {"O2", "O3"}


def test_best_current_option_shows_id_and_tier_only():
    answer, _ = _layers(render.to_markdown(run_with()[0]))
    assert "- **Best current option:** O2 (recommended)\n" in answer


def test_identical_quotes_share_one_evidence_number():
    md = render.to_markdown(run_with()[0])
    evidence = md.split("### Evidence (verified quotes)\n\n", 1)[1].split("\n\n", 1)[0]
    assert evidence.count(RAMAN_QUOTE) == 1
    number = next(line for line in evidence.splitlines() if RAMAN_QUOTE in line).split(".", 1)[0]
    assert md.count(f"[{number}: S01 p.16]") >= 3     # option, recommendation, measurement concept, range


def test_brief_answer_naming_a_method_outside_the_proposal_is_a_soft_warning():
    ok, _ = run_with()
    assert not soft(ok, "brief_answer_methods")
    a = with_(brief_answer="Test a Raman probe first and MIR as well. The ethanol range is still open.")
    result, _ = run_with(assess=a)
    warning = soft(result, "brief_answer_methods")
    assert warning and "['MIR']" in warning[0].message and result.report.passed
    a["recommendations"][1]["role"] = "conditional"
    a["brief_answer"] = "Test a Raman probe first; NIR transmission only if the range is high."
    assert not soft(run_with(assess=a)[0], "brief_answer_methods")


def test_prompt_lines_for_short_cells_and_never_speaking_for_afs():
    text = pipeline.prompt("assess")
    assert "(about 6 words)" in text and "Never speak for AFS" in text and '"we will confirm"' in text
    assert "no other section repeats its sentences" in text
