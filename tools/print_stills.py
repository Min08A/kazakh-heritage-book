"""High-resolution still illustrations for the printable book (print/images/<slug>.png).

The video scenes are drawn at 2x and normally downscaled; here every layer keeps its 2x size
(1440x1280), and all layers, including the labels, are composited into one finished picture.
Run: python3 print_stills.py [slug ...]
"""
import os
import sys

from PIL import Image, ImageDraw

import art
import art2

# keep the 2x drawing instead of downscaling it
art.Cv.out = lambda self: self.img

BUILDERS = dict(art.BUILDERS)
BUILDERS.update(art2.BUILDERS2)
OUT = os.path.join(os.path.dirname(__file__), '..', 'print', 'images')


def still(slug):
    sc = BUILDERS[slug]()
    W, H = art.W * art.S, art.H * art.S
    base = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(base)
    r = int(min(W, H) * 0.47)
    cx, cy = W // 2, H // 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(238, 226, 200, 255))
    d.ellipse([cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18], outline=art.GOLD, width=4)
    for layer in sc.layers:
        base.alpha_composite(layer.img)
    return base


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for s in sys.argv[1:] or list(BUILDERS):
        p = os.path.join(OUT, f'{s}.png')
        still(s).save(p, optimize=True)
        print(s, os.path.getsize(p) // 1024, 'KB')
