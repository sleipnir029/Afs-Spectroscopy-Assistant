"""Phase 3 fix round (3.R) offline tests: review fixes B1-B3 and N1-N10, two layers,
the code-derived confidence rating, and the distinct-options check.

Same made-up generic enquiry and fixtures as test_phase2 (no dev or final scenario text).
"""

from __future__ import annotations

import copy
import json
import re

import pytest
import yaml
from test_phase2 import ASSESSMENT, INTAKE, RAMAN_QUOTE, cit, run_with
from test_phase3 import EXTENDED, _load_script, hard, soft, still_open, with_

from afs_assistant import kb, paths, pipeline, render
from afs_assistant.llm import config
from afs_assistant.options import (
    CONFIDENCE_NOTE,
    confidence,
    confidence_label,
    option_confidence,
)
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import SLOT_VALUES, TECHNIQUES, screen
from afs_assistant.verify import (
    MAX_ANSWER_WORDS,
    PRICE_PATTERN,
    RECHECK_NAMES,
    forbidden_hits,
    sanitize_intake,
)

LIQUID_CLEAR = {"physical_state": "liquid", "optical_regime": "clear", "aqueous": "yes"}


# ----------------------------------------------------------------- B1 ids unique
@pytest.mark.parametrize("key", ["recommendations", "solution_options", "parameters"])
def test_duplicate_ids_are_a_hard_failure(key):
    a = with_()
    a[key][1]["id"] = a[key][0]["id"]
    result, _ = run_with(assess=a, repairs=[a, a])
    fail = [c for c in hard(result, "ids_unique") if c.location == key]
    assert fail and a[key][0]["id"] in fail[0].message
    assert "ids_unique" in RECHECK_NAMES


def test_duplicate_option_ids_stay_open_after_finalize():
    a = with_()
    a["solution_options"][1]["id"] = "O1"
    a["proposal"]["best_current_option"] = "O1"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert "ids_unique" in still_open(result)


def test_unique_ids_pass():
    result, _ = run_with()
    assert all(c.passed for c in result.report.checks if c.name == "ids_unique")
    assert {c.location for c in result.report.checks if c.name == "ids_unique"} == {
        "recommendations", "solution_options", "parameters"}


# ----------------------------------------------------------------- B2 proposal basis
def test_supplied_basis_without_a_verified_citation_becomes_engineering_judgement():
    a = with_()
    a["solution_options"][1]["citations"] = []
    a["recommendations"][0]["citations"] = [cit("S01", 16, "Raman measures ethanol in every broth.")]  # fails
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.proposal.basis == "engineering_judgement"
    change = next(x for x in result.removed if x["location"] == "proposal.basis")
    assert change["corrects"] == "proposal_basis" and change["item"] == "supplied"
    assert "engineering judgement" in result.flagged["proposal"]
    assert "**Basis:** engineering judgement" in render.to_markdown(result)


def test_supplied_basis_with_a_verified_citation_on_a_recommendation_stays():
    a = with_()
    a["solution_options"][1]["citations"] = []                       # M1 keeps RAMAN_QUOTE
    result, _ = run_with(assess=a)
    assert result.assessment.proposal.basis == "supplied"
    assert not any(x["location"] == "proposal.basis" for x in result.removed)


def test_basis_flag_is_added_to_a_removed_option_flag():
    a = with_()
    a["proposal"]["best_current_option"] = "O9"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.proposal.basis == "engineering_judgement"
    assert "removed by verification" in result.flagged["proposal"] and "engineering judgement" in result.flagged["proposal"]


# ----------------------------------------------------------------- B3 currency
@pytest.mark.parametrize("text", ["The probe costs $ 900.", "About 900 USD.", "Some euros for the probe.",
                                  "A few thousand dollars.", "Priced in CHF.", "£ 50 for the cable.", "€ 10 each.",
                                  "Budget 3 GBP per sample.", "One euro per run."])
def test_currency_in_model_text_is_a_price_hit(text):
    assert any(h.startswith("price") for h in forbidden_hits(text)), text


def test_currency_negation_handling_is_unchanged():
    assert forbidden_hits("We cannot quote any price in euros here.") == []
    assert re.search(PRICE_PATTERN, "Measured in dollars", re.IGNORECASE)


def test_currency_in_an_option_cell_is_a_hard_failure():
    a = with_()
    a["solution_options"][0]["cost_drivers"] = "Mostly the spectrometer, a few thousand dollars"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert "price" in hard(result, "forbidden_wording")[0].message


def test_markdown_has_no_currency_anywhere_and_no_cost_footer():
    result, _ = run_with(assess=with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))
    result.manifest["cost_usd"] = 0.0123
    md = render.to_markdown(result)
    assert not re.search(PRICE_PATTERN, md, re.IGNORECASE)
    assert "cost" not in md.rsplit("*Run ", 1)[1]
    assert render.to_json(result)["manifest"]["cost_usd"] == 0.0123          # still in the JSON


def test_cost_class_script_scans_the_whole_markdown_for_currency(tmp_path):
    result, _ = run_with()
    (tmp_path / "X.json").write_text(json.dumps(render.to_json(result)), encoding="utf-8")
    md = render.to_markdown(result)
    (tmp_path / "X.md").write_text(md, encoding="utf-8")
    script = _load_script("check_cost_class")
    assert script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1()) == []
    (tmp_path / "X.md").write_text(md + "\n*cost $0.01*\n", encoding="utf-8")
    problems = script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1())
    assert any("currency" in p for p in problems)


# ----------------------------------------------------------------- N1 single primary out of scope
def test_single_primary_is_skipped_outside_the_supported_scope():
    a = with_(decision_status="outside_supported_scope")
    a["recommendations"][0]["role"] = "comparison"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert not [c for c in result.report.checks if c.name == "single_primary"]
    assert "single_primary" not in still_open(result)
    b = with_(decision_status="insufficient_information")
    b["recommendations"][0]["role"] = "comparison"
    assert hard(run_with(assess=b, repairs=[b, b])[0], "single_primary")


# ----------------------------------------------------------------- N2 option parameter refs
def test_option_referencing_a_missing_parameter_is_a_hard_failure():
    a = with_()
    a["solution_options"][1]["parameter_ids"] = ["P1", "P9"]
    result, _ = run_with(assess=a, repairs=[a, a])
    fail = hard(result, "option_parameter_refs")
    assert fail and "P9" in fail[0].message and "option_parameter_refs" in still_open(result)


# ----------------------------------------------------------------- 4b options distinct
def test_two_options_with_the_same_recommendations_are_a_hard_failure():
    a = with_()
    a["solution_options"][0]["recommendation_ids"] = ["M1"]
    result, _ = run_with(assess=a, repairs=[a, a])
    fail = hard(result, "options_distinct")
    assert fail and "O1 = O2" in fail[0].message and "options_distinct" in still_open(result)


def test_order_of_recommendation_ids_does_not_make_options_distinct():
    a = with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    a["solution_options"][1]["recommendation_ids"] = ["M2", "M1"]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "options_distinct")
    assert not hard(run_with()[0], "options_distinct")


def test_remap_to_the_same_entry_makes_options_equal_and_stays_open():
    a = with_()
    dup = copy.deepcopy(a["recommendations"][0])
    dup.update(id="M3", role="comparison")
    a["recommendations"].append(dup)
    a["solution_options"][0]["recommendation_ids"] = ["M3"]          # remapped to M1, same as O2
    result, _ = run_with(assess=a, repairs=[a, a])
    assert "options_distinct" in still_open(result)


# ----------------------------------------------------------------- N3, N5, N6, N7
def test_invalid_best_option_does_not_echo_the_model_value():
    a = with_()
    a["proposal"]["best_current_option"] = "the Raman one"
    md = render.to_markdown(run_with(assess=a, repairs=[a, a])[0])
    proposal = md.split("## Proposal", 1)[1].split("\n## ", 1)[0]
    assert "**Best current option:** (invalid option id)" in proposal and "the Raman one" not in proposal


def test_prompt_says_numbers_in_brief_answer_and_proposal_come_from_the_enquiry():
    text = pipeline.prompt("assess")
    assert "`brief_answer` and `proposal` carry no citations: use a number there only if it appears in the " \
           "customer's enquiry." in text


def test_placeholder_quote_with_a_real_value_is_reported():
    intake = copy.deepcopy(INTAKE)
    intake["process"].append({"aspect": "temperature", "value": "about hot", "enquiry_quote": "unknown"})
    _, removed = sanitize_intake(Intake.model_validate(intake), "We want to follow ethanol.")
    item = next(x for x in removed if x["location"] == "intake.process[1]")
    assert not item.get("placeholder")
    assert "intake.process[1]" in render.to_markdown(run_with(intake=intake)[0])


def test_remap_reason_names_the_role_change():
    a = with_()
    dup = copy.deepcopy(a["recommendations"][0])
    dup.update(id="M3", role="comparison")
    a["recommendations"].append(dup)
    a["solution_options"][1]["recommendation_ids"] = ["M3"]
    result, _ = run_with(assess=a, repairs=[a, a])
    reason = next(x["reason"] for x in result.removed if "now M1" in x.get("reason", ""))
    assert "role changed from comparison to primary" in reason


def test_remap_reason_without_a_role_change_says_nothing_about_roles():
    a = with_()
    dup = copy.deepcopy(a["recommendations"][0])
    dup.update(id="M3")                                              # same role (primary)
    a["recommendations"].append(dup)
    a["solution_options"][1]["recommendation_ids"] = ["M3"]
    result, _ = run_with(assess=a, repairs=[a, a])
    reason = next(x["reason"] for x in result.removed if "now M1" in x.get("reason", ""))
    assert "role" not in reason


# ----------------------------------------------------------------- N8, N9, N10 scripts and docs
def test_mermaid_script_prints_the_parse_error_line():
    script = _load_script("check_mermaid")
    stderr = "\n".join([f"    at frame{i} (file.js:{i})" for i in range(30)][:10] + [
        "Error: Parse error on line 3:", "...probe1[\"x\"] -->", "------^", "Expecting 'SEMI', got 'EOF'"]
        + [f"    at frame{i} (file.js:{i})" for i in range(30)])
    excerpt = script.error_excerpt(stderr)
    assert excerpt.startswith("Error: Parse error on line 3:") and "Expecting 'SEMI'" in excerpt
    assert script.error_excerpt("plain failure") == "plain failure"


def test_rules_yaml_slot_vocabulary_matches_slot_values():
    header = paths.RULES_FILE.read_text(encoding="utf-8").split("\nrules:", 1)[0]
    for slot, allowed in SLOT_VALUES.items():
        m = re.search(rf"^#\s+{slot}: ([^(\n]+)", header, re.MULTILINE)
        assert m, slot
        documented = {v.strip() for v in m.group(1).split("|")} - {"unknown"}
        assert documented == allowed, (slot, documented, allowed)
    yaml.safe_load(paths.RULES_FILE.read_text(encoding="utf-8"))


def test_cost_class_script_has_its_own_mapping():
    source = (paths.ROOT / "scripts" / "check_cost_class.py").read_text(encoding="utf-8")
    assert not re.search(r"^\s*(?:from|import) afs_assistant", source, re.MULTILINE)
    script = _load_script("check_cost_class")
    assert script.TECHNIQUES == TECHNIQUES                            # same content, independent copy


# ----------------------------------------------------------------- two layers
def test_answer_comes_first_and_expert_detail_holds_the_rest():
    md = render.to_markdown(run_with()[0])
    answer, expert = md.split("\n# Expert detail\n", 1)
    for part in ("**Customer request:** Follow ethanol in a flowing aqueous fermentation broth.", "## Brief answer",
                 "## Proposal", "**Decision status:**", "## Solution options", "## Setup sketch", "## Key questions"):
        assert part in answer
    for part in ("## Parameters", "## Requirements", "## Recommendation",
                 "## Evidence (verified quotes)", "## Verification", "**Customer enquiry**"):
        assert part in expert and part not in answer
    assert "cost drivers" not in answer and "**O2 cost drivers:**" in expert


def test_answer_shows_only_the_top_three_questions():
    words = ["one", "two", "three", "four", "five"]
    questions = [{"id": f"Q{i}", "question": f"Question number {w}?", "why_it_matters": "Decides the method.",
                  "affects": ["M1"]} for i, w in enumerate(words, 1)]
    md = render.to_markdown(run_with(assess=with_(clarification_questions=questions))[0])
    answer, expert = md.split("\n# Expert detail\n", 1)
    key = answer.split("## Key questions", 1)[1]
    assert "Question number three?" in key and "Question number four?" not in key and "Why it matters" not in key
    assert all(f"Question number {w}?" in expert for w in ("one", "five"))


def test_request_line_falls_back_to_the_enquiry_when_the_summary_has_an_unsupported_figure():
    intake = copy.deepcopy(INTAKE)
    intake["summary"] = "Follow ethanol down to 3 g/L in a broth."
    md = render.to_markdown(run_with(intake=intake)[0])
    assert "**Customer request:** We want to follow ethanol in a clear aqueous fermentation broth" in md
    assert "3 g/L" not in md


def test_answer_length_is_a_soft_check():
    ok, _ = run_with()
    assert not soft(ok, "answer_length")
    answer = render.to_markdown(ok).split("\n# Expert detail\n", 1)[0]
    assert len(re.sub(r"```mermaid.*?```", "", answer, flags=re.DOTALL).split()) <= MAX_ANSWER_WORDS
    long = with_(status_reason=" ".join(["word"] * (MAX_ANSWER_WORDS + 1)))
    result, _ = run_with(assess=long)
    assert soft(result, "answer_length") and result.report.passed


# ----------------------------------------------------------------- confidence rating (one test per rule)
def _assessment(**changes) -> Assessment:
    return Assessment.model_validate(with_(**changes))


def _conf(a: Assessment, option_id: str, slots: dict = LIQUID_CLEAR) -> dict:
    option = next(o for o in a.solution_options if o.id == option_id)
    return confidence(a, option, screen(slots), slots)


def test_confidence_no_downgrade_is_high():
    assert _conf(_assessment(), "O2") == {"level": "High", "reasons": []}


def test_confidence_rule1_unknown_deciding_slot():
    slots = {"physical_state": "liquid"}                     # clarity unknown: NIR transmission open
    conf = _conf(_assessment(), "O1", slots)
    assert conf == {"level": "Medium", "reasons": ["sample clarity unknown"]}
    assert _conf(_assessment(), "O2", slots)["level"] == "High"    # Raman probe passes on "liquid"


def test_confidence_rule1_counts_a_combined_method_without_its_own_entry():
    a = _assessment()
    a.recommendations[0].combined_with = ["Fluorescence"]        # fluorophore unknown -> Fluorescence open
    conf = _conf(a, "O2")
    assert "fluorescent target unknown" in conf["reasons"]


def test_confidence_rule2_no_verified_citation_and_precedent_only():
    a = _assessment()
    a.solution_options[1].citations = []
    a.recommendations[0].citations = []
    assert _conf(a, "O2")["reasons"] == ["no verified source citation"]
    a.recommendations[0].citations = [cit_model("S01", 16, RAMAN_QUOTE, "application_precedent")]
    assert _conf(a, "O2")["reasons"] == ["precedent only"]


def cit_model(doc, page, quote, kind):
    from afs_assistant.schema import Citation

    return Citation.model_validate(cit(doc, page, quote, kind))


def test_confidence_rule3_uncited_required_auxiliary_sensor_or_not_measurable():
    a = _assessment()
    a.parameters[1].necessity = "required"
    assert _conf(a, "O2")["reasons"] == ["uncited auxiliary sensor"]
    a.parameters[1].citations = [cit_model("S01", 16, RAMAN_QUOTE, "general")]
    assert _conf(a, "O2")["reasons"] == []
    a.parameters[1].necessity = "optional"
    a.parameters[0].measured_by.type = "not_measurable_inline"
    assert _conf(a, "O2")["reasons"] == ["a required parameter is not measurable in-line"]


def test_confidence_rule3_ignores_an_optional_auxiliary_sensor():
    a = _assessment()
    assert a.parameters[1].necessity == "optional" and not a.parameters[1].citations
    assert _conf(a, "O2")["level"] == "High"


def test_confidence_rule4_contradicted_premise_or_status():
    premise = {"premise": "Water blocks Raman.", "verdict": "contradicted", "explanation": "Low water absorbance.",
               "citations": [cit("S01", 16, RAMAN_QUOTE)]}
    a = _assessment(decision_status="premise_not_supported", premise_checks=[premise])
    assert _conf(a, "O2")["reasons"] == ["a customer premise is contradicted, status: premise not supported"]
    b = _assessment(decision_status="insufficient_information")
    assert _conf(b, "O2")["reasons"] == ["status: insufficient information"]


def test_confidence_rule5_multi_method():
    a = _assessment(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    assert _conf(a, "O3") == {"level": "Medium", "reasons": ["multi-method, fusion benefit not yet shown"]}


def test_confidence_floor_is_low_and_all_reasons_are_kept():
    a = _assessment(decision_status="insufficient_information",
                    solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    for r in a.recommendations:
        r.citations = []
    a.parameters[1].necessity = "required"
    conf = _conf(a, "O3", {"physical_state": "liquid"})
    assert conf["level"] == "Low" and len(conf["reasons"]) == 5
    assert confidence_label(conf).startswith("Low: sample clarity unknown; no verified source citation; ")


def test_confidence_is_rendered_and_in_the_json():
    a = with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    result, _ = run_with(assess=a)
    md = render.to_markdown(result)
    assert "| O3 | Extended (multi-method) | M1 Raman probe; M2 NIR, transmission/transflection probe | " \
           "Medium: multi-method, fusion benefit not yet shown | high (rows 7, 12) |" in md
    assert CONFIDENCE_NOTE in md and "not a predicted accuracy" in CONFIDENCE_NOTE
    data = render.to_json(result)
    assert data["option_confidence"] == option_confidence(result.assessment, result.candidates, result.slots)
    assert data["option_confidence"]["O2"] == {"level": "High", "reasons": []}


def test_model_never_writes_the_confidence():
    assert "confidence" not in json.dumps(Assessment.model_json_schema()).lower()
    assert "never write one yourself" in pipeline.prompt("assess")


# ----------------------------------------------------------------- 4b max tokens
def test_assess_and_repair_have_room_for_reasoning():
    roles = config()["roles"]
    assert roles["assess"]["max_tokens"] >= 64000 and roles["repair"]["max_tokens"] >= 64000


def test_currency_codes_are_case_sensitive_so_journal_abbreviations_pass():
    import re

    from afs_assistant.verify import PRICE_PATTERN

    pat = re.compile(PRICE_PATTERN, re.IGNORECASE)
    assert pat.search("about 5,000 EUR")
    assert pat.search("a few thousand euros")
    assert not pat.search("Eur. Urol. 2009, 56, 636-643")
    assert not pat.search("Usd and Chf are not codes here")
