"""Generates the dot-matrix profile banner (dark + light) as self-contained SVGs.
Usage: python3 scripts/banner.py assets
"""
import sys
from pathlib import Path

GLYPHS = {
    'E': ['11111', '10000', '10000', '11110', '10000', '10000', '11111'],
    'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
    'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
    'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
    'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
    'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
    'V': ['10001', '10001', '10001', '10001', '10001', '01010', '00100'],
    'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'],
    'M': ['10001', '11011', '10101', '10101', '10001', '10001', '10001'],
    'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
    'I': ['11111', '00100', '00100', '00100', '00100', '00100', '11111'],
    ' ': ['00000'] * 7,
}

NAME = 'ERNESTO VERAMENDI'
ACCENT_LETTERS = {0, 8}  # E and V, like the portfolio's original accent
W, H = 1200, 240
CELL = 10
R_ON, R_OFF = 3.8, 1.3

THEMES = {
    'dark': {'bg': '#000000', 'on': '#f2f2f2', 'off': '#2a2a2a', 'accent': '#ff2b2b', 'sub': '#a1a1a8'},
    'light': {'bg': '#f5f5f5', 'on': '#111111', 'off': '#d4d4d4', 'accent': '#e60012', 'sub': '#4b4b4f'},
}


def build(theme: dict) -> str:
    cols = len(NAME) * 6 - 1
    x0 = (W - cols * CELL) / 2
    y0 = 50
    dots_off, dots_on = [], []
    n = 0
    for ci, ch in enumerate(NAME):
        for row, bits in enumerate(GLYPHS[ch]):
            for col, bit in enumerate(bits):
                cx = x0 + (ci * 6 + col) * CELL + CELL / 2
                cy = y0 + row * CELL + CELL / 2
                if bit == '1':
                    color = theme['accent'] if ci in ACCENT_LETTERS else theme['on']
                    delay = (n * 37) % 90 * 0.012  # scrambled LED order
                    dots_on.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{R_ON}" fill="{color}" style="animation-delay:{delay:.3f}s"/>')
                    n += 1
                else:
                    dots_off.append(f'<circle cx="{cx:g}" cy="{cy:g}" r="{R_OFF}"/>')
    sub_y = y0 + 7 * CELL + 48
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="t">
<title id="t">Ernesto Veramendi, desarrollador full-stack y diseñador de interfaces</title>
<style>
  .on circle {{ animation: led 0.6s steps(3, end) both; }}
  .pulse {{ animation: pulse 2.4s ease-in-out infinite; }}
  @keyframes led {{ 0% {{ opacity: 0; }} 50% {{ opacity: 1; }} 75% {{ opacity: 0.35; }} 100% {{ opacity: 1; }} }}
  @keyframes pulse {{ 50% {{ opacity: 0.25; }} }}
  @media (prefers-reduced-motion: reduce) {{ .on circle, .pulse {{ animation: none; }} }}
</style>
<rect width="{W}" height="{H}" rx="24" fill="{theme['bg']}"/>
<g fill="{theme['off']}">{''.join(dots_off)}</g>
<g class="on">{''.join(dots_on)}</g>
<circle class="pulse" cx="{W - 48}" cy="44" r="7" fill="{theme['accent']}"/>
<text x="{W / 2:g}" y="{sub_y}" text-anchor="middle" fill="{theme['sub']}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" font-size="22" letter-spacing="1">Desarrollador full-stack y diseñador de interfaces</text>
</svg>
'''


out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
for name, theme in THEMES.items():
    svg = build(theme)
    assert svg.count('<circle') > 300, 'banner lost its dots'
    (out / f'banner-{name}.svg').write_text(svg, encoding='utf-8')
    print(name, len(svg) // 1024, 'KB')
