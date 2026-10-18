"""Phase 5 step 4 offline tests (D-050): Phase 3 carry-overs 1 (stated-by-the-customer quotes),
5 (expert-layer clutter) and 6 (test gaps).

Same made-up generic enquiry and fixtures as test_phase2 (no dev, adversarial or final scenario text).
"""

from __future__ import annotations

import copy
import json

from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE, run_with
from test_phase3 import EXTENDED, with_
from test_phase3_r import _clean, _conf
from test_phase3_r3 import _client, _collapsed_intake

from afs_assistant import pipeline, render
from afs_assistant.schema import Assessment, Intake
from afs_assistant.ui import diagrams

FACT_LONG = "clear aqueous fermentation broth that flows through a pipe"
FACT_REF = "Gas chromatography results from the lab are available as reference."


def _stated_block(intake: dict) -> str:
    """The 'Stated by the customer' list of a run whose assessment states no requirement."""
    result = run_with(assess=with_(requirements_stated=[]))[0]
    result.intake = Intake.model_validate(intake)
    md = render.to_markdown(result)
    return md.split("**Stated by the customer**\n\n", 1)[1].split("\n\n", 1)[0]


def _intake(facts: list[str], targets: list[str]) -> dict:
    intake = copy.deepcopy(INTAKE)
    intake["facts_stated"] = [{"text": "fact", "enquiry_quote": q} for q in facts]
    intake["targets"] = [{"variable": "ethanol", "purpose": "follow", "enquiry_quote": q} for q in targets]
    return intake


# ----------------------------------------------------------------- 1. stated by the customer
def test_stated_fallback_drops_a_quote_contained_in_another_ignoring_case():
    block = _stated_block(_intake(["Fermentation broth", "clear aqueous fermentation broth", "CLEAR aqueous"],
                                  ["follow ethanol", "ethanol"]))
    assert block == '- "clear aqueous fermentation broth"\n- "follow ethanol"'


def test_stated_fallback_keeps_the_first_of_two_quotes_equal_but_for_case():
    block = _stated_block(_intake(["Clear aqueous fermentation broth", "clear aqueous fermentation broth"],
                                  ["follow ethanol"]))
    assert block == '- "Clear aqueous fermentation broth"\n- "follow ethanol"'


def test_stated_fallback_is_capped_when_it_covers_most_of_the_enquiry():
    assert len(FACT_LONG) + len(FACT_REF) + len("follow ethanol") > render.STATED_MAX_SHARE * len(ENQUIRY)
    block = _stated_block(_intake([FACT_LONG, FACT_REF], ["follow ethanol"]))
    # The target first, then the facts while they fit in half the enquiry; shown in the original order.
    assert block == (f'- "{FACT_LONG}"\n- "follow ethanol"\n'
                     "- *Further statements: see the customer enquiry above.*")


def test_capped_fallback_keeps_at_least_one_quote():
    long_target = "We want to follow ethanol in a clear aqueous fermentation broth that flows through a pipe."
    block = _stated_block(_intake([FACT_REF], [long_target]))
    assert block == f'- "{long_target}"\n- *Further statements: see the customer enquiry above.*'


def test_stated_fallback_under_the_cap_has_no_note():
    block = _stated_block(_intake(["clear aqueous fermentation broth"], ["follow ethanol"]))
    assert "Further statements" not in block


# ----------------------------------------------------------------- 5. expert-layer clutter
def test_spectral_range_of_a_method_in_no_option_is_not_shown():
    ranges = ASSESSMENT["spectral_ranges"] + [{"method": "MIR", "statement": "Nominal MIR range.", "citations": []}]
    md = render.to_markdown(run_with(assess=with_(spectral_ranges=ranges))[0])
    section = md.split("### Spectral range\n\n", 1)[1].split("\n\n", 1)[0]
    assert "**NIR:**" in section and "**Raman:**" in section and "MIR" not in section


def test_without_options_every_spectral_range_is_shown():
    ranges = ASSESSMENT["spectral_ranges"] + [{"method": "MIR", "statement": "Nominal MIR range.", "citations": []}]
    a = Assessment.model_validate(with_(spectral_ranges=ranges, solution_options=[]))
    assert [s.method for _, s in render.shown_spectral_ranges(a)] == ["NIR", "Raman", "MIR"]


def _combined(rationale: str, conditions: str) -> dict:
    a = with_(solution_options=ASSESSMENT["solution_options"] + [{**EXTENDED, "recommendation_ids": ["M1"]}])
    a["recommendations"][0].update(combined_with=["NIR"], rationale=rationale, conditions=conditions)
    return a


def _m1_line(assess: dict) -> str:
    result = run_with()[0]
    result.assessment = Assessment.model_validate(assess)     # rendered as given (no repair round)
    md = render.to_markdown(result)
    return next(x for x in md.split("\n") if x.startswith("- **M1 · "))


def test_later_hypothesis_tail_is_added_when_the_model_text_does_not_say_it():
    assert _m1_line(_combined("Water interferes little with Raman.", "none")).endswith(
        " Later hypothesis, after single-method tests.")


def test_later_hypothesis_tail_is_not_repeated_after_the_model_says_it():
    for rationale, conditions in [("Water interferes little with Raman.", "Only after the single-method tests."),
                                  ("A fused model is a later hypothesis.", "none"),
                                  ("Any gain must beat the best single method.", "none")]:
        assert "Later hypothesis, after single-method tests." not in _m1_line(_combined(rationale, conditions))


def test_sketch_label_borrows_the_technique_of_the_combined_method():
    a = Assessment.model_validate(_combined("Water interferes little with Raman.", "none"))
    extended = a.solution_options[-1]
    chart = render.mermaid_chart(a, extended, {})
    assert '"NIR, transmission/transflection probe"' in chart and "technique not specified" not in chart
    labels = [lane["label"] for lane in diagrams.option_nodes(a, extended, {})["lanes"]]
    assert labels == ["Raman probe", "NIR, transmission/transflection probe"]


def test_sketch_label_without_any_entry_for_the_combined_method_stays_unspecified():
    a = _combined("Water interferes little with Raman.", "none")
    a["recommendations"][0]["combined_with"] = ["MIR"]
    a = Assessment.model_validate(a)
    assert '"MIR (technique not specified)"' in render.mermaid_chart(a, a.solution_options[-1], {})


# ----------------------------------------------------------------- 6. test gaps
def test_open_question_and_two_weaknesses_stay_at_the_low_floor():
    a = _clean(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    a.clarification_questions[0].affects = ["method"]
    conf = _conf(a, "O3", {"physical_state": "liquid"})          # clarity unknown: NIR transmission open
    assert conf["level"] == "Low"
    assert conf["reasons"][0] == "open question: Q1 (starts at Medium)"
    assert "sample clarity unknown" in conf["reasons"]
    assert "multi-method, fusion benefit not yet shown" in conf["reasons"]
    assert len(conf["reasons"]) >= 3                              # Medium start + 2 weaknesses, floor Low


def test_intake_problems_reach_the_json_and_the_markdown_end_to_end():
    result = pipeline.run(ENQUIRY, _client([_collapsed_intake(), _collapsed_intake()]), run_id="t")
    data = json.loads(json.dumps(render.to_json(result)))
    problems = data["manifest"]["intake_problems"]
    assert problems and data["manifest"]["intake_attempts"] == 2
    verification = render.to_markdown(result).split("### Verification\n", 1)[1]
    for p in problems:
        assert f"- ⚠ Intake incomplete after 2 attempt(s): {p}\n" in verification


def test_intake_recovered_on_the_retry_leaves_no_warning():
    result = pipeline.run(ENQUIRY, _client([_collapsed_intake(), INTAKE]), run_id="t")
    assert render.to_json(result)["manifest"]["intake_problems"] == []
    assert "Intake incomplete" not in render.to_markdown(result)
