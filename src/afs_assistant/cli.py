"""Command-line entry point: `uv run afs-assist ...`."""

from __future__ import annotations

import argparse
import sys


def _kb_build(_: argparse.Namespace) -> int:
    from afs_assistant import graph, kb, kb_build

    if not kb_build.paths.MATERIALS.exists():
        print("resources/materials/ not found: unzip the organizer materials.zip into resources/ first.")
        return 2
    counts = kb_build.build_all()
    for cache in (kb.pages, kb.rules, kb.fibers, kb.table1):
        cache.cache_clear()
    g = graph.build()
    graph.save(g)
    print(f"pages: {counts}")
    print(f"graph: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")
    return 0


def _kb_check(_: argparse.Namespace) -> int:
    from afs_assistant import kb_check

    findings = kb_check.run()
    for f in findings:
        print(f"[{'PASS' if f.ok else 'FAIL'}] {f.check}: {f.detail}")
    return 0 if all(f.ok for f in findings) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="afs-assist")
    sub = parser.add_subparsers(dest="command", required=True)
    kb_parser = sub.add_parser("kb", help="knowledge base commands")
    kb_sub = kb_parser.add_subparsers(dest="kb_command", required=True)
    kb_sub.add_parser("build", help="rebuild knowledge/ from resources/").set_defaults(func=_kb_build)
    kb_sub.add_parser("check", help="validate knowledge/").set_defaults(func=_kb_check)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
