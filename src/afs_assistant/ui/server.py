"""The local web UI: FastAPI + Jinja2 templates + htmx (vendored), started by `uv run afs-assist ui`.

Routes (PHASES.md 5.6''''): `GET /` start · `GET /runs/{id}` answer turn(s) · `GET /runs/{id}/cite/{tag}`
source panel · `POST /assess` -> `GET /jobs/{id}` start + poll (`POST /jobs/{id}/stop`) ·
`POST /runs/{id}/clarify` re-assess with answers or an added detail · `GET /runs/{id}.md` / `.json`
downloads · `GET /api/runs[/{id}]`, `/api/jobs/{id}` JSON for tests.
A run id is `<set>-<stem>` of a saved output (`outputs/<set>/<stem>.json`). New runs go through the
same path as the CLI (`cli._assess_one`: provenance record, `outputs/ui/`), one at a time, in a
background thread; a client proxy reports which pipeline stage is running. A follow-up turn records
its parent in `outputs/ui/turns/<stem>.json`, so the thread survives a restart.
Conversations (5.12, `chat.py`): `POST /chat` first message -> assess job · `GET /chat/{cid}` the thread ·
`POST /chat/{cid}/message` free text -> ask job (a new assessment while there is no usable run) ·
`POST /chat/{cid}/reassess` answers / added detail / suggested facts -> reassess job (the clarify path) ·
`GET /chat/{cid}/turns/{n}/cite/{k}` source panel of an answer's citation · `POST /runs/{id}/chat` opens a
saved run as a conversation. Every job kind shares the one-job lock.
Requests with a foreign Host header are refused (400), and so are POSTs from another origin (403).
"""

from __future__ import annotations

import json
import re
import threading
import time
import uuid
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlsplit

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from afs_assistant import activity, chat, paths
from afs_assistant.pipeline import OFF_TOPIC_EXAMPLES
from afs_assistant.ui import view

HERE = Path(__file__).parent
_SET = re.compile(r"^[a-z0-9_]+$")
_STEM = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.-]*$")
LIVE_SET = "ui"
TURNS = "turns"
MAX_TURNS = 12
POLL_SECONDS = 1
MAX_CHARS = 8000                              # per enquiry, answer or follow-up (form maxlength + server check)
TOO_LONG = f"Please keep each text to {MAX_CHARS} characters or fewer; shorten it and send it again."
LOCAL_HOSTS = {"127.0.0.1", "localhost"}
# Which display step a model call belongs to (external roles are named external_*).
ROLE_STEP = {"intake": "intake", "assess": "assess", "repair": "assess", "chat_answer": "answer"}
# What the model is doing during each call, for the activity feed.
ROLE_DOING = {"intake": "read the enquiry", "assess": "write the assessment", "repair": "fix the failed checks",
              "external_queries": "plan literature searches", "external_evidence": "pick literature quotes",
              "chat_answer": "answer the question"}
ASK_STEPS = (("answer", "Answering"),)        # an ask job: one model call (and at most one repair call)
FEED_KEEP, FEED_SHOW = 40, 8


class Stopped(RuntimeError):
    """The user pressed Stop; raised before the next model call."""


# ------------------------------------------------------------------------------------------- runs
def split_id(rid: str) -> tuple[str, str]:
    set_name, _, stem = rid.partition("-")
    if not (_SET.match(set_name) and _STEM.match(stem)) or ".." in stem:
        raise HTTPException(404, "unknown run")
    return set_name, stem


@lru_cache(maxsize=64)
def _load(path: str, mtime: float) -> tuple[dict, str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    md_path = Path(path).with_suffix(".md")
    return data, md_path.read_text(encoding="utf-8") if md_path.exists() else ""


@lru_cache(maxsize=32)
def _view(path: str, mtime: float, rid: str) -> dict:
    data, md = _load(path, mtime)
    return view.build(data, md, rid)


@dataclass
class Store:
    root: Path

    def path(self, rid: str, suffix: str = ".json") -> Path:
        set_name, stem = split_id(rid)
        p = (self.root / set_name / f"{stem}{suffix}").resolve()
        if self.root.resolve() not in p.parents or not p.exists():
            raise HTTPException(404, "unknown run")
        return p

    def data(self, rid: str) -> tuple[dict, str]:
        p = self.path(rid)
        return _load(str(p), p.stat().st_mtime)

    def view(self, rid: str) -> dict:
        p = self.path(rid)
        return _view(str(p), p.stat().st_mtime, rid)

    def turn(self, rid: str) -> dict:
        """The follow-up record of a run ({"parent", "question"}), or {} for a first question."""
        set_name, stem = split_id(rid)
        p = self.root / set_name / TURNS / f"{stem}.json"
        try:
            return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        except (OSError, ValueError):
            return {}

    def save_turn(self, rid: str, parent: str, question: str) -> None:
        set_name, stem = split_id(rid)
        d = self.root / set_name / TURNS
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{stem}.json").write_text(json.dumps({"parent": parent, "question": question}, ensure_ascii=False),
                                        encoding="utf-8")

    def thread(self, rid: str) -> list[str]:
        """Run ids from the first question to `rid` (follow-ups record their parent)."""
        chain = [rid]
        while len(chain) < MAX_TURNS:
            parent = self.turn(chain[0]).get("parent")
            if not parent or parent in chain:
                break
            try:
                self.path(parent)
            except HTTPException:
                break
            chain.insert(0, parent)
        return chain

    def list(self) -> list[dict]:
        """Finished answers to first questions (follow-up turns open from their thread)."""
        out = []
        if not self.root.exists():
            return out
        for p in sorted(self.root.glob("*/*.json")):
            set_name, stem = p.parent.name, p.stem
            if not (_SET.match(set_name) and _STEM.match(stem)):
                continue
            try:
                data, md = _load(str(p), p.stat().st_mtime)
            except (OSError, ValueError):
                continue
            if not isinstance(data, dict) or "enquiry" not in data:
                continue
            rid = f"{set_name}-{stem}"
            if self.turn(rid).get("parent") or view.is_off_topic(data) or view.is_incomplete(data):
                continue                          # finished answers only; others stay reachable by URL
            out.append({"id": rid, "set": set_name, "stem": stem, "title": view.title_of(md, data),
                        "status": view.status_label(data),
                        "date": str((data.get("manifest") or {}).get("created_utc", ""))[:10]})
        out.sort(key=lambda r: (r["set"] != LIVE_SET, r["set"], r["stem"]))
        return out


# ------------------------------------------------------------------------------------------- jobs
@dataclass
class Job:
    id: str
    enquiry: str
    question: str = ""                            # what the user typed for this turn
    parent: str | None = None
    kind: str = "assess"                          # assess | reassess | ask (5.12)
    conversation: str | None = None
    state: str = "running"                       # running | done | failed | stopped
    started: float = field(default_factory=time.monotonic)
    ended: float | None = None
    steps: list[dict] = field(default_factory=lambda: [
        {"key": k, "label": label, "state": "pending", "seconds": 0.0, "since": None} for k, label, _ in view.STEPS])
    current: str | None = None
    understood: str = ""                          # the intake summary, shown as soon as intake returns
    result: str | None = None                     # run id when done
    error: str | None = None
    stop_requested: bool = False
    notes: list[tuple[float, str]] = field(default_factory=list)   # (seconds since start, text), newest last
    waiting: tuple[float, str] | None = None      # (since, what the model is doing) while a call runs
    lock: threading.Lock = field(default_factory=threading.Lock)

    def __post_init__(self) -> None:
        if self.kind == "ask":
            self.steps = [{"key": k, "label": label, "state": "pending", "seconds": 0.0, "since": None}
                          for k, label in ASK_STEPS]

    @property
    def target(self) -> str | None:
        """Where the finished job is shown: its conversation, else the new run."""
        if self.conversation:
            return f"/chat/{self.conversation}"
        return f"/runs/{self.result}" if self.result else None

    @property
    def back(self) -> str:
        if self.conversation:
            return f"/chat/{self.conversation}"
        return f"/runs/{self.parent}" if self.parent else "/"

    def add_note(self, text: str) -> None:
        with self.lock:
            self.notes = [*self.notes, (time.monotonic() - self.started, text)][-FEED_KEEP:]

    def wait_for(self, doing: str | None) -> None:
        with self.lock:
            self.waiting = (time.monotonic(), doing) if doing else None

    def enter(self, key: str) -> None:
        """Start a display step; earlier pending steps are done (screening has no model call)."""
        with self.lock:
            now = time.monotonic()
            self._stop_step(now)
            for st in self.steps:
                if st["key"] == key:
                    st["state"], st["since"] = "running", now
                    break
                if st["state"] == "pending":
                    st["state"] = "done"
            self.current = key

    def _stop_step(self, now: float) -> None:
        for st in self.steps:
            if st["key"] == self.current and st["since"] is not None:
                st["seconds"] += now - st["since"]
                st["state"], st["since"] = "done", None

    def finish(self, rid: str | None, timings: dict | None, error: str | None = None, state: str = "") -> None:
        with self.lock:
            now = time.monotonic()
            self._stop_step(now)
            self.current, self.ended, self.result, self.error = None, now, rid, error
            self.state = state or ("failed" if error else "done")
            recorded = {k: sum(timings[s] for s in stages if s in timings)
                        for k, _, stages in view.STEPS} if timings else {}
            for st in self.steps:
                if st["state"] == "pending" and self.state == "done":
                    st["state"] = "skipped"
                if recorded.get(st["key"]):
                    st["seconds"] = recorded[st["key"]]

    def snapshot(self) -> dict:
        with self.lock:
            now = time.monotonic()
            steps = []
            for st in self.steps:
                seconds = st["seconds"] + (now - st["since"] if st["since"] else 0.0)
                steps.append({"key": st["key"], "label": st["label"], "state": st["state"],
                              "seconds": round(seconds, 2), "time": view.seconds_text(seconds)})
            elapsed = (self.ended or now) - self.started
            feed = [{"at": f"{int(t // 60)}:{int(t % 60):02d}", "text": x} for t, x in self.notes[-FEED_SHOW:]]
            waiting = waiting_clock = None
            if self.waiting and self.state == "running":
                w = now - self.waiting[0]
                waiting, waiting_clock = f"Waiting for the model to {self.waiting[1]}", f"{int(w // 60)}:{int(w % 60):02d}"
            return {"id": self.id, "state": self.state, "steps": steps, "parent": self.parent, "kind": self.kind,
                    "conversation": self.conversation, "back": self.back,
                    "target": self.target if self.state == "done" else None,
                    "question": self.question, "understood": self.understood, "elapsed": round(elapsed, 1),
                    "clock": f"{int(elapsed // 60)}:{int(elapsed % 60):02d}", "result": self.result,
                    "error": self.error, "stop_requested": self.stop_requested, "feed": feed, "waiting": waiting,
                    "waiting_text": waiting, "waiting_clock": waiting_clock}


class ProgressClient:
    """Wraps the model client: every call names its pipeline role, which marks the running step.

    Stop takes effect when the running call returns (it cannot be cut off; it finishes or times out).
    During the literature step the pipeline keeps the finished assessment and records the step as failed."""

    def __init__(self, inner, job: Job) -> None:
        self._inner, self._job = inner, job

    def __getattr__(self, name):                 # tracker etc. come from the real client
        return getattr(self._inner, name)

    def complete_json(self, role: str, *args, **kwargs):
        if self._job.stop_requested:
            raise Stopped("stopped by the user")
        self._job.enter(ROLE_STEP.get(role, "external" if role.startswith("external") else "assess"))
        self._job.wait_for(ROLE_DOING.get(role, "answer"))
        try:
            result = self._inner.complete_json(role, *args, **kwargs)
        finally:
            self._job.wait_for(None)
        took, tokens = getattr(result, "latency_s", 0.0), getattr(result, "completion_tokens", 0)
        self._job.add_note(f"The model answered ({ROLE_DOING.get(role, role)}) in {view.seconds_text(took)}"
                           + (f", {tokens:,} tokens." if tokens else "."))
        if self._job.stop_requested:              # pressed while this call ran: drop its answer
            raise Stopped("stopped by the user")
        if role == "intake" and isinstance(getattr(result, "data", None), dict):
            self._job.understood = " ".join(str(result.data.get("summary", "")).split())
        if role in ("assess", "repair"):
            self._job.enter("verify")
        return result


class Jobs:
    """At most one run at a time (API cost); jobs live in memory for the server's lifetime."""

    def __init__(self, client_factory, store: Store, external: str) -> None:
        self.client_factory, self.store, self.external = client_factory, store, external
        self.out_dir = store.root / LIVE_SET
        self.jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def running(self) -> Job | None:
        return next((j for j in self.jobs.values() if j.state == "running"), None)

    def start(self, enquiry: str, question: str, parent: str | None = None, kind: str = "",
              conversation: str | None = None) -> Job:
        with self._lock:
            if self.running() is not None:
                raise HTTPException(409, "A question is already being assessed; wait for it or stop it.")
            kind = kind or ("reassess" if parent else "assess")
            job = Job(uuid.uuid4().hex[:12], enquiry, question, parent, kind=kind, conversation=conversation)
            self.jobs[job.id] = job
        threading.Thread(target=self._work, args=(job,), daemon=True).start()
        return job

    def _work(self, job: Job) -> None:
        from afs_assistant import cli

        if job.kind == "ask":
            return self._ask(job)
        try:
            job.enter("intake")
            client = ProgressClient(self.client_factory(), job)
            with activity.sink(job.add_note):
                out = cli._assess_one(job.enquiry, None, client, self.out_dir, external=self.external)
            rid = f"{LIVE_SET}-{out['run_id']}"
            if job.parent:
                self.store.save_turn(rid, job.parent, job.question)
            data = json.loads((self.out_dir / f"{out['run_id']}.json").read_text(encoding="utf-8"))
            if job.conversation:
                chat.append(self.out_dir, job.conversation, {"kind": job.kind, "question": job.question, "run_id": rid})
            job.finish(rid, data.get("timings_s"))
        except Stopped:
            job.finish(None, None, "Stopped before the answer was complete.", state="stopped")
        except Exception as exc:                 # noqa: BLE001 - any failure is shown on the running page
            job.finish(None, None, f"{type(exc).__name__}: {exc}")


    def _ask(self, job: Job) -> None:
        """An ask turn over the conversation's current run: one checked `chat_answer` call (5.12)."""
        try:
            job.enter("answer")
            client = ProgressClient(self.client_factory(), job)
            data, _ = self.store.data(job.parent)
            turn = chat.ask(self.store.view(job.parent), data, job.question, client)
            chat.append(self.out_dir, job.conversation, turn)
            removed = len(turn["answer"]["removed"])
            job.add_note(f"Checked the answer: {len(turn['answer']['claims'])} claim(s) shown"
                         + (f", {removed} removed (unsupported figure or quote)." if removed else "."))
            job.finish(job.parent, None)
        except Stopped:
            job.finish(None, None, "Stopped before the answer was complete.", state="stopped")
        except Exception as exc:                 # noqa: BLE001 - any failure is shown on the running page
            job.finish(None, None, f"{type(exc).__name__}: {exc}")


def _default_client():
    from afs_assistant.llm import OpenRouterClient

    return OpenRouterClient()


def _host_of(value: str) -> str:
    """'127.0.0.1:8765' or 'http://localhost:8765/x' -> host name, lowercased, without port."""
    if "//" not in value:
        value = "//" + value
    try:
        return (urlsplit(value).hostname or "").lower()
    except ValueError:
        return ""


def _netloc_of(url: str) -> str:
    """'http://127.0.0.1:8765/x' -> '127.0.0.1:8765'; anything unparsable or 'null' -> ''."""
    try:
        return urlsplit(url).netloc.lower()
    except ValueError:
        return ""


def _too_long(*texts: str) -> bool:
    return any(len(t) > MAX_CHARS for t in texts)


# -------------------------------------------------------------------------------------------- app
def create_app(outputs: Path = paths.OUTPUTS, client_factory=_default_client, external: str = "live",
               host: str = "127.0.0.1") -> FastAPI:
    app = FastAPI(title="AFS Spectroscopy Assistant", docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
    templates = Jinja2Templates(directory=HERE / "templates")
    templates.env.globals["MAX_CHARS"] = MAX_CHARS
    store = Store(outputs)
    jobs = Jobs(client_factory, store, external)
    allowed = LOCAL_HOSTS | {host.lower()}
    app.state.store, app.state.jobs, app.state.allowed_hosts = store, jobs, allowed

    @app.middleware("http")
    async def local_only(request: Request, call_next):
        """DNS-rebinding and cross-site POST guard: Host must be local; a POST's Origin/Referer too."""
        if _host_of(request.headers.get("host", "")) not in allowed:
            return PlainTextResponse("Unknown host.", status_code=400)
        if request.method not in ("GET", "HEAD", "OPTIONS"):
            origin = request.headers.get("origin")
            referer = request.headers.get("referer")
            source = origin if origin is not None else referer
            # same origin = same host AND port as this server (another local app on :3000 is foreign)
            if source is not None and _netloc_of(source) != request.headers.get("host", "").lower():
                return PlainTextResponse("Cross-origin request refused.", status_code=403)
        return await call_next(request)

    def page(request: Request, name: str, status_code: int = 200, **context) -> HTMLResponse:
        context.setdefault("saved", store.list())
        context.setdefault("busy", jobs.running())
        context["htmx"] = request.headers.get("HX-Request") == "true"
        return templates.TemplateResponse(request=request, name=name, context=context, status_code=status_code)

    @app.get("/", response_class=HTMLResponse)
    def start(request: Request, q: str = ""):
        return page(request, "start.html", q=q, examples=list(OFF_TOPIC_EXAMPLES))

    @app.get("/runs/{rid}.md")
    def download_md(rid: str):
        return FileResponse(store.path(rid, ".md"), media_type="text/markdown; charset=utf-8", filename=f"{rid}.md")

    @app.get("/runs/{rid}.json")
    def download_json(rid: str):
        return FileResponse(store.path(rid, ".json"), media_type="application/json", filename=f"{rid}.json")

    @app.get("/runs/{rid}", response_class=HTMLResponse)
    def run_page(request: Request, rid: str):
        chain = store.thread(rid)
        turns = []
        for i, r in enumerate(chain):
            v = store.view(r)
            record = store.turn(r) if i else {}
            turns.append({"v": v, "question": record.get("question") or v["enquiry"], "is_follow_up": bool(i),
                          "changed": view.compare(turns[-1]["v"], v) if i else None})
        return page(request, "run.html", turns=turns, v=turns[-1]["v"])

    @app.get("/runs/{rid}/cite/{tag}", response_class=HTMLResponse)
    def cite(request: Request, rid: str, tag: str):
        v = store.view(rid)
        c = (v.get("citations") or {}).get(tag)
        if c is None:
            raise HTTPException(404, "unknown citation")
        src = view.source(c["doc"], c["page"], c["quote"]) if c["kind"] == "supplied" else None
        return page(request, "cite.html", v=v, c=c, src=src)

    @app.post("/assess")
    def assess(request: Request, enquiry: str = Form("")):
        text = enquiry.strip()
        if not text or _too_long(text):
            return page(request, "start.html", status_code=422, q=text[:MAX_CHARS], examples=list(OFF_TOPIC_EXAMPLES),
                        error=TOO_LONG if text else "Describe what you want to measure first.")
        job = jobs.start(text, text)
        return RedirectResponse(f"/jobs/{job.id}", status_code=303)

    def _clarify_input(v: dict, form, follow_up: str) -> tuple[list[dict], str] | None:
        """The answered questions and added detail of a clarify / reassess form; None when too long."""
        answers = [{"question": q["question"], "answer": str(form.get(f"answer_{q['id']}", "")).strip()}
                   for q in v.get("questions", [])]
        given = [a for a in answers if a["answer"]]
        if _too_long(follow_up, *(a["answer"] for a in given)):
            return None
        return given, "\n".join([f"{a['question']} {a['answer']}" for a in given] + ([follow_up] if follow_up else []))

    @app.post("/runs/{rid}/clarify")
    async def clarify(request: Request, rid: str):
        v = store.view(rid)
        form = await request.form()
        follow_up = str(form.get("followup", "")).strip()
        parsed = _clarify_input(v, form, follow_up)
        if parsed is None:
            return page(request, "error.html", status_code=422, message=TOO_LONG, back=f"/runs/{rid}")
        given, question = parsed
        if not question:
            return RedirectResponse(f"/runs/{rid}#sharpen", status_code=303)
        job = jobs.start(view.answers_to_facts(v["enquiry"], given, follow_up), question, parent=rid)
        return RedirectResponse(f"/jobs/{job.id}", status_code=303)

    # ------------------------------------------------------------------------------- conversations
    live = jobs.out_dir

    def _conversation(cid: str) -> dict:
        conv = chat.load(live, cid)
        if conv is None:
            raise HTTPException(404, "unknown conversation")
        return conv

    def _usable(rid: str | None) -> dict | None:
        """The current run's view, or None when there is none to ask about (missing, off topic, incomplete)."""
        if rid is None:
            return None
        try:
            v = store.view(rid)
        except HTTPException:
            return None
        return None if v.get("off_topic") or v.get("incomplete") else v

    def _thread(conv: dict) -> list[dict]:
        """Display model of each turn: its run view, What changed for a reassess, the checked answer for an ask."""
        turns, previous, changed_by_run = [], None, {}
        last_run_turn = max((i for i, t in enumerate(conv.get("turns", [])) if t["kind"] != "ask"), default=None)
        for i, t in enumerate(conv.get("turns", [])):
            item = {"n": i, "kind": t["kind"], "question": t.get("question", ""), "p": f"t{i}-", "v": None,
                    "run_id": t.get("run_id"), "changed": None, "current": False}
            if t.get("run_id"):
                try:
                    item["v"] = store.view(t["run_id"])
                except HTTPException:
                    item["missing"] = True
            if t["kind"] != "ask":
                if t["kind"] == "reassess" and previous is not None and item["v"] is not None:
                    item["changed"] = view.compare(previous, item["v"])
                    changed_by_run[t["run_id"]] = item["changed"]
                previous = item["v"] or previous
                item["current"] = i == last_run_turn          # only the latest run takes answers (reassess)
                if not item["question"] and item["v"] is not None:
                    item["question"] = item["v"]["enquiry"]
            else:
                item["answer"] = t.get("answer") or {}
                item["changed"] = changed_by_run.get(t.get("run_id"))
                item["checks"] = t.get("checks") or {}
            turns.append(item)
        return turns

    @app.post("/chat")
    def chat_start(request: Request, enquiry: str = Form("")):
        text = enquiry.strip()
        if not text or _too_long(text):
            return page(request, "start.html", status_code=422, q=text[:MAX_CHARS], examples=list(OFF_TOPIC_EXAMPLES),
                        error=TOO_LONG if text else "Describe what you want to measure first.")
        if jobs.running() is not None:
            raise HTTPException(409, "A question is already being assessed; wait for it or stop it.")
        conv = chat.new_conversation(live)
        jobs.start(text, text, kind=chat.route(None, "message"), conversation=conv["id"])
        return RedirectResponse(f"/chat/{conv['id']}", status_code=303)

    @app.post("/runs/{rid}/chat")
    def chat_from_run(rid: str):
        v = store.view(rid)
        conv = chat.new_conversation(live, seed_run=rid, question=v["enquiry"])
        return RedirectResponse(f"/chat/{conv['id']}", status_code=303)

    @app.get("/chat/{cid}", response_class=HTMLResponse)
    def chat_page(request: Request, cid: str):
        conv = _conversation(cid)
        busy = jobs.running()
        mine = busy if busy is not None and busy.conversation == cid else None
        return page(request, "conversation.html", conv=conv, turns=_thread(conv), cid=cid,
                    job=mine.snapshot() if mine else None, poll=POLL_SECONDS,
                    current=_usable(chat.current_run(conv)))

    @app.post("/chat/{cid}/message")
    def chat_message(request: Request, cid: str, text: str = Form("")):
        conv = _conversation(cid)
        text = text.strip()
        if not text:
            return RedirectResponse(f"/chat/{cid}", status_code=303)
        if _too_long(text):
            return page(request, "error.html", status_code=422, message=TOO_LONG, back=f"/chat/{cid}")
        rid = chat.current_run(conv)
        kind = chat.route(conv, "message") if _usable(rid) is not None else "assess"
        if kind == "ask":
            jobs.start("", text, parent=rid, kind="ask", conversation=cid)
        else:                                    # nothing usable to ask about: assess the text as an enquiry
            jobs.start(text, text, kind="assess", conversation=cid)
        return RedirectResponse(f"/chat/{cid}", status_code=303)

    @app.post("/chat/{cid}/reassess")
    async def chat_reassess(request: Request, cid: str):
        conv = _conversation(cid)
        rid = chat.current_run(conv)
        v = _usable(rid)
        form = await request.form()
        follow_up = " ".join(str(form.get(k, "")).strip() for k in ("followup", "text")).strip()
        if v is None or chat.route(conv, "reassess") != "reassess":
            return RedirectResponse(f"/chat/{cid}", status_code=303)
        parsed = _clarify_input(v, form, follow_up)
        if parsed is None:
            return page(request, "error.html", status_code=422, message=TOO_LONG, back=f"/chat/{cid}")
        given, question = parsed
        if not question:
            return RedirectResponse(f"/chat/{cid}", status_code=303)
        jobs.start(view.answers_to_facts(v["enquiry"], given, follow_up), question, parent=rid, kind="reassess",
                   conversation=cid)
        return RedirectResponse(f"/chat/{cid}", status_code=303)

    @app.get("/chat/{cid}/turns/{n}/cite/{k}", response_class=HTMLResponse)
    def chat_cite(request: Request, cid: str, n: int, k: str):
        """Source panel of one citation of an ask answer: claim index and citation index, `<claim>-<cite>`."""
        conv = _conversation(cid)
        turns = conv.get("turns", [])
        ci, _, cj = k.partition("-")
        try:
            c = turns[n]["answer"]["claims"][int(ci)]["citations"][int(cj)]
        except (IndexError, KeyError, ValueError, TypeError):
            raise HTTPException(404, "unknown citation") from None
        v = store.view(turns[n]["run_id"])
        if c["kind"] == "external":
            ext = next((x for x in v["citations"].values() if x["kind"] == "external" and x["label"] == c["label"]), None)
            if ext is None:
                raise HTTPException(404, "unknown citation")
            return page(request, "cite.html", v=v, c=ext, src=None)
        src = view.source(c["doc"], c["page"], c["quote"])
        shown = {"kind": "supplied", "label": c["label"], "verified": bool(src and src["verified"]),
                 "quote_status": c.get("quote_status", ""), "precedent": c.get("precedent", False),
                 "quote": c["quote"]}
        return page(request, "cite.html", v=v, c=shown, src=src)

    def _job(jid: str) -> Job:
        job = jobs.jobs.get(jid)
        if job is None:
            raise HTTPException(404, "unknown job")
        return job

    @app.post("/jobs/{jid}/stop")
    def stop(jid: str):
        job = _job(jid)
        job.stop_requested = True
        return RedirectResponse(f"/jobs/{jid}", status_code=303)

    @app.get("/jobs/{jid}", response_class=HTMLResponse)
    def job_page(request: Request, jid: str):
        if jid not in jobs.jobs and request.headers.get("HX-Request") == "true":
            # jobs live in memory: after a restart a polling page gets one final answer and stops (286)
            return HTMLResponse('<p class="flag" id="job-steps">This question is no longer tracked (the assistant '
                                'was restarted). <a href="/">Start again</a></p>', status_code=286)
        snap = _job(jid).snapshot()
        target = snap["target"]
        htmx = request.headers.get("HX-Request") == "true"
        if target and not htmx:
            return RedirectResponse(target, status_code=303)
        if htmx:
            response = page(request, "job_steps.html", job=snap, poll=POLL_SECONDS)
            if target:
                response.headers["HX-Redirect"] = target
            elif snap["state"] != "running":
                response.status_code = 286        # htmx: stop polling
            return response
        return page(request, "job.html", job=snap, poll=POLL_SECONDS)

    @app.get("/api/runs")
    def api_runs():
        return store.list()

    @app.get("/api/runs/{rid}")
    def api_run(rid: str):
        return store.view(rid)

    @app.get("/api/jobs/{jid}")
    def api_job(jid: str):
        return _job(jid).snapshot()

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> Response:
        if request.url.path.startswith("/api/"):
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        return page(request, "error.html", status_code=exc.status_code, message=exc.detail)

    return app


def serve(host: str = "127.0.0.1", port: int = 8765, external: str = "live") -> None:
    import uvicorn

    uvicorn.run(create_app(external=external, host=host), host=host, port=port, log_level="warning")
