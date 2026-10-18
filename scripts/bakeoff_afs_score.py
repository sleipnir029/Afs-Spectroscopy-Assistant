"""Score bake-off arms on D01-D08 against the AFS-provided evaluation data (no model calls).

AFS data (scenarios/, from the organiser docx): `dev.jsonl` gives each case's `eval_useful_sources` (pages a good
answer draws on) and `eval_facts_stated`; `dev_reference.jsonl` gives worked answers for some cases. Scored here:
- useful-source recall: share of the listed pages that the answer cites with a verified quote;
- worked-answer methods: the methods the worked answer's Recommendation names vs the answer's primary and
  comparison methods (only where a worked answer exists).
`eval_facts_stated` coverage needs reading and is left to the reviewer.

Usage: uv run python scripts/bakeoff_afs_score.py [--root outputs/bakeoff-dev] [ARM ...]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
METHODS = ("NIR", "MIR", "Raman", "UV-Vis", "fluorescence")


def useful_pages(spec: str) -> set[tuple[str, int]]:
    """'S01 p.5, 10, 14–15; S02 p.6' -> {(S01, 5), (S01, 10), (S01, 14), (S01, 15), (S02, 6)}."""
    pages = set()
    for part in spec.split(";"):
        m = re.match(r"\s*(S\d\d)\s+p\.(.*)", part)
        if not m:
            continue
        for item in m.group(2).split(","):
            lo, _, hi = item.strip().replace("–", "-").partition("-")
            for p in range(int(lo), int(hi or lo) + 1):
                pages.add((m.group(1), p))
    return pages


def worked_methods(answer: str) -> set[str]:
    block = answer[answer.find("Recommendation"):answer.find("Measurement concept")]
    heads = re.findall(r"^\s*([^\n.]{2,40})\.\s", block, flags=re.MULTILINE)
    return {m for h in heads for m in METHODS if re.search(rf"\b{re.escape(m)}\b", h, flags=re.IGNORECASE)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="outputs/bakeoff-dev")
    ap.add_argument("arms", nargs="*")
    args = ap.parse_args()
    root = REPO / args.root
    cases = {json.loads(x)["id"]: json.loads(x) for x in (REPO / "scenarios/dev.jsonl").read_text().splitlines()}
    worked = {json.loads(x)["id"]: json.loads(x)["worked_answer"]
              for x in (REPO / "scenarios/dev_reference.jsonl").read_text().splitlines()}
    arms = args.arms or sorted(p.name for p in root.iterdir() if (p / "dev").is_dir())
    print("| arm | " + " | ".join(sorted(cases)) + " | mean recall |\n|" + "---|" * (len(cases) + 2))
    method_rows = []
    for arm in arms:
        cells, recalls = [], []
        for cid in sorted(cases):
            path = root / arm / "dev" / f"{cid}.json"
            if not path.exists():
                cells.append("–")
                continue
            d = json.loads(path.read_text(encoding="utf-8"))
            cited = {(c["doc"], c["page"]) for c in d["verification"]["citations"] if c["verified"]}
            want = useful_pages(cases[cid]["eval_useful_sources"])
            recall = len(want & cited) / len(want) if want else 1.0
            recalls.append(recall)
            cells.append(f"{len(want & cited)}/{len(want)}")
            if cid in worked:
                recs = d["assessment"]["recommendations"]
                used = {r["method"] for r in recs if r.get("role") in ("primary", "comparison")}
                primary = next((r["method"] for r in recs if r.get("role") == "primary"), "-")
                method_rows.append((arm, cid, sorted(worked_methods(worked[cid])), primary, sorted(used)))
        mean = sum(recalls) / len(recalls) if recalls else 0.0
        print(f"| {arm} | " + " | ".join(cells) + f" | {mean:.0%} |")
    print("\n| arm | case | AFS worked answer methods | primary | primary + comparison |\n|---|---|---|---|---|")
    for arm, cid, want, primary, used in method_rows:
        print(f"| {arm} | {cid} | {', '.join(want)} | {primary} | {', '.join(used)} |")


if __name__ == "__main__":
    main()
