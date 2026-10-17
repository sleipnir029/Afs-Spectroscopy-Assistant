"""Phase 5.0 early robustness offline tests (D-040): the off-topic short-circuit, parallel set
runs (thread-safe spend tracker, provenance lock, summary order) and LLM timeouts.

No network and no LLM calls: FakeClient-style stand-ins and a fake OpenAI SDK client.
Made-up generic enquiries only (no dev or final scenario text).
"""

from __future__ import annotations

import copy
import json
import re
import threading
import time
from types import SimpleNamespace

import httpx
import openai
import pytest
from dulwich.object_store import iter_tree_contents
from dulwich.repo import Repo
from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE, run_with

from afs_assistant import cli, llm, paths, pipeline, provenance, render, scenarios
from afs_assistant.llm import (
    FakeClient,
    LLMResult,
    OpenRouterClient,
    SpendCapExceeded,
    SpendTracker,
)
from afs_assistant.schema import Intake

OFF_ENQUIRY = "Can you recommend a good restaurant near the trade fair for our team dinner next week?"


def _slot():
    return {"value": "unknown", "basis": "unknown", "enquiry_quote": None}


OFF_INTAKE = {
    "routes": ["out_of_scope"],
    "summary": "Asks for a restaurant recommendation for a team dinner.",
    "facts_stated": [{"text": "Team dinner next week", "enquiry_quote": "our team dinner next week"}],
    "targets": [],
    "sample": {k: _slot() for k in ("physical_state", "optical_regime", "aqueous", "heterogeneous", "fluorophore")},
    "process": [],
    "customer_premises": [],
    "proposed_fiber": {"family": "none", "for_method": "none", "enquiry_quote": None},
    "unknowns": [],
}


def _off_topic_run(**kw):
    client = FakeClient({"intake": [OFF_INTAKE]})
    return pipeline.run(OFF_ENQUIRY, client, run_id="off-1", **kw), client


# ----------------------------------------------------------------- 1. off-topic short-circuit
def test_off_topic_stops_after_one_intake_call():
    result, client = _off_topic_run(external="live")       # no external step either
    assert [s["role"] for s in client.seen] == ["intake"]
    assert result.assessment is None and result.assessment_raw is None and result.report is None
    assert result.candidates == [] and result.repairs == [] and result.external is None
    assert result.off_topic["message"] == pipeline.OFF_TOPIC_MESSAGE
    assert 2 <= len(result.off_topic["examples"]) <= 3
    assert result.manifest["off_topic"] is True and result.manifest["verification"] is None
    assert result.manifest["calls"] == 1 and result.manifest["intake_attempts"] == 1


def test_off_topic_markdown_is_a_short_redirect_page():
    result, _ = _off_topic_run()
    md = render.to_markdown(result, "Test")
    assert md.startswith("# First technical assessment: Test\n\n## Answer\n")
    assert pipeline.OFF_TOPIC_MESSAGE in md
    for q in pipeline.OFF_TOPIC_EXAMPLES:
        assert f"- {q}\n" in md
    for absent in ("Expert detail", "```mermaid", "Proposal", "Verification", "$"):
        assert absent not in md


def test_off_topic_json_keeps_every_key_and_is_serializable():
    off = render.to_json(_off_topic_run()[0])
    full = render.to_json(run_with()[0])
    assert set(full) | {"off_topic"} == set(off)
    assert off["assessment"] is None and off["assessment_raw"] is None and off["verification"] is None
    assert off["screening"] == [] and off["option_costs"] == {} and off["setup_sketches"] == {}
    assert off["off_topic"]["examples"] == list(pipeline.OFF_TOPIC_EXAMPLES)
    json.loads(json.dumps(off))


def test_off_topic_provenance_files_and_message(tmp_path):
    result, _ = _off_topic_run()
    data, md = render.to_json(result), render.to_markdown(result)
    files = provenance.run_files(data, md)
    assert "off_topic.json" in files and "assessment.json" not in files and "verification.json" not in files
    message = provenance.commit_message(data)
    assert "Verifier: not run (off-topic enquiry: stopped after the intake)" in message
    Repo.init(str(tmp_path))
    assert provenance.record("off-1", files, message, repo_path=tmp_path)


def test_off_topic_examples_are_generic():
    text = pipeline.OFF_TOPIC_MESSAGE + " ".join(pipeline.OFF_TOPIC_EXAMPLES)
    assert not re.search(r"\b[DH]0\d\b", text)
    assert all(q.endswith("?") for q in pipeline.OFF_TOPIC_EXAMPLES)


def _intake(**changes):
    return Intake.model_validate({**copy.deepcopy(OFF_INTAKE), **changes})


@pytest.mark.parametrize(("intake", "removed", "enquiry", "off"), [
    (_intake(), [], OFF_ENQUIRY, True),
    (_intake(), [{"location": "intake.facts_stated[0]"}], OFF_ENQUIRY, True),        # stated facts may go
    (_intake(routes=["out_of_scope", "needs_clarification"]), [], OFF_ENQUIRY, False),
    (_intake(routes=[]), [], OFF_ENQUIRY, False),
    (_intake(routes=["in_scope"]), [], OFF_ENQUIRY, False),
    (_intake(targets=[{"variable": "x", "purpose": "y", "enquiry_quote": "restaurant"}]), [], OFF_ENQUIRY, False),
    (_intake(process=[{"aspect": "other", "value": "v", "enquiry_quote": "trade fair"}]), [], OFF_ENQUIRY, False),
    (_intake(customer_premises=[{"claim": "c", "enquiry_quote": "good restaurant"}]), [], OFF_ENQUIRY, False),
    (_intake(sample={**OFF_INTAKE["sample"], "physical_state": {"value": "liquid", "basis": "stated",
                                                                 "enquiry_quote": "dinner"}}), [], OFF_ENQUIRY, False),
    (_intake(proposed_fiber={"family": "silica", "for_method": "NIR", "enquiry_quote": "fair"}), [], OFF_ENQUIRY,
     False),
    (_intake(), [{"location": "intake.targets[0]"}], OFF_ENQUIRY, False),             # removed by the quote check
    (_intake(), [{"location": "intake.process[0]"}], OFF_ENQUIRY, False),
    (_intake(), [{"location": "intake.customer_premises[0]"}], OFF_ENQUIRY, False),
    (_intake(), [], "Is Raman fun at a team dinner?", False),                       # a named method
    (_intake(), [], "Could you measure our team dinner?", False),                    # a measurement word
    (_intake(), [], "Any fibre deals for the trade fair?", False),
])
def test_is_off_topic(intake, removed, enquiry, off):
    assert pipeline.is_off_topic(intake, removed, enquiry) is off


def _paraphrased_in_scope():
    bad = copy.deepcopy(INTAKE)          # quotes not verbatim: target and fact removed -> 2 problems
    bad["targets"][0]["enquiry_quote"] = "monitor the ethanol content"
    bad["facts_stated"][0]["enquiry_quote"] = "a clear broth"
    return bad


def _out_of_scope_with_unverified_target():
    off = copy.deepcopy(OFF_INTAKE)
    off["facts_stated"] = []
    off["targets"] = [{"variable": "ethanol", "purpose": "follow it", "enquiry_quote": "track the ethanol level"}]
    return off


def _bare_out_of_scope():
    off = copy.deepcopy(OFF_INTAKE)
    off["facts_stated"] = []
    return off


@pytest.mark.parametrize("intakes", [
    [_paraphrased_in_scope(), _bare_out_of_scope()],      # review B1: a later attempt flips to off-topic
    [_out_of_scope_with_unverified_target()] * 2,         # review B2: the target was removed by the quote check
], ids=["later-attempt-off-topic", "removed-target"])
def test_misrouted_measurement_enquiry_still_gets_the_full_assessment(intakes):
    client = FakeClient({"intake": intakes, "assess": [ASSESSMENT], "repair": [ASSESSMENT, ASSESSMENT]})
    result = pipeline.run(ENQUIRY, client, run_id="m")
    assert result.off_topic is None and result.assessment is not None
    assert "assess" in [s["role"] for s in client.seen]
    assert result.manifest["intake_attempts"] == 2


def test_vague_one_line_measurement_enquiry_stays_full():
    enquiry = "Can you help us measure something in our product?"
    client = FakeClient({"intake": [_bare_out_of_scope()] * 2, "assess": [ASSESSMENT],
                         "repair": [ASSESSMENT, ASSESSMENT]})
    result = pipeline.run(enquiry, client, run_id="v")
    assert result.off_topic is None and "assess" in [s["role"] for s in client.seen]


def test_intake_prompt_defines_out_of_scope_narrowly():
    text = pipeline.prompt("intake")
    assert "not a measurement or process-analysis question at all" in text
    assert "is NOT out_of_scope: use `needs_clarification`" in text


def test_external_replay_on_an_off_topic_run(tmp_path, capsys):
    path = tmp_path / "off.json"
    path.write_text(json.dumps(render.to_json(_off_topic_run()[0])), encoding="utf-8")
    assert cli.main(["external", "replay", str(path)]) == 2
    assert "off-topic run" in capsys.readouterr().out


def test_borderline_routes_still_get_the_full_assessment():
    borderline = copy.deepcopy(INTAKE)
    borderline["routes"] = ["out_of_scope", "needs_clarification"]
    borderline["targets"] = []
    client = FakeClient({"intake": [borderline, borderline], "assess": [ASSESSMENT]})
    result = pipeline.run(ENQUIRY, client, run_id="b")
    assert result.off_topic is None and result.assessment is not None
    assert "assess" in [s["role"] for s in client.seen]
    assert "Expert detail" in render.to_markdown(result)


def test_out_of_scope_with_a_target_still_gets_the_full_assessment():
    with_target = copy.deepcopy(INTAKE)
    with_target["routes"] = ["out_of_scope"]
    client = FakeClient({"intake": [with_target], "assess": [ASSESSMENT]})
    result = pipeline.run(ENQUIRY, client, run_id="t")
    assert result.off_topic is None and "off_topic" not in render.to_json(result)


def test_check_scripts_skip_off_topic_runs(tmp_path):
    from test_phase3 import _load_script

    result, _ = _off_topic_run()
    (tmp_path / "X.json").write_text(json.dumps(render.to_json(result)), encoding="utf-8")
    (tmp_path / "X.md").write_text(render.to_markdown(result), encoding="utf-8")
    mermaid = _load_script("check_mermaid")
    assert mermaid.blocks([tmp_path]) == []
    cost = _load_script("check_cost_class")
    assert cost.main([str(tmp_path)]) == 1        # nothing left to check (all skipped), but no crash


# ----------------------------------------------------------------- 2. parallel set runs
class _ThreadedClient:
    """Thread-safe fake: one shared real SpendTracker; every call costs `cost`. Each case's enquiry ends
    with "Case N."; its assess call first waits for `gates[N]` (if any); `barrier` holds the intake calls
    until all runs started."""

    def __init__(self, cost=0.4, run_cap=1.0, session_cap=1e9, barrier=None, gates=None):
        self.tracker = SpendTracker(run_cap, session_cap)
        self.cost, self.barrier, self.gates = cost, barrier, gates or {}

    def complete_json(self, role, system, user, schema_name, schema):
        self.tracker.check()
        case = int(re.search(r"Case (\d+)\.", user).group(1))
        if role == "intake" and self.barrier is not None:
            self.barrier.wait(timeout=10)
        if role == "assess" and case in self.gates:
            assert self.gates[case].wait(timeout=10)
        data = copy.deepcopy(INTAKE if role == "intake" else ASSESSMENT)
        result = LLMResult(data=data, model=f"fake/{role}", cost_usd=self.cost)
        self.tracker.add(role, result)
        return result


@pytest.fixture
def set_env(monkeypatch, tmp_path):
    """Patch the set runner's world: scenarios, outputs dir, client factory, provenance."""
    state = {"records": [], "client": None}
    items = [{"id": f"C{k}", "title": f"Case {k}", "enquiry": f"{ENQUIRY} Case {k}."} for k in range(1, 5)]
    monkeypatch.setattr(scenarios, "load", lambda name: list(state.get("items", items)))
    monkeypatch.setattr(paths, "OUTPUTS", tmp_path)
    monkeypatch.setattr(llm, "OpenRouterClient", lambda: state["client"])
    lock = threading.Lock()

    def fake_record(run_id, files, message, repo_path=None):
        with lock:
            state["records"].append(run_id)
        return "0" * 40

    monkeypatch.setattr(provenance, "record", fake_record)
    monkeypatch.setattr(provenance, "code_sha", lambda: "test")
    monkeypatch.setattr(provenance, "code_dirty", lambda: False)
    state["items"] = items
    return state


def test_parallel_run_order_and_per_run_cap(set_env, capsys, tmp_path, monkeypatch):
    # All four runs in flight at once (barrier). Case k's assess waits until case k+1's line was printed,
    # so the cases finish 4, 3, 2, 1 (events, no sleeps).
    printed = {k: threading.Event() for k in range(1, 5)}

    def spy_print(*args, **kwargs):
        print(*args, **kwargs)
        m = re.match(r"C(\d): ", str(args[0]) if args else "")
        if m:
            printed[int(m.group(1))].set()

    monkeypatch.setattr(cli, "print", spy_print, raising=False)
    set_env["client"] = _ThreadedClient(barrier=threading.Barrier(4), gates={k: printed[k + 1] for k in (1, 2, 3)})
    assert cli.main(["run", "--set", "dev", "--external", "off", "--workers", "4"]) == 0
    out = capsys.readouterr().out.splitlines()
    finished = [line.split(":")[0] for line in out if re.match(r"C\d: ", line)]
    assert finished == ["C4", "C3", "C2", "C1"]
    head = out.index("summary (scenario order):")
    assert [line.strip().split(":")[0] for line in out[head + 1:head + 5]] == ["C1", "C2", "C3", "C4"]
    assert out[-1] == "session cost $3.2000; failed: none"
    # Per-run cap 1.0 with 0.8 per run: a shared run counter would have tripped it; each run has its own calls.
    for k in range(1, 5):
        data = json.loads((tmp_path / "dev" / f"C{k}.json").read_text(encoding="utf-8"))
        assert data["manifest"]["cost_usd"] == pytest.approx(0.8)
        assert [c["role"] for c in data["calls"]] == ["intake", "assess"]
        assert f"Case {k}." in data["enquiry"]
    assert sorted(r.split("-")[0] for r in set_env["records"]) == ["C1", "C2", "C3", "C4"]


def test_session_cap_stops_submitting_new_cases(set_env, capsys):
    set_env["client"] = _ThreadedClient(session_cap=1.0)     # case 1 costs 0.8; case 2's assess hits the cap
    with pytest.raises(SpendCapExceeded):
        cli.main(["run", "--set", "dev", "--external", "off", "--workers", "1"])
    out = capsys.readouterr().out
    assert "C1: verification" in out and "C2: FAILED SpendCapExceeded" in out
    assert "C3: not run (stopped)" in out and "C4: not run (stopped)" in out
    assert [r.split("-")[0] for r in set_env["records"]] == ["C1"]


def test_workers_must_be_positive(set_env):
    assert cli.main(["run", "--set", "dev", "--workers", "0"]) == 2


def test_spend_tracker_run_totals_are_per_thread():
    tracker = SpendTracker(1.0, 1e9)
    seen = {}

    def one(name, cost):
        tracker.start_run()
        for _ in range(3):
            tracker.check()
            tracker.add(name, LLMResult(data={}, model="m", cost_usd=cost))
            time.sleep(0.01)
        seen[name] = (tracker.run_usd, [c["role"] for c in tracker.run_calls])

    threads = [threading.Thread(target=one, args=(f"r{k}", 0.3)) for k in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert all(usd == pytest.approx(0.9) and roles == [name] * 3 for name, (usd, roles) in seen.items())
    assert tracker.session_usd == pytest.approx(3.6) and len(tracker.calls) == 12


def test_provenance_record_is_serialized(tmp_path, monkeypatch):
    Repo.init(str(tmp_path))
    real_tree, active, peak, guard = provenance._tree, [0], [0], threading.Lock()

    def slow_tree(repo, files):
        with guard:
            active[0] += 1
            peak[0] = max(peak[0], active[0])
        time.sleep(0.05)
        try:
            return real_tree(repo, files)
        finally:
            with guard:
                active[0] -= 1

    monkeypatch.setattr(provenance, "_tree", slow_tree)
    threads = [threading.Thread(target=provenance.record, args=(f"r{k}", {"a.txt": f"{k}"}, f"run r{k}"),
                                kwargs={"repo_path": tmp_path}) for k in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert peak[0] == 1
    repo = Repo(str(tmp_path))
    head = repo[repo.refs[b"refs/heads/provenance"]]
    paths_ = {e.path.decode() for e in iter_tree_contents(repo.object_store, head.tree)}
    assert paths_ == {f"runs/r{k}/a.txt" for k in range(4)}        # no commit lost


# ----------------------------------------------------------------- 3. LLM timeouts
def _response(content='{"a": 1}'):
    usage = SimpleNamespace(prompt_tokens=10, completion_tokens=5, prompt_tokens_details=None, cost=0.001)
    return SimpleNamespace(id="r1", model="test/model", provider="p", usage=usage,
                           choices=[SimpleNamespace(message=SimpleNamespace(content=content), finish_reason="stop")])


def _timeout():
    return openai.APITimeoutError(request=httpx.Request("POST", "https://example.invalid/v1/chat/completions"))


def _connection_error():
    return openai.APIConnectionError(request=httpx.Request("POST", "https://example.invalid/v1/chat/completions"))


class _FakeOpenAI:
    """Replies or raises in order; records the request kwargs."""

    def __init__(self, script):
        self.script, self.kwargs = list(script), []
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.kwargs.append(kwargs)
        item = self.script.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def _client(script, monkeypatch) -> OpenRouterClient:
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    client = OpenRouterClient.__new__(OpenRouterClient)      # no API key or .env needed
    client.client = _FakeOpenAI(script)
    client.tracker = SpendTracker(1e9, 1e9)
    return client


SCHEMA = {"type": "object", "properties": {}}


def test_two_timeouts_fail_the_call(monkeypatch):
    client = _client([_timeout(), _timeout(), _response()], monkeypatch)
    with pytest.raises(RuntimeError, match="timed out 2 times"):
        client.complete_json("intake", "sys", "user", "intake", SCHEMA)
    assert len(client.client.kwargs) == 2                   # not a third attempt


def test_one_timeout_is_retried(monkeypatch):
    client = _client([_timeout(), _response()], monkeypatch)
    assert client.complete_json("intake", "sys", "user", "intake", SCHEMA).data == {"a": 1}
    assert len(client.client.kwargs) == 2


def test_other_transient_errors_keep_three_attempts(monkeypatch):
    client = _client([_connection_error(), _connection_error(), _response()], monkeypatch)
    assert client.complete_json("intake", "sys", "user", "intake", SCHEMA).data == {"a": 1}
    assert len(client.client.kwargs) == 3


@pytest.mark.parametrize(("role", "seconds"), [("intake", 240), ("assess", 600), ("repair", 600),
                                                ("external_queries", 180), ("external_evidence", 180)])
def test_per_role_timeout_is_passed(monkeypatch, role, seconds):
    client = _client([_response()], monkeypatch)
    client.complete_json(role, "sys", "user", role, SCHEMA)
    assert client.client.kwargs[0]["timeout"] == seconds == llm.timeout_s(role)


def test_sdk_client_has_no_retries_and_a_timeout(monkeypatch):
    import dotenv

    made = {}

    class _Recorder:
        def __init__(self, **kwargs):
            made.update(kwargs)

    monkeypatch.setattr(dotenv, "load_dotenv", lambda *a, **k: False)
    monkeypatch.setattr(openai, "OpenAI", _Recorder)
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-not-real")
    OpenRouterClient()
    assert made["max_retries"] == 0 and made["timeout"] == float(llm.config()["timeout_s"])


# ----------------------------------------------------------------- 5.0.R: wall-clock deadline, Ctrl-C cancel
class _HangingOpenAI:
    """The first `hang` calls block until `release` is set (a reply that never completes); then it replies."""

    def __init__(self, hang: int):
        self.hang, self.kwargs, self.release = hang, [], threading.Event()
        self.chat = SimpleNamespace(completions=SimpleNamespace(create=self._create))

    def _create(self, **kwargs):
        self.kwargs.append(kwargs)
        if len(self.kwargs) <= self.hang:
            self.release.wait(timeout=10)
            raise RuntimeError("released after the test")
        return _response()


@pytest.fixture
def hanging(monkeypatch):
    made = []

    def make(hang, seconds=0.2):
        monkeypatch.setattr(llm, "timeout_s", lambda role: seconds)
        client = _client([], monkeypatch)
        client.client = _HangingOpenAI(hang)
        made.append(client.client)
        return client

    yield make
    for fake in made:
        fake.release.set()


def test_wall_clock_deadline_counts_as_a_timeout_and_is_retried_once(hanging):
    client = hanging(hang=1)
    started = time.monotonic()
    assert client.complete_json("intake", "sys", "user", "intake", SCHEMA).data == {"a": 1}
    assert time.monotonic() - started < 3
    assert len(client.client.kwargs) == 2
    assert [c["role"] for c in client.tracker.calls] == ["intake:timeout", "intake"]


def test_two_wall_clock_deadlines_fail_the_call(hanging):
    client = hanging(hang=2)
    with pytest.raises(RuntimeError, match="timed out 2 times"):
        client.complete_json("intake", "sys", "user", "intake", SCHEMA)
    assert len(client.client.kwargs) == 2


def test_cancel_stops_a_waiting_call_at_once(hanging):
    client = hanging(hang=1, seconds=30)
    threading.Timer(0.2, client.tracker.cancel.set).start()
    started = time.monotonic()
    with pytest.raises(llm.RunCancelled):
        client.complete_json("intake", "sys", "user", "intake", SCHEMA)
    assert time.monotonic() - started < 3 and len(client.client.kwargs) == 1


def test_tracker_check_raises_once_cancelled():
    tracker = SpendTracker(1e9, 1e9)
    tracker.check()
    tracker.cancel.set()
    with pytest.raises(llm.RunCancelled):
        tracker.check()


class _BlockingClient:
    """Each started case blocks in its intake call until the tracker is cancelled, then checks again."""

    def __init__(self):
        self.tracker = SpendTracker(1e9, 1e9)
        self.started, self.ended, self.lock = [], [], threading.Lock()

    def complete_json(self, role, system, user, schema_name, schema):
        case = re.search(r"Case (\d+)\.", user).group(1)
        with self.lock:
            self.started.append(case)
        try:
            self.tracker.check()
            self.tracker.cancel.wait(timeout=10)
            self.tracker.check()
        except Exception as exc:
            with self.lock:
                self.ended.append(type(exc).__name__)
            raise
        raise AssertionError("not cancelled")


def test_ctrl_c_cancels_queued_and_running_cases(set_env, monkeypatch, capsys):
    import concurrent.futures

    client = _BlockingClient()
    set_env["client"] = client

    def interrupted_wait(fs, timeout=None, return_when=None):
        deadline = time.monotonic() + 5
        while len(client.started) < 2 and time.monotonic() < deadline:   # both workers are in a call
            time.sleep(0.01)
        raise KeyboardInterrupt

    monkeypatch.setattr(concurrent.futures, "wait", interrupted_wait)
    started = time.monotonic()
    with pytest.raises(KeyboardInterrupt):
        cli.main(["run", "--set", "dev", "--external", "off", "--workers", "2"])
    assert time.monotonic() - started < 3
    assert client.tracker.cancel.is_set()
    deadline = time.monotonic() + 5
    while len(client.ended) < 2 and time.monotonic() < deadline:
        time.sleep(0.01)
    assert sorted(client.started) == ["1", "2"]                     # cases 3 and 4 never started
    assert client.ended == ["RunCancelled", "RunCancelled"]
    assert set_env["records"] == []
    assert "interrupted" in capsys.readouterr().out
