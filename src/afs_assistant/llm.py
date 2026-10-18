"""LLM access through OpenRouter (OpenAI-compatible API) with structured JSON output.

`OpenRouterClient` is the real client; `FakeClient` returns queued responses for offline
tests. Both return `LLMResult`. Every call is costed and checked against spend caps.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import yaml

from afs_assistant import paths

CONFIG_FILE = paths.ROOT / "config" / "models.yaml"
# Alternative models config (absolute, or relative to the repo root), e.g. one bake-off arm (D-054).
CONFIG_ENV = "AFS_MODELS_CONFIG"
# Request parameters a model may leave out via `model_params: {<model>: {omit: [...]}}` (D-054).
OMITTABLE = ("temperature", "max_tokens", "response_format")


class SpendCapExceeded(RuntimeError):
    pass


class RunCancelled(RuntimeError):
    """The set run was interrupted (Ctrl-C): a running case stops at its next LLM call or while waiting."""


class DeadlineExceeded(RuntimeError):
    """No complete reply within the role's wall-clock `timeout_s`; counted as a timeout (retried once)."""


def config_path() -> Path:
    """The models config in use: `AFS_MODELS_CONFIG` if set, else config/models.yaml."""
    value = os.environ.get(CONFIG_ENV, "").strip()
    if not value:
        return CONFIG_FILE
    path = Path(value)
    return path if path.is_absolute() else paths.ROOT / path


@lru_cache(maxsize=1)
def _config_source() -> tuple[Path, bytes]:
    path = config_path()
    return path, path.read_bytes()


@lru_cache(maxsize=1)
def config() -> dict:
    return yaml.safe_load(_config_source()[1].decode("utf-8"))


def config_provenance() -> dict:
    """Path (repo-relative when inside the repo) and sha256 of the loaded models config, for the run manifest."""
    path, data = _config_source()
    try:
        shown = path.resolve().relative_to(paths.ROOT.resolve()).as_posix()
    except ValueError:
        shown = str(path)
    return {"path": shown, "sha256": hashlib.sha256(data).hexdigest()}


def omitted_params(model: str) -> set[str]:
    """Request parameters the model does not accept (e.g. `temperature`); a name outside OMITTABLE is an error."""
    omit = set(config().get("model_params", {}).get(model, {}).get("omit", []))
    unknown = omit - set(OMITTABLE)
    if unknown:
        raise ValueError(f"model_params.{model}.omit: cannot omit {sorted(unknown)} (allowed: {list(OMITTABLE)})")
    return omit


@dataclass
class LLMResult:
    data: dict
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    cached_tokens: int = 0
    cost_usd: float = 0.0
    latency_s: float = 0.0
    response_id: str = ""
    provider: str = ""


@dataclass
class SpendTracker:
    """Spend caps and the call log, safe to share between threads (parallel set runs).

    The session total and `calls` are shared under a lock. The run total and `run_calls`
    belong to the calling thread: `start_run` resets them for the run on that thread, so the
    per-run cap stays per run when several runs share one tracker.
    """
    per_run_cap: float
    per_session_cap: float
    session_usd: float = 0.0
    calls: list[dict] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False, repr=False, compare=False)
    _local: threading.local = field(default_factory=threading.local, init=False, repr=False, compare=False)
    cancel: threading.Event = field(default_factory=threading.Event, init=False, repr=False, compare=False)

    @property
    def run_usd(self) -> float:
        return getattr(self._local, "run_usd", 0.0)

    @property
    def run_calls(self) -> list[dict]:
        """The calls of the run on this thread since its `start_run`."""
        if not hasattr(self._local, "calls"):
            self._local.calls = []
        return self._local.calls

    def start_run(self) -> None:
        self._local.run_usd = 0.0
        self._local.calls = []

    def check(self) -> None:
        if self.cancel.is_set():
            raise RunCancelled("set run cancelled")
        with self._lock:
            if self.run_usd >= self.per_run_cap:
                raise SpendCapExceeded(f"run spend {self.run_usd:.4f} USD reached cap {self.per_run_cap}")
            if self.session_usd >= self.per_session_cap:
                raise SpendCapExceeded(f"session spend {self.session_usd:.4f} USD reached cap "
                                       f"{self.per_session_cap}")

    def add(self, role: str, result: LLMResult) -> None:
        call = {"role": role, "model": result.model, "provider": result.provider,
                "prompt_tokens": result.prompt_tokens,
                "completion_tokens": result.completion_tokens, "cached_tokens": result.cached_tokens,
                "cost_usd": round(result.cost_usd, 6), "latency_s": round(result.latency_s, 2)}
        with self._lock:
            self._local.run_usd = self.run_usd + result.cost_usd
            self.session_usd += result.cost_usd
            self.calls.append(call)
            self.run_calls.append(call)


def make_tracker() -> SpendTracker:
    caps = config()["spend_cap_usd"]
    return SpendTracker(caps["per_run"], caps["per_session"])


def strict_schema(schema: dict) -> dict:
    """Make a pydantic JSON schema acceptable to strict structured-output mode.

    Strict mode needs every object to list all properties as required and to forbid
    extra properties; pydantic defaults leave both open.
    """
    def fix(node):
        if isinstance(node, dict):
            if node.get("type") == "object" and "properties" in node:
                node["required"] = list(node["properties"].keys())
                node["additionalProperties"] = False
            node.pop("default", None)
            node.pop("title", None)
            for value in node.values():
                fix(value)
        elif isinstance(node, list):
            for item in node:
                fix(item)
        return node

    return fix(json.loads(json.dumps(schema)))


def timeout_s(role: str) -> float:
    """Per-request timeout of a role (seconds): its `timeout_s`, else the top-level `timeout_s`."""
    cfg = config()
    return float(cfg["roles"][role].get("timeout_s", cfg["timeout_s"]))


class OpenRouterClient:
    """Real client. Reads OPENROUTER_API_KEY from the environment or .env.

    The SDK does not retry (`max_retries=0`); this class retries transient errors itself, and a
    timed-out request (per-role `timeout_s`) at most once, so a stalled provider cannot block a run.
    The SDK timeout bounds each network read, not the whole reply (a slow trickle never trips it), so
    every request also runs under a wall-clock deadline of the same `timeout_s` (5.0.R).
    """

    TRANSIENT = ("APIConnectionError", "APITimeoutError", "DeadlineExceeded", "RateLimitError",
                 "InternalServerError")
    TIMEOUTS = ("APITimeoutError", "DeadlineExceeded")
    MAX_TIMEOUTS = 2        # a timed-out call is retried once; the second timeout fails the call
    POLL_S = 0.5            # how often a waiting call looks at the cancel event

    def __init__(self, tracker: SpendTracker | None = None) -> None:
        from dotenv import load_dotenv
        from openai import OpenAI

        load_dotenv(paths.ROOT / ".env")
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            raise RuntimeError("OPENROUTER_API_KEY is not set (put it in .env; never commit it)")
        self.client = OpenAI(base_url=config()["base_url"], api_key=key, max_retries=0,
                             timeout=float(config()["timeout_s"]))
        self.tracker = tracker or make_tracker()

    def complete_json(self, role: str, system: str, user: str, schema_name: str, schema: dict) -> LLMResult:
        cfg = config()
        role_cfg = cfg["roles"][role]
        model = role_cfg["model"]
        if cfg.get("response_mode", "json_schema") == "json_schema":
            response_format = {"type": "json_schema",
                               "json_schema": {"name": schema_name, "strict": True, "schema": strict_schema(schema)}}
        else:
            response_format = {"type": "json_object"}
        messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        routing = {"require_parameters": True, **cfg.get("provider_routing", {}).get(model, {})}
        extra = {"provider": routing, "usage": {"include": True}}
        if "reasoning" in role_cfg:          # e.g. {effort: low}: bounds the hidden reasoning of a small step
            extra["reasoning"] = role_cfg["reasoning"]
        # Not sent at all when the model omits them: with require_parameters a sent `temperature` leaves no
        # endpoint for a model that does not accept it.
        params = {"temperature": cfg.get("temperature", 0), "max_tokens": role_cfg.get("max_tokens", 8000),
                  "response_format": response_format}
        for name in omitted_params(model):
            params.pop(name)

        last_error: Exception | None = None
        timeouts = 0
        for attempt in range(3):
            self.tracker.check()          # per attempt: a retried call must not run past the cap
            started = time.monotonic()
            try:
                response = self._create_with_deadline(
                    timeout_s(role),
                    model=model, messages=messages, **params, extra_body=extra, timeout=timeout_s(role),
                )
            except Exception as exc:  # retry only transient API errors
                if type(exc).__name__ not in self.TRANSIENT:
                    raise
                last_error = exc
                if type(exc).__name__ in self.TIMEOUTS:
                    # Logged with cost 0: an abandoned reply that still completes later is not costed.
                    self.tracker.add(role + ":timeout",
                                     LLMResult(data={}, model=model, latency_s=time.monotonic() - started))
                    timeouts += 1
                    if timeouts >= self.MAX_TIMEOUTS:
                        raise RuntimeError(f"LLM call timed out {timeouts} times ({timeout_s(role):.0f} s each, "
                                           f"role {role})") from exc
                time.sleep(2 * (attempt + 1))
                continue
            # Cost every reply, including the ones discarded below (truncated or invalid JSON).
            result = LLMResult(data={}, model=response.model or model, latency_s=time.monotonic() - started,
                               response_id=response.id or "", provider=getattr(response, "provider", "") or "")
            _account(result, response.usage, cfg.get("prices", {}).get(model, {"input": 0, "output": 0}))
            content = response.choices[0].message.content or ""
            finish = response.choices[0].finish_reason
            try:
                if finish == "length":
                    raise json.JSONDecodeError("reply truncated at max_tokens", content, len(content))
                data = json.loads(content)
            except json.JSONDecodeError as exc:  # empty or truncated reply from the provider: retry
                self.tracker.add(role + ":discarded", result)
                last_error = RuntimeError(f"invalid JSON from provider {result.provider or '?'} "
                                          f"(finish={finish}, {len(content)} chars): {exc}")
                continue
            result.data = data
            self.tracker.add(role, result)
            return result
        raise RuntimeError(f"LLM call failed after retries: {last_error}")


    def _create_with_deadline(self, seconds: float, **kwargs):
        """The SDK request on a daemon thread, waited for at most `seconds` (wall clock). Past the deadline
        the request is abandoned (DeadlineExceeded); a set cancel event stops the wait at once."""
        box: dict = {}

        def call() -> None:
            try:
                box["response"] = self.client.chat.completions.create(**kwargs)
            except BaseException as exc:  # noqa: BLE001 - handed to the waiting thread
                box["error"] = exc

        worker = threading.Thread(target=call, name="llm-request", daemon=True)
        worker.start()
        deadline = time.monotonic() + seconds
        while worker.is_alive():
            if self.tracker.cancel.is_set():
                raise RunCancelled("set run cancelled while waiting for the model")
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise DeadlineExceeded(f"no complete reply within {seconds:.0f} s (wall clock)")
            worker.join(min(self.POLL_S, remaining))
        if "error" in box:
            raise box["error"]
        return box["response"]


def _account(result: LLMResult, usage, price: dict) -> None:
    """Fill tokens and cost from the usage block; fall back to configured prices."""
    if usage is not None:
        result.prompt_tokens = usage.prompt_tokens or 0
        result.completion_tokens = usage.completion_tokens or 0
        details = getattr(usage, "prompt_tokens_details", None)
        result.cached_tokens = getattr(details, "cached_tokens", 0) or 0
        result.cost_usd = float(getattr(usage, "cost", 0.0) or 0.0)
    if not result.cost_usd:
        result.cost_usd = (result.prompt_tokens * price["input"] + result.completion_tokens * price["output"]) / 1e6


class FakeClient:
    """Offline stand-in: returns queued dicts per role, records the prompts it saw."""

    def __init__(self, responses: dict[str, list[dict]]) -> None:
        self.responses = {role: list(items) for role, items in responses.items()}
        self.seen: list[dict] = []
        self.tracker = SpendTracker(1e9, 1e9)

    def complete_json(self, role: str, system: str, user: str, schema_name: str, schema: dict) -> LLMResult:
        self.seen.append({"role": role, "system": system, "user": user, "schema_name": schema_name})
        if not self.responses.get(role):
            raise AssertionError(f"FakeClient has no queued response for role {role!r}")
        result = LLMResult(data=self.responses[role].pop(0), model=f"fake/{role}")
        self.tracker.add(role, result)
        return result
