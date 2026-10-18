"""Hand-written blueprint SVG for the mockup (option O2 of a saved dev run).

Colours come from CSS custom properties on the wrapper (--bp-ink, --bp-faint,
--bp-accent, --bp-paper, --bp-callout), so one markup serves all directions.
No ids, no markers: arrowheads are explicit polygons.
"""


def arrow(x1, y1, x2, y2, cls="ln"):
    # straight arrow, head at (x2,y2); horizontal or vertical only
    if y1 == y2:
        d = 1 if x2 > x1 else -1
        head = f"{x2},{y2} {x2 - 8 * d},{y2 - 4} {x2 - 8 * d},{y2 + 4}"
    else:
        d = 1 if y2 > y1 else -1
        head = f"{x2},{y2} {x2 - 4},{y2 - 8 * d} {x2 + 4},{y2 - 8 * d}"
    return (f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>'
            f'<polygon class="head" points="{head}"/>')


def hatch(x0, y0, x1, y1, step=6):
    out = [f'<rect class="thin" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/>']
    h = y1 - y0
    x = x0 - h
    while x < x1:
        ax, ay, bx, by = x, y1, x + h, y0
        # clip to rect
        if ax < x0:
            ay -= x0 - ax
            ax = x0
        if bx > x1:
            by += bx - x1
            bx = x1
        out.append(f'<line class="hair" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}"/>')
        x += step
    return "".join(out)


def callout(x, y, label, lx=None, ly=None, linked=False):
    s = ""
    if lx is not None:
        s += f'<line class="hair lead" x1="{x}" y1="{y}" x2="{lx}" y2="{ly}"/><circle class="dot" cx="{lx}" cy="{ly}" r="2.2"/>'
    cls = "co linked" if linked else "co"
    s += (f'<g class="{cls}"><circle cx="{x}" cy="{y}" r="13"/>'
          f'<text x="{x}" y="{y + 4}" text-anchor="middle">{label}</text></g>')
    return s


def text(x, y, s, cls="lbl", anchor="start"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>'


def spectrometer(x, y, name):
    w, h = 180, 74
    s = f'<rect class="ln box" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    # slit, grating, detector
    s += f'<line class="thk" x1="{x + 14}" y1="{y + 30}" x2="{x + 14}" y2="{y + 52}"/>'
    s += f'<line class="hair" x1="{x + 14}" y1="{y + 41}" x2="{x + 70}" y2="{y + 41}"/>'
    s += hatch(x + 70, y + 30, x + 88, y + 54, 4)
    s += f'<line class="hair" x1="{x + 88}" y1="{y + 41}" x2="{x + 150}" y2="{y + 36}"/>'
    s += f'<line class="hair" x1="{x + 88}" y1="{y + 44}" x2="{x + 150}" y2="{y + 50}"/>'
    s += f'<rect class="thin" x="{x + 150}" y="{y + 28}" width="10" height="28"/>'
    s += text(x + 10, y + 18, name, "cap")
    return s


def model_box(x, y, title, sub):
    w, h = 170, 74
    s = f'<rect class="ln box" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    # tiny calibration plot
    s += f'<polyline class="thin" points="{x + 122},{y + 22} {x + 122},{y + 60} {x + 160},{y + 60}"/>'
    s += f'<line class="hair" x1="{x + 124}" y1="{y + 58}" x2="{x + 158}" y2="{y + 26}"/>'
    for dx, dy in ((6, -8), (13, -16), (20, -20), (27, -29), (33, -31)):
        s += f'<circle class="pt" cx="{x + 124 + dx}" cy="{y + 58 + dy}" r="1.6"/>'
    s += text(x + 10, y + 26, title, "cap")
    s += text(x + 10, y + 44, sub, "lbl sm")
    return s


def svg() -> str:
    p = []
    W, H = 1000, 480
    # ---- pipe section (process point) ------------------------------------
    p.append(hatch(30, 204, 262, 216, 6))
    p.append(hatch(30, 264, 262, 276, 6))
    p.append('<line class="hair chain" x1="18" y1="240" x2="276" y2="240"/>')
    # break lines at the cut ends
    for x in (30, 262):
        p.append(f'<polyline class="thin" points="{x},198 {x},226 {x - 5},233 {x + 5},247 {x},254 {x},282"/>')
    p.append(arrow(44, 232, 92, 232, "thin"))
    p.append(text(44, 256, "whey stream", "lbl it sm"))
    # ---- probe 1: NIR transmission/transflection, from the top ---------
    x = 120
    p.append(f'<rect class="ln" x="{x - 15}" y="190" width="30" height="14"/>')
    p.append(f'<rect class="ln" x="{x - 6}" y="104" width="12" height="86"/>')
    p.append(f'<rect class="ln" x="{x - 6}" y="204" width="12" height="20"/>')
    p.append(f'<rect class="thin" x="{x - 6}" y="230" width="12" height="6"/>')  # mirror past the gap
    p.append(f'<line class="hair" x1="{x - 6}" y1="224" x2="{x - 6}" y2="230"/><line class="hair" x1="{x + 6}" y1="224" x2="{x + 6}" y2="230"/>')
    p.append(f'<rect class="ln" x="{x - 10}" y="88" width="20" height="16"/>')
    # ---- probe 2: MIR ATR, from the bottom -------------------------------
    x = 216
    p.append(f'<rect class="ln" x="{x - 15}" y="276" width="30" height="14"/>')
    p.append(f'<rect class="ln" x="{x - 7}" y="290" width="14" height="86"/>')
    p.append(f'<rect class="ln" x="{x - 7}" y="256" width="14" height="20"/>')
    p.append(f'<polygon class="ln" points="{x - 7},256 {x + 7},256 {x},246"/>')  # ATR crystal
    p.append(f'<rect class="ln" x="{x - 10}" y="376" width="20" height="16"/>')
    # ---- auxiliary sensors (dashed = availability to be confirmed) -------
    p.append('<rect class="dash" x="56" y="168" width="14" height="36"/>')
    p.append('<rect class="dash" x="56" y="276" width="14" height="36"/>')
    # ---- fibers -----------------------------------------------------------
    p.append('<path class="fib" d="M130 96 C220 96, 270 116, 380 116"/>')
    p.append('<path class="fib" d="M226 384 C290 384, 305 350, 380 350"/>')
    # ---- spectrometers ------------------------------------------------------
    p.append(spectrometer(380, 80, "NIR SPECTROMETER"))
    p.append(spectrometer(380, 314, "MIR SPECTROMETER"))
    p.append(arrow(560, 117, 616, 117))
    p.append(arrow(560, 351, 616, 351))
    # ---- PC / chemometrics -------------------------------------------------
    p.append('<rect class="dash pc" x="604" y="62" width="196" height="348"/>')
    p.append(text(614, 236, "PC · CHEMOMETRICS", "cap faint"))
    p.append(model_box(618, 80, "MODEL (NIR)", "chemometric model"))
    p.append(model_box(618, 314, "MODEL (MIR)", "chemometric model"))
    # ---- result --------------------------------------------------------------
    p.append('<polyline class="ln" points="788,117 830,117 830,234"/>')
    p.append('<polyline class="ln" points="788,351 830,351 830,234"/>')
    p.append(arrow(830, 234, 856, 234))
    p.append('<rect class="thk box" x="856" y="196" width="130" height="76"/>')
    p.append(text(866, 220, "RESULT", "cap"))
    p.append(text(866, 240, "protein", "lbl"))
    p.append(text(866, 256, "concentration", "lbl"))
    # aux signal routes (dashed) into the models
    p.append('<polyline class="dash" points="63,168 63,40 703,40 703,72"/>')
    p.append('<polygon class="head" points="703,80 699,72 707,72"/>')
    p.append('<polyline class="dash" points="63,312 63,424 703,424 703,396"/>')
    p.append('<polygon class="head" points="703,388 699,396 707,396"/>')
    # ---- labels -----------------------------------------------------------------
    p.append(text(140, 70, "NIR transmission/transflection probe", "lbl b"))
    p.append(text(196, 140, "fiber: silica or chalcogenide or", "lbl it sm"))
    p.append(text(196, 154, "hollow waveguide…", "lbl it sm"))
    p.append(text(128, 414, "MIR ATR probe · conditional", "lbl b"))
    p.append(text(262, 300, "fiber: chalcogenide or", "lbl it sm"))
    p.append(text(262, 314, "polycrystalline or hollow", "lbl it sm"))
    p.append(text(262, 328, "waveguide…", "lbl it sm"))
    p.append(text(80, 30, "turbidity / optical-density sensor", "lbl sm"))
    p.append(text(80, 444, "temperature sensor (confirm with AFS)", "lbl sm"))
    p.append(text(84, 298, "PROCESS POINT", "cap"))
    p.append(text(84, 313, "whey line, before the", "lbl sm") + text(84, 326, "concentration stage", "lbl sm"))
    # ---- callouts (ids match the sections below) ---------------------------
    p.append(callout(296, 240, "Q3", 264, 240))
    p.append(callout(96, 140, "M1", 113, 150))
    p.append(callout(180, 352, "M2", 208, 352))
    p.append(callout(40, 60, "P2", 56, 176, linked=True))
    p.append(callout(40, 410, "P3", 56, 300))
    p.append(callout(921, 172, "P1", 921, 196))
    # ---- title block ------------------------------------------------------------
    tb = ('<g class="tb">'
          '<rect class="ln" x="604" y="436" width="382" height="38"/>'
          '<line class="thin" x1="764" y1="436" x2="764" y2="474"/>'
          '<line class="thin" x1="900" y1="436" x2="900" y2="474"/>'
          + text(612, 451, "SETUP SKETCH", "cap tiny")
          + text(612, 467, "Option O2 · recommended", "lbl sm")
          + text(772, 451, "SCHEMATIC", "cap tiny")
          + text(772, 467, "not a configuration", "lbl sm")
          + text(908, 451, "SHEET", "cap tiny")
          + text(908, 467, "1 / 1", "lbl sm")
          + '</g>')
    p.append(tb)
    body = "".join(p)
    return (f'<svg class="bp" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="Setup sketch, option O2: whey line with an NIR transmission/transflection probe and a conditional MIR ATR probe, '
            f'each on a fiber to its spectrometer and chemometric model, giving protein concentration; dashed auxiliary turbidity and temperature sensors">'
            f'{body}</svg>')


if __name__ == "__main__":
    print(svg())
