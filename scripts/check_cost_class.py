"""Cross-check every rendered cost class against knowledge/table1_methods.json.

Usage: uv run python scripts/check_cost_class.py [DIR ...]   (default: outputs/dev)

For each <id>.json + <id>.md pair: re-derive each option's cost class straight from
the Table 1 rows (independently of afs_assistant: the name mappings below are this
script's own copy), then compare it with the cost cell of the rendered options table
and with `option_costs` in the run JSON. Also scans the Markdown for any currency sign,
code or word, except the "Evidence (verified quotes)" section (verbatim supplied quotes,
e.g. a journal abbreviation). Exit 0 if all agree, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Own copy of the S01 Table 1 name mappings (independent of afs_assistant.screen, review N10).
METHOD_IDS = {
    "IR spectroscopy": "MIR",
    "NIR spectroscopy": "NIR",
    "Raman spectroscopy": "Raman",
    "UV/Visible spectroscopy": "UV-Vis",
    "Fluorimetry": "Fluorescence",
}
# Table 1 technique -> (technique id, usable in-line at a process point)
TECHNIQUES = {
    "ATR platform": ("ATR", False),
    "ATR probe*": ("ATR", True),
    "ATR probe": ("ATR", True),
    "cuvette": ("cuvette", False),
    "cuvette 90 deg": ("cuvette", False),
    "sample layer": ("thin_film_transmission", False),
    "sample surface": ("diffuse_reflection", False),
    "transmission or transflection probe": ("transmission_transflection", True),
    "diffuse reflection probe": ("diffuse_reflection", True),
    "integrating sphere": ("diffuse_reflection", False),
    "surface at a distance": ("diffuse_reflection_remote", True),
    "Raman probe": ("raman_probe", True),
    "probe, lens": ("emission_probe", True),
    "fluorimetric probe": ("fluorescence_probe", True),
}

ORDER = ["low", "average", "high"]
CELL = r"(?:[^|\\]|\\.)*"
# | ID | Tier | Methods | Confidence | Cost class | ...
ROW = re.compile(rf"^\| (O\d+) \| [^|]+ \| {CELL} \| {CELL} \| ({CELL}) \|")
# Codes in any case, except before a journal abbreviation such as "Eur. Urol." (a dot and a capital).
CURRENCY = re.compile(r"[€$£]|\b(?:eur|usd|gbp|chf)\b(?!\.\s?(?-i:[A-Z]))|\beuros?\b|\bdollars?\b", re.IGNORECASE)
# A section from its heading (any level) to the next heading of any level.
SOLUTION_OPTIONS = re.compile(r"^#+ Solution options\n(.*?)(?=^#|\Z)", re.MULTILINE | re.DOTALL)
EVIDENCE = re.compile(r"^#+ Evidence \(verified quotes\)\n.*?(?=^#|\Z)", re.MULTILINE | re.DOTALL)


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
    m = SOLUTION_OPTIONS.search(markdown)
    section = m.group(1) if m else ""
    return {m.group(1): m.group(2).strip() for line in section.splitlines() if (m := ROW.match(line))}


def check_pair(json_path: Path, md_path: Path, table: list[dict]) -> list[str]:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    want = expected(data["assessment"], table)
    markdown = md_path.read_text(encoding="utf-8")
    cells = rendered(markdown)
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
            m = re.match(r"(low|average|high) cost \(rows? ([\d, ]+)\)", cell)
            got = (m.group(1), sorted(int(x) for x in m.group(2).split(","))) if m else None
            if got != (top, rows):
                problems.append(f"{oid}: expected {top} rows {rows}, rendered {cell!r}")
        s = stored.get(oid)
        if s is None or s["cost_class"] != top or sorted(r["row"] for r in s["rows"]) != rows:
            problems.append(f"{oid}: run JSON option_costs {s} disagrees with {top} rows {rows}")
    scanned = EVIDENCE.sub("", markdown)
    for m in CURRENCY.finditer(scanned):
        problems.append(f"currency in the Markdown: {scanned[max(0, m.start() - 40):m.end() + 40]!r}")
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
