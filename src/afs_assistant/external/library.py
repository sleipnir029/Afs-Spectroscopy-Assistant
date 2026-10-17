"""The curated external library (`knowledge/external/library.jsonl`): the offline fallback.

One JSON object per line:
  {library_id, title, authors[], year, venue, doi, url, licence, access, retrieved_at,
   sha256 (of the full fetched text), topics[], passages[{para, text, sha256, passage_sha256}]}
Each passage is a verified verbatim quote (<= 400 characters, <= 2 sentences) of
paragraph `para` of the fetched text; `sha256` is that full paragraph's, `passage_sha256`
that of the stored text (so `kb check` and replay detect a hand-edited passage). No full text is
committed. In a run, an entry's paragraphs are its passages (numbered as in the source),
so library quotes verify offline and on a fresh clone. Built by
`scripts/build_external_library.py`. An absent or empty file means no library.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from afs_assistant import paths
from afs_assistant.external.extract import clean_meta
from afs_assistant.external.sources import SourceRecord, policy_problem, sha

MIN_SCORE = 2                       # shared content words between a query and an entry
_WORD = re.compile(r"[a-z0-9][a-z0-9\-]{2,}")
STOPWORDS = frozenset({
    "and", "are", "for", "from", "has", "have", "how", "into", "its", "not", "off", "one", "the", "their",
    "this", "that", "these", "those", "use", "used", "using", "via", "was", "were", "what", "when", "which",
    "with", "within", "without", "can", "could", "may", "between", "based", "data", "study", "studies",
})
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def words(text: str) -> set[str]:
    return {w.strip("-") for w in _WORD.findall(text.lower())} - STOPWORDS - {""}


def load(path: Path | None = None) -> list[dict]:
    f = path or paths.EXTERNAL_LIBRARY
    if not f.exists():
        return []
    return [json.loads(line) for line in f.read_text(encoding="utf-8").splitlines() if line.strip()]


def library_sha(path: Path | None = None) -> str:
    f = path or paths.EXTERNAL_LIBRARY
    return sha(f.read_text(encoding="utf-8") if f.exists() else "")


def entry_words(entry: dict) -> set[str]:
    return words(" ".join([entry.get("title", ""), " ".join(entry.get("topics", [])),
                           *(p["text"] for p in entry.get("passages", []))]))


def search(queries: list[str], entries: list[dict], limit: int) -> list[tuple[dict, str, int]]:
    """Entries sharing >= MIN_SCORE content words with a query: (entry, best query, score), best first."""
    scored = []
    for e in entries:
        ew = entry_words(e)
        best = max(((len(words(q) & ew), q) for q in queries), default=(0, ""))
        if best[0] >= MIN_SCORE:
            scored.append((e, best[1], best[0]))
    scored.sort(key=lambda x: -x[2])
    return scored[:limit]


def to_record(entry: dict, source_id: str, query: str) -> SourceRecord:
    passages = entry["passages"]
    return SourceRecord(
        id=source_id, url=entry.get("url", ""), doi=entry.get("doi"), title=clean_meta(entry["title"], "[title removed]"),
        authors=[clean_meta(a, "[author removed]") for a in entry.get("authors", [])], year=entry.get("year"),
        venue=clean_meta(entry.get("venue"), "[venue removed]") or None,
        licence=entry.get("licence"), access=entry.get("access", "full_text"),
        retrieved_at=entry.get("retrieved_at", ""), retrieval_query=query, api="library", http_status=None,
        sha256=entry["sha256"], paragraphs=[p["text"] for p in passages], library_id=entry["library_id"],
        paragraph_numbers=[int(p["para"]) for p in passages])


def problems(entries: list[dict]) -> list[str]:
    """Static checks for `kb check`: metadata present, every passage short, numbered and hashed."""
    out = []
    ids = [e.get("library_id") for e in entries]
    if len(ids) != len(set(ids)):
        out.append("duplicate library_id")
    for e in entries:
        lid = e.get("library_id", "?")
        for key in ("title", "url", "licence", "access", "retrieved_at"):
            if not e.get(key):
                out.append(f"{lid}: missing {key}")
        if e.get("access") not in ("full_text", "abstract_only"):
            out.append(f"{lid}: access must be full_text or abstract_only")
        if not _HEX64.match(str(e.get("sha256", ""))):
            out.append(f"{lid}: missing sha256 of the fetched text")
        if not e.get("passages"):
            out.append(f"{lid}: no passages")
        numbers = [p.get("para") for p in e.get("passages", [])]
        if len(numbers) != len(set(numbers)):
            out.append(f"{lid}: two passages with the same paragraph number")
        for p in e.get("passages", []):
            where = f"{lid} ¶{p.get('para')}"
            if not isinstance(p.get("para"), int) or p["para"] < 1:
                out.append(f"{where}: bad paragraph number")
            if not _HEX64.match(str(p.get("sha256", ""))):
                out.append(f"{where}: passage without sha256")
            text = p.get("text", "")
            if p.get("passage_sha256") != sha(text):
                out.append(f"{where}: passage_sha256 missing or not the sha256 of the passage text")
            if len(text) < 12:
                out.append(f"{where}: passage too short")
            why = policy_problem(text)
            if why:
                out.append(f"{where}: {why}")
    return out


# ----------------------------------------------------------------- build (scripts/build_external_library.py)
OPENALEX_WORK = "https://api.openalex.org/works/doi:{doi}"
SPEC_KEYS = ("library_id", "title", "authors", "year", "venue", "doi", "licence", "topics")


def fetch_spec_text(spec: dict, fetcher) -> tuple[list[str], str, str, str]:
    """Fetch the text an entry spec names: (paragraphs, access, url, retrieved_at). Raises ValueError on failure.

    `source` is one of {pmcid: PMC...} (Europe PMC full text), {url: ...} (open-access HTML or PDF) or
    {abstract: openalex} (the OpenAlex abstract of `doi`, for a closed paper: access abstract_only).
    """
    from afs_assistant.external import clients, extract

    source = spec.get("source") or {}
    if source.get("pmcid"):
        r = clients.epmc_fulltext(fetcher, source["pmcid"])
        raw, access, url = extract.xml_paragraphs(r.content), "full_text", \
            f"https://europepmc.org/article/PMC/{source['pmcid']}"
    elif source.get("url"):
        r = fetcher.get(source["url"])
        if r.status != 200:
            raise ValueError(f"HTTP {r.status}")
        raw, access, url = extract.paragraphs_for(r.content, r.content_type, source["url"]), "full_text", source["url"]
    elif source.get("abstract") == "openalex" and spec.get("doi"):
        r = fetcher.get(OPENALEX_WORK.format(doi=spec["doi"]), email_param="mailto", openalex_key=True)
        if r.status != 200:
            raise ValueError(f"HTTP {r.status}")
        raw = [clients.abstract_from_inverted_index(r.json().get("abstract_inverted_index"))]
        access, url = "abstract_only", f"https://doi.org/{spec['doi']}"
    else:
        raise ValueError("source must give pmcid, url, or abstract: openalex with a doi")
    paragraphs, _ = extract.clean(raw)
    if paragraphs is None:
        raise ValueError(f"under {extract.MIN_CHARS} characters of text extracted")
    return paragraphs, access, url, r.retrieved_at


def build_entry(spec: dict, fetcher) -> tuple[dict | None, list[str]]:
    """Fetch the spec's source, verify each chosen passage verbatim, and return (entry, problems).

    A passage is stored as the matched span of the fetched paragraph (the source's own text), with that
    paragraph's number and sha256. Any failing passage fails the entry (None): nothing unverified is written.
    """
    from afs_assistant import quotes
    from afs_assistant.external.http import Unavailable
    from afs_assistant.external.sources import full_text_sha

    lid = spec.get("library_id", "?")
    try:
        paragraphs, access, url, retrieved_at = fetch_spec_text(spec, fetcher)
    except (Unavailable, ValueError) as exc:
        return None, [f"{lid}: fetch failed ({exc})"]
    problems, passages = [], []
    for text in spec.get("passages", []):
        why = policy_problem(text)
        if why:
            problems.append(f"{lid}: {why}: {text[:60]!r}")
            continue
        for number, para in enumerate(paragraphs, 1):
            check = quotes.verify_text(para, text, sha(para))
            if check.ok:
                passage = para[check.start:check.end]
                passages.append({"para": number, "text": passage, "sha256": sha(para),
                                 "passage_sha256": sha(passage)})
                break
        else:
            problems.append(f"{lid}: passage not found verbatim: {text[:60]!r}")
    if not spec.get("passages"):
        problems.append(f"{lid}: no passages chosen")
    if problems:
        return None, problems
    entry = {k: spec.get(k) for k in SPEC_KEYS}
    entry.update({"url": url, "access": access, "retrieved_at": retrieved_at, "sha256": full_text_sha(paragraphs),
                  "passages": sorted(passages, key=lambda p: p["para"])})
    entry["authors"] = list(entry["authors"] or [])
    entry["topics"] = list(entry["topics"] or [])
    return entry, problems


def write(entries: list[dict], path: Path | None = None) -> None:
    f = path or paths.EXTERNAL_LIBRARY
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text("".join(json.dumps(e, ensure_ascii=False, sort_keys=True) + "\n"
                         for e in sorted(entries, key=lambda e: e["library_id"])), encoding="utf-8")
