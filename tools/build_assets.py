#!/usr/bin/env python3
"""Generate the animated SVGs used by the profile README.

Run:  python tools/build_assets.py   (writes into assets/)
Everything is pure SVG + CSS/SMIL, so it animates inside GitHub's <img> tags.
"""
import math
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


def header():
    W, H = 1200, 260
    cy, amp = 130, 46

    # DNA helix drawn once (with depth baked into size/opacity) and slid sideways by
    # exactly one wavelength: a single transform animation, so it stays smooth.
    x0, x1, wl = 760, 1120, 240
    pts = 12
    dots = []
    for i in range(int((x1 - x0 + wl) / wl * pts) + 2):
        x = x0 - wl + i * wl / pts
        ph = 2 * math.pi * i / pts
        dy, depth = amp * math.sin(ph), math.cos(ph)
        dots.append(f'<rect x="{x - .5:.1f}" y="{cy - abs(dy):.1f}" width="1" height="{2 * abs(dy):.1f}" fill="{MUTED}" opacity=".25"/>')
        for col, sy, dz in ((ACCENT, 1, depth), (TEXT, -1, -depth)):
            dots.append(f'<circle cx="{x:.1f}" cy="{cy + sy * dy:.1f}" r="{3.2 + dz * 1.2:.1f}" fill="{col}" opacity="{.6 + dz * .4:.2f}"/>')
    helix = (f'<g clip-path="url(#hc)"><g>{"".join(dots)}'
             f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{wl} 0" dur="4s" repeatCount="indefinite"/></g></g>')

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="helixo22 — arch, hyprland, python">
<defs>
  <style>
    text {{ font-family: {MONO}; font-size: 20px }}
  </style>
  <clipPath id="hc"><rect x="{x0 - 6}" y="0" width="{x1 - x0 + 12}" height="{H}"/></clipPath>
</defs>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{BG}" stroke="{EDGE}"/>
<text x="78" y="120" style="font-size:52px;font-weight:700;letter-spacing:-1px" fill="{TEXT}">helixo22</text>
<rect x="338" y="80" width="4" height="44" fill="{ACCENT}">
  <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/>
</rect>
<text x="80" y="168" fill="{MUTED}">arch · hyprland · python</text>
{helix}
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
  </style>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="14" fill="{BG}" stroke="{EDGE}" stroke-width="1.5"/>
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
