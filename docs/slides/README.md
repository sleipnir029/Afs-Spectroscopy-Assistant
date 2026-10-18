# Slides

- `slides.html`: the deck (8 slides, 1280×720). Fonts come from `src/afs_assistant/ui/static/fonts/`, images from this folder.
- `slides.md`: the same text as plain Markdown, kept in sync with `slides.html`.
- `slides.pdf`: exported from `slides.html` with headless Chrome (no other tool needed).

Story (DEVIATIONS D-068; the submission form's slide topics): title → the challenge and our approach → system architecture (flow and model team) → use of the AFS materials (documents, what code builds, the checks, the reader-facing labels) → example recommendation (H04) → example feasibility-study plan (H04) → the six evaluation cases with results → limitations and next steps. Slides 5 and 6 copy lines from `outputs/final/brief/H04.md` and `outputs/final/H04.md` character for character (trimmed, never reworded).

## Re-export the PDF

From the repo root (macOS, Google Chrome installed):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html"
```

Check: `pdfinfo docs/slides/slides.pdf` shows 8 pages of 960 × 540 pts.

## Placeholder to replace before submitting

The team members' names are filled in (slide 1). One placeholder is left, in both `slides.html` and `slides.md`:

| Placeholder | Where | Replace with |
|---|---|---|
| (filled) | slide 1 and slide 8 | https://github.com/sleipnir029/Afs-Spectroscopy-Assistant |

Replace it, then re-export (macOS `sed`; `#` is the delimiter so the URL's slashes need no escaping):

```bash
sed -i '' -e 's#REPO_URL_PENDING#https://github.com/OWNER/REPO#g' \
  docs/slides/slides.html docs/slides/slides.md
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html"
grep -c "_PENDING" docs/slides/slides.html docs/slides/slides.md   # expect 0 and 0
```

## Images

- The 8-slide deck uses no images.
- `answer-recommendation.png` (crop of `docs/video/frames/09_recommendation.png`, box (160, 0, 1275, 656)), `blocks-options-clean.png`, `blocks-setup-clean.png`, `brief-answer-1440.png`, `blocks-options.png`, `blocks-setup.png`: images of earlier decks, no longer used (kept in git).

## Numbers not in another committed file, or derived

- Checks per answer, 122–161 (slide 3): `manifest.verification.checks` in `outputs/final/H0*.json`.
- 4.06 vs 4.15 and 3–6× faster (slide 3): mix 4.06 at 84 s, best single model 4.15 at 259 s, old setup 504 s per case, in `outputs/bakeoff-dev/blind/summary.md` (7 setups, D01–D08 practice cases, 4 blind AI judges); $0.03 per case is the mix's $0.030 there.
- Knowledge counts (slide 4): `uv run afs-assist kb check`, 13/13 PASS (67 pages, 44 rules, 77 rule and fiber quotes exact on their page: 70 rule quotes in `knowledge/rules.yaml` + 7 fiber quotes); 19 rows in `knowledge/table1_methods.json`; 7 fiber families in `knowledge/fibers.json`.
- 120/120 quotes (slides 4 and 7): `manifest.verification.citations_verified / citations_total` in `outputs/final/H0*.json` (14 + 16 + 21 + 25 + 22 + 22).
- 0 failed hard checks, 8 minor warnings (slide 7): `hard_failures` 0 and `soft_failures` 1, 0, 2, 3, 1, 1 in `outputs/final/H0*.json`.
- 1.5–3 min per case (slide 7): `timings_s.wall` in `outputs/final/H0*.json`, 97–184 s. $0.29: the sum of `manifest.cost_usd`, $0.288.
- Short view 560–698 words (slide 8): words in `outputs/final/brief/H0*.md`, counting tokens that contain a letter or digit (`wc -w` gives 598–741 because it also counts table pipes). Full answers about 3,000: `wc -w outputs/final/H0*.md` gives 3,058–3,455. AFS's worked answers 300–400: `scenarios/dev_reference.jsonl` (README.md "Known limitations").
- 15 of 17 options "Low" (slide 8): the Confidence column of the options tables in `outputs/final/brief/H0*.md` (H02 has two options, both Medium; the other five have three options each, all Low).
- 4–5 questions on a complete enquiry (slide 8): README.md "Known limitations" (A07, D-051).
- Fixing step 46–72 % of each run (slide 8): `timings_s.repair / timings_s.wall` in `outputs/final/H0*.json` (H01 44/97 s, H04 130/180 s).
- Judging criteria and weights (slide 2): the organiser's challenge brief PDF (in `resources/`, not committed); the same weights are in `docs/review-final/A-brief-and-outputs.md` §1c.

Every other figure names its source file in the slide footer.
