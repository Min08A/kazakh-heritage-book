"""Render the fully built illustration of every object into one contact sheet (for quick visual checks)."""
import sys
import numpy as np
from PIL import Image
import art

slugs = sys.argv[1:] or list(art.BUILDERS)
tiles = []
for s in slugs:
    sc = art.BUILDERS[s]()
    base = Image.new('RGBA', (art.W, art.H), (246, 239, 224, 255))
    for l in sc.layers:
        base.alpha_composite(l.img)
    tiles.append(base.convert('RGB'))
cols = 2 if len(tiles) > 1 else 1
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new('RGB', (cols * art.W, rows * art.H), (255, 255, 255))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * art.W, (i // cols) * art.H))
out = '/tmp/claude-0/preview.png' if False else '/home/claude/kazakh-heritage-book/tools/_preview.png'
sheet.save(out)
print(out, sheet.size)
