"""The model inputs of the frozen held-out run must not change by accident.

The held-out outputs (outputs/final/, tag freeze-1) were generated once. Their manifest records the sha256
of every prompt, the skill, the knowledge block, the page text, the rules, the curated library and the
models config. This test recomputes them from the working tree, so a refactor that silently changes what
the model sees fails here. The strict JSON schemas are not in the manifest: their hashes were computed
from the freeze-1 code (same as the current tree) and are pinned below.

A deliberate change to any of these inputs must update this test and be logged in DEVIATIONS.md.
"""

from __future__ import annotations

import hashlib
import json

import pytest

from afs_assistant import kb, paths, pipeline
from afs_assistant.external import library, step
from afs_assistant.llm import config_provenance
from afs_assistant.schema import Assessment, Intake

MANIFEST = json.loads((paths.OUTPUTS / "final" / "H01.json").read_text(encoding="utf-8"))["manifest"]

# sha256 of json.dumps(Model.model_json_schema()), the schema sent with each strict-JSON call (freeze-1 code).
SCHEMA_SHA256 = {
    "Intake": "02d95b3d3b7f7b7d81f532603fe337f68109cd77069878e110f298efe01df4da",
    "Assessment": "f9e598414367af91bca73cfdc42fec198cbb0570e644096c45754b7bf4167d76",
    "QueryPlan": "d8a6b8428a9b502227120e2e3536937e4c0511ccd785496102df00b1ce1711ea",
    "EvidenceReply": "64c3b378cb44f0fa021ea0d447950ff43d2be6dcafb2a880186dffff9db4e5f0",
}


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_prompts_match_the_freeze_manifest():
    recorded = MANIFEST["prompt_sha256"]
    assert set(recorded) == {"intake", "assess", "repair", "external_queries", "external_evidence"}
    current = {n: _sha(pipeline.prompt(n)) for n in ("intake", "assess", "repair")} | step.prompt_hashes()
    assert current == recorded


def test_skill_matches_the_freeze_manifest():
    assert {n: _sha(pipeline.skill(n)) for n in pipeline.ASSESS_SKILLS} == MANIFEST["skills_sha256"]


def test_rules_library_and_models_config_match_the_freeze_manifest(monkeypatch):
    monkeypatch.delenv("AFS_MODELS_CONFIG", raising=False)
    assert _sha(paths.RULES_FILE.read_text(encoding="utf-8")) == MANIFEST["rules_sha256"]
    assert library.library_sha() == MANIFEST["external_library_sha256"]
    assert config_provenance() == MANIFEST["models_config"]


@pytest.mark.needs_pages
def test_knowledge_block_and_pages_match_the_freeze_manifest():
    assert _sha(paths.PAGES_FILE.read_text(encoding="utf-8")) == MANIFEST["pages_sha256"]
    assert _sha(pipeline.knowledge_block()) == MANIFEST["knowledge_sha256"]
    assert kb.pages_available()


def test_strict_schemas_are_unchanged():
    models = {"Intake": Intake, "Assessment": Assessment, "QueryPlan": step.QueryPlan,
              "EvidenceReply": step.EvidenceReply}
    assert {name: _sha(json.dumps(m.model_json_schema())) for name, m in models.items()} == SCHEMA_SHA256
