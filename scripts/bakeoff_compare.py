"""Compare 5.8 bake-off arms case by case (no model calls).

Reads outputs/bakeoff/<arm>/<set>/<case>.json and prints a Markdown table per case plus arm totals:
wall time, cost, completion tokens, runaways (replies discarded at max_tokens / invalid JSON), timeouts,
hard failures, citations verified/total, repair rounds, finalize fallbacks, primary method, questions.

Usage: uv run python scripts/bakeoff_compare.py [ARM ...]   (default: every arm folder)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "outputs" / "bakeoff"


def row(path: Path) -> dict:
    d = json.loads(path.read_text(encoding="utf-8"))
    calls, m, a = d.get("calls", []), d["manifest"], d.get("assessment") or {}
    primary = next((r for r in a.get("recommendations", []) if r.get("role") == "primary"), None)
    words = len(path.with_suffix(".md").read_text(encoding="utf-8").split()) if path.with_suffix(".md").exists() else 0
    return {
        "wall_s": d["timings_s"].get("wall", 0.0),
        "cost": sum(c.get("cost_usd", 0.0) for c in calls),
        "out_tok": sum(c.get("completion_tokens", 0) for c in calls),
        "assess_tok": max((c.get("completion_tokens", 0) for c in calls if c["role"] in ("assess", "repair")), default=0),
        "runaways": sum(1 for c in calls if c["role"].endswith(":discarded")),
        "timeouts": sum(1 for c in calls if c["role"].endswith(":timeout")),
        "hard": m["verification"]["hard_failures"] if m.get("verification") else None,
        "cit": f"{m['verification']['citations_verified']}/{m['verification']['citations_total']}"
               if m.get("verification") else "-",
        "repairs": m.get("repair_rounds", 0),
        "fallbacks": len(m.get("finalize_fallbacks", [])),
        "removed": len(d.get("removed_citations", [])),
        "primary": f"{primary['method']} {primary['technique']}" if primary else "-",
        "questions": len(a.get("clarification_questions", [])),
        "words": words,
    }


def main(arms: list[str]) -> None:
    arms = arms or sorted(p.name for p in ROOT.iterdir() if p.is_dir() and p.name != "smoke")
    cases = sorted({f"{p.parent.name}/{p.stem}" for arm in arms for p in (ROOT / arm).glob("*/*.json")})
    cols = ["wall_s", "cost", "out_tok", "assess_tok", "runaways", "timeouts", "hard", "cit", "repairs",
            "fallbacks", "removed", "primary", "questions", "words"]
    totals = {arm: {"cases": 0, "failed": 0, "wall_s": 0.0, "cost": 0.0, "runaways": 0, "timeouts": 0, "hard": 0}
              for arm in arms}
    for case in cases:
        print(f"\n### {case}\n\n| arm | " + " | ".join(cols) + " |\n|" + "---|" * (len(cols) + 1))
        for arm in arms:
            path = ROOT / arm / f"{case}.json"
            if not path.exists():
                print(f"| {arm} | " + " | ".join(["(no output)"] + [""] * (len(cols) - 1)) + " |")
                totals[arm]["failed"] += 1
                continue
            r = row(path)
            t = totals[arm]
            t["cases"] += 1
            for k in ("wall_s", "cost", "runaways", "timeouts"):
                t[k] += r[k]
            t["hard"] += r["hard"] or 0
            cells = [f"{r[c]:.0f}" if c == "wall_s" else f"${r[c]:.3f}" if c == "cost" else str(r[c]) for c in cols]
            print(f"| {arm} | " + " | ".join(cells) + " |")
    print("\n### Totals\n\n| arm | cases | no output | mean wall s | max wall s | mean $/case | runaways | timeouts | hard |")
    print("|---|---|---|---|---|---|---|---|---|")
    for arm in arms:
        t = totals[arm]
        n = t["cases"] or 1
        walls = [row(p)["wall_s"] for p in (ROOT / arm).glob("*/*.json")]
        print(f"| {arm} | {t['cases']} | {t['failed']} | {t['wall_s'] / n:.0f} | {max(walls, default=0):.0f} | "
              f"${t['cost'] / n:.3f} | {t['runaways']} | {t['timeouts']} | {t['hard']} |")


if __name__ == "__main__":
    main(sys.argv[1:])
