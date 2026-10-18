# Slides

- `slides.html`: the deck (11 slides, 1280×720). Fonts come from `src/afs_assistant/ui/static/fonts/`, images from this folder.
- `slides.md`: the same text as plain Markdown, kept in sync with `slides.html`.
- `slides.pdf`: exported from `slides.html` with headless Chrome (no other tool needed).

## Re-export the PDF

From the repo root (macOS, Google Chrome installed):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html"
```

Check: `pdfinfo docs/slides/slides.pdf` shows 11 pages of 960 × 540 pts.

## Repository URL (slide 11)

Slide 11 carries the placeholder `REPO_URL_PENDING` in both `slides.html` and `slides.md`. At publish, replace it with the public URL and re-export:

```bash
sed -i '' 's#REPO_URL_PENDING#https://github.com/OWNER/REPO#g' docs/slides/slides.html docs/slides/slides.md
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html"
```

## Images

- `answer-recommendation.png` (slide 3): crop of `docs/video/frames/09_recommendation.png`, box (160, 0, 1275, 656).
- `blocks-options-clean.png` (slide 5): crop of `docs/video/frames/11_options.png`, box (165, 104, 897, 342), header to the end of the cost-class row.
- `blocks-setup-clean.png` (slide 5): crop of `docs/video/frames/12_setup.png`, box (165, 104, 897, 486), full diagram with labels.
- `brief-answer-1440.png`, `blocks-options.png`, `blocks-setup.png`: images of the earlier deck, no longer used.

## Numbers not in another committed file

- Offline tests (slide 8): `uv run pytest -q` on master 979b59b, 2026-10-18 14:44 CEST, with `knowledge/pages.jsonl` rebuilt locally: **890 passed, 2 skipped**.

Every other figure names its source file in the slide footer.
