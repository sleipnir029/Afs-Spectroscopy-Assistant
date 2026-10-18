"""kb check guards against silent knowledge traps, and a clean failure when the page text is absent."""

from __future__ import annotations

import pytest

from afs_assistant import cli, kb, kb_check, paths


# ------------------------------------------------------------------ doc ids vs schema.Doc
def test_doc_ids_in_schema_passes_for_the_schema_documents():
    pages = {(d, 1): {} for d in ("S01", "S02", "S03", "S04", "S05", "S06", "REF")}
    assert kb_check.doc_ids_in_schema(pages).ok


def test_a_document_missing_from_schema_doc_fails():
    pages = {(d, 1): {} for d in ("S01", "S02", "S03", "S04", "S05", "S06", "REF", "S07")}
    finding = kb_check.doc_ids_in_schema(pages)
    assert not finding.ok and "S07" in finding.detail


# ------------------------------------------------------------------ rule `when` vocabulary
def _rule(effect: str, when: dict) -> dict:
    return {"id": "R-TEST-1", "effect": effect, "when": when}


def test_committed_rules_use_the_screening_vocabulary():
    assert kb_check.rule_when_vocabulary(kb.rules()).ok


@pytest.mark.parametrize("when", [
    {"method": "NIR", "optical_regime": ["clear", "turbid"]},
    {"technique": "transmission", "aqueous": "yes"},
    {"heterogeneous": "no", "remote_distance": "yes"},
    {},
])
def test_valid_when_conditions_pass(when):
    assert kb_check.rule_when_vocabulary([_rule("exclude", when)]).ok


@pytest.mark.parametrize("when, expected", [
    ({"phys_state": "liquid"}, "unknown key 'phys_state'"),
    ({"physical_state": "liqud"}, "physical_state=['liqud']"),
    ({"method": "FTIR"}, "method=['FTIR']"),
    ({"technique": ["ATR", "transmision"]}, "technique=['transmision']"),
    ({"optical_regime": ["clear", "cloudy"]}, "optical_regime=['cloudy']"),
])
def test_a_typo_in_a_screening_rule_fails(when, expected):
    finding = kb_check.rule_when_vocabulary([_rule("exclude", when)])
    assert not finding.ok and expected in finding.detail


def test_evidence_keys_are_allowed_only_outside_screening_rules():
    assert kb_check.rule_when_vocabulary([_rule("scope_limit", {"claim": "readiness_clinical"})]).ok
    assert not kb_check.rule_when_vocabulary([_rule("warn", {"claim": "readiness_clinical"})]).ok


# ------------------------------------------------------------------ fresh clone without pages.jsonl
@pytest.fixture
def no_pages(monkeypatch, tmp_path):
    monkeypatch.setattr(paths, "PAGES_FILE", tmp_path / "pages.jsonl")
    kb.pages.cache_clear()
    yield
    kb.pages.cache_clear()


def test_missing_pages_raise_a_clear_error(no_pages):
    assert not kb.pages_available()
    with pytest.raises(kb.PagesMissing, match="afs-assist kb build"):
        kb.pages()


def test_kb_check_reports_missing_pages_with_the_hint(no_pages):
    findings = {f.check: f for f in kb_check.run()}
    assert not findings["pages_present"].ok
    assert "afs-assist kb build" in findings["pages_present"].detail
    assert "page_counts" not in findings and "source_quotes_exact" not in findings
    assert findings["rule_when_vocabulary"].ok and findings["no_case_ids"].ok


@pytest.mark.parametrize("argv", [
    ["assess", "--text", "We want to follow moisture in a powder.", "--external", "off"],
    ["run", "--set", "dev", "--only", "X"],
    ["ui"],
])
def test_cli_commands_that_need_pages_fail_cleanly(no_pages, monkeypatch, capsys, argv):
    from afs_assistant.ui import server

    monkeypatch.setattr(server, "serve", lambda *a, **k: pytest.fail("server started without pages"))
    monkeypatch.setattr(cli, "_assess_one", lambda *a, **k: pytest.fail("assessment started without pages"))
    assert cli.main(argv) == 2
    err = capsys.readouterr().err
    assert "needs knowledge/pages.jsonl" in err and "afs-assist kb build" in err
