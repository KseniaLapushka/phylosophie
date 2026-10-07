#!/usr/bin/env python3
"""Генерирует фавиконку сайта: круг с заливкой и буква «Ф».

  python3 tools/make_favicon.py

Пишет docs/assets/favicon.svg (исходник) и docs/assets/favicon.png (его
использует mkdocs.yml: PNG открывается во всех браузерах). Буква нарисована
линиями, а не шрифтом, поэтому выглядит одинаково везде. Круг залит сам,
а не прозрачный — поэтому читается и на светлой, и на тёмной панели вкладок.
Цвета меняются в двух константах ниже.
"""
from pathlib import Path
from PIL import Image, ImageDraw

FILL = '#c15f3c'      # цвет круга (тёплый терракотовый, середина по яркости)
LETTER = '#faf9f5'    # цвет буквы (кремовый, как фон сайта)

# Геометрия в сетке 64x64: (x1, y1, x2, y2) для линий, bbox для овала
STROKE = 6.4
STEM = (32, 11, 32, 53)
SERIFS = [(24, 11, 40, 11), (24, 53, 40, 53)]
BOWL = (17, 20, 47, 44)   # овал вокруг стойки

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'assets'


def svg() -> str:
    lines = ''.join(
        f'<line x1="{a}" y1="{b}" x2="{c}" y2="{d}"/>' for a, b, c, d in [STEM, *SERIFS])
    cx, cy = (BOWL[0] + BOWL[2]) / 2, (BOWL[1] + BOWL[3]) / 2
    rx, ry = (BOWL[2] - BOWL[0]) / 2, (BOWL[3] - BOWL[1]) / 2
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        f'<circle cx="32" cy="32" r="31" fill="{FILL}"/>'
        f'<g fill="none" stroke="{LETTER}" stroke-width="{STROKE}" stroke-linecap="round">'
        f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/>{lines}</g></svg>\n')


def png(size: int = 256, ss: int = 8) -> Image.Image:
    k = size * ss / 64
    im = Image.new('RGBA', (size * ss, size * ss), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse((1 * k, 1 * k, 63 * k, 63 * k), fill=FILL)
    w = STROKE * k
    d.ellipse([c * k for c in BOWL], outline=LETTER, width=round(w))
    for a, b, c, e in [STEM, *SERIFS]:
        d.line((a * k, b * k, c * k, e * k), fill=LETTER, width=round(w))
        for x, y in ((a, b), (c, e)):  # круглые концы, как stroke-linecap="round"
            r = w / 2
            d.ellipse((x * k - r, y * k - r, x * k + r, y * k + r), fill=LETTER)
    return im.resize((size, size), Image.LANCZOS)


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'favicon.svg').write_text(svg(), encoding='utf-8')
    png().save(OUT / 'favicon.png')
    print('OK:', OUT)
