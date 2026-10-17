"""One guarded HTTP GET for all external clients, with a local response cache.

Guards: http/https only, no IP-literal, numeric-shorthand or localhost hosts, and (live, before
every request) every address the host resolves to must be global (no loopback, private or
link-local; DNS rebinding between this check and the connect is an accepted residual risk);
at most MAX_REDIRECTS redirects (each target checked again), at most MAX_BYTES, TIMEOUT_S per
connect/read, REQUEST_DEADLINE_S wall time per request (a slow drip-feed counts), and a
minimum interval per host (polite rate limits). Every response is cached under
runs/external_cache/http/<sha256(public url)>.json (gitignored).

Modes: `live` (network, writes the cache), `cache` (cache only; a miss is unavailable),
`off` (nothing). Any failure raises `Unavailable`. A `fatal` one (network error, timeout,
rate limit, cache miss, mode off) makes the step fall back to the library; a non-fatal one
(blocked url, too large, too many redirects, over the wall deadline, HTTP error status) only
skips that source.
Non-fatal failures are cached too, so `cache` mode replays them the same way.

`CONTACT_EMAIL` (and an optional `OPENALEX_API_KEY`) are read from the environment or .env
and added only to requests that ask for them. The public url (used as the cache key and
in messages) never contains them; request urls are not stored in outputs at all.
"""

from __future__ import annotations

import base64
import hashlib
import ipaddress
import json
import os
import re
import socket
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import httpx

from afs_assistant import paths

TIMEOUT_S = 8.0                 # per connect / read
REQUEST_DEADLINE_S = 15.0       # wall time per request, redirects and body included
MAX_REDIRECTS = 3
MAX_BYTES = 10 * 1024 * 1024
DEFAULT_INTERVAL_S = 0.2
HOST_INTERVAL_S = {"api.crossref.org": 1.0, "export.arxiv.org": 3.0}
SECRET_PARAMS = ("mailto", "email", "api_key")
KEPT_HEADERS = ("content-type", "retry-after", "x-ratelimit-remaining", "x-ratelimit-remaining-usd",
                "x-ratelimit-cost-usd", "x-ratelimit-limit")
MODES = ("live", "cache", "off")
USER_AGENT = "afs-assistant/0.1 (research prototype; scholarly API client)"


class Unavailable(Exception):
    """The request could not be answered (network, timeout, rate limit, blocked url, cache miss, mode off)."""

    def __init__(self, reason: str, url: str = "", status: int | None = None, fatal: bool = True) -> None:
        super().__init__(f"{reason}: {url}" if url else reason)
        self.reason = reason
        self.url = url
        self.status = status
        self.fatal = fatal


class RateLimited(Unavailable):
    pass


@dataclass
class Response:
    url: str                    # public url (no email or key)
    status: int
    headers: dict[str, str]
    content: bytes
    retrieved_at: str           # when the network response was received (kept from the cache in `cache` mode)
    from_cache: bool = False

    @property
    def content_type(self) -> str:
        return self.headers.get("content-type", "").split(";")[0].strip().lower()

    def json(self):
        return json.loads(self.content.decode("utf-8"))


def public_url(url: str | httpx.URL) -> str:
    """The url without secret query parameters (cache key and log form)."""
    u = httpx.URL(str(url))
    params = [(k, v) for k, v in u.params.multi_items() if k not in SECRET_PARAMS]
    return str(u.copy_with(params=params or None)) if params else str(u.copy_with(query=None))


_NUMERIC_LABEL = re.compile(r"[0-9]+|0x[0-9a-f]*")


def blocked_reason(url: httpx.URL) -> str | None:
    """Static checks on the url (no DNS): scheme, local names, IP literals and numeric shorthand hosts."""
    if url.scheme not in ("http", "https"):
        return f"scheme {url.scheme!r} not allowed"
    host = (url.host or "").strip("[]").lower().rstrip(".")
    if not host:
        return "no host"
    if host == "localhost" or host.endswith((".localhost", ".local")):
        return "local host not allowed"
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        return "IP-literal host not allowed"
    # A host whose last label is a number is an IPv4 address to URL parsers and resolvers
    # (127.1, 2130706433, 0x7f.1, 0177.0.0.1); a real top-level domain is never numeric.
    if _NUMERIC_LABEL.fullmatch(host.rsplit(".", 1)[-1]):
        return "numeric host not allowed"
    return None


def resolved_block_reason(host: str) -> str | None:
    """Resolve `host`; a reason if any address is not global. Raises Unavailable (fatal) if DNS fails."""
    host = host.strip("[]").rstrip(".")
    try:
        infos = socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)
    except (OSError, UnicodeError):
        raise Unavailable("network error (DNS lookup failed)", host) from None
    for info in infos:
        address = str(info[4][0])
        try:
            if not ipaddress.ip_address(address).is_global:
                return "host resolves to a non-public address"
        except ValueError:          # e.g. a scoped IPv6 address
            return "host resolves to a non-public address"
    return None if infos else "host does not resolve"


def _load_env() -> None:
    from dotenv import load_dotenv

    load_dotenv(paths.ROOT / ".env")


class Fetcher:
    def __init__(self, mode: str = "live", cache_dir: Path | None = None, transport: httpx.BaseTransport | None = None,
                 email: str | None = None, openalex_key: str | None = None,
                 intervals: dict[str, float] | None = None, default_interval: float = DEFAULT_INTERVAL_S,
                 sleep=time.sleep, monotonic=time.monotonic) -> None:
        if mode not in MODES:
            raise ValueError(f"external mode must be one of {MODES}")
        self.mode = mode
        self.cache_dir = cache_dir or paths.EXTERNAL_CACHE / "http"
        self._transport = transport
        if email is None or openalex_key is None:
            _load_env()
        self.email = email if email is not None else os.environ.get("CONTACT_EMAIL", "")
        self.openalex_key = openalex_key if openalex_key is not None else os.environ.get("OPENALEX_API_KEY", "")
        self.intervals = HOST_INTERVAL_S if intervals is None else intervals
        self.default_interval = default_interval
        self._sleep = sleep
        self._monotonic = monotonic
        self._last: dict[str, float] = {}
        self._client: httpx.Client | None = None

    # ------------------------------------------------------------------ cache
    def _cache_file(self, public: str) -> Path:
        return self.cache_dir / f"{hashlib.sha256(public.encode('utf-8')).hexdigest()}.json"

    def _read_cache(self, public: str) -> Response | None:
        f = self._cache_file(public)
        if not f.exists():
            return None
        d = json.loads(f.read_text(encoding="utf-8"))
        if "error" in d:
            raise Unavailable(d["error"], d["url"], fatal=False)
        return Response(d["url"], d["status"], d["headers"], base64.b64decode(d["body_b64"]), d["retrieved_at"],
                        from_cache=True)

    def _write_cache(self, r: Response) -> None:
        f = self._cache_file(r.url)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"url": r.url, "status": r.status, "headers": r.headers,
                                 "retrieved_at": r.retrieved_at,
                                 "body_b64": base64.b64encode(r.content).decode("ascii")}), encoding="utf-8")

    def _write_error(self, public: str, reason: str) -> None:
        f = self._cache_file(public)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps({"url": public, "error": reason}), encoding="utf-8")

    # ------------------------------------------------------------------ network
    def _http(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(timeout=TIMEOUT_S, follow_redirects=False, transport=self._transport,
                                        headers={"User-Agent": USER_AGENT})
        return self._client

    def _wait(self, host: str) -> None:
        interval = self.intervals.get(host, self.default_interval)
        last = self._last.get(host)
        if last is not None:
            gap = interval - (self._monotonic() - last)
            if gap > 0:
                self._sleep(gap)
        self._last[host] = self._monotonic()

    def get(self, url: str, params: dict | None = None, *, email_param: str | None = None,
            openalex_key: bool = False, accept: str | None = None) -> Response:
        """GET with the guards above. `email_param` names the query parameter for CONTACT_EMAIL (mailto/email)."""
        public_params = dict(params or {})
        try:
            request = httpx.URL(url, params=public_params or None)
        except httpx.InvalidURL:            # e.g. an out-of-range dotted host such as 0177.0.0.1
            raise Unavailable("invalid url", fatal=False) from None
        public = public_url(request)
        if self.mode == "off":
            raise Unavailable("external mode off", public)
        why = blocked_reason(request)
        if why:
            raise Unavailable(why, public, fatal=False)
        if self.mode == "cache":
            cached = self._read_cache(public)
            if cached is None:
                raise Unavailable("cache miss", public)
            return self._checked(cached)

        secret = dict(public_params)
        if email_param and self.email:
            secret[email_param] = self.email
        if openalex_key and self.openalex_key:
            secret["api_key"] = self.openalex_key
        target = httpx.URL(url, params=secret or None)
        headers = {"Accept": accept} if accept else {}
        deadline = self._monotonic() + REQUEST_DEADLINE_S
        late = f"no complete response within {REQUEST_DEADLINE_S:.0f} s"
        for _ in range(MAX_REDIRECTS + 1):
            why = blocked_reason(target) or resolved_block_reason(target.host)
            if why:                         # a blocked target (also after a redirect)
                self._write_error(public, why)
                raise Unavailable(why, public, fatal=False)
            self._wait(target.host)
            if self._monotonic() > deadline:
                self._write_error(public, late)
                raise Unavailable(late, public, fatal=False)
            try:
                with self._http().stream("GET", target, headers=headers) as resp:
                    if resp.is_redirect:
                        location = resp.headers.get("location", "")
                        target = target.join(location)
                        continue
                    body = bytearray()
                    for chunk in resp.iter_bytes():
                        body += chunk
                        if len(body) > MAX_BYTES:
                            self._write_error(public, "response larger than 10 MB")
                            raise Unavailable("response larger than 10 MB", public, fatal=False)
                        if self._monotonic() > deadline:     # a server drip-feeding bytes never hits TIMEOUT_S
                            self._write_error(public, late)
                            raise Unavailable(late, public, fatal=False)
                    kept = {k: resp.headers[k] for k in KEPT_HEADERS if k in resp.headers}
                    result = Response(public, resp.status_code, kept, bytes(body),
                                      datetime.now(UTC).isoformat(timespec="seconds"))
            except httpx.InvalidURL:            # a redirect to a malformed location
                self._write_error(public, "invalid redirect url")
                raise Unavailable("invalid redirect url", public, fatal=False) from None
            except httpx.HTTPError as exc:      # timeouts, connection errors, protocol errors
                raise Unavailable(f"network error ({type(exc).__name__})", public) from None
            self._write_cache(result)
            return self._checked(result)
        self._write_error(public, f"more than {MAX_REDIRECTS} redirects")
        raise Unavailable(f"more than {MAX_REDIRECTS} redirects", public, fatal=False)

    @staticmethod
    def _checked(r: Response) -> Response:
        if r.status == 429:
            raise RateLimited("rate limited (HTTP 429)", r.url, 429)
        return r

    def close(self) -> None:
        if self._client is not None:
            self._client.close()
            self._client = None
