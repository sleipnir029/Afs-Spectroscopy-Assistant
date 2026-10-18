"""Build docs/mockups/index.html. All content strings are copied from outputs/dev/D03.json."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bp import svg

HERE = pathlib.Path(__file__).parent
OUT = HERE.parent / "index.html"
SVG = svg()

ENQ = ("Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate "
       "whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the "
       "reference. The stream can become more turbid under some operating conditions. We need a first measurement concept "
       "that handles this change rather than assuming the liquid always remains clear.")
HEAD = "Start with NIR transmission/transflection."
SUM = ("The sources name whey as a preferred case for it, and it is the least effort. Because the stream can turn turbid, "
       "keep mid-IR ATR as the fallback and treat a fused NIR plus mid-IR ATR model as a later hypothesis. The protein "
       "range, required accuracy and the nature of the turbidity are still open.")
STATUS = "Provisional feasibility assessment"
NEXT = "Answer Q1 to Q3 and run the sample series with NIR transmission first, then mid-IR ATR on the same samples."
CHANGE = ("If the required accuracy or the turbidity range shows that NIR transmission cannot cover the stream, the choice "
          "moves to M2 alone or to the fused M3.")
CONF = "Medium"
CONF_WHY = "open question: Q1, Q2"
CHIPS = ["S01 p.18", "S01 p.5", "S01 p.13", "S04 p.4", "S01 p.9"]
EXT = "E02 ¶12"
COST = "high cost (rows 2, 7)"
EASE = "two probes, one method at a time"
UPKEEP = "two probes, two calibrations to keep"
FIT = "covers clear and turbid operating states"
DRIVERS = "NIR and MIR spectrometers, MIR fibers, ATR probe"
M1 = ("NIR, transmission/transflection probe", "primary",
      "Applies while the stream stays clear enough for transmission with a controlled optical pathlength.")
M2 = ("MIR, ATR probe", "conditional", "Applies only if the turbid operating state defeats NIR transmission.")
PARAMS = [
    ("P1", "protein concentration", "required", "Spectroscopy: NIR", "It is the stated target of the investigation.", "S01 p.17"),
    ("P2", "turbidity (optical density) of the stream", "required",
     "Auxiliary sensor: inline turbidity or optical-density sensor (cited; confirm availability with AFS)",
     "The stream can become more turbid, and physical variation can mimic a composition change, so the state must be recorded with each spectrum.",
     "S01 p.7"),
    ("P3", "process temperature at the measurement point", "optional",
     "Auxiliary sensor: temperature sensor (engineering judgement: confirm availability with AFS)",
     "Temperature shifts the water and protein bands and the physical state of the stream; a temperature signal should already be available at a dairy process point.",
     None),
]
QS = [
    ("Q1", "What protein concentration range must be covered, and what accuracy and response time are required?",
     "These decide whether one method can cover the target and they set the go/no-go criteria for the test."),
    ("Q2", "How turbid does the stream become, and what causes the turbidity (particles, fat or dissolved species)?",
     "The severity and nature decide whether NIR transmission still works or whether ATR is needed."),
    ("Q3", "Where is the measurement point, is it in-line in the pipe, in a bypass or at-line, and how far is the analyzer from it?",
     "This fixes the probe type and the fiber link, which differ between NIR and mid-IR."),
]
QUOTES = [  # verified quotes from D03.json citations
    ("S01 p.18", "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."),
    ("S01 p.13", "typically at a depth of few microns"),
    ("S01 p.18", "it fails when the milk becomes too “thick” or fat-rich, as the light cannot penetrate the sample."),
]
TABS = [("Simple", "NIR · least effort"), ("Recommended", "NIR + MIR · best fit"), ("Extended", "NIR + MIR · several methods")]


def chips(cls="chip"):
    return "".join(f'<span class="{cls}">{c}</span>' for c in CHIPS) + f'<span class="{cls} ext">{EXT} · external, not AFS material</span>'


# ------------------------------------------------------------------ A
def dir_a(dark=False):
    if dark:
        return f'''<div class="A dark"><div class="in" style="padding:22px">
<div class="eyebrow"><b>1</b>Our recommendation</div><h1>{HEAD}</h1>
<p>{SUM.split(". ")[0]}.</p>
<div style="font-size:14px"><span class="meter"><i class="f"></i><i class="f"></i><i></i></span><b>{CONF} confidence</b> · {CONF_WHY}</div>
<div class="chips" style="margin-top:8px">{chips()}</div>
<div class="fig mini" style="padding:10px">{SVG}</div></div></div>'''
    rows = "".join(
        f'<tr class="{"hl" if p[0] == "P2" else ""}"><td><span class="id">{p[0]}</span>{p[1]}</td><td>{p[2]}</td><td>{p[3]}</td><td>{p[4]}</td>'
        f'<td>{f"<span class=chip>{p[5]}</span>" if p[5] else "<span class=eng>engineering judgement, no source</span>"}</td></tr>'
        for p in PARAMS)
    qs = "".join(f'<li><b><span class="id">{q[0]}</span></b>{q[1]}<small>Why it matters: {q[2]}</small></li>' for q in QS)
    return f'''<div class="A">
<div class="top"><div class="brand">AFS Spectroscopy Assistant<small>In-line measurement advice, every claim sourced</small></div>
<div><span class="btn">Examples</span><span class="btn">Dark</span><span class="btn pri">New question</span></div></div>
<div class="page">
<nav class="rail"><h4>On this page</h4>
<a class="on" href="#"><b>1</b>Answer</a><a href="#"><b>2</b>Setup drawing</a><a href="#"><b>3</b>Options</a><a href="#"><b>4</b>What to measure</a><a href="#"><b>5</b>Open questions</a>
<h4 style="margin-top:28px">Status</h4><div style="font-size:14px;color:var(--muted)">{STATUS}</div></nav>
<main>
<div class="q"><div class="lab">Your question</div>{ENQ}</div>
<div class="card">
<div class="eyebrow"><b>1</b>Our recommendation</div>
<h1>{HEAD}</h1>
<p class="sum">{SUM}</p>
<dl class="facts">
<dt>Confidence</dt><dd><span class="meter"><i class="f"></i><i class="f"></i><i></i></span><b>{CONF}</b> · {CONF_WHY}</dd>
<dt>Sources</dt><dd><div class="chips">{chips()}</div></dd>
<dt>Next step</dt><dd>{NEXT}</dd>
<dt>What would change it</dt><dd>{CHANGE}</dd>
</dl></div>

<section><div class="eyebrow"><b>2</b>Setup drawing</div><h2>How it would be set up</h2>
<div class="fig">{SVG}</div>
<div class="figcap"><span class="co">P2</span> Callouts carry the IDs used below: P = what is measured (§4), M = method (§3), Q = open question (§5). Dashed means an auxiliary sensor whose availability is to be confirmed with AFS. Drawn by code from the option: a schematic, not a configuration.</div></section>

<section><div class="eyebrow"><b>3</b>Options</div><h2>Three ways to start</h2>
<div class="tabs">{"".join(f'<div class="tab{" on" if t[0]=="Recommended" else ""}"><b>{t[0]}</b>{t[1]}</div>' for t in TABS)}</div>
<div class="grid4"><div><div class="k">Cost class</div>{COST}<div class="chips"><span class="chip">S01 Table 1 (p.6)</span></div></div>
<div><div class="k">Ease of use</div>{EASE}</div><div><div class="k">Upkeep</div>{UPKEEP}</div>
<div><div class="k">Confidence</div><span class="meter"><i class="f"></i><i class="f"></i><i></i></span>{CONF}<br><small style="color:var(--muted)">{CONF_WHY}</small></div></div>
<ul class="meth"><li><span class="id">M1</span><b>{M1[0]}</b> · {M1[1]}. {M1[2]}</li><li><span class="id">M2</span><b>{M2[0]}</b> · {M2[1]}. {M2[2]}</li>
<li><span style="color:var(--muted)">Why this option:</span> {FIT}. <span style="color:var(--muted)">Cost drivers:</span> {DRIVERS}.</li></ul></section>

<section><div class="eyebrow"><b>4</b>What to measure</div>
<details open><summary>What to measure and how <span>3 parameters</span></summary>
<table class="t"><thead><tr><th>Parameter</th><th>Need</th><th>Measured by</th><th>Why</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table>
<div class="hlnote">Hover state shown: pointing at P2 on the drawing highlights this row, and the other way round.</div></details></section>

<section><div class="eyebrow"><b>5</b>Open questions</div><h2>What we still need to know</h2><ol class="qs">{qs}</ol></section>
</main><div></div></div></div>'''


# ------------------------------------------------------------------ B
def dir_b(dark=False):
    if dark:
        return f'''<div class="B dark"><div class="in" style="padding:22px">
<div class="sc">§1 · Answer</div><h1 style="font-weight:500">{HEAD}</h1><p>{SUM.split(". ")[0]}.<sup>1</sup></p>
<div style="font-size:14px"><i style="color:var(--muted)">Confidence</i> {CONF} · {CONF_WHY}</div>
<div class="plate mini" style="padding:12px">{SVG}</div></div></div>'''
    side = "".join(f'<li><b>{i + 1}</b><span class="cite">{q[0]}</span> — “{q[1]}”</li>' for i, q in enumerate(QUOTES))
    rows = "".join(
        f'<tr><td class="id">{p[0]}</td><td>{p[1]}</td><td><i>{p[2]}</i></td><td>{p[3]}</td><td>{p[4]}</td><td>{p[5] or "<i>engineering judgement</i>"}</td></tr>'
        for p in PARAMS)
    qs = "".join(f'<li><b>{q[0]}</b>{q[1]}<em>{q[2]}</em></li>' for q in QS)
    return f'''<div class="B">
<div class="mast"><div class="name">AFS Spectroscopy Assistant</div><div class="sub">A first technical assessment, every claim sourced</div>
<nav><span>Examples</span><span>Dark</span><span class="pri">New question</span></nav></div>
<div class="page">
<div class="sc" style="margin-bottom:10px">The enquiry</div>
<blockquote>{ENQ}</blockquote>
<div class="sc">§1 · Our recommendation</div>
<h1>{HEAD}</h1>
<p class="lede">The sources name whey as a preferred case for it,<sup>1</sup> and it is the least effort. Because the stream can turn turbid,<sup>3</sup> keep mid-IR ATR as the fallback<sup>2</sup> and treat a fused NIR plus mid-IR ATR model as a later hypothesis. The protein range, required accuracy and the nature of the turbidity are still open.</p>
<div class="verdict"><div><span>Confidence</span><b>{CONF}</b> · {CONF_WHY}</div><div><span>Status</span>{STATUS}</div></div>
<p style="font-size:17px;margin-top:12px"><i style="color:var(--muted)">Next step.</i> {NEXT}</p>
<aside class="side" style="grid-row:3 / span 5"><ol>{side}
<li class="ext"><span class="cite">{EXT}</span> — external, not AFS material; quote and URL in the sources panel.</li></ol>
<p style="margin-top:14px">Further sources for this option: {", ".join(CHIPS[1:])}.</p></aside>

<h2 class="wide"><i>§2</i>How it would be set up</h2>
<figure class="wide" style="margin:0"><div class="plate">{SVG}</div>
<figcaption class="caption"><b>Fig. 1.</b> Setup sketch for option O2 (recommended). Callouts P1–P3 refer to Table 2, M1–M2 to §3 and Q3 to §5. Dashed: auxiliary sensor whose availability is to be confirmed with AFS. Drawn by code from the option: a schematic, not a configuration.</figcaption></figure>

<h2><i>§3</i>Options</h2>
<div class="tabs">{"".join(f'<span class="{"on" if t[0]=="Recommended" else ""}">{t[0]}<small>{t[1]}</small></span>' for t in TABS)}</div>
<dl><dt>Methods</dt><dd><b>M1</b> {M1[0]} ({M1[1]}). {M1[2]}<br><b>M2</b> {M2[0]} ({M2[1]}). {M2[2]}</dd>
<dt>Cost class</dt><dd>{COST}, S01 Table 1 (p.6)</dd><dt>Ease of use</dt><dd>{EASE}</dd><dt>Upkeep</dt><dd>{UPKEEP}</dd><dt>Why this option</dt><dd>{FIT}</dd><dt>Cost drivers</dt><dd>{DRIVERS}</dd></dl>

<h2 class="wide"><i>§4</i>What to measure and how</h2>
<table class="booktabs wide"><caption><b>Table 2.</b> Parameters for option O2. Source column: supplied AFS material, or marked as engineering judgement.</caption>
<thead><tr><th></th><th>Parameter</th><th>Need</th><th>Measured by</th><th>Why</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table>

<h2><i>§5</i>Open questions</h2><ol class="qs">{qs}</ol>
</div></div>'''


# ------------------------------------------------------------------ C
def dir_c(dark=False):
    if dark:
        return f'''<div class="C dark"><div class="in" style="padding:22px">
<div class="kicker">01 · Recommendation</div><h1>{HEAD}</h1><p>{SUM.split(". ")[0]}.</p>
<div style="font-size:14px"><span class="bar"><i class="f"></i><i class="f"></i><i></i></span><b>{CONF}</b> · {CONF_WHY}</div>
<div class="chips">{chips()}</div>
<div class="bpwrap mini" style="padding:10px">{SVG}</div></div></div>'''
    rows = "".join(
        f'<tr><td><span class="tag">{p[0]}</span> {p[1]}</td><td>{p[2]}</td><td>{p[3]}</td><td>{p[4]}</td>'
        f'<td>{f"<span class=chip>{p[5]}</span>" if p[5] else "<span class=eng>engineering judgement, no source</span>"}</td></tr>'
        for p in PARAMS)
    qs = "".join(f'<li><span class="tag">{q[0]}</span><div>{q[1]}<small>{q[2]}</small></div></li>' for q in QS)
    return f'''<div class="C">
<div class="top"><div class="brand">AFS Spectroscopy Assistant<small>In-line measurement advice, every claim sourced</small></div>
<div><span class="btn">Examples</span><span class="btn">Dark</span><span class="btn pri">New question</span></div></div>
<div class="page">
<div class="row"><div class="num q">?</div><div class="body"><div class="kicker m">Your question</div><p class="qtext">{ENQ}</p></div></div>
<div class="row flow"><div class="num">01</div><div class="body"><div class="kicker">Recommendation</div>
<h1>{HEAD}</h1><p class="sum">{SUM}</p>
<div class="strip"><div><div class="k">Status</div><div class="v">{STATUS}</div></div>
<div><div class="k">Confidence</div><div class="v"><span class="bar"><i class="f"></i><i class="f"></i><i></i></span>{CONF}</div><small style="color:var(--muted)">{CONF_WHY}</small></div>
<div><div class="k">Cost class</div><div class="v">{COST}</div></div>
<div><div class="k">Next step</div>{NEXT}</div></div>
<div class="chips">{chips()}</div></div></div>

<div class="row flow"><div class="num">02</div><div class="body"><div class="kicker">Setup drawing</div><h2>How it would be set up</h2>
<div class="bpwrap k">{SVG}</div>
<div class="key"><div><b>M1</b><b>M2</b> probes and methods<span class="to">continue in 03 Options ↓</span></div>
<div><b>P1</b><b>P2</b><b>P3</b> measured quantities<span class="to">continue in 04 What to measure ↓</span></div>
<div><b>Q3</b> measurement point not fixed<span class="to">continue in 05 Open questions ↓</span></div></div></div></div>

<div class="row flow"><div class="num">03</div><div class="body"><div class="kicker">Options</div>
<div class="opts">{"".join(f'<div class="opt{" on" if t[0]=="Recommended" else ""}"><b>{t[0]}</b>{t[1]}</div>' for t in TABS)}</div>
<div class="card"><div class="hd">Recommended · O2 <span>S01 Table 1 (p.6)</span></div>
<div class="cells"><div><div class="k">Cost class</div>{COST}</div><div><div class="k">Ease of use</div>{EASE}</div><div><div class="k">Upkeep</div>{UPKEEP}</div><div><div class="k">Why</div>{FIT}</div></div>
<div class="mm"><span class="tag">M1</span><div><b>{M1[0]}</b> · {M1[1]}. {M1[2]}</div></div>
<div class="mm"><span class="tag">M2</span><div><b>{M2[0]}</b> · {M2[1]}. {M2[2]}</div></div></div></div></div>

<div class="row flow"><div class="num">04</div><div class="body"><div class="kicker">What to measure</div>
<div class="card"><div class="hd">What to measure and how <span>3 parameters · expanded</span></div>
<table><thead><tr><th>Parameter</th><th>Need</th><th>Measured by</th><th>Why</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div></div></div>

<div class="row"><div class="num">05</div><div class="body"><div class="kicker">Open questions</div>
<div class="card"><ul class="ql">{qs}</ul></div></div></div>
</div></div>'''


SPEC = {
    "A": {
        "tag": ("A", "Technical report", "IBM Plex Serif headings · Plex Sans body · whiteprint drawing on gridded paper"),
        "fonts": [("Display / headings", "IBM Plex Serif 500, 600"), ("Body / UI", "IBM Plex Sans 400, 500, 600, italic 400"),
               ("IDs, citations", "IBM Plex Mono 400, 500"), ("Licence", "SIL OFL 1.1, all three; woff2 on Google Fonts and Fontsource; Sans and Mono are already self-hosted in the app")],
        "why": "The smallest change from today: it adds only Plex Serif, and the three Plex families share metrics and a technical tone. Layout: a sticky numbered index on the left, a recommendation card with a definition list, and a 64 px gap between sections. The drawing is a diazo-style “whiteprint” (blue ink on gridded paper), which stays readable in print and in light mode.",
        "cap": "Dark mode: paper becomes slate and the ink becomes light blue. The orange callout accent stays."},
    "B": {
        "tag": ("B", "Journal", "Newsreader for all reading text · Source Sans 3 only for UI chrome · cyanotype plate as Fig. 1"),
        "fonts": [("Display + body", "Newsreader 400, 500, 600, italic 400 (optical size axis 6–72)"), ("UI chrome only", "Source Sans 3 600 (tabs, labels, buttons)"),
               ("Licence", "SIL OFL 1.1, both; woff2 on Google Fonts and Fontsource (Newsreader as a variable font with an opsz axis)")],
        "why": "Reads like a paper. The citations move into a margin column with their verified quotes, Tufte-style, the parameter table is a booktabs table, and the drawing is a numbered figure with a caption. The cyanotype plate (white lines on Prussian blue) is the most recognisable “blueprint”. The cost is that serif body text at small sizes on low-DPI screens is softer, and the layout is the furthest from today’s.",
        "cap": "Dark mode: warm near-black paper. The plate stays cyanotype blue, so it looks the same in both modes."},
    "C": {
        "tag": ("C", "Engineering dossier", "Source Sans 3 body · Source Serif 4 display · white-line blueprint · numbered section rail"),
        "fonts": [("Display / headings", "Source Serif 4 600 (opsz 36–60)"), ("Body / UI", "Source Sans 3 400, 600, 700, italic 400"),
               ("IDs, citations", "Source Code Pro 500, 600"), ("Licence", "SIL OFL 1.1, all three (Adobe); woff2 in the Adobe repos, on Google Fonts and on Fontsource")],
        "why": "Adobe’s Source superfamily was designed as one system, and its sans has tabular lining figures by default. A numbered rail (01–05) runs from the recommendation through the drawing to the details. Under the drawing, a key strip sends each callout group (M, P, Q) to its section, so the drawing visibly “flows into” the page. This direction has the strongest hierarchy and the most modern feel.",
        "cap": "Dark mode: GitHub-like near-black. The blueprint deepens to midnight blue and the cyan callouts stay."},
}


def block(key, fn):
    s = SPEC[key]
    t = s["tag"]
    rows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in s["fonts"])
    return f'''<div class="dir-tag" id="tag-{key.lower()}"><b>{t[0]}</b><span>{t[1]}</span><em>{t[2]}</em></div>
<section class="dir" id="direction-{key.lower()}">{fn()}</section>
<div class="spec"><div><h3>Direction {t[0]}: fonts and rationale</h3><table>{rows}</table><p>{s["why"]}</p></div>
<div><h3>Dark-mode swatch</h3><div class="sw">{fn(dark=True)}</div><p class="swatch-cap">{s["cap"]}</p></div></div>'''


html = (HERE / "template.html").read_text()
html = html.replace("<!--DIR_A-->", block("A", dir_a)).replace("<!--DIR_B-->", block("B", dir_b)).replace("<!--DIR_C-->", block("C", dir_c))
OUT.write_text(html)
print("wrote", OUT, len(html))
