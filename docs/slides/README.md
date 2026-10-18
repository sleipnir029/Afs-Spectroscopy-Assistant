# Slides

- `slides.html`: the deck (12 slides, 1280×720). Fonts come from `src/afs_assistant/ui/static/fonts/`, images from this folder.
- `slides.md`: the same text as plain Markdown, kept in sync with `slides.html`.
- `slides.pdf`: exported from `slides.html` with headless Chrome (no other tool needed).

Story (DEVIATIONS D-067): title → the challenge and how it is judged → what we built → how it works (flow, reading the AFS documents, the checks, the model team) → proof (the six held-out questions, H04 up close) → results in numbers → what we'd add next → thank you.

## Re-export the PDF

From the repo root (macOS, Google Chrome installed):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html"
```

Check: `pdfinfo docs/slides/slides.pdf` shows 12 pages of 960 × 540 pts.

## Placeholders to replace before submitting

Two placeholders appear in both `slides.html` and `slides.md`:

| Placeholder | Where | Replace with |
|---|---|---|
| `TEAM_MEMBERS_PENDING` | slide 1 (under "Team Helios") and slide 12 | the team members' names, e.g. `Ada Lovelace · Alan Turing` |
| `REPO_URL_PENDING` | slide 1 (small line) and slide 12 | the public repository URL |

Replace both, then re-export (macOS `sed`; `#` is the delimiter so the URL's slashes need no escaping):

```bash
sed -i '' -e 's#TEAM_MEMBERS_PENDING#Name One · Name Two · Name Three#g' \
          -e 's#REPO_URL_PENDING#https://github.com/OWNER/REPO#g' \
  docs/slides/slides.html docs/slides/slides.md
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="$PWD/docs/slides/slides.pdf" "file://$PWD/docs/slides/slides.html"
grep -c "_PENDING" docs/slides/slides.html docs/slides/slides.md   # expect 0 and 0
```

## Images

- `answer-recommendation.png` (slide 3): crop of `docs/video/frames/09_recommendation.png`, box (160, 0, 1275, 656).
- `blocks-options-clean.png`, `blocks-setup-clean.png`, `brief-answer-1440.png`, `blocks-options.png`, `blocks-setup.png`: images of earlier decks, no longer used (kept in git).

## Numbers not in another committed file, or derived

- Offline tests (slide 10): `uv run pytest -q` on master 979b59b, 2026-10-18 14:44 CEST, with `knowledge/pages.jsonl` rebuilt locally: **890 passed, 2 skipped** (also README.md "Reproducibility").
- Checks per answer, 122–161 (slide 4): `manifest.verification.checks` in `outputs/final/H0*.json`.
- 1.5–3 min per question (slide 10): `timings_s.wall` in `outputs/final/H0*.json`, 97–184 s. $0.29: the sum of `manifest.cost_usd`, $0.288.
- Fixing step 46–72 % of each run (slide 11): `timings_s.repair / timings_s.wall` in `outputs/final/H0*.json` (H01 44/97 s, H04 130/180 s).
- 3–6× faster (slide 7): 259 s and 504 s against 84 s per case in `outputs/bakeoff-dev/blind/summary.md`.
- Chat follow-ups 1.4–6.3 s (slide 10): `wall_s` of the 10 questions in `docs/chat/live-check-20261018.json` (1.36–6.34 s).
- Short view 560–698 words (slide 11): words in `outputs/final/brief/H0*.md`, counting tokens that contain a letter or digit (`wc -w` gives 598–741 because it also counts table pipes). Full answers about 3,000: `wc -w outputs/final/H0*.md` gives 3,058–3,455.
- Knowledge counts (slide 5): `uv run afs-assist kb check`, 13/13 PASS (67 pages, 44 rules, 77 rule quotes exact on their page); 19 rows in `knowledge/table1_methods.json`; 7 fiber families in `knowledge/fibers.json`.
- Judging criteria and weights (slide 2): the organiser's challenge brief PDF (in `resources/`, not committed); the same weights are in `docs/review-final/A-brief-and-outputs.md` §1c.

Every other figure names its source file in the slide footer.
