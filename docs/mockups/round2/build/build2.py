"""Build docs/mockups/round2/index.html: hybrid variants H1-H3 of round-1 directions A and C.
All content strings are copied from outputs/dev/D03.json (option O2). Run: uv run python docs/mockups/round2/build/build2.py
"""
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from bp2 import narrow, wide

OUT = HERE.parent / "index.html"

ENQ = ("Our dairy process includes a relatively clear whey stream before a concentration stage. We want to investigate "
       "whether spectroscopy can track protein concentration as the stream changes, with laboratory results used as the "
       "reference. The stream can become more turbid under some operating conditions. We need a first measurement concept "
       "that handles this change rather than assuming the liquid always remains clear.")
HEAD = "Start with NIR transmission/<wbr>transflection."
SUM = ("The sources name whey as a preferred case for it, and it is the least effort. Because the stream can turn turbid, "
       "keep mid-IR ATR as the fallback and treat a fused NIR plus mid-IR ATR model as a later hypothesis. The protein "
       "range, required accuracy and the nature of the turbidity are still open.")
NEXT = "Answer Q1 to Q3 and run the sample series with NIR transmission first, then mid-IR ATR on the same samples."
CHANGE = ("If the required accuracy or the turbidity range shows that NIR transmission cannot cover the stream, the choice "
          "moves to M2 alone or to the fused M3.")
CITES = [("S01 p.18", "NIR Transmission is the preferred method for transparent or semi-transparent liquids, such as skim milk, whey, or permeate."),
         ("S01 p.5", "making it ideal for online applications, including remote measurements via fiber optic probes."),
         ("S01 p.13", "typically at a depth of few microns"),
         ("S04 p.4", "suitability of analyzed samples for ATR measurements, which is true for liquid or soft solid samples and their components, allowing a tight contact with the probe head."), ("S01 p.9", "Vibrational spectroscopy in the mid-IR range (4000-400 cm-1) is one of the most informative methods of chemical analysis.")]
EXT = "E02 ¶12"
EASE, UPKEEP = "two probes, one method at a time", "two probes, two calibrations to keep"
FIT, DRIVERS = "covers clear and turbid operating states", "NIR and MIR spectrometers, MIR fibers, ATR probe"
M = [("M1", "NIR, transmission/transflection probe", "primary",
      "Applies while the stream stays clear enough for transmission with a controlled optical pathlength."),
     ("M2", "MIR, ATR probe", "conditional", "Applies only if the turbid operating state defeats NIR transmission.")]
PARAMS = [
    ("P1", "protein concentration", "required", "Spectroscopy: NIR", "It is the stated target of the investigation.", "S01 p.17"),
    ("P2", "turbidity (optical density) of the stream", "required",
     "Auxiliary sensor: inline turbidity or optical-density sensor (cited; confirm availability with AFS)",
     "The stream can become more turbid, and physical variation can mimic a composition change, so the state must be recorded with each spectrum.",
     "S01 p.7"),
    ("P3", "process temperature at the measurement point", "optional",
     "Auxiliary sensor: temperature sensor (engineering judgement: confirm availability with AFS)",
     "Temperature shifts the water and protein bands and the physical state of the stream; a temperature signal should already be available at a dairy process point.",
     None)]
QS = [("Q1", "What protein concentration range must be covered, and what accuracy and response time are required?",
       "These decide whether one method can cover the target and they set the go/no-go criteria for the test."),
      ("Q2", "How turbid does the stream become, and what causes the turbidity (particles, fat or dissolved species)?",
       "The severity and nature decide whether NIR transmission still works or whether ATR is needed."),
      ("Q3", "Where is the measurement point, is it in-line in the pipe, in a bypass or at-line, and how far is the analyzer from it?",
       "This fixes the probe type and the fiber link, which differ between NIR and mid-IR.")]
TABS = [("Simple", "NIR · least effort"), ("Recommended", "NIR + MIR · best fit"), ("Extended", "NIR + MIR · several methods")]
SECTIONS = [("1", "Answer"), ("2", "Setup drawing"), ("3", "Options"), ("4", "What to measure"), ("5", "Open questions")]


# ------------------------------------------------------------------ shared pieces
def cite(label, quote="", cls=""):
    q = f' data-q="“{quote}”"' if quote else ""
    return f'<button type="button" class="cite {cls}"{q} aria-label="Source {label}, open the quoted passage">{label}</button>'


def cites(demo=""):
    out = "".join(cite(c, q, demo if i == 0 else "") for i, (c, q) in enumerate(CITES))
    return out + f'<button type="button" class="cite ext" aria-label="External source {EXT}, not AFS material">{EXT}<span> external</span></button>'


def meter():
    return '<span class="meter" aria-hidden="true"><i class="on"></i><i class="on"></i><i></i></span>'


def strip(n=4):
    cells = [("Confidence", f"{meter()}Medium", "open questions Q1, Q2"),
             ("Cost class", "High", f"rows 2, 7 · {cite('S01 Table 1 (p.6)')}"),
             ("Status", "Provisional", "feasibility assessment")]
    if n == 4:
        cells.append(("Next step", "Answer Q1–Q3", "then run the sample series"))
    return '<dl class="strip">' + "".join(f'<div><dt>{k}</dt><dd><b>{v}</b><span>{s}</span></dd></div>' for k, v, s in cells) + "</dl>"


def deflist(rows):
    return '<dl class="dl">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows) + "</dl>"


def figure(style, cls, linked="P2"):
    key = ('<ul class="key" aria-label="Callout key">'
           '<li><a href="#"><span class="ids"><i>M1</i><i>M2</i></span><span class="kt">Probes and methods</span><span class="to">→ 3 Options</span></a></li>'
           '<li><a href="#"><span class="ids"><i>P1</i><i class="lk">P2</i><i>P3</i></span><span class="kt">Measured quantities</span><span class="to">→ 4 What to measure</span></a></li>'
           '<li><a href="#"><span class="ids"><i>Q3</i></span><span class="kt">Measurement point not fixed</span><span class="to">→ 5 Open questions</span></a></li></ul>')
    return (f'<figure class="fig {cls}"><div class="figwrap"><div class="fig-wide">{wide(style, linked)}</div>'
            f'<div class="fig-narrow">{narrow(style, linked)}</div></div>{key}</figure>'
            '<p class="figcap">Drawn by code from the option: a schematic, not a configuration. Dashed: auxiliary sensor, availability to be confirmed with AFS.</p>')


def tabs():
    return ('<div class="seg" role="tablist" aria-label="Solution options">' + "".join(
        f'<button type="button" role="tab" aria-selected="{"true" if t == "Recommended" else "false"}"><span class="seg-t">{t}</span><span class="seg-s">{s}</span></button>'
        for t, s in TABS) + "</div>")


def option_panel():
    specs = (f'<dl class="specs"><div><dt>Cost class</dt><dd>high cost (rows 2, 7) {cite("S01 Table 1 (p.6)")}</dd></div>'
             f'<div><dt>Ease of use</dt><dd>{EASE}</dd></div><div><dt>Upkeep</dt><dd>{UPKEEP}</dd></div>'
             f'<div><dt>Confidence</dt><dd>{meter()}Medium<span class="sub">open questions Q1, Q2</span></dd></div></dl>')
    meth = "".join(f'<li><span class="id">{i}</span><div><b>{n}</b> · {r}. {c}</div></li>' for i, n, r, c in M)
    return (f'<div role="tabpanel" class="optp"><p class="opt-title"><b>Recommended</b> <span class="best">proposed</span> NIR + MIR, two probes</p>{specs}'
            f'<ul class="meth">{meth}</ul><p class="why"><span class="muted">Why this option:</span> {FIT}. '
            f'<span class="muted">Cost drivers:</span> {DRIVERS}.</p></div>')


def ptable():
    rows = "".join(
        f'<tr class="{"hl" if p[0] == "P2" else ""}"><td data-l="Parameter"><span class="id">{p[0]}</span> {p[1]}</td><td data-l="Need">{p[2]}</td>'
        f'<td data-l="Measured by">{p[3]}</td><td data-l="Why">{p[4]}</td>'
        f'<td data-l="Source">{cite(p[5]) if p[5] else "<em class=eng>engineering judgement, no source</em>"}</td></tr>' for p in PARAMS)
    return (f'<table class="ptable"><thead><tr><th>Parameter</th><th>Need</th><th>Measured by</th><th>Why</th><th>Source</th></tr></thead>'
            f'<tbody>{rows}</tbody></table><p class="hlnote">Hover state shown: P2 is lit on the drawing and here at the same time.</p>')


def questions():
    return '<ol class="qs">' + "".join(f'<li><span class="id">{q}</span><div>{t}<span class="sub">Why it matters: {w}</span></div></li>' for q, t, w in QS) + "</ol>"


def topbar():
    return ('<header class="top"><div class="brand">AFS Spectroscopy Assistant<span>In-line measurement advice, every claim sourced</span></div>'
            '<div class="acts"><button type="button" class="btn">Examples</button><button type="button" class="btn">Dark</button>'
            '<button type="button" class="btn pri">New question</button></div></header>')


def composer():
    return ('<div class="composer"><input type="text" aria-label="Ask a follow-up" placeholder="Add a detail or ask a follow-up, e.g. the line runs at 60 °C">'
            '<button type="button" class="btn pri">Send</button></div>')


def node(n, cls="node"):
    return f'<span class="{cls}" aria-hidden="true">{n}</span>'


# ------------------------------------------------------------------ H1: sticky index = rail
def h1(dark=False):
    if dark:
        return f'''<div class="v h1 dark"><div class="pad"><h2 class="sh">{node(1)}Our recommendation</h2>
<h1 class="headline">{HEAD}</h1>{strip(3)}<div class="cites">{cites()}</div>{figure("id", "wp")}</div></div>'''
    idx = "".join(f'<li><a href="#" class="{"on" if n == "1" else ""}" {"aria-current=true" if n == "1" else ""}>{node(n)}<span>{t}</span></a></li>' for n, t in SECTIONS)
    return f'''<div class="v h1">{topbar()}
<div class="grid"><nav class="idx" aria-label="On this page"><p class="idx-h">On this page</p><ol>{idx}</ol>
<p class="idx-h">Status</p><p class="idx-s">Provisional feasibility assessment</p></nav>
<main>
<section class="q"><p class="lab">Your question</p><p>{ENQ}</p></section>
<section class="rec"><h2 class="sh">{node(1)}Our recommendation</h2>
<h1 class="headline">{HEAD}</h1><p class="sum">{SUM}</p>{strip(3)}
{deflist([("Next step", NEXT), ("What would change it", CHANGE), ("Based on", f'<div class="cites">{cites("focus")}</div>')])}</section>
<section class="wide-sec"><h2 class="sh">{node(2)}How it would be set up</h2>{figure("id", "wp")}</section>
<section><h2 class="sh">{node(3)}Options</h2>{tabs()}{option_panel()}</section>
<section><h2 class="sh">{node(4)}What to measure</h2><details open><summary>What to measure and how <span>3 parameters</span></summary>{ptable()}</details></section>
<section><h2 class="sh">{node(5)}Open questions</h2>{questions()}</section>
</main></div>{composer()}</div>'''


# ------------------------------------------------------------------ H2: in-flow rail, def-list card, navy blueprint
def h2(dark=False):
    if dark:
        return f'''<div class="v h2 dark"><div class="pad"><p class="kick">1 · Our recommendation</p><h1 class="headline">{HEAD}</h1>
{deflist([("Confidence", f"{meter()}<b>Medium</b> · open questions Q1, Q2"), ("Status", "Provisional feasibility assessment")])}
<div class="cites">{cites()}</div>{figure("id", "navy")}</div></div>'''

    def row(n, kick, body, flow=True, last=False):
        return f'<div class="row{" flow" if flow else ""}{" last" if last else ""}">{node(n)}<div class="rb"><p class="kick">{kick}</p>{body}</div></div>'
    rec = (f'<h1 class="headline">{HEAD}</h1><p class="sum">{SUM}</p>'
           + deflist([("Confidence", f"{meter()}<b>Medium</b> · open questions Q1, Q2"),
                      ("Cost class", f"high cost (rows 2, 7) {cite('S01 Table 1 (p.6)')}"),
                      ("Status", "Provisional feasibility assessment"),
                      ("Next step", NEXT), ("What would change it", CHANGE),
                      ("Based on", f'<div class="cites">{cites("focus")}</div>')]))
    return f'''<div class="v h2">{topbar()}<main class="wrap">
<section class="q"><p class="lab">Your question</p><p>{ENQ}</p></section>
{row(1, "Our recommendation", rec)}
{row(2, "Setup drawing", '<h2 class="h">How it would be set up</h2>' + figure("id", "navy"))}
{row(3, "Options", '<h2 class="h">Three ways to start</h2>' + tabs() + option_panel())}
{row(4, "What to measure", '<details open><summary>What to measure and how <span>3 parameters</span></summary>' + ptable() + '</details>')}
{row(5, "Open questions", '<h2 class="h">What we still need to know</h2>' + questions(), flow=False, last=True)}
</main>{composer()}</div>'''


# ------------------------------------------------------------------ H3: section bar + hanging numerals, adaptive blueprint, pill callouts
def h3(dark=False):
    if dark:
        return f'''<div class="v h3 dark"><div class="pad"><h1 class="headline">{HEAD}</h1>{strip(3)}
<div class="cites">{cites()}</div>{figure("pill", "adapt")}</div></div>'''
    bar = "".join(f'<a href="#" class="{"on" if n == "1" else ""}"><b>{n}</b>{t}</a>' for n, t in SECTIONS)

    def sec(n, title, body, cls=""):
        return f'<section class="s {cls}"><div class="num" aria-hidden="true">{n}</div><div class="sb"><h2 class="h"><span class="sr">{n} </span>{title}</h2>{body}</div></section>'
    rec = (f'<h1 class="headline">{HEAD}</h1><p class="sum">{SUM}</p>{strip(3)}'
           + deflist([("Next step", NEXT), ("What would change it", CHANGE), ("Based on", f'<div class="cites">{cites("pop")}</div>')]))
    return f'''<div class="v h3">{topbar()}<nav class="bar" aria-label="Sections">{bar}</nav><main class="wrap">
<section class="q"><p class="lab">Your question</p><p>{ENQ}</p></section>
{sec(1, "Our recommendation", rec, "rec")}
{sec(2, "How it would be set up", figure("pill", "adapt"), "wide-sec")}
{sec(3, "Options", tabs() + option_panel())}
{sec(4, "What to measure", '<details open><summary>What to measure and how <span>3 parameters</span></summary>' + ptable() + '</details>')}
{sec(5, "Open questions", questions())}
</main>{composer()}</div>'''


CSS = (HERE / "style2.css").read_text()

SPEC = {
    "h1": ("H1", "Index rail", "A’s sticky index becomes C’s rail: index numbers = section numbers. C’s facts strip, A’s whiteprint drawing, callout key strip.",
           [("Headings", "IBM Plex Serif 600 (headline 40 px, section titles 26 px)"), ("Body, UI", "IBM Plex Sans 400/500/600 (already self-hosted)"),
            ("IDs, numbers, citations", "IBM Plex Mono 500 (already self-hosted)"), ("Licence", "SIL OFL 1.1; adds one family (Plex Serif, 2 woff2 files)")],
           "Where to look is fixed on the left at all times, and the rail nodes repeat as section badges, so the index and the page share one numbering. The drawing breaks out to 1000 px so its labels render at 12 px or more. On phones the index becomes a sticky horizontal bar."),
    "h2": ("H2", "Rail dossier", "C’s in-flow rail and navy white-line blueprint, A’s recommendation as a plain definition list, the app’s segmented tabs.",
           [("Headings", "IBM Plex Serif 500 (headline 44 px, section titles 26 px)"), ("Body, UI", "IBM Plex Sans 400/500/600"),
            ("IDs, numbers, citations", "IBM Plex Mono 500"), ("Licence", "SIL OFL 1.1; adds Plex Serif only")],
           "The strongest top-to-bottom flow: the rail runs from the answer through the drawing into the details. The definition list keeps every fact in one scannable column with no boxed strip. The navy panel looks the same in light and dark mode."),
    "h3": ("H3", "Margin numerals, adaptive blueprint", "A’s calm paper look with C’s hierarchy: a sticky section bar, large hanging numerals, a blueprint that is a whiteprint in light mode and a cyanotype in dark mode, and pill callouts that carry the section number.",
           [("Headline only", "IBM Plex Serif 600 (one use per page)"), ("Body, UI, section titles", "IBM Plex Sans 400/500/600"),
            ("Numerals, IDs, citations", "IBM Plex Mono 500"), ("Licence", "SIL OFL 1.1; adds Plex Serif only")],
           "The closest to today’s app. Serif is used for the one answer headline only, and the hierarchy comes from the numerals and white space. The section bar works at every width and next to the 400 px citation panel. Each callout says where to go next (“4 P2”) without needing a key, and the key strip is still there."),
}


def block(k, fn):
    tag, name, line, fonts, why = SPEC[k]
    rows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in fonts)
    return f'''<div class="dir-tag"><b>{tag}</b><span>{name}</span><em>{line}</em></div>
<section class="dir" id="{k}">{fn()}</section>
<div class="spec"><div><h3>{tag}: fonts and rationale</h3><table>{rows}</table><p>{why}</p>
<h3 style="margin-top:28px">Dark-mode swatch</h3><div class="sw">{fn(dark=True)}</div></div>
<div><h3>390 px phone column</h3><div class="phone" id="{k}-m">{fn()}</div></div></div>'''


PAGE = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Hybrid Answer Mockups</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Serif:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<header class="doc-head"><h1>Round 2: hybrids of A (Technical report) and C (Engineering dossier)</h1>
<p>Three ways to combine A and C. Each fixes the problems found in the round-1 UX audit (<code>ux-audit.md</code>). All variants use the app’s colour tokens and its self-hosted IBM Plex Sans and Mono, and add IBM Plex Serif for display text only. Content is copied from <code>outputs/dev/D03.json</code> (option O2). The drawings are hand-written SVG for the mockup. In the app they stay code-drawn, with a wide and a narrow version, as <code>diagrams.py</code> does today.</p>
<p><b>What is shown:</b> the desktop slice at 1440 px, then for each variant its fonts, a dark-mode swatch and the real 390 px phone column (the same markup, collapsed by container queries). P2 is shown in its hover state on the drawing and in the table. In H1 the first citation chip shows a keyboard focus ring, and in H3 it shows the quote preview.</p></header>
{block("h1", h1)}
{block("h2", h2)}
{block("h3", h3)}
<footer class="doc-foot"><b>Sources for the audit:</b> NN/g 10 usability heuristics (nngroup.com/articles/ten-usability-heuristics/); NN/g visual hierarchy (nngroup.com/articles/visual-hierarchy-ux-definition/); NN/g F-shaped pattern (nngroup.com/articles/f-shaped-pattern-reading-web-content/); NN/g information scent (nngroup.com/articles/information-scent/); NN/g Gestalt proximity and common region (nngroup.com/articles/gestalt-proximity/, nngroup.com/articles/common-region/); WCAG 2.2 (w3.org/TR/WCAG22/). Font and blueprint sources are as in round 1 (../README.md).</footer>
</body></html>'''

OUT.write_text(PAGE)
print("wrote", OUT, len(PAGE))
