"""Phase 2 offline tests: pipeline flow, verification checks, finalize, render, provenance.

Fixtures use a made-up generic enquiry (not a dev or final scenario) and real quotes
from knowledge/pages.jsonl.
"""

from __future__ import annotations

import copy
import json
import os

import pytest
from dulwich.object_store import iter_tree_contents
from dulwich.repo import Repo

from afs_assistant import pipeline, provenance, render
from afs_assistant.llm import FakeClient, strict_schema
from afs_assistant.schema import Assessment, Intake
from afs_assistant.verify import forbidden_hits

ENQUIRY = ("We want to follow ethanol in a clear aqueous fermentation broth that flows through a pipe. "
           "Gas chromatography results from the lab are available as reference.")

RAMAN_QUOTE = ("Raman is particularly well-suited for aqueous environments, as it exhibits low absorbance "
               "for water molecules compared to infrared methods.")
NIR_QUOTE = "NIR spectra (780-2500 nm) contain predominantly overtones and component bands of fundamental vibrations"
PLAN_QUOTE = ("Representative samples or process states, independent reference measurements, what is compared, "
              "and the basis for the go / no-go decision.")


def cit(doc, page, quote, kind="general"):
    return {"doc": doc, "page": page, "quote": quote, "claim_kind": kind}


def slot(value, basis="unknown", quote=None):
    return {"value": value, "basis": basis, "enquiry_quote": quote}


INTAKE = {
    "routes": ["in_scope", "needs_clarification"],
    "summary": "Follow ethanol in a flowing aqueous fermentation broth.",
    "facts_stated": [{"text": "Broth is clear and aqueous", "enquiry_quote": "clear aqueous fermentation broth"}],
    "targets": [{"variable": "ethanol", "purpose": "follow during fermentation", "enquiry_quote": "follow ethanol"}],
    "sample": {
        "physical_state": slot("liquid", "inferred_from_stated", "flows through a pipe"),
        "optical_regime": slot("clear", "stated", "clear aqueous fermentation broth"),
        "aqueous": slot("yes", "stated", "aqueous"),
        "heterogeneous": slot("unknown"),
        "fluorophore": slot("unknown"),
    },
    "process": [{"aspect": "reference_method", "value": "lab GC", "enquiry_quote": "Gas chromatography results"}],
    "customer_premises": [],
    "proposed_fiber": {"family": "none", "for_method": "none", "enquiry_quote": None},
    "unknowns": ["ethanol concentration range", "temperature"],
}

ASSESSMENT = {
    "decision_status": "provisional_assessment",
    "status_reason": "Methods for aqueous metabolite monitoring can be shortlisted; ranges are unknown.",
    "premise_checks": [],
    "requirements_stated": ["Ethanol in a clear aqueous broth", "Lab GC reference available"],
    "key_unknowns": ["Ethanol concentration range", "Temperature"],
    "clarification_questions": [
        {"id": "Q1", "question": "Which ethanol concentration range must be followed?",
         "why_it_matters": "Decides whether NIR sensitivity is enough.", "affects": ["M2"]},
    ],
    "recommendations": [
        {"id": "M1", "method": "Raman", "technique": "raman_probe", "role": "primary", "combined_with": [],
         "rationale": "Water interferes little with Raman.", "conditions": "none",
         "citations": [cit("S01", 16, RAMAN_QUOTE)]},
        {"id": "M2", "method": "NIR", "technique": "transmission_transflection", "role": "comparison",
         "combined_with": [],
         "rationale": "NIR transmission suits clear liquids.", "conditions": "if the range is high enough",
         "citations": [cit("S01", 10, NIR_QUOTE)]},
    ],
    "measurement_concept": {"probe_and_geometry": "Immersion Raman probe; NIR transmission probe for comparison.",
                            "location": "In the flowing line, to be agreed.", "fiber_link": "Silica fibers.",
                            "citations": [cit("S01", 16, RAMAN_QUOTE)]},
    "spectral_ranges": [{"method": "NIR", "statement": "Nominal NIR range 780-2500 nm; usable range depends on the setup.",
                         "citations": [cit("S01", 10, NIR_QUOTE)]},
                        {"method": "Raman", "statement": "State the excitation wavelength separately from the "
                                                         "Raman shift; usable range depends on the setup.",
                         "citations": [cit("S01", 16, RAMAN_QUOTE)]}],
    "risks": [{"risk": "Fluorescence background may limit Raman.", "rule_ids": ["R-RAM-1"],
               "citations": [cit("S01", 11, "superposition of luminescence (fluorescence), which has a significantly higher intensity.")]}],
    "feasibility_plan": {"steps": [{"step": "Collect representative broth samples with GC references.",
                                    "purpose": "Build and validate single-method models.",
                                    "citations": [cit("REF", 3, PLAN_QUOTE)]}],
                         "reference_measurements": "Lab GC on the same samples.",
                         "decision_basis": "Error and bias against criteria agreed with the customer."},
    "assumptions": [],
    "not_in_sources": ["Ethanol detection limits for this broth"],
    "parameters": [
        {"id": "P1", "name": "Ethanol concentration", "kind": "quantitative", "necessity": "required",
         "why": "The quantity the customer wants to follow.",
         "measured_by": {"type": "spectroscopy", "method": "Raman", "sensor": None, "alternative": None},
         "citations": []},
        {"id": "P2", "name": "Broth temperature", "kind": "quantitative", "necessity": "optional",
         "why": "Temperature changes the spectra and may need compensation.",
         "measured_by": {"type": "auxiliary_sensor", "method": None, "sensor": "temperature sensor in the line",
                         "alternative": None},
         "citations": []},
    ],
    "solution_options": [
        {"id": "O1", "tier": "simple", "recommendation_ids": ["M2"], "parameter_ids": ["P1"],
         "ease_of_use": "One transmission probe in the line", "maintenance": "Window cleaning",
         "performance_fit": "Depends on the ethanol range", "cost_drivers": "One spectrometer and one probe",
         "fusion_note": None, "citations": []},
        {"id": "O2", "tier": "recommended", "recommendation_ids": ["M1"], "parameter_ids": ["P1", "P2"],
         "ease_of_use": "One immersion probe in the line", "maintenance": "Probe window cleaning",
         "performance_fit": "Water interferes little", "cost_drivers": "Laser source and spectrometer",
         "fusion_note": None, "citations": [cit("S01", 16, RAMAN_QUOTE)]},
    ],
    "chemometrics_note": None,
    "realtime_tracking_note": None,
    "future_direction": None,
    "proposal": {"best_current_option": "O2", "basis": "supplied",
                 "what_would_change_it": "A low ethanol range or a strong fluorescence background of the broth.",
                 "next_step": "Measure representative broth samples with GC references."},
    "brief_answer": ("Test a Raman probe in the line first, with NIR transmission as a comparison. "
                     "The ethanol range and the fluorescence of the broth are still open."),
}


def run_with(intake=INTAKE, assess=ASSESSMENT, repairs=()):
    client = FakeClient({"intake": [intake], "assess": [assess], "repair": list(repairs)})
    return pipeline.run(ENQUIRY, client, run_id="test-run"), client


def failures(result, name):
    return [c for c in result.report.hard_failures if c.name == name]


# ----------------------------------------------------------------- schema
def test_fixtures_match_schemas():
    Intake.model_validate(INTAKE)
    Assessment.model_validate(ASSESSMENT)


def test_strict_schema_requires_all_properties():
    def objects(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                yield node
            for v in node.values():
                yield from objects(v)
        elif isinstance(node, list):
            for v in node:
                yield from objects(v)
    for model in (Intake, Assessment):
        for obj in objects(strict_schema(model.model_json_schema())):
            assert set(obj["required"]) == set(obj["properties"]) and obj["additionalProperties"] is False


# ----------------------------------------------------------------- happy path
def test_clean_assessment_passes_without_repair():
    result, client = run_with()
    assert result.report.passed, [(c.name, c.location, c.message) for c in result.report.hard_failures]
    assert [s["role"] for s in client.seen] == ["intake", "assess"]
    assert result.report.summary()["citations_verified"] == result.report.summary()["citations_total"]


def test_assess_prompt_contains_knowledge_and_screening():
    _, client = run_with()
    assess = next(s for s in client.seen if s["role"] == "assess")
    assert "[S01 p.10 |" in assess["system"] and "[R-FIB-1]" in assess["system"]
    assert "Figure (our description)" not in assess["system"]          # S02 notes never shown as quotable
    assert "# SCREENING" in assess["user"] and ENQUIRY in assess["user"]


# ----------------------------------------------------------------- verification failures
def test_fake_quote_triggers_repair_and_is_removed():
    bad = copy.deepcopy(ASSESSMENT)
    bad["recommendations"][0]["citations"] = [cit("S01", 16, "Raman always beats NIR for ethanol in every broth.")]
    result, client = run_with(assess=bad, repairs=[bad, bad])
    assert [s["role"] for s in client.seen] == ["intake", "assess", "repair", "repair"]
    assert failures(result, "quote_verified")
    assert result.removed and result.assessment.recommendations[0].citations == []
    md = render.to_markdown(result)
    assert "✓ **S01 p.16** (general): \"Raman always" not in md
    assert "⚠" in md and "no verified source" in md


def test_repair_that_fixes_the_quote_passes():
    bad = copy.deepcopy(ASSESSMENT)
    bad["recommendations"][0]["citations"] = [cit("S01", 16, "Raman always beats NIR for ethanol in every broth.")]
    result, _ = run_with(assess=bad, repairs=[ASSESSMENT])
    assert result.report.passed and len(result.repairs) == 1


def test_invented_number_is_flagged_claim_locally():
    bad = copy.deepcopy(ASSESSMENT)
    bad["recommendations"][1]["rationale"] = "NIR reaches 0.05% accuracy over a 150 m silica cable."
    result, _ = run_with(assess=bad, repairs=[bad, bad])
    assert failures(result, "numbers_claim_local")


def test_invented_client_fact_is_flagged():
    bad = copy.deepcopy(INTAKE)
    bad["facts_stated"].append({"text": "Temperature is 37 C", "enquiry_quote": "kept at 37 °C"})
    bad["sample"]["heterogeneous"] = slot("no", "stated", "perfectly homogeneous")
    result, client = run_with(intake=bad)
    assert [s["role"] for s in client.seen] == ["intake", "assess"]          # no repair loop for intake
    assert all("37" not in f.text for f in result.intake.facts_stated)
    assert result.intake.sample.heterogeneous.value == "unknown"
    assert {r["location"] for r in result.intake_removed} == {"intake.facts_stated[1]", "intake.sample.heterogeneous"}
    assert "37" not in next(s["user"] for s in client.seen if s["role"] == "assess").split("# INTAKE")[1]


def test_recommending_a_failed_candidate_is_flagged():
    intake = copy.deepcopy(INTAKE)
    intake["sample"]["fluorophore"] = slot("no", "stated", "ethanol")
    bad = copy.deepcopy(ASSESSMENT)
    bad["recommendations"].append({"id": "M3", "method": "Fluorescence", "technique": "fluorescence_probe",
                                   "role": "primary", "combined_with": [], "rationale": "Very sensitive.",
                                   "conditions": "none",
                                   "citations": [cit("S01", 16, RAMAN_QUOTE)]})
    result, _ = run_with(intake=intake, assess=bad, repairs=[bad, bad])
    assert failures(result, "respects_screen")


def test_contradicted_premise_cannot_stay_provisional():
    bad = copy.deepcopy(ASSESSMENT)
    bad["premise_checks"] = [{"premise": "Fluorescence can measure ethanol directly", "verdict": "contradicted",
                              "explanation": "Fluorescence needs a fluorescent species.",
                              "citations": [cit("S01", 5, "However, most chemicals do not exhibit this property.")]}]
    result, _ = run_with(assess=bad, repairs=[bad, bad])
    assert failures(result, "status_vs_premises")


def test_forbidden_wording_is_flagged():
    bad = copy.deepcopy(ASSESSMENT)
    bad["status_reason"] = "Raman will work and we guarantee the result."
    result, _ = run_with(assess=bad, repairs=[bad, bad])
    assert failures(result, "forbidden_wording")


def test_unknown_deciding_slot_must_be_asked():
    intake = copy.deepcopy(INTAKE)
    intake["sample"]["optical_regime"] = slot("unknown")
    bad = copy.deepcopy(ASSESSMENT)          # recommends NIR transmission but asks nothing about clarity
    result, _ = run_with(intake=intake, assess=bad, repairs=[bad, bad])
    assert failures(result, "unknown_slot_addressed")


def test_scope_mismatch_is_flagged():
    bad = copy.deepcopy(ASSESSMENT)
    bad["recommendations"][0]["citations"] = [cit("S05", 1, "Test of Customer Process in-situ", "general")]
    result, _ = run_with(assess=bad, repairs=[bad, bad])
    assert failures(result, "citation_scope") or failures(result, "quote_verified")


# ----------------------------------------------------------------- render + provenance
def test_render_has_all_sections():
    result, _ = run_with()
    md = render.to_markdown(result, "test")
    for heading in ("Decision status", "## Requirements", "## Clarification questions", "## Recommendation",
                    "## Measurement concept", "## Spectral range", "## Risks and uncertainty",
                    "## First feasibility experiment", "## Evidence (verified quotes)", "## Verification"):
        assert heading in md
    data = render.to_json(result)
    assert json.dumps(data) and data["verification"]["summary"]["passed"]


def test_provenance_commit_on_separate_ref(tmp_path):
    Repo.init(str(tmp_path))
    result, _ = run_with()
    data = render.to_json(result)
    sha1 = provenance.record("r1", provenance.run_files(data, "md"), "run r1", repo_path=tmp_path)
    sha2 = provenance.record("r2", provenance.run_files(data, "md"), "run r2", repo_path=tmp_path)
    repo = Repo(str(tmp_path))
    assert repo.refs[b"refs/heads/provenance"].decode() == sha2
    assert repo[sha2.encode()].parents == [sha1.encode()]
    paths_in_tree = {e.path.decode() for e in iter_tree_contents(repo.object_store, repo[sha2.encode()].tree)}
    assert "runs/r1/manifest.json" in paths_in_tree and "runs/r2/assessment.json" in paths_in_tree
    assert b"refs/heads/master" not in repo.refs and b"refs/heads/main" not in repo.refs


@pytest.mark.skipif(not os.environ.get("OPENROUTER_API_KEY"), reason="no API key (live smoke test)")
def test_live_smoke():
    from afs_assistant.llm import OpenRouterClient
    result = pipeline.run(ENQUIRY, OpenRouterClient(), run_id="live-smoke")
    assert result.assessment.recommendations


# ----------------------------------------------------------------- fixes 2.R


@pytest.mark.parametrize("text", [
    "The example is a reason to test, not proof that NIR will work for this blend.",
    "The sources do not guarantee it for this specific process.",
    "No source says the sensor is ready for clinical use.",
])
def test_negated_cautious_phrases_are_not_forbidden(text):
    assert forbidden_hits(text) == []


@pytest.mark.parametrize("text", [
    "NIR will work for this blend.",
    "We guarantee the accuracy.",
    "The sensor is ready for clinical use.",
    "Order part ABC-12345 for about $400.",
])
def test_asserted_forbidden_phrases_are_flagged(text):
    assert forbidden_hits(text)


def test_duplicate_method_technique_is_a_hard_failure():
    bad = copy.deepcopy(ASSESSMENT)
    dup = copy.deepcopy(bad["recommendations"][0])
    dup.update(id="M3", role="not_recommended")
    bad["recommendations"].append(dup)
    result, _ = run_with(assess=bad, repairs=[bad, bad])
    assert failures(result, "recommendations_unique")


def test_too_many_recommendations_is_a_soft_warning():
    bad = copy.deepcopy(ASSESSMENT)
    for i, (m, tq) in enumerate([("MIR", "ATR"), ("UV-Vis", "transmission_transflection"),
                                 ("NIR", "diffuse_reflection"), ("UV-Vis", "ATR")]):
        bad["recommendations"].append({"id": f"M{i + 3}", "method": m, "technique": tq, "role": "not_recommended",
                                       "combined_with": [], "rationale": "Listed for completeness.",
                                       "conditions": "none", "citations": []})
    result, _ = run_with(assess=bad)
    assert any(c.name == "recommendation_count" for c in result.report.soft_failures)


def test_combination_is_rendered_as_hypothesis():
    combo = copy.deepcopy(ASSESSMENT)
    combo["recommendations"][0]["combined_with"] = ["NIR"]
    result, _ = run_with(assess=combo)
    md = render.to_markdown(result)
    assert "Primary candidate: Raman probe.**" in md and "Raman + NIR" not in md
    assert "Later hypothesis, after single-method tests: combine with NIR." in md
    assert any(c.name == "primary_single_method" for c in result.report.soft_failures)
