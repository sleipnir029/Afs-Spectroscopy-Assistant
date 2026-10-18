"""Readable activity notes for a live run (the web UI's progress feed).

`note(text)` is a no-op unless the current thread has a sink, so the CLI and set runs are unchanged.
The UI's job thread sets one with `with sink(job.add_note): ...`; the pipeline and the external step
call `note` at the points a person watching would care about (what was understood, screened, checked).
"""
from __future__ import annotations

import threading
from collections.abc import Callable, Iterator
from contextlib import contextmanager

_local = threading.local()


@contextmanager
def sink(callback: Callable[[str], None]) -> Iterator[None]:
    previous = getattr(_local, "sink", None)
    _local.sink = callback
    try:
        yield
    finally:
        _local.sink = previous


def note(text: str) -> None:
    callback = getattr(_local, "sink", None)
    if callback is not None:
        try:
            callback(" ".join(str(text).split()))
        except Exception:           # noqa: BLE001, S110 - a display problem must never stop a run
            pass


def plural(n: int, word: str, many: str | None = None) -> str:
    return f"{n} {word if n == 1 else many or word + 's'}"
