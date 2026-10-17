"""Thin clients for keyless scholarly APIs: Europe PMC, OpenAlex, Unpaywall.

Each search returns `Hit`s (metadata plus whatever text the API gives: an abstract, an
open-access url, a PMC id for Europe PMC full text). Fetching and extracting the text is
the step's job. All requests go through `http.Fetcher` (guards, cache, polite intervals).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from afs_assistant.external.http import Fetcher, Unavailable

EPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
EPMC_FULLTEXT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
OPENALEX_WORKS = "https://api.openalex.org/works"
UNPAYWALL = "https://api.unpaywall.org/v2/{doi}"
PAGE_SIZE = 5
MAX_OPENALEX_SEARCHES = 3          # keyless budget is about 100 searches per day per IP
OPENALEX_SELECT = ("id,doi,title,publication_year,authorships,primary_location,best_oa_location,"
                   "open_access,abstract_inverted_index")


@dataclass
class Hit:
    api: str
    query: str
    title: str
    doi: str | None = None
    year: int | None = None
    authors: list[str] = field(default_factory=list)
    venue: str | None = None
    licence: str | None = None
    abstract: str = ""
    landing_url: str = ""
    oa_url: str = ""               # an open-access full-text url (PDF or HTML), if known
    pmcid: str | None = None       # Europe PMC open-access full text available
    retrieved_at: str = ""         # when the search response (with the abstract) was received
    http_status: int | None = None


def clean_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            doi = doi[len(prefix):]
    return doi.lower() or None


def _year(value) -> int | None:
    try:
        return int(str(value)[:4])
    except (TypeError, ValueError):
        return None


# ----------------------------------------------------------------- Europe PMC
def epmc_search(fetcher: Fetcher, query: str, size: int = PAGE_SIZE) -> list[Hit]:
    r = fetcher.get(EPMC_SEARCH, {"query": query, "format": "json", "resultType": "core", "pageSize": size})
    if r.status != 200:
        raise Unavailable(f"HTTP {r.status}", r.url, r.status, fatal=False)
    return _stamp(parse_epmc(r.json(), query), r)


def _stamp(hits: list[Hit], r) -> list[Hit]:
    for h in hits:
        h.retrieved_at, h.http_status = r.retrieved_at, r.status
    return hits


def parse_epmc(data: dict, query: str) -> list[Hit]:
    hits = []
    for item in data.get("resultList", {}).get("result", []):
        doi = clean_doi(item.get("doi"))
        pmcid = item.get("pmcid")
        open_text = item.get("isOpenAccess") == "Y" and item.get("inEPMC") == "Y" and pmcid
        journal = (item.get("journalInfo") or {}).get("journal") or {}
        landing = (f"https://europepmc.org/article/PMC/{pmcid}" if pmcid
                   else f"https://europepmc.org/article/{item.get('source', 'MED')}/{item.get('id', '')}")
        hits.append(Hit(api="europepmc", query=query, title=item.get("title", "").strip(), doi=doi,
                        year=_year(item.get("pubYear")),
                        authors=[a.strip() for a in item.get("authorString", "").rstrip(".").split(",") if a.strip()],
                        venue=journal.get("title"), licence=item.get("license"),
                        abstract=item.get("abstractText", "") or "", landing_url=landing,
                        pmcid=pmcid if open_text else None))
    return hits


def epmc_fulltext(fetcher: Fetcher, pmcid: str):
    r = fetcher.get(EPMC_FULLTEXT.format(pmcid=pmcid), accept="application/xml")
    if r.status != 200:
        raise Unavailable(f"HTTP {r.status}", r.url, r.status, fatal=False)
    return r


# ----------------------------------------------------------------- OpenAlex
def abstract_from_inverted_index(index: dict | None) -> str:
    """Rebuild an abstract from OpenAlex's {word: [positions]} form."""
    if not index:
        return ""
    words: dict[int, str] = {}
    for word, positions in index.items():
        for p in positions:
            words[p] = word
    return " ".join(words[p] for p in sorted(words))


def openalex_search(fetcher: Fetcher, query: str, size: int = PAGE_SIZE) -> tuple[list[Hit], bool]:
    """Returns the hits and whether the keyless budget is used up (stop searching OpenAlex this run)."""
    r = fetcher.get(OPENALEX_WORKS, {"search": query, "per-page": size, "select": OPENALEX_SELECT},
                    email_param="mailto", openalex_key=True)
    if r.status != 200:
        raise Unavailable(f"HTTP {r.status}", r.url, r.status, fatal=False)
    return _stamp(parse_openalex(r.json(), query), r), budget_exhausted(r.headers)


def budget_exhausted(headers: dict[str, str]) -> bool:
    try:
        if headers.get("x-ratelimit-remaining") is not None and int(headers["x-ratelimit-remaining"]) <= 0:
            return True
        remaining, cost = headers.get("x-ratelimit-remaining-usd"), headers.get("x-ratelimit-cost-usd")
        return remaining is not None and cost is not None and float(remaining) < float(cost)
    except ValueError:
        return False


def parse_openalex(data: dict, query: str) -> list[Hit]:
    hits = []
    for w in data.get("results", []):
        best = w.get("best_oa_location") or {}
        primary = w.get("primary_location") or {}
        oa = w.get("open_access") or {}
        source = primary.get("source") or {}
        doi = clean_doi(w.get("doi"))
        hits.append(Hit(api="openalex", query=query, title=(w.get("title") or "").strip(), doi=doi,
                        year=_year(w.get("publication_year")),
                        authors=[(a.get("author") or {}).get("display_name", "") for a in w.get("authorships", [])
                                 if (a.get("author") or {}).get("display_name")],
                        venue=source.get("display_name"), licence=best.get("license") or primary.get("license"),
                        abstract=abstract_from_inverted_index(w.get("abstract_inverted_index")),
                        landing_url=(f"https://doi.org/{doi}" if doi else primary.get("landing_page_url") or ""),
                        oa_url=best.get("pdf_url") or oa.get("oa_url") or best.get("landing_page_url") or ""))
    return hits


# ----------------------------------------------------------------- Unpaywall
def unpaywall(fetcher: Fetcher, doi: str) -> tuple[str, str | None] | None:
    """DOI -> (open-access url, licence), or None. Needs CONTACT_EMAIL; without it Unpaywall is skipped."""
    if not fetcher.email:
        return None
    r = fetcher.get(UNPAYWALL.format(doi=doi), email_param="email")
    if r.status != 200:
        return None
    return parse_unpaywall(r.json())


def parse_unpaywall(data: dict) -> tuple[str, str | None] | None:
    best = data.get("best_oa_location") or {}
    url = best.get("url_for_pdf") or best.get("url") or best.get("url_for_landing_page")
    return (url, best.get("license")) if url else None
