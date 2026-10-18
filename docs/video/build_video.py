"""Demo video builder: compose captioned frames (Pillow), write captions.srt, build demo.mp4 (ffmpeg concat, libx264).

Usage: uv run --with pillow python docs/video/build_video.py WORKDIR   (WORKDIR/shots/ holds the raw 1440x900 Playwright screenshots).
Needs Pillow and /opt/homebrew/bin/ffmpeg (this ffmpeg build has no drawtext/libass, so captions are drawn with Pillow).
"""
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SCR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent   # work dir with shots/
SHOTS = SCR / "shots"
OUT = Path(__file__).resolve().parent
FR = OUT / "frames"
W, H = 1440, 900
SUP = Path("/System/Library/Fonts/Supplemental")
ARIAL, ARIAL_B = str(SUP / "Arial.ttf"), str(SUP / "Arial Bold.ttf")
GEO, GEO_B, GEO_I = str(SUP / "Georgia.ttf"), str(SUP / "Georgia Bold.ttf"), str(SUP / "Georgia Italic.ttf")
BG, INK, RED, MUTED = (246, 241, 234), (28, 23, 20), (176, 58, 30), (110, 100, 92)

# (output name, source shot or card, seconds, caption, caption position)
SHOTLIST = [
    ("01_title", "card:title", 4, "", "bottom"),
    ("02_start", "s01_start.png", 6, "Start screen: `uv run afs-assist ui` serves a local page. Describe what you want to measure.", "bottom"),
    ("03_enquiry", "s02_typed.png", 7, "A new, generic enquiry: ethanol in a clear, filtered fermentation broth in a pipe; GC is the lab reference.", "bottom"),
    ("04_running", "s03_running_00.png", 4, "Get assessment: the real pipeline starts (production models, live literature search).", "top"),
    ("05_steps", "s03_running_03.png", 5, "Pipeline steps with timings: read the enquiry, screen methods against the AFS rules, assess.", "top"),
    ("06_feed", "s03_running_07.png", 7, "Live activity feed: methods ruled out with the S01 Table 1 reason; 29 citations checked against the AFS pages.", "top"),
    ("07_repair", "s03_running_08.png", 5, "One hard check failed, so the failed checks go back to the model for a repair round.", "top"),
    ("08_answer", "s04_answer_top.png", 8, "Answer after 107 s (pipeline wall time, $0.036): the recommendation, a pinned strip (status, confidence, open questions), quotes in the margin.", "bottom"),
    ("09_recommendation", "s05_recommendation.png", 8, "Status, confidence with its reason, and the next step. Every quote beside the answer is word for word from AFS.", "bottom"),
    ("10_verify", "s06b_verify.png", 9, "Open a margin quote: the stored S01 p.18 page text with the quote highlighted, marked verified (exact match).", "bottom"),
    ("11_options", "s07_options.png", 8, "Options: simple, recommended, extended. Cost class comes from S01 Table 1 (p.6) rows; it is not a price.", "bottom"),
    ("12_setup", "s08_setup.png", 8, "Setup sketch drawn by code from the proposed option; the dashed sensor is auxiliary, to be confirmed with AFS.", "bottom"),
    ("13_followup", "s10_followup_typed.png", 4, "A follow-up in the composer: \"Why not Raman as the first choice?\"", "top"),
    ("14_followup_wait", "s11_followup_wait.png", 4, "Follow-up questions are answered from the assessment and the AFS pages: one model call, quotes checked before display.", "top"),
    ("15_followup_answer", "s12_followup_answer.png", 9, "Answer in 5.3 s, $0.006: each point cited (S01 p.18, p.11, p.6), or marked as engineering judgement.", "bottom"),
    ("16_followup_blocks", "s13_followup_blocks.png", 6, "Inline result blocks: the options table is shown again inside the answer.", "bottom"),
    ("17_followup_setup", "s14_followup_simple_setup.png", 6, "...plus the setup sketch of the Raman (simple) option and the first feasibility test.", "bottom"),
    ("18_answer_question", "s15_answer_q2.png", 7, "Answer an open question in place: process temperature about 32 °C, 28 to 36 °C during a batch.", "top"),
    ("19_reassess_running", "s16_reassess_run_05.png", 6, "Update the recommendation: the full assessment runs again with the new fact (v2).", "bottom"),
    ("20_v2", "s17_v2_top.png", 7, "v2 after 147 s ($0.046): the temperature range is now part of the advice; the open questions drop to Q1 and Q3.", "bottom"),
    ("21_what_changed", "s18_what_changed.png", 9, "What changed, v1 to v2: the proposed setup now tests NIR and Raman together; status and confidence unchanged.", "bottom"),
    ("22_closing", "card:closing", 8, "", "bottom"),
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
    for i, t in enumerate(["Live demo of the real app: one new enquiry, a follow-up question, one re-assessment.",
                           "Production models (mix-a), live literature search. No voice; captions only.",
                           "Team Helios · Art Fiber Systems challenge · October 2026"]):
        d.text((160, 470 + i * 52), t, font=font(ARIAL, 28), fill=MUTED if i == 2 else INK)
    return img


def card_closing():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.text((160, 130), "Evaluation results", font=font(GEO_B, 60), fill=INK)
    d.text((160, 215), "From STATUS.md (freeze-1, production models mix-a, external search live).",
           font=font(ARIAL, 26), fill=MUTED)
    stats = [("0", "hard failures", "H01–H06 held-out set, run once"),
             ("120/120", "citations verified", "H01–H06, every quote checked against its AFS page"),
             ("~105 s", "mean time per case", "19-case gate on mix-a (dev + adversarial)")]
    for i, (num, label, sub) in enumerate(stats):
        x = 160 + i * 380
        d.line([(x, 320), (x + 330, 320)], fill=RED, width=3)
        d.text((x, 345), num, font=font(ARIAL_B, 72), fill=RED)
        d.text((x, 450), label, font=font(ARIAL_B, 30), fill=INK)
        for j, line in enumerate(wrap(d, sub, font(ARIAL, 23), 330)):
            d.text((x, 500 + j * 32), line, font=font(ARIAL, 23), fill=MUTED)
    d.text((160, 690), "Every important claim quotes the supplied AFS documents word for word.",
           font=font(GEO_I, 32), fill=INK)
    d.text((160, 745), "uv run afs-assist ui", font=font(str(SUP / "Courier New.ttf"), 30), fill=INK)
    return img


def srt_time(s):
    return f"{int(s // 3600):02d}:{int(s % 3600 // 60):02d}:{int(s % 60):02d},{round((s % 1) * 1000):03d}"


def main():
    if FR.exists():
        shutil.rmtree(FR)
    FR.mkdir(parents=True)
    concat, srt, t, n = [], [], 0.0, 0
    for name, src, secs, cap, pos in SHOTLIST:
        if src == "card:title":
            img = card_title()
        elif src == "card:closing":
            img = card_closing()
        else:
            img = Image.open(SHOTS / src)
            assert img.size == (W, H), (src, img.size)
        Image.Image.save(img.convert("RGB"), FR / f"{name}.png", optimize=True)        # clean key frame
        burned = caption(img, cap, pos) if cap else img.convert("RGB")
        p = SCR / "burned" / f"{name}.png"
        p.parent.mkdir(exist_ok=True)
        burned.save(p)
        concat.append(f"file '{p}'\nduration {secs}\n")
        if cap:
            n += 1
            srt.append(f"{n}\n{srt_time(t)} --> {srt_time(t + secs)}\n{cap}\n")
        t += secs
    concat.append(f"file '{p}'\n")                 # concat demuxer: repeat last file so its duration applies
    (SCR / "concat.txt").write_text("".join(concat))
    (OUT / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    subprocess.run(["/opt/homebrew/bin/ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
                    "-safe", "0", "-i", str(SCR / "concat.txt"), "-vf", "fps=30,format=yuv420p",
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-tune", "stillimage",
                    "-t", str(t), "-movflags", "+faststart", str(OUT / "demo.mp4")], check=True)
    print("total seconds", t)


if __name__ == "__main__":
    main()
