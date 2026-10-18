"""Plan 5.R1 offline tests (D-047): the two structure checks, their repair trigger and the finalize fallbacks.

Same made-up generic enquiry and fixtures as test_phase2 (no dev, adversarial or final scenario text).
"""

from __future__ import annotations

import copy

from test_phase2 import ASSESSMENT, run_with
from test_phase3 import still_open
from test_phase5_eval import _write

from afs_assistant import evaluate, pipeline, render
from afs_assistant.evaluate import FAIL, PASS
from afs_assistant.schema import Assessment
from afs_assistant.verify import (
    METHOD_ADDED_FLAG,
    QUESTION_ADDED_FLAG,
    RECHECK_NAMES,
    Report,
    check_options,
    check_questions,
    recheck,
)

UNKNOWNS = ["Ethanol concentration range", "Broth temperature.", "Line pressure", "Cleaning cycle"]
# A self-combined comparison entry (its own method in combined_with) in an extended option.
SELF_COMBINED = {"id": "M3", "method": "MIR", "technique": "ATR", "role": "comparison", "combined_with": ["MIR"],
                 "rationale": "MIR ATR suits a clear liquid.", "conditions": "none", "citations": []}
EXTENDED = {"id": "O3", "tier": "extended", "recommendation_ids": ["M3"], "parameter_ids": ["P1"],
            "ease_of_use": "Two probes at one port", "maintenance": "Two calibrations to keep",
            "performance_fit": "Only if one method is not enough", "cost_drivers": "Two spectrometers",
            "fusion_note": "Same spot, synchronised acquisition, one model per method first; must beat the best "
                           "single method.", "citations": []}


def with_(**changes) -> dict:
    a = copy.deepcopy(ASSESSMENT)
    a.update(copy.deepcopy(changes))
    return a


def hard(report_or_result, name: str) -> list:
    report = getattr(report_or_result, "report", report_or_result)
    return [c for c in report.hard_failures if c.name == name]


def no_questions(**changes) -> dict:
    return with_(clarification_questions=[], key_unknowns=UNKNOWNS, **changes)


def self_combined(**changes) -> dict:
    a = with_(**changes)
    a["recommendations"].append(copy.deepcopy(SELF_COMBINED))
    a["solution_options"].append(copy.deepcopy(EXTENDED))
    return a


# ----------------------------------------------------------------- questions_for_unknowns
def test_no_question_with_open_unknowns_is_a_hard_failure():
    report = Report()
    check_questions(Assessment.model_validate(no_questions()), report)
    assert hard(report, "questions_for_unknowns")
    assert "questions_for_unknowns" in RECHECK_NAMES


def test_no_question_with_a_non_provisional_status_is_a_hard_failure():
    report = Report()
    a = with_(clarification_questions=[], key_unknowns=[], decision_status="insufficient_information")
    check_questions(Assessment.model_validate(a), report)
    assert hard(report, "questions_for_unknowns")


def test_no_question_needed_without_unknowns_on_a_provisional_status():
    report = Report()
    check_questions(Assessment.model_validate(with_(clarification_questions=[], key_unknowns=[])), report)
    assert not hard(report, "questions_for_unknowns")


def test_missing_questions_trigger_a_repair_that_fixes_them():
    result, client = run_with(assess=no_questions(), repairs=[with_(key_unknowns=UNKNOWNS)])
    assert [s["role"] for s in client.seen] == ["intake", "assess", "repair"]
    repair_user = next(s["user"] for s in client.seen if s["role"] == "repair")
    assert "[questions_for_unknowns] clarification_questions" in repair_user
    assert result.report.passed and result.manifest["finalize_fallbacks"] == []
    assert not any(x.get("corrects") == "questions_for_unknowns" for x in result.removed)


def test_question_fallback_builds_up_to_three_questions_from_the_first_unknowns():
    a = no_questions()
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "questions_for_unknowns")              # the kept round still has no question
    qs = result.assessment.clarification_questions
    assert [q.id for q in qs] == ["Q1", "Q2", "Q3"]
    assert qs[0].question == "Could you tell us more about this open point: ethanol concentration range?"
    assert qs[1].question.endswith("broth temperature?")          # the trailing full stop is replaced
    assert all(q.affects == ["status"] and q.why_it_matters == pipeline.FALLBACK_WHY for q in qs)
    changes = [x for x in result.removed if x.get("corrects") == "questions_for_unknowns"]
    assert [x["location"] for x in changes] == [f"clarification_questions[{i}]" for i in range(3)]
    assert all(f"clarification_questions[{i}]" in result.flagged for i in range(3))
    assert result.manifest["finalize_fallbacks"] == ["questions_for_unknowns"]
    assert "questions_for_unknowns" not in still_open(result)
    assert not hard(recheck(result.assessment, result.candidates), "questions_for_unknowns")
    payload = render.to_json(result)
    assert sum(x.get("corrects") == "questions_for_unknowns" for x in payload["finalize_changes"]) == 3


def test_question_fallback_skips_an_unknown_with_an_unsupported_figure():
    a = with_(clarification_questions=[], key_unknowns=["Line pressure above 40 bar", "Ethanol concentration range"])
    result, _ = run_with(assess=a, repairs=[a, a])
    qs = result.assessment.clarification_questions
    assert len(qs) == 1 and "ethanol concentration range" in qs[0].question
    assert "questions_for_unknowns" not in still_open(result)


def test_fallback_question_keeps_an_acronym_and_lower_cases_a_plain_word():
    text = pipeline._question_text
    assert text("Whether the line is cleaned daily.") == ("Could you tell us more about this open point: "
                                                          "whether the line is cleaned daily?")
    assert text("MIR fibre length for the link.").endswith("point: MIR fibre length for the link?")
    assert text("NaCl content of the broth").endswith("point: NaCl content of the broth?")
    assert text("pH range").endswith("point: pH range?")


def test_question_fallback_sees_a_status_that_finalize_changed():
    contradicted = {"premise": "Raman cannot be used in water.", "verdict": "contradicted",
                    "explanation": "Water interferes little with Raman.",
                    "citations": [ASSESSMENT["recommendations"][0]["citations"][0]]}
    a = no_questions(premise_checks=[contradicted])
    assert a["decision_status"] == "provisional_assessment"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.decision_status == "premise_not_supported"     # finalize step 5
    assert len(result.assessment.clarification_questions) == 3
    locations = [x["location"] for x in result.removed]
    assert locations.index("decision_status") < locations.index("clarification_questions[0]")
    assert not hard(recheck(result.assessment, result.candidates), "questions_for_unknowns")
    assert "questions_for_unknowns" not in still_open(result)


def test_question_fallback_cannot_build_without_unknowns_and_stays_open():
    a = with_(clarification_questions=[], key_unknowns=[], decision_status="insufficient_information",
              status_reason="The facts given cannot justify a method choice yet.")
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.clarification_questions == []
    assert "questions_for_unknowns" in still_open(result)
    assert result.manifest["finalize_fallbacks"] == []


# ----------------------------------------------------------------- extended_two_methods
def test_extended_option_whose_only_combination_is_its_own_method_is_a_hard_failure():
    report = Report()
    a = Assessment.model_validate(self_combined())
    check_options(a, [], report)
    fail = hard(report, "extended_two_methods")
    assert fail and fail[0].location == "solution_options[2]" and "['MIR']" in fail[0].message
    assert "extended_two_methods" in RECHECK_NAMES


def test_extended_option_with_a_real_second_method_passes():
    a = self_combined()
    a["recommendations"][2]["combined_with"] = ["NIR"]
    report = Report()
    check_options(Assessment.model_validate(a), [], report)
    assert not hard(report, "extended_two_methods")


def test_not_recommended_entry_does_not_count_as_a_method():
    a = self_combined()
    a["recommendations"].append({"id": "M4", "method": "UV-Vis", "technique": "ATR", "role": "not_recommended",
                                 "combined_with": [], "rationale": "Not needed.", "conditions": "none",
                                 "citations": []})
    a["solution_options"][2]["recommendation_ids"] = ["M3", "M4"]
    report = Report()
    check_options(Assessment.model_validate(a), [], report)
    assert hard(report, "extended_two_methods")


def test_one_method_extended_option_triggers_a_repair_that_fixes_it():
    fixed = self_combined()
    fixed["solution_options"][2]["recommendation_ids"] = ["M3", "M1"]
    result, client = run_with(assess=self_combined(), repairs=[fixed])
    repair_user = next(s["user"] for s in client.seen if s["role"] == "repair")
    assert "[extended_two_methods] solution_options[2]" in repair_user
    assert not hard(result, "extended_two_methods") and result.manifest["finalize_fallbacks"] == []


def test_extended_fallback_adds_the_primary_before_other_finalize_steps():
    a = self_combined()
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "extended_two_methods")
    o3 = next(o for o in result.assessment.solution_options if o.id == "O3")
    assert o3.recommendation_ids == ["M3", "M1"]
    m3 = next(r for r in result.assessment.recommendations if r.id == "M3")
    assert m3.combined_with == []                                   # the normalisation still ran
    change = next(x for x in result.removed if x.get("corrects") == "extended_two_methods")
    assert change["location"] == "solution_options[2].recommendation_ids" and change["item"] == ["M3"]
    assert "primary M1 (Raman)" in change["reason"]
    locations = [x["location"] for x in result.removed]
    assert locations.index(change["location"]) < locations.index("recommendations[2].combined_with")
    assert result.flagged["solution_options[2]"] == METHOD_ADDED_FLAG
    assert result.manifest["finalize_fallbacks"] == ["extended_two_methods"]
    assert "extended_two_methods" not in still_open(result) and not result.recheck


def test_extended_fallback_skips_a_pick_that_would_copy_another_option():
    a = self_combined()
    a["solution_options"][1]["recommendation_ids"] = ["M1", "M3"]   # O3 + M1 would equal O2: M2 is next
    result, _ = run_with(assess=a, repairs=[a, a])
    o3 = next(o for o in result.assessment.solution_options if o.id == "O3")
    assert o3.recommendation_ids == ["M3", "M2"]
    assert "extended_two_methods" not in still_open(result)


def test_extended_fallback_does_nothing_when_every_pick_would_copy_an_option():
    a = self_combined()
    a["solution_options"][0]["recommendation_ids"] = ["M2", "M3"]
    a["solution_options"][1]["recommendation_ids"] = ["M1", "M3"]
    result, _ = run_with(assess=a, repairs=[a, a])
    o3 = next(o for o in result.assessment.solution_options if o.id == "O3")
    assert o3.recommendation_ids == ["M3"]
    assert "extended_two_methods" in still_open(result) and result.manifest["finalize_fallbacks"] == []


def test_extended_fallback_adds_the_comparison_when_the_primary_has_the_same_method():
    a = self_combined()
    a["recommendations"][2]["method"], a["recommendations"][2]["technique"] = "Raman", "ATR"
    a["recommendations"][2]["combined_with"] = ["Raman"]
    result, _ = run_with(assess=a, repairs=[a, a])
    o3 = next(o for o in result.assessment.solution_options if o.id == "O3")
    assert o3.recommendation_ids == ["M3", "M2"]
    change = next(x for x in result.removed if x.get("corrects") == "extended_two_methods")
    assert "comparison M2 (NIR)" in change["reason"]
    assert "extended_two_methods" not in still_open(result)


def test_extended_fallback_never_adds_a_primary_that_failed_screening():
    a = self_combined()
    a["recommendations"][0]["method"], a["recommendations"][0]["technique"] = "NIR", "diffuse_reflection"
    result, _ = run_with(assess=a, repairs=[a, a])
    o3 = next(o for o in result.assessment.solution_options if o.id == "O3")
    assert "M1" not in o3.recommendation_ids and o3.recommendation_ids == ["M3", "M2"]
    change = next(x for x in result.removed if x.get("corrects") == "extended_two_methods")
    assert "comparison M2 (NIR)" in change["reason"]


# ----------------------------------------------------------------- eval agrees with verify
def _eval_run(tmp_path, result):
    return _write(tmp_path, render.to_json(result), render.to_markdown(result, "Synthetic"))


def test_eval_options_rules_counts_methods_like_verify(tmp_path):
    a = self_combined()
    a["recommendations"].append({"id": "M4", "method": "UV-Vis", "technique": "ATR", "role": "not_recommended",
                                 "combined_with": [], "rationale": "Not needed.", "conditions": "none",
                                 "citations": []})
    a["solution_options"][2]["recommendation_ids"] = ["M3", "M4"]
    data = render.to_json(run_with(assess=a, repairs=[a, a])[0])
    data["assessment"] = a                       # the model's options, before finalize changed them
    result, reason = evaluate.options_rules(evaluate.Run(data, ""))
    assert result == FAIL and "O3 combines fewer than two methods" in reason


def test_eval_flag_check_ignores_fallback_flags_only(tmp_path):
    a = no_questions()
    result, _ = run_with(assess=a, repairs=[a, a])
    assert set(result.flagged.values()) == {QUESTION_ADDED_FLAG}
    run = _eval_run(tmp_path, result)
    assert evaluate.no_flagged_figures(run)[0] == PASS
    run.data["flagged"]["brief_answer"] = "contains a figure not found in its sources or the enquiry"
    verdict, reason = evaluate.no_flagged_figures(run)
    assert verdict == FAIL and "brief_answer" in reason and "clarification_questions" not in reason
