"""Round-2 blueprint SVGs for option O2 of outputs/dev/D03.json (hand-drawn mockup, not app code).

Two drawings, like the app's diagrams.py: a wide one (needs >= ~860 px so text renders >= 12 px)
and a narrow vertical one for phones (viewBox 360 wide, rendered ~1:1).
Colours come from CSS custom properties (--bp-ink, --bp-accent, --bp-co-ink, --bp-box, --bp-mark).
No ids and no markers; arrowheads are polygons. No opacity on text.
Callout style 'id' = filled circle with the ID; 'pill' = section number + ID.
"""

SEC = {"P1": 4, "P2": 4, "P3": 4, "M1": 3, "M2": 3, "Q3": 5}


def t(x, y, s, cls="lbl", anchor="start"):
    return f'<text class="{cls}" x="{x}" y="{y}" text-anchor="{anchor}">{s}</text>'


def arrow(x1, y1, x2, y2, cls="ln"):
    if y1 == y2:
        d = 1 if x2 > x1 else -1
        head = f"{x2},{y2} {x2 - 9 * d},{y2 - 4.5} {x2 - 9 * d},{y2 + 4.5}"
    else:
        d = 1 if y2 > y1 else -1
        head = f"{x2},{y2} {x2 - 4.5},{y2 - 9 * d} {x2 + 4.5},{y2 - 9 * d}"
    return f'<line class="{cls}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/><polygon class="head" points="{head}"/>'


def hatch(x0, y0, x1, y1, step=6):
    out = [f'<rect class="thin" x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}"/>']
    h = y1 - y0
    x = x0 - h
    while x < x1:
        ax, ay, bx, by = x, y1, x + h, y0
        if ax < x0:
            ay -= x0 - ax
            ax = x0
        if bx > x1:
            by += bx - x1
            bx = x1
        out.append(f'<line class="hair" x1="{ax}" y1="{ay}" x2="{bx}" y2="{by}"/>')
        x += step
    return "".join(out)


def callout(x, y, cid, style, lx=None, ly=None, linked=False):
    s = ""
    if lx is not None:
        s += f'<line class="lead" x1="{x}" y1="{y}" x2="{lx}" y2="{ly}"/><circle class="dot" cx="{lx}" cy="{ly}" r="2.6"/>'
    cls = "co linked" if linked else "co"
    if style == "pill":
        w = 54
        s += (f'<g class="{cls} pill" data-part="{cid}"><rect x="{x - w / 2}" y="{y - 13}" width="{w}" height="26" rx="13"/>'
              f'<rect class="sec" x="{x - w / 2}" y="{y - 13}" width="22" height="26" rx="11"/>'
              f'<text class="secn" x="{x - w / 2 + 11}" y="{y + 5}" text-anchor="middle">{SEC[cid]}</text>'
              f'<text x="{x + 10}" y="{y + 5}" text-anchor="middle">{cid}</text></g>')
    else:
        s += (f'<g class="{cls}" data-part="{cid}"><circle cx="{x}" cy="{y}" r="15"/>'
              f'<text x="{x}" y="{y + 5}" text-anchor="middle">{cid}</text></g>')
    return s


# ------------------------------------------------------------------ wide
def spectrometer(x, y, name, w=170, h=74):
    s = f'<rect class="ln box" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    s += f'<line class="thk" x1="{x + 14}" y1="{y + 34}" x2="{x + 14}" y2="{y + 58}"/>'
    s += f'<line class="hair" x1="{x + 14}" y1="{y + 46}" x2="{x + 66}" y2="{y + 46}"/>'
    s += hatch(x + 66, y + 34, x + 84, y + 58, 4)
    s += f'<line class="hair" x1="{x + 84}" y1="{y + 45}" x2="{x + 140}" y2="{y + 40}"/>'
    s += f'<line class="hair" x1="{x + 84}" y1="{y + 48}" x2="{x + 140}" y2="{y + 54}"/>'
    s += f'<rect class="thin" x="{x + 140}" y="{y + 32}" width="10" height="28"/>'
    s += t(x + 10, y + 21, name, "cap")
    return s


def model_box(x, y, title, w=170, h=74):
    s = f'<rect class="ln box" x="{x}" y="{y}" width="{w}" height="{h}"/>'
    s += f'<polyline class="thin" points="{x + 124},{y + 26} {x + 124},{y + 62} {x + 160},{y + 62}"/>'
    s += f'<line class="hair" x1="{x + 126}" y1="{y + 60}" x2="{x + 158}" y2="{y + 30}"/>'
    for dx, dy in ((6, -8), (13, -15), (20, -19), (26, -27)):
        s += f'<circle class="pt" cx="{x + 126 + dx}" cy="{y + 60 + dy}" r="1.8"/>'
    s += t(x + 10, y + 26, title, "cap")
    s += t(x + 10, y + 46, "chemometric", "sm")
    s += t(x + 10, y + 63, "model", "sm")
    return s


def wide(style="id", linked="P2"):
    p = []
    # pipe
    p.append(hatch(30, 204, 292, 216))
    p.append(hatch(30, 264, 292, 276))
    p.append('<line class="hair chain" x1="18" y1="240" x2="304" y2="240"/>')
    for x in (30, 292):
        p.append(f'<polyline class="thin" points="{x},198 {x},226 {x - 5},233 {x + 5},247 {x},254 {x},282"/>')
    p.append(arrow(44, 232, 92, 232, "thin"))
    p.append(t(44, 258, "whey stream", "sm it"))
    # probe 1 (NIR transmission/transflection, top)
    x = 120
    p.append(f'<rect class="ln" x="{x - 15}" y="190" width="30" height="14"/>')
    p.append(f'<rect class="ln" x="{x - 6}" y="104" width="12" height="86"/>')
    p.append(f'<rect class="ln" x="{x - 6}" y="204" width="12" height="20"/>')
    p.append(f'<rect class="thin" x="{x - 6}" y="230" width="12" height="6"/>')
    p.append(f'<rect class="ln" x="{x - 10}" y="88" width="20" height="16"/>')
    # probe 2 (MIR ATR, bottom)
    x = 236
    p.append(f'<rect class="ln" x="{x - 15}" y="276" width="30" height="14"/>')
    p.append(f'<rect class="ln" x="{x - 7}" y="290" width="14" height="86"/>')
    p.append(f'<rect class="ln" x="{x - 7}" y="256" width="14" height="20"/>')
    p.append(f'<polygon class="ln" points="{x - 7},256 {x + 7},256 {x},246"/>')
    p.append(f'<rect class="ln" x="{x - 10}" y="376" width="20" height="16"/>')
    # aux sensors
    p.append('<rect class="dash" x="56" y="168" width="14" height="36"/>')
    p.append('<rect class="dash" x="56" y="276" width="14" height="36"/>')
    # fibers
    p.append('<path class="fib" d="M130 96 C230 96, 300 127, 430 127"/>')
    p.append('<path class="fib" d="M246 384 C320 384, 340 363, 430 363"/>')
    # spectrometers, models, result
    p.append(spectrometer(430, 90, "NIR SPECTROMETER"))
    p.append(spectrometer(430, 326, "MIR SPECTROMETER"))
    p.append(arrow(600, 127, 668, 127))
    p.append(arrow(600, 363, 668, 363))
    p.append('<rect class="dash" x="654" y="70" width="200" height="352"/>')
    p.append(t(668, 252, "PC · CHEMOMETRICS", "cap"))
    p.append(model_box(670, 90, "MODEL (NIR)"))
    p.append(model_box(670, 326, "MODEL (MIR)"))
    p.append('<polyline class="ln" points="840,127 864,127 864,246"/>')
    p.append('<polyline class="ln" points="840,363 864,363 864,246"/>')
    p.append(arrow(864, 246, 878, 246))
    p.append('<rect class="thk box" x="878" y="204" width="114" height="84"/>')
    p.append(t(888, 228, "RESULT", "cap"))
    p.append(t(888, 250, "protein", "lbl"))
    p.append(t(888, 270, "concentration", "lbl"))
    # aux routes
    p.append('<polyline class="dash" points="63,168 63,44 755,44 755,82"/>')
    p.append('<polygon class="head" points="755,90 750.5,81 759.5,81"/>')
    p.append('<polyline class="dash" points="63,312 63,436 755,436 755,408"/>')
    p.append('<polygon class="head" points="755,400 750.5,409 759.5,409"/>')
    # labels
    p.append(t(84, 34, "turbidity / optical-density sensor", "sm"))
    p.append(t(84, 458, "temperature sensor (confirm with AFS)", "sm"))
    p.append(t(146, 72, "NIR transmission/transflection probe", "lbl b"))
    p.append(t(196, 146, "fiber: silica or chalcogenide or", "sm it"))
    p.append(t(196, 163, "hollow waveguide…", "sm it"))
    p.append(t(126, 420, "MIR ATR probe · conditional", "lbl b"))
    p.append(t(282, 302, "fiber: chalcogenide or", "sm it"))
    p.append(t(282, 319, "polycrystalline or hollow", "sm it"))
    p.append(t(282, 336, "waveguide…", "sm it"))
    p.append(t(80, 300, "PROCESS POINT", "cap"))
    p.append(t(80, 318, "whey line, before the", "sm"))
    p.append(t(80, 335, "concentration stage", "sm"))
    # callouts
    pill = style == "pill"
    p.append(callout(336 if not pill else 346, 240, "Q3", style, 294, 240))
    p.append(callout(84 if not pill else 70, 140, "M1", style, 113, 150))
    p.append(callout(188 if not pill else 176, 356, "M2", style, 228, 356))
    p.append(callout(34 if not pill else 40, 78, "P2", style, 56, 176, linked == "P2"))
    p.append(callout(34 if not pill else 40, 404, "P3", style, 56, 300, linked == "P3"))
    p.append(callout(935, 180, "P1", style, 935, 204, linked == "P1"))
    # title block
    p.append('<rect class="ln" x="560" y="452" width="432" height="44"/>'
             '<line class="thin" x1="760" y1="452" x2="760" y2="496"/><line class="thin" x1="912" y1="452" x2="912" y2="496"/>'
             + t(570, 469, "SETUP SKETCH", "cap tb") + t(570, 488, "Option O2 · recommended", "sm")
             + t(770, 469, "SCHEMATIC", "cap tb") + t(770, 488, "not a configuration", "sm")
             + t(922, 469, "SHEET", "cap tb") + t(922, 488, "1 / 1", "sm"))
    return ('<svg class="bp" viewBox="0 0 1000 504" role="img" aria-label="'
            'Setup sketch, option O2: whey line with an NIR transmission/transflection probe and a conditional MIR ATR probe, '
            'each on a fiber to its spectrometer and chemometric model, giving protein concentration; dashed: auxiliary turbidity '
            'and temperature sensors">' + "".join(p) + "</svg>")


# ------------------------------------------------------------------ narrow (phones)
def narrow(style="id", linked="P2"):
    p = []
    L, R = 116, 246
    p.append(t(20, 26, "PROCESS POINT", "cap"))
    p.append(t(20, 44, "whey line, before the concentration stage", "sm"))
    p.append(hatch(20, 62, 340, 72))
    p.append(hatch(20, 108, 340, 118))
    p.append('<line class="hair chain" x1="10" y1="90" x2="350" y2="90"/>')
    p.append(arrow(150, 90, 206, 90, "thin"))
    # aux sensors on top wall
    p.append('<rect class="dash" x="36" y="50" width="12" height="12"/>' if False else "")
    p.append('<rect class="dash" x="30" y="118" width="12" height="30"/>')
    p.append('<rect class="dash" x="48" y="118" width="12" height="30"/>')
    # probes going down
    for x, atr in ((L, False), (R, True)):
        p.append(f'<rect class="ln" x="{x - 14}" y="118" width="28" height="12"/>')
        p.append(f'<rect class="ln" x="{x - 6}" y="96" width="12" height="22"/>')
        if atr:
            p.append(f'<polygon class="ln" points="{x - 6},96 {x + 6},96 {x},86"/>')
        p.append(f'<rect class="ln" x="{x - 6}" y="130" width="12" height="54"/>')
        p.append(f'<rect class="ln" x="{x - 9}" y="184" width="18" height="14"/>')
    p.append(t(L, 220, "NIR transmission/", "sm b", "middle"))
    p.append(t(L, 236, "transflection probe", "sm b", "middle"))
    p.append(t(R, 220, "MIR ATR probe", "sm b", "middle"))
    p.append(t(R, 236, "conditional", "sm b", "middle"))
    # fibers (wavy verticals)
    for x in (L, R):
        p.append(f'<path class="fib" d="M{x} 244 C{x - 14} 262, {x + 14} 278, {x} 296"/>')
    p.append(t(L + 14, 258, "fiber: silica,", "xs it"))
    p.append(t(L + 14, 273, "chalcogenide…", "xs it"))
    p.append(t(R + 14, 258, "fiber:", "xs it"))
    p.append(t(R + 14, 273, "chalcogenide,", "xs it"))
    p.append(t(R + 14, 288, "polycrystal…", "xs it"))
    # spectrometers
    for x, n in ((L, "NIR"), (R, "MIR")):
        p.append(f'<rect class="ln box" x="{x - 62}" y="300" width="124" height="58"/>')
        p.append(t(x - 52, 322, f"{n} SPECTRO-", "cap"))
        p.append(t(x - 52, 340, "METER", "cap"))
        p.append(arrow(x, 358, x, 404))
    # aux bus
    p.append('<polyline class="dash" points="36,148 36,380 276,380"/><line class="dash" x1="54" y1="148" x2="54" y2="380"/>')
    for x in (L - 30, R + 30):
        p.append(f'<line class="dash" x1="{x}" y1="380" x2="{x}" y2="398"/><polygon class="head" points="{x},406 {x - 4.5},397 {x + 4.5},397"/>')
    # models
    for x, n in ((L, "NIR"), (R, "MIR")):
        p.append(f'<rect class="ln box" x="{x - 62}" y="406" width="124" height="58"/>')
        p.append(t(x - 52, 428, f"MODEL ({n})", "cap"))
        p.append(t(x - 52, 448, "chemometric", "sm"))
    p.append(f'<polyline class="ln" points="{L},464 {L},488 {R},488 {R},464"/>')
    p.append(arrow(180, 488, 180, 512))
    p.append('<rect class="thk box" x="100" y="512" width="160" height="66"/>')
    p.append(t(112, 536, "RESULT", "cap"))
    p.append(t(112, 558, "protein concentration", "sm"))
    # legend for aux sensors
    p.append(t(20, 612, "dashed: auxiliary sensors (P2 turbidity /", "sm"))
    p.append(t(20, 630, "optical density, P3 temperature), confirm", "sm"))
    p.append(t(20, 648, "availability with AFS; signals go to both models", "sm"))
    # callouts
    pill = style == "pill"
    p.append(callout(318 if not pill else 306, 30, "Q3", style, 300, 62))
    p.append(callout(L + 44 if not pill else L + 50, 165, "M1", style, L + 6, 165))
    p.append(callout(R + 44 if not pill else R + 50, 165, "M2", style, R + 6, 165))
    p.append(callout(18 if not pill else 32, 186, "P2", style, 36, 150, linked == "P2"))
    p.append(callout(18 if not pill else 32, 262, "P3", style, 54, 150, linked == "P3"))
    p.append(callout(296 if not pill else 302, 545, "P1", style, 260, 545, linked == "P1"))
    p.append('<rect class="ln" x="20" y="668" width="320" height="44"/><line class="thin" x1="200" y1="668" x2="200" y2="712"/>'
             + t(30, 685, "SETUP SKETCH", "cap tb") + t(30, 704, "Option O2 · recommended", "sm")
             + t(210, 685, "SCHEMATIC", "cap tb") + t(210, 704, "not a configuration", "sm"))
    return ('<svg class="bp" viewBox="0 0 360 720" role="img" aria-label="'
            'Setup sketch, option O2, drawn top to bottom: whey line; NIR transmission/transflection probe and conditional MIR ATR probe; '
            'fibers; NIR and MIR spectrometers; one chemometric model each; result protein concentration; dashed auxiliary sensors">'
            + "".join(p) + "</svg>")
