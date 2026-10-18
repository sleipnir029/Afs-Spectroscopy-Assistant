"""Demo video builder: compose captioned frames (Pillow), write captions.srt, build demo.mp4 (ffmpeg concat, libx264).

Usage: uv run --with pillow python docs/video/build_video.py [WORKDIR]
- The app screenshots are the committed, caption-free frames in docs/video/frames/ (1440x900 Playwright shots).
  They are read in place and never deleted or rewritten. A frame not named in SHOTLIST stays on disk, unused.
- The cards (title, problem, limits, closing) are drawn here and saved to docs/video/frames/ as well.
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
    ("02_start", "shot", 7, "The local app (uv run afs-assist ui): type an enquiry, try an example, or open a finished one.", "bottom"),
    ("03_enquiry", "shot", 7, "A new, generic enquiry: ethanol in a clear, filtered fermentation broth in a pipe; GC is the lab reference.", "bottom"),
    ("04_running", "shot", 5, "Get assessment: the real pipeline starts (production models, live literature search).", "top"),
    ("05_steps", "shot", 6, "Pipeline steps with timings: read the enquiry, screen methods against the AFS rules, assess.", "top"),
    ("06_feed", "shot", 7, "Live activity feed: methods ruled out with the S01 Table 1 reason; 29 citations checked against the AFS pages.", "top"),
    ("07_repair", "shot", 7, "One hard check failed, so the failed checks go back to the model for a repair round.", "top"),
    ("08_answer", "shot", 9, "Answer after 107 s (pipeline wall time, $0.036): the recommendation, a pinned strip (status, confidence, open questions), quotes in the margin.", "bottom"),
    ("09_recommendation", "shot", 8, "Status, confidence with its reason, and the next step. Every quote beside the answer is word for word from AFS.", "bottom"),
    ("10_verify", "shot", 7, "Open a margin quote: the stored S01 p.18 page text with the quote highlighted, marked verified (exact match).", "bottom"),
    ("11_options", "shot", 7, "Options: simple, recommended, extended. Cost class comes from S01 Table 1 (p.6) rows; it is not a price.", "bottom"),
    ("12_setup", "shot", 8, "Setup sketch drawn by code from the proposed option; the dashed sensor is auxiliary, to be confirmed with AFS.", "bottom"),
    ("13_followup", "shot", 5, "A follow-up in the composer: \"Why not Raman as the first choice?\"", "top"),
    ("14_followup_wait", "shot", 8, "Follow-up questions are answered from the assessment and the AFS pages: one model call, quotes checked before display.", "top"),
    ("15_followup_answer", "shot", 7, "Answer in 5.3 s, $0.006: each point cited (S01 p.18, p.11, p.6), or marked as engineering judgement.", "bottom"),
    ("17_followup_setup", "shot", 7, "Inline result blocks: the setup sketch of the Raman (simple) option and the first feasibility test.", "bottom"),
    ("18_answer_question", "shot", 7, "Answer an open question in place: process temperature about 32 °C, 28 to 36 °C during a batch.", "top"),
    ("19_reassess_running", "shot", 5, "Update the recommendation: the full assessment runs again with the new fact (v2).", "bottom"),
    ("20_v2", "shot", 9, "v2 after 147 s ($0.046): the temperature range is now part of the advice; the open questions drop to Q1 and Q3.", "bottom"),
    ("21_what_changed", "shot", 14, ("What changed, v1 to v2: the method now adds a Raman probe; status and confidence unchanged. "
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
    claim = "Every quote is checked word for word against its AFS page; claims without a source are labelled."
    for j, line in enumerate(wrap(d, claim, font(GEO_I, 32), 1120)):
        d.text((160, 650 + j * 44), line, font=font(GEO_I, 32), fill=INK)
    d.text((160, 760), "uv run afs-assist ui", font=font(str(SUP / "Courier New.ttf"), 30), fill=INK)
    return img


CARDS = {"card:title": card_title, "card:problem": card_problem, "card:limits": card_limits, "card:closing": card_closing}


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
