"""Phase 2 fixes 2.R2 (offline): bounded intake, verifier, finalize, LLM costing, provenance, render, CLI.

Same made-up generic enquiry and fixtures as test_phase2 (no dev or final scenario text).
"""

from __future__ import annotations

import copy
import json
from types import SimpleNamespace

import pytest
from dulwich import porcelain
from test_phase2 import (
    ASSESSMENT,
    ENQUIRY,
    INTAKE,
    PLAN_QUOTE,
    RAMAN_QUOTE,
    cit,
    failures,
    run_with,
    slot,
)

from afs_assistant import cli, kb, llm, paths, pipeline, provenance, render, scenarios
from afs_assistant.llm import (
    FakeClient,
    OpenRouterClient,
    SpendCapExceeded,
    SpendTracker,
)
from afs_assistant.methods import named_methods
from afs_assistant.schema import Intake
from afs_assistant.verify import SLOT_PATTERNS, forbidden_hits

BAD_QUOTE = "Raman always beats NIR for ethanol in every broth."
FUZZY_QUOTE = ("Raman is particularly well suited for aqueous environment, as it exhibits low absorbance "
               "for water molecules compared to infrared methods.")


def bad_quotes(n: int) -> dict:
    """ASSESSMENT with the first n citation-bearing items given an invented quote (1 hard failure each)."""
    a = copy.deepcopy(ASSESSMENT)
    targets = [a["recommendations"][0], a["recommendations"][1], a["measurement_concept"], a["spectral_ranges"][0]]
    for item in targets[:n]:
        item["citations"] = [cit("S01", 16, BAD_QUOTE)]
    return a


# ----------------------------------------------------------------- 1. intake: methods named in the enquiry (code)
def test_intake_schema_has_no_llm_filled_method_list():
    assert "proposed_methods" not in Intake.model_json_schema()["properties"]


@pytest.mark.parametrize("text, expected", [
    ("We want to compare MIR ATR and fluorescence information.", {"MIR": "MIR", "Fluorescence": "fluorescence"}),
    ("Could near-infrared or Raman follow the reaction?", {"NIR": "near-infrared", "Raman": "Raman"}),
    ("An FTIR lab method and UV/Vis absorbance are in use.", {"MIR": "FTIR", "UV-Vis": "UV/Vis"}),
    ("A fluorescent marker is added; NIRS is the alternative.", {"NIR": "NIRS", "Fluorescence": "fluorescent"}),
    ("Infrared spectroscopy of the mirror coating.", {}),
])
def test_named_methods_are_found_verbatim_by_word_list(text, expected):
    found = named_methods(text)
    assert found == expected
    assert all(q in text for q in found.values())


def test_named_methods_reach_the_assess_context_and_the_run_json():
    enquiry = ENQUIRY + " We are considering Raman or near-infrared."
    client = FakeClient({"intake": [INTAKE], "assess": [ASSESSMENT], "repair": [ASSESSMENT, ASSESSMENT]})
    result = pipeline.run(enquiry, client, run_id="test-run")
    assess_user = next(s["user"] for s in client.seen if s["role"] == "assess")
    assert '# METHODS NAMED IN THE ENQUIRY' in assess_user and 'NIR ("near-infrared"), Raman ("Raman")' in assess_user
    assert render.to_json(result)["named_methods"] == {"NIR": "near-infrared", "Raman": "Raman"}


def test_intake_prompt_defines_physical_state_values():
    text = (paths.ROOT / "prompts" / "intake.md").read_text(encoding="utf-8")
    for value in ("`liquid`", "`paste`", "`soft_solid`", "`powder`", "`solid`"):
        assert value in text
    assert "proposed_methods" not in text


def test_intake_prompt_has_no_enquiry_example_and_lists_stated_process_only():
    text = pipeline.prompt("intake")
    assert "processing line" not in text and '"exact"' not in text
    assert "list only the aspects the enquiry actually states" in text


# ----------------------------------------------------------------- 2. verify
@pytest.mark.parametrize("quote", ["", "   ", "a", "...", " a "])
def test_empty_or_short_enquiry_quote_is_rejected(quote):
    intake = copy.deepcopy(INTAKE)
    intake["facts_stated"].append({"text": "Something", "enquiry_quote": quote})
    intake["sample"]["heterogeneous"] = slot("no", "stated", quote)
    result, _ = run_with(intake=intake)
    assert len(result.intake.facts_stated) == 1
    assert result.intake.sample.heterogeneous.value == "unknown"


def test_short_but_real_enquiry_quote_is_kept():
    intake = copy.deepcopy(INTAKE)
    intake["facts_stated"].append({"text": "Lab reference exists", "enquiry_quote": "lab"})   # 3 chars: too short
    intake["facts_stated"].append({"text": "A pipe", "enquiry_quote": "pipe"})                # 4 chars: kept
    result, _ = run_with(intake=intake)
    assert [f.enquiry_quote for f in result.intake.facts_stated][1:] == ["pipe"]


@pytest.mark.parametrize("slot_name, text", [
    ("physical_state", "Please send more information on the required performance."),
    ("optical_regime", "It is unclear which reference method is used."),
    ("fluorophore", "We need the remarkable details."),
])
def test_slot_keywords_do_not_match_inside_other_words(slot_name, text):
    assert not SLOT_PATTERNS[slot_name].search(text)


@pytest.mark.parametrize("slot_name, text", [
    ("physical_state", "Is the sample a liquid or a paste?"),
    ("optical_regime", "Is the broth clear or turbid?"),
    ("fluorophore", "Does the target fluoresce?"),
])
def test_slot_keywords_match_whole_words(slot_name, text):
    assert SLOT_PATTERNS[slot_name].search(text)


def test_question_with_slot_word_inside_another_word_does_not_cover_the_slot():
    intake = copy.deepcopy(INTAKE)
    intake["sample"]["optical_regime"] = slot("unknown")
    a = copy.deepcopy(ASSESSMENT)
    a["clarification_questions"][0]["why_it_matters"] = "It is unclear which range matters."
    result, _ = run_with(intake=intake, assess=a, repairs=[a, a])
    assert failures(result, "unknown_slot_addressed")


@pytest.mark.parametrize("text", [
    "This is not a lab result, but NIR will work for this blend.",
    "Not tested yet; we guarantee the result.",
    "No pilot data. Raman will work here.",
    "Without a reference, the probe is ready for production use.",
])
def test_negation_in_another_clause_does_not_excuse_forbidden_wording(text):
    assert forbidden_hits(text)


@pytest.mark.parametrize("text", [
    "We cannot, at this stage, guarantee the result.",
    "We do not, and cannot, guarantee a detection limit.",
    "A 0.5 mm path does not guarantee a clear spectrum.",
])
def test_negation_with_an_aside_or_a_decimal_still_excuses_cautious_wording(text):
    assert not forbidden_hits(text)


@pytest.mark.parametrize("text", [
    "It is not cheap, however it will work.",
    "We did not test it, so it will work.",
])
def test_however_and_plain_commas_still_end_the_clause(text):
    assert forbidden_hits(text)


@pytest.mark.parametrize("field_name", ["requirements_stated", "key_unknowns", "not_in_sources"])
def test_numbers_in_uncited_lists_must_come_from_the_enquiry(field_name):
    a = copy.deepcopy(ASSESSMENT)
    a[field_name] = ["Response within 15 s over a 150 m fiber"]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert any(c.location == f"{field_name}[0]" for c in failures(result, "numbers_uncited_text"))


def test_rule_statement_used_as_quote_gets_the_source_quote_hint():
    rule = next(r for r in kb.rules() if r["id"] == "R-GEO-1")
    a = copy.deepcopy(ASSESSMENT)
    a["recommendations"][1]["citations"] = [cit("S01", 18, rule["statement"])]
    result, _ = run_with(assess=a, repairs=[a, a])
    msg = next(c.message for c in failures(result, "quote_verified") if c.location.startswith("recommendations[1]"))
    assert "R-GEO-1's paraphrase" in msg and rule["sources"][0]["quote"] in msg


def test_primary_with_combination_is_a_soft_warning():
    a = copy.deepcopy(ASSESSMENT)
    a["recommendations"][0]["combined_with"] = ["NIR"]
    result, _ = run_with(assess=a)
    assert result.report.passed
    assert any(c.name == "primary_single_method" for c in result.report.soft_failures)


# ----------------------------------------------------------------- 3. pipeline: knowledge block, finalize, repair
def test_knowledge_block_lists_rule_source_quotes_and_marks_paraphrase():
    block = pipeline.knowledge_block()
    rule = next(r for r in kb.rules() if r["id"] == "R-GEO-1")
    assert f"[R-GEO-1] ({rule['effect']}) paraphrase, never quote this: {rule['statement']}" in block
    src = rule["sources"][0]
    assert f'source [{kb.citation_label(src["doc"], src["page"])}]: "{src["quote"]}"' in block


def test_finalize_dedupes_keeping_the_highest_role():
    a = copy.deepcopy(ASSESSMENT)
    dup = copy.deepcopy(a["recommendations"][0])
    a["recommendations"][0]["role"] = "not_recommended"          # same Raman entry, first as not_recommended
    dup.update(id="M3", role="primary")
    a["recommendations"].append(dup)
    result, _ = run_with(assess=a, repairs=[a, a])
    recs = result.assessment.recommendations
    assert [(r.id, r.role) for r in recs] == [("M2", "comparison"), ("M3", "primary")]
    change = next(x for x in result.removed if x["location"] == "recommendations[0]")
    assert change["item"]["role"] == "not_recommended" and "duplicate" in change["reason"]


def test_finalize_forces_not_recommended_on_screen_fail_and_downgrades_status():
    intake = copy.deepcopy(INTAKE)
    intake["sample"]["fluorophore"] = slot("no", "stated", "ethanol")
    a = copy.deepcopy(ASSESSMENT)
    a["recommendations"] = [{"id": "M1", "method": "Fluorescence", "technique": "fluorescence_probe",
                             "role": "primary", "combined_with": [], "rationale": "Very sensitive.",
                             "conditions": "none", "citations": []}]
    result, _ = run_with(intake=intake, assess=a, repairs=[a, a])
    assert result.assessment.recommendations[0].role == "not_recommended"
    assert result.assessment.decision_status == "insufficient_information"
    reasons = " ".join(x["reason"] for x in result.removed)
    assert "failed screening" in reasons and "status_vs_recommendations failed" in reasons


def test_finalize_contradicted_premise_sets_premise_not_supported():
    a = copy.deepcopy(ASSESSMENT)
    a["premise_checks"] = [{"premise": "Fluorescence can measure ethanol directly", "verdict": "contradicted",
                            "explanation": "Fluorescence needs a fluorescent species.",
                            "citations": [cit("S01", 5, "However, most chemicals do not exhibit this property.")]}]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.decision_status == "premise_not_supported"


def test_finalize_supported_premise_without_citation_becomes_not_covered():
    a = copy.deepcopy(ASSESSMENT)
    a["premise_checks"] = [{"premise": "Raman suits aqueous samples", "verdict": "supported",
                            "explanation": "Water is a weak Raman scatterer.",
                            "citations": [cit("S01", 16, BAD_QUOTE)]}]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.premise_checks[0].verdict == "not_covered"
    assert any(x["location"] == "premise_checks[0]" and "not_covered" in x["reason"] for x in result.removed)


def test_finalize_unverified_contradiction_becomes_not_covered_and_keeps_status():
    a = copy.deepcopy(ASSESSMENT)
    a["premise_checks"] = [{"premise": "Fluorescence can measure ethanol directly", "verdict": "contradicted",
                            "explanation": "Fluorescence needs a fluorescent species.",
                            "citations": [cit("S01", 16, BAD_QUOTE)]}]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.premise_checks[0].verdict == "not_covered"
    assert result.assessment.decision_status == ASSESSMENT["decision_status"] == "provisional_assessment"
    assert not any(x["location"] == "decision_status" for x in result.removed)


def test_status_change_flags_the_reason_and_hides_the_corrected_failure():
    a = copy.deepcopy(ASSESSMENT)
    a["premise_checks"] = [{"premise": "Fluorescence can measure ethanol directly", "verdict": "contradicted",
                            "explanation": "Fluorescence needs a fluorescent species.",
                            "citations": [cit("S01", 5, "However, most chemicals do not exhibit this property.")]}]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert "status_reason" in result.flagged
    md = render.to_markdown(result)
    status_line = next(line for line in md.splitlines() if line.startswith("**Decision status:**"))
    assert "⚠ *(status changed by verification" in status_line
    assert "⚠ status_vs_premises" not in md and "still open: 0" in md


def test_screen_forced_not_recommended_is_flagged_and_not_listed_as_open():
    intake = copy.deepcopy(INTAKE)
    intake["sample"]["fluorophore"] = slot("no", "stated", "ethanol")
    a = copy.deepcopy(ASSESSMENT)
    a["recommendations"] = [{"id": "M1", "method": "Fluorescence", "technique": "fluorescence_probe",
                             "role": "primary", "combined_with": [], "rationale": "Very sensitive.",
                             "conditions": "none", "citations": []}]
    result, _ = run_with(intake=intake, assess=a, repairs=[a, a])
    assert "recommendations[0]" in result.flagged
    md = render.to_markdown(result)
    m1 = next(line for line in md.splitlines() if line.startswith("- **M1"))
    assert "⚠ *(failed screening" in m1
    assert "⚠ respects_screen" not in md and "⚠ status_vs_recommendations" not in md


def test_items_that_lost_a_citation_or_failed_a_number_check_are_flagged_inline():
    a = bad_quotes(1)
    a["recommendations"][1]["rationale"] = "NIR reaches 0.05% accuracy."
    result, _ = run_with(assess=a, repairs=[a, a])
    assert set(result.flagged) == {"recommendations[0]", "recommendations[1]"}
    md = render.to_markdown(result)
    m1 = next(line for line in md.splitlines() if line.startswith("- **M1"))
    m2 = next(line for line in md.splitlines() if line.startswith("- **M2"))
    assert "⚠ *(a citation failed verification" in m1 and "⚠ *(contains a figure" in m2


def test_fuzzy_quote_failure_gets_the_page_span_in_repair_only():
    a = copy.deepcopy(ASSESSMENT)
    a["recommendations"][0]["citations"] = [cit("S01", 16, FUZZY_QUOTE)]
    result, client = run_with(assess=a, repairs=[a, a])
    repair_user = next(s["user"] for s in client.seen if s["role"] == "repair")
    assert 'closest passage on that page: "' in repair_user and RAMAN_QUOTE[:40] in repair_user
    assert "closest passage" not in json.dumps(render.to_json(result), ensure_ascii=False)
    assert "closest passage" not in render.to_markdown(result)


def test_repair_keeps_the_round_with_fewest_hard_failures():
    result, _ = run_with(assess=bad_quotes(1), repairs=[bad_quotes(3), bad_quotes(2)])
    assert result.manifest["kept_round"] == 0 and len(result.report.hard_failures) == 1
    assert [r["hard_failures_after"] for r in result.repairs] == [3, 2]


def test_repair_tie_keeps_the_later_round():
    later = copy.deepcopy(ASSESSMENT)
    later["risks"][0]["citations"] = [cit("S01", 16, BAD_QUOTE)]           # 1 failure, other item
    result, _ = run_with(assess=bad_quotes(1), repairs=[later, bad_quotes(2)])
    assert result.manifest["kept_round"] == 1
    assert result.assessment.recommendations[0].citations             # round 1 kept M1's good quote


# ----------------------------------------------------------------- 4. llm: retries are costed, cap per attempt
def _response(content: str, finish: str = "stop", cost: float = 0.01, provider: str = "prov-a"):
    usage = SimpleNamespace(prompt_tokens=100, completion_tokens=50, prompt_tokens_details=None, cost=cost)
    return SimpleNamespace(id="r1", model="test/model", provider=provider, usage=usage,
                           choices=[SimpleNamespace(message=SimpleNamespace(content=content), finish_reason=finish)])


class _FakeOpenAI:
    def __init__(self, responses):
        self.responses, self.kwargs = list(responses), []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.kwargs.append(kwargs)
        return self.responses.pop(0)


def _client(responses, cap: float = 1e9) -> OpenRouterClient:
    client = OpenRouterClient.__new__(OpenRouterClient)      # no API key or .env needed
    client.client = _FakeOpenAI(responses)
    client.tracker = SpendTracker(cap, 1e9)
    return client


@pytest.mark.parametrize("first", [_response('{"a": 1', finish="length", cost=0.02),
                                   _response("{not json", cost=0.02), _response("", cost=0.02)])
def test_discarded_reply_is_retried_and_costed(first):
    client = _client([first, _response('{"a": 1}', cost=0.01)])
    result = client.complete_json("intake", "sys", "user", "intake", {"type": "object", "properties": {}})
    assert result.data == {"a": 1}
    assert [c["role"] for c in client.tracker.calls] == ["intake:discarded", "intake"]
    assert client.tracker.run_usd == pytest.approx(0.03)
    assert all(c["provider"] == "prov-a" and c["prompt_tokens"] == 100 for c in client.tracker.calls)


def test_spend_cap_is_checked_before_every_attempt():
    client = _client([_response("", finish="length", cost=0.02), _response('{"a": 1}')], cap=0.015)
    with pytest.raises(SpendCapExceeded):
        client.complete_json("intake", "sys", "user", "intake", {"type": "object", "properties": {}})
    assert len(client.client.kwargs) == 1 and client.tracker.calls[0]["role"] == "intake:discarded"


def test_provider_routing_config_is_passed_through():
    client = _client([_response('{"a": 1}')])
    client.complete_json("assess", "sys", "user", "assessment", {"type": "object", "properties": {}})
    cfg = llm.config()
    model = cfg["roles"]["assess"]["model"]
    sent = client.client.kwargs[0]
    assert sent["model"] == model and sent["max_tokens"] == cfg["roles"]["assess"]["max_tokens"]
    assert sent["extra_body"]["provider"] == {"require_parameters": True, **cfg["provider_routing"][model]}
    assert sent["response_format"]["json_schema"]["strict"] is True


# ----------------------------------------------------------------- 5. run JSON, provenance, run ids
def test_run_json_and_provenance_tree_hold_raw_rounds_calls_timings():
    intake = copy.deepcopy(INTAKE)
    intake["facts_stated"].append({"text": "invented", "enquiry_quote": "not in the enquiry"})
    a = bad_quotes(1)
    result, _ = run_with(intake=intake, assess=a, repairs=[ASSESSMENT])
    data = render.to_json(result)
    assert data["assessment_raw"]["recommendations"][0]["citations"][0]["quote"] == BAD_QUOTE
    assert data["repairs"][0]["assessment"] == data["assessment"]
    assert [c["role"] for c in data["calls"]] == ["intake", "assess", "repair"]
    assert data["intake_removed"][0]["item"]["enquiry_quote"] == "not in the enquiry"
    assert {"intake", "screen", "assess", "verify", "repair", "finalize", "wall"} <= set(data["timings_s"])
    assert data["manifest"]["timings_s"] == data["timings_s"]
    files = provenance.run_files(data, "md")
    assert {"assessment_raw.json", "repair_round_1.json", "calls.json", "intake_removed.json",
            "finalize.json"} <= set(files)


@pytest.mark.parametrize("scenario_id, stem_prefix", [("X01", "X01"), (None, "adhoc-")])
def test_run_id_is_unique_and_output_stem_is_the_scenario_id(tmp_path, monkeypatch, scenario_id, stem_prefix):
    recorded = []
    monkeypatch.setattr(provenance, "record", lambda run_id, files, msg: recorded.append(run_id) or "c0ffee")
    monkeypatch.setattr(provenance, "code_sha", lambda: "abc")
    monkeypatch.setattr(provenance, "code_dirty", lambda: True)
    client = FakeClient({"intake": [INTAKE], "assess": [ASSESSMENT]})
    out = cli._assess_one(ENQUIRY, scenario_id, client, tmp_path)
    assert out["run_id"].startswith(f"{scenario_id or 'adhoc'}-") and out["run_id"] != (scenario_id or "adhoc")
    assert recorded == [out["run_id"]]
    written = sorted(p.name for p in tmp_path.iterdir())
    stem = scenario_id or out["run_id"]
    assert written == [f"{stem}.json", f"{stem}.md"] and stem.startswith(stem_prefix)
    data = json.loads((tmp_path / f"{stem}.json").read_text(encoding="utf-8"))
    assert data["manifest"]["code_dirty"] is True and data["manifest"]["code_sha"] == "abc"


def test_code_dirty_flag(tmp_path):
    repo = porcelain.init(str(tmp_path))
    (tmp_path / "a.txt").write_text("one\n")
    porcelain.add(repo, [str(tmp_path / "a.txt")])
    porcelain.commit(repo, message=b"init", author=b"t <t@t>", committer=b"t <t@t>")
    assert provenance.code_dirty(tmp_path) is False
    (tmp_path / "untracked.txt").write_text("x\n")
    assert provenance.code_dirty(tmp_path) is False                  # untracked files do not count
    (tmp_path / "a.txt").write_text("two\n")
    assert provenance.code_dirty(tmp_path) is True


# ----------------------------------------------------------------- 6. render
def test_precedent_only_citation_has_its_own_badge():
    a = copy.deepcopy(ASSESSMENT)
    a["feasibility_plan"]["steps"][0]["citations"] = [cit("REF", 3, PLAN_QUOTE, "method_gain")]
    result, _ = run_with(assess=a)
    md = render.to_markdown(result)
    assert '✓ (precedent only) **REF §3** (method gain)' in md
    assert '✓ **S01 p.16** (general)' in md


def test_premise_text_ending_in_a_period_has_no_double_period():
    a = copy.deepcopy(ASSESSMENT)
    a["premise_checks"] = [{"premise": "Raman suits aqueous samples.", "verdict": "supported",
                            "explanation": "Water is a weak Raman scatterer.",
                            "citations": [cit("S01", 16, RAMAN_QUOTE)]}]
    result, _ = run_with(assess=a)
    md = render.to_markdown(result)
    assert "Raman suits aqueous samples. Water is" in md and ".." not in md


def test_assess_prompt_states_caps_and_single_method_primary():
    text = pipeline.prompt("assess")
    for phrase in ("`combined_with` must be empty for role `primary`", "at most 4 risks", "at most 5 steps",
                   "`key_unknowns`: at most 6", "No generic boilerplate"):
        assert phrase in text


# ----------------------------------------------------------------- 7. CLI set run and scenario parser
def test_run_set_continues_after_a_failing_scenario_and_exits_nonzero(monkeypatch, capsys):
    class StubClient:
        def __init__(self):
            self.tracker = SpendTracker(1e9, 1e9)

    items = [{"id": "X01", "title": "a", "enquiry": "first"}, {"id": "X02", "title": "b", "enquiry": "second"}]
    seen = []

    def fake_assess_one(enquiry, scenario_id, client, out_dir, title):
        seen.append(scenario_id)
        if scenario_id == "X01":
            raise RuntimeError("LLM call failed after retries")
        return {"summary": {"passed": True}, "cost_usd": 0.0}

    monkeypatch.setattr(llm, "OpenRouterClient", StubClient)
    monkeypatch.setattr(scenarios, "load", lambda name: items)
    monkeypatch.setattr(cli, "_assess_one", fake_assess_one)
    assert cli.main(["run", "--set", "dev"]) == 1
    assert seen == ["X01", "X02"]
    out = capsys.readouterr().out
    assert "X01: FAILED RuntimeError" in out and "X02: verification" in out and "failed: ['X01']" in out


def test_final_set_needs_the_explicit_flag(monkeypatch):
    monkeypatch.setattr(llm, "OpenRouterClient", lambda: pytest.fail("must not create a client"))
    assert cli.main(["run", "--set", "final"]) == 2


def test_scenario_parsers_split_on_headings(tmp_path, monkeypatch):
    blocks = ["Contents", "1. Development scenarios | page 2", "1. Development scenarios",
              "X01 · First title", "Enquiry one text.", "Facts stated a, b", "Useful sources S01 p.5",
              "X02 · Second title", "Enquiry two text.", "2. Worked examples", "X01 · First title", "Answer."]
    section = scenarios._section(blocks, "1. Development scenarios", "2. Worked examples")
    items = scenarios._split_by_heading(section)
    assert [(i, t, b[0]) for i, t, b in items] == [("X01", "First title", "Enquiry one text."),
                                                   ("X02", "Second title", "Enquiry two text.")]
    (tmp_path / scenarios.FINAL_NAME).write_text(
        "Header line\nZ11 | Alpha case\n=====\nLine one\nline two\n\nZ12 | Beta case\nOnly line\n", encoding="utf-8")
    monkeypatch.setattr(paths, "MATERIALS", tmp_path)
    assert scenarios.load_final() == [{"id": "Z11", "title": "Alpha case", "enquiry": "Line one line two"},
                                      {"id": "Z12", "title": "Beta case", "enquiry": "Only line"}]
