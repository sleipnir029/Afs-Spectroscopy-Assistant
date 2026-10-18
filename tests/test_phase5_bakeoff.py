"""Plan 5.8 offline tests (D-054): per-model omitted request params, the AFS_MODELS_CONFIG override with its
manifest record, `run --outputs`, and the bake-off arm configs.

No network and no LLM calls: a fake OpenAI SDK client and FakeClient. Made-up generic enquiry only.
"""

from __future__ import annotations

import copy
import hashlib

import pytest
from test_phase2 import run_with
from test_phase2_r2 import _client, _response

from afs_assistant import cli, llm, paths, scenarios
from afs_assistant.llm import SpendTracker

SCHEMA = {"type": "object", "properties": {}}


@pytest.fixture
def fresh_config(monkeypatch):
    """Load the models config anew (cached per process) before and after the test."""
    monkeypatch.delenv(llm.CONFIG_ENV, raising=False)
    llm._config_source.cache_clear()
    llm.config.cache_clear()
    yield
    llm._config_source.cache_clear()
    llm.config.cache_clear()


def _with_params(monkeypatch, model_params: dict) -> dict:
    cfg = copy.deepcopy(llm.config())
    cfg["model_params"] = model_params
    monkeypatch.setattr(llm, "config", lambda: cfg)
    return cfg


# ----------------------------------------------------------------- (a) per-model omitted params
def test_temperature_is_sent_by_default():
    client = _client([_response('{"a": 1}')])
    client.complete_json("assess", "sys", "user", "assessment", SCHEMA)
    assert client.client.kwargs[0]["temperature"] == llm.config()["temperature"]


def test_a_model_that_omits_temperature_gets_no_temperature(monkeypatch):
    model = llm.config()["roles"]["assess"]["model"]
    cfg = _with_params(monkeypatch, {model: {"omit": ["temperature"]}})
    client = _client([_response('{"a": 1}')])
    client.complete_json("assess", "sys", "user", "assessment", SCHEMA)
    sent = client.client.kwargs[0]
    assert "temperature" not in sent
    assert sent["max_tokens"] == cfg["roles"]["assess"]["max_tokens"] and sent["response_format"]["type"]
    assert sent["extra_body"]["provider"]["require_parameters"] is True


def test_params_of_another_model_do_not_apply(monkeypatch):
    _with_params(monkeypatch, {"other/model": {"omit": ["temperature"]}})
    client = _client([_response('{"a": 1}')])
    client.complete_json("assess", "sys", "user", "assessment", SCHEMA)
    assert "temperature" in client.client.kwargs[0]


def test_omitting_a_required_param_is_a_config_error(monkeypatch):
    model = llm.config()["roles"]["assess"]["model"]
    _with_params(monkeypatch, {model: {"omit": ["messages"]}})
    client = _client([_response('{"a": 1}')])
    with pytest.raises(ValueError, match="cannot omit"):
        client.complete_json("assess", "sys", "user", "assessment", SCHEMA)
    assert client.client.kwargs == []


# ----------------------------------------------------------------- (b) AFS_MODELS_CONFIG and the manifest
def test_default_models_config_is_recorded_in_the_manifest(fresh_config):
    assert llm.config_path() == llm.CONFIG_FILE
    result, _ = run_with()
    digest = hashlib.sha256(llm.CONFIG_FILE.read_bytes()).hexdigest()
    assert result.manifest["models_config"] == {"path": "config/models.yaml", "sha256": digest}


def test_env_var_selects_another_config_relative_to_the_repo_root(fresh_config, monkeypatch, tmp_path):
    root, work = tmp_path / "repo", tmp_path / "elsewhere"
    alt = root / "config" / "alt.yaml"
    alt.parent.mkdir(parents=True)
    work.mkdir()
    alt.write_text(llm.CONFIG_FILE.read_text(encoding="utf-8").replace("per_run: 1.00", "per_run: 0.25"),
                   encoding="utf-8")
    monkeypatch.setattr(paths, "ROOT", root)
    monkeypatch.setenv(llm.CONFIG_ENV, "config/alt.yaml")
    monkeypatch.chdir(work)                         # relative to the repo root, not the working directory
    assert llm.config_path() == alt and llm.config()["spend_cap_usd"]["per_run"] == 0.25
    assert llm.config_provenance() == {"path": "config/alt.yaml",
                                       "sha256": hashlib.sha256(alt.read_bytes()).hexdigest()}


def test_env_var_with_an_absolute_path_outside_the_repo(fresh_config, monkeypatch, tmp_path):
    other = tmp_path / "models.yaml"
    text = llm.CONFIG_FILE.read_text(encoding="utf-8").replace("per_run: 1.00", "per_run: 0.50")
    other.write_text(text, encoding="utf-8")
    monkeypatch.setenv(llm.CONFIG_ENV, str(other))
    assert llm.config()["spend_cap_usd"]["per_run"] == 0.5
    assert llm.config_provenance() == {"path": str(other), "sha256": hashlib.sha256(other.read_bytes()).hexdigest()}


# ----------------------------------------------------------------- (c) run --outputs
def _run_set_out_dirs(monkeypatch, argv: list[str]) -> list:
    class StubClient:
        def __init__(self):
            self.tracker = SpendTracker(1e9, 1e9)

    seen = []

    def fake_assess_one(enquiry, scenario_id, client, out_dir, title, **_):
        seen.append(out_dir)
        return {"summary": {"passed": True}, "cost_usd": 0.0}

    monkeypatch.setattr(llm, "OpenRouterClient", StubClient)
    monkeypatch.setattr(scenarios, "load", lambda name: [{"id": "X01", "title": "a", "enquiry": "first"}])
    monkeypatch.setattr(cli, "_assess_one", fake_assess_one)
    assert cli.main(argv) == 0
    return seen


def test_run_writes_to_outputs_set_by_default(monkeypatch):
    assert _run_set_out_dirs(monkeypatch, ["run", "--set", "dev"]) == [paths.OUTPUTS / "dev"]


def test_run_outputs_flag_sets_the_directory(monkeypatch, tmp_path):
    out = tmp_path / "bakeoff" / "arm" / "dev"
    assert _run_set_out_dirs(monkeypatch, ["run", "--set", "dev", "--outputs", str(out)]) == [out]


# ----------------------------------------------------------------- bake-off arm configs (config/bakeoff/)
ARMS = sorted((paths.ROOT / "config" / "bakeoff").glob("*.yaml"))


def _use(monkeypatch, config_file) -> dict:
    monkeypatch.setenv(llm.CONFIG_ENV, str(config_file))
    llm._config_source.cache_clear()
    llm.config.cache_clear()
    return llm.config()


def test_there_are_bakeoff_arms():
    assert len(ARMS) >= 4


@pytest.mark.parametrize("arm", ARMS, ids=lambda p: p.stem)
def test_bakeoff_arm_matches_the_main_config(fresh_config, monkeypatch, arm):
    base = copy.deepcopy(llm.config())
    cfg = _use(monkeypatch, arm)
    assert set(cfg["roles"]) == set(base["roles"])
    for key in ("provider", "base_url", "temperature", "response_mode", "timeout_s", "spend_cap_usd"):
        assert cfg[key] == base[key], key
    for role, rc in cfg["roles"].items():
        assert rc["max_tokens"] == base["roles"][role]["max_tokens"], role
        assert rc.get("timeout_s") == base["roles"][role].get("timeout_s"), role
    for model in {rc["model"] for rc in cfg["roles"].values()}:
        routing = cfg["provider_routing"][model]
        assert routing["only"] and set(routing["order"]) <= set(routing["only"]), model
        assert cfg["prices"][model]["input"] > 0 and cfg["prices"][model]["output"] > 0, model
        llm.omitted_params(model)                       # a bad omit name raises


def test_an_arm_without_temperature_sends_none(fresh_config, monkeypatch):
    cfg = _use(monkeypatch, paths.ROOT / "config" / "bakeoff" / "gpt-6-luna.yaml")
    client = _client([_response('{"a": 1}')])
    client.complete_json("assess", "sys", "user", "assessment", SCHEMA)
    sent = client.client.kwargs[0]
    assert sent["model"] == "openai/gpt-6-luna" and "temperature" not in sent
    assert sent["extra_body"]["provider"] == {"require_parameters": True, **cfg["provider_routing"][sent["model"]]}
    assert sent["extra_body"]["reasoning"] == {"effort": "medium"}
