"""Phase 3 fix rounds (3.R, 3.R2) offline tests: review fixes B1-B3 and N1-N10, two layers,
the code-derived confidence rating, the distinct-options check, and the 3.R2 fixes
(precedent by page scope, unscreened technique, open top questions, Sources cell pool,
open-check warning, currency codes, request label, heading levels).

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
    option_citations,
    option_confidence,
)
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import SLOT_VALUES, TECHNIQUES, screen
from afs_assistant.verify import (
    MAX_ANSWER_WORDS,
    PRICE_PATTERN,
    RECHECK_NAMES,
    answer_texts,
    forbidden_hits,
    request_text,
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
    proposal = md.split("\n### Proposal\n", 1)[1].split("\n#", 1)[0]
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
    answer, expert = md.split("\n## Expert detail\n", 1)
    for part in ("**Customer request (our summary):** Follow ethanol in a flowing aqueous fermentation broth.",
                 "### Brief answer", "### Proposal", "**Decision status:**", "### Solution options", "### Setup sketch",
                 "### Key questions"):
        assert part in answer
    for part in ("### Parameters", "### Requirements", "### Recommendation",
                 "### Evidence (verified quotes)", "### Verification", "**Customer enquiry**"):
        assert part in expert and part not in answer
    assert "cost drivers" not in answer and "**O2 cost drivers:**" in expert


def test_answer_shows_only_the_top_three_questions():
    words = ["one", "two", "three", "four", "five"]
    questions = [{"id": f"Q{i}", "question": f"Question number {w}?", "why_it_matters": "Decides the method.",
                  "affects": ["M1"]} for i, w in enumerate(words, 1)]
    md = render.to_markdown(run_with(assess=with_(clarification_questions=questions))[0])
    answer, expert = md.split("\n## Expert detail\n", 1)
    key = answer.split("### Key questions", 1)[1]
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
    answer = render.to_markdown(ok).split("\n## Expert detail\n", 1)[0]
    assert len(re.sub(r"```mermaid.*?```", "", answer, flags=re.DOTALL).split()) <= MAX_ANSWER_WORDS
    long = with_()
    long["proposal"]["next_step"] = " ".join(["word"] * (MAX_ANSWER_WORDS + 1))
    result, _ = run_with(assess=long)
    assert soft(result, "answer_length") and result.report.passed


# ----------------------------------------------------------------- confidence rating (one test per rule)
def _assessment(**changes) -> Assessment:
    return Assessment.model_validate(with_(**changes))


def cit_model(doc, page, quote, kind="general"):
    from afs_assistant.schema import Citation

    return Citation.model_validate(cit(doc, page, quote, kind))


def _clean(**changes) -> Assessment:
    """The fixture with nothing that downgrades O2: the auxiliary sensor cited, no question on a method."""
    a = _assessment(**changes)
    a.parameters[1].citations = [cit_model("S01", 16, RAMAN_QUOTE)]
    for q in a.clarification_questions:
        q.affects = ["status"]
    return a


def _conf(a: Assessment, option_id: str, slots: dict = LIQUID_CLEAR) -> dict:
    option = next(o for o in a.solution_options if o.id == option_id)
    return confidence(a, option, screen(slots), slots)


def test_confidence_no_downgrade_is_high():
    assert _conf(_clean(), "O2") == {"level": "High", "reasons": []}


def test_confidence_rule1_unknown_deciding_slot():
    slots = {"physical_state": "liquid"}                     # clarity unknown: NIR transmission open
    conf = _conf(_clean(), "O1", slots)
    assert conf == {"level": "Medium", "reasons": ["sample clarity unknown"]}
    assert _conf(_clean(), "O2", slots)["level"] == "High"    # Raman probe passes on "liquid"


def test_confidence_rule1_counts_a_combined_method_without_its_own_entry():
    a = _clean()
    a.recommendations[0].combined_with = ["Fluorescence"]        # fluorophore unknown -> Fluorescence open
    conf = _conf(a, "O2")
    assert "fluorescent target unknown" in conf["reasons"]


@pytest.mark.parametrize("method,technique", [("Raman", "to_be_determined"), ("NIR", "ATR")])
def test_confidence_rule1_unscreened_or_undetermined_technique(method, technique):
    a = _clean()
    a.recommendations[0].method, a.recommendations[0].technique = method, technique
    assert _conf(a, "O2") == {"level": "Medium", "reasons": ["technique not screened for this sample"]}


def test_confidence_rule1_open_top_question_on_the_option():
    a = _clean()
    a.clarification_questions[0].affects = ["M1"]
    assert _conf(a, "O2") == {"level": "Medium", "reasons": ["open question: Q1 (starts at Medium)"]}
    assert _conf(a, "O1")["reasons"] == []                       # Q1 does not affect M2
    for word in ("method", "method_choice", "Method choice"):    # the model's real spelling is "method"
        a.clarification_questions[0].affects = [word]
        assert _conf(a, "O1")["reasons"] == _conf(a, "O2")["reasons"] == ["open question: Q1 (starts at Medium)"]


def test_confidence_rule1_ignores_a_question_below_the_top_three():
    words = ["one", "two", "three", "four"]
    questions = [{"id": f"Q{i}", "question": f"Question {w}?", "why_it_matters": "Decides it.",
                  "affects": ["status"]} for i, w in enumerate(words, 1)]
    a = _clean(clarification_questions=questions)
    a.clarification_questions[3].affects = ["M1"]
    assert _conf(a, "O2")["level"] == "High"
    a.clarification_questions[1].affects = ["M1"]
    a.clarification_questions[2].affects = ["method_choice"]
    assert _conf(a, "O2")["reasons"] == ["open question: Q2, Q3 (starts at Medium)"]


def test_confidence_rule2_no_verified_citation_and_precedent_only():
    a = _clean()
    a.solution_options[1].citations = []
    a.recommendations[0].citations = []
    assert _conf(a, "O2")["reasons"] == ["no verified source citation"]
    a.recommendations[0].citations = [cit_model("S01", 16, RAMAN_QUOTE, "application_precedent")]
    assert _conf(a, "O2")["reasons"] == ["precedent only"]


@pytest.mark.parametrize("doc,page", [("S02", 13), ("S01", 15), ("S01", 3)])
def test_confidence_rule2_general_citation_to_an_example_page_is_precedent(doc, page):
    tags = set(kb.page(doc, page)["scope"])
    assert not tags & {"method", "component_spec", "guidance"}
    a = _clean()
    a.solution_options[1].citations = []
    a.recommendations[0].citations = [cit_model(doc, page, "a quote from this page")]
    assert _conf(a, "O2")["reasons"] == ["precedent only"]


def test_confidence_rule2_general_citation_to_a_method_page_is_not_precedent():
    a = _clean()
    a.solution_options[1].citations = [cit_model("S02", 13, "a quote from this page")]
    assert set(kb.page("S01", 16)["scope"]) & {"method"}            # M1 keeps its S01 p.16 citation
    assert _conf(a, "O2")["level"] == "High"


def test_confidence_rule3_counts_only_required_parameters():
    """3.R3 item 7 (c): an optional auxiliary or not-measurable parameter does not downgrade."""
    a = _clean()
    a.parameters[1].citations = []
    a.parameters[1].necessity = "optional"
    assert _conf(a, "O2")["reasons"] == []
    a.parameters[1].necessity = "required"
    assert _conf(a, "O2")["reasons"] == ["uncited auxiliary sensor"]
    a.parameters[1].citations = [cit_model("S01", 16, RAMAN_QUOTE)]
    assert _conf(a, "O2")["reasons"] == []
    a.parameters[1].measured_by.type = "not_measurable_inline"
    assert _conf(a, "O2")["reasons"] == ["a parameter is not measurable in-line"]
    a.parameters[1].necessity = "optional"
    assert _conf(a, "O2")["reasons"] == []


def test_confidence_rule4_contradicted_premise_or_status():
    premise = {"premise": "Water blocks Raman.", "verdict": "contradicted", "explanation": "Low water absorbance.",
               "citations": [cit("S01", 16, RAMAN_QUOTE)]}
    a = _clean(decision_status="premise_not_supported", premise_checks=[premise])
    assert _conf(a, "O2")["reasons"] == ["a customer premise is contradicted, status: premise not supported"]
    b = _clean(decision_status="insufficient_information")
    assert _conf(b, "O2")["reasons"] == ["status: insufficient information"]


def test_confidence_rule5_multi_method():
    a = _clean(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    assert _conf(a, "O3") == {"level": "Medium", "reasons": ["multi-method, fusion benefit not yet shown"]}


def test_confidence_floor_is_low_and_all_reasons_are_kept():
    a = _assessment(decision_status="insufficient_information",
                    solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    for r in a.recommendations:
        r.citations = []
    a.parameters[1].necessity = "required"
    conf = _conf(a, "O3", {"physical_state": "liquid"})
    assert conf["level"] == "Low" and len(conf["reasons"]) == 6
    assert confidence_label(conf) == ("Low: open question: Q1 (starts at Medium); sample clarity unknown; "
                                      "no verified source citation; uncited auxiliary sensor; "
                                      "status: insufficient information; multi-method, fusion benefit not yet shown")


def test_confidence_is_rendered_and_in_the_json():
    a = with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    result, _ = run_with(assess=a)
    md = render.to_markdown(result)
    assert "| O3 | Extended (multi-method) | M1 Raman probe; M2 NIR, transmission/transflection probe | " \
           "Low: open question: Q1 (starts at Medium); multi-method, fusion benefit not yet shown | " \
           "high cost (rows 7, 12) |" in md
    assert CONFIDENCE_NOTE in md and "not a predicted accuracy" in CONFIDENCE_NOTE
    data = render.to_json(result)
    assert data["option_confidence"] == option_confidence(result.assessment, result.candidates, result.slots)
    assert data["option_confidence"]["O2"] == {"level": "High", "reasons": []}       # P2 is optional


# ----------------------------------------------------------------- 3.R2 item 3: Sources cell = rating pool
def _option_row(md: str, option_id: str) -> str:
    return next(line for line in md.splitlines() if line.startswith(f"| {option_id} |"))


def test_sources_cell_shows_the_recommendations_citations():
    md = render.to_markdown(run_with()[0])
    o1 = _option_row(md, "O1")                     # O1 has no own citation; its M2 cites S01 p.10
    assert "no verified source" not in o1 and o1.rstrip(" |").endswith("S01 p.10]")
    o2 = _option_row(md, "O2")                     # O2 and M1 cite the same quote: shown once
    assert o2.count("S01 p.16") == 1


def test_sources_cell_says_no_source_only_when_the_pool_is_empty():
    a = with_()
    a["recommendations"][1]["citations"] = []
    md = render.to_markdown(run_with(assess=a)[0])
    row = _option_row(md, "O1")
    assert "no verified source citation" in row and "no verified source: engineering judgement" in row


def test_option_citations_is_the_rating_pool():
    a = _clean()
    recs = {r.id: r for r in a.recommendations}
    pool = option_citations(a.solution_options[1], recs)
    assert [(c.doc, c.page) for c in pool] == [("S01", 16)]
    assert [(c.doc, c.page) for c in option_citations(a.solution_options[0], recs)] == [("S01", 10)]


# ----------------------------------------------------------------- 3.R2 N3: open checks, per-index confidence
def test_answer_warns_when_hard_checks_are_still_open():
    clean = render.to_markdown(run_with()[0])
    assert "still open; see Verification" not in clean
    a = with_()
    a["solution_options"][1]["id"] = "O1"
    a["proposal"]["best_current_option"] = "O1"
    result, _ = run_with(assess=a, repairs=[a, a])
    md = render.to_markdown(result)
    n = len(render.open_failures(result))
    assert n and md.split("\n## Answer\n\n", 1)[1].startswith(
        f"⚠ {n} verification check(s) still open; see Verification.\n")


def test_confidence_is_computed_per_option_row_even_with_repeated_ids():
    a = with_()
    a["solution_options"][1]["id"] = "O1"
    a["proposal"]["best_current_option"] = "O1"
    md = render.to_markdown(run_with(assess=a, repairs=[a, a])[0])
    rows = [line for line in md.splitlines() if line.startswith("| O1 |")]
    assert len(rows) == 2
    assert "Medium: open question: Q1 (starts at Medium) |" in rows[0] and "| High |" in rows[1]


def test_model_never_writes_the_confidence():
    assert "confidence" not in json.dumps(Assessment.model_json_schema()).lower()
    assert "never write one yourself" in pipeline.prompt("assess")


# ----------------------------------------------------------------- 4b max tokens
def test_assess_and_repair_have_room_for_reasoning():
    roles = config()["roles"]
    assert roles["assess"]["max_tokens"] >= 64000 and roles["repair"]["max_tokens"] >= 64000


@pytest.mark.parametrize("text", ["eur 500", "about 3000 usd", "EUR 5,000", "Priced in chf.", "500 Gbp each"])
def test_currency_codes_match_in_any_case(text):
    assert re.search(PRICE_PATTERN, text, re.IGNORECASE), text
    assert any(h.startswith("price") for h in forbidden_hits(text)), text


def test_journal_abbreviation_is_not_a_currency_code():
    pat = re.compile(PRICE_PATTERN, re.IGNORECASE)
    assert not pat.search("Eur. Urol. 2009, 56, 636-643")
    assert not pat.search("Eur.Urol.")
    hits = [(key, m.group()) for key, page in kb.pages().items()
            for m in re.finditer(r"\bEur\.\s?[A-Z]\w*", page["text"])]
    assert hits                                                       # the supplied pages carry one
    for key, abbreviation in hits:
        assert not pat.search(abbreviation), (key, abbreviation)


def test_cost_class_script_uses_the_same_currency_rule_and_skips_the_evidence_section(tmp_path):
    script = _load_script("check_cost_class")
    assert script.CURRENCY.search("about 3000 usd") and not script.CURRENCY.search("Eur. Urol.")
    result, _ = run_with()
    (tmp_path / "X.json").write_text(json.dumps(render.to_json(result)), encoding="utf-8")
    md = render.to_markdown(result)
    evidence = "\n### Evidence (verified quotes)\n\n"
    assert evidence in md
    (tmp_path / "X.md").write_text(md.replace(evidence, evidence + "1. ✓ quote \"Eur 5 here\"\n"), encoding="utf-8")
    assert script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1()) == []
    (tmp_path / "X.md").write_text(md.replace("\n### Verification\n", "\n### Verification\n\nAbout 5 eur.\n"),
                                   encoding="utf-8")
    assert any("currency" in p for p in script.check_pair(tmp_path / "X.json", tmp_path / "X.md", kb.table1()))


# ----------------------------------------------------------------- 3.R2 N4, N7
def test_request_label_says_our_summary_only_for_the_summary():
    md = render.to_markdown(run_with()[0])
    assert "**Customer request (our summary):** Follow ethanol" in md
    intake = copy.deepcopy(INTAKE)
    intake["summary"] = "Follow ethanol down to 3 g/L in a broth."
    md = render.to_markdown(run_with(intake=intake)[0])
    assert "**Customer request:** We want to follow ethanol" in md and "(our summary)" not in md


def test_answer_length_counts_the_rendered_request_line():
    intake = copy.deepcopy(INTAKE)
    intake["summary"] = "Follow ethanol down to 3 g/L in a broth."            # falls back to the enquiry
    long = with_()
    long["proposal"]["next_step"] = " ".join(["word"] * MAX_ANSWER_WORDS)  # fails, so the count is shown
    result, _ = run_with(intake=intake, assess=long)
    line = render.request_line(result)
    assert line == request_text(result.intake.summary, result.enquiry) and "3 g/L" not in line
    words = sum(len(t.split()) for t in answer_texts(result.assessment, line))
    check = soft(result, "answer_length")[0]
    assert check.message.startswith(f"{words} words")
    assert words > sum(len(t.split()) for t in answer_texts(result.assessment, result.intake.summary))


def test_layer_headings_are_h2_and_sections_h3():
    md = render.to_markdown(run_with()[0])
    assert re.findall(r"^## .+$", md, re.MULTILINE) == ["## Answer", "## Expert detail"]
    assert re.findall(r"^# .+$", md, re.MULTILINE) == ["# First technical assessment"]
    assert "\n### Solution options\n" in md and "\n### Verification\n" in md
