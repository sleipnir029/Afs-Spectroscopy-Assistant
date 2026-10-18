# UX audit: round-1 directions A, B, C and round-2 hybrids H1–H3

_Written 2026-10-18 09:37 CEST by the mockup agent (Claude). Method: a heuristic expert review of the static mockups, plus measurements in Chromium (Playwright) and computed WCAG contrast ratios. This is **not** user testing. The same agent built and audited the variants, so this is not an independent review: run a separate reviewer pass before anything is implemented._

## Heuristics and standards used

- NN/g, 10 usability heuristics (consistency and standards, recognition rather than recall, aesthetic and minimalist design): https://www.nngroup.com/articles/ten-usability-heuristics/
- NN/g, visual hierarchy (size, colour, contrast, alignment, proximity): https://www.nngroup.com/articles/visual-hierarchy-ux-definition/
- NN/g, F-shaped scanning (people scan the left edge and the first words of lines): https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/
- NN/g, information scent (labels must predict what is behind them): https://www.nngroup.com/articles/information-scent/
- NN/g, Gestalt proximity and common region: https://www.nngroup.com/articles/gestalt-proximity/ and https://www.nngroup.com/articles/common-region/
- WCAG 2.2 AA: 1.4.3 text contrast 4.5:1, 1.4.11 non-text contrast 3:1, 1.4.10 reflow at 320 CSS px, 2.4.7 focus visible, 2.4.11 focus not obscured, 2.5.8 target size at least 24×24 CSS px: https://www.w3.org/TR/WCAG22/
- NN/g severity scale: 1 cosmetic, 2 minor, 3 major, 4 catastrophic.
- The baseline is the existing app (`src/afs_assistant/ui/static/app.css`):
  - IBM Plex Sans and Mono, self-hosted; one deep-blue accent; "no cards, no shadows, hairlines and type carry the structure".
  - Targets of 44–52 px; a `:focus-visible` ring.
  - Container queries keep SVG text at 12 px or more, with a wide and a narrow drawing.
  - A 400 px citation panel that pushes the column aside at 1180 px or wider; a pinned composer.

Scores run from 1 (poor) to 5 (good).

---

## Part 1: round 1 (A Technical report, B Journal, C Engineering dossier)

### Scores

| Criterion | A | B | C |
|---|---|---|---|
| Hierarchy, where to look | 4 | 3 | 5 |
| Scannability (F-pattern) | 4 | 2 | 5 |
| Information scent of numbered sections | 4 | 3 | 4 |
| Citation affordance | 2 | 4 | 3 |
| Drawing-to-section linkage | 3 | 3 | 4 |
| Density and white space | 4 | 3 | 3 |
| Contrast (measured) | 3 | 3 | 4 |
| Phone at 390 px | 1 | 1 | 2 |
| Keyboard and focus | 1 | 1 | 1 |
| Consistency with the existing app | 4 | 1 | 2 |
| **Total (of 50)** | **30** | **24** | **33** |

### Measured problems that affect all three

- **Drawing text is far too small (severity 3; 4 on phones).** The wide SVG (viewBox 1000) renders at about 740 px in A, 890 px in B and 910 px in C. Its 11 px labels therefore render at about 8.1 px, 9.8 px and 10 px, and the title block at 6.3–7.7 px. The app already enforces at least 12 px with container queries; the round-1 mockups dropped that. At 390 px there was no narrow drawing at all: the wide one would scale to about 0.33, so 11 px becomes about 3.6 px, which is unreadable.
- **No phone layout (severity 4, WCAG 1.4.10).** A uses a fixed `240px + 780px` grid, B uses a `660px + 280px` text-plus-margin grid, and C uses a fixed 4-column strip and a 3-column key. Round 1 only wrapped each direction in `overflow-x:auto`, so the pages scroll sideways at 390 px.
- **Controls are not controls (severity 3, 2.4.7, 4.1.2).** Option tabs are `<div>`s and citation chips are `<span>`s, with no focus style. The app uses `role="tab"` buttons and a 2 px focus ring, and round 1 regressed from that.
- **Faded text in the drawing (severity 2, 1.4.3).** The "PC · CHEMOMETRICS" label at 55 % opacity measures 3.08:1 in A and 4.09:1 in B. Both fail 4.5:1. C passes (4.66:1).

### Contrast, round 1 (computed; script: `build/contrast.py r1`)

| Pair | Ratio | Needs | Result |
|---|---|---|---|
| A body ink / paper `#1b1f24`/`#f7f5f0` | 15.20 | 4.5 | PASS |
| A muted / paper `#5b6470`/`#f7f5f0` | 5.50 | 4.5 | PASS |
| A chip `#0f4c81`/`#e3ecf5` | 7.42 | 4.5 | PASS |
| A drawing ink / whiteprint `#123d6b`/`#fbfaf6` | 10.55 | 4.5 | PASS |
| A drawing label at 55 % opacity | 3.08 | 4.5 | **FAIL** |
| A orange callout / whiteprint `#b4471f`/`#fbfaf6` | 5.21 | 4.5 | PASS |
| A card border / paper (non-text) | 1.31 | 3.0 | FAIL, but decorative (the content is identifiable without it) |
| A dark muted / bg `#9aa3ad`/`#15181c` | 6.97 | 4.5 | PASS |
| A dark drawing ink / panel `#a9c9ec`/`#111821` | 10.42 | 4.5 | PASS |
| B muted / paper `#6a645a`/`#fdfbf6` | 5.67 | 4.5 | PASS |
| B cyanotype ink `#f2f5fa`/`#1d3f72` | 9.58 | 4.5 | PASS |
| B gold callout `#ffd27a`/`#1d3f72` | 7.35 | 4.5 | PASS |
| B drawing label at 55 % opacity | 4.09 | 4.5 | **FAIL** |
| C muted / bg `#56606d`/`#f2f4f7` | 5.79 | 4.5 | PASS |
| C chip `#1b4f9c`/`#ffffff` | 7.94 | 4.5 | PASS |
| C drawing ink / navy `#e8f0fb`/`#0f2d57` | 11.93 | 4.5 | PASS |
| C cyan callout `#7fd3ff`/`#0f2d57` | 8.26 | 4.5 | PASS |
| C key secondary `#9fb4d3`/`#0b2346` | 7.40 | 4.5 | PASS |
| C grey rail segment / bg (non-text) | 1.26 | 3.0 | FAIL (it marks the unnumbered "?" row; the meaning is carried by the numbered nodes) |
| C dark muted / surface `#9aa6b2`/`#151b23` | 6.98 | 4.5 | PASS |
| C dark drawing ink `#e8f0fb`/`#0a1a33` | 15.13 | 4.5 | PASS |

### How each would collapse at 390 px (sketch)

```
A (as built: sideways scroll)       B (as built: sideways scroll)      C (as built: sideways scroll)
needs: index -> top chip bar         needs: margin notes -> footnotes   needs: rail 96 -> 36 px
       card full width                      plate -> narrow drawing            strip 4 col -> 2x2
       defs -> stacked                      booktabs -> stacked rows           cards stack, key 3 -> 1 col
       drawing -> narrow version            superscripts -> chips              drawing -> narrow version
```

### A: Technical report

**Strengths**
- The calmest page and the closest to the app: Plex, hairlines and the same confidence meter.
- The sticky numbered index answers "where am I". The recommendation card is a clear common region.
- The definition list (Confidence, Sources, Next step, What would change it) scans well down the left edge (F-pattern).
- The whiteprint drawing prints well and suits light mode.

**Problems**
- (3) Drawing text renders at 6–9 px (see above).
- (3) No phone layout; the sticky index has no collapsed form.
- (2) Citations are one row of chips, detached from the claims they support, with no preview.
- (2) The index (240 px) plus gap (56 px) plus column (780 px) is 1076 px. With the app's 400 px citation panel open at 1440 px, only about 1016 px is left, so the layout breaks.
- (2) Callouts link to sections only through a caption legend ("P = §4"), which relies on recall rather than recognition.
- (1) The orange callout accent adds a second accent colour the app doesn't use.

### B: Journal

**Strengths**
- The verified quote sits next to the text in the margin: the best trust signal of the three.
- The booktabs table and the "Fig. 1" caption are academic and coherent.

**Problems**
- (3) Serif body text at 19 px across a 660 px measure, with italic labels: the slowest to scan (weak left-edge anchors).
- (3) Superscript citation targets are about 7×11 px. They pass 2.5.8 only through its spacing exception, and the affordance is poor.
- (3) No persistent index: the § numbers only show once you reach them.
- (4) The margin-note layout has no phone form.
- (3) It is the furthest from the app: new type, new chrome and a new table style.

### C: Engineering dossier

**Strengths**
- The strongest hierarchy: a big headline, then the key-facts strip, then chips.
- The numbered rail gives continuity, and the key strip under the drawing is the only real "flows into" device in round 1.
- Pill chips are about 26 px tall.

**Problems**
- (2) The 4-column strip is cramped: "Provisional feasibility assessment" wraps to 3 lines and "Next step" holds a full sentence.
- (2) Cards, a selection ring with a soft shadow, and pill shapes break the app's "no cards, no shadows" rule and its square tags.
- (2) The "?" node for the question has no meaning and breaks the 01–05 numbering.
- (2) Section labels are 12 px uppercase kickers; the number is louder than the name, which weakens information scent.
- (3) No narrow drawing.
- (1) Source Serif 4, Sans 3 and Code Pro mean three new families to self-host, versus zero for Plex.

### What the hybrid must keep and avoid

**Keep**
- C's rail and numbering, and C's key strip under the drawing.
- C's facts strip, with short values only (Confidence, Cost class, Status), leaving sentences to a definition list.
- A's definition list for Next step and What would change it.
- A's whiteprint look in light mode, and A's index ("where am I").
- The app's Plex Sans/Mono, tokens, segmented tabs, 44 px controls and focus ring.
- The quote preview idea from B, moved onto the chips (hover or focus) instead of the margin.

**Avoid**
- SVG text under 12 px; a wide drawing without a narrow twin; opacity-faded text.
- `<div>` or `<span>` controls.
- Boxed cards and shadows; the "?" node.
- A layout wider than the column the citation panel leaves free.
- A second accent colour. Use the app's `--color-mark` for the linked or hover state.

---

## Part 2: round 2 (hybrids H1, H2, H3)

**Fixes in all three:**
- The app's tokens and Plex Sans/Mono; Plex Serif for display only. Plex Serif shares the family's proportions, adds a single woff2 family, and needs no new vendor, so the audit gave no reason to choose Source Serif 4.
- Real `<button>`s with `role="tab"`; 44–52 px controls; citation chips 28 px tall, with a focus ring and a quote preview on hover or focus.
- `scroll-margin-top` so the sticky bars don't cover focused or anchored sections (2.4.11).
- A wide drawing with a narrow twin, switched by container queries. Measured minimum rendered SVG text is 12.2–12.5 px on desktop and 12.2–12.3 px at 390 px. No opacity on text.
- The P2 linked state uses the app's mark colour on both the drawing and the table row.
- A key strip under every drawing, linking each callout group to its section.
- No horizontal page scroll at 390 px. The only sideways scrolling is inside the sticky section bars of H1 and H3, by design.

### Contrast, round 2 (computed; script: `build/contrast.py r2`). All pairs pass.

| Pair | Ratio | Needs |
|---|---|---|
| Body ink / paper, light `#171b21`/`#f7f6f3` | 15.99 | 4.5 |
| Muted / paper, light `#51555c`/`#f7f6f3` | 6.93 | 4.5 |
| Chip / chip wash, light `#104a97`/`#e4eefc` | 7.32 | 4.5 |
| Selected tab, light `#fcfbf9`/`#104a97` | 8.29 | 4.5 |
| Index rail line, light (non-text) `#83868c` | 3.38 | 3.0 |
| Focus ring, light `#145ec1` | 5.71 | 3.0 |
| Whiteprint ink / paper `#123d6b`/`#fcfbf9` | 10.66 | 4.5 |
| Whiteprint ink over a major grid line | 8.60 | 4.5 |
| Whiteprint callout `#fff`/`#104a97` | 8.58 | 4.5 |
| Linked callout `#171b21`/`#ecdeaa` | 12.83 | 4.5 |
| Whiteprint key link `#104a97`/`#f1efe8` | 7.45 | 4.5 |
| Navy ink / panel `#e8f0fb`/`#0f2d57` | 11.93 | 4.5 |
| Navy callout `#0f2d57`/`#7fd3ff` | 8.26 | 4.5 |
| Navy key link `#9fd8ff`/`#0b2346` | 10.23 | 4.5 |
| Dark: ink / paper `#e9e8e3`/`#131518` | 14.91 | 4.5 |
| Dark: muted / paper `#a7abb1`/`#131518` | 7.93 | 4.5 |
| Dark: chip `#7facf0`/`#1c2738` | 6.49 | 4.5 |
| Dark: rail line (non-text) `#71757a` | 3.94 | 3.0 |
| Dark: focus ring `#7cb2ff` | 8.42 | 3.0 |
| H1 dark whiteprint ink `#b8d0ee`/`#121a24` | 11.09 | 4.5 |
| H3 dark cyanotype ink `#f2f5fa`/`#1d3f72` | 9.58 | 4.5 |
| H3 dark cyanotype key link `#ffd27a`/`#16335e` | 8.84 | 4.5 |

### Comparison

| Criterion | A | C | H1 Index rail | H2 Rail dossier | H3 Margin numerals |
|---|---|---|---|---|---|
| Hierarchy, where to look | 4 | 5 | 5 | 4 | 5 |
| Scannability | 4 | 5 | 5 | 4 | 5 |
| Information scent of numbered sections | 4 | 4 | 5 | 4 | 5 |
| Citation affordance | 2 | 3 | 4 | 4 | 5 |
| Drawing-to-section linkage | 3 | 4 | 4 | 5 | 5 |
| Density and white space | 4 | 3 | 4 | 3 | 4 |
| Contrast (measured) | 3 | 4 | 5 | 5 | 5 |
| Phone at 390 px | 1 | 2 | 4 | 4 | 4 |
| Keyboard and focus | 1 | 1 | 4 | 4 | 4 |
| Consistency with the existing app | 4 | 2 | 4 | 3 | 5 |
| **Total (of 50)** | 30 | 33 | **44** | **40** | **47** |

### H1: Index rail
A's sticky index is now C's rail: index node numbers are the section badge numbers. It adds C's 3-cell facts strip, A's whiteprint drawing and the key strip.

**Strengths**
- "Where am I" is always visible, and the index and the sections share one numbering (recognition, not recall).
- The drawing breaks out to 1000 px, so its labels render at 12.5 px.

**Problems**
- (2) Index 200 px + gap 48 px + column 760 px is about 1088 px with padding, more than the 1016 px left when the citation panel is open. The index must switch to its top-bar form when the panel opens (the collapsed form already exists for phones).
- (2) On phones the horizontal index hides sections 4–5 off-screen and needs a scroll cue (fade edge).
- (1) Serif section titles plus rail nodes plus a serif headline make three display devices; a little busy.

### H2: Rail dossier
C's in-flow rail and navy white-line blueprint, A's recommendation as one definition list, and the app's segmented tabs.

**Strengths**
- The most continuous top-to-bottom flow: the rail runs from the answer through the drawing, and the key strip sits inside the navy panel.
- The navy panel looks the same in both themes.

**Problems**
- (2) Confidence, cost class and status become ordinary definition rows, so the answer's key facts are less glanceable than in a strip.
- (2) No persistent index: the numbers are seen only when scrolled to.
- (2) The navy panel is the heaviest object on a hairline page and pulls the eye from the answer (visual hierarchy).
- (2) On phones the rail costs 52 px. The drawing breaks out of the rail to stay readable, which slightly breaks the rail metaphor. It is also the longest phone page (5444 px).

### H3: Margin numerals, adaptive blueprint
A's paper look with C's hierarchy:
- a sticky section bar at every width;
- large hanging Plex Mono numerals with a hairline rail;
- serif only on the one answer headline;
- a whiteprint drawing in light mode that becomes a cyanotype in dark mode;
- pill callouts that carry the section number ("4 P2"), plus the key strip.

**Strengths**
- The closest to the app (same paper, tokens, Plex Sans section titles).
- The section bar works at every width and next to the citation panel, because it is horizontal and needs no column.
- The callouts say where to go without needing a key.
- The quote preview on the chips brings B's trust strength without B's margin layout.

**Problems**
- (2) On phones the section bar hides items 4–5 off-screen, so it needs a scroll cue (as in H1).
- (1) On phones the numeral sits above the recommendation's top rule and looks slightly detached.
- (1) The quote preview covers the content below it while open; this is fine for hover or focus but must close on Escape.
- (2) Pill callouts need new code in `diagrams.py` (callout = section number + ID). The narrow two-branch drawing is laid out by hand here and must be generalised for options with one or three methods.

### Recommendation
**H3**, with one item from H1: show H1's vertical index at 1280 px or wider while the citation panel is closed, and fall back to H3's horizontal section bar otherwise.

Why H3:
- It scores highest (47/50). It is the most consistent with the existing app, so it is the cheapest and safest to implement before the deadline.
- It answers 5.10 with hanging numerals, white space and one serif headline, and 5.11 with an academic serif accent and a blueprint whose callouts carry section numbers into the page.

H2 is the right pick only if the user wants the blueprint to dominate the page.

### Still unverified
- No real keyboard or screen-reader pass on implemented code. Arrow-key navigation between tabs, Escape to close the quote preview, and focus moving into the citation panel all need JavaScript and testing.
- Contrast was computed from token pairs, not from pixels. Antialiased 12 px text on the grid background was checked only against the major grid-line colour.
- The scores are one reviewer's judgement. An independent reviewer pass is still needed.
