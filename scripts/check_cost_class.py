"""Cross-check every rendered cost class against knowledge/table1_methods.json.

Usage: uv run python scripts/check_cost_class.py [DIR ...]   (default: outputs/dev)

For each <id>.json + <id>.md pair: re-derive each option's cost class straight from
the Table 1 rows (independently of afs_assistant.options), then compare it with the
cost cell of the rendered options table and with `option_costs` in the run JSON.
Exit 0 if all agree, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from afs_assistant.screen import METHOD_IDS, TECHNIQUES

ORDER = ["low", "average", "high"]
ROW = re.compile(r"^\| (O\d+) \| [^|]+ \| (?:[^|\\]|\\.)* \| ((?:[^|\\]|\\.)*) \|")


def expected(assessment: dict, table: list[dict]) -> dict[str, tuple[str | None, list[int]]]:
    recs = {r["id"]: r for r in assessment["recommendations"]}
    result = {}
    for o in assessment["solution_options"]:
        used = [recs[i] for i in o["recommendation_ids"] if i in recs]
        rows = set()
        for r in used:
            for row in table:
                technique, in_line = TECHNIQUES[row["measurement_technique"]]
                if in_line and METHOD_IDS[row["method"]] == r["method"] and technique == r["technique"]:
                    rows.add(row["row"])
        costs = [next(x["cost"] for x in table if x["row"] == n) for n in rows]
        top = max(costs, key=ORDER.index) if costs else None
        result[o["id"]] = (top, sorted(rows))
    return result


def rendered(markdown: str) -> dict[str, str]:
    section = markdown.split("## Solution options", 1)[1].split("\n## ", 1)[0] if "## Solution options" in markdown else ""
    return {m.group(1): m.group(2).strip() for line in section.splitlines() if (m := ROW.match(line))}


def check_pair(json_path: Path, md_path: Path, table: list[dict]) -> list[str]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    want = expected(data["assessment"], table)
    cells = rendered(md_path.read_text(encoding="utf-8"))
    stored = data.get("option_costs", {})
    problems = []
    for oid, (top, rows) in want.items():
        cell = cells.get(oid)
        if cell is None:
            problems.append(f"{oid}: no rendered row")
            continue
        if top is None:
            if not cell.startswith("not rated in S01 Table 1"):
                problems.append(f"{oid}: expected 'not rated', rendered {cell!r}")
        else:
            m = re.match(r"(low|average|high) \(rows? ([\d, ]+)\)", cell)
            got = (m.group(1), sorted(int(x) for x in m.group(2).split(","))) if m else None
            if got != (top, rows):
                problems.append(f"{oid}: expected {top} rows {rows}, rendered {cell!r}")
        s = stored.get(oid)
        if s is None or s["cost_class"] != top or sorted(r["row"] for r in s["rows"]) != rows:
            problems.append(f"{oid}: run JSON option_costs {s} disagrees with {top} rows {rows}")
    if re.search(r"[€$£]\s*\d|\b\d+(?:[.,]\d+)?\s*(?:EUR|USD|euros?|dollars?)\b", "\n".join(cells.values())):
        problems.append("currency in a cost cell")
    return problems


def main(argv: list[str]) -> int:
    table = json.loads((ROOT / "knowledge" / "table1_methods.json").read_text(encoding="utf-8"))["rows"]
    dirs = [Path(a) for a in argv] or [ROOT / "outputs" / "dev"]
    total = bad = 0
    for d in dirs:
        for json_path in sorted(d.glob("*.json")):
            md_path = json_path.with_suffix(".md")
            if not md_path.exists():
                continue
            total += 1
            problems = check_pair(json_path, md_path, table)
            bad += bool(problems)
            print(f"[{'FAIL' if problems else 'PASS'}] {json_path.name}" + "".join(f"\n  - {p}" for p in problems))
    print(f"{total - bad}/{total} files agree with S01 Table 1")
    return 1 if bad or not total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
