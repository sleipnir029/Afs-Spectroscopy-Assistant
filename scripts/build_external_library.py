"""Build or update the curated external library (knowledge/external/library.jsonl).

Usage: uv run python scripts/build_external_library.py --input SPEC.yaml [--out FILE] [--dry-run]

SPEC.yaml is a list of entries we chose by hand (generic topics only; never built from
held-out scenario text):

    - library_id: pat-data-fusion-review          # stable id, lowercase words and hyphens
      title: "..."
      authors: ["A. Author", "B. Author"]
      year: 2022
      venue: "Journal"
      doi: "10.xxxx/yyyy"
      licence: "cc-by"                            # as the publisher / Europe PMC states it; "unknown" if none
      topics: ["data fusion", "process analytical technology"]
      source: {pmcid: "PMC1234567"}               # or {url: "https://..."} (OA HTML/PDF)
                                                  # or {abstract: openalex} (closed paper: abstract only, needs doi)
      passages:                                   # 1-4 verbatim passages, each <= 400 characters, <= 2 sentences
        - "Exact sentence copied from the paper."

The script fetches each source live (CONTACT_EMAIL from .env as mailto/email only), extracts
the text exactly as a run does, and verifies every passage verbatim. An entry with any
failing passage is not written. Written per entry: metadata, licence, access, retrieved_at
(real clock), sha256 of the fetched text, and the passages with their paragraph number and
the paragraph's sha256. No full text is written to the library; the fetched text stays in
the local cache under runs/external_cache/ (gitignored). Entries with the same library_id
are replaced; others are kept. Exit 1 if any entry failed.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from afs_assistant import paths
from afs_assistant.external import library
from afs_assistant.external.http import Fetcher


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--input", required=True, help="YAML list of entry specs")
    parser.add_argument("--out", default=str(paths.EXTERNAL_LIBRARY))
    parser.add_argument("--dry-run", action="store_true", help="verify only; do not write")
    args = parser.parse_args(argv)

    specs = yaml.safe_load(Path(args.input).read_text(encoding="utf-8")) or []
    out = Path(args.out)
    existing = {e["library_id"]: e for e in library.load(out)}
    fetcher = Fetcher("live")
    failed = []
    try:
        for spec in specs:
            entry, problems = library.build_entry(spec, fetcher)
            if entry is None:
                failed.append(spec.get("library_id", "?"))
                for p in problems:
                    print(f"FAIL {p}")
                continue
            existing[entry["library_id"]] = entry
            print(f"ok   {entry['library_id']}: {len(entry['passages'])} passage(s), {entry['access']}, "
                  f"sha256 {entry['sha256'][:12]}")
    finally:
        fetcher.close()
    problems = library.problems(list(existing.values()))
    for p in problems:
        print(f"FAIL {p}")
    if not args.dry_run and not problems:
        library.write(list(existing.values()), out)
        print(f"wrote {len(existing)} entries to {out}")
    return 1 if failed or problems else 0


if __name__ == "__main__":
    sys.exit(main())
