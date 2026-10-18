"""Phase 5.6'''' web UI, direction A "Answer + Ask" (FastAPI + Jinja2 + htmx). Offline: saved runs and stubs."""

from __future__ import annotations

import copy
import json
import re
import shutil
import threading
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from test_phase2 import ASSESSMENT, ENQUIRY, INTAKE

from afs_assistant import cli, kb, kb_check, paths, provenance
from afs_assistant.llm import FakeClient
from afs_assistant.pipeline import OFF_TOPIC_EXAMPLES
from afs_assistant.ui import diagrams, server, view

SAVED = "D03"                                     # a dev run with external evidence and proposal support
FIXTURE = Path(__file__).parent / "fixtures" / "ui"  # frozen copy, so a live re-run does not change the expected text
DEV = sorted(p.stem for p in (paths.OUTPUTS / "dev").glob("*.json"))
BASE = "http://127.0.0.1:8765"
HX = {"HX-Request": "true"}
OFF_TOPIC_RUN = {"run_id": "adhoc-off", "enquiry": "Which pizza topping sells best on Fridays?",
                 "intake": {"routes": ["out_of_scope"], "summary": "Asks about pizza sales."}, "assessment": None,
                 "off_topic": {"message": "Polite redirect line.", "examples": ["Example one?", "Example two?"]}}
INCOMPLETE_RUN = {"run_id": "adhoc-cut", "enquiry": "Follow sugar in juice.", "intake": {"routes": ["in_scope"]},
                  "assessment": None}


@pytest.fixture
def outputs(tmp_path):
    (tmp_path / "dev").mkdir()
    for suffix in (".json", ".md"):
        shutil.copy(FIXTURE / f"{SAVED}{suffix}", tmp_path / "dev" / f"{SAVED}{suffix}")
    (tmp_path / "dev" / "X90.json").write_text(json.dumps(OFF_TOPIC_RUN), encoding="utf-8")
    (tmp_path / "dev" / "X91.json").write_text(json.dumps(INCOMPLETE_RUN), encoding="utf-8")
    return tmp_path


@pytest.fixture
def no_provenance(monkeypatch):
    monkeypatch.setattr(provenance, "record", lambda run_id, files, msg: "c0ffee")
    monkeypatch.setattr(provenance, "code_sha", lambda: "abc")
    monkeypatch.setattr(provenance, "code_dirty", lambda: False)


def fake_factory(seen: list | None = None, cls=FakeClient):
    def make():
        # enough responses for an intake retry and two repair rounds (the stub does not fit every enquiry)
        client = cls({"intake": [INTAKE, INTAKE], "assess": [ASSESSMENT], "repair": [ASSESSMENT, ASSESSMENT]})
        if seen is not None:
            seen.append(client)
        return client
    return make


def app_client(outputs, factory=None):
    app = server.create_app(outputs, client_factory=factory or fake_factory(), external="off")
    return TestClient(app, base_url=BASE), app


def wait_job(client, jid, timeout=20.0):
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        snap = client.get(f"/api/jobs/{jid}").json()
        if snap["state"] != "running":
            return snap
        time.sleep(0.05)
    raise AssertionError("job did not finish")


def start_job(client, data, url="/assess"):
    r = client.post(url, data=data, follow_redirects=False)
    assert r.status_code == 303, r.text
    return r.headers["location"].rsplit("/", 1)[1]


# --------------------------------------------------------------------------------- start, list
def test_start_page_and_examples(outputs):
    client, _ = app_client(outputs)
    html = client.get("/").text
    assert "What do you want to measure?" in html and "Get assessment" in html
    assert all(e.split(",")[0] in html for e in OFF_TOPIC_EXAMPLES)
    assert f'href="/runs/dev-{SAVED}"' in html and "A clear whey stream before concentration" in html
    assert "dev-D03</" not in html and "deepseek" not in html          # titles only on the start page
    assert client.get("/?q=hello").text.count(">hello</textarea>") == 1


def test_list_runs_holds_finished_answers_only(outputs):
    client, _ = app_client(outputs)
    runs = {r["id"]: r for r in client.get("/api/runs").json()}
    assert runs[f"dev-{SAVED}"]["status"] == "Provisional feasibility assessment"
    assert "dev-X90" not in runs and "dev-X91" not in runs           # off-topic / incomplete: by URL only
    assert view.status_label(OFF_TOPIC_RUN) == "Off topic" and view.status_label(INCOMPLETE_RUN) == "Incomplete run"
    assert client.get("/runs/dev-X90").status_code == 200 and client.get("/runs/dev-X91").status_code == 200


# --------------------------------------------------------------------------------- answer turn
def test_answer_turn_order_and_option_switch(outputs):
    client, _ = app_client(outputs)
    html = client.get(f"/runs/dev-{SAVED}").text
    order = ["Your question", "Our recommendation", "How it would be set up", 'role="tablist"',
             "Help us sharpen this", "What to measure and how", ">Risks<", "First feasibility test",
             ">Literature", "How this answer was made", "Technical detail", "Copy as customer reply",
             'name="followup"']
    positions = [html.index(s) for s in order]
    assert positions == sorted(positions)
    v = client.get(f"/api/runs/dev-{SAVED}").json()
    assert v["recommendation"]["headline"] == "Start with an MIR ATR probe."
    for o in v["options"]:
        assert f'id="opt-{o["id"]}"' in html and f'aria-controls="opt-{o["id"]}"' in html
        assert "fig-schematic" in o["figure"]["wide"] and "fig-setup" in o["figure"]["narrow"]
    assert re.search(r'aria-controls="opt-O2" aria-selected="true"', html)
    assert html.count("data-hidden") == len(v["options"]) - 1
    assert "mermaid" not in html.lower()


@pytest.mark.parametrize("stem", DEV)
def test_every_saved_run_renders_and_every_citation_opens(stem):
    client, _ = app_client(paths.OUTPUTS)
    assert client.get(f"/runs/dev-{stem}").status_code == 200
    v = client.get(f"/api/runs/dev-{stem}").json()
    ids = list(v["citations"])
    assert ids, stem
    assert [i for i in ids if i.startswith("s")] == [f"s{k}" for k in range(1, 1 + sum(i[0] == "s" for i in ids))]
    for cid in ids:
        r = client.get(f"/runs/dev-{stem}/cite/{cid}", headers=HX)
        expected = "Table 1 rows" if cid.startswith("t") else "Verified quote"
        assert r.status_code == 200 and expected in r.text, (stem, cid)


@pytest.mark.parametrize("stem", DEV)
def test_setup_diagrams_show_full_text(stem):
    """No node text is cut: every option's wide and narrow setup figure is free of an ellipsis, and every
    node carries its full text as a <title>."""
    v = server.Store(paths.OUTPUTS).view(f"dev-{stem}")
    for o in v["options"]:
        for key in ("wide", "narrow"):
            svg = o["figure"][key]
            assert "…" not in svg, (stem, o["id"], key)
            assert svg.count('<g class="sn') == svg.count("<title>"), (stem, o["id"], key)


@pytest.mark.parametrize("stem", DEV)
def test_main_view_shows_no_internal_ids(stem):
    client, _ = app_client(paths.OUTPUTS)
    html = client.get(f"/runs/dev-{stem}").text
    main = html[:html.index('<section class="more"')]
    main = re.sub(r"<svg.*?</svg>", " ", main, flags=re.DOTALL)
    main = re.sub(r"<title>.*?</title>|<script.*?</script>|<[^>]+>", " ", main, flags=re.DOTALL)
    assert not re.search(r"\bO\d\b|\bP\d+\b|\bQ\d+\b", main), re.findall(r".{40}\b[OPQ]\d+\b.{20}", main)[:3]


def test_citation_panel_supplied_and_external(outputs):
    client, _ = app_client(outputs)
    v = client.get(f"/api/runs/dev-{SAVED}").json()
    sid = next(k for k, c in v["citations"].items() if c["kind"] == "supplied")
    eid = next(k for k, c in v["citations"].items() if c["kind"] == "external")
    frag = client.get(f"/runs/dev-{SAVED}/cite/{sid}", headers=HX).text
    assert "<html" not in frag and "<mark>" in frag
    assert client.get(f"/runs/dev-{SAVED}/cite/{sid}").text.count("Back to the answer") == 1
    ext = client.get(f"/runs/dev-{SAVED}/cite/{eid}", headers=HX).text
    assert "external, not AFS material" in ext and "doi:" in ext and "<mark>" not in ext
    assert client.get(f"/runs/dev-{SAVED}/cite/s9999").status_code == 404


def test_tag_tooltip_shows_quote_and_says_not_verified(outputs):
    data = json.loads((outputs / "dev" / f"{SAVED}.json").read_text())
    v = view.build(data, "", "dev-x")
    assert all(c["verified"] for c in v["citations"].values() if c["kind"] != "table")
    data["verification"]["citations"] = []                        # nothing on record as verified
    client, _ = app_client(outputs)
    (outputs / "dev" / "X92.json").write_text(json.dumps(data), encoding="utf-8")
    html = client.get("/runs/dev-X92").text
    supplied = re.findall(r'<a class="tag tag-supplied"[^>]*title="([^"]*)"', html)
    assert supplied and all(t.endswith("not verified: open the quote") for t in supplied)
    good = client.get(f"/runs/dev-{SAVED}").text
    assert "open the verified quote" in good and "not verified" not in good


def test_source_context_locates_the_quote():
    quote = "NIR spectra (780-2500 nm)"
    src = view.source("S01", 10, quote)
    assert src["verified"] and src["match"] == quote and src["before"] and src["after"]
    assert view.source("S01", 999, quote) is None


def test_downloads(outputs):
    client, _ = app_client(outputs)
    md = client.get(f"/runs/dev-{SAVED}.md")
    assert md.text == (outputs / "dev" / f"{SAVED}.md").read_text(encoding="utf-8")
    assert "attachment" in md.headers["content-disposition"]
    assert client.get(f"/runs/dev-{SAVED}.json").json()["run_id"]
    assert client.get("/runs/dev-X90.md").status_code == 404        # no Markdown: no link either
    assert 'href="/runs/dev-X90.md"' not in client.get("/runs/dev-X90").text


@pytest.mark.parametrize("rid", ["dev-..", "nope-D03", "dev-D03%2F..%2F..", "Dev-D03", "dev"])
def test_unknown_or_unsafe_run_ids(outputs, rid):
    client, _ = app_client(outputs)
    assert client.get(f"/runs/{rid}").status_code == 404
    assert client.get(f"/api/runs/{rid}").status_code == 404


# --------------------------------------------------------------------------------- off topic, incomplete
def test_off_topic_turn_uses_the_run_wording(outputs):
    client, _ = app_client(outputs)
    html = client.get("/runs/dev-X90").text
    assert "Polite redirect line." in html and html.count('href="/?q=Example') == 2
    assert "Our recommendation" not in html and 'name="followup"' not in html


def test_incomplete_run_is_not_called_off_topic(outputs):
    client, _ = app_client(outputs)
    html = client.get("/runs/dev-X91").text
    assert "Incomplete run" in html and "Off topic" not in html


# --------------------------------------------------------------------------------- security
def test_xss_in_model_text_and_urls_is_inert(outputs):
    data = json.loads((outputs / "dev" / f"{SAVED}.json").read_text())
    data["assessment"]["brief_answer"] = "<script>alert(1)</script> Use NIR."
    for s in data["external"]["sources"]:
        s["doi"], s["url"] = None, "javascript:alert(1)"
    (outputs / "dev" / "X93.json").write_text(json.dumps(data), encoding="utf-8")
    client, _ = app_client(outputs)
    html = client.get("/runs/dev-X93").text
    assert "<script>alert(1)" not in html and "&lt;script&gt;alert(1)" in html
    assert 'href="javascript:' not in html.lower()
    v = client.get("/api/runs/dev-X93").json()
    eid = next(k for k, c in v["citations"].items() if c["kind"] == "external")
    panel = client.get(f"/runs/dev-X93/cite/{eid}", headers=HX).text
    assert 'href="javascript:' not in panel.lower() and "javascript:alert(1)" in panel     # shown as text only


def test_foreign_host_is_refused(outputs):
    client, _ = app_client(outputs)
    assert client.get("/", headers={"host": "evil.example"}).status_code == 400
    assert client.get("/", headers={"host": "localhost:8765"}).status_code == 200


@pytest.mark.parametrize("header", [{"origin": "http://evil.example"}, {"referer": "http://evil.example/x"},
                                    {"origin": "null"}, {"origin": "http://localhost:3000"},
                                    {"origin": "http://127.0.0.1:1"}, {"referer": "http://127.0.0.1:9999/runs"}])
def test_cross_origin_post_is_refused(outputs, header):
    client, app = app_client(outputs)
    r = client.post("/assess", data={"enquiry": ENQUIRY}, headers=header, follow_redirects=False)
    assert r.status_code == 403 and app.state.jobs.jobs == {}
    r = client.post(f"/runs/dev-{SAVED}/clarify", data={"followup": "x"}, headers=header, follow_redirects=False)
    assert r.status_code == 403 and app.state.jobs.jobs == {}


def test_same_origin_post_is_accepted(outputs, no_provenance):
    client, _ = app_client(outputs)
    r = client.post("/assess", data={"enquiry": ENQUIRY}, headers={"origin": BASE}, follow_redirects=False)
    assert r.status_code == 303
    wait_job(client, r.headers["location"].rsplit("/", 1)[1])


# --------------------------------------------------------------------------------- live path (stubbed)
def test_assess_runs_in_background_with_progress(outputs, no_provenance):
    client, _ = app_client(outputs)
    jid = start_job(client, {"enquiry": ENQUIRY})
    snap = wait_job(client, jid)
    assert snap["state"] == "done", snap["error"]
    states = {s["key"]: s["state"] for s in snap["steps"]}
    assert states == {"intake": "done", "screen": "done", "assess": "done", "verify": "done", "external": "skipped"}
    assert snap["understood"] == INTAKE["summary"]
    rid = snap["result"]
    assert rid.startswith("ui-adhoc-") and (outputs / "ui" / f"{rid[3:]}.json").exists()
    plain = client.get(f"/jobs/{jid}", follow_redirects=False)
    assert plain.status_code == 303 and plain.headers["location"] == f"/runs/{rid}"
    assert client.get(f"/jobs/{jid}", headers=HX).headers["HX-Redirect"] == f"/runs/{rid}"
    assert client.get(f"/runs/{rid}").status_code == 200


def test_running_page_polls_and_can_be_stopped(outputs, no_provenance):
    gate = threading.Event()

    class Slow(FakeClient):
        def complete_json(self, role, *args, **kwargs):
            if role == "assess":
                gate.wait(10)
            return super().complete_json(role, *args, **kwargs)

    client, _ = app_client(outputs, fake_factory(cls=Slow))
    jid = start_job(client, {"enquiry": ENQUIRY})
    deadline = time.monotonic() + 5
    while client.get(f"/api/jobs/{jid}").json()["steps"][2]["state"] != "running":
        assert time.monotonic() < deadline
        time.sleep(0.02)
    page = client.get(f"/jobs/{jid}").text
    assert 'hx-trigger="every 1s"' in page and "usually a few minutes" in page and ">Stop<" in page
    assert ENQUIRY in page and "Follow ethanol" in page                    # question turn + what we understood
    assert 'id="ask" type="text" disabled' in page
    assert "What is happening" in page and "Waiting for the model to write the assessment" in page
    assert "Screened " in page                                              # activity feed from the pipeline
    assert client.post("/assess", data={"enquiry": ENQUIRY}).status_code == 409     # one run at a time
    assert client.post(f"/jobs/{jid}/stop", follow_redirects=False).status_code == 303
    gate.set()
    snap = wait_job(client, jid)
    assert snap["state"] == "stopped" and snap["result"] is None
    assert client.get(f"/jobs/{jid}", headers=HX).status_code == 286


def test_activity_feed_tells_what_happened(outputs, no_provenance):
    client, app = app_client(outputs)
    jid = start_job(client, {"enquiry": ENQUIRY})
    assert wait_job(client, jid)["state"] == "done"
    notes = [text for _, text in app.state.jobs.jobs[jid].notes]
    assert notes[0].startswith("The model answered (read the enquiry)")
    assert any(n.startswith("Understood: target ") for n in notes)
    assert any(n.startswith("Screened ") and "against the AFS rules" in n for n in notes)
    assert any(n.startswith("Checked ") and "verified (quote and page scope)" in n for n in notes)
    snap = client.get(f"/api/jobs/{jid}").json()
    assert 0 < len(snap["feed"]) <= server.FEED_SHOW and snap["waiting"] is None
    assert snap["feed"][-1]["text"] == notes[-1] and re.fullmatch(r"\d+:\d\d", snap["feed"][-1]["at"])


def test_activity_note_without_a_sink_is_a_no_op():
    from afs_assistant import activity

    activity.note("nobody listens")                      # CLI and set runs: nothing happens
    seen = []
    with activity.sink(seen.append):
        activity.note("  two   words ")
        with activity.sink(lambda text: 1 / 0):          # a broken display never stops a run
            activity.note("ignored")
        activity.note("back")
    activity.note("after")
    assert seen == ["two words", "back"]


def test_failed_run_stops_polling(outputs, no_provenance):
    client, _ = app_client(outputs, lambda: FakeClient({}))          # no queued response: intake raises
    snap = wait_job(client, start_job(client, {"enquiry": ENQUIRY}))
    assert snap["state"] == "failed" and "AssertionError" in snap["error"]


def test_unknown_job_stops_polling(outputs):
    client, _ = app_client(outputs)
    assert client.get("/jobs/nope", headers=HX).status_code == 286          # e.g. after a server restart
    assert client.get("/jobs/nope").status_code == 404


def test_empty_enquiry_is_rejected(outputs):
    client, _ = app_client(outputs)
    assert client.post("/assess", data={"enquiry": "  "}).status_code == 422


def test_overlong_texts_are_refused_with_a_message(outputs):
    client, app = app_client(outputs)
    long = "x" * (server.MAX_CHARS + 1)
    r = client.post("/assess", data={"enquiry": long})
    assert r.status_code == 422 and "characters or fewer" in r.text
    r = client.post(f"/runs/dev-{SAVED}/clarify", data={"followup": long})
    assert r.status_code == 422 and "characters or fewer" in r.text and app.state.jobs.jobs == {}
    assert f'maxlength="{server.MAX_CHARS}"' in client.get("/").text
    assert client.get(f"/runs/dev-{SAVED}").text.count(f'maxlength="{server.MAX_CHARS}"') >= 2


def test_follow_up_appends_a_turn_with_what_changed(outputs, no_provenance):
    seen: list = []
    client, _ = app_client(outputs, fake_factory(seen))
    v = client.get(f"/api/runs/dev-{SAVED}").json()
    q1 = v["top_questions"][0]
    jid = start_job(client, {f"answer_{q1['id']}": "Between 4 and 8 g/L.", "followup": "The line runs at 50 C."},
                    f"/runs/dev-{SAVED}/clarify")
    snap = wait_job(client, jid)
    assert snap["state"] == "done" and snap["parent"] == f"dev-{SAVED}"
    prompt_text = seen[0].seen[0]["user"]
    assert v["enquiry"] in prompt_text and "Answer: Between 4 and 8 g/L." in prompt_text
    assert "Additional detail: The line runs at 50 C." in prompt_text
    rid = snap["result"]
    html = client.get(f"/runs/{rid}").text
    assert "Your follow-up" in html and "The line runs at 50 C." in html and "What changed" in html
    changed = html[html.index("What changed"):html.index("Our recommendation")]
    assert "Recommended" in changed and not re.search(r"\bO\d\b", changed)          # tiers, not option ids
    assert 'class="turn-folded"' in html and f'href="/runs/dev-{SAVED}"' in html       # earlier turn collapsed
    assert all(r["id"] != rid for r in client.get("/api/runs").json())              # follow-ups not listed
    assert (outputs / "ui" / "turns" / f"{rid[3:]}.json").exists()


def test_clarify_without_input_starts_nothing(outputs):
    client, app = app_client(outputs)
    r = client.post(f"/runs/dev-{SAVED}/clarify", data={}, follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].endswith("#sharpen")
    assert app.state.jobs.jobs == {}


def test_progress_client_marks_steps():
    job = server.Job("j", "e")
    proxy = server.ProgressClient(FakeClient({"intake": [{"summary": "s"}], "assess": [{}],
                                              "external_queries": [{}]}), job)
    assert proxy.tracker is not None                     # the pipeline's spend tracker comes through
    proxy.complete_json("intake", "", "", "", {})
    assert job.understood == "s"
    proxy.complete_json("assess", "", "", "", {})
    assert [s["state"] for s in job.snapshot()["steps"]] == ["done", "done", "done", "running", "pending"]
    proxy.complete_json("external_queries", "", "", "", {})
    job.finish("dev-x", {"intake": 1.0, "assess": 2.0, "repair": 0.5, "external": 3.0, "screen": 0.01})
    snap = job.snapshot()
    assert [s["time"] for s in snap["steps"]] == ["1.0 s", "<0.1 s", "2.5 s", "<0.1 s", "3.0 s"]


# --------------------------------------------------------------------------------- figures, copy, lint
def test_every_printed_range_number_is_on_the_cited_page():
    rows = diagrams.spectral_rows({"MIR", "NIR", "Raman", "UV-Vis", "Fluorescence"}, set(),
                                  {f["id"] for f in kb.fibers()})
    for r in rows:
        numbers = re.findall(r"\d+(?:\.\d+)?", r["label"])
        doc, page = r["source"].split(" p.")
        text = kb.page(doc, int(page))["text"]
        for n in numbers:
            assert re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", text), (r["name"], n, r["source"])
    fluo = next(r for r in rows if r["name"] == "Fluorescence")
    assert fluo["label"] == "range not stated" and fluo["lo"] is None


def test_spectral_figure_shows_only_fibers_for_the_proposed_method(outputs):
    v = server.Store(outputs).view(f"dev-{SAVED}")
    svg = v["figures"]["spectral"]["wide"]
    assert "sp-proposed" in svg and "range not stated" in svg and "Fluorescence" in svg
    assert "UV-VIS silica" not in svg and "Chalcogenide" in svg          # MIR proposed: no UV-Vis silica fiber
    assert ">UV<" in svg and ">MIR<" in svg                               # region band


def test_figure_text_is_at_least_12px():
    css = (paths.ROOT / "src" / "afs_assistant" / "ui" / "static" / "app.css").read_text()
    sizes = [float(x) for x in re.findall(r"svg\.fig [^{]*\{[^}]*font-size:\s*([\d.]+)px", css)]
    assert sizes and min(sizes) >= 12
    assert diagrams.SMALL >= 12 and diagrams.TEXT >= 12


def test_id_words_and_cost_tag(outputs):
    v = server.Store(outputs).view(f"dev-{SAVED}")
    a = view.Assessment.model_validate(json.loads((outputs / "dev" / f"{SAVED}.json").read_text())["assessment"])
    words = view.id_words(a)
    assert words("see Q1 to Q3 and O1") == "see questions 1 to 3 and the simple option"
    tag = v["options"][0]["cost"]["cites"]
    assert tag and v["citations"][tag[0]]["kind"] == "table" and v["citations"][tag[0]]["rows"]
    client, _ = app_client(outputs)
    panel = client.get(f"/runs/dev-{SAVED}/cite/{tag[0]}", headers=HX).text
    assert "Table 1 rows" in panel and "Not verified" not in panel and "<td" in panel


def test_customer_reply_text(outputs):
    v = server.Store(outputs).view(f"dev-{SAVED}")
    assert v["recommendation"]["text"] in v["reply"] and v["proposal"]["next_step"] in v["reply"]
    assert all(q["question"] in v["reply"] for q in v["top_questions"])


def test_no_shadows_and_no_clip_in_css():
    css = (paths.ROOT / "src" / "afs_assistant" / "ui" / "static" / "app.css").read_text()
    assert "box-shadow" not in css and "overflow-x: clip" not in css


def test_ui_code_has_no_case_ids():
    ui = paths.ROOT / "src" / "afs_assistant" / "ui"
    hits = [f"{f.relative_to(ui)}:{i}"
            for f in ui.rglob("*") if f.is_file() and f.suffix in {".py", ".html", ".css", ".js", ".md"}
            and "__pycache__" not in f.parts and not f.name.endswith(".min.js")
            for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1) if kb_check.CASE_ID.search(line)]
    assert hits == []


def test_headline_wording():
    a = copy.deepcopy(ASSESSMENT)
    from afs_assistant.schema import Assessment
    assessment = Assessment.model_validate(a)
    best = next(o for o in assessment.solution_options if o.id == assessment.proposal.best_current_option)
    text = view.headline(assessment, best)
    assert text.endswith(".") and text.split()[0] in ("Start", "Test")


def test_cli_has_ui_command(monkeypatch):
    called = {}
    monkeypatch.setattr(server, "serve", lambda host, port, external: called.update(host=host, port=port, ext=external))
    assert cli.main(["ui", "--port", "9999", "--external", "off"]) == 0
    assert called == {"host": "127.0.0.1", "port": 9999, "ext": "off"}
