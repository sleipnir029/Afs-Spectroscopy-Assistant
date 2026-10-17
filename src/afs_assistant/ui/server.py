"""The local web UI: FastAPI + Jinja2 templates + htmx (vendored), started by `uv run afs-assist ui`.

Routes (PHASES.md 5.6'''): `GET /` start · `GET /runs/{id}` answer page · `GET /runs/{id}/cite/{tag}`
citation panel · `POST /assess` -> `GET /jobs/{id}` start + poll · `POST /runs/{id}/clarify` re-assess
with answers · `GET /runs/{id}.md` / `.json` downloads · `GET /api/runs[/{id}]` JSON for tests.
A run id is `<set>-<stem>` of a saved output (`outputs/<set>/<stem>.json`), e.g. the dev set's runs.
New runs go through the same path as the CLI (`cli._assess_one`: provenance record, outputs/<live set>/),
one at a time, in a background thread; a client proxy reports which pipeline stage is running.
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

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    RedirectResponse,
    Response,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from afs_assistant import paths
from afs_assistant.ui import view

HERE = Path(__file__).parent
_SET = re.compile(r"^[a-z0-9_]+$")
_STEM = re.compile(r"^[A-Za-z0-9_.][A-Za-z0-9_.-]*$")
LIVE_SET = "ui"
POLL_SECONDS = 1
# Which display step a model call belongs to (external roles are named external_*).
ROLE_STEP = {"intake": "intake", "assess": "assess", "repair": "assess"}


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

    def list(self) -> list[dict]:
        """Saved runs, newest set first; each with title, status and date."""
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
            if "enquiry" not in data:
                continue
            out.append({"id": f"{set_name}-{stem}", "set": set_name, "stem": stem, "title": view.title_of(md, data),
                        "status": view.status_label(data),
                        "date": str((data.get("manifest") or {}).get("created_utc", ""))[:10]})
        out.sort(key=lambda r: (r["set"] != LIVE_SET, r["set"], r["stem"]))
        return out


# ------------------------------------------------------------------------------------------- jobs
@dataclass
class Job:
    id: str
    enquiry: str
    parent: str | None = None
    state: str = "running"                       # running | done | failed
    started: float = field(default_factory=time.monotonic)
    ended: float | None = None
    steps: list[dict] = field(default_factory=lambda: [
        {"key": k, "label": label, "state": "pending", "seconds": 0.0, "since": None} for k, label, _ in view.STEPS])
    current: str | None = None
    result: str | None = None                    # run id when done
    error: str | None = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    def enter(self, key: str) -> None:
        """Start a display step; earlier pending steps are done (screening has no model call)."""
        with self.lock:
            now = time.monotonic()
            self._stop(now)
            for st in self.steps:
                if st["key"] == key:
                    st["state"], st["since"] = "running", now
                    break
                if st["state"] == "pending":
                    st["state"] = "done"
            self.current = key

    def _stop(self, now: float) -> None:
        for st in self.steps:
            if st["key"] == self.current and st["since"] is not None:
                st["seconds"] += now - st["since"]
                st["state"], st["since"] = "done", None

    def finish(self, rid: str | None, timings: dict | None, error: str | None = None) -> None:
        with self.lock:
            now = time.monotonic()
            self._stop(now)
            self.current, self.ended, self.result, self.error = None, now, rid, error
            self.state = "failed" if error else "done"
            recorded = {k: sum(timings[s] for s in stages if s in timings)
                        for k, _, stages in view.STEPS} if timings else {}
            for st in self.steps:
                if st["state"] == "pending" and not error:
                    st["state"] = "skipped"
                if recorded.get(st["key"]):
                    st["seconds"] = recorded[st["key"]]

    def snapshot(self) -> dict:
        with self.lock:
            now = time.monotonic()
            steps = [{"key": st["key"], "label": st["label"], "state": st["state"],
                      "seconds": round(st["seconds"] + (now - st["since"] if st["since"] else 0.0), 1)}
                     for st in self.steps]
            return {"id": self.id, "state": self.state, "steps": steps, "parent": self.parent,
                    "elapsed": round((self.ended or now) - self.started, 1), "result": self.result,
                    "error": self.error}


class ProgressClient:
    """Wraps the model client; every call names its pipeline role, which marks the running step."""

    def __init__(self, inner, job: Job) -> None:
        self._inner, self._job = inner, job

    def __getattr__(self, name):                 # tracker etc. come from the real client
        return getattr(self._inner, name)

    def complete_json(self, role: str, *args, **kwargs):
        self._job.enter(ROLE_STEP.get(role, "external" if role.startswith("external") else "assess"))
        result = self._inner.complete_json(role, *args, **kwargs)
        if role in ("assess", "repair"):
            self._job.enter("verify")
        return result


class Jobs:
    """At most one run at a time (API cost); jobs live in memory for the server's lifetime."""

    def __init__(self, client_factory, out_dir: Path, external: str) -> None:
        self.client_factory, self.out_dir, self.external = client_factory, out_dir, external
        self.jobs: dict[str, Job] = {}
        self._lock = threading.Lock()

    def running(self) -> Job | None:
        return next((j for j in self.jobs.values() if j.state == "running"), None)

    def start(self, enquiry: str, parent: str | None = None) -> Job:
        with self._lock:
            if self.running() is not None:
                raise HTTPException(409, "A run is already in progress.")
            job = Job(uuid.uuid4().hex[:12], enquiry, parent)
            self.jobs[job.id] = job
        threading.Thread(target=self._work, args=(job,), daemon=True).start()
        return job

    def _work(self, job: Job) -> None:
        from afs_assistant import cli

        try:
            job.enter("intake")
            client = ProgressClient(self.client_factory(), job)
            out = cli._assess_one(job.enquiry, None, client, self.out_dir, external=self.external)
            rid = f"{self.out_dir.name}-{out['run_id']}"
            data = json.loads((self.out_dir / f"{out['run_id']}.json").read_text(encoding="utf-8"))
            job.finish(rid, data.get("timings_s"))
        except Exception as exc:                 # noqa: BLE001 - any failure is shown on the running page
            job.finish(None, None, f"{type(exc).__name__}: {exc}")


def _default_client():
    from afs_assistant.llm import OpenRouterClient

    return OpenRouterClient()


# -------------------------------------------------------------------------------------------- app
def create_app(outputs: Path = paths.OUTPUTS, client_factory=_default_client, external: str = "live") -> FastAPI:
    app = FastAPI(title="AFS Spectroscopy Assistant", docs_url=None, redoc_url=None, openapi_url=None)
    app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
    templates = Jinja2Templates(directory=HERE / "templates")
    store = Store(outputs)
    jobs = Jobs(client_factory, outputs / LIVE_SET, external)
    app.state.store, app.state.jobs = store, jobs

    def page(request: Request, name: str, status_code: int = 200, **context) -> HTMLResponse:
        context.setdefault("saved", store.list())
        context["htmx"] = request.headers.get("HX-Request") == "true"
        return templates.TemplateResponse(request=request, name=name, context=context, status_code=status_code)

    @app.get("/", response_class=HTMLResponse)
    def start(request: Request, q: str = ""):
        return page(request, "start.html", q=q, busy=jobs.running())

    @app.get("/runs/{rid}.md")
    def download_md(rid: str):
        p = store.path(rid, ".md")
        return FileResponse(p, media_type="text/markdown; charset=utf-8", filename=f"{rid}.md")

    @app.get("/runs/{rid}.json")
    def download_json(rid: str):
        p = store.path(rid, ".json")
        return FileResponse(p, media_type="application/json", filename=f"{rid}.json")

    @app.get("/runs/{rid}", response_class=HTMLResponse)
    def run_page(request: Request, rid: str, compare: str = ""):
        v = store.view(rid)
        diff = None
        if compare:
            try:
                diff = view.compare(store.view(compare), v)
            except HTTPException:
                diff = None
        return page(request, "run.html", v=v, diff=diff)

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
        if not text:
            return page(request, "start.html", status_code=422, q="", busy=jobs.running(),
                        error="Paste a customer enquiry first.")
        job = jobs.start(text)
        return RedirectResponse(f"/jobs/{job.id}", status_code=303)

    @app.post("/runs/{rid}/clarify")
    async def clarify(request: Request, rid: str):
        v = store.view(rid)
        if v.get("off_topic"):
            raise HTTPException(400, "an off-topic run has no questions")
        form = await request.form()
        answers = [{"question": q["question"], "answer": str(form.get(f"answer_{q['id']}", ""))}
                   for q in v["questions"]]
        if not any(a["answer"].strip() for a in answers):
            return RedirectResponse(f"/runs/{rid}#questions", status_code=303)
        job = jobs.start(view.answers_to_facts(v["enquiry"], answers), parent=rid)
        return RedirectResponse(f"/jobs/{job.id}", status_code=303)

    @app.get("/jobs/{jid}", response_class=HTMLResponse)
    def job_page(request: Request, jid: str):
        job = jobs.jobs.get(jid)
        if job is None:
            raise HTTPException(404, "unknown job")
        snap = job.snapshot()
        target = None
        if snap["state"] == "done":
            target = f"/runs/{snap['result']}" + (f"?compare={snap['parent']}" if snap["parent"] else "")
        htmx = request.headers.get("HX-Request") == "true"
        if target and not htmx:
            return RedirectResponse(target, status_code=303)
        if htmx:
            response = page(request, "job_steps.html", job=snap, poll=POLL_SECONDS)
            if target:
                response.headers["HX-Redirect"] = target
            elif snap["state"] == "failed":
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
        job = jobs.jobs.get(jid)
        if job is None:
            raise HTTPException(404, "unknown job")
        return job.snapshot()

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> Response:
        if request.url.path.startswith("/api/"):
            return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
        return page(request, "error.html", status_code=exc.status_code, message=exc.detail,
                    busy=jobs.running())

    return app


def serve(host: str = "127.0.0.1", port: int = 8765, external: str = "live") -> None:
    import uvicorn

    uvicorn.run(create_app(external=external), host=host, port=port, log_level="warning")
