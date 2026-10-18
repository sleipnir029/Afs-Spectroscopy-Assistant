"""D-061 offline tests: the proposal names the recommended option; the `variable` optical regime.

Same made-up generic enquiry and fixtures as test_phase2 (no dev, adversarial or final scenario text).
"""

from __future__ import annotations

import copy

import pytest
from test_phase2 import ASSESSMENT, run_with

from afs_assistant import kb, render, screen
from afs_assistant.options import _unknown_phrases
from afs_assistant.schema import Assessment, RegimeSlot
from afs_assistant.verify import (
    PROPOSAL_CHANGED_FLAG,
    RECHECK_NAMES,
    TEXT_FOR_OTHER_OPTION_FLAG,
    TIER_SWAPPED_FLAG,
    Report,
    check_options,
    recheck,
)


def proposing(option_id: str) -> dict:
    a = copy.deepcopy(ASSESSMENT)
    a["proposal"]["best_current_option"] = option_id
    return a


def hard(report_or_result, name: str) -> list:
    report = getattr(report_or_result, "report", report_or_result)
    return [c for c in report.hard_failures if c.name == name]


def options_report(a: dict) -> Report:
    report = Report()
    check_options(Assessment.model_validate(a), [], report)
    return report


# ----------------------------------------------------------------- proposal_is_recommended
def test_proposal_on_the_recommended_option_passes():
    assert not hard(options_report(proposing("O2")), "proposal_is_recommended")
    assert "proposal_is_recommended" in RECHECK_NAMES


def soft(report_or_result, name: str) -> list:
    report = getattr(report_or_result, "report", report_or_result)
    return [c for c in report.soft_failures if c.name == name]


def test_proposal_on_another_option_is_a_soft_failure():
    report = options_report(proposing("O1"))
    failed = soft(report, "proposal_is_recommended")
    assert failed and failed[0].location == "proposal.best_current_option"
    assert not hard(report, "proposal_is_recommended")             # no repair round on its own (D-061a)


def test_proposal_check_leaves_a_missing_option_and_no_recommended_tier_to_other_checks():
    report = options_report(proposing("O9"))
    assert hard(report, "proposal_option_exists") and not soft(report, "proposal_is_recommended")
    a = proposing("O1")
    a["solution_options"][1]["tier"] = "extended"
    report = options_report(a)
    assert hard(report, "option_recommended_tier") and not soft(report, "proposal_is_recommended")


def test_a_proposed_simple_option_takes_the_recommended_tier():
    result, client = run_with(assess=proposing("O1"))
    assert not any(s["role"] == "repair" for s in client.seen)     # the soft check alone starts no repair
    final = result.assessment
    assert final.proposal.best_current_option == "O1"               # the brief answer argues for it
    assert {o.id: o.tier for o in final.solution_options} == {"O1": "recommended", "O2": "simple"}
    change = next(x for x in result.removed if x.get("corrects") == "proposal_is_recommended")
    assert change["location"] == "solution_options[0].tier" and change["item"] == "simple"
    assert result.flagged["solution_options[0]"] == result.flagged["solution_options[1]"] == TIER_SWAPPED_FLAG
    assert result.manifest["finalize_fallbacks"] == ["proposal_is_recommended"]
    assert not soft(recheck(final, result.candidates), "proposal_is_recommended")
    payload = render.to_json(result)
    assert any(x.get("corrects") == "proposal_is_recommended" for x in payload["finalize_changes"])


def test_a_proposed_extended_option_moves_the_proposal_and_flags_the_text():
    a = proposing("O1")
    a["solution_options"][0]["tier"] = "extended"
    a["solution_options"][0]["fusion_note"] = "Fusion is a later hypothesis to test against the best single method."
    result, _ = run_with(assess=a, repairs=[a, a])              # an extended option may need repairs of its own
    final = result.assessment
    assert final.proposal.best_current_option == "O2"
    assert {o.id: o.tier for o in final.solution_options}["O1"] == "extended"
    assert result.flagged["proposal"] == PROPOSAL_CHANGED_FLAG
    assert result.flagged["brief_answer"] == result.flagged["proposal.next_step"] == TEXT_FOR_OTHER_OPTION_FLAG


# ----------------------------------------------------------------- optical regime `variable`
def test_regime_slot_accepts_variable():
    assert RegimeSlot.model_validate({"value": "variable", "basis": "stated", "enquiry_quote": "x"}).value == "variable"
    screen.validate_slots({"optical_regime": "variable"})
    assert screen.REGIME_SAMPLE_TYPES["variable"] == (screen.REGIME_SAMPLE_TYPES["clear"]
                                                      | screen.REGIME_SAMPLE_TYPES["turbid"]
                                                      | screen.REGIME_SAMPLE_TYPES["opaque"])


@pytest.mark.parametrize(("expected", "state"), [
    (["clear", "turbid", "opaque"], "yes"),  # holds for every state
    ("clear", "maybe"),                     # holds for one state only
    (["turbid", "opaque"], "maybe"),
    (["opaque_absorbing"], "no"),           # holds for none
])
def test_when_state_checks_a_variable_regime_as_each_state(expected, state):
    cand = screen.Candidate("NIR", "diffuse_reflection", [], True, set())
    slots = {"optical_regime": "variable"}
    assert screen._when_state({"optical_regime": expected}, cand, slots) == state
    # Another failing condition still decides 'no'.
    assert screen._when_state({"method": "MIR", "optical_regime": expected}, cand, slots) == "no"


def _by_key(cands):
    return {(c.method, c.technique): c for c in cands}


def test_variable_liquid_keeps_transmission_and_diffuse_reflection():
    variable = _by_key(screen.screen({"physical_state": "liquid", "optical_regime": "variable"}))
    clear = _by_key(screen.screen({"physical_state": "liquid", "optical_regime": "clear"}))
    assert clear[("NIR", "diffuse_reflection")].status == "fail"          # the single-state verdict
    for key in (("NIR", "transmission_transflection"), ("NIR", "diffuse_reflection"),
                ("UV-Vis", "transmission_transflection")):
        assert variable[key].status in ("pass", "unknown"), key


def test_exclude_rule_for_one_state_gives_unknown_for_a_variable_sample(monkeypatch):
    rule = {"id": "R-TEST-1", "statement": "Transmission fails for this state.", "effect": "exclude",
            "when": {"optical_regime": "turbid"}, "target": {"technique": "transmission"}, "sources": []}
    rules = [*kb.rules(), rule]
    monkeypatch.setattr(kb, "rules", lambda: rules)
    slots = {"physical_state": "liquid", "optical_regime": "variable"}
    uv = _by_key(screen.screen(slots))[("UV-Vis", "transmission_transflection")]
    assert uv.status == "unknown"
    assert any(r["rule"] == "R-TEST-1" and r["status"] == "unknown" for r in uv.reasons)
    assert "sample clarity varies" in _unknown_phrases(uv, slots)
    turbid = _by_key(screen.screen({**slots, "optical_regime": "turbid"}))
    assert turbid[("UV-Vis", "transmission_transflection")].status == "fail"


def test_variable_liquid_keeps_transmission_preferred_and_the_reflection_caveat():
    by = {(c.method, c.technique): c for c in screen.screen({"physical_state": "liquid", "optical_regime": "variable"})}
    assert by[("NIR", "transmission_transflection")].status == "pass"          # S01 p.18: preferred for clear
    reflection = by[("NIR", "diffuse_reflection")]
    assert reflection.status == "pass" and "R-GEO-4" in reflection.warnings    # the clear-liquid caveat stays
    clear = {(c.method, c.technique): c for c in screen.screen({"physical_state": "liquid", "optical_regime": "clear"})}
    assert clear[("NIR", "diffuse_reflection")].status == "fail"
