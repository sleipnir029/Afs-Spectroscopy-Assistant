"""Phase 5.6''': the web UI (FastAPI + Jinja2 + htmx). Offline: saved runs and FakeClient stubs only."""

from __future__ import annotations

import json
import shutil
import threading
import time

import pytest
from fastapi.testclient import TestClient
from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE

from afs_assistant import cli, kb_check, paths, provenance
from afs_assistant.fibers import METHOD_RANGES_UM
from afs_assistant.llm import FakeClient
from afs_assistant.ui import diagrams, server, view

SAVED = "D03"                                     # a dev run with external evidence and proposal support
HX = {"HX-Request": "true"}
OFF_TOPIC_RUN = {"run_id": "adhoc-off", "enquiry": "Which pizza topping sells best on Fridays?",
                 "intake": {"routes": ["out_of_scope"], "summary": "Asks about pizza sales."}}


@pytest.fixture
def outputs(tmp_path):
    (tmp_path / "dev").mkdir()
    for suffix in (".json", ".md"):
        shutil.copy(paths.OUTPUTS / "dev" / f"{SAVED}{suffix}", tmp_path / "dev" / f"{SAVED}{suffix}")
    (tmp_path / "dev" / "X90.json").write_text(json.dumps(OFF_TOPIC_RUN), encoding="utf-8")
    return tmp_path


@pytest.fixture
def no_provenance(monkeypatch):
    monkeypatch.setattr(provenance, "record", lambda run_id, files, msg: "c0ffee")
    monkeypatch.setattr(provenance, "code_sha", lambda: "abc")
    monkeypatch.setattr(provenance, "code_dirty", lambda: False)


def fake_factory(seen: list | None = None):
    def make():
        # enough responses for an intake retry and two repair rounds (the stub does not fit every enquiry)
        client = FakeClient({"intake": [INTAKE, INTAKE], "assess": [ASSESSMENT], "repair": [ASSESSMENT, ASSESSMENT]})
        if seen is not None:
            seen.append(client)
        return client
    return make


def app_client(outputs, factory=None):
    app = server.create_app(outputs, client_factory=factory or fake_factory(), external="off")
    return TestClient(app), app


def wait_job(client, jid, timeout=20.0):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        snap = client.get(f"/api/jobs/{jid}").json()
        if snap["state"] != "running":
            return snap
        time.sleep(0.05)
    raise AssertionError("job did not finish")


# --------------------------------------------------------------------------------- saved runs
def test_list_runs_and_start_page(outputs):
    client, _ = app_client(outputs)
    runs = {r["id"]: r for r in client.get("/api/runs").json()}
    assert runs[f"dev-{SAVED}"]["title"] == "A clear whey stream before concentration"
    assert runs[f"dev-{SAVED}"]["status"] == "Provisional feasibility assessment"
    assert runs["dev-X90"]["status"] == "Off topic"
    html = client.get("/").text
    assert "Paste a customer enquiry" in html and f'href="/runs/dev-{SAVED}"' in html
    assert client.get("/?q=hello").text.count(">hello</textarea>") == 1


def test_answer_page_order_and_content(outputs):
    client, _ = app_client(outputs)
    r = client.get(f"/runs/dev-{SAVED}")
    assert r.status_code == 200
    html = r.text
    order = ["Customer enquiry", ">Status<", ">Answer<", ">Proposal<", "fig-setup", "fig-spectral",
             "Options compared", "Open questions", "Answer and re-assess", ">Parameters<", ">Premise check<",
             ">Risks<", ">Test plan<", ">Literature<", ">Verification<", "How this answer was made"]
    positions = [html.index(s) for s in order]
    assert positions == sorted(positions)
    assert "external, not AFS material" in html
    assert "mermaid" not in html.lower()             # the figures are server-drawn SVG
    assert 'class="best"' in html and "proposed" in html


def test_api_run_view(outputs):
    client, _ = app_client(outputs)
    v = client.get(f"/api/runs/dev-{SAVED}").json()
    assert v["proposal"]["best"] == {"id": "O2", "tier": "Recommended"}
    assert v["proposal"]["confidence"]["level"] == "Medium"
    supplied = [c for c in v["citations"].values() if c["kind"] == "supplied"]
    external = [c for c in v["citations"].values() if c["kind"] == "external"]
    assert supplied and all(c["verified"] for c in supplied)
    assert {c["label"] for c in external} >= {"E01 ¶12"}
    assert [c["label"] for c in (v["citations"][x] for x in v["proposal"]["external_support"])] == ["E01 ¶12"]
    assert [s["label"] for s in v["made"]["steps"]] == [label for _, label, _ in view.STEPS]


def test_citation_panel_supplied_and_external(outputs):
    client, _ = app_client(outputs)
    v = client.get(f"/api/runs/dev-{SAVED}").json()
    sid = next(k for k, c in v["citations"].items() if c["kind"] == "supplied")
    xid = next(k for k, c in v["citations"].items() if c["kind"] == "external")
    frag = client.get(f"/runs/dev-{SAVED}/cite/{sid}", headers=HX).text
    assert "<html" not in frag and "verified quote" in frag
    assert f"<mark>{v['citations'][sid]['quote']}</mark>" in frag.replace("&#39;", "'").replace("&quot;", '"')
    full = client.get(f"/runs/dev-{SAVED}/cite/{sid}").text
    assert "<html" in full and "Back to the assessment" in full
    ext = client.get(f"/runs/dev-{SAVED}/cite/{xid}", headers=HX).text
    assert "external, not AFS material" in ext and "doi:" in ext and "licence" in ext.lower()
    assert "<mark>" not in ext                        # stored quote only, no page text
    assert client.get(f"/runs/dev-{SAVED}/cite/s9999").status_code == 404


def test_source_context_locates_the_quote():
    quote = METHOD_RANGES_UM["NIR"]["basis"]          # "NIR spectra (780-2500 nm)", on S01 p.10
    src = view.source("S01", 10, quote)
    assert src["verified"] and src["match"] == quote and src["before"] and src["after"]
    assert view.source("S01", 999, quote) is None


def test_downloads(outputs):
    client, _ = app_client(outputs)
    md = client.get(f"/runs/dev-{SAVED}.md")
    js = client.get(f"/runs/dev-{SAVED}.json")
    assert md.text == (outputs / "dev" / f"{SAVED}.md").read_text(encoding="utf-8")
    assert js.json()["run_id"] == json.loads((outputs / "dev" / f"{SAVED}.json").read_text())["run_id"]
    assert "attachment" in md.headers["content-disposition"]


@pytest.mark.parametrize("rid", ["dev-..", "nope-D03", "dev-D03%2F..%2F..", "Dev-D03", "dev"])
def test_unknown_or_unsafe_run_ids(outputs, rid):
    client, _ = app_client(outputs)
    assert client.get(f"/runs/{rid}").status_code == 404
    assert client.get(f"/api/runs/{rid}").status_code == 404


# --------------------------------------------------------------------------------- off topic
def test_off_topic_display(outputs):
    client, _ = app_client(outputs)
    v = client.get("/api/runs/dev-X90").json()
    assert v["off_topic"]["message"] == view.OFF_TOPIC_MESSAGE
    assert len(v["off_topic"]["examples"]) == 3
    html = client.get("/runs/dev-X90").text
    assert view.OFF_TOPIC_MESSAGE in html and "Options compared" not in html
    assert html.count('href="/?q=') == 3


def test_off_topic_wording_from_the_pipeline_wins():
    data = {**OFF_TOPIC_RUN, "intake": {"routes": ["in_scope"]}, "assessment": {"x": 1},
            "off_topic": {"message": "Polite redirect.", "examples": ["One?", "Two?"]}}
    v = view.build(data)
    assert v["off_topic"] == {"message": "Polite redirect.", "examples": ["One?", "Two?"]}


# --------------------------------------------------------------------------------- live path (stubbed)
def test_assess_runs_in_background_with_progress(outputs, no_provenance):
    client, _ = app_client(outputs)
    r = client.post("/assess", data={"enquiry": ENQUIRY}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/jobs/")
    jid = r.headers["location"].rsplit("/", 1)[1]
    snap = wait_job(client, jid)
    assert snap["state"] == "done", snap["error"]
    states = {s["key"]: s["state"] for s in snap["steps"]}
    assert states == {"intake": "done", "screen": "done", "assess": "done", "verify": "done", "external": "skipped"}
    rid = snap["result"]
    assert rid.startswith("ui-adhoc-") and (outputs / "ui" / f"{rid[3:]}.json").exists()
    plain = client.get(f"/jobs/{jid}", follow_redirects=False)
    assert plain.status_code == 303 and plain.headers["location"] == f"/runs/{rid}"
    polled = client.get(f"/jobs/{jid}", headers=HX)
    assert polled.headers["HX-Redirect"] == f"/runs/{rid}"
    assert client.get(f"/runs/{rid}").status_code == 200
    assert any(x["id"] == rid for x in client.get("/api/runs").json())


def test_running_page_polls_until_done(outputs, no_provenance):
    gate = threading.Event()

    class Slow(FakeClient):
        def complete_json(self, role, *args, **kwargs):
            if role == "assess":
                gate.wait(10)
            return super().complete_json(role, *args, **kwargs)

    client, _ = app_client(outputs, lambda: Slow({"intake": [INTAKE], "assess": [ASSESSMENT]}))
    jid = client.post("/assess", data={"enquiry": ENQUIRY}, follow_redirects=False).headers["location"].split("/")[-1]
    deadline = time.monotonic() + 5
    while client.get(f"/api/jobs/{jid}").json()["steps"][2]["state"] != "running":
        assert time.monotonic() < deadline
        time.sleep(0.02)
    page = client.get(f"/jobs/{jid}").text
    assert 'hx-trigger="every 1s"' in page and "Reading enquiry" in page and "Searching literature" in page
    assert client.post("/assess", data={"enquiry": ENQUIRY}).status_code == 409     # one run at a time
    gate.set()
    assert wait_job(client, jid)["state"] == "done"


def test_failed_run_stops_polling(outputs, no_provenance):
    client, _ = app_client(outputs, lambda: FakeClient({}))          # no queued response: intake raises
    jid = client.post("/assess", data={"enquiry": ENQUIRY}, follow_redirects=False).headers["location"].split("/")[-1]
    snap = wait_job(client, jid)
    assert snap["state"] == "failed" and "AssertionError" in snap["error"]
    r = client.get(f"/jobs/{jid}", headers=HX)
    assert r.status_code == 286 and "The run failed" in r.text


def test_empty_enquiry_is_rejected(outputs):
    client, _ = app_client(outputs)
    assert client.post("/assess", data={"enquiry": "  "}).status_code == 422


def test_clarify_appends_answers_and_compares(outputs, no_provenance):
    seen: list = []
    client, _ = app_client(outputs, fake_factory(seen))
    v = client.get(f"/api/runs/dev-{SAVED}").json()
    q1 = v["questions"][0]
    r = client.post(f"/runs/dev-{SAVED}/clarify", data={f"answer_{q1['id']}": "Between 4 and 8 g/L."},
                    follow_redirects=False)
    jid = r.headers["location"].split("/")[-1]
    snap = wait_job(client, jid)
    assert snap["state"] == "done" and snap["parent"] == f"dev-{SAVED}"
    intake_prompt = seen[0].seen[0]["user"]
    assert v["enquiry"] in intake_prompt and "Answer: Between 4 and 8 g/L." in intake_prompt
    assert q1["question"] in intake_prompt
    target = client.get(f"/jobs/{jid}", follow_redirects=False).headers["location"]
    assert target == f"/runs/{snap['result']}?compare=dev-{SAVED}"
    html = client.get(target).text
    assert "Re-assessed with the customer" in html and "Before" in html and "After" in html


def test_clarify_without_answers_starts_nothing(outputs):
    client, app = app_client(outputs)
    r = client.post(f"/runs/dev-{SAVED}/clarify", data={}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].endswith("#questions")
    assert app.state.jobs.jobs == {}


def test_progress_client_marks_steps():
    job = server.Job("j", "e")
    proxy = server.ProgressClient(FakeClient({"intake": [{}], "assess": [{}], "external_queries": [{}]}), job)
    assert proxy.tracker is not None                     # the pipeline's spend tracker comes through
    proxy.complete_json("intake", "", "", "", {})
    assert [s["state"] for s in job.snapshot()["steps"]] == ["running", "pending", "pending", "pending", "pending"]
    proxy.complete_json("assess", "", "", "", {})
    assert [s["state"] for s in job.snapshot()["steps"]] == ["done", "done", "done", "running", "pending"]
    proxy.complete_json("external_queries", "", "", "", {})
    job.finish("dev-x", {"intake": 1.0, "assess": 2.0, "repair": 0.5, "external": 3.0})
    snap = job.snapshot()
    assert [s["seconds"] for s in snap["steps"]] == [1.0, 0.0, 2.5, 0.0, 3.0]
    assert all(s["state"] == "done" for s in snap["steps"])


# --------------------------------------------------------------------------------- figures, lint
def test_figures_use_only_sourced_numbers(outputs):
    v = server.Store(outputs).view(f"dev-{SAVED}")
    svg = v["figures"]["spectral"]["wide"]
    for m, r in METHOD_RANGES_UM.items():
        lo, hi = r["range_um"]
        assert diagrams.range_text(lo, hi) in svg, m
    assert "sp-proposed" in svg                                    # MIR of the proposed option highlighted
    setup = v["figures"]["setup"]["narrow"]
    assert "MIR, ATR probe" in setup and "dg-aux" in setup and "Auxiliary sensor" in setup
    assert v["figures"]["params"]["wide"].count("<rect") == len(v["parameters"]) + len(
        {p["measured_by"].split(" (")[0] for p in v["parameters"]})


def test_ui_code_has_no_case_ids():
    ui = paths.ROOT / "src" / "afs_assistant" / "ui"
    hits = [f"{f.relative_to(ui)}:{i}"
            for f in ui.rglob("*") if f.is_file() and f.suffix in {".py", ".html", ".css", ".js"}
            and "vendor" not in f.parts and "__pycache__" not in f.parts
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1) if kb_check.CASE_ID.search(line)]
    assert hits == []


def test_cli_has_ui_command(monkeypatch):
    called = {}
    monkeypatch.setattr(server, "serve", lambda host, port, external: called.update(host=host, port=port, ext=external))
    assert cli.main(["ui", "--port", "9999", "--external", "off"]) == 0
    assert called == {"host": "127.0.0.1", "port": 9999, "ext": "off"}
