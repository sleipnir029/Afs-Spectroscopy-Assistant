"""Demo video builder: compose captioned frames (Pillow), write captions.srt, build demo.mp4 (ffmpeg concat, libx264).

Usage: uv run --with pillow python docs/video/build_video.py [WORKDIR]
- The app screenshots are the committed, caption-free frames in docs/video/frames/ (1440x900 Playwright shots).
  They are read in place and never deleted or rewritten. A frame not named in SHOTLIST stays on disk, unused.
- The cards (title, problem, architecture, feasibility plan, limits, closing) are drawn here and saved to docs/video/frames/ as well.
- WORKDIR (default: a new temp dir) receives the captioned frames and the ffmpeg concat list.
Needs Pillow, the macOS fonts in /System/Library/Fonts/Supplemental and /opt/homebrew/bin/ffmpeg
(this ffmpeg build has no drawtext/libass, so captions are drawn with Pillow).
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(tempfile.mkdtemp(prefix="afs-video-"))   # scratch output
OUT = Path(__file__).resolve().parent
FR = OUT / "frames"
W, H = 1440, 900
SUP = Path("/System/Library/Fonts/Supplemental")
ARIAL, ARIAL_B = str(SUP / "Arial.ttf"), str(SUP / "Arial Bold.ttf")
GEO, GEO_B, GEO_I = str(SUP / "Georgia.ttf"), str(SUP / "Georgia Bold.ttf"), str(SUP / "Georgia Italic.ttf")
BG, INK, RED, MUTED = (246, 241, 234), (28, 23, 20), (176, 58, 30), (110, 100, 92)

# (frame name in frames/, "shot" or a card, seconds, caption, caption position)
# 16_followup_blocks.png is not used: it shows the options table twice, a bug fixed after recording (4ac8f83).
SHOTLIST = [
    ("01_title", "card:title", 4, "", "bottom"),
    ("01b_problem", "card:problem", 10, "", "bottom"),
    ("01c_architecture", "card:architecture", 12, "", "bottom"),
    ("02_start", "shot", 8, "The local app (uv run afs-assist ui): type an enquiry, try an example, or open a finished one.", "bottom"),
    ("03_enquiry", "shot", 8, "A new, generic enquiry: ethanol in a clear, filtered fermentation broth in a pipe; GC is the lab reference.", "bottom"),
    ("04_running", "shot", 5, "Get assessment: the real pipeline starts (production models, live literature search).", "top"),
    ("05_steps", "shot", 6, "Pipeline steps with timings: read the enquiry, screen methods against the AFS rules, assess.", "top"),
    ("06_feed", "shot", 8, "Live activity feed: methods ruled out with the S01 Table 1 reason; 29 citations checked against the AFS pages.", "top"),
    ("07_repair", "shot", 7, "One hard check failed, so the failed checks go back to the model for a repair round.", "top"),
    ("08_answer", "shot", 9, "Answer after 107 s (pipeline wall time, $0.036): the recommendation, a pinned strip (status, confidence, open questions), quotes in the margin.", "bottom"),
    ("09_recommendation", "shot", 8, "Status, confidence with its reason, and the next step. Every quote beside the answer was found on its AFS page.", "bottom"),
    ("10_verify", "shot", 8, "Open a margin quote: the stored S01 p.18 page text with the quote highlighted, marked verified (exact match).", "bottom"),
    ("11_options", "shot", 8, "Options: simple, recommended, extended. Cost class comes from S01 Table 1 (p.6) rows; it is not a price.", "bottom"),
    ("12_setup", "shot", 8, "Setup sketch drawn by code from the proposed option; the dashed sensor is auxiliary, to be confirmed with AFS.", "bottom"),
    ("12b_feasibility", "card:feasibility", 14, "", "bottom"),
    ("13_followup", "shot", 5, "A follow-up in the composer: \"Why not Raman as the first choice?\"", "top"),
    ("14_followup_wait", "shot", 8, "Follow-up questions are answered from the assessment and the AFS pages: one model call, quotes checked before display.", "top"),
    ("15_followup_answer", "shot", 7, "Answer in 5.3 s, $0.006: each point cited (S01 p.18, p.11, p.6), or marked as engineering judgement.", "bottom"),
    ("17_followup_setup", "shot", 7, "Inline result blocks: the setup sketch of the Raman (simple) option and the first feasibility test.", "bottom"),
    ("18_answer_question", "shot", 8, "Answer an open question in place: process temperature about 32 °C, 28 to 36 °C during a batch.", "top"),
    ("19_reassess_running", "shot", 6, "Update the recommendation: the full assessment runs again with the new fact (v2).", "bottom"),
    ("20_v2", "shot", 9, "v2 after 147 s ($0.046): the temperature range is now part of the advice; the open questions drop to Q1 and Q3.", "bottom"),
    ("21_what_changed", "shot", 15, ("What changed, v1 to v2: the method now adds a Raman probe; status and confidence unchanged. "
                                     "A temperature alone does not justify that: a re-assessment is a fresh model run and can "
                                     "shift (a known limitation)."), "bottom"),
    ("21b_limits", "card:limits", 10, "", "bottom"),
    ("22_closing", "card:closing", 9, "", "bottom"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def caption(img, text, pos):
    img = img.convert("RGBA")
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    fnt = font(ARIAL, 27)
    lines = wrap(d, text, fnt, W - 160)
    lh, pad = 38, 20
    bh = len(lines) * lh + 2 * pad
    y0 = H - bh - 28 if pos == "bottom" else 28
    d.rounded_rectangle([60, y0, W - 60, y0 + bh], radius=10, fill=(20, 17, 15, 218))
    for i, line in enumerate(lines):
        tw = d.textlength(line, font=fnt)
        d.text(((W - tw) / 2, y0 + pad + i * lh), line, font=fnt, fill=(255, 255, 255, 255))
    return Image.alpha_composite(img, layer).convert("RGB")


def card_title():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((160, 250), "AFS Spectroscopy Assistant", font=font(GEO_B, 72), fill=INK)
    d.text((160, 350), "An in-line spectroscopy enquiry in, a cited first technical assessment out.",
           font=font(GEO_I, 34), fill=INK)
    d.line([(160, 430), (1280, 430)], fill=RED, width=3)
    for i, t in enumerate(["The real app during a live run (captioned screenshots): one enquiry, a follow-up, one re-assessment.",
                           "Production models (mix-a), live literature search. No voice; captions only.",
                           "Team Helios · Art Fiber Systems challenge · October 2026"]):
        d.text((160, 470 + i * 52), t, font=font(ARIAL, 28), fill=MUTED if i == 2 else INK)
    return img


def card_problem():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((160, 150), "The problem", font=font(GEO_B, 60), fill=INK)
    d.text((160, 245), "An AFS sales engineer gets a customer enquiry about in-line spectroscopy:",
           font=font(ARIAL, 28), fill=INK)
    d.text((160, 300), "“Which method and probe should we test first, and what do you need from us?”",
           font=font(GEO_I, 32), fill=INK)
    d.line([(160, 380), (1280, 380)], fill=RED, width=3)
    d.text((160, 410), "What they need is a cited first technical assessment:", font=font(ARIAL_B, 28), fill=INK)
    for i, t in enumerate(["screen NIR, MIR, Raman, UV-Vis and fluorescence against sample, probe and fiber limits",
                           "propose one option to test first, and ask only what would change it",
                           "back the key claims with the supplied AFS material, page by page"]):
        d.text((160, 470 + i * 52), "–  " + t, font=font(ARIAL, 27), fill=INK)
    return img


# Architecture card: models from config/models.yaml (roles intake, assess, repair); counts from `uv run afs-assist kb check`.
ARCH_STEPS = [("model", "Understand the enquiry", "Gemini 3.5 Flash-Lite"),
              ("code", "Screen the 5 methods against 44 AFS rules", ""),
              ("model", "Write the assessment from 67 AFS pages", "GLM-5.3-Flash"),
              ("code", "Check every quote, page, number, wording", ""),
              ("model", "Fix what failed", "second model: Gemini 3.8 Flash"),
              ("code", "Answer with sources", "")]


def card_architecture():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((120, 130), "How it works", font=font(GEO_B, 60), fill=INK)
    d.text((120, 215), "One assessment, left to right. Red boxes are model calls; black-outlined boxes are plain code.",
           font=font(ARIAL, 26), fill=MUTED)
    d.line([(120, 280), (1320, 280)], fill=RED, width=3)
    bw, gap, y0, y1 = 176, 28, 330, 600
    for i, (kind, step, model) in enumerate(ARCH_STEPS):
        x = 120 + i * (bw + gap)
        is_model = kind == "model"
        d.rounded_rectangle([x, y0, x + bw, y1], radius=10, fill=(250, 228, 218) if is_model else (255, 252, 248),
                            outline=RED if is_model else INK, width=3)
        d.text((x + 14, y0 + 16), "MODEL" if is_model else "CODE", font=font(ARIAL_B, 19), fill=RED if is_model else INK)
        for j, line in enumerate(wrap(d, step, font(ARIAL_B, 23), bw - 28)):
            d.text((x + 14, y0 + 56 + j * 30), line, font=font(ARIAL_B, 23), fill=INK)
        mlines = wrap(d, model, font(ARIAL, 20), bw - 28) if model else []
        for j, line in enumerate(mlines):
            d.text((x + 14, y1 - 16 - (len(mlines) - j) * 26), line, font=font(ARIAL, 20), fill=RED)
        if i < len(ARCH_STEPS) - 1:                                        # arrow to the next box
            ax, ay = x + bw + 4, (y0 + y1) // 2
            d.line([(ax, ay), (ax + gap - 10, ay)], fill=INK, width=3)
            d.polygon([(ax + gap - 8, ay), (ax + gap - 18, ay - 7), (ax + gap - 18, ay + 7)], fill=INK)
    d.text((120, 650), "Literature is searched only for gaps the AFS documents leave open, and marked secondary.",
           font=font(GEO_I, 29), fill=INK)
    d.text((120, 760), "Models: config/models.yaml (mix-a). Rules and pages: uv run afs-assist kb check.",
           font=font(ARIAL, 22), fill=MUTED)
    return img


# Feasibility card: steps copied word for word (selected, not reworded) from the demo run v1 record,
# runs/adhoc-20261018T103823Z-e0e0/assessment.json, field feasibility_plan.steps[].step (5 steps; 4 is left out).
# Steps 1-3 are also on screen in frames/17_followup_setup.png. The step 5 tag is that step's own citation.
FEAS_STEPS = [("1", "Collect representative filtered broth samples across the expected variation in ethanol concentration, "
                    "temperature and co-fermentation components over several runs.", ""),
              ("2", "Measure each sample with GC as the independent reference, using the customer's existing lab method.", ""),
              ("3", "Record NIR transmission/transflection spectra at a controlled pathlength on the same samples, "
                    "and Raman probe spectra in parallel as the comparison method.", ""),
              ("5", "Define the go/no-go basis with the customer: the in-line prediction error on held-out runs must "
                    "meet the accuracy they specify against GC before an in-line installation is designed.", "REF p.3")]


def card_feasibility():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((160, 110), "Feasibility-study plan", font=font(GEO_B, 60), fill=INK)
    d.text((160, 195), "From this demo run (v1), generated by the assistant. Steps 1–3 and 5 of 5, word for word.",
           font=font(ARIAL, 26), fill=MUTED)
    d.line([(160, 255), (1280, 255)], fill=RED, width=3)
    y, fnt = 290, font(ARIAL, 27)
    for num, step, cite in FEAS_STEPS:
        d.text((160, y), num + ".", font=font(ARIAL_B, 27), fill=RED)
        lines = wrap(d, step, fnt, 1070)
        for j, line in enumerate(lines):
            d.text((210, y + j * 38), line, font=fnt, fill=INK)
        if cite:
            lx = 210 + d.textlength(lines[-1], font=fnt) + 14
            ly = y + (len(lines) - 1) * 38
            d.rectangle([lx, ly + 1, lx + d.textlength(cite, font=font(ARIAL_B, 20)) + 14, ly + 32], outline=RED, width=2)
            d.text((lx + 7, ly + 5), cite, font=font(ARIAL_B, 20), fill=RED)
        y += len(lines) * 38 + 26
    d.text((160, 790), "Source: demo run record on the provenance branch, runs/adhoc-20261018T103823Z-e0e0/assessment.json.",
           font=font(ARIAL, 22), fill=MUTED)
    return img


def card_limits():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((160, 200), "Known limits", font=font(GEO_B, 60), fill=INK)
    d.line([(160, 300), (1280, 300)], fill=RED, width=3)
    for i, t in enumerate(["Reports are long: 3,000–3,500 words, vs 300–400 in the AFS worked answers.",
                           "“Verified” means the quote is on the cited page, not that it fully supports the claim.",
                           "A re-assessment is a fresh model run and can shift the method, as in this demo."]):
        d.text((160, 340 + i * 60), "–  " + t, font=font(ARIAL, 29), fill=INK)
    d.text((160, 560), "Full list: README, “Known limitations”.", font=font(ARIAL, 26), fill=MUTED)
    return img


def card_closing():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((160, 130), "Evaluation results", font=font(GEO_B, 60), fill=INK)
    d.text((160, 215), "H01–H06 held-out set, run once at tag freeze-1 (production models mix-a, external search live).",
           font=font(ARIAL, 26), fill=MUTED)
    stats = [("0", "hard failures", "all six held-out cases"),
             ("120/120", "citations verified", "each quote found word for word on its AFS page"),
             ("97–184 s", "per case", "$0.288 for all six cases")]
    for i, (num, label, sub) in enumerate(stats):
        x = 160 + i * 380
        d.line([(x, 320), (x + 330, 320)], fill=RED, width=3)
        d.text((x, 345), num, font=font(ARIAL_B, 72), fill=RED)
        d.text((x, 450), label, font=font(ARIAL_B, 30), fill=INK)
        for j, line in enumerate(wrap(d, sub, font(ARIAL, 23), 330)):
            d.text((x, 500 + j * 32), line, font=font(ARIAL, 23), fill=MUTED)
    claim = "Every quote is checked against its AFS page; claims without a source are labelled."
    for j, line in enumerate(wrap(d, claim, font(GEO_I, 32), 1120)):
        d.text((160, 650 + j * 44), line, font=font(GEO_I, 32), fill=INK)
    d.text((160, 760), "uv run afs-assist ui", font=font(str(SUP / "Courier New.ttf"), 30), fill=INK)
    return img


CARDS = {"card:title": card_title, "card:problem": card_problem, "card:architecture": card_architecture,
         "card:feasibility": card_feasibility, "card:limits": card_limits, "card:closing": card_closing}


def srt_time(s):
    return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{round((s % 1) * 1000):03d}"


def main():
    burned_dir = SCR / "burned"
    burned_dir.mkdir(parents=True, exist_ok=True)
    concat, srt, t, n = [], [], 0.0, 0
    for name, src, secs, cap, pos in SHOTLIST:
        if src in CARDS:
            img = CARDS[src]()
            img.save(FR / f"{name}.png", optimize=True)                  # cards are drawn here; shots are never rewritten
        else:
            img = Image.open(FR / f"{name}.png")
        assert img.size == (W, H), (name, img.size)
        burned = caption(img, cap, pos) if cap else img.convert("RGB")
        p = burned_dir / f"{name}.png"
        burned.save(p)
        concat.append(f"file '{p}'\nduration {secs}\n")
        if cap:
            n += 1
            srt.append(f"{n}\n{srt_time(t)} --> {srt_time(t + secs)}\n{cap}\n")
            print(f"#{n:2d} {srt_time(t)} {name}: {len(cap.split())} words / {secs} s = {len(cap.split()) / secs:.2f} w/s")
        t += secs
    concat.append(f"file '{p}'\n")                 # concat demuxer: repeat last file so its duration applies
    (SCR / "concat.txt").write_text("".join(concat))
    (OUT / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
                    "-safe", "0", "-i", str(SCR / "concat.txt"), "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "stillimage",
                    "-t", str(t), "-movflags", "+faststart", str(OUT / "demo.mp4")], check=True)
    print("total seconds", t, "work dir", SCR)


if __name__ == "__main__":
    main()
