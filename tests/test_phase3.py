"""Phase 3 offline tests: brief answer, proposal, parameters, solution options, cost class,
auxiliary label, Mermaid sketch, and the cheap open points (3.7).

Same made-up generic enquiry and fixtures as test_phase2 (no dev or final scenario text).
"""

from __future__ import annotations

import copy
import importlib.util
import re

import pytest
from dulwich import porcelain
from test_phase2 import (
    ASSESSMENT,
    INTAKE,
    NIR_QUOTE,
    RAMAN_QUOTE,
    cit,
    failures,
    run_with,
    slot,
)

from afs_assistant import kb, paths, pipeline, provenance, quotes, render
from afs_assistant.options import NOT_RATED, cost_class, method_label, option_costs
from afs_assistant.schema import Assessment, Intake
from afs_assistant.screen import screen
from afs_assistant.verify import Report, check_options, sanitize_intake

EXTENDED = {"id": "O3", "tier": "extended", "recommendation_ids": ["M1", "M2"], "parameter_ids": ["P1", "P2"],
            "ease_of_use": "Two probes at one port", "maintenance": "Two calibrations to keep",
            "performance_fit": "Only if one method is not enough", "cost_drivers": "Two spectrometers",
            "fusion_note": "Same spot, synchronised acquisition, one model per method first; must beat the best "
                           "single method.", "citations": []}


def with_(**changes) -> dict:
    a = copy.deepcopy(ASSESSMENT)
    a.update(copy.deepcopy(changes))
    return a


def hard(result, name: str) -> list:
    return failures(result, name)


def soft(result, name: str) -> list:
    return [c for c in result.report.soft_failures if c.name == name]


def still_open(result) -> set[str]:
    return {c.name for c in render.open_failures(result)}


# ----------------------------------------------------------------- 3.1 schema
def test_clean_fixture_passes_every_phase3_check():
    result, _ = run_with()
    names = {c.name for c in result.report.checks}
    for name in ("brief_answer_present", "proposal_present", "proposal_option_exists", "option_count",
                 "option_tiers_distinct", "option_recommended_tier", "option_recommendation_refs", "option_screen",
                 "parameter_method_in_option", "single_primary", "status_needs_contradiction"):
        assert name in names
    assert result.report.passed and not result.report.soft_failures and not result.recheck


def test_precedent_only_is_a_premise_verdict_and_needs_a_citation():
    premise = {"premise": "A published application shows it works.", "verdict": "precedent_only",
               "explanation": "A similar application is shown.", "citations": []}
    result, _ = run_with(assess=with_(premise_checks=[premise]))
    assert result.assessment.premise_checks[0].verdict == "not_covered"
    assert any("precedent_only" in x["reason"] for x in result.removed)


def test_optional_notes_are_nullable_and_rendered_when_given():
    result, _ = run_with(assess=with_(chemometrics_note="Build one calibration per method first."))
    md = render.to_markdown(result)
    assert "## Further notes" in md and "**Chemometrics:** Build one calibration" in md
    assert "Real-time tracking" not in md
    assert "## Further notes" not in render.to_markdown(run_with()[0])


# ----------------------------------------------------------------- 3.3 hard checks (fail fixtures)
@pytest.mark.parametrize("field,value", [("brief_answer", "  ")])
def test_empty_brief_answer_is_a_hard_failure(field, value):
    result, _ = run_with(assess=with_(**{field: value}), repairs=[with_(**{field: value})] * 2)
    assert hard(result, "brief_answer_present")


def test_empty_proposal_field_and_unknown_option_are_hard_failures():
    a = with_()
    a["proposal"]["next_step"] = ""
    a["proposal"]["best_current_option"] = "O9"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "proposal_present") and hard(result, "proposal_option_exists")
    assert {"proposal_present", "proposal_option_exists"} <= still_open(result)


@pytest.mark.parametrize("n", [1, 4])
def test_option_count_outside_two_to_three_is_a_hard_failure(n):
    options = copy.deepcopy(ASSESSMENT["solution_options"])
    while len(options) < n:
        extra = copy.deepcopy(options[0])
        extra["id"] = f"O{len(options) + 1}"
        options.append(extra)
    a = with_(solution_options=options[:n])
    if n == 1:
        a["solution_options"][0]["tier"] = "recommended"
        a["proposal"]["best_current_option"] = "O1"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "option_count")


def test_repeated_tier_and_missing_recommended_tier_are_hard_failures():
    a = with_()
    a["solution_options"][1]["tier"] = "simple"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "option_tiers_distinct") and hard(result, "option_recommended_tier")


def test_option_referencing_a_missing_or_not_recommended_entry_is_a_hard_failure():
    a = with_()
    a["recommendations"].append({"id": "M3", "method": "MIR", "technique": "ATR", "role": "not_recommended",
                                 "combined_with": [], "rationale": "Not needed here.", "conditions": "none",
                                 "citations": []})
    a["solution_options"][0]["recommendation_ids"] = ["M2", "M3", "M7"]
    result, _ = run_with(assess=a, repairs=[a, a])
    fail = hard(result, "option_recommendation_refs")
    assert fail and "M3" in fail[0].message and "M7" in fail[0].message
    # finalize drops the bad references and logs them; the check is no longer open
    assert result.assessment.solution_options[0].recommendation_ids == ["M2"]
    assert "option_recommendation_refs" not in still_open(result)
    assert sum("recommendation_ids" in x["location"] for x in result.removed) == 2


def test_option_using_a_screen_failed_candidate_is_a_hard_failure():
    a = with_()
    a["recommendations"].append({"id": "M3", "method": "NIR", "technique": "diffuse_reflection",
                                 "role": "conditional", "combined_with": [], "rationale": "Reflection.",
                                 "conditions": "if turbid", "citations": []})
    a["solution_options"][0]["recommendation_ids"] = ["M3"]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "option_screen")
    # finalize: M3 becomes not_recommended, the reference is dropped, the empty option is dropped and logged,
    # and the option count (now 1) stays visibly open.
    assert [o.id for o in result.assessment.solution_options] == ["O2"]
    assert any(x["location"] == "solution_options[0]" and "dropped" in x["reason"] for x in result.removed)
    assert "option_count" in still_open(result) and "option_screen" not in still_open(result)


def test_combined_method_that_fails_everywhere_fails_the_option_screen():
    a = Assessment.model_validate(with_())
    a.recommendations[1].combined_with = ["Fluorescence"]
    slots = {"physical_state": "liquid", "optical_regime": "clear", "fluorophore": "no"}
    report = Report()
    check_options(a, screen(slots), report)
    assert not next(c for c in report.checks if c.name == "option_screen").passed
    report = Report()
    check_options(a, screen({"physical_state": "liquid", "optical_regime": "clear"}), report)  # unknown: open
    assert all(c.passed for c in report.checks if c.name == "option_screen")


def test_extended_option_needs_a_fusion_note_and_two_methods():
    ok, _ = run_with(assess=with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))
    assert ok.report.passed and not soft(ok, "extended_multi_method")
    bad = copy.deepcopy(EXTENDED)
    bad["fusion_note"] = None
    bad["recommendation_ids"] = ["M1"]
    a = with_(solution_options=ASSESSMENT["solution_options"] + [bad])
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "extended_fusion_note") and soft(result, "extended_multi_method")


@pytest.mark.parametrize("method", ["MIR", None])
def test_spectroscopy_parameter_method_must_appear_in_an_option(method):
    a = with_()
    a["parameters"][0]["measured_by"]["method"] = method
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "parameter_method_in_option")


def test_parameter_method_from_a_combination_counts():
    a = with_()
    a["recommendations"][1]["combined_with"] = ["MIR"]
    a["recommendations"][1]["role"] = "conditional"
    a["parameters"][0]["measured_by"]["method"] = "MIR"
    result, _ = run_with(assess=a)
    assert not hard(result, "parameter_method_in_option")


@pytest.mark.parametrize("roles", [("primary", "primary"), ("comparison", "conditional")])
def test_exactly_one_primary_is_a_hard_check(roles):
    a = with_()
    for rec, role in zip(a["recommendations"], roles, strict=True):
        rec["role"] = role
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "single_primary") and "single_primary" in still_open(result)


# ----------------------------------------------------------------- 3.3 new text through existing checks
def test_new_text_fields_go_through_the_forbidden_lexicon():
    a = with_(brief_answer="The Raman probe will work for this broth.")
    a["proposal"]["next_step"] = "Order the set for €500 and start."
    a["solution_options"][0]["cost_drivers"] = "About 2000 EUR for the probe."
    result, _ = run_with(assess=a, repairs=[a, a])
    message = hard(result, "forbidden_wording")[0].message
    assert "certainty" in message and message.count("price") == 2


def test_new_text_fields_go_through_the_claim_local_number_checks():
    a = with_(brief_answer="Raman reaches 5 ppm ethanol in this broth.", future_direction="A 300 m link later.")
    a["solution_options"][1]["performance_fit"] = "Error below 0.2 percent"          # not in its RAMAN_QUOTE
    a["parameters"][0]["why"] = "Needed down to 3 g/L."
    result, _ = run_with(assess=a, repairs=[a, a])
    loose = {c.location for c in hard(result, "numbers_uncited_text")}
    local = {c.location for c in hard(result, "numbers_claim_local")}
    assert {"brief_answer", "future_direction"} <= loose
    assert {"solution_options[1]", "parameters[0]"} <= local
    assert {"brief_answer", "solution_options[1]", "parameters[0]"} <= set(result.flagged)


def test_option_number_supported_by_its_own_quote_passes():
    a = with_()
    a["solution_options"][0]["performance_fit"] = "NIR spectra span 780-2500 nm"
    a["solution_options"][0]["citations"] = [cit("S01", 10, NIR_QUOTE)]
    result, _ = run_with(assess=a)
    assert not hard(result, "numbers_claim_local")


def test_parameter_and_option_quotes_are_verified_and_failing_ones_removed():
    a = with_()
    a["parameters"][0]["citations"] = [cit("S01", 16, "Raman measures ethanol in every broth.")]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert any(c.location == "parameters[0].citations[0]" for c in hard(result, "quote_verified"))
    assert result.assessment.parameters[0].citations == [] and "parameters[0]" in result.flagged


# ----------------------------------------------------------------- 3.3 soft checks
def test_long_brief_answer_and_many_premises_are_soft_warnings():
    premise = {"premise": "Raman suits water.", "verdict": "supported", "explanation": "Low water absorbance.",
               "citations": [cit("S01", 16, RAMAN_QUOTE)]}
    result, _ = run_with(assess=with_(brief_answer=" ".join(["word"] * 81), premise_checks=[premise] * 4))
    assert soft(result, "brief_answer_length") and soft(result, "premise_count") and result.report.passed


# ----------------------------------------------------------------- 3.7 premise reverse check
def test_premise_not_supported_needs_a_contradicted_premise():
    premise = {"premise": "Any method will do.", "verdict": "not_covered", "explanation": "Not addressed.",
               "citations": []}
    a = with_(decision_status="premise_not_supported", premise_checks=[premise])
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "status_needs_contradiction") and "status_needs_contradiction" in still_open(result)
    assert result.assessment.decision_status == "premise_not_supported"        # judgement: not auto-changed


def test_premise_not_supported_with_a_verified_contradiction_passes():
    premise = {"premise": "Water blocks Raman.", "verdict": "contradicted", "explanation": "Low water absorbance.",
               "citations": [cit("S01", 16, RAMAN_QUOTE)]}
    result, _ = run_with(assess=with_(decision_status="premise_not_supported", premise_checks=[premise]))
    assert not hard(result, "status_needs_contradiction")


# ----------------------------------------------------------------- finalize and options
def test_reference_to_a_deduplicated_entry_is_remapped_to_the_kept_one():
    a = with_()
    dup = copy.deepcopy(a["recommendations"][0])
    dup.update(id="M3", role="comparison")
    a["recommendations"].append(dup)
    a["solution_options"][1]["recommendation_ids"] = ["M3"]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert result.assessment.solution_options[1].recommendation_ids == ["M1"]
    assert any("now M1" in x["reason"] for x in result.removed)


def test_proposal_pointing_to_a_dropped_option_is_flagged_and_open():
    a = with_()
    a["recommendations"].append({"id": "M3", "method": "NIR", "technique": "diffuse_reflection", "role": "comparison",
                                 "combined_with": [], "rationale": "Reflection.", "conditions": "none",
                                 "citations": []})
    a["solution_options"][1]["recommendation_ids"] = ["M3"]
    a["recommendations"][0]["role"] = "comparison"
    a["recommendations"][1]["role"] = "primary"
    a["parameters"][0]["measured_by"]["method"] = "NIR"
    result, _ = run_with(assess=a, repairs=[a, a])
    assert [o.id for o in result.assessment.solution_options] == ["O1"]
    assert "proposal" in result.flagged
    assert {"proposal_option_exists", "option_count", "option_recommended_tier"} <= still_open(result)
    assert "**Best current option:** (invalid option id)" in render.to_markdown(result)


# ----------------------------------------------------------------- 3.2 cost class
def _recs(a: Assessment) -> dict:
    return {r.id: r for r in a.recommendations}


def test_cost_class_comes_from_table1_rows():
    a = Assessment.model_validate(with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))
    costs = option_costs(a)
    assert (costs["O1"]["cost_class"], [r["row"] for r in costs["O1"]["rows"]]) == ("average", [7])
    assert (costs["O2"]["cost_class"], [r["row"] for r in costs["O2"]["rows"]]) == ("high", [12])
    assert costs["O3"]["cost_class"] == "high" and [r["row"] for r in costs["O3"]["rows"]] == [7, 12]
    assert costs["O3"]["label"] == "high (rows 7, 12)" and costs["O3"]["citation"] == "S01 Table 1 (p.6)"
    table = {r["row"]: r["cost"] for r in kb.table1()}
    for c in costs.values():
        assert all(table[r["row"]] == r["cost"] for r in c["rows"])


def test_unrated_parts_are_never_guessed():
    a = Assessment.model_validate(with_())
    a.recommendations[1].technique = "to_be_determined"
    a.recommendations[0].combined_with = ["Fluorescence"]
    o2 = cost_class(a.solution_options[1], _recs(a))
    assert o2.cost_class == "high" and o2.unrated == ["Fluorescence (technique not specified)"]
    assert o2.label() == f"high (row 12); {NOT_RATED}: Fluorescence (technique not specified)"
    o1 = cost_class(a.solution_options[0], _recs(a))
    assert o1.cost_class is None and o1.label() == NOT_RATED


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, paths.ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_cost_class_cross_check_script(tmp_path):
    import json

    result, _ = run_with(assess=with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))
    (tmp_path / "X.json").write_text(json.dumps(render.to_json(result)), encoding="utf-8")
    md = render.to_markdown(result)
    (tmp_path / "X.md").write_text(md, encoding="utf-8")
    script = _load_script("check_cost_class")
    table = kb.table1()
    assert script.check_pair(tmp_path / "X.json", tmp_path / "X.md", table) == []
    (tmp_path / "X.md").write_text(md.replace("| average (row 7) |", "| low (row 7) |"), encoding="utf-8")
    assert script.check_pair(tmp_path / "X.json", tmp_path / "X.md", table)


# test_cost_never_shows_currency is replaced by the currency fail-fixtures in test_phase3_r.py (3.R B3).


# ----------------------------------------------------------------- 3.2 auxiliary label, not measurable in-line
def test_auxiliary_sensor_label_always_stays_and_says_cited_when_verified():
    result, _ = run_with()
    md = render.to_markdown(result)
    assert "Auxiliary sensor: temperature sensor in the line (engineering judgement: confirm availability with AFS)" in md
    a = with_()
    a["parameters"][1]["citations"] = [cit("S01", 16, RAMAN_QUOTE)]
    md = render.to_markdown(run_with(assess=a)[0])
    assert "Auxiliary sensor: temperature sensor in the line (cited; confirm availability with AFS) |" in md
    assert "engineering judgement: confirm availability" not in md
    nodes, _ = _structure(_charts(md)[0])
    assert nodes["aux1"].endswith("(confirm with AFS)")                 # the sketch keeps the label too


def test_auxiliary_label_returns_when_the_citation_fails():
    a = with_()
    a["parameters"][1]["citations"] = [cit("S01", 16, "Thermocouples are supplied with every probe.")]
    result, _ = run_with(assess=a, repairs=[a, a])
    assert "confirm availability with AFS" in render.to_markdown(result)


def test_not_measurable_inline_is_rendered_with_the_named_alternative():
    a = with_()
    a["parameters"].append({"id": "P3", "name": "Viscosity", "kind": "quantitative", "necessity": "optional",
                            "why": "The customer asks for it.",
                            "measured_by": {"type": "not_measurable_inline", "method": None, "sensor": None,
                                            "alternative": "an offline viscometer"}, "citations": []})
    md = render.to_markdown(run_with(assess=a)[0])
    assert "Not measurable in-line by spectroscopy; alternative: an offline viscometer" in md


# ----------------------------------------------------------------- 3.5 Mermaid
NODE = re.compile(r'^    (\w+)\["([^"\[\]|<>{}`]*)"\]$')
EDGE = re.compile(r"^    (\w+) (-->|-\.->) (\w+)$")


def _charts(md: str) -> list[str]:
    return re.findall(r"```mermaid\n(.*?)\n```", md, re.DOTALL)


def _structure(chart: str) -> tuple[dict, list]:
    lines = chart.splitlines()
    assert lines[0] == "flowchart LR"
    nodes, edges = {}, []
    for line in lines[1:]:
        if m := NODE.match(line):
            assert m.group(1) not in nodes
            nodes[m.group(1)] = m.group(2)
        else:
            m = EDGE.match(line)
            assert m, f"not a node or edge line: {line!r}"
            edges.append((m.group(1), m.group(2), m.group(3)))
    assert all(a in nodes and b in nodes for a, _, b in edges)
    return nodes, edges


def test_mermaid_chart_structure_for_the_recommended_option():
    md = render.to_markdown(run_with()[0])
    charts = _charts(md)
    assert len(charts) == 1
    nodes, edges = _structure(charts[0])
    chain = [("proc", "-->", "probe1"), ("probe1", "-->", "fiber1"), ("fiber1", "-->", "spec1"),
             ("spec1", "-->", "model"), ("model", "-->", "result")]
    assert all(e in edges for e in chain)
    assert nodes["probe1"] == "Raman probe" and nodes["spec1"] == "Raman spectrometer"
    assert nodes["fiber1"].startswith("Fiber: silica")
    assert ("aux1", "-.->", "model") in edges and nodes["aux1"].endswith("(confirm with AFS)")
    assert nodes["result"] == "Result: Ethanol concentration"


def test_mermaid_extended_option_gets_a_second_chart_with_a_fusion_model():
    md = render.to_markdown(run_with(assess=with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))[0])
    charts = _charts(md)
    assert len(charts) == 2
    nodes, edges = _structure(charts[1])
    assert {"probe1", "probe2"} <= set(nodes) and "fusion" in nodes["model"].lower()
    assert ("spec1", "-->", "model") in edges and ("spec2", "-->", "model") in edges


def test_mermaid_labels_are_escaped():
    a = with_()
    a["measurement_concept"]["location"] = 'Pipe "A" [DN50] | pump {x} <hot> #3 `y`'
    a["parameters"][1]["measured_by"]["sensor"] = 'sensor "T" [a|b]'
    chart = _charts(render.to_markdown(run_with(assess=a)[0]))[0]
    nodes, _ = _structure(chart)
    assert "#quot;A#quot;" in nodes["proc"] and "#91;DN50#93;" in nodes["proc"] and "#124;" in nodes["proc"]
    assert "#35;3" in nodes["proc"] and "#lt;hot#gt;" in nodes["proc"]
    assert render.mermaid_escape("#quot;") == "#35;quot;"            # '#' first: no double meaning


def test_mermaid_proposed_fiber_is_used_and_long_labels_are_shortened():
    a = with_()
    a["measurement_concept"]["location"] = "word " * 40
    r = run_with(assess=a)[0]
    r.slots["proposed_fiber"] = {"family": "silica", "for_method": "Raman"}
    nodes, _ = _structure(_charts(render.to_markdown(r))[0])
    assert nodes["fiber1"] == "Fiber: silica (proposed)"
    assert len(nodes["proc"]) <= render.MERMAID_LABEL_CHARS + 1 and nodes["proc"].endswith("…")


def test_mermaid_check_script_finds_blocks(tmp_path):
    md = render.to_markdown(run_with(assess=with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED]))[0])
    (tmp_path / "A.md").write_text(md, encoding="utf-8")
    found = _load_script("check_mermaid").blocks([tmp_path])
    assert [n for _, n, _ in found] == [1, 2] and all(c.startswith("flowchart LR") for _, _, c in found)


# ----------------------------------------------------------------- 3.6 render order and tables
def test_render_order():
    md = render.to_markdown(run_with(assess=with_(chemometrics_note="One model per method."))[0])
    order = ["# Answer", "**Customer request:**", "## Brief answer", "## Proposal", "**Decision status:**",
             "## Solution options", "## Setup sketch", "## Key questions", "# Expert detail", "**Customer enquiry**",
             "## Parameters", "## Solution option details", "## Requirements", "## Clarification questions",
             "## Recommendation", "## First feasibility experiment", "## Further notes", "## Evidence",
             "## Verification"]
    positions = [md.index(h) for h in order]
    assert positions == sorted(positions)
    assert "| P1 | Ethanol concentration | quantitative | required | Spectroscopy: Raman |" in md
    assert "| O2 | Recommended | M1 Raman probe | High | high (row 12) |" in md


def test_table_cells_escape_pipes():
    a = with_()
    a["solution_options"][0]["ease_of_use"] = "Easy | quick"
    md = render.to_markdown(run_with(assess=a)[0])
    assert "Easy \\| quick" in md


# ----------------------------------------------------------------- 3.4 prompt and skill
def test_assess_context_loads_the_fusion_skill_and_the_new_steps():
    _, client = run_with()
    system = next(s for s in client.seen if s["role"] == "assess")["system"]
    assert "# SKILL: multi-method-fusion" in system and "# SOURCE PAGES" in system
    text = pipeline.prompt("assess")
    for phrase in ("Single method first; combine methods only if one method is not enough",
                   "exactly one entry has role `primary`", "**Parameters**", "**Solution options**",
                   "**Proposal**", "**Brief answer**", "never write a price, a currency or a cost class yourself",
                   "`precedent_only`"):
        assert phrase in text


def test_skill_quotes_are_verbatim_on_the_cited_pages():
    text = (paths.ROOT / "skills" / "multi-method-fusion.md").read_text(encoding="utf-8")
    cited = re.findall(r'(S0\d) p\.(\d+) \["([^"]+)"\]', text)
    assert len(cited) >= 8
    for doc, page, quote in cited:
        assert quotes.verify(doc, int(page), quote).status == "exact", (doc, page, quote)


def test_manifest_records_the_skill_hash():
    result, _ = run_with()
    assert set(result.manifest["skills_sha256"]) == {"multi-method-fusion"}


# ----------------------------------------------------------------- 3.7 cheap open points
def test_combined_with_is_deduped_and_drops_the_own_method():
    a = with_()
    a["recommendations"][1]["combined_with"] = ["Raman", "Raman", "NIR"]
    a["recommendations"][1]["role"] = "conditional"
    result, _ = run_with(assess=a)
    assert result.assessment.recommendations[1].combined_with == ["Raman"]
    assert any(x["location"] == "recommendations[1].combined_with" for x in result.removed)


def test_combined_with_own_method_only_is_a_duplicate_of_the_single_entry():
    a = with_()
    dup = copy.deepcopy(a["recommendations"][0])
    dup.update(id="M3", role="comparison", combined_with=["Raman"])
    a["recommendations"].append(dup)
    result, _ = run_with(assess=a, repairs=[a, a])
    assert hard(result, "recommendations_unique")
    assert [r.id for r in result.assessment.recommendations] == ["M1", "M2"]


def test_code_dirty_ignores_outputs(tmp_path):
    repo = porcelain.init(str(tmp_path))
    (tmp_path / "outputs").mkdir()
    for name in ("a.py", "outputs/x.md"):
        (tmp_path / name).write_text("one\n")
    porcelain.add(repo, [str(tmp_path / "a.py"), str(tmp_path / "outputs" / "x.md")])
    porcelain.commit(repo, message=b"init", author=b"t <t@t>", committer=b"t <t@t>")
    (tmp_path / "outputs" / "x.md").write_text("two\n")
    assert provenance.code_dirty(tmp_path) is False
    (tmp_path / "a.py").write_text("two\n")
    assert provenance.code_dirty(tmp_path) is True


def test_method_labels_do_not_repeat_the_method():
    assert method_label("Raman", "raman_probe") == "Raman probe"
    assert method_label("Fluorescence", "fluorescence_probe") == "fluorescence probe"
    assert method_label("NIR", "transmission_transflection") == "NIR, transmission/transflection probe"
    assert "raman probe" not in render.to_markdown(run_with()[0])


@pytest.mark.parametrize("quote", ["unknown", "Unknown.", "n/a", "", "not stated"])
def test_intake_placeholders_are_not_reported_as_unquoted_removals(quote):
    intake = copy.deepcopy(INTAKE)
    intake["process"].append({"aspect": "temperature", "value": "unknown", "enquiry_quote": quote})
    _, removed = sanitize_intake(Intake.model_validate(intake), "We want to follow ethanol.")
    assert any(x.get("placeholder") for x in removed)
    result, _ = run_with(intake=intake)
    assert not [c for c in result.report.checks if c.name == "intake_sanitized" and "process" in c.location]
    assert "intake.process[1]" not in render.to_markdown(result)


def test_invented_quote_is_still_reported_as_a_removal():
    intake = copy.deepcopy(INTAKE)
    intake["process"].append({"aspect": "temperature", "value": "hot", "enquiry_quote": "runs at high heat"})
    result, _ = run_with(intake=intake)
    assert any(c.name == "intake_sanitized" for c in result.report.checks)
    assert "intake.process[1]" in render.to_markdown(result)


def test_mir_link_length_warning_needs_a_stated_distance():
    base = {"physical_state": "liquid", "optical_regime": "clear"}
    mir = {(c.method, c.technique): c for c in screen(base)}[("MIR", "ATR")]
    assert "R-FIB-2" not in mir.warnings
    far = {(c.method, c.technique): c for c in screen({**base, "remote_distance": "yes"})}[("MIR", "ATR")]
    assert "R-FIB-2" in far.warnings


def test_distance_process_fact_sets_the_remote_distance_slot():
    intake = copy.deepcopy(INTAKE)
    assert "remote_distance" not in pipeline.slots_from_intake(Intake.model_validate(intake))
    intake["process"].append({"aspect": "distance_or_remote_analyzer", "value": "analyzer away from the pipe",
                              "enquiry_quote": "flows through a pipe"})
    intake["sample"]["fluorophore"] = slot("unknown")
    assert pipeline.slots_from_intake(Intake.model_validate(intake))["remote_distance"] == "yes"


def test_option_flags_are_renumbered_after_an_option_is_dropped():
    a = with_(solution_options=ASSESSMENT["solution_options"] + [EXTENDED])
    a["recommendations"].append({"id": "M3", "method": "NIR", "technique": "diffuse_reflection", "role": "comparison",
                                 "combined_with": [], "rationale": "Reflection.", "conditions": "none",
                                 "citations": []})
    a["solution_options"][0]["recommendation_ids"] = ["M3"]                       # O1 will be dropped
    a["solution_options"][1]["performance_fit"] = "Error below 0.2 percent"       # O2 flagged (number)
    a["solution_options"][2]["maintenance"] = "Recalibrate every 7 weeks"         # O3 flagged (number)
    result, _ = run_with(assess=a, repairs=[a, a])
    assert [o.id for o in result.assessment.solution_options] == ["O2", "O3"]
    assert "figure" in result.flagged["solution_options[0]"] and "figure" in result.flagged["solution_options[1]"]
    assert "solution_options[2]" not in result.flagged
