"""LLM access through OpenRouter (OpenAI-compatible API) with structured JSON output.

`OpenRouterClient` is the real client; `FakeClient` returns queued responses for offline
tests. Both return `LLMResult`. Every call is costed and checked against spend caps.
"""

from __future__ import annotations

import json
import os
import threading
import time
from dataclasses import dataclass, field
from functools import lru_cache

import yaml

from afs_assistant import paths

CONFIG_FILE = paths.ROOT / "config" / "models.yaml"


class SpendCapExceeded(RuntimeError):
    pass


@lru_cache(maxsize=1)
def config() -> dict:
    return yaml.safe_load(CONFIG_FILE.read_text(encoding="utf-8"))


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
    """

    TRANSIENT = ("APIConnectionError", "APITimeoutError", "RateLimitError", "InternalServerError")
    MAX_TIMEOUTS = 2        # a timed-out call is retried once; the second timeout fails the call

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

        last_error: Exception | None = None
        timeouts = 0
        for attempt in range(3):
            self.tracker.check()          # per attempt: a retried call must not run past the cap
            started = time.monotonic()
            try:
                response = self.client.chat.completions.create(
                    model=model, messages=messages, temperature=cfg.get("temperature", 0),
                    max_tokens=role_cfg.get("max_tokens", 8000), response_format=response_format,
                    extra_body=extra, timeout=timeout_s(role),
                )
            except Exception as exc:  # retry only transient API errors
                if type(exc).__name__ not in self.TRANSIENT:
                    raise
                last_error = exc
                if type(exc).__name__ == "APITimeoutError":
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
