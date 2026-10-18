"""Shared test setup: tests that need the supplied page text skip in a fresh clone.

knowledge/pages.jsonl (the full text of the organiser materials) is not distributed; `afs-assist kb build`
recreates it from resources/materials/. Without it, a test that reads the pages is skipped with that hint:
- tests marked `needs_pages` (they need the pages but catch the error themselves, e.g. a background job);
- any other test whose setup or body raises `kb.PagesMissing`.
With the file present, nothing here changes a test: a `kb.PagesMissing` raised then is a real failure.
"""

from __future__ import annotations

import pytest

from afs_assistant import kb

# Decided once at load: tests that monkeypatch the pages path must not turn failures into skips.
PAGES_PRESENT = kb.pages_available()


def pytest_configure(config):
    config.addinivalue_line("markers", f"needs_pages: skipped when knowledge/pages.jsonl is absent ({kb.PAGES_MISSING_HINT})")


def pytest_collection_modifyitems(config, items):
    if PAGES_PRESENT:
        return
    skip = pytest.mark.skip(reason=kb.PAGES_MISSING_HINT)
    for item in items:
        if item.get_closest_marker("needs_pages"):
            item.add_marker(skip)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_setup(item):
    try:
        return (yield)
    except kb.PagesMissing:
        if PAGES_PRESENT:
            raise
        pytest.skip(kb.PAGES_MISSING_HINT)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item):
    try:
        return (yield)
    except kb.PagesMissing:
        if PAGES_PRESENT:
            raise
        pytest.skip(kb.PAGES_MISSING_HINT)
