"""WCAG 2.x contrast ratios for the colour pairs used in the mockups (round 1 and round 2)."""
import sys


def hx(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def blend(fg, bg, a):
    f, b = hx(fg), hx(bg)
    return "#" + "".join(f"{round((a * x + (1 - a) * y) * 255):02x}" for x, y in zip(f, b))


def lum(c):
    def ch(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(v) for v in hx(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def report(rows):
    for name, fg, bg, need in rows:
        r = ratio(fg, bg)
        ok = "PASS" if r >= need else "FAIL"
        print(f"| {name} | `{fg}` on `{bg}` | {r:.2f} | {need} | {ok} |")


R1 = [
    # A light
    ("A body ink / paper", "#1b1f24", "#f7f5f0", 4.5),
    ("A muted text / paper", "#5b6470", "#f7f5f0", 4.5),
    ("A chip text / chip wash", "#0f4c81", "#e3ecf5", 4.5),
    ("A external chip (muted) / paper", "#5b6470", "#fffefb", 4.5),
    ("A drawing ink / whiteprint paper", "#123d6b", "#fbfaf6", 4.5),
    ("A drawing 'PC · CHEMOMETRICS' (55% opacity)", blend("#123d6b", "#fbfaf6", .55), "#fbfaf6", 4.5),
    ("A callout orange / whiteprint", "#b4471f", "#fbfaf6", 4.5),
    ("A linked callout text / orange fill", "#fbfaf6", "#b4471f", 4.5),
    ("A card border / paper (non-text)", "#ddd8cc", "#f7f5f0", 3.0),
    ("A dark muted / bg", "#9aa3ad", "#15181c", 4.5),
    ("A dark drawing ink / panel", "#a9c9ec", "#111821", 4.5),
    ("A dark callout / panel", "#f08a5d", "#111821", 4.5),
    # B
    ("B muted / paper", "#6a645a", "#fdfbf6", 4.5),
    ("B accent sup / paper", "#1d3f72", "#fdfbf6", 4.5),
    ("B drawing ink / cyanotype", "#f2f5fa", "#1d3f72", 4.5),
    ("B callout gold / cyanotype", "#ffd27a", "#1d3f72", 4.5),
    ("B drawing faint label (55%)", blend("#f2f5fa", "#1d3f72", .55), "#1d3f72", 4.5),
    ("B dark muted / bg", "#a49c8e", "#1a1815", 4.5),
    # C
    ("C muted / bg", "#56606d", "#f2f4f7", 4.5),
    ("C accent chip / white", "#1b4f9c", "#ffffff", 4.5),
    ("C drawing ink / navy", "#e8f0fb", "#0f2d57", 4.5),
    ("C callout cyan / navy", "#7fd3ff", "#0f2d57", 4.5),
    ("C drawing faint label (55%)", blend("#e8f0fb", "#0f2d57", .55), "#0f2d57", 4.5),
    ("C key strip secondary / key bg", "#9fb4d3", "#0b2346", 4.5),
    ("C rail line (grey) / bg (non-text)", "#d6dbe2", "#f2f4f7", 3.0),
    ("C dark muted / surface", "#9aa6b2", "#151b23", 4.5),
    ("C dark accent / chip wash", "#78a9ff", "#18243a", 4.5),
    ("C dark drawing ink / panel", "#e8f0fb", "#0a1a33", 4.5),
]

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "r1"
    rows = R1 if which == "r1" else __import__("tokens2").R2
    print("| Pair | Colours | Ratio | Needs | Result |\n|---|---|---|---|---|")
    report(rows)
