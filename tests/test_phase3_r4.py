"""Phase 3 fix round 3.R4 offline tests (3.R3 code review): the visible intake warning, customer
words in the stated-requirements fallback, near-match screen reasons, the `affects` vocabulary,
quiet finalize logging, the merged precedent badge, the confidence starting level and the
"at least" cost cross-check.

Same made-up generic enquiry and fixtures as test_phase2 (no dev or final scenario text).
"""

from __future__ import annotations

import copy
import json

from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE, run_with
from test_phase3 import EXTENDED, _load_script, with_
from test_phase3_r import _clean, _conf
from test_phase3_r3 import _cand, _client, _collapsed_intake

from afs_assistant import kb, pipeline, render
from afs_assistant.schema import Citation, Intake
from afs_assistant.verify import intake_problems, normalize_affects, sanitize_intake

TABLE1 = "S01 Table 1 (p.6)"


# ----------------------------------------------------------------- 1. B1 visible intake warning
def test_collapsed_intake_shows_a_warning_line_in_the_verification_section():
    result = pipeline.run(ENQUIRY, _client([_collapsed_intake(), _collapsed_intake()]), run_id="t")
    verification = render.to_markdown(result).split("### Verification\n", 1)[1]
    assert "- ⚠ Intake incomplete after 2 attempt(s): no target left after checking the quotes against the " \
           "enquiry\n" in verification


def test_clean_intake_has_no_intake_warning_line():
    assert "Intake incomplete" not in render.to_markdown(run_with()[0])


def test_placeholder_only_vague_intake_is_not_collapsed():
    vague = copy.deepcopy(INTAKE)
    vague["facts_stated"] = [{"text": "unknown", "enquiry_quote": "unknown"}, {"text": "n/a", "enquiry_quote": "n/a"}]
    vague["process"] = [{"aspect": "temperature", "value": "not stated", "enquiry_quote": "not stated"}]
    intake, removed = sanitize_intake(Intake.model_validate(vague), ENQUIRY)
    assert len(removed) == 3 and all(r.get("placeholder") for r in removed)
    assert intake_problems(intake, removed) == []


def test_invented_items_still_count_next_to_placeholders():
    bad = copy.deepcopy(INTAKE)
    bad["facts_stated"] = [{"text": "unknown", "enquiry_quote": "unknown"},
                           {"text": "Invented", "enquiry_quote": "never written here"}]
    problems = intake_problems(*sanitize_intake(Intake.model_validate(bad), ENQUIRY))
    assert problems == []                                   # 1 of 3 (target, process, invented fact)
    bad["process"] = []
    problems = intake_problems(*sanitize_intake(Intake.model_validate(bad), ENQUIRY))
    assert problems == ["1 of 2 intake items removed (quote not verbatim in the enquiry)"]


# ----------------------------------------------------------------- 2. B2 customer words only
def test_stated_fallback_shows_only_verified_customer_words_deduplicated():
    intake = copy.deepcopy(INTAKE)
    intake["facts_stated"][0]["text"] = "Broth is very clear, invented paraphrase"
    intake["facts_stated"].append({"text": "Another paraphrase", "enquiry_quote": "clear  aqueous fermentation broth"})
    md = render.to_markdown(run_with(intake=intake, assess=with_(requirements_stated=[]))[0])
    block = md.split("**Stated by the customer**\n\n", 1)[1].split("\n\n", 1)[0]
    assert block == '- "clear aqueous fermentation broth"\n- "follow ethanol"'
    assert "paraphrase" not in md and "Target:" not in md


# ----------------------------------------------------------------- 3. N1 both screen reasons
def test_near_match_keeps_the_dark_sample_reason():
    slots = {"physical_state": "soft_solid", "optical_regime": "opaque_absorbing"}
    c = _cand(slots, "NIR", "diffuse_reflection_remote")                  # Table 1: solid, powder
    table = [r["message"] for r in c.reasons if r["rule"] == TABLE1]
    assert c.status == "unknown" and len(table) == 2
    assert table[0].endswith("fit for soft solid to be tested") and table[1].startswith("dark, absorbing")


def test_near_match_keeps_the_unknown_regime_reason():
    c = _cand({"physical_state": "soft_solid"}, "NIR", "diffuse_reflection_remote")
    table = [r["message"] for r in c.reasons if r["rule"] == TABLE1]
    assert c.status == "unknown" and len(table) == 2
    assert table[0].endswith("fit for soft solid to be tested") and table[1].startswith("sample state or optical")


def test_without_a_near_match_the_branches_are_unchanged():
    dark = _cand({"physical_state": "liquid", "optical_regime": "opaque_absorbing"}, "NIR", "diffuse_reflection_remote")
    assert [r["message"] for r in dark.reasons if r["rule"] == TABLE1] == [
        "dark, absorbing (non-scattering) sample: diffuse reflection signal must be tested"]
    near = _cand({"physical_state": "soft_solid", "optical_regime": "turbid"}, "Fluorescence", "fluorescence_probe")
    assert len([r for r in near.reasons if r["rule"] == TABLE1]) == 1


def test_both_reasons_reach_the_confidence_phrase():
    a = _clean()
    a.recommendations[0].method, a.recommendations[0].technique = "NIR", "diffuse_reflection_remote"
    slots = {"physical_state": "soft_solid", "optical_regime": "opaque_absorbing", "aqueous": "yes"}
    assert _conf(a, "O2", slots)["reasons"] == [
        "fit for soft solid to be tested, diffuse reflection on a dark sample untested"]


# ----------------------------------------------------------------- 4. N2 affects vocabulary
def test_any_word_starting_with_method_means_the_method_choice():
    assert normalize_affects(["methods", "Method selection", "method-choice", "O2", "m1"]) == (
        ["method", "O2", "M1"], [])


def test_an_option_id_in_a_top_question_affects_that_option():
    a = _clean()
    a.clarification_questions[0].affects = ["o2"]
    assert _conf(a, "O2")["reasons"] == ["open question: Q1 (starts at Medium)"]
    assert _conf(a, "O1")["reasons"] == []


# ----------------------------------------------------------------- 5. N3 finalize logs only drops
def test_case_only_normalisation_is_not_logged():
    a = with_()
    a["clarification_questions"][0]["affects"] = ["Method", "m2", "O1"]
    result, _ = run_with(assess=a)
    assert result.assessment.clarification_questions[0].affects == ["method", "M2", "O1"]
    assert not [x for x in result.removed if x["location"].endswith(".affects")]


# ----------------------------------------------------------------- 6. N4 merged precedent badge
def test_merged_evidence_entry_keeps_the_precedent_badge():
    general = Citation.model_validate({"doc": "S02", "page": 13, "quote": "a quote", "claim_kind": "general"})
    figure = Citation.model_validate({"doc": "S02", "page": 13, "quote": "a quote",
                                      "claim_kind": "performance_figure"})
    cite = render._Citer()
    assert cite.refs([general]) == cite.refs([figure]) == " [1: S02 p.13]"
    assert len(cite.entries) == 1 and cite.precedent == [True]
    other = render._Citer()
    other.refs([general])
    assert other.precedent == [False]


# ----------------------------------------------------------------- 7. confidence starting level
def test_single_weakness_without_an_open_question_is_medium():
    a = _clean(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    assert _conf(a, "O2")["level"] == "High" and _conf(a, "O3")["level"] == "Medium"


def test_open_question_separates_a_fusion_option_from_a_single_method_option():
    a = _clean(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    a.clarification_questions[0].affects = ["method"]
    assert _conf(a, "O2") == {"level": "Medium", "reasons": ["open question: Q1 (starts at Medium)"]}
    assert _conf(a, "O3") == {"level": "Low", "reasons": ["open question: Q1 (starts at Medium)",
                                                          "multi-method, fusion benefit not yet shown"]}


def test_confidence_note_describes_the_starting_level():
    md = render.to_markdown(run_with()[0])
    assert "It starts at High, or at Medium when a key question on the method or the option is open" in md


# ----------------------------------------------------------------- 8. N7 "at least" cross-check
def _cost_pair(tmp_path, combined: list[str]):
    a = with_(solution_options=ASSESSMENT["solution_options"] + [{**EXTENDED, "recommendation_ids": ["M1"]}])
    a["recommendations"][0]["combined_with"] = combined
    a["recommendations"][0]["role"] = "comparison"
    a["recommendations"][1]["role"] = "primary"
    a["solution_options"][1]["recommendation_ids"] = ["M1", "M2"]
    result, _ = run_with(assess=a)
    (tmp_path / "X.json").write_text(json.dumps(render.to_json(result)), encoding="utf-8")
    return render.to_markdown(result)


def test_cost_script_flags_a_missing_at_least(tmp_path):
    script = _load_script("check_cost_class")
    md = _cost_pair(tmp_path, ["MIR"])
    assert "at least high cost (row 12); MIR row not identified" in md
    (tmp_path / "X.md").write_text(md.replace("at least high cost", "high cost"), encoding="utf-8")
    problems = script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1())
    assert any("'at least' expected when" in p for p in problems)


def test_cost_script_flags_a_spurious_at_least(tmp_path):
    script = _load_script("check_cost_class")
    md = _cost_pair(tmp_path, ["NIR"])
    assert "| high cost (rows 7, 12) |" in md
    (tmp_path / "X.md").write_text(md.replace("| high cost (rows 7, 12) |", "| at least high cost (rows 7, 12) |"),
                                   encoding="utf-8")
    problems = script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1())
    assert any("'at least' expected only when" in p for p in problems)
