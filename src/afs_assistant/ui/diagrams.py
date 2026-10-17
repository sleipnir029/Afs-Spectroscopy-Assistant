"""Inline SVG figures for the web UI, drawn by code from the run and the knowledge base.

- `setup`: the proposed option as process point -> probe -> fiber -> spectrometer -> model -> result,
  auxiliary sensors dashed into the model (the same structure as `render.mermaid_chart`).
- `spectral`: nominal method ranges (`fibers.METHOD_RANGES_UM`, source pages listed) and the fiber
  transmission windows (`knowledge/fibers.json`, S02 p.6 figure reading) on one log wavelength axis.
- `parameter_map`: each parameter linked to how it is measured.
No number is drawn that is not in those data. Colours are CSS classes (theme tokens in app.css).
Each figure comes in a wide and a narrow layout; the page shows one by viewport width.
"""

from __future__ import annotations

import math
import textwrap
from html import escape

from afs_assistant import kb
from afs_assistant.fibers import METHOD_RANGES_UM
from afs_assistant.options import is_fusion, method_label, option_parts
from afs_assistant.render import fiber_label
from afs_assistant.schema import Assessment, SolutionOption

FONT = 12.5          # px, node text
CAPTION = 10.0       # px, node caption
CHAR_W = 0.56        # average glyph width in em (IBM Plex Sans, mixed case)
_uid = 0


def _next_id(prefix: str) -> str:
    global _uid
    _uid += 1
    return f"{prefix}{_uid}"


def _wrap(text: str, width_px: float, max_lines: int, size: float = FONT) -> list[str]:
    chars = max(6, int((width_px - 16) / (size * CHAR_W)))
    lines = textwrap.wrap(" ".join(str(text).split()), chars, break_long_words=True) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][: max(1, chars - 1)].rstrip(" ,;:.") + "…"
    return lines


def _text(x: float, y: float, lines: list[str], cls: str, size: float = FONT, anchor: str = "start") -> str:
    spans = "".join(f'<tspan x="{x:.1f}" dy="{0 if i == 0 else size * 1.3:.1f}">{escape(t)}</tspan>'
                    for i, t in enumerate(lines))
    return f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}">{spans}</text>'


def _svg(width: float, height: float, body: list[str], label: str, cls: str) -> str:
    return (f'<svg class="fig {cls}" viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{escape(label)}" '
            f'xmlns="http://www.w3.org/2000/svg">{"".join(body)}</svg>')


def _marker(mid: str) -> str:
    return (f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path class="dg-head" d="M0,1 L9,5 L0,9 z"/></marker></defs>')


# ------------------------------------------------------------------------------------------ setup
def setup_nodes(a: Assessment, option: SolutionOption, slots: dict) -> tuple[list[dict], list[tuple], int]:
    """Nodes (id, caption, text, col, lane, span, kind) and edges; the third value is the lane count."""
    recs = {r.id: r for r in a.recommendations}
    params = {p.id: p for p in a.parameters}
    used = [params[i] for i in option.parameter_ids if i in params]
    parts = option_parts(option, recs)
    lanes = max(1, len(parts))
    fused = len(parts) <= 1 or is_fusion(option, recs)
    nodes = [{"id": "proc", "cap": "Process point", "text": a.measurement_concept.location, "col": 0, "lane": 0,
              "span": lanes, "kind": "proc"}]
    edges: list[tuple] = []
    for k, (method, technique) in enumerate(parts):
        fiber = fiber_label(method, slots).removeprefix("Fiber: ")
        nodes += [{"id": f"probe{k}", "cap": "Probe", "text": method_label(method, technique), "col": 1, "lane": k,
                   "span": 1, "kind": "box"},
                  {"id": f"fiber{k}", "cap": "Fiber link", "text": fiber, "col": 2, "lane": k, "span": 1,
                   "kind": "fiber"},
                  {"id": f"spec{k}", "cap": "Spectrometer", "text": f"{method} spectrometer", "col": 3, "lane": k,
                   "span": 1, "kind": "box"}]
        model = "model" if fused else f"model{k}"
        edges += [("proc", f"probe{k}", "solid"), (f"probe{k}", f"fiber{k}", "solid"),
                  (f"fiber{k}", f"spec{k}", "solid"), (f"spec{k}", model, "solid")]
        if not fused:
            nodes.append({"id": model, "cap": "Model", "text": f"Chemometric model ({method})", "col": 4, "lane": k,
                          "span": 1, "kind": "box"})
            edges.append((model, "result", "solid"))
    if fused:
        nodes.append({"id": "model", "cap": "Model", "col": 4, "lane": 0, "span": lanes, "kind": "box",
                      "text": "Chemometric model" if len(parts) <= 1 else "Data fusion model (per-method calibration)"})
        edges.append(("model", "result", "solid"))
    spectro = [p.name for p in used if p.measured_by.type == "spectroscopy"] or [p.name for p in used]
    nodes.append({"id": "result", "cap": "Result", "text": ", ".join(spectro) or "measured parameters", "col": 5,
                  "lane": 0, "span": lanes, "kind": "result"})
    aux = [p for p in used if p.measured_by.type == "auxiliary_sensor"]
    models = ["model"] if fused else [f"model{k}" for k in range(len(parts))]
    for j, p in enumerate(aux):
        nodes.append({"id": f"aux{j}", "cap": "Auxiliary sensor · confirm with AFS",
                      "text": p.measured_by.sensor or p.name, "col": 3, "lane": lanes + j, "span": 1, "kind": "aux"})
        edges += [(f"aux{j}", m, "aux") for m in models]
    return nodes, edges, lanes + len(aux)


def setup(a: Assessment, option: SolutionOption, slots: dict, narrow: bool = False) -> str:
    nodes, edges, total_lanes = setup_nodes(a, option, slots)
    pad = 12.0
    if narrow:     # flow runs down the page; lanes are columns
        lane_w = (336 - 2 * pad - (total_lanes - 1) * 10) / total_lanes
        box_u, gap_u, box_v, gap_v = 70.0, 26.0, lane_w, 10.0
    else:
        box_u, gap_u, box_v, gap_v = 152.0, 34.0, 70.0, 18.0

    def rect(n: dict) -> tuple[float, float, float, float]:
        """(u0, v0, u1, v1): u along the flow, v across the lanes."""
        u0 = pad + n["col"] * (box_u + gap_u)
        v0 = pad + n["lane"] * (box_v + gap_v)
        v1 = v0 + n["span"] * box_v + (n["span"] - 1) * gap_v
        return u0, v0, u0 + box_u, v1

    def xy(u: float, v: float) -> tuple[float, float]:
        return (v, u) if narrow else (u, v)

    mid = _next_id("arr")
    body = [_marker(mid)]
    boxes = {n["id"]: rect(n) for n in nodes}
    for src, dst, style in edges:       # edges first, under the boxes
        su0, sv0, su1, sv1 = boxes[src]
        du0, dv0, du1, dv1 = boxes[dst]
        if style == "aux":
            # bus: out of the sensor's far side, along to the model's middle, then into the model's lane edge
            start = xy(su1, (sv0 + sv1) / 2)
            corner = xy((du0 + du1) / 2, (sv0 + sv1) / 2)
            end = xy((du0 + du1) / 2, dv1)
            body.append(f'<polyline class="dg-edge dg-dashed" points="{start[0]:.1f},{start[1]:.1f} '
                        f'{corner[0]:.1f},{corner[1]:.1f} {end[0]:.1f},{end[1]:.1f}" marker-end="url(#{mid})"/>')
            continue
        # straight in the lane of the narrower node
        v = (max(sv0, dv0) + min(sv1, dv1)) / 2 if (sv1 - sv0) != (dv1 - dv0) else (sv0 + sv1) / 2
        if (sv1 - sv0) > (dv1 - dv0):
            v = (dv0 + dv1) / 2
        elif (dv1 - dv0) > (sv1 - sv0):
            v = (sv0 + sv1) / 2
        x1, y1 = xy(su1, v)
        x2, y2 = xy(du0 - 1.5, v)
        body.append(f'<line class="dg-edge" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'marker-end="url(#{mid})"/>')
    for n in nodes:
        u0, v0, u1, v1 = boxes[n["id"]]
        x0, y0 = xy(u0, v0)
        x1, y1 = xy(u1, v1)
        w, h = x1 - x0, y1 - y0
        kind = n["kind"]
        radius = h / 2 if kind == "fiber" and not narrow else 3
        body.append(f'<rect class="dg-node dg-{kind}" x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" height="{h:.1f}" '
                    f'rx="{min(radius, 14):.1f}"/>')
        if kind == "proc":          # a pipe section with the flow direction, the probe's insertion point
            py = y0 + 8 if narrow else y0 + h / 2 - 22
            body.append(f'<path class="dg-pipe" d="M{x0 + 8:.1f},{py:.1f} h{w - 16:.1f} M{x0 + 8:.1f},{py + 12:.1f} '
                        f'h{w - 16:.1f}"/><path class="dg-flow" d="M{x0 + 14:.1f},{py + 6:.1f} h{w - 34:.1f}" '
                        f'marker-end="url(#{mid})"/>')
            top = py + 26
        else:
            top = y0 + 16
        inner = w - 4
        cap = _wrap(n["cap"], inner, 2, CAPTION)
        body.append(_text(x0 + 8, top, cap, "dg-cap", CAPTION))
        avail = (y1 - top - len(cap) * CAPTION * 1.3 - 6)
        max_lines = max(1, int(avail // (FONT * 1.3)) + (1 if narrow else 0))
        lines = _wrap(n["text"], inner, max_lines)
        body.append(_text(x0 + 8, top + len(cap) * CAPTION * 1.3 + 4, lines, "dg-txt"))
    last = max(boxes.values(), key=lambda b: b[2])[2] + pad
    far = max(b[3] for b in boxes.values()) + pad
    width, height = xy(last, far)
    label = "Setup sketch: " + "; ".join(f"{n['cap']}: {n['text']}" for n in nodes)
    return _svg(width, height, body, label, "fig-setup")


# --------------------------------------------------------------------------------------- spectral
LO_UM, HI_UM = 0.15, 30.0
TICKS_UM = [(0.2, "200 nm"), (0.4, "400 nm"), (0.78, "780 nm"), (1.0, "1 µm"), (2.5, "2.5 µm"), (5.0, "5 µm"),
            (10.0, "10 µm"), (25.0, "25 µm")]
TICKS_NARROW = {0.2, 1.0, 2.5, 10.0, 25.0}
WAVENUMBER_TICKS = [(2.5, "4000"), (5.0, "2000"), (10.0, "1000"), (25.0, "400 cm⁻¹")]
METHOD_ORDER = ("UV-Vis", "Fluorescence", "Raman", "NIR", "MIR")
METHOD_NOTE = {"Raman": "detection region", "Fluorescence": "UV/visible irradiation"}


def range_text(lo: float, hi: float) -> str:
    if hi <= 1.2:
        return f"{lo * 1000:.0f}–{hi * 1000:.0f} nm"
    def um(v: float) -> str:
        return f"{v:g}"
    return f"{um(lo)}–{um(hi)} µm"


def spectral_rows(methods_used: set[str]) -> list[dict]:
    rows = []
    for m in METHOD_ORDER:
        r = METHOD_RANGES_UM[m]
        lo, hi = r["range_um"]
        note = METHOD_NOTE.get(m)
        rows.append({"group": "method", "name": m + (f" ({note})" if note else ""), "lo": lo, "hi": hi,
                     "range": range_text(lo, hi), "source": r["source"], "basis": r["basis"],
                     "used": m in methods_used})
    for f in kb.fibers():
        rows.append({"group": "fiber", "name": f["name"], "lo": f["min_um"], "hi": f["max_um"],
                     "range": range_text(f["min_um"], f["max_um"]),
                     "source": ", ".join(sorted({kb.citation_label(s["doc"], s["page"]) for s in f["sources"]})),
                     "basis": "figure reading", "used": False, "family": f["family"]})
    return rows


def spectral(methods_used: set[str], fiber_families: set[str], narrow: bool = False) -> str:
    rows = spectral_rows(methods_used)
    for r in rows:
        if r["group"] == "fiber":
            r["used"] = r["family"] in fiber_families
    width = 340.0 if narrow else 960.0
    label_w = 0.0 if narrow else 260.0
    pad, axis_top = 10.0, 34.0
    x0, x1 = pad + label_w, width - pad - (0 if narrow else 6)
    row_h = 34.0 if narrow else 24.0
    group_gap = 30.0

    def x(um: float) -> float:
        return x0 + (math.log10(um) - math.log10(LO_UM)) / (math.log10(HI_UM) - math.log10(LO_UM)) * (x1 - x0)

    body: list[str] = []
    y = axis_top + 14
    layout = []
    for group, title in (("method", "Method ranges (nominal)"), ("fiber", "Fiber transmission windows (S02 p.6)")):
        layout.append(("title", title, y))
        y += 20
        for r in (r for r in rows if r["group"] == group):
            layout.append(("row", r, y))
            y += row_h
        y += group_gap - 14
    bottom = y + 4
    for um, text in TICKS_UM:                       # grid + wavelength axis on top
        if narrow and um not in TICKS_NARROW:
            continue
        gx = x(um)
        body.append(f'<line class="sp-grid" x1="{gx:.1f}" y1="{axis_top:.1f}" x2="{gx:.1f}" y2="{bottom:.1f}"/>')
        body.append(_text(gx, axis_top - 8, [text], "sp-tick", 10.5, "middle"))
    body.append(f'<line class="sp-axis" x1="{x0:.1f}" y1="{axis_top:.1f}" x2="{x1:.1f}" y2="{axis_top:.1f}"/>')
    body.append(f'<line class="sp-axis" x1="{x0:.1f}" y1="{bottom:.1f}" x2="{x1:.1f}" y2="{bottom:.1f}"/>')
    for um, text in WAVENUMBER_TICKS:               # wavenumber axis (infrared) at the bottom
        if narrow and um == 5.0:
            continue
        body.append(_text(x(um), bottom + 15, [text], "sp-tick", 10.5, "middle"))
    body.append(_text(x0, axis_top - 22, ["Wavelength (log scale)"], "sp-axis-label", 10.5))
    body.append(_text(x1, bottom + 30, ["Wavenumber, infrared"], "sp-axis-label", 10.5, "end"))
    for kind, item, yy in layout:
        if kind == "title":
            body.append(_text(pad, yy + 4, [item], "sp-group", 11))
            continue
        r = item
        bar_y = yy + (14 if narrow else 4)
        bx0, bx1 = x(max(r["lo"], LO_UM)), x(min(r["hi"], HI_UM))
        cls = "sp-bar sp-used" if r["used"] else ("sp-bar sp-fiber" if r["group"] == "fiber" else "sp-bar")
        body.append(f'<rect class="{cls}" x="{bx0:.1f}" y="{bar_y:.1f}" width="{bx1 - bx0:.1f}" height="12" rx="2">'
                    f'<title>{escape(r["name"])}: {escape(r["range"])} ({escape(r["source"])})</title></rect>')
        name = r["name"] if r["group"] == "method" else r["name"].split(" (")[0]
        if narrow:
            body.append(_text(pad, yy + 9, [f"{name} · {r['range']}"], "sp-label" + (" sp-label-used" if r["used"]
                                                                                      else ""), 10.5))
        else:
            body.append(_text(pad, bar_y + 10, _wrap(name, label_w - 8, 1, 11.5),
                              "sp-label" + (" sp-label-used" if r["used"] else ""), 11.5))
            inside = bx1 - bx0 > 120
            tx = bx0 + 6 if inside else bx1 + 6
            if not inside and tx > x1 - 70:
                tx, anchor = bx0 - 6, "end"
            else:
                anchor = "start"
            body.append(_text(tx, bar_y + 10, [f"{r['range']} · {r['source']}"],
                              "sp-val" + (" sp-val-in" if inside and r["used"] else ""), 10.5, anchor))
    height = bottom + 38
    return _svg(width, height, body, "Spectral ranges of the methods and fiber transmission windows on a "
                                     "logarithmic wavelength axis", "fig-spectral")


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


def parameter_map(a: Assessment, narrow: bool = False) -> str:
    if not a.parameters:
        return ""
    width = 340.0 if narrow else 960.0
    col_w = 128.0 if narrow else 300.0
    pad = 8.0
    size = 11.5 if narrow else FONT
    rights: list[tuple[str, str]] = []
    for p in a.parameters:
        k = measure_key(p)
        if k not in rights:
            rights.append(k)

    def box_h(text: str) -> tuple[list[str], float]:
        lines = _wrap(text, col_w, 4, size)
        return lines, 14 + len(lines) * size * 1.3

    left = [(p, *box_h(f"{p.id} · {p.name}")) for p in a.parameters]
    right = [(k, *box_h(k[1])) for k in rights]
    gap = 10.0
    lh = sum(h for *_, h in left) + gap * (len(left) - 1)
    rh = sum(h for *_, h in right) + gap * (len(right) - 1)
    total = max(lh, rh)
    body, pos = [], {}
    mid = _next_id("arr")
    body.append(_marker(mid))
    rx0 = width - pad - col_w
    y = pad + (total - rh) / 2
    for k, lines, h in right:
        pos[k] = (y, h)
        y += h + gap
    y = pad + (total - lh) / 2
    lpos = []
    for p, lines, h in left:
        lpos.append((p, lines, y, h))
        y += h + gap
    for p, _, ly, lh_ in lpos:                    # connectors under the boxes
        ry, rh_ = pos[measure_key(p)]
        sx, sy, ex, ey = pad + col_w, ly + lh_ / 2, rx0 - 1.5, ry + rh_ / 2
        cx = (sx + ex) / 2
        dashed = " dg-dashed" if p.measured_by.type != "spectroscopy" else ""
        body.append(f'<path class="dg-edge{dashed}" d="M{sx:.1f},{sy:.1f} C{cx:.1f},{sy:.1f} {cx:.1f},{ey:.1f} '
                    f'{ex:.1f},{ey:.1f}" marker-end="url(#{mid})"/>')
    for p, lines, ly, h in lpos:
        body.append(f'<rect class="dg-node" x="{pad:.1f}" y="{ly:.1f}" width="{col_w:.1f}" height="{h:.1f}" rx="3"/>')
        body.append(_text(pad + 8, ly + 7 + size, lines, "dg-txt", size))
    for k, lines, h in right:
        ry, _ = pos[k]
        cls = "dg-node dg-fiber" if k[0] == "spectroscopy" else ("dg-node dg-aux" if k[0] == "aux" else "dg-node")
        body.append(f'<rect class="{cls}" x="{rx0:.1f}" y="{ry:.1f}" width="{col_w:.1f}" height="{h:.1f}" rx="3"/>')
        body.append(_text(rx0 + 8, ry + 7 + size, lines, "dg-txt", size))
    label = "Parameters and how each is measured: " + "; ".join(f"{p.name}: {measure_key(p)[1]}" for p in a.parameters)
    return _svg(width, total + 2 * pad, body, label, "fig-params")
