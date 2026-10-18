# Answer-page mockups: tasks 5.10 (layout) and 5.11 (look)

_Written 2026-10-18 09:14 CEST by a mockup agent (Claude). Static mockups only. No app code was changed._

Open `index.html` in a browser. It is one self-contained page: inline CSS, with fonts from Google Fonts for the mockup only. The app would self-host woff2. It shows three directions for the same slice of the answer page: the question, the recommendation (headline, summary, confidence, citation chips), the setup drawing as a blueprint, the option tabs, an expanded "What to measure" section and the open questions. Under each direction are its fonts, licence, weights, rationale and a dark-mode swatch.

**Content:** every text, ID and citation is copied from the saved dev output `outputs/dev/D03.json` (option O2, recommended). The headline is the first clause of that run's `brief_answer`. The blueprint SVG was drawn by hand for the mockup. In the app it would still be drawn by code from the option (`diagrams.py`).

**How the drawing links to the sections:** the callouts on the drawing (P1–P3, M1–M2, Q3) use the same IDs as the parameter rows, the methods and the open questions below. A shows the hover state (P2 highlighted in the drawing and in the table). B points to the sections from the figure caption. C adds a key strip under the drawing that sends each callout group to its numbered section, and a numbered rail runs down the whole page.

| | Direction | Fonts (all SIL OFL 1.1) | Layout (5.10) | Blueprint (5.11) |
|---|---|---|---|---|
| A | Technical report | IBM Plex Serif 500/600, Plex Sans 400–600, Plex Mono 400/500 | sticky numbered index on the left; recommendation card with a definition list | whiteprint: blue ink on gridded paper, double frame, title block |
| B | Journal | Newsreader 400–600 with an opsz axis; Source Sans 3 600 for UI chrome only | single reading column, citations as margin notes with their quotes, booktabs table | cyanotype plate (white on Prussian blue) as "Fig. 1" with a caption |
| C | Engineering dossier | Source Sans 3 400–700, Source Serif 4 600 (opsz), Source Code Pro 500/600 | numbered section rail 01–05, key-facts strip, cards | white-line blueprint on navy with a key strip that flows into sections 03–05 |

Screenshots (1440 px wide, the first 1400 px of each direction): `direction-a.png`, `direction-b.png`, `direction-c.png`, and `overview.png` with all three side by side.

Rebuild: `uv run python docs/mockups/build/build.py` (writes `index.html` from `build/template.html` and `build/bp.py`).

## Sources (fetched 2026-10-18)

1. Adobe Fonts, Source Serif repository (OFL-1.1; Source Serif 4 adds optical sizes; WOFF2 provided): https://github.com/adobe-fonts/source-serif
2. Source Sans LaTeX package documentation (Source Sans 3 under OFL 1.1; lining and tabular figures by default): https://mirrors.mit.edu/CTAN/fonts/sourcesans/doc/sourcesans.tex
3. Production Type, Newsreader (commissioned by Google Fonts for on-screen long-form reading; 3 optical sizes, 7 weights): https://www.productiontype.com/news/new_fonts_from_production_type_newsreader
4. STIX Two (OFL; started by a group of scientific publishers for technical publishing). Considered and not used, because it is built for print and maths rather than UI text: https://tug.ctan.org/fonts/stix2-otf/README.md and https://fontsource.org/fonts/stix-two-text/about
5. IBM Plex (OFL-1.1 superfamily; Sans and Mono are already self-hosted in the app): https://github.com/IBM/plex
6. ISO 128-2:2022, basic line conventions for technical drawings (line types and widths; used for the thick/thin/hair hierarchy, the chain centre line and dashed hidden parts): https://iteh.es/catalog/standards/iso/ed38e2d0-844f-4eb5-97a9-8770b7a9acd6/iso-128-2-2022
7. Blueprint and cyanotype history (white lines on Prussian blue; diazo "whiteprints" with blue lines on white replaced them from the 1940s): https://en.wikipedia.org/wiki/Blueprint and https://en.wikipedia.org/wiki/Cyanotype
8. Pairing guidance (a serif with a sans gives contrast within harmony; keep the role assignment consistent): https://www.typewolf.com/blog/google-fonts-combinations

## Caveats

- The licence for each family was checked from the sources above. The exact weight and axis ranges on Google Fonts were not re-checked one by one.
- The ISO 128 line widths were not read from the standard itself, only its scope. The drawing uses a plausible thick/thin/hair ratio, not a normative one.
- The mockup was checked at desktop width only. The 390 px layout is not designed yet.
