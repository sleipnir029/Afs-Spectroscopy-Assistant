# Independent UX review of round 2 (reviewer agent, 2026-10-18 ~09:50)

**Verdict: PASS_WITH_CAVEATS.** Pick: **H3 with H1's circle callouts** (then H1, then H2).

The builder's scores look inflated by 4–6 points; my estimates are H1 ~40, H2 ~35, H3 ~42. Keyboard handling, the open citation panel and intermediate widths were never tested.

Not taken from the audit's pick:
- **No H1 vertical index at ≥1280 px.** It would add a second navigation mode, and the column would jump ~250 px whenever a citation opens.
- **No "4 P2" pill callouts.** On the narrow drawing they collide with the frame and lines, and the number means nothing until the reader learns the key.

## Must-fix for H3 before implementation
1. Circle callouts showing the ID only, reusing the existing `data-part` highlighting (`app.js:42–47`).
2. Drop the CSS `::after` quote tooltip; it fails WCAG 1.4.13. Keep the existing citation panel.
3. The facts strip must name the option its cost class comes from, or the headline must be bound to the recommended option. Today the headline says "NIR, least effort" while the strip says "High (rows 2, 7)" from option O2 "NIR + MIR".
4. Wide-drawing switch at ≥ 930 px, or SVG minimum font 14. Between 860 and 923 px the drawing text renders at ~11.2 px.
5. Use one label per section in both the bar and the headings.
6. Phones: scroll-spy JS, a fading right edge on the section bar, and the active item scrolled into view.
7. Phones: move the recommendation rule above the "1" numeral.
8. Full fiber text in the figure notes instead of "…" (`_fit()` takes notes).
9. Add Plex Serif 600 woff2 to `static/fonts/` (OFL).

## Other findings
- H2: the focus ring is ~2.5:1 on the navy key strip, and lines run to ~115 characters.
- H1: too many display devices per section; the circles crowd the phone bar.

## Tests before closing
- Run a 1-method and a 3-method option at 320, 390, 1100, 1280 and 1440 px, with the panel open and closed, in both themes.
- Assert that SVG text is ≥ 12 px at each width.
- Do one keyboard pass.
