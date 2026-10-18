"""Short brief view (`afs_assistant.brief`): code-built from the saved run JSON, no model call."""

from __future__ import annotations

import copy
import json
import re
import shutil

import pytest

from afs_assistant import brief, cli, kb, paths, quotes

pytestmark = pytest.mark.skipif(not paths.PAGES_FILE.exists(),
                                reason="knowledge/pages.jsonl missing: run `afs-assist kb build` (rule quotes are "
                                       "checked against the pages)")

SETS = ("dev", "final")
RUNS = sorted(p for s in SETS for p in (paths.OUTPUTS / s).glob("*.json"))
ADVERSARIAL = sorted((paths.OUTPUTS / "adversarial").glob("*.json"))
WORD_MIN, WORD_MAX = 300, 700
# Internal ids: option, recommendation, question, parameter, gap, external-source and rule ids.
INTERNAL_ID = re.compile(r"\b[OMNQPG]\d+\b|\bE\d\d\b|\bR-[A-Z]+-\d+\b")
CITE = re.compile(r"\b(S0\d p\.\d+|REF §\d+)")
RELATED = re.compile(r'related AFS source: (S0\d) p\.(\d+), "(.*?)"; not checked against this sentence\)')


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _verified_labels(data: dict) -> set[str]:
    return {kb.citation_label(d, p) for d, p, _ in brief.verified_set(data)}


def _without_related(text: str) -> str:
    return RELATED.sub("", text)


def test_saved_runs_exist():
    assert len(RUNS) >= 2


@pytest.mark.parametrize("path", RUNS + ADVERSARIAL, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_saved_run_renders(path):
    data = _load(path)
    text = brief.to_markdown(data, "a title", "[full](../x.md)")
    assert text.startswith("# Short brief: a title")
    assert "…" not in text and "..." not in text
    assert not INTERNAL_ID.search(text), INTERNAL_ID.search(text)
    if data.get("assessment") is not None:
        assert WORD_MIN <= brief.word_count(text) <= WORD_MAX
        for heading in ("## Requirements", "## Recommendation", "## Measurement concept",
                        "## Risks and uncertainty", "## Feasibility plan", "## Sources"):
            assert heading in text


@pytest.mark.parametrize("path", RUNS + ADVERSARIAL, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_shown_citation_was_verified_by_the_run(path):
    data = _load(path)
    text = brief.to_markdown(data)
    allowed = _verified_labels(data)
    shown = set(CITE.findall(_without_related(text)))
    assert shown <= allowed, shown - allowed


@pytest.mark.parametrize("path", RUNS + ADVERSARIAL, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_related_rule_sources_are_stored_rule_quotes_verbatim_on_their_page(path):
    text = brief.to_markdown(_load(path))
    stored = {(s["doc"], int(s["page"]), " ".join(s["quote"].split())) for r in kb.rules() for s in r["sources"]}
    for doc, page, quote in RELATED.findall(text):
        assert (doc, int(page), quote) in stored
        assert quotes.verify(doc, int(page), quote).ok


@pytest.mark.parametrize("set_name", SETS)
def test_committed_briefs_are_current_and_generation_is_idempotent(set_name):
    src = paths.OUTPUTS / set_name
    committed = src / "brief"
    runs = [p for p in sorted(src.glob("*.json")) if brief.is_run_json(_load(p))]
    assert runs
    for run in runs:
        text = brief.brief_for(run, committed)
        assert text == brief.brief_for(run, committed)                  # same JSON, same page
        assert (committed / f"{run.stem}.md").read_text(encoding="utf-8") == text   # committed copy is current


def test_full_answer_link_is_relative_to_the_brief_folder(tmp_path):
    run = RUNS[0]
    shutil.copy(run, tmp_path / run.name)
    (written, _), = brief.write_briefs(tmp_path, tmp_path / "brief")
    assert f"[{run.stem}.md](../{run.stem}.md)" in written.read_text(encoding="utf-8")


def _first_assessed() -> dict:
    return copy.deepcopy(next(d for d in map(_load, RUNS) if d.get("assessment")))


@pytest.mark.parametrize("path", RUNS, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_status_line_leads_with_the_runs_own_status_label(path):
    data = _load(path)
    label, _ = brief.STATUS_LINE[data["assessment"]["decision_status"]]
    lines = [x for x in brief.to_markdown(data).splitlines() if x.startswith("**")]
    assert lines[0].startswith(f"**{label}:** ")
    assert "Decision status" not in lines[0]


def test_every_status_has_a_plain_label_and_one_short_clause():
    from afs_assistant.schema import Assessment
    statuses = set(Assessment.model_fields["decision_status"].annotation.__args__)
    assert set(brief.STATUS_LINE) == statuses
    assert brief.STATUS_LINE["premise_not_supported"][0] == "Premise not supported"
    for _, clause in brief.STATUS_LINE.values():
        assert clause.endswith(".") and clause.count(".") == 1 and len(clause.split()) <= 20


def test_unverified_citation_is_not_shown():
    data = _first_assessed()
    a = data["assessment"]
    a["measurement_concept"]["citations"] = [{"doc": "S05", "page": 1, "quote": "not a verified quote at all",
                                              "claim_kind": "general"}]
    data["verification"]["citations"] = [c for c in data["verification"]["citations"] if c["doc"] != "S05"]
    text = brief.to_markdown(data)
    assert "S05 p.1" not in text


def test_internal_ids_are_replaced_by_labels():
    data = _first_assessed()
    a = data["assessment"]
    rec = a["recommendations"][0]
    option = a["solution_options"][0]
    q_ids = [q["id"] for q in a["clarification_questions"]]
    a["feasibility_plan"]["decision_basis"] = (f"Criteria from the customer ({q_ids[0]}); compare "
                                               f"{rec['id']}/{rec['id']} and keep {option['id']} if it is enough "
                                               f"(method per {q_ids[-1]}).")
    text = brief.to_markdown(data)
    line = next(x for x in text.splitlines() if x.startswith("- **Decision basis:**"))
    assert not INTERNAL_ID.search(line)
    assert "Criteria from the customer; compare" in line
    assert f"the {option['tier']} option" in line
    assert f"{rec['method']}" in line


def test_external_item_shown_only_when_it_supports_the_proposed_option():
    data = _first_assessed()
    best = data["assessment"]["proposal"]["best_current_option"]
    other = next((o["id"] for o in data["assessment"]["solution_options"] if o["id"] != best), None)
    source = {"id": "X1", "title": "A verified paper", "year": 2020, "url": "https://example.org/paper"}
    item = {"gap_id": "G1", "option_id": other,
            "citation": {"source_id": "X1", "label": "X1 ¶1", "quote": "A verified passage from the paper."}}
    data["external"] = {"items": [item], "sources": [source], "gap_results": [{"gap_id": "G1", "items": []}]}
    assert "Secondary literature" not in brief.to_markdown(data)
    item["option_id"] = best
    text = brief.to_markdown(data)
    assert "## Secondary literature (external, not AFS material)" in text
    assert '*A verified paper* (2020), https://example.org/paper: "A verified passage from the paper."' in text
    assert "no usable external source" not in text


def test_unknowns_already_asked_by_a_shown_question_are_left_out():
    questions = [{"question": "Which reference assay and sampling frequency are available?"}]
    unknowns = ["Reference assay and sampling frequency available", "Process temperature range"]
    assert brief.unasked(unknowns, questions) == ["Process temperature range"]


def test_off_topic_run_gives_a_short_page():
    off = next((d for d in map(_load, ADVERSARIAL) if d.get("assessment") is None), None)
    if off is None:
        pytest.skip("no saved off-topic run")
    text = brief.to_markdown(off, "t")
    assert "Outside the supported scope" in text and off["off_topic"]["message"] in text


def test_cli_brief_writes_one_file_per_run(tmp_path, capsys):
    run = RUNS[0]
    shutil.copy(run, tmp_path / run.name)
    assert cli.main(["brief", str(tmp_path), "--out", str(tmp_path / "out")]) == 0
    assert (tmp_path / "out" / f"{run.stem}.md").exists()
    assert "1 brief(s) written" in capsys.readouterr().out
    assert cli.main(["brief", str(tmp_path / "missing")]) == 2
