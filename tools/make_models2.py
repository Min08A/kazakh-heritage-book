"""Extra procedural models: dombra, kobyz, yurt, saukele (used as offline fallbacks / alternatives
to the Sketchfab embeds). No external assets. Run: python3 make_models2.py [slug ...] [--preview]"""
import math
import os
import sys

import numpy as np

import make_models as mm
from make_models import Model, lathe, sphere, tube, torus, box, xf, ring_loft, OUT

WOODL = (0.80, 0.55, 0.30)
WOODM = (0.62, 0.38, 0.20)
DARK = (0.12, 0.08, 0.06)
STRING = (0.93, 0.90, 0.80)
CREAMC = (0.95, 0.91, 0.80)
FELT = (0.94, 0.91, 0.82)
TEALC = (0.12, 0.50, 0.50)
RED = (0.55, 0.10, 0.16)
GOLDC = (0.80, 0.62, 0.24)
PEARL = (0.96, 0.94, 0.88)
CORAL = (0.85, 0.30, 0.25)
SAND = (0.86, 0.80, 0.66)


def merge(meshes):
    Vs, Fs, off = [], [], 0
    for V, F, _ in meshes:
        Vs.append(np.asarray(V, float))
        Fs.append(np.asarray(F, np.int64) + off)
        off += len(V)
    return np.vstack(Vs), np.vstack(Fs), True


def bead(pos, r, lat=6, lon=10):
    return xf(sphere(r, lat, lon), pos=pos)


def cyl(r, h, seg=24, y0=0.0):
    return lathe([(0.0005, y0), (r, y0), (r, y0 + h), (0.0005, y0 + h)], seg)


# ------------------------------------------------------------------ dombra
def dombra():
    m = Model('dombra')
    # pear-shaped body along Y, flattened in Z
    ys = np.linspace(0, 1.7, 36)

    def rad(y):
        t = y / 1.7
        return 0.66 * (math.sin(math.pi * min(1, t * 1.0) ** 0.85)) ** 0.7 + 0.12 * t * (1 - t) if t < 0.99 else 0.02

    prof = [(max(rad(y), 0.0005), y) for y in ys]
    prof[0] = (0.0005, 0.0)
    # keep the top rounded but wide enough to join the neck
    prof = [(max(r, 0.0005), y) for r, y in prof]
    prof[-1] = (0.16, 1.7)
    prof.append((0.0005, 1.7))
    m.add(lathe(prof, 56, scale=(1, 1, 0.34)), WOODL, 0.0, 0.55, name='body')
    # soundboard hole
    zf = lambda y: rad(y) * 0.34
    m.add(xf(cyl(0.15, 0.02, 32), rot=(90, 0, 0), pos=(0, 0.72, zf(0.72) - 0.004)), DARK, 0, 0.9, name='soundhole')
    # decorative ring around the hole
    m.add(xf(torus(0.18, 0.012, 40, 8), rot=(90, 0, 0), pos=(0, 0.72, zf(0.72) + 0.003)), GOLDC, 0.6, 0.35, name='ring')
    # neck + fretboard
    m.add(xf(box(0.17, 2.7, 0.13), pos=(0, 1.7 + 1.25, 0.0)), WOODM, 0, 0.6, name='neck')
    m.add(xf(box(0.19, 2.6, 0.03), pos=(0, 1.7 + 1.3, 0.08)), DARK, 0, 0.5, name='fingerboard')
    for k in range(9):
        y = 1.9 + k * 0.27
        m.add(xf(box(0.2, 0.012, 0.035), pos=(0, y, 0.095)), CREAMC, 0, 0.5, name='fret')
    # headstock + pegs
    m.add(xf(box(0.26, 0.5, 0.1), rot=(-14, 0, 0), pos=(0, 4.55, -0.04)), WOODM, 0, 0.6, name='head')
    for sx in (-1, 1):
        m.add(xf(cyl(0.035, 0.3, 12), rot=(0, 0, 90), pos=(sx * 0.2, 4.5, -0.02)), DARK, 0, 0.5, name='peg')
        m.add(xf(sphere(0.07, 8, 12, scale=(1.4, 1, 0.6)), pos=(sx * 0.38, 4.5, -0.02)), WOODM, 0, 0.5, name='pegknob')
    # strings + bridge
    m.add(xf(box(0.34, 0.05, 0.07), pos=(0, 0.28, zf(0.28) + 0.03)), DARK, 0, 0.5, name='bridge')
    for sx in (-0.045, 0.045):
        m.add(tube([(sx, 0.3, zf(0.3) + 0.075), (sx, 2.0, 0.13), (sx, 4.35, 0.07)], 0.007, 6), STRING, 0.2, 0.4, name='string')
    return m


# ------------------------------------------------------------------ kobyz
def kobyz():
    m = Model('kobyz')
    th = np.linspace(0, math.pi * 0.5, 24)
    # deep rounded bowl body, open end up covered by a lid
    prof = [(0.0005, 0.0)] + [(0.62 * math.sin(t), 0.62 - 0.62 * math.cos(t)) for t in th[1:]]
    prof += [(0.62 - 0.12 * k / 8, 0.62 + 0.55 * k / 8) for k in range(1, 9)]
    m.add(lathe(prof, 56, scale=(1, 1, 0.85)), WOODM, 0, 0.6, name='body')
    top = prof[-1][1]
    m.add(cyl(prof[-1][0] * 1.0, 0.03, 48, top), CREAMC, 0, 0.9, name='lid')
    m.add(xf(torus(prof[-1][0], 0.025, 48, 8), pos=(0, top, 0), scale=(1, 1, 0.85)), GOLDC, 0.5, 0.4, name='rim')
    # soundholes in the lid
    for sx in (-0.2, 0.2):
        m.add(xf(cyl(0.07, 0.034, 20, top), pos=(sx, 0.0005, 0.0)), DARK, 0, 0.9, name='hole')
    # neck rising from the body
    m.add(xf(box(0.2, 2.9, 0.18), pos=(0, top + 1.3, 0)), WOODM, 0, 0.6, name='neck')
    # curved headstock (horse-head style)
    m.add(tube([(0, top + 2.6, 0), (0, top + 3.0, 0.08), (0, top + 3.2, 0.3), (0, top + 3.05, 0.5)], 0.11, 10, taper=lambda t: 1 - 0.35 * t), WOODM, 0, 0.6, name='scroll')
    for sx in (-1, 1):
        m.add(xf(cyl(0.035, 0.34, 12), rot=(0, 0, 90), pos=(sx * 0.2, top + 2.75, 0)), DARK, 0, 0.5, name='peg')
        m.add(xf(sphere(0.08, 8, 12, scale=(1.4, 1, 0.7)), pos=(sx * 0.4, top + 2.75, 0)), WOODM, 0, 0.5, name='pegknob')
    # horsehair strings and bridge
    m.add(xf(box(0.3, 0.05, 0.05), pos=(0, top + 0.18, 0.12)), DARK, 0, 0.5, name='bridge')
    for sx in (-0.05, 0.05):
        m.add(tube([(sx, top + 0.15, 0.15), (sx, top + 1.4, 0.11), (sx, top + 2.7, 0.06)], 0.009, 6), STRING, 0.0, 0.7, name='string')
    # bow lying beside
    arc = [(-1.5 + 0.05 * math.sin(math.pi * k / 20), 0.1 + 0.15 * k / 20 * 6.0 * 0.5, 0.0) for k in range(21)]
    arc = [(-1.4 + 0.18 * math.sin(math.pi * k / 20), 0.0 + 3.0 * k / 20, 0.3) for k in range(21)]
    m.add(tube(arc, 0.025, 8), WOODM, 0, 0.6, name='bow')
    m.add(tube([(-1.4, 0.0, 0.3), (-1.4, 3.0, 0.3)], 0.011, 6), STRING, 0, 0.8, name='hair')
    return m


# ------------------------------------------------------------------ yurt
def yurt():
    m = Model('yurt')
    m.add(cyl(2.15, 0.04, 64), SAND, 0, 0.95, name='ground')
    # wall (felt)
    wall = ring_loft([0.04, 1.2], [1.62, 1.62], [1.62, 1.62], seg=72)
    m.add(wall, FELT, 0, 0.95, double=True, name='wall')
    # dome roof
    prof = [(1.7, 1.15), (1.62, 1.3), (1.38, 1.62), (1.0, 1.95), (0.62, 2.2), (0.36, 2.32), (0.3, 2.34)]
    ang = 72
    roof = lathe(prof, ang)
    m.add(roof, FELT, 0, 0.95, double=True, name='roof')
    # ropes (tubes as tori) around walls
    for y, c in ((0.55, TEALC), (1.1, TEALC)):
        m.add(xf(torus(1.645, 0.035, 72, 8), pos=(0, y, 0)), c, 0, 0.7, name='band')
    # turquoise ornament belt
    m.add(ring_loft([0.8, 0.95], [1.63, 1.63], [1.63, 1.63], seg=72), TEALC, 0, 0.8, double=True, name='belt')
    # shanyrak crown ring + spokes
    m.add(xf(torus(0.3, 0.05, 40, 10), pos=(0, 2.34, 0)), WOODM, 0, 0.6, name='crown')
    for k in range(3):
        a = k * 60
        m.add(xf(box(0.62, 0.035, 0.035), rot=(0, a, 0), pos=(0, 2.34, 0)), WOODM, 0, 0.6, name='spoke')
    # roof ribs (uyk)
    for k in range(24):
        a = 2 * math.pi * k / 24
        pts = [(1.7 * math.cos(a), 1.15, 1.7 * math.sin(a)), (1.38 * math.cos(a), 1.65, 1.38 * math.sin(a)), (1.0 * math.cos(a), 1.99, 1.0 * math.sin(a)), (0.34 * math.cos(a), 2.36, 0.34 * math.sin(a))]
        m.add(tube(pts, 0.014, 5), WOODM, 0, 0.7, name='rib')
    # door on +Z
    m.add(xf(box(0.62, 0.95, 0.07), pos=(0, 0.52, 1.64)), WOODM, 0, 0.6, name='door')
    m.add(xf(box(0.78, 1.08, 0.04), pos=(0, 0.58, 1.62)), TEALC, 0, 0.6, name='doorframe')
    m.add(xf(box(0.12, 0.12, 0.03), rot=(0, 0, 45), pos=(0, 0.74, 1.69)), GOLDC, 0.5, 0.4, name='doororn')
    return m


# ------------------------------------------------------------------ saukele
def saukele():
    m = Model('saukele')
    # velvet base band
    base = lathe([(0.0005, 0.0), (0.85, 0.0), (0.88, 0.08), (0.88, 0.42), (0.80, 0.5), (0.0005, 0.5)], 64)
    m.add(base, RED, 0, 0.85, name='base')
    # tall cone
    prof = [(0.74, 0.5), (0.62, 0.9), (0.5, 1.4), (0.38, 1.9), (0.26, 2.35), (0.16, 2.7), (0.08, 2.95), (0.0005, 3.05)]
    m.add(lathe(prof, 64), RED, 0, 0.85, name='cone')
    # gold bands
    for r, y in ((0.89, 0.07), (0.89, 0.42), (0.66, 0.78), (0.52, 1.3), (0.39, 1.8), (0.27, 2.28)):
        m.add(xf(torus(r, 0.03, 60, 8), pos=(0, y, 0)), GOLDC, 0.8, 0.3, name='band')
    # pearls/beads around the base
    pearls = [bead((0.9 * math.cos(2 * math.pi * k / 28), 0.25, 0.9 * math.sin(2 * math.pi * k / 28)), 0.055) for k in range(28)]
    m.add(merge(pearls), PEARL, 0.1, 0.25, name='pearls')
    corals = [bead((0.9 * math.cos(2 * math.pi * (k + .5) / 28), 0.25, 0.9 * math.sin(2 * math.pi * (k + .5) / 28)), 0.04) for k in range(28)]
    m.add(merge(corals), CORAL, 0.0, 0.4, name='corals')
    # gold plates on the cone
    plates = []
    for lvl, (r, y) in enumerate(((0.66, 0.8), (0.52, 1.3), (0.39, 1.8))):
        n = 8 - lvl * 2
        for k in range(n):
            a = 2 * math.pi * k / n + lvl * 0.2
            plates.append(xf(sphere(0.09 - lvl * 0.012, 8, 12, scale=(1, 1.3, 0.35)), rot=(0, -math.degrees(a) + 90, 0), pos=(r * 1.02 * math.cos(a), y + 0.3, r * 1.02 * math.sin(a))))
    m.add(merge(plates), GOLDC, 0.8, 0.3, name='plates')
    # turquoise stones
    stones = []
    for lvl, (r, y) in enumerate(((0.66, 0.8), (0.52, 1.3), (0.39, 1.8))):
        n = 8 - lvl * 2
        for k in range(n):
            a = 2 * math.pi * k / n + lvl * 0.2
            stones.append(bead((r * 1.1 * math.cos(a), y + 0.3, r * 1.1 * math.sin(a)), 0.03 - lvl * 0.004))
    m.add(merge(stones), TEALC, 0.0, 0.35, name='stones')
    # crest: gold sphere and feather tuft
    m.add(bead((0, 3.1, 0), 0.07), GOLDC, 0.8, 0.3, name='finial')
    m.add(tube([(0, 3.1, 0), (0.03, 3.4, 0), (0.1, 3.65, 0)], 0.02, 6, taper=lambda t: 1 - 0.6 * t), CREAMC, 0, 0.7, name='feather')
    # pendants (temple strands)
    pend = []
    pcol = []
    for sx in (-1, 1):
        for s, off in enumerate((-0.28, 0.0, 0.28)):
            for k in range(9):
                pend.append(bead((sx * (0.93 + 0.02 * s), 0.4 - 0.12 * k - 0.0, off), 0.045 - 0.002 * (k % 2)))
    m.add(merge(pend), PEARL, 0.1, 0.3, name='pendants')
    drops = [bead((sx * (0.93 + 0.02 * s), 0.4 - 0.12 * 9, off), 0.07) for sx in (-1, 1) for s, off in enumerate((-0.28, 0.0, 0.28))]
    m.add(merge(drops), CORAL, 0, 0.4, name='drops')
    return m


BUILD = {'dombra': dombra, 'kobyz': kobyz, 'yurt': yurt, 'saukele': saukele}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sheet = []
    for n in args or list(BUILD):
        mdl = BUILD[n]()
        path = os.path.join(OUT, f'{n}.glb')
        mdl.write(path)
        print(n, os.path.getsize(path) // 1024, 'KB', sum(len(p['F']) for p in mdl.parts), 'triangles')
        if '--preview' in sys.argv:
            sheet.append(np.hstack([mm.render_preview(mdl, 440, 35, 18), mm.render_preview(mdl, 440, 150, 12)]))
    if sheet:
        import cv2
        cv2.imwrite(os.path.join(os.path.dirname(__file__), '_models2.png'), np.vstack(sheet))
