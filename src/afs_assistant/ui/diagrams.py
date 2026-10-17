"""Inline SVG figures for the web UI, drawn by code from the run and the knowledge base.

- `setup`: the proposed option, top to bottom: process point -> probe -> fiber -> spectrometer -> model ->
  result, auxiliary sensors dashed into the model (the same structure as `render.mermaid_chart`).
- `spectral`: nominal method ranges (`fibers.METHOD_RANGES_UM`, source pages listed) and the fiber
  transmission windows (`knowledge/fibers.json`, S02 p.6 figure reading) on one log wavelength axis.
- `parameter_map`: each parameter linked to how it is measured.
No number is drawn that is not in those data. Colours are CSS classes (theme tokens in app.css).
Every figure is drawn for a given width (desktop and phone); the page shows one by viewport width.
"""

from __future__ import annotations

import itertools
import math
import textwrap
from html import escape

from afs_assistant import kb
from afs_assistant.fibers import METHOD_RANGES_UM, method_fiber_coverage
from afs_assistant.options import is_fusion, method_label, option_parts
from afs_assistant.render import fiber_label
from afs_assistant.schema import Assessment, SolutionOption

CAPTION = 10.0       # px, node caption
MAX_AUX_ROWS = 3     # auxiliary sensors drawn beside probe, fiber and spectrometer
AUX_WEIGHT = 1.5     # a method lane is this many times wider than the auxiliary column
CHAR_W = 0.56        # average glyph width in em (IBM Plex Sans, mixed case)
LINE = 1.3
_ids = itertools.count(1)


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


# ------------------------------------------------------------------------------------------ setup
def setup_nodes(a: Assessment, option: SolutionOption, slots: dict) -> tuple[list[dict], list[tuple], int, int]:
    """Nodes (id, cap, text, row, lane, span, kind), edges, method lane count and total lane count."""
    recs = {r.id: r for r in a.recommendations}
    params = {p.id: p for p in a.parameters}
    used = [params[i] for i in option.parameter_ids if i in params]
    parts = option_parts(option, recs)
    lanes = max(1, len(parts))
    fused = len(parts) <= 1 or is_fusion(option, recs)
    nodes = [{"id": "proc", "cap": "Process point", "text": a.measurement_concept.location, "row": 0, "lane": 0,
              "span": lanes, "kind": "proc"}]
    edges: list[tuple] = []
    for k, (method, technique) in enumerate(parts):
        model = "model" if fused else f"model{k}"
        nodes += [{"id": f"probe{k}", "cap": "Probe", "text": method_label(method, technique), "row": 1, "lane": k,
                   "span": 1, "kind": "box"},
                  {"id": f"fiber{k}", "cap": "Fiber link", "text": fiber_label(method, slots).removeprefix("Fiber: "),
                   "row": 2, "lane": k, "span": 1, "kind": "fiber"},
                  {"id": f"spec{k}", "cap": "Spectrometer", "text": f"{method} spectrometer", "row": 3, "lane": k,
                   "span": 1, "kind": "box"}]
        edges += [("proc", f"probe{k}", "solid"), (f"probe{k}", f"fiber{k}", "solid"),
                  (f"fiber{k}", f"spec{k}", "solid"), (f"spec{k}", model, "solid")]
        if not fused:
            nodes.append({"id": model, "cap": "Model", "text": f"Chemometric model ({method})", "row": 4, "lane": k,
                          "span": 1, "kind": "box"})
            edges.append((model, "result", "solid"))
    if fused:
        nodes.append({"id": "model", "cap": "Model", "row": 4, "lane": 0, "span": lanes, "kind": "box",
                      "text": "Chemometric model" if len(parts) <= 1 else "Data fusion model (per-method calibration)"})
        edges.append(("model", "result", "solid"))
    spectro = [p.name for p in used if p.measured_by.type == "spectroscopy"] or [p.name for p in used]
    nodes.append({"id": "result", "cap": "Result", "text": ", ".join(spectro) or "measured parameters", "row": 5,
                  "lane": 0, "span": lanes, "kind": "result"})
    aux = [p for p in used if p.measured_by.type == "auxiliary_sensor"]
    models = ["model"] if fused else [f"model{k}" for k in range(len(parts))]
    # Auxiliary sensors stack in one extra column (rows 1-3, beside probe/fiber/spectrometer); more are merged.
    names = [p.measured_by.sensor or p.name for p in aux]
    if len(names) > MAX_AUX_ROWS:
        names = names[:MAX_AUX_ROWS - 1] + [f"{names[MAX_AUX_ROWS - 1]}; and {len(names) - MAX_AUX_ROWS + 1} more"]
    for j, name in enumerate(names):
        nodes.append({"id": f"aux{j}", "cap": "Auxiliary sensor, confirm with AFS", "text": name, "row": 1 + j,
                      "lane": lanes, "span": 1, "kind": "aux"})
        edges += [(f"aux{j}", m, "aux") for m in models]
    return nodes, edges, lanes, lanes + (1 if names else 0)


def setup(a: Assessment, option: SolutionOption, slots: dict, width: float = 560.0) -> str:
    nodes, edges, lanes, total = setup_nodes(a, option, slots)
    pad, gap_lane, gap_row, bus = 2.0, 14.0, 26.0, 12.0
    size = 12.5 if width >= 480 else 11.5
    has_aux = total > lanes
    # method lanes are wider than the auxiliary column; the dashed bus runs at the right edge
    usable = width - 2 * pad - (total - 1) * gap_lane - (bus if has_aux else 0)
    lane_w = usable / (lanes * AUX_WEIGHT + (1 if has_aux else 0)) * AUX_WEIGHT
    aux_w = usable - lanes * lane_w
    for n in nodes:
        w = aux_w if n["kind"] == "aux" else n["span"] * lane_w + (n["span"] - 1) * gap_lane
        n["w"] = w
        n["cap_lines"] = _wrap(n["cap"], w - 16, 2, CAPTION)
        n["lines"] = _wrap(n["text"], w - 16, 5, size)
        n["h"] = (12 + (26 if n["kind"] == "proc" else 0) + len(n["cap_lines"]) * CAPTION * LINE
                  + len(n["lines"]) * size * LINE + 8)
    rows = max(n["row"] for n in nodes) + 1
    row_h = [max([n["h"] for n in nodes if n["row"] == r] or [0]) for r in range(rows)]
    row_y = [pad + sum(row_h[:r]) + r * gap_row for r in range(rows)]
    box = {}
    for n in nodes:
        x0 = pad + min(n["lane"], lanes) * (lane_w + gap_lane)
        y0 = row_y[n["row"]]
        box[n["id"]] = (x0, y0, x0 + n["w"], y0 + row_h[n["row"]])
    mid, defs = _marker()
    body = [defs]
    for src, dst, style in edges:        # under the boxes
        sx0, _, sx1, sy1 = box[src]
        dx0, dy0, dx1, dy1 = box[dst]
        if style == "aux":   # out of the sensor's right side, down the bus, into the model's right side
            sy = (box[src][1] + sy1) / 2
            bx, my = width - pad - bus / 2, (dy0 + dy1) / 2
            body.append(f'<polyline class="dg-edge dg-dashed" points="{sx1:.1f},{sy:.1f} {bx:.1f},{sy:.1f} '
                        f'{bx:.1f},{my:.1f} {dx1 + 1.5:.1f},{my:.1f}" marker-end="url(#{mid})"/>')
            continue
        narrow_src = (sx1 - sx0) <= (dx1 - dx0)
        x = (sx0 + sx1) / 2 if narrow_src else (dx0 + dx1) / 2
        body.append(f'<line class="dg-edge" x1="{x:.1f}" y1="{sy1:.1f}" x2="{x:.1f}" y2="{dy0 - 1.5:.1f}" '
                    f'marker-end="url(#{mid})"/>')
    for n in nodes:
        x0, y0, x1, y1 = box[n["id"]]
        w, h = x1 - x0, y1 - y0
        body.append(f'<rect class="dg-node dg-{n["kind"]}" x="{x0:.1f}" y="{y0:.1f}" width="{w:.1f}" '
                    f'height="{h:.1f}" rx="{10 if n["kind"] == "fiber" else 2}"/>')
        top = y0 + 12 + CAPTION * 0.8
        if n["kind"] == "proc":     # a pipe section with the flow direction
            py = y0 + 10
            body.append(f'<path class="dg-pipe" d="M{x0 + 10:.1f},{py:.1f} h{w - 20:.1f} M{x0 + 10:.1f},{py + 14:.1f} '
                        f'h{w - 20:.1f}"/><path class="dg-flow" d="M{x0 + 18:.1f},{py + 7:.1f} h{min(w - 40, 120):.1f}" '
                        f'marker-end="url(#{mid})"/>')
            top += 26
        body.append(_text(x0 + 8, top, n["cap_lines"], "dg-cap", CAPTION))
        body.append(_text(x0 + 8, top + len(n["cap_lines"]) * CAPTION * LINE + 4, n["lines"], "dg-txt", size))
    height = max(b[3] for b in box.values()) + pad
    label = "Setup sketch of the proposed option: " + "; ".join(f"{n['cap']}: {n['text']}" for n in nodes)
    return _svg(width, height, body, label, "fig-setup")


# --------------------------------------------------------------------------------------- spectral
LO_UM, HI_UM = 0.15, 30.0
TICKS_UM = [(0.2, "200 nm"), (0.4, "400 nm"), (1.0, "1 µm"), (2.5, "2.5 µm"), (5.0, "5 µm"), (10.0, "10 µm"),
            (25.0, "25 µm")]
TICKS_NARROW = {0.2, 1.0, 2.5, 10.0, 25.0}
WAVENUMBER_TICKS = [(2.5, "4000"), (5.0, "2000"), (10.0, "1000"), (25.0, "400")]
METHOD_ORDER = ("UV-Vis", "Fluorescence", "Raman", "NIR", "MIR")
METHOD_NOTE = {"Raman": "detection region", "Fluorescence": "UV/visible irradiation"}
FIBER_SOURCE = "S02 p.6"


def range_text(lo: float, hi: float) -> str:
    if hi <= 1.2:
        return f"{lo * 1000:.0f}–{hi * 1000:.0f} nm"
    return f"{lo:g}–{hi:g} µm"


def option_highlights(a: Assessment, option: SolutionOption | None) -> tuple[set[str], set[str], set[str]]:
    """Methods of the proposed option, methods of the other options, and fiber ids covering the proposed ones."""
    recs = {r.id: r for r in a.recommendations}
    proposed = {m for m, _ in option_parts(option, recs)} if option else set()
    others = {m for o in a.solution_options if o is not option for m, _ in option_parts(o, recs)} - proposed
    fibers = {c.fiber_id for m in proposed if m in METHOD_RANGES_UM
              for c in method_fiber_coverage(m) if c.status != "none"}
    return proposed, others, fibers


def spectral_rows(proposed: set[str], others: set[str], fiber_ids: set[str]) -> list[dict]:
    rows = []
    for m in METHOD_ORDER:
        r = METHOD_RANGES_UM[m]
        lo, hi = r["range_um"]
        note = METHOD_NOTE.get(m)
        rows.append({"group": "method", "name": m + (f" ({note})" if note else ""), "lo": lo, "hi": hi,
                     "range": range_text(lo, hi) + (" · 4000–400 cm⁻¹" if m == "MIR" else ""),
                     "source": r["source"], "state": "proposed" if m in proposed else ("other" if m in others else "")})
    for f in kb.fibers():
        rows.append({"group": "fiber", "name": f["name"].split(" (")[0], "lo": f["min_um"], "hi": f["max_um"],
                     "range": range_text(f["min_um"], f["max_um"]), "source": "",
                     "state": "fiber-used" if f["id"] in fiber_ids else "fiber"})
    return rows


def spectral(proposed: set[str], others: set[str], fiber_ids: set[str], width: float = 560.0) -> str:
    rows = spectral_rows(proposed, others, fiber_ids)
    narrow = width < 480
    size = 11.0
    pad, axis_top = 2.0, 30.0
    x0, x1 = pad + 4, width - pad - 18

    def x(um: float) -> float:
        return x0 + (math.log10(um) - math.log10(LO_UM)) / (math.log10(HI_UM) - math.log10(LO_UM)) * (x1 - x0)

    body: list[str] = []
    items, y = [], axis_top + 18
    for group, title in (("method", "Method ranges, nominal"),
                         ("fiber", f"Fiber transmission windows, {FIBER_SOURCE} (figure reading)")):
        items.append(("title", title, y))
        y += 18
        for r in (r for r in rows if r["group"] == group):
            label = f"{r['name']} · {r['range']}" + (f" · {r['source']}" if r["source"] else "")
            lines = _wrap(label, x1 - x0, 2, size)
            items.append(("row", (r, lines), y))
            y += len(lines) * size * LINE + 20
        y += 12
    bottom = y - 4
    for um, text in TICKS_UM:
        if narrow and um not in TICKS_NARROW:
            continue
        gx = x(um)
        body.append(f'<line class="sp-grid" x1="{gx:.1f}" y1="{axis_top:.1f}" x2="{gx:.1f}" y2="{bottom:.1f}"/>')
        body.append(_text(gx, axis_top - 7, [text], "sp-tick", 10.5, "middle"))
    body.append(f'<line class="sp-axis" x1="{x0:.1f}" y1="{axis_top:.1f}" x2="{x1:.1f}" y2="{axis_top:.1f}"/>')
    body.append(f'<line class="sp-axis" x1="{x0:.1f}" y1="{bottom:.1f}" x2="{x1:.1f}" y2="{bottom:.1f}"/>')
    for um, text in WAVENUMBER_TICKS:
        if narrow and um == 5.0:
            continue
        body.append(_text(x(um), bottom + 15, [text], "sp-tick", 10.5, "middle"))
    body.append(_text(x1, bottom + 31, ["wavenumber, cm⁻¹ (infrared)"], "sp-axis-label", 10.5, "end"))
    body.append(_text(x0, 10, ["wavelength, log scale"], "sp-axis-label", 10.5))
    for kind, item, yy in items:
        if kind == "title":
            body.append(_text(x0, yy, [item], "sp-group", 10.5))
            continue
        r, lines = item
        state = r["state"]
        body.append(_text(x0, yy + size, lines, "sp-label" + (" sp-label-on" if state == "proposed" else ""), size))
        bar_y = yy + len(lines) * size * LINE + 4
        bx0, bx1 = x(max(r["lo"], LO_UM)), x(min(r["hi"], HI_UM))
        body.append(f'<rect class="sp-bar sp-{state or "off"}" x="{bx0:.1f}" y="{bar_y:.1f}" '
                    f'width="{bx1 - bx0:.1f}" height="9" rx="1.5"><title>{escape(r["name"])}: {escape(r["range"])}'
                    f'</title></rect>')
    height = bottom + 38
    return _svg(width, height, body, "Nominal spectral ranges of the methods and fiber transmission windows on a "
                                     "logarithmic wavelength axis; methods of the proposed option highlighted",
                "fig-spectral")


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


def parameter_map(a: Assessment, width: float = 900.0) -> str:
    if not a.parameters:
        return ""
    narrow = width < 480
    size = 11.5 if narrow else 12.5
    pad, gap = 2.0, 10.0
    col_w = (width - 2 * pad) * (0.40 if narrow else 0.36)
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
