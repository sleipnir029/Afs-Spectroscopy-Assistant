"""Render every Mermaid block in assessment Markdown files with mermaid-cli (mmdc).

Usage: uv run python scripts/check_mermaid.py [FILE_OR_DIR ...]   (default: outputs/dev)

Each ```mermaid block is written to a temporary .mmd file and rendered to SVG with
`npx -y @mermaid-js/mermaid-cli`. Exit 0 if all render, 1 if any fails, 2 if mmdc
cannot run at all (e.g. npx missing or the headless browser download failed); then
the offline structural tests in tests/ remain the check.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)
MMDC = ["npx", "-y", "@mermaid-js/mermaid-cli"]
TIMEOUT_S = 300
# mmdc drives a headless browser through puppeteer; use an installed Chrome when puppeteer has none.
BROWSERS = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]


def blocks(paths: list[Path]) -> list[tuple[str, int, str]]:
    found = []
    for path in paths:
        files = sorted(path.glob("*.md")) if path.is_dir() else [path]
        for f in files:
            for n, m in enumerate(BLOCK.finditer(f.read_text(encoding="utf-8")), 1):
                found.append((str(f.relative_to(ROOT) if f.is_relative_to(ROOT) else f), n, m.group(1)))
    return found


def render(chart: str, workdir: Path, name: str) -> tuple[bool, str]:
    src, out = workdir / f"{name}.mmd", workdir / f"{name}.svg"
    src.write_text(chart, encoding="utf-8")
    env = dict(os.environ)
    if "PUPPETEER_EXECUTABLE_PATH" not in env:
        browser = next((b for b in BROWSERS if Path(b).exists()), None)
        if browser:
            env["PUPPETEER_EXECUTABLE_PATH"] = browser
    try:
        proc = subprocess.run([*MMDC, "-q", "-i", str(src), "-o", str(out)], capture_output=True, text=True,
                              timeout=TIMEOUT_S, env=env, check=False)
    except subprocess.TimeoutExpired:
        return False, f"timeout after {TIMEOUT_S} s"
    ok = proc.returncode == 0 and out.exists() and out.stat().st_size > 0
    return ok, error_excerpt(proc.stderr or proc.stdout)


def error_excerpt(text: str, context: int = 3) -> str:
    """The parse-error line and the lines after it (mmdc puts a long stack trace around it); else the tail."""
    lines = text.strip().splitlines()
    for i, line in enumerate(lines):
        if re.search(r"parse error|syntax error|lexical error|error:", line, re.IGNORECASE):
            return "\n".join(lines[i:i + 1 + context])
    return text.strip()[-400:]


def main(argv: list[str]) -> int:
    if shutil.which("npx") is None:
        print("npx not found: mermaid-cli cannot run; the offline structural tests are the check.")
        return 2
    targets = [Path(a).resolve() for a in argv] or [ROOT / "outputs" / "dev"]
    charts = blocks(targets)
    if not charts:
        print("no mermaid blocks found")
        return 1
    failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        # Smoke test: if a trivial chart does not render, mmdc itself cannot run here.
        ok, msg = render("flowchart LR\n    a --> b", work, "smoke")
        if not ok:
            print(f"mermaid-cli cannot run here ({msg}); the offline structural tests are the check.")
            return 2
        for i, (where, n, chart) in enumerate(charts):
            ok, msg = render(chart, work, f"c{i}")
            failed += not ok
            print(f"[{'PASS' if ok else 'FAIL'}] {where} chart {n}" + ("" if ok else f": {msg}"))
    print(f"{len(charts) - failed}/{len(charts)} charts rendered")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
