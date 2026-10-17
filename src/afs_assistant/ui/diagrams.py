"""Inline SVG figures for the web UI, drawn by code from the run and the knowledge base.

- `schematic` (wide) and `setup` (narrow): one solution option as process point -> probe(s) -> fiber ->
  spectrometer -> model -> result, auxiliary sensors dashed into the model (the structure of
  `render.mermaid_chart`). Nodes carry `data-part` so the page can highlight matching parts.
- `spectral`: the stated method ranges (`RANGES`, every printed number is on the cited page; a range
  the sources do not state gets no number and no bar) and the fiber windows that cover the proposed
  method (`knowledge/fibers.json`, S02 p.6, printed as the slide labels them), on one log axis.
- `parameter_map`: each parameter linked to how it is measured.
All SVG text is at least 12 px at the figure's native width; the page never shows a figure below it.
Colours are CSS classes (theme tokens in app.css).
"""

from __future__ import annotations

import itertools
import math
import re
import textwrap
from html import escape

from afs_assistant import kb
from afs_assistant.fibers import method_fiber_coverage
from afs_assistant.options import TECHNIQUE_LABEL, is_fusion, method_label, option_parts
from afs_assistant.render import fiber_label
from afs_assistant.schema import Assessment, SolutionOption

TEXT = 13.0          # px, node text
SMALL = 12.0         # px, captions, ticks, sub-labels (the floor)
CHAR_W = 0.56        # average glyph width in em (IBM Plex Sans, mixed case)
LINE = 1.3
MAX_AUX = 3
_ids = itertools.count(1)

# Line-art icons (24x24, stroke): our own drawings.
ICONS = {
    "proc": "M2 9h20M2 15h20M6 9v6M18 9v6",
    "probe": "M12 2v12M9 14h6l-1 6h-4zM9 6h6",
    "fiber": "M3 12c3-6 6 6 9 0s6 6 9 0",
    "spec": "M3 6h18v12H3zM7 10h4M7 14h10",
    "model": "M4 20V4M4 20h16M7 15l4-4 3 3 5-6",
    "result": "M4 18a8 8 0 1 1 16 0M12 18l4-6",
    "aux": "M10 4a2 2 0 1 1 4 0v10a4 4 0 1 1-4 0z",
}


def _wrap(text: str, width_px: float, max_lines: int, size: float) -> list[str]:
    chars = max(6, int(width_px / (size * CHAR_W)))
    lines = textwrap.wrap(" ".join(str(text).split()), chars, break_long_words=False) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(1, chars - 1)].rstrip(" ,;:.") + "…"
    return lines


def _text(x: float, y: float, lines: list[str], cls: str, size: float, anchor: str = "start") -> str:
    spans = "".join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * LINE:.1f}">{escape(t)}</tspan>'
                    for i, t in enumerate(lines))
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{spans}</text>'


def _svg(width: float, height: float, body: list[str], label: str, cls: str) -> str:
    return (f'<svg class="fig {cls}" viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" '
            f'height="{height:.0f}" role="img" aria-label="{escape(label)}" xmlns="http://www.w3.org/2000/svg">'
            f'{"".join(body)}</svg>')


def _marker() -> tuple[str, str]:
    mid = f"arr{next(_ids)}"
    return mid, (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                 f'markerHeight="7" orient="auto-start-reverse"><path class="dg-head" d="M0,1 L9,5 L0,9 z"/>'
                 f'</marker></defs>')


# ------------------------------------------------------------------------------------- option nodes
def option_nodes(a: Assessment, option: SolutionOption, slots: dict) -> dict:
    """The parts of one option's setup, shared by the wide schematic and the narrow sketch."""
    recs = {r.id: r for r in a.recommendations}
    params = {p.id: p for p in a.parameters}
    used = [params[i] for i in option.parameter_ids if i in params]
    parts = option_parts(option, recs)
    fused = len(parts) <= 1 or is_fusion(option, recs)
    lanes = []
    for method, technique in parts:
        probe = TECHNIQUE_LABEL.get(technique, "technique not specified") if technique else "technique not specified"
        lanes.append({"method": method, "probe_title": f"{method} probe" if method not in probe else probe,
                      "probe_sub": probe if method not in probe else "", "label": method_label(method, technique),
                      "fiber": fiber_label(method, slots).removeprefix("Fiber: ")})
    spectro = [p.name for p in used if p.measured_by.type == "spectroscopy"] or [p.name for p in used]
    aux = [p.measured_by.sensor or p.name for p in used if p.measured_by.type == "auxiliary_sensor"]
    if len(aux) > MAX_AUX:
        aux = aux[:MAX_AUX - 1] + [f"{aux[MAX_AUX - 1]}; and {len(aux) - MAX_AUX + 1} more"]
    return {"location": a.measurement_concept.location, "lanes": lanes, "fused": fused, "aux": aux,
            "model": ("Chemometric model" if len(parts) <= 1 else "Data fusion model") if fused else "",
            "model_sub": "per-method calibration" if fused and len(parts) > 1 else "",
            "result": ", ".join(spectro) or "measured parameters"}


def schematic(a: Assessment, option: SolutionOption, slots: dict, width: float = 760.0) -> str:
    """Wide layout: icon nodes left to right, one row per method; auxiliary sensors on top, dashed."""
    n = option_nodes(a, option, slots)
    cols, icon = 6, 48.0
    col_w = width / cols
    text_w = col_w - 10
    top_pad = 4.0 + (len(n["aux"]) * 8 + 6 if n["aux"] else 0)

    def block_h(title: str, sub: str) -> float:
        return icon + 8 + TEXT * LINE * len(_wrap(title, text_w, 2, TEXT)) + SMALL * LINE * len(
            _wrap(sub, text_w, 3, SMALL)) + 14

    aux_h = max([block_h("Auxiliary sensor", s) for s in n["aux"]] or [0])
    lane_h = max(block_h(f"{ln['method']} spectrometer", ln["fiber"]) for ln in n["lanes"]) if n["lanes"] else 120
    lane_h = max(lane_h, block_h("Process point", n["location"]) / max(1, len(n["lanes"])))
    y_lanes = top_pad + aux_h
    lanes = max(1, len(n["lanes"]))
    nodes = []          # (part, col, icon_y, title, sub, cls)

    def lane_y(k: int) -> float:
        return y_lanes + k * lane_h

    span_y = (lane_y(0) + lane_y(lanes - 1)) / 2
    nodes.append(("proc", 0, span_y, "Process point", n["location"], ""))
    for k, ln in enumerate(n["lanes"]):
        nodes += [("probe", 1, lane_y(k), ln["probe_title"], ln["probe_sub"], "sn-key"),
                  ("fiber", 2, lane_y(k), "Fiber link", ln["fiber"], "sn-fiber"),
                  ("spec", 3, lane_y(k), f"{ln['method']} spectrometer", "", "")]
        if not n["fused"]:
            nodes.append(("model", 4, lane_y(k), "Chemometric model", ln["method"], ""))
    if n["fused"]:
        nodes.append(("model", 4, span_y, n["model"], n["model_sub"], ""))
    nodes.append(("result", 5, span_y, "Result", n["result"], "sn-result"))
    for j, s in enumerate(n["aux"]):
        nodes.append(("aux", max(3 - j, 1), top_pad, "Auxiliary sensor", s + " (confirm with AFS)",
                      "sn-aux"))
    mid, defs = _marker()
    body = [defs]

    def cx(col: int) -> float:
        return col * col_w + col_w / 2

    half = icon / 2
    lane_ys = [lane_y(k) for k in range(lanes)]
    model_ys = [span_y] if n["fused"] else lane_ys

    def link(x1, y1, x2, y2, dashed=False):
        cls = "dg-edge dg-dashed" if dashed else "dg-edge"
        if abs(y1 - y2) < 0.5:
            return (f'<line class="{cls}" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'marker-end="url(#{mid})"/>')
        xm = (x1 + x2) / 2
        return (f'<polyline class="{cls}" points="{x1:.1f},{y1:.1f} {xm:.1f},{y1:.1f} {xm:.1f},{y2:.1f} '
                f'{x2:.1f},{y2:.1f}" marker-end="url(#{mid})"/>')

    gap = 6.0
    for y in lane_ys:                                         # process -> probes
        body.append(link(cx(0) + half + gap, span_y + half, cx(1) - half - gap, y + half))
        for c in (1, 2):
            body.append(link(cx(c) + half + gap, y + half, cx(c + 1) - half - gap, y + half))
    for k, y in enumerate(lane_ys):                           # spectrometer -> model
        my = model_ys[0] if n["fused"] else model_ys[k]
        body.append(link(cx(3) + half + gap, y + half, cx(4) - half - gap, my + half))
    for my in model_ys:                                       # model -> result
        body.append(link(cx(4) + half + gap, my + half, cx(5) - half - gap, span_y + half))
    for j, _ in enumerate(n["aux"]):                          # aux: up to its bus, across, down into the model
        col = max(3 - j, 1)
        bus = 4.0 + j * 8
        tx = cx(4) - 12 + j * 8
        body.append(f'<polyline class="dg-edge dg-dashed" points="{cx(col):.1f},{top_pad - 2:.1f} '
                    f'{cx(col):.1f},{bus:.1f} {tx:.1f},{bus:.1f} {tx:.1f},{model_ys[0] - gap:.1f}" '
                    f'marker-end="url(#{mid})"/>')
    for part, col, y, title, sub, cls in nodes:
        x = cx(col)
        body.append(f'<g class="sn {cls}" data-part="{part}">'
                    f'<rect class="sn-box" x="{x - half:.1f}" y="{y:.1f}" width="{icon:.0f}" height="{icon:.0f}" rx="6"/>'
                    f'<g transform="translate({x - 14:.1f},{y + half - 14:.1f}) scale(1.1667)">'
                    f'<path class="sn-icon" d="{ICONS[part]}"/></g>')
        t_lines = _wrap(title, text_w, 2, TEXT)
        body.append(_text(x, y + icon + 8 + TEXT, t_lines, "sn-title", TEXT, "middle"))
        if sub:
            body.append(_text(x, y + icon + 8 + TEXT + len(t_lines) * TEXT * LINE, _wrap(sub, text_w, 3, SMALL),
                              "sn-sub", SMALL, "middle"))
        body.append("</g>")
    height = y_lanes + lanes * lane_h + 4
    label = (f"Setup of option {option.id}: process point ({n['location']}), "
             + "; ".join(f"{ln['label']} via {ln['fiber']} fiber to a {ln['method']} spectrometer" for ln in n["lanes"])
             + f"; {n['model'] or 'one model per method'}; result: {n['result']}"
             + (f"; auxiliary sensors (dashed): {', '.join(n['aux'])}" if n["aux"] else ""))
    return _svg(width, height, body, label, "fig-schematic")


def setup(a: Assessment, option: SolutionOption, slots: dict, width: float = 340.0) -> str:
    """Narrow layout: boxes top to bottom, lanes as columns; auxiliary sensors full width below the result,
    joined to the model by a dashed line up the right edge."""
    n = option_nodes(a, option, slots)
    lanes = max(1, len(n["lanes"]))
    nodes = [{"part": "proc", "cap": "Process point", "text": n["location"], "row": 0, "lane": 0, "span": lanes}]
    for k, ln in enumerate(n["lanes"]):
        nodes += [{"part": "probe", "cap": "Probe", "text": ln["label"], "row": 1, "lane": k, "span": 1},
                  {"part": "fiber", "cap": "Fiber link", "text": ln["fiber"], "row": 2, "lane": k, "span": 1},
                  {"part": "spec", "cap": "Spectrometer", "text": f"{ln['method']} spectrometer", "row": 3, "lane": k,
                   "span": 1}]
        if not n["fused"]:
            nodes.append({"part": "model", "cap": "Model", "text": f"Chemometric model ({ln['method']})", "row": 4,
                          "lane": k, "span": 1, "id": f"model{k}"})
    if n["fused"]:
        nodes.append({"part": "model", "cap": "Model", "text": n["model"] + (f" ({n['model_sub']})" if n["model_sub"]
                                                                              else ""),
                      "row": 4, "lane": 0, "span": lanes, "id": "model0"})
    nodes.append({"part": "result", "cap": "Result", "text": n["result"], "row": 5, "lane": 0, "span": lanes})
    for j, s in enumerate(n["aux"]):
        nodes.append({"part": "aux", "cap": "Auxiliary sensor, confirm with AFS", "text": s, "row": 6 + j,
                      "lane": 0, "span": lanes})
    has_aux = bool(n["aux"])
    pad, gap_lane, gap_row, bus = 2.0, 12.0, 24.0, 16.0
    usable = width - 2 * pad - (lanes - 1) * gap_lane - (bus if has_aux else 0)
    lane_w = usable / lanes
    for nd in nodes:
        w = nd["span"] * lane_w + (nd["span"] - 1) * gap_lane
        nd["w"], nd["cap_lines"] = w, _wrap(nd["cap"], w - 16, 2, SMALL)
        nd["lines"] = _wrap(nd["text"], w - 16, 5, TEXT)
        nd["h"] = (10 + (24 if nd["part"] == "proc" else 0) + len(nd["cap_lines"]) * SMALL * LINE
                   + len(nd["lines"]) * TEXT * LINE + 8)
    rows = max(nd["row"] for nd in nodes) + 1
    row_h = [max([nd["h"] for nd in nodes if nd["row"] == r] or [0]) for r in range(rows)]
    row_y = [pad + sum(row_h[:r]) + r * gap_row for r in range(rows)]
    for nd in nodes:
        x0 = pad + nd["lane"] * (lane_w + gap_lane)
        nd["box"] = (x0, row_y[nd["row"]], x0 + nd["w"], row_y[nd["row"]] + row_h[nd["row"]])
    by_row_lane = {(nd["row"], nd["lane"]): nd for nd in nodes if nd["part"] != "aux"}
    for nd in nodes:                                  # auxiliary rows: only as tall as their own text
        if nd["part"] == "aux":
            nd["box"] = (nd["box"][0], nd["box"][1], nd["box"][2], nd["box"][1] + nd["h"])
    mid, defs = _marker()
    body = [defs]

    def down(src, dst):
        sx0, _, sx1, sy1 = src["box"]
        dx0, dy0, dx1, _ = dst["box"]
        x = (sx0 + sx1) / 2 if (sx1 - sx0) <= (dx1 - dx0) else (dx0 + dx1) / 2
        return (f'<line class="dg-edge" x1="{x:.1f}" y1="{sy1:.1f}" x2="{x:.1f}" y2="{dy0 - 1.5:.1f}" '
                f'marker-end="url(#{mid})"/>')

    proc, result = nodes[0], next(nd for nd in nodes if nd["part"] == "result")
    models = [nd for nd in nodes if nd["part"] == "model"]
    for k in range(len(n["lanes"])):
        body.append(down(proc, by_row_lane[(1, k)]))
        body.append(down(by_row_lane[(1, k)], by_row_lane[(2, k)]))
        body.append(down(by_row_lane[(2, k)], by_row_lane[(3, k)]))
        body.append(down(by_row_lane[(3, k)], models[0] if n["fused"] else by_row_lane[(4, k)]))
    for m in models:
        body.append(down(m, result))
    for nd in (x for x in nodes if x["part"] == "aux"):
        sx1, sy = nd["box"][2], (nd["box"][1] + nd["box"][3]) / 2
        bx = width - pad - bus / 2
        m = models[-1]["box"]
        my = (m[1] + m[3]) / 2
        body.append(f'<polyline class="dg-edge dg-dashed" points="{sx1:.1f},{sy:.1f} {bx:.1f},{sy:.1f} '
                    f'{bx:.1f},{my:.1f} {m[2] + 1.5:.1f},{my:.1f}" marker-end="url(#{mid})"/>')
    for nd in nodes:
        x0, y0, x1, y1 = nd["box"]
        cls = {"fiber": "sn-fiber", "aux": "sn-aux", "result": "sn-result", "probe": "sn-probe"}.get(nd["part"], "")
        body.append(f'<g class="sn {cls}" data-part="{nd["part"]}"><rect class="sn-box" x="{x0:.1f}" y="{y0:.1f}" '
                    f'width="{x1 - x0:.1f}" height="{y1 - y0:.1f}" rx="{10 if nd["part"] == "fiber" else 3}"/>')
        top = y0 + 10 + SMALL * 0.85
        if nd["part"] == "proc":
            py = y0 + 9
            body.append(f'<path class="dg-pipe" d="M{x0 + 10:.1f},{py:.1f} h{x1 - x0 - 20:.1f} M{x0 + 10:.1f},'
                        f'{py + 12:.1f} h{x1 - x0 - 20:.1f}"/>')
            top += 24
        body.append(_text(x0 + 8, top, nd["cap_lines"], "dg-cap", SMALL))
        body.append(_text(x0 + 8, top + len(nd["cap_lines"]) * SMALL * LINE + 4, nd["lines"], "dg-txt", TEXT))
        body.append("</g>")
    height = max(nd["box"][3] for nd in nodes) + pad
    label = "Setup sketch: " + "; ".join(f"{nd['cap']}: {nd['text']}" for nd in nodes)
    return _svg(width, height, body, label, "fig-setup")


# --------------------------------------------------------------------------------------- spectral
# Method ranges as the supplied pages state them in their text (tests check every number on the page).
# A method whose range no page states is listed without number or bar.
RANGES = (
    {"method": "UV-Vis", "name": "UV-Vis, UV region", "lo": 190, "hi": 360, "unit": "nm", "doc": "S01", "page": 5},
    {"method": "Raman", "name": "Raman, detection region", "lo": 400, "hi": 1100, "unit": "nm", "doc": "S01",
     "page": 11},
    {"method": "NIR", "name": "NIR", "lo": 780, "hi": 2500, "unit": "nm", "doc": "S01", "page": 10},
    {"method": "MIR", "name": "MIR", "lo": 4000, "hi": 400, "unit": "cm-1", "doc": "S01", "page": 9},
    {"method": "Fluorescence", "name": "Fluorescence", "lo": None, "hi": None, "unit": None, "doc": "S01",
     "page": 12},
)
# Region band: names only, no numbers printed (boundaries follow the stated ranges above).
BAND = (("UV", 0.15, 0.40), ("VIS", 0.40, 0.78), ("NIR", 0.78, 2.5), ("MIR", 2.5, 30.0))
LO_UM, HI_UM = 0.15, 30.0
TICKS = [(0.2, "200 nm"), (0.4, "400 nm"), (1.0, "1000 nm"), (2.5, "2500 nm"), (5.0, "5 µm"), (10.0, "10 µm"),
         (25.0, "25 µm")]
TICKS_NARROW = {0.2, 1.0, 5.0, 25.0}
WAVENUMBER_TICKS = [(2.5, "4000"), (10.0, "1000"), (25.0, "400")]
_LABEL_NUM = re.compile(r"(\d+(?:\.\d+)?)\s*(nm|µm)")


def to_um(value: float, unit: str) -> float:
    return {"nm": value / 1000, "µm": value, "cm-1": 1e4 / value}[unit]


def range_label(r: dict) -> str:
    if r["lo"] is None:
        return "range not stated"
    unit = "cm⁻¹" if r["unit"] == "cm-1" else r["unit"]
    return f"{r['lo']:g}–{r['hi']:g} {unit}"


def fiber_label_text(f: dict) -> str:
    """The window as the slide labels it: first and last number with their units (S02 p.6 bar text)."""
    nums = _LABEL_NUM.findall(f["sources"][0]["quote"])
    if len(nums) < 2:
        return "window not stated"
    (lo, lu), (hi, hu) = nums[0], nums[-1]
    return f"{lo}–{hi} {hu}" if lu == hu else f"{lo} {lu} – {hi} {hu}"


def option_highlights(a: Assessment, option: SolutionOption | None) -> tuple[set[str], set[str], set[str]]:
    """Methods of the proposed option, methods of the other options, fiber ids covering the proposed ones."""
    recs = {r.id: r for r in a.recommendations}
    proposed = {m for m, _ in option_parts(option, recs)} if option else set()
    others = {m for o in a.solution_options if o is not option for m, _ in option_parts(o, recs)} - proposed
    fibers = set()
    for m in proposed:
        try:
            fibers |= {c.fiber_id for c in method_fiber_coverage(m) if c.status != "none"}
        except KeyError:
            continue
    return proposed, others, fibers


def spectral_rows(proposed: set[str], others: set[str], fiber_ids: set[str]) -> list[dict]:
    rows = []
    for r in RANGES:
        state = "proposed" if r["method"] in proposed else "other" if r["method"] in others else "off"
        lo_um = hi_um = None
        if r["lo"] is not None:
            a, b = to_um(r["lo"], r["unit"]), to_um(r["hi"], r["unit"])
            lo_um, hi_um = min(a, b), max(a, b)
        rows.append({"group": "method", "name": r["name"], "label": range_label(r), "lo": lo_um, "hi": hi_um,
                     "source": kb.citation_label(r["doc"], r["page"]), "state": state, "range": r})
    for f in kb.fibers():
        if f["id"] in fiber_ids:
            rows.append({"group": "fiber", "name": f["name"].split(" (")[0], "label": fiber_label_text(f),
                         "lo": f["min_um"], "hi": f["max_um"], "source": "S02 p.6", "state": "fiber", "fiber": f})
    return rows


def spectral(proposed: set[str], others: set[str], fiber_ids: set[str], width: float = 720.0) -> str:
    rows = spectral_rows(proposed, others, fiber_ids)
    narrow = width < 480
    pad = 2.0
    label_w = 0.0 if narrow else 250.0
    x0, x1 = pad + label_w + (24 if narrow else 0), width - pad - 16    # narrow: room for the first tick
    band_y, axis_top = 2.0, 46.0

    def x(um: float) -> float:
        return x0 + (math.log10(um) - math.log10(LO_UM)) / (math.log10(HI_UM) - math.log10(LO_UM)) * (x1 - x0)

    body: list[str] = []
    for name, lo, hi in BAND:                                  # UV | VIS | NIR | MIR band
        bx0, bx1 = x(lo), x(hi)
        body.append(f'<rect class="sp-band" x="{bx0:.1f}" y="{band_y:.1f}" width="{bx1 - bx0:.1f}" height="18"/>')
        body.append(_text((bx0 + bx1) / 2, band_y + 13.5, [name], "sp-band-t", SMALL, "middle"))
    items, y = [], axis_top + 18
    for group, title in (("method", "Method ranges stated in the sources"),
                         ("fiber", "Fibers that carry the proposed method (S02 p.6, figure reading)")):
        group_rows = [r for r in rows if r["group"] == group]
        if not group_rows:
            continue
        title_lines = _wrap(title, width - 2 * pad, 2, SMALL)
        items.append(("title", title_lines, y))
        y += 10 + len(title_lines) * SMALL * LINE
        for r in group_rows:
            room = (width - 2 * pad) if narrow else label_w - 10
            lines = _wrap(r["name"], room, 1, SMALL) + _wrap(f"{r['label']} · {r['source']}", room, 1, SMALL)
            items.append(("row", (r, lines), y))
            y += (len(lines) * SMALL * LINE + 18) if narrow else max(26.0, len(lines) * SMALL * LINE + 10)
        y += 10
    bottom = y
    for um, text in TICKS:
        if narrow and um not in TICKS_NARROW:
            continue
        gx = x(um)
        body.append(f'<line class="sp-grid" x1="{gx:.1f}" y1="{axis_top:.1f}" x2="{gx:.1f}" y2="{bottom:.1f}"/>')
        body.append(_text(gx, axis_top - 6, [text], "sp-tick", SMALL, "middle"))
    body.append(f'<line class="sp-axis" x1="{x0:.1f}" y1="{axis_top:.1f}" x2="{x1:.1f}" y2="{axis_top:.1f}"/>')
    body.append(f'<line class="sp-axis" x1="{x0:.1f}" y1="{bottom:.1f}" x2="{x1:.1f}" y2="{bottom:.1f}"/>')
    for um, text in WAVENUMBER_TICKS:
        body.append(_text(x(um), bottom + 16, [text], "sp-tick", SMALL, "middle"))
    body.append(_text(x1, bottom + 34, ["wavenumber, cm⁻¹"], "sp-axis-label", SMALL, "end"))
    for kind, item, yy in items:
        if kind == "title":
            body.append(_text(pad, yy, item, "sp-group", SMALL))
            continue
        r, lines = item
        on = r["state"] == "proposed"
        cls = "sp-label sp-label-on" if on else "sp-label"
        lx = pad
        body.append(_text(lx, yy + SMALL, lines[:1], cls, SMALL))
        body.append(_text(lx, yy + SMALL + SMALL * LINE, lines[1:], "sp-value", SMALL))
        bar_y = yy + len(lines) * SMALL * LINE + 3 if narrow else yy + SMALL * LINE - 3
        if r["lo"] is None:
            continue                                            # no stated range: no bar
        bx0, bx1 = x(max(r["lo"], LO_UM)), x(min(r["hi"], HI_UM))
        body.append(f'<rect class="sp-bar sp-{r["state"]}" x="{bx0:.1f}" y="{bar_y:.1f}" width="{bx1 - bx0:.1f}" '
                    f'height="10" rx="1.5"><title>{escape(r["name"])}: {escape(r["label"])} ({escape(r["source"])})'
                    f'</title></rect>')
    height = bottom + 42
    return _svg(width, height, body, "Spectral ranges stated in the sources and the fiber windows for the "
                                     "proposed method on a logarithmic wavelength axis", "fig-spectral")


# ---------------------------------------------------------------------------------- parameter map
def measure_key(p) -> tuple[str, str]:
    mb = p.measured_by
    if mb.type == "spectroscopy":
        return "spectroscopy", f"Spectroscopy: {mb.method or 'method not named'}"
    if mb.type == "auxiliary_sensor":
        return "aux", f"Auxiliary sensor: {mb.sensor or 'not named'}"
    if mb.type == "reference_lab":
        return "lab", f"Reference lab: {mb.sensor or 'not named'}"
    return "none", f"Not measurable in-line; alternative: {mb.alternative or 'none named'}"


def parameter_map(a: Assessment, width: float = 720.0) -> str:
    if not a.parameters:
        return ""
    narrow = width < 480
    size = TEXT
    pad, gap = 2.0, 10.0
    col_w = (width - 2 * pad) * (0.42 if narrow else 0.38)
    rights: list[tuple[str, str]] = []
    for p in a.parameters:
        if measure_key(p) not in rights:
            rights.append(measure_key(p))

    def block(text: str) -> tuple[list[str], float]:
        lines = _wrap(text, col_w - 16, 5, size)
        return lines, 14 + len(lines) * size * LINE

    left = [(p, *block(f"{p.id} · {p.name}")) for p in a.parameters]
    right = [(k, *block(k[1])) for k in rights]
    lh = sum(h for *_, h in left) + gap * (len(left) - 1)
    rh = sum(h for *_, h in right) + gap * (len(right) - 1)
    total = max(lh, rh)
    rx0 = width - pad - col_w
    mid, defs = _marker()
    body = [defs]
    pos, y = {}, pad + (total - rh) / 2
    for k, _, h in right:
        pos[k] = (y, h)
        y += h + gap
    lpos, y = [], pad + (total - lh) / 2
    for p, lines, h in left:
        lpos.append((p, lines, y, h))
        y += h + gap
    for p, _, ly, h in lpos:
        ry, rh_ = pos[measure_key(p)]
        sx, sy, ex, ey = pad + col_w, ly + h / 2, rx0 - 1.5, ry + rh_ / 2
        cx = (sx + ex) / 2
        dashed = "" if p.measured_by.type == "spectroscopy" else " dg-dashed"
        body.append(f'<path class="dg-edge{dashed}" d="M{sx:.1f},{sy:.1f} C{cx:.1f},{sy:.1f} {cx:.1f},{ey:.1f} '
                    f'{ex:.1f},{ey:.1f}" marker-end="url(#{mid})"/>')
    for p, lines, ly, h in lpos:
        body.append(f'<rect class="dg-node" x="{pad:.1f}" y="{ly:.1f}" width="{col_w:.1f}" height="{h:.1f}" rx="2"/>')
        body.append(_text(pad + 8, ly + 6 + size, lines, "dg-txt", size))
    for k, lines, h in right:
        ry, _ = pos[k]
        kind = {"spectroscopy": "fiber", "aux": "aux"}.get(k[0], "box")
        body.append(f'<rect class="dg-node dg-{kind}" x="{rx0:.1f}" y="{ry:.1f}" width="{col_w:.1f}" '
                    f'height="{h:.1f}" rx="2"/>')
        body.append(_text(rx0 + 8, ry + 6 + size, lines, "dg-txt", size))
    label = "Parameters and how each is measured: " + "; ".join(f"{p.name}: {measure_key(p)[1]}" for p in a.parameters)
    return _svg(width, total + 2 * pad, body, label, "fig-params")
