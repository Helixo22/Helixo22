#!/usr/bin/env python3
"""Generate the animated SVGs used by the profile README.

Run:  python tools/build_assets.py   (writes into assets/)
Everything is pure SVG + CSS/SMIL, so it animates inside GitHub's <img> tags.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

BG = "#0d1117"
EDGE = "#21262d"
TEXT = "#e6edf3"
MUTED = "#7d8590"
ACCENT = "#a78bfa"

MONO = "'JetBrains Mono','Fira Code','SFMono-Regular',Menlo,Consolas,'DejaVu Sans Mono',monospace"
NO_MOTION = "@media (prefers-reduced-motion: reduce) { * { animation: none !important } }"


def header():
    W, H = 1200, 260
    cy, amp = 130, 46

    # DNA helix: dots bob with ease-in-out (≈ sine); depth is faked with a scale
    # animation offset by a quarter period.
    n, x0, x1 = 22, 760, 1120
    dur, twists = 1.8, 1.4
    full = dur * 2
    dots = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / (n - 1)
        d = -(i * twists / n) * full
        dq = d + dur / 2
        dots.append(f'<rect class="r" x="{x - .5:.1f}" y="{cy - amp}" width="1" height="{amp * 2}" '
                    f'style="animation-delay:{d:.3f}s"/>')
        for col, direction in ((ACCENT, "alternate"), (TEXT, "alternate-reverse")):
            dots.append(
                f'<g class="b" style="animation-delay:{d:.3f}s;animation-direction:{direction}">'
                f'<circle class="d" cx="{x:.1f}" cy="{cy}" r="4" fill="{col}" '
                f'style="animation-delay:{dq:.3f}s;animation-direction:{direction}"/></g>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="helixo22 — arch, hyprland, python">
<defs>
  <style>
    text {{ font-family: {MONO}; font-size: 20px }}
    @keyframes hy {{ from {{ transform: translateY(-{amp}px) }} to {{ transform: translateY({amp}px) }} }}
    @keyframes dp {{ from {{ transform: scale(.5); opacity:.3 }} to {{ transform: scale(1.1); opacity:1 }} }}
    @keyframes rg {{ from {{ transform: scaleY(1) }} to {{ transform: scaleY(-1) }} }}
    .b {{ animation: hy {dur}s ease-in-out infinite alternate }}
    .d {{ transform-box: fill-box; transform-origin: center; animation: dp {dur}s ease-in-out infinite alternate }}
    .r {{ fill: {MUTED}; opacity: .25; transform-box: fill-box; transform-origin: center; animation: rg {dur}s ease-in-out infinite alternate }}
    {NO_MOTION}
  </style>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{EDGE}"/>
<text x="78" y="120" style="font-size:52px;font-weight:700;letter-spacing:-1px" fill="{TEXT}">helixo22</text>
<rect x="338" y="80" width="4" height="44" fill="{ACCENT}">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
</rect>
<text x="80" y="168" fill="{MUTED}">arch · hyprland · python</text>
{''.join(dots)}
</svg>"""
    (OUT / "header.svg").write_text(svg)


def card(fname, name, desc_lines, lang):
    W, H = 560, 132
    desc = "".join(f'<text x="32" y="{80 + i * 24}" fill="{MUTED}">{escape(l)}</text>'
                   for i, l in enumerate(desc_lines))
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{name}">
<defs>
  <style>
    text {{ font-family: {MONO}; font-size: 15px }}
    @keyframes run {{ to {{ stroke-dashoffset: -100 }} }}
    .run {{ animation: run 6s linear infinite }}
    {NO_MOTION}
  </style>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{EDGE}" stroke-width="1.5"/>
<rect class="run" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="none" stroke="{ACCENT}" stroke-width="1.5" pathLength="100" stroke-dasharray="12 88" stroke-linecap="round"/>
<text x="32" y="50" style="font-size:22px;font-weight:700" fill="{TEXT}">{name}</text>
{desc}
<circle cx="38" cy="104" r="5" fill="{ACCENT}"/>
<text x="52" y="109" style="font-size:14px" fill="{MUTED}">{lang}</text>
</svg>"""
    (OUT / fname).write_text(svg)


if __name__ == "__main__":
    header()
    card("card-wp-penguin.svg", "wp-penguin",
["wallpaper engine on hyprland"], "Python")
    card("card-debt-clock.svg", "debt-clock",
["public debt & yield curves"], "Python")
    print("assets written to", OUT)
