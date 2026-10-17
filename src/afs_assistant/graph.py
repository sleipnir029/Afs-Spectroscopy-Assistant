"""Knowledge graph over methods, techniques, sample types, fibers, rules and source pages.

Built deterministically from knowledge/{table1_methods,fibers}.json, rules.yaml and
pages.jsonl, and saved as networkx node-link JSON (knowledge/graph.json). The graph is
used to look things up and to explain checks; the checks themselves live in screen.py,
fibers.py, quotes.py and scope.py.

Node ids: method:NIR, technique:ATR, sample_type:liquid, fiber:cir_chalcogenide,
rule:R-FIB-1, page:S01:10, table_row:7.
Edge `rel` values: has_technique, suits_sample, row_of, uses_technique, transmits_for,
applies_to, targets, supported_by, cites.
"""

from __future__ import annotations

import json
from functools import lru_cache

import networkx as nx

from afs_assistant import kb, paths
from afs_assistant.fibers import METHOD_RANGES_UM, coverage
from afs_assistant.screen import METHOD_IDS, TECHNIQUES


def _value_list(value) -> list:
    return value if isinstance(value, list) else [value]


def build() -> nx.MultiDiGraph:
    g = nx.MultiDiGraph()

    for (doc, number), rec in kb.pages().items():
        g.add_node(f"page:{doc}:{number}", kind="page", doc=doc, page=number,
                   label=kb.citation_label(doc, number), title=rec["title"], scope=rec["scope"],
                   sha256=rec["sha256"])

    for method, info in METHOD_RANGES_UM.items():
        g.add_node(f"method:{method}", kind="method", label=method,
                   range_um=list(info["range_um"]), range_source=info["source"], range_basis=info["basis"])

    for row in kb.table1():
        method = METHOD_IDS[row["method"]]
        technique, in_line = TECHNIQUES[row["measurement_technique"]]
        row_id = f"table_row:{row['row']}"
        g.add_node(row_id, kind="table_row", label=f"{row['method']} / {row['measurement_technique']}",
                   citation=row["citation"], in_line=in_line,
                   **{k: row[k] for k in ("physical_phenomenon", "optical_path_or_depth", "sensitivity",
                                          "selectivity", "cost", "min_mm", "max_mm")})
        g.add_node(f"technique:{technique}", kind="technique", label=technique)
        if not g.has_edge(f"method:{method}", f"technique:{technique}"):
            g.add_edge(f"method:{method}", f"technique:{technique}", rel="has_technique")
        g.add_edge(row_id, f"method:{method}", rel="row_of")
        g.add_edge(row_id, f"technique:{technique}", rel="uses_technique")
        g.add_edge(row_id, "page:S01:6", rel="cites")
        for sample_type in row["sample_types"]:
            g.add_node(f"sample_type:{sample_type}", kind="sample_type", label=sample_type)
            g.add_edge(row_id, f"sample_type:{sample_type}", rel="suits_sample")

    for f in kb.fibers():
        node = f"fiber:{f['id']}"
        g.add_node(node, kind="fiber", label=f["name"], family=f["family"],
                   window_um=[f["min_um"], f["max_um"]], vendor_context=f["vendor_context"],
                   discrepancy=f.get("discrepancy", ""))
        for s in f["sources"]:
            g.add_edge(node, f"page:{s['doc']}:{s['page']}", rel="supported_by", quote=s["quote"])
    for method, info in METHOD_RANGES_UM.items():
        for c in coverage(*info["range_um"]):
            if c.status != "none":
                g.add_edge(f"fiber:{c.fiber_id}", f"method:{method}", rel="transmits_for",
                           coverage=c.status, overlap_um=list(c.overlap_um))

    for r in kb.rules():
        node = f"rule:{r['id']}"
        g.add_node(node, kind="rule", label=r["id"], statement=r["statement"], effect=r["effect"],
                   when=r.get("when", {}), target=r.get("target", {}))
        when = r.get("when", {})
        for m in _value_list(when.get("method", [])):
            g.add_edge(node, f"method:{m}", rel="applies_to")
        for key, prefix in (("technique", "technique"),):
            for t in _value_list(r.get("target", {}).get(key, [])) + _value_list(when.get(key, [])):
                if g.has_node(f"{prefix}:{t}"):
                    g.add_edge(node, f"{prefix}:{t}", rel="targets")
        for fam in _value_list(r.get("target", {}).get("fiber_family", [])):
            for f in kb.fibers():
                if f["family"] == fam:
                    g.add_edge(node, f"fiber:{f['id']}", rel="targets")
        for s in r["sources"]:
            g.add_edge(node, f"page:{s['doc']}:{s['page']}", rel="supported_by", quote=s["quote"])
    return g


def save(g: nx.MultiDiGraph) -> None:
    data = nx.node_link_data(g, edges="edges")
    paths.GRAPH_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                                encoding="utf-8")


@lru_cache(maxsize=1)
def load() -> nx.MultiDiGraph:
    data = json.loads(paths.GRAPH_FILE.read_text(encoding="utf-8"))
    return nx.node_link_graph(data, multigraph=True, directed=True, edges="edges")


def neighbors(node: str, rel: str | None = None) -> list[dict]:
    """Outgoing and incoming neighbours of a node, optionally filtered by relation."""
    g = load()
    out = []
    for _, dst, data in g.out_edges(node, data=True):
        if rel is None or data.get("rel") == rel:
            out.append({"direction": "out", "node": dst, **data, "label": g.nodes[dst].get("label")})
    for src, _, data in g.in_edges(node, data=True):
        if rel is None or data.get("rel") == rel:
            out.append({"direction": "in", "node": src, **data, "label": g.nodes[src].get("label")})
    return out
