"""Phase 5.1/5.2 offline tests: the eval checklist, the must/must_not predicates, missing outputs,
the summary files, the CLI and the adversarial scenario file.

No network and no LLM calls: synthetic runs from the FakeClient pipeline (made-up generic
enquiries), mutated per test. Case ids here are synthetic (X..); no dev or final scenario text.
"""

from __future__ import annotations

import copy
import json
import re
import typing

import pytest
from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE, cit
from test_phase5_early import _off_topic_run

from afs_assistant import cli, evaluate, kb_check, paths, pipeline, render
from afs_assistant.evaluate import FAIL, NA, NOT_RUN, PASS
from afs_assistant.llm import FakeClient
from afs_assistant.schema import Assessment, Intake, MeasuredBy, PremiseCheck, Technique

PLAN_QUOTE = ("Representative samples or process states, independent reference measurements, what is compared, "
              "and the basis for the go / no-go decision.")


def _assessment(**changes) -> dict:
    a = copy.deepcopy(ASSESSMENT)
    a["feasibility_plan"]["steps"].append(
        {"step": "Compare both probes on the same samples.", "purpose": "Choose the method on real data.",
         "citations": [cit("REF", 3, PLAN_QUOTE)]})
    a.update(changes)
    return a


def _write(tmp_path, data: dict, md: str, sid: str = "X01"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    jp, mp = tmp_path / f"{sid}.json", tmp_path / f"{sid}.md"
    jp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    mp.write_text(md, encoding="utf-8")
    return evaluate.Run(data, md, jp, mp)


def _produced(intake=INTAKE, assess=None, enquiry=ENQUIRY):
    client = FakeClient({"intake": [intake], "assess": [assess or _assessment()], "repair": []})
    result = pipeline.run(enquiry, client, run_id="eval-test")
    return render.to_json(result), render.to_markdown(result, "Synthetic")


@pytest.fixture
def base():
    return _produced()


def _run(tmp_path, base, data_change=None, md_change=None):
    data, md = copy.deepcopy(base[0]), base[1]
    if data_change:
        data_change(data)
    if md_change:
        md = md_change(md)
    return _write(tmp_path, data, md)


# ----------------------------------------------------------------- the clean run
def test_clean_run_passes_every_applicable_item(tmp_path, base):
    _write(tmp_path, *base)
    case = evaluate.evaluate_case({"id": "X01", "title": "t"}, tmp_path)
    results = {k: v["result"] for k, v in case["checklist"].items()}
    assert case["status"] == "evaluated"
    assert {k for k, r in results.items() if r == NA} == {
        "premise_flags", "external_secondary", "external_replay", "off_topic_handled", "mermaid_renders"}
    assert all(r == PASS for k, r in results.items() if r != NA), case["checklist"]
    assert len(evaluate.CHECKLIST) >= 15
    assert {crit for _, crit, _, _ in evaluate.CHECKLIST} == set(evaluate.CRITERIA)


# ----------------------------------------------------------------- one failing case per item
def _a(data):
    return data["assessment"]


FAILS = {
    "structured_output": {"data_change": lambda d: d.pop("still_open")},
    "sections_present": {"md_change": lambda m: m.replace("### Spectral range", "### Spectra")},
    "citations_verified": {"data_change": lambda d: d["verification"]["summary"].update(citations_verified=0)},
    "no_open_failures": {"data_change": lambda d: d["still_open"].append(
        {"name": "option_count", "location": "solution_options", "message": "1 option"})},
    "no_flagged_figures": {"data_change": lambda d: d["flagged"].update(brief_answer="unsupported figure: 5 %")},
    "no_currency": {"md_change": lambda m: m.replace("### Brief answer\n", "### Brief answer\n\nAbout 900 EUR. ")},
    "no_certainty_wording": {"data_change": lambda d: _a(d).update(brief_answer="This will definitely work.")},
    "cost_class_table1": {"data_change": lambda d: d["option_costs"]["O2"].update(cost_class="low")},
    "options_rules": {"data_change": lambda d: _a(d)["solution_options"][0].update(tier="recommended")},
    "proposal_rules": {"data_change": lambda d: _a(d)["proposal"].update(best_current_option="O9")},
    "feasibility_plan": {"data_change": lambda d: _a(d)["feasibility_plan"].update(decision_basis="n/a")},
    "questions_present": {"md_change": lambda m: m.replace("### Key questions\n\n1. ", "### Key questions\n\n- ")},
    "questions_tied_to_options": {"data_change": lambda d: _a(d)["clarification_questions"][0].update(
        affects=["budget"])},
    "answer_length": {"data_change": lambda d: _a(d).update(brief_answer="word " * 700)},
}


@pytest.mark.parametrize("item", sorted(FAILS))
def test_each_item_fails_on_its_defect(tmp_path, base, item):
    run = _run(tmp_path, base, **FAILS[item])
    fn = next(f for i, _, _, f in evaluate.CHECKLIST if i == item)
    result, reason = fn(run)
    assert result == FAIL and reason


def test_schema_mismatch_fails_structured_output(tmp_path, base):
    run = _run(tmp_path, base, data_change=lambda d: _a(d).update(decision_status="certain"))
    assert evaluate.structured_output(run)[0] == FAIL and run.a is None


def test_currency_inside_quoted_evidence_is_allowed(tmp_path, base):
    run = _run(tmp_path, base, md_change=lambda m: m.replace(
        "### Evidence (verified quotes)\n", "### Evidence (verified quotes)\n\n1. ✓ \"cost 5 EUR\"\n"))
    assert evaluate.no_currency(run)[0] == PASS


def test_currency_in_the_quoted_enquiry_is_allowed(tmp_path):
    data, md = _produced(enquiry=ENQUIRY + " Our budget is 900 EUR.")
    assert "> " + data["enquiry"] in md and "900 EUR" in md
    run = _write(tmp_path, data, md)
    assert evaluate.no_currency(run)[0] == PASS
    model_text = _write(tmp_path, data, md.replace("### Brief answer\n", "### Brief answer\n\nAbout 900 EUR. "))
    assert evaluate.no_currency(model_text)[0] == FAIL


def test_extended_option_needs_fusion_note(tmp_path, base):
    def change(d):
        _a(d)["recommendations"][1]["role"] = "comparison"
        _a(d)["solution_options"].append({**_a(d)["solution_options"][0], "id": "O3", "tier": "extended",
                                          "recommendation_ids": ["M1", "M2"], "fusion_note": None})
    result, reason = evaluate.options_rules(_run(tmp_path, base, data_change=change))
    assert result == FAIL and "fusion note" in reason


def test_question_affecting_only_installation_does_not_tie_to_options(tmp_path, base):
    run = _run(tmp_path, base, data_change=lambda d: _a(d)["clarification_questions"][0].update(
        affects=["installation"]))
    result, reason = evaluate.questions_tied_to_options(run)
    assert result == FAIL and "no top question" in reason


def test_no_questions_with_open_unknowns_fails(tmp_path, base):
    run = _run(tmp_path, base, data_change=lambda d: _a(d).update(clarification_questions=[]))
    assert evaluate.questions_present(run)[0] == FAIL
    assert evaluate.questions_tied_to_options(run)[0] == NA


# ----------------------------------------------------------------- premise flags
def test_premise_flags_pass_fail_and_na(tmp_path, base):
    assert evaluate.premise_flags(_run(tmp_path, base))[0] == NA
    routed = _run(tmp_path, base, data_change=lambda d: d["intake"]["routes"].append("premise_to_check"))
    assert evaluate.premise_flags(routed)[0] == FAIL
    check = {"premise": "Raman works here", "verdict": "contradicted", "explanation": "x", "citations": []}
    contradicted = _run(tmp_path, base, data_change=lambda d: (d["intake"]["routes"].append("premise_to_check"),
                                                               _a(d)["premise_checks"].append(check)))
    result, reason = evaluate.premise_flags(contradicted)
    assert result == FAIL and "provisional" in reason
    ok = _run(tmp_path, base, data_change=lambda d: (d["intake"]["routes"].append("premise_to_check"),
                                                     _a(d)["premise_checks"].append({**check, "verdict": "not_covered"})))
    assert evaluate.premise_flags(ok)[0] == PASS


# ----------------------------------------------------------------- external evidence
EXT_QUOTE = "Raman spectroscopy was used to monitor ethanol in fermentation."


def _with_external(data, label="E01 ¶3", url="https://example.org/paper", gap_kind="multi_method"):
    data["external"] = {
        "gaps": [{"id": "G1", "kind": gap_kind, "text": "gap"}],
        "items": [{"gap_id": "G1", "option_id": "O2", "finding": "f", "how_it_applies": "h",
                   "limits_and_transfer_risks": "l", "quote_status": "exact", "paragraph_sha256": "x", "notes": [],
                   "citation": {"source_id": "E01", "para": 3, "cited_para": 3, "quote": EXT_QUOTE, "label": label,
                                "url": url, "doi": None}}],
        "dropped": [], "sources": [{"id": "E01", "access": "full_text", "url": url}],
        "proposal_support": [], "gap_results": []}


def _ext_md(md, label="E01 ¶3"):
    section = (f"### {evaluate.EXTERNAL_TITLE}\n\n**G1 · multi-method:** gap\n\n- **{label}** f\n"
               f"  > \"{EXT_QUOTE}\"\n\n")
    return md.replace("### Evidence (verified quotes)\n", section + "### Evidence (verified quotes)\n")


def test_external_secondary_pass_and_fail(tmp_path, base):
    ok = _run(tmp_path, base, data_change=_with_external, md_change=_ext_md)
    assert evaluate.external_secondary(ok)[0] == PASS
    no_section = _run(tmp_path, base, data_change=_with_external)
    assert evaluate.external_secondary(no_section)[0] == FAIL
    no_url = _run(tmp_path, base, data_change=lambda d: _with_external(d, url=None), md_change=_ext_md)
    result, reason = evaluate.external_secondary(no_url)
    assert result == FAIL and "URL" in reason
    mixed = _run(tmp_path, base, data_change=_with_external, md_change=lambda m: _ext_md(m).replace(
        "### Evidence (verified quotes)\n", "### Evidence (verified quotes)\n\n1. ✓ **E01 ¶3** mixed in\n"))
    assert evaluate.external_secondary(mixed)[0] == FAIL


def test_external_support_from_a_sensor_gap_fails_the_proposal(tmp_path, base):
    def change(d):
        _with_external(d, gap_kind="auxiliary_sensor")
        d["external"]["proposal_support"] = ["E01 ¶3"]
    result, reason = evaluate.proposal_rules(_run(tmp_path, base, data_change=change))
    assert result == FAIL and "auxiliary_sensor" in reason
    def method_gap(d):
        _with_external(d)
        d["external"]["proposal_support"] = ["E01 ¶3"]
    assert evaluate.proposal_rules(_run(tmp_path, base, data_change=method_gap))[0] == PASS


@pytest.mark.parametrize("rows, expected", [
    ([{"item": "kept G1 E01 ¶3", "recorded": "kept", "replayed": "kept", "equal": True}], PASS),
    ([{"item": "kept G1 E01 ¶3", "recorded": "kept", "replayed": "dropped: x", "equal": False}], FAIL),
    ([{"item": "kept G1 E01 ¶3", "recorded": "kept", "replayed": evaluate.CACHE_MISSING, "equal": False}], NA),
    ([{"item": "kept G1 E01 ¶3", "recorded": "kept", "replayed": "kept", "equal": True},
      {"item": "kept G1 E02 ¶1", "recorded": "kept", "replayed": evaluate.CACHE_MISSING, "equal": False}], PASS),
    ([{"item": "kept G1 E01 ¶3", "recorded": "kept", "replayed": "dropped: x", "equal": False},
      {"item": "kept G1 E02 ¶1", "recorded": "kept", "replayed": evaluate.CACHE_MISSING, "equal": False}], FAIL),
])
def test_external_replay_states(tmp_path, base, monkeypatch, rows, expected):
    from afs_assistant.external import step

    monkeypatch.setattr(step, "replay", lambda block, cache_root=None: rows)
    run = _run(tmp_path, base, data_change=_with_external, md_change=_ext_md)
    result, reason = evaluate.external_replay(run)
    assert result == expected
    if any(r["replayed"] == evaluate.CACHE_MISSING for r in rows):
        assert "not in the local cache" in reason      # items without cached text are reported
    assert evaluate.external_replay(_run(tmp_path, base))[0] == NA        # no external block


# ----------------------------------------------------------------- off-topic and mermaid
def test_off_topic_run_handled_and_other_items_not_applicable(tmp_path):
    result, _ = _off_topic_run()
    data, md = render.to_json(result), render.to_markdown(result)
    _write(tmp_path, data, md)
    case = evaluate.evaluate_case({"id": "X01"}, tmp_path)
    c = {k: v["result"] for k, v in case["checklist"].items()}
    assert c["off_topic_handled"] == PASS and c["structured_output"] == PASS and c["no_currency"] == PASS
    assert {k for k, r in c.items() if r == PASS} == {"off_topic_handled", "structured_output", "no_currency"}
    broken = _write(tmp_path, data, md.replace(pipeline.OFF_TOPIC_MESSAGE, ""))
    assert evaluate.off_topic_handled(broken)[0] == FAIL


def test_mermaid_item_is_optional(tmp_path, base):
    assert evaluate.mermaid_renders(_run(tmp_path, base))[0] == NA


# ----------------------------------------------------------------- must / must_not
def test_predicates_on_an_assessed_run(tmp_path, base):
    run = _run(tmp_path, base)
    holds = lambda spec: evaluate.predicate(run, spec)[0]
    assert holds({"check": "off_topic", "value": False}) and not holds({"check": "off_topic", "value": True})
    assert holds({"check": "status_in", "values": ["provisional_assessment"]})
    assert holds({"check": "route_in", "values": ["needs_clarification"]})
    assert holds({"check": "max_questions", "n": 3}) and not holds({"check": "min_questions", "n": 2})
    assert holds({"check": "mentions", "fields": ["questions"], "pattern": r"concentration range"})
    assert not holds({"check": "mentions", "fields": ["risks"], "pattern": r"viscos"})
    assert holds({"check": "parameter", "name": "temperat", "types": ["auxiliary_sensor"]})
    assert not holds({"check": "parameter", "name": "temperat", "types": ["spectroscopy"]})
    assert holds({"check": "option_technique_in", "values": ["raman_probe"]})
    assert holds({"check": "primary_technique_in", "values": ["raman_probe"]})
    assert not holds({"check": "extended_fusion"}) and not holds({"check": "primary_fused"})
    assert not holds({"check": "forbidden_wording"}) and not holds({"check": "currency"})
    assert not holds({"check": "premise_verdict_in", "values": ["contradicted"]})
    assert holds({"check": "any_of", "items": [{"check": "status_in", "values": ["x"]},
                                                {"check": "assessment_present"}]})
    with pytest.raises(ValueError):
        evaluate.predicate(run, {"check": "nonsense"})


def test_extended_fusion_and_fused_primary_predicates(tmp_path, base):
    def change(d):
        _a(d)["recommendations"][0]["combined_with"] = ["NIR"]
        _a(d)["solution_options"].append({**_a(d)["solution_options"][0], "id": "O3", "tier": "extended",
                                          "recommendation_ids": ["M1", "M2"],
                                          "fusion_note": "Same spot; must beat the best single method."})
    run = _run(tmp_path, base, data_change=change)
    assert evaluate.predicate(run, {"check": "extended_fusion"})[0]
    assert evaluate.predicate(run, {"check": "primary_fused"})[0]


def test_must_and_must_not_results(tmp_path, base):
    run = _run(tmp_path, base)
    scenario = {"must": [{"check": "status_in", "values": ["insufficient_information"], "why": "w"}],
                "must_not": [{"check": "parameter", "name": "temperat", "types": ["auxiliary_sensor"]},
                             {"check": "currency"}]}
    items = evaluate.scenario_items(run, scenario)
    assert [(x["kind"], x["result"]) for x in items] == [("must", FAIL), ("must_not", FAIL), ("must_not", PASS)]
    assert "provisional_assessment" in items[0]["reason"] and items[0]["why"] == "w"


def test_assessment_predicates_are_false_on_an_off_topic_run(tmp_path):
    result, _ = _off_topic_run()
    run = _write(tmp_path, render.to_json(result), render.to_markdown(result))
    assert evaluate.predicate(run, {"check": "off_topic"})[0]
    assert not evaluate.predicate(run, {"check": "assessment_present"})[0]
    holds, found = evaluate.predicate(run, {"check": "status_in", "values": ["insufficient_information"]})
    assert not holds and "off-topic" in found


# ----------------------------------------------------------------- missing outputs, summary, CLI
def test_missing_and_unreadable_outputs_are_reported_not_raised(tmp_path, base):
    _write(tmp_path, *base, sid="X01")
    (tmp_path / "X03.json").write_text("{not json", encoding="utf-8")
    (tmp_path / "X03.md").write_text("# x", encoding="utf-8")
    (tmp_path / "X04.json").write_text("{}", encoding="utf-8")            # Markdown missing
    items = [{"id": "X01", "title": "a"}, {"id": "X02", "title": "b", "must": [{"check": "off_topic"}]},
             {"id": "X03", "title": "c"}, {"id": "X04", "title": "d"}]
    res = evaluate.evaluate_set("synthetic", tmp_path, items=items)
    status = {c["id"]: c["status"] for c in res["cases"]}
    assert status == {"X01": "evaluated", "X02": NOT_RUN, "X03": "error", "X04": NOT_RUN}
    x02 = res["cases"][1]
    assert all(v["result"] == NOT_RUN for v in x02["checklist"].values())
    assert x02["scenario_items"][0]["result"] == NOT_RUN and "X02.json" in x02["reason"]
    assert res["totals"]["not_run"] == 2 and res["totals"]["scenario_items"]["must"]["not_run"] == 1


def test_summary_files_merge_sets_and_list_fail_reasons(tmp_path, base):
    out = tmp_path / "eval"
    _run(tmp_path / "a", base, data_change=lambda d: d["flagged"].update(brief_answer="unsupported figure"))
    first = evaluate.evaluate_set("dev", tmp_path / "a", items=[{"id": "X01", "title": "a"}])
    evaluate.write_summary({"dev": first}, out)
    second = evaluate.evaluate_set("adversarial", tmp_path / "b", items=[{"id": "X02", "title": "b"}])
    summary = evaluate.write_summary({"adversarial": second}, out)
    assert set(summary["sets"]) == {"dev", "adversarial"}
    md = (out / "summary.md").read_text(encoding="utf-8")
    assert "## Set: dev" in md and "## Set: adversarial" in md
    assert "| no_flagged_figures | **FAIL** |" in md
    assert "- X01 · no_flagged_figures: flagged brief_answer: unsupported figure" in md
    assert "not run" in md
    assert json.loads((out / "summary.json").read_text(encoding="utf-8"))["items"][0]["id"] == "structured_output"


def test_cli_eval_exit_codes(tmp_path, base, monkeypatch):
    run_dir, out = tmp_path / "runs", tmp_path / "eval"
    _write(run_dir, *base)
    monkeypatch.setattr(paths, "SCENARIOS", tmp_path)
    (tmp_path / "adversarial.jsonl").write_text(
        json.dumps({"id": "X01", "title": "t", "enquiry": "e", "must": [],
                    "must_not": [{"check": "assessment_present"}]}) + "\n", encoding="utf-8")
    assert cli.main(["eval", "--set", "adversarial", "--outputs", str(run_dir), "--out", str(out)]) == 1
    (tmp_path / "adversarial.jsonl").write_text(
        json.dumps({"id": "X01", "title": "t", "enquiry": "e", "must": [{"check": "assessment_present"}],
                    "must_not": []}) + "\n", encoding="utf-8")
    assert cli.main(["eval", "--set", "adversarial", "--outputs", str(run_dir), "--out", str(out)]) == 0
    assert cli.main(["eval", "--outputs", str(run_dir), "--out", str(out)]) == 2      # --outputs needs --set
    assert (out / "summary.md").exists()


# ----------------------------------------------------------------- the adversarial set
def _adversarial():
    with (paths.SCENARIOS / "adversarial.jsonl").open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def test_adversarial_file_format_and_coverage(tmp_path, base):
    items = _adversarial()
    ids = [s["id"] for s in items]
    assert len(items) == 12 and len(set(ids)) == 12 and all(re.fullmatch(r"A\d{2}", i) for i in ids)
    for s in items:
        assert s["enquiry"].strip() and s["title"].strip() and s["covers"].strip()
        assert s["must"] and s["must_not"]
        assert not kb_check.CASE_ID.search(json.dumps(s))
    covers = " | ".join(s["covers"] for s in items)
    for topic in ("soil", "dissolution", "MIR link", "viable cells", "non-optical", "vague", "over-questioned",
                  "guarantee", "clinical", "viscosity + temperature", "fusion", "off-topic"):
        assert topic in covers
    # Every predicate is known and evaluates on an assessed and on an off-topic run without error.
    run = _run(tmp_path, base)
    result, _ = _off_topic_run()
    off = _write(tmp_path / "off", render.to_json(result), render.to_markdown(result))
    for s in items:
        for r in (run, off):
            rows = evaluate.scenario_items(r, s)
            assert all(x["result"] in (PASS, FAIL) and "check error" not in x["found"] for x in rows), rows
    off_case = next(s for s in items if "off-topic" in s["covers"])
    assert all(x["result"] == PASS for x in evaluate.scenario_items(off, off_case))


def test_adversarial_set_is_runnable_by_the_cli():
    parser_sets = re.search(r'"--set", choices=\[([^\]]*)\], required=True',
                            (paths.ROOT / "src" / "afs_assistant" / "cli.py").read_text(encoding="utf-8"))
    assert parser_sets and '"adversarial"' in parser_sets.group(1)


# ----------------------------------------------------------------- review fixes (5.2)
def _literals(annotation) -> set[str]:
    """Every string of the Literal(s) inside an annotation (list[Literal[...]], Literal[...] | None, ...)."""
    if typing.get_origin(annotation) is typing.Literal:
        return {a for a in typing.get_args(annotation) if isinstance(a, str)}
    return set().union(*(_literals(a) for a in typing.get_args(annotation)), set())


ENUMS = {
    "status_in": _literals(Assessment.model_fields["decision_status"].annotation),
    "route_in": _literals(Intake.model_fields["routes"].annotation),
    "premise_verdict_in": _literals(PremiseCheck.model_fields["verdict"].annotation),
    "option_technique_in": _literals(Technique),
    "primary_technique_in": _literals(Technique),
}


def _specs(specs):
    for spec in specs:
        yield spec
        yield from _specs(spec.get("items", []))


def test_adversarial_predicate_values_are_schema_members():
    """A typo in an enum value would make a must_not pass silently: every value is a schema member."""
    assert all(ENUMS.values()) and _literals(MeasuredBy.model_fields["type"].annotation)
    checked = 0
    for s in _adversarial():
        for spec in _specs(s["must"] + s["must_not"]):
            if spec["check"] in ENUMS:
                assert spec["values"] and set(spec["values"]) <= ENUMS[spec["check"]], (s["id"], spec)
                checked += 1
            if spec["check"] == "parameter" and "types" in spec:
                assert set(spec["types"]) <= _literals(MeasuredBy.model_fields["type"].annotation), (s["id"], spec)
                checked += 1
            if spec["check"] == "mentions":
                assert set(spec["fields"]) <= set(evaluate.TEXT_FIELDS), (s["id"], spec)
    assert checked >= 10


def test_a_raising_predicate_fails_only_its_own_item(tmp_path, base):
    run = _run(tmp_path, base)
    scenario = {"must": [{"check": "assessment_present"}, {"check": "nonsense"},
                         {"check": "mentions", "fields": ["no_such_field"], "pattern": "x"}],
                "must_not": [{"check": "currency"}, {"check": "status_in"}]}       # status_in lacks "values"
    items = evaluate.scenario_items(run, scenario)
    assert [(x["kind"], x["result"]) for x in items] == [
        ("must", PASS), ("must", FAIL), ("must", FAIL), ("must_not", PASS), ("must_not", FAIL)]
    assert all("check error" in items[i]["reason"] for i in (1, 2, 4))


def test_unreadable_and_off_schema_runs_fail_every_scenario_item(tmp_path, base):
    scenario = {"id": "X01", "must": [{"check": "off_topic", "value": False}],
                "must_not": [{"check": "assessment_present"}, {"check": "currency"}]}
    (tmp_path / "X01.json").write_text("{not json", encoding="utf-8")
    (tmp_path / "X01.md").write_text("# x", encoding="utf-8")
    bad = evaluate.evaluate_case(scenario, tmp_path)
    assert bad["status"] == "error" and len(bad["scenario_items"]) == 3
    assert all(x["result"] == FAIL and "unreadable" in x["reason"] for x in bad["scenario_items"])
    _run(tmp_path, base, data_change=lambda d: _a(d).update(decision_status="certain"))
    off_schema = evaluate.evaluate_case(scenario, tmp_path)
    assert off_schema["status"] == "error" and "schema" in off_schema["reason"]
    assert [x["result"] for x in off_schema["scenario_items"]] == [FAIL, FAIL, FAIL]
    assert off_schema["checklist"]["structured_output"]["result"] == FAIL


def _cli_set(tmp_path, monkeypatch, cases):
    monkeypatch.setattr(paths, "SCENARIOS", tmp_path)
    (tmp_path / "adversarial.jsonl").write_text("".join(
        json.dumps({"id": sid, "title": "t", "enquiry": "e", "must": [{"check": "assessment_present"}],
                    "must_not": []}) + "\n" for sid in cases), encoding="utf-8")


def test_cli_eval_fails_on_not_run_or_unreadable_cases(tmp_path, base, monkeypatch):
    run_dir, out = tmp_path / "runs", tmp_path / "eval"
    _write(run_dir, *base, sid="X01")
    args = ["eval", "--set", "adversarial", "--outputs", str(run_dir), "--out", str(out)]
    _cli_set(tmp_path, monkeypatch, ["X01", "X02"])                 # X02 has no output
    assert cli.main(args) == 1
    assert cli.main([*args, "--allow-incomplete"]) == 0
    (run_dir / "X02.json").write_text("{not json", encoding="utf-8")
    (run_dir / "X02.md").write_text("# x", encoding="utf-8")
    assert cli.main(args) == 1
    assert cli.main([*args, "--allow-incomplete"]) == 0
    _cli_set(tmp_path, monkeypatch, ["X01"])
    assert cli.main(args) == 0


def _adversarial_case(covers: str) -> dict:
    return next(s for s in _adversarial() if covers in s["covers"])


def test_question_text_ignores_why_it_matters(tmp_path, base):
    case = _adversarial_case("over-questioned")
    spec = case["must_not"][0]
    assert spec["fields"] == ["question_text"]
    run = _run(tmp_path, base, data_change=lambda d: _a(d)["clarification_questions"][0].update(
        question="Where along the pipe can the probe be installed?",
        why_it_matters="The sampling point must match the reference method."))
    assert not evaluate.predicate(run, spec)[0]
    assert evaluate.predicate(run, {**spec, "fields": ["questions"]})[0]        # why_it_matters is in "questions"
    rows = evaluate.scenario_items(run, {"must_not": [spec]})
    assert rows[0]["result"] == PASS
    asks = _run(tmp_path, base, data_change=lambda d: _a(d)["clarification_questions"][0].update(
        question="Which reference method do you use?"))
    assert evaluate.predicate(asks, spec)[0]


def test_first_question_and_premise_pattern_predicates(tmp_path, base):
    def two_questions(d):
        first = {**_a(d)["clarification_questions"][0], "id": "Q0", "question": "Where is the pipe installed?"}
        _a(d)["clarification_questions"].insert(0, first)
    run = _run(tmp_path, base, data_change=two_questions)
    spec = {"check": "mentions", "fields": ["first_question"], "pattern": "concentration"}
    assert not evaluate.predicate(run, spec)[0]
    assert evaluate.predicate(run, {**spec, "fields": ["question_text"]})[0]
    check = {"premise": "A long fiber link works", "verdict": "not_covered", "explanation": "x", "citations": []}
    premised = _run(tmp_path, base, data_change=lambda d: _a(d)["premise_checks"].append(check))
    pv = {"check": "premise_verdict_in", "values": ["not_covered"]}
    assert evaluate.predicate(premised, {**pv, "pattern": "fib(?:er|re)"})[0]
    assert not evaluate.predicate(premised, {**pv, "pattern": "viscos"})[0]
