"""Procedural simplified models (GLB) for the 26 chapters added in the two-part edition.
Used as the 3D model when no Sketchfab model fits, and as an offline fallback otherwise.
No external assets. Run: python3 make_models3.py [slug ...] [--preview]
"""
import math
import os
import sys

import numpy as np

import make_models as mm
import make_models2 as m2
from make_models import Model, lathe, sphere, tube, torus, box, xf, ring_loft, extrude, OUT

# ------------------------------------------------------------------ palette
WOOD = (0.76, 0.52, 0.30)
WOODL = (0.84, 0.62, 0.38)
WOODD = (0.46, 0.29, 0.16)
LEATHER = (0.56, 0.34, 0.19)
LEATHERD = (0.38, 0.22, 0.12)
GOLD = (0.80, 0.62, 0.24)
SILVER = (0.82, 0.83, 0.86)
IRON = (0.30, 0.31, 0.33)
TEAL = (0.12, 0.47, 0.46)
TURQ = (0.18, 0.62, 0.60)
RED = (0.62, 0.14, 0.17)
REDL = (0.78, 0.30, 0.26)
CREAM = (0.95, 0.91, 0.80)
MILK = (0.97, 0.96, 0.92)
FELT = (0.94, 0.91, 0.82)
BRICK = (0.80, 0.56, 0.38)
BRICKD = (0.66, 0.42, 0.27)
CLAY = (0.78, 0.66, 0.50)
GRASS = (0.42, 0.62, 0.30)
GRASSD = (0.32, 0.50, 0.24)
WATER = (0.36, 0.62, 0.78)
SNOW = (0.95, 0.96, 0.98)
SAND = (0.86, 0.80, 0.66)
CAMEL = (0.74, 0.56, 0.36)
CAMELD = (0.58, 0.42, 0.26)
HORSE = (0.48, 0.28, 0.16)
HORSED = (0.20, 0.12, 0.08)
GLASS = (0.72, 0.84, 0.86)
STONE = (0.62, 0.60, 0.56)
BAURSAK = (0.83, 0.58, 0.27)
SKIN = (0.93, 0.78, 0.66)


def cyl(r, h, seg=32, y0=0.0):
    return lathe([(0.0005, y0), (r, y0), (r, y0 + h), (0.0005, y0 + h)], seg)


def bowl_profile(r, h, wall=0.04, foot=0.35):
    """Open bowl: outside then inside surface, as a lathe profile."""
    pts = [(0.0005, 0.0), (r * foot, 0.0), (r * foot, 0.04)]
    for t in np.linspace(0.1, 1.0, 10):
        pts.append((r * (foot + (1 - foot) * math.sin(t * math.pi / 2)), h * t))
    pts.append((r - wall, h))
    for t in np.linspace(1.0, 0.1, 8):
        pts.append(((r - wall) * (foot + (1 - foot) * math.sin(t * math.pi / 2)) * 0.98, max(h * t - wall * 0.5, 0.06)))
    pts.append((0.0005, 0.06))
    return pts


def embed(dst, src, rot=(0, 0, 0), pos=(0, 0, 0), scale=(1, 1, 1)):
    """Copy all parts of another Model into dst with a transform."""
    for p in src.parts:
        mesh = xf((p['V'].astype(float), p['F'].astype(np.int64), True), rot=rot, pos=pos, scale=scale)
        dst.add(mesh, p['color'], p['metal'], p['rough'], p['double'], p['name'])


def diamond(w, h, t):
    return extrude([(0, h / 2), (w / 2, 0), (0, -h / 2), (-w / 2, 0)], t)


def legs4(m, pts, r, color, name='leg'):
    for a, b in pts:
        m.add(tube([a, b], r, 10), color, 0, 0.8, name=name)


# ------------------------------------------------------------------ animals
def camel(m, pos=(0, 0, 0), yaw=0, color=CAMEL, load=None):
    """A simple two-humped camel facing +X. `load` is a callback(m, T) to add cargo."""
    def T(mesh):
        return xf(mesh, rot=(0, yaw, 0), pos=pos)
    m.add(T(xf(sphere(0.62, 14, 22), pos=(0, 1.55, 0), scale=(1.25, 0.62, 0.62))), color, 0, 0.85, name='camel-body')
    for x in (-0.38, 0.32):
        m.add(T(xf(sphere(0.26, 10, 16), pos=(x, 1.95, 0), scale=(1, 1.1, 0.9))), color, 0, 0.85, name='hump')
    neck = [(0.7, 1.6, 0), (1.0, 1.55, 0), (1.18, 1.85, 0), (1.25, 2.2, 0)]
    m.add(T(tube(neck, 0.15, 12, taper=lambda t: 1.15 - 0.3 * t)), color, 0, 0.85, name='neck')
    m.add(T(xf(sphere(0.17, 10, 14), pos=(1.38, 2.28, 0), scale=(1.5, 0.85, 0.8))), color, 0, 0.85, name='head')
    for s in (-1, 1):
        m.add(T(xf(sphere(0.04, 6, 8), pos=(1.25, 2.4, s * 0.09))), CAMELD, 0, 0.8, name='ear')
    for x in (-0.55, 0.5):
        for z in (-0.22, 0.22):
            m.add(T(tube([(x, 1.35, z), (x + 0.04, 0.75, z), (x, 0.06, z)], 0.075, 8)), CAMELD, 0, 0.85, name='leg')
            m.add(T(xf(sphere(0.1, 8, 10), pos=(x, 0.05, z), scale=(1.3, 0.5, 1.1))), CAMELD, 0, 0.85, name='foot')
    m.add(T(tube([(-0.74, 1.6, 0), (-0.86, 1.3, 0), (-0.82, 1.05, 0)], 0.035, 6)), CAMELD, 0, 0.85, name='tail')
    if load:
        load(m, T)


def horse(m, pos=(0, 0, 0), yaw=0, color=HORSE, gallop=False, saddle=True):
    def T(mesh):
        return xf(mesh, rot=(0, yaw, 0), pos=pos)
    m.add(T(xf(sphere(0.5, 14, 22), pos=(0, 1.25, 0), scale=(1.45, 0.62, 0.55))), color, 0, 0.6, name='horse-body')
    neck = [(0.55, 1.35, 0), (0.78, 1.6, 0), (0.92, 1.9, 0)]
    m.add(T(tube(neck, 0.17, 12, taper=lambda t: 1.1 - 0.35 * t)), color, 0, 0.6, name='neck')
    m.add(T(xf(sphere(0.16, 10, 14), pos=(1.08, 1.86, 0), rot=(0, 0, -35), scale=(1.75, 0.72, 0.68))), color, 0, 0.6, name='head')
    for s in (-1, 1):
        m.add(T(xf(sphere(0.035, 6, 8), pos=(0.95, 2.06, s * 0.06), scale=(1, 2, 1))), color, 0, 0.6, name='ear')
    mane = [(0.5, 1.55, 0), (0.72, 1.82, 0), (0.92, 2.04, 0)]
    m.add(T(tube(mane, 0.06, 8)), HORSED, 0, 0.8, name='mane')
    if gallop:
        legs = [((0.5, 1.05, 0.14), (0.95, 0.75, 0.14), (1.05, 0.35, 0.14)), ((0.5, 1.05, -0.14), (0.75, 0.55, -0.14), (0.55, 0.2, -0.14)),
                ((-0.5, 1.05, 0.14), (-0.85, 0.65, 0.14), (-1.2, 0.5, 0.14)), ((-0.5, 1.05, -0.14), (-0.55, 0.55, -0.14), (-0.35, 0.15, -0.14))]
    else:
        legs = [((x, 1.05, z), (x + 0.03, 0.55, z), (x, 0.04, z)) for x in (0.48, -0.48) for z in (-0.14, 0.14)]
    for lg in legs:
        m.add(T(tube(list(lg), 0.06, 8)), color, 0, 0.6, name='leg')
        m.add(T(xf(sphere(0.07, 6, 8), pos=lg[-1], scale=(1.1, 0.7, 1))), HORSED, 0, 0.7, name='hoof')
    tail = [(-0.7, 1.35, 0), (-0.95, 1.2, 0), (-1.1, 0.85, 0)] if not gallop else [(-0.7, 1.35, 0), (-1.0, 1.35, 0), (-1.3, 1.2, 0)]
    m.add(T(tube(tail, 0.07, 8, taper=lambda t: 1 - 0.5 * t)), HORSED, 0, 0.8, name='tail')
    if saddle:
        m.add(T(xf(sphere(0.3, 10, 16), pos=(0.0, 1.62, 0), scale=(1.1, 0.35, 0.95))), RED, 0, 0.7, name='saddle-cloth')
        m.add(T(xf(sphere(0.2, 10, 14), pos=(0.02, 1.72, 0), scale=(1.2, 0.45, 0.9))), LEATHERD, 0, 0.6, name='saddle')
        m.add(T(xf(box(0.06, 0.2, 0.06), pos=(0.24, 1.82, 0))), GOLD, 0.4, 0.4, name='pommel')


# ------------------------------------------------------------------ PART 1
def khan_shatyr():
    m = Model('khan-shatyr')
    m.add(cyl(2.6, 0.05, 72), (0.80, 0.82, 0.80), 0, 0.9, name='plaza')
    # elliptical tent: lathe with concave sides, flattened in Z
    prof = [(1.9, 0.05)]
    for t in np.linspace(0.05, 1, 22):
        prof.append((1.9 * (1 - t) ** 1.9 + 0.06, 0.05 + 3.3 * t))
    prof.append((0.0005, 3.36))
    m.add(lathe(prof, 72, scale=(1, 1, 0.78)), GLASS, 0.1, 0.25, double=True, name='roof')
    # cable net: meridians and rings
    for k in range(36):
        a = 2 * math.pi * k / 36
        pts = [((1.9 * (1 - t) ** 1.9 + 0.065) * math.cos(a), 0.05 + 3.3 * t, (1.9 * (1 - t) ** 1.9 + 0.065) * math.sin(a) * 0.78) for t in np.linspace(0, 1, 24)]
        m.add(tube(pts, 0.008, 4), (0.9, 0.9, 0.88), 0.3, 0.5, name='cable')
    for t in (0.08, 0.18, 0.3, 0.45, 0.62):
        r = 1.9 * (1 - t) ** 1.9 + 0.07
        m.add(xf(torus(r, 0.008, 72, 4), pos=(0, 0.05 + 3.3 * t, 0), scale=(1, 1, 0.78)), (0.9, 0.9, 0.88), 0.3, 0.5, name='ring')
    # mast with a slight tilt, like the real building
    m.add(tube([(0, 3.25, 0), (-0.12, 4.4, 0)], 0.035, 10, taper=lambda t: 1 - 0.7 * t), (0.85, 0.85, 0.85), 0.6, 0.35, name='mast')
    # base ring building and entrance
    m.add(ring_loft([0.05, 0.35], [1.95, 1.95], [1.52, 1.52], 72), (0.92, 0.9, 0.84), 0, 0.6, double=True, name='base')
    m.add(xf(box(0.7, 0.32, 0.25), pos=(0, 0.21, 1.55)), (0.35, 0.42, 0.46), 0.2, 0.4, name='entrance')
    for k in range(10):
        a = 2 * math.pi * k / 10
        m.add(xf(sphere(0.12, 8, 10), pos=(2.3 * math.cos(a), 0.15, 2.3 * math.sin(a) * 0.9)), GRASSD, 0, 0.9, name='tree')
    return m


def kyz_zhibek():
    m = Model('kyz-zhibek')
    # girl's takiya: soft dome cap of red velvet with gold embroidery and an owl-feather tuft (uki)
    prof = [(0.0005, 1.05), (0.25, 1.03), (0.5, 0.96), (0.7, 0.82), (0.82, 0.62), (0.88, 0.4), (0.9, 0.2), (0.9, 0.0)]
    m.add(lathe(prof[::-1], 64), RED, 0, 0.85, double=True, name='cap')
    m.add(ring_loft([0.0, 0.22], [0.915, 0.915], [0.915, 0.915], 64), GOLD, 0.6, 0.35, double=True, name='band')
    for k in range(16):
        a = 2 * math.pi * k / 16
        m.add(xf(diamond(0.1, 0.13, 0.02), rot=(0, -math.degrees(a) + 90, 0), pos=(0.93 * math.cos(a), 0.11, 0.93 * math.sin(a))), RED, 0, 0.6, name='band-orn')
    for k in range(8):
        a = 2 * math.pi * k / 8
        pts = [(0.86 * math.cos(a) * math.sin(t) / math.sin(1.35), 0.35 + 0.66 * (1 - (t / 1.35) ** 2) ** 0.6, 0.86 * math.sin(a) * math.sin(t) / math.sin(1.35)) for t in np.linspace(0.1, 1.33, 16)]
        m.add(tube(pts, 0.018, 6), GOLD, 0.6, 0.35, name='seam')
    for k in range(24):
        a = 2 * math.pi * k / 24
        m.add(xf(sphere(0.03, 6, 8), pos=(0.9 * math.cos(a), -0.02, 0.9 * math.sin(a))), MILK, 0.1, 0.3, name='pearl')
    m.add(xf(sphere(0.08, 10, 12), pos=(0, 1.08, 0)), GOLD, 0.6, 0.3, name='top-bead')
    rng = np.random.RandomState(3)
    for k in range(11):
        a = 2 * math.pi * k / 11
        tilt = 0.25 + 0.2 * rng.rand()
        pts = [(0.02 * math.cos(a) + tilt * math.cos(a) * t ** 1.4, 1.1 + 0.9 * t, 0.02 * math.sin(a) + tilt * math.sin(a) * t ** 1.4) for t in np.linspace(0, 1, 10)]
        col = (0.93, 0.92, 0.88) if k % 3 else (0.55, 0.50, 0.44)
        m.add(tube(pts, 0.045, 6, taper=lambda t: 0.5 + 0.8 * math.sin(math.pi * min(t, 0.999)) ** 0.7), col, 0, 0.9, name='feather')
    for s in (-1, 1):
        for k in range(5):
            m.add(xf(sphere(0.035, 6, 8), pos=(s * 0.92, -0.08 - 0.1 * k, 0.15)), CREAM if k % 2 else REDL, 0.1, 0.4, name='pendant')
    return m


def mausoleum_base(m, w, h, color, tile):
    m.add(xf(box(w, h, w), pos=(0, h / 2 + 0.08, 0)), color, 0, 0.85, name='walls')
    m.add(xf(box(w + 0.3, 0.08, w + 0.3), pos=(0, 0.04, 0)), STONE, 0, 0.9, name='plinth')
    # carved tile pattern: rows of small diamonds on every face
    for face in range(4):
        yaw = face * 90
        for i in range(-4, 5):
            for j in range(6):
                x = i * w / 10
                y = 0.35 + j * (h - 0.6) / 6
                if abs(x) < w * 0.22 and face == 0:
                    continue
                d = 0.07 if (i + j) % 2 else 0.05
                m.add(xf(diamond(d * 2, d * 2, 0.04), rot=(0, yaw, 0), pos=(x * math.cos(math.radians(yaw)) + (w / 2 + 0.01) * math.sin(math.radians(yaw)), y, (w / 2 + 0.01) * math.cos(math.radians(yaw)) - x * math.sin(math.radians(yaw)))), tile, 0, 0.8, name='tile')


def pointed_arch(w, h, n=12):
    pts = [(-w / 2, 0), (w / 2, 0)]
    r = w * 0.85
    for t in np.linspace(0, 1, n):
        a = math.acos((w / 2 - r) / -r) if False else None
        x = w / 2 - (w / 2) * t
        y = h * 0.62 + h * 0.38 * math.sin(math.pi / 2 * t) ** 1.2
        pts.append((x, y))
    for t in np.linspace(1, 0, n)[1:]:
        pts.append((-(w / 2 - (w / 2) * t), h * 0.62 + h * 0.38 * math.sin(math.pi / 2 * t) ** 1.2))
    return pts


def aisha_bibi():
    m = Model('aisha-bibi')
    w, h = 2.0, 2.3
    m.add(cyl(2.4, 0.04, 60), SAND, 0, 0.95, name='ground')
    mausoleum_base(m, w, h, BRICK, BRICKD)
    # massive fluted corner columns
    for sx in (-1, 1):
        for sz in (-1, 1):
            col = lathe([(0.0005, 0.08), (0.22, 0.08), (0.2, h * 0.5), (0.17, h + 0.08), (0.0005, h + 0.08)], 24)
            m.add(xf(col, pos=(sx * w / 2, 0, sz * w / 2)), BRICKD, 0, 0.85, name='column')
            for k in range(6):
                m.add(xf(torus(0.205 - 0.01 * k, 0.012, 24, 4), pos=(sx * w / 2, 0.4 + 0.35 * k, sz * w / 2)), BRICK, 0, 0.8, name='column-ring')
    # front portal niche with pointed arch
    m.add(xf(extrude(pointed_arch(0.9, 1.7), 0.08), pos=(0, 0.1, w / 2 + 0.02)), (0.42, 0.26, 0.16), 0, 0.9, name='portal')
    m.add(xf(extrude(pointed_arch(1.15, 1.95), 0.05), pos=(0, 0.08, w / 2 + 0.005)), BRICKD, 0, 0.85, name='portal-frame')
    # crowning frieze
    m.add(xf(box(w + 0.06, 0.16, w + 0.06), pos=(0, h + 0.02, 0)), BRICKD, 0, 0.85, name='frieze')
    return m


def karakhan():
    m = Model('karakhan')
    w, h = 1.9, 1.6
    m.add(cyl(2.4, 0.04, 60), SAND, 0, 0.95, name='ground')
    mausoleum_base(m, w, h, CLAY, BRICKD)
    # drum and dome
    m.add(cyl(0.78, 0.35, 48, h + 0.08), CLAY, 0, 0.85, name='drum')
    dome = [(0.8, h + 0.42)] + [(0.8 * math.cos(t) ** 0.9, h + 0.42 + 0.95 * math.sin(t)) for t in np.linspace(0.05, math.pi / 2, 16)]
    dome[-1] = (0.0005, dome[-1][1])
    m.add(lathe(dome, 48), (0.46, 0.66, 0.66), 0.1, 0.5, name='dome')
    for k in range(16):
        a = 2 * math.pi * k / 16
        pts = [(0.81 * math.cos(t) * math.cos(a), h + 0.42 + 0.96 * math.sin(t), 0.81 * math.cos(t) * math.sin(a)) for t in np.linspace(0.02, 1.45, 12)]
        m.add(tube(pts, 0.012, 4), (0.36, 0.52, 0.52), 0, 0.5, name='dome-rib')
    m.add(tube([(0, h + 1.35, 0), (0, h + 1.65, 0)], 0.025, 6), GOLD, 0.6, 0.3, name='finial')
    m.add(xf(sphere(0.05, 8, 10), pos=(0, h + 1.62, 0)), GOLD, 0.6, 0.3, name='finial-ball')
    # tall entrance portal (pishtaq) rising above the walls
    m.add(xf(box(1.5, h + 0.75, 0.32), pos=(0, (h + 0.75) / 2 + 0.08, w / 2 + 0.12)), CLAY, 0, 0.85, name='pishtaq')
    m.add(xf(extrude(pointed_arch(0.8, 1.5), 0.06), pos=(0, 0.1, w / 2 + 0.3)), (0.40, 0.27, 0.18), 0, 0.9, name='portal')
    for sx in (-1, 1):
        m.add(xf(lathe([(0.0005, 0.08), (0.12, 0.08), (0.1, h + 0.85), (0.0005, h + 0.95)], 16), pos=(sx * 0.72, 0, w / 2 + 0.28)), BRICKD, 0, 0.8, name='portal-column')
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.add(xf(lathe([(0.0005, 0.08), (0.16, 0.08), (0.13, h + 0.2), (0.0005, h + 0.3)], 20), pos=(sx * w / 2, 0, sz * w / 2)), BRICKD, 0, 0.85, name='corner-tower')
    return m


def airan():
    m = Model('airan')
    m.add(xf(cyl(1.6, 0.08, 56), scale=(1, 1, 0.75)), (0.62, 0.20, 0.20), 0, 0.85, name='cloth')
    m.add(xf(torus(1.6, 0.035, 56, 6), pos=(0, 0.08, 0), scale=(1, 1, 0.75)), GOLD, 0.3, 0.6, name='cloth-trim')
    # kese bowl with airan
    m.add(xf(lathe(bowl_profile(0.6, 0.5), 48), pos=(-0.45, 0.08, 0.1)), MILK, 0.05, 0.25, double=True, name='kese')
    m.add(xf(cyl(0.53, 0.01, 40), pos=(-0.45, 0.08 + 0.42, 0.1)), (0.98, 0.97, 0.93), 0, 0.5, name='airan')
    for k in range(10):
        a = 2 * math.pi * k / 10
        m.add(xf(diamond(0.1, 0.14, 0.02), rot=(0, -math.degrees(a) + 90, 0), pos=(-0.45 + 0.585 * math.cos(a), 0.08 + 0.33, 0.1 + 0.585 * math.sin(a))), (0.15, 0.38, 0.62), 0, 0.4, name='blue-pattern')
    m.add(xf(torus(0.6, 0.012, 48, 4), pos=(-0.45, 0.08 + 0.5, 0.1)), (0.15, 0.38, 0.62), 0, 0.4, name='rim')
    # clay jug
    prof = [(0.0005, 0.0), (0.3, 0.0), (0.42, 0.25), (0.45, 0.55), (0.35, 0.85), (0.18, 1.05), (0.16, 1.25), (0.2, 1.3), (0.0005, 1.3)]
    m.add(xf(lathe(prof, 40), pos=(0.65, 0.08, -0.15)), (0.70, 0.45, 0.28), 0, 0.7, name='jug')
    m.add(xf(tube([(0.65 + 0.17, 1.25, -0.15), (0.65 + 0.55, 1.05, -0.15), (0.65 + 0.42, 0.55, -0.15)], 0.04, 8), pos=(0, 0.0, 0)), (0.62, 0.38, 0.22), 0, 0.7, name='handle')
    m.add(xf(torus(0.44, 0.02, 40, 6), pos=(0.65, 0.08 + 0.55, -0.15)), (0.95, 0.88, 0.70), 0, 0.6, name='jug-band')
    return m


# ------------------------------------------------------------------ PART 2
def carpet(m, w, d, y=0.0):
    m.add(xf(box(w, 0.04, d), pos=(0, y + 0.02, 0)), RED, 0, 0.9, name='carpet')
    m.add(xf(box(w - 0.3, 0.045, d - 0.3), pos=(0, y + 0.022, 0)), (0.75, 0.27, 0.2), 0, 0.9, name='carpet-field')
    for i in range(-2, 3):
        m.add(xf(diamond(0.35, 0.35, 0.01), rot=(90, 0, 45), pos=(i * w / 6, y + 0.05, 0)), GOLD, 0, 0.7, name='carpet-orn')
    for k in range(int(w / 0.12)):
        for sz in (-1, 1):
            m.add(tube([(-w / 2 + 0.06 + k * 0.12, y + 0.02, sz * d / 2), (-w / 2 + 0.06 + k * 0.12, y + 0.02, sz * (d / 2 + 0.1))], 0.012, 4), CREAM, 0, 0.9, name='fringe')


def aitys():
    m = Model('aitys')
    carpet(m, 3.4, 2.0)
    d = m2.dombra()
    embed(m, d, rot=(0, 0, 62), pos=(-0.55, 0.5, -0.35), scale=(0.62, 0.62, 0.62))
    embed(m, d, rot=(0, 180, 62), pos=(0.55, 0.5, 0.35), scale=(0.62, 0.62, 0.62))
    for s in (-1, 1):
        m.add(xf(sphere(0.38, 12, 18), pos=(s * 1.25, 0.15, -s * 0.1), scale=(1, 0.35, 1)), TEAL if s < 0 else (0.55, 0.15, 0.2), 0, 0.85, name='cushion')
    # speech arcs between the two instruments
    for k in range(3):
        r = 0.3 + 0.18 * k
        pts = [(r * math.cos(a) * 0.7, 1.45 + r * math.sin(a), 0) for a in np.linspace(0.3, math.pi - 0.3, 18)]
        m.add(tube(pts, 0.022, 6), GOLD, 0.4, 0.4, name='verse')
    return m


def asyk_bone(seed):
    V, F, s = sphere(0.22, 14, 20, scale=(1.25, 0.72, 0.85), noise=0.07, seed=seed)
    V = V.copy()
    # pinch the middle to suggest the waisted knucklebone shape
    V[:, 2] *= 1 - 0.25 * np.exp(-(V[:, 0] / 0.12) ** 2)
    V[:, 1] += 0.04 * np.sign(V[:, 1]) * np.exp(-(V[:, 0] / 0.18) ** 2)
    return V, F, s


def asyk():
    m = Model('asyk')
    m.add(xf(cyl(2.2, 0.03, 60), scale=(1, 1, 0.7)), SAND, 0, 0.95, name='ground')
    m.add(tube([(-1.6, 0.04, 0.6), (1.6, 0.04, 0.6)], 0.015, 4), (0.6, 0.5, 0.36), 0, 0.9, name='line')
    cols = [CREAM, (0.92, 0.84, 0.66), (0.65, 0.2, 0.2), CREAM, (0.2, 0.45, 0.6), CREAM, (0.92, 0.84, 0.66)]
    for i, c in enumerate(cols):
        m.add(xf(asyk_bone(i), pos=(-1.2 + i * 0.4, 0.17, 0.2), rot=(0, 90 + (i % 3) * 25, (i % 2) * 180)), c, 0, 0.6, name='asyk')
    m.add(xf(asyk_bone(9), pos=(0.3, 0.22, -0.7), rot=(0, 30, 0), scale=(1.35, 1.35, 1.35)), (0.75, 0.55, 0.30), 0.3, 0.45, name='saqa')
    m.add(xf(cyl(0.05, 0.02, 12), pos=(0.3, 0.42, -0.7)), IRON, 0.6, 0.4, name='lead')
    return m


def wheel(m, pos, r=0.9, axis_z=True):
    rot = (90, 0, 0) if axis_z else (0, 0, 90)
    m.add(xf(torus(r, 0.06, 48, 8), rot=rot, pos=pos), WOODD, 0, 0.7, name='rim')
    m.add(xf(torus(r + 0.02, 0.025, 48, 6), rot=rot, pos=pos), IRON, 0.5, 0.5, name='tyre')
    m.add(xf(cyl(0.13, 0.28, 16, -0.14), rot=rot, pos=pos), WOOD, 0, 0.7, name='hub')
    for k in range(12):
        a = 2 * math.pi * k / 12
        m.add(tube([(pos[0] + 0.12 * math.cos(a), pos[1] + 0.12 * math.sin(a), pos[2]), (pos[0] + r * math.cos(a), pos[1] + r * math.sin(a), pos[2])], 0.03, 6), WOOD, 0, 0.7, name='spoke')


def at_arba():
    m = Model('at-arba')
    m.add(xf(cyl(2.8, 0.03, 60), scale=(1, 1, 0.65)), SAND, 0, 0.95, name='ground')
    for z in (-0.75, 0.75):
        wheel(m, (-0.4, 0.93, z), 0.9)
    m.add(tube([(-0.4, 0.93, -0.9), (-0.4, 0.93, 0.9)], 0.05, 8), WOODD, 0, 0.7, name='axle')
    m.add(xf(box(1.9, 0.08, 1.2), pos=(-0.3, 1.1, 0)), WOOD, 0, 0.75, name='bed')
    for z in (-0.6, 0.6):
        m.add(xf(box(1.9, 0.3, 0.05), pos=(-0.3, 1.3, z)), WOODL, 0, 0.75, name='side')
        for x in np.linspace(-1.2, 0.6, 5):
            m.add(xf(box(0.05, 0.42, 0.06), pos=(x, 1.3, z)), WOODD, 0, 0.75, name='stake')
    m.add(xf(box(0.05, 0.3, 1.2), pos=(-1.25, 1.3, 0)), WOODL, 0, 0.75, name='back')
    for z in (-0.4, 0.4):
        m.add(tube([(0.6, 1.12, z), (1.6, 1.0, z * 0.9), (2.4, 0.95, z * 0.8)], 0.04, 8), WOODD, 0, 0.75, name='shaft')
    m.add(xf(sphere(0.38, 10, 14, noise=0.08), pos=(-0.5, 1.45, 0), scale=(1.8, 0.6, 1.2)), (0.84, 0.74, 0.40), 0, 0.95, name='hay')
    return m


def baige():
    m = Model('baige')
    m.add(xf(cyl(2.6, 0.03, 60), scale=(1, 1, 0.6)), GRASS, 0, 0.95, name='ground')
    horse(m, pos=(0, 0.0, 0), gallop=True)
    # small rider
    m.add(xf(sphere(0.18, 10, 14), pos=(0.05, 2.05, 0), scale=(0.8, 1.2, 0.8)), (0.15, 0.40, 0.58), 0, 0.8, name='rider')
    m.add(xf(sphere(0.1, 10, 12), pos=(0.16, 2.33, 0)), SKIN, 0, 0.8, name='rider-head')
    m.add(xf(sphere(0.11, 10, 12), pos=(0.16, 2.38, 0), scale=(1, 0.6, 1)), RED, 0, 0.8, name='rider-cap')
    m.add(tube([(0.1, 2.1, 0.12), (0.5, 2.0, 0.15), (0.65, 2.25, 0.18)], 0.025, 6), LEATHERD, 0, 0.7, name='qamshy')
    # finish posts and ribbon
    for z in (-0.9, 0.9):
        m.add(tube([(1.9, 0.0, z), (1.9, 1.6, z)], 0.04, 8), WOODL, 0, 0.7, name='post')
        m.add(xf(extrude([(0, 0), (0.4, -0.12), (0, -0.24)], 0.01), pos=(1.9, 1.6, z)), RED if z < 0 else TEAL, 0, 0.8, double=True, name='flag')
    m.add(tube([(1.9, 1.3, -0.9), (1.9, 1.25, 0), (1.9, 1.3, 0.9)], 0.015, 4), GOLD, 0, 0.7, name='ribbon')
    return m


def baursak():
    m = Model('baursak')
    m.add(lathe([(0.0005, 0.0), (1.2, 0.0), (1.5, 0.08), (1.6, 0.18), (1.55, 0.2), (1.4, 0.12), (1.1, 0.08), (0.0005, 0.08)], 64), MILK, 0.05, 0.3, name='plate')
    for k in range(32):
        a = 2 * math.pi * k / 32
        m.add(xf(diamond(0.07, 0.07, 0.02), rot=(-75, -math.degrees(a) + 90, 0), pos=(1.47 * math.cos(a), 0.12, 1.47 * math.sin(a))), (0.15, 0.38, 0.62), 0, 0.4, name='plate-orn')
    rng = np.random.RandomState(7)
    placed = []
    for layer, (n, rad, y) in enumerate(((11, 0.95, 0.2), (7, 0.6, 0.38), (4, 0.3, 0.55), (1, 0.0, 0.7))):
        for k in range(n):
            a = 2 * math.pi * k / max(n, 1) + layer * 0.4
            pos = (rad * math.cos(a) + rng.uniform(-.05, .05), y, rad * math.sin(a) + rng.uniform(-.05, .05))
            shape = rng.choice(['sq', 'tri', 'ball'])
            sc = (1.15, 0.72, 1.15) if shape == 'sq' else (1.0, 0.8, 1.0)
            m.add(xf(sphere(0.18, 10, 4 if shape == 'sq' else (3 if shape == 'tri' else 14), scale=sc, noise=0.06, seed=k + 9 * layer), pos=pos, rot=(rng.uniform(-15, 15), rng.uniform(0, 360), rng.uniform(-15, 15))),
                  BAURSAK if (k + layer) % 3 else (0.74, 0.48, 0.20), 0, 0.65, name='baursak')
            placed.append(pos)
    return m


def zhailau():
    m = Model('zhailau')
    m.add(xf(cyl(2.8, 0.1, 64)), GRASS, 0, 0.95, name='meadow')
    for x, z, r, h in ((-1.5, -2.2, 0.7, 0.6), (-0.3, -2.45, 0.8, 1.0), (1.1, -2.2, 0.7, 0.7)):
        m.add(xf(sphere(r, 12, 18), pos=(x, 0.05, z), scale=(1.3, h / r, 0.55)), GRASSD, 0, 0.95, name='hill')
    m.add(xf(sphere(0.35, 10, 14), pos=(-0.3, 0.86, -2.45), scale=(1.2, 0.55, 0.5)), SNOW, 0, 0.8, name='snowcap')
    stream = [(-2.7, 0.11, 1.2), (-1.4, 0.11, 0.8), (-0.2, 0.11, 1.5), (1.2, 0.11, 1.0), (2.7, 0.11, 1.6)]
    m.add(xf(tube(stream, 0.16, 10), scale=(1, 0.12, 1)), WATER, 0.1, 0.2, name='stream')
    y = m2.yurt()
    embed(m, y, pos=(0.3, 0.1, -0.2), scale=(0.42, 0.42, 0.42))
    embed(m, y, pos=(-1.3, 0.1, -0.5), scale=(0.3, 0.3, 0.3), rot=(0, 40, 0))
    for i, (x, z) in enumerate(((1.4, 0.3), (1.8, 0.6), (1.5, 0.9), (2.0, 0.1), (-0.8, 0.8), (-1.1, 1.1))):
        m.add(xf(sphere(0.14, 8, 12, noise=0.1, seed=i), pos=(x, 0.25, z), scale=(1.3, 0.85, 0.9)), MILK, 0, 0.95, name='sheep')
        m.add(xf(sphere(0.06, 6, 8), pos=(x + 0.19, 0.28, z)), HORSED, 0, 0.8, name='sheep-head')
    rng = np.random.RandomState(4)
    for k in range(40):
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(0.4, 2.6)
        m.add(xf(sphere(0.035, 4, 6), pos=(r * math.cos(a), 0.12, r * math.sin(a))), (0.95, 0.85, 0.3) if k % 3 else (0.85, 0.35, 0.5), 0, 0.8, name='flower')
    return m


def kazakh_kuresi():
    m = Model('kazakh-kuresi')
    m.add(cyl(2.2, 0.12, 64), (0.22, 0.42, 0.62), 0, 0.85, name='mat')
    m.add(xf(cyl(1.6, 0.005, 64, 0.12)), (0.92, 0.80, 0.30), 0, 0.85, name='circle')
    m.add(xf(cyl(1.5, 0.006, 64, 0.12)), (0.22, 0.42, 0.62), 0, 0.85, name='circle-in')
    # two wrestling belts (belbeu) loosely coiled
    for s, col in ((-1, RED), (1, (0.12, 0.35, 0.65))):
        pts = [(s * 0.55 + 0.42 * math.cos(t), 0.2 + 0.012 * t, s * 0.1 + 0.32 * math.sin(t)) for t in np.linspace(0, 2 * math.pi * 1.6, 60)]
        m.add(xf(tube(pts, 0.07, 8), scale=(1, 0.55, 1)), col, 0, 0.85, name='belt')
        m.add(xf(box(0.2, 0.06, 0.12), pos=(s * 0.55 + 0.42, 0.22, s * 0.1)), GOLD, 0.6, 0.35, name='buckle')
    # winner's trophy
    m.add(lathe([(0.0005, 0.12), (0.25, 0.12), (0.12, 0.3), (0.1, 0.55), (0.3, 0.75), (0.32, 1.0), (0.28, 1.0), (0.0005, 0.85)], 32), GOLD, 0.7, 0.3, name='cup')
    return m


def caravan_load(color=RED):
    def add(m, T):
        m.add(T(xf(sphere(0.45, 10, 14), pos=(0, 2.05, 0), scale=(1.2, 0.4, 0.95))), color, 0, 0.85, name='blanket')
        for s in (-1, 1):
            m.add(T(xf(box(0.55, 0.42, 0.3), pos=(-0.05, 1.8, s * 0.62))), (0.86, 0.78, 0.6), 0, 0.9, name='pack')
            m.add(T(tube([(-0.32, 2.03, s * 0.48), (-0.32, 1.6, s * 0.79)], 0.015, 4)), LEATHERD, 0, 0.8, name='strap')
        m.add(T(xf(cyl(0.16, 0.9, 16), rot=(90, 0, 0), pos=(-0.05, 2.28, 0.45))), (0.55, 0.25, 0.35), 0, 0.85, name='roll')
    return add


def keruen():
    m = Model('keruen')
    m.add(xf(cyl(4.6, 0.03, 72), scale=(1, 1, 0.42)), SAND, 0, 0.95, name='desert')
    rng = np.random.RandomState(2)
    for k in range(7):
        m.add(xf(sphere(0.6, 10, 14), pos=(rng.uniform(-3.5, 3.5), -0.25, rng.uniform(-1.6, -1.0)), scale=(2.2, 0.6, 1)), (0.90, 0.82, 0.62), 0, 0.95, name='dune')
    xs = [-2.6, -0.6, 1.4]
    cols = [RED, TEAL, (0.55, 0.25, 0.35)]
    for i, x in enumerate(xs):
        camel(m, pos=(x, 0, 0.1 * i), load=caravan_load(cols[i]))
    for a, b in zip(xs[:-1], xs[1:]):
        m.add(tube([(a + 1.38, 2.2, 0.1 * xs.index(a)), (a + 1.7, 1.6, 0.05 + 0.1 * xs.index(a)), (b - 0.6, 1.8, 0.1 * xs.index(b))], 0.012, 4), LEATHERD, 0, 0.8, name='lead-rope')
    return m


def kosh():
    m = Model('kosh')
    m.add(xf(cyl(2.8, 0.03, 64), scale=(1, 1, 0.6)), GRASS, 0, 0.95, name='steppe')

    def load(m, T):
        m.add(T(xf(sphere(0.5, 10, 14), pos=(0, 2.0, 0), scale=(1.25, 0.35, 1.0))), RED, 0, 0.85, name='carpet')
        # folded lattice walls (kerege) on both sides
        for s in (-1, 1):
            base = (0.0, 1.85, s * 0.66)
            m.add(T(xf(box(1.0, 0.7, 0.12), pos=base)), (0.80, 0.58, 0.36), 0, 0.8, name='kerege')
            for k in range(7):
                x = -0.45 + k * 0.15
                m.add(T(tube([(x, 1.52, s * 0.73), (x + 0.15, 2.18, s * 0.73)], 0.014, 4)), WOODD, 0, 0.8, name='lattice')
                m.add(T(tube([(x + 0.15, 1.52, s * 0.73), (x, 2.18, s * 0.73)], 0.014, 4)), WOODD, 0, 0.8, name='lattice')
        # felt rolls and bundle of roof poles (uyk)
        for k, z in enumerate((-0.25, 0.25)):
            m.add(T(xf(cyl(0.2, 1.2, 18), rot=(0, 0, 90), pos=(0.6, 2.25 + 0.05 * k, z))), FELT, 0, 0.95, name='felt-roll')
        for k in range(9):
            m.add(T(tube([(-0.9, 2.3 + 0.02 * k, -0.18 + 0.045 * k), (0.9, 2.42 + 0.02 * k, -0.18 + 0.045 * k)], 0.022, 5)), (0.75, 0.38, 0.22), 0, 0.7, name='uyk')
        # the shanyraq rides on top
        m.add(T(xf(torus(0.35, 0.05, 32, 8), pos=(-0.1, 2.68, 0))), WOODD, 0, 0.6, name='shanyraq')
        for a in (0, 60, 120):
            m.add(T(xf(box(0.7, 0.04, 0.04), rot=(0, a, 0), pos=(-0.1, 2.7, 0))), WOODD, 0, 0.6, name='kuldiresh')
        # tassels on the lead camel
        for k in range(5):
            m.add(T(tube([(1.1 + 0.04 * k, 1.75, 0.12), (1.1 + 0.04 * k, 1.45, 0.14)], 0.02, 4)), (0.85, 0.2, 0.25) if k % 2 else GOLD, 0, 0.8, name='tassel')
    camel(m, pos=(-0.3, 0, 0), load=load)
    return m


def tostagan(m, pos, r=0.6, h=0.45, color=WOOD, liquid=MILK):
    m.add(xf(lathe(bowl_profile(r, h), 48), pos=pos), color, 0, 0.55, double=True, name='bowl')
    m.add(xf(cyl(r * 0.9, 0.01, 40), pos=(pos[0], pos[1] + h * 0.8, pos[2])), liquid, 0, 0.4, name='liquid')
    m.add(xf(torus(r * 0.99, 0.02, 48, 6), pos=(pos[0], pos[1] + h * 0.55, pos[2])), GOLD, 0.6, 0.35, name='bowl-band')
    for k in range(12):
        a = 2 * math.pi * k / 12
        m.add(xf(diamond(0.07, 0.1, 0.02), rot=(0, -math.degrees(a) + 90, 0), pos=(pos[0] + r * 0.97 * math.cos(a), pos[1] + h * 0.35, pos[2] + r * 0.97 * math.sin(a))), GOLD, 0.6, 0.35, name='bowl-orn')


def kymyz():
    m = Model('kymyz')
    m.add(lathe([(0.0005, 0.0), (1.5, 0.0), (1.5, 0.12), (0.0005, 0.12)], 56), WOODD, 0, 0.7, name='table')
    m.add(xf(torus(1.5, 0.04, 56, 6), pos=(0, 0.11, 0)), GOLD, 0.4, 0.5, name='table-rim')
    tostagan(m, (-0.2, 0.12, 0.1), 0.62, 0.5)
    tostagan(m, (0.85, 0.12, 0.55), 0.32, 0.26)
    tostagan(m, (0.8, 0.12, -0.6), 0.32, 0.26)
    # ozhau ladle resting across the big bowl
    m.add(tube([(-0.95, 0.75, 0.2), (-0.2, 0.68, 0.15), (0.35, 0.6, 0.05)], 0.035, 8), WOODL, 0, 0.6, name='ladle-handle')
    m.add(xf(lathe(bowl_profile(0.17, 0.12, 0.02), 24), pos=(0.38, 0.5, 0.05)), WOODL, 0, 0.6, double=True, name='ladle-cup')
    m.add(xf(sphere(0.05, 8, 10), pos=(-0.97, 0.76, 0.2)), GOLD, 0.6, 0.35, name='ladle-end')
    return m


def kui():
    m = Model('kui')
    d = m2.dombra()
    embed(m, d, rot=(0, 0, -20), pos=(-0.2, 0.0, 0), scale=(0.9, 0.9, 0.9))
    # floating notes
    for i, (x, y, z, s) in enumerate(((1.0, 2.6, 0.2, 1.0), (1.5, 3.1, -0.2, 0.8), (1.9, 2.3, 0.3, 0.9), (0.6, 3.5, 0.0, 0.7), (2.2, 3.4, -0.1, 0.75))):
        col = GOLD if i % 2 == 0 else TEAL
        m.add(xf(sphere(0.12 * s, 10, 14), pos=(x, y, z), rot=(0, 0, 25), scale=(1.35, 0.95, 0.55)), col, 0.5, 0.35, name='note-head')
        m.add(tube([(x + 0.14 * s, y, z), (x + 0.14 * s, y + 0.55 * s, z)], 0.018 * s, 6), col, 0.5, 0.35, name='note-stem')
        if i % 2 == 0:
            m.add(tube([(x + 0.14 * s, y + 0.55 * s, z), (x + 0.32 * s, y + 0.38 * s, z)], 0.018 * s, 6), col, 0.5, 0.35, name='note-flag')
    for k in range(3):
        pts = [(0.5 + 0.35 * t * 6, 1.6 + 0.25 * math.sin(t * 9 + k) + 0.25 * k, -0.4) for t in np.linspace(0, 1, 30)]
        m.add(tube(pts, 0.012, 4), (0.85, 0.75, 0.55), 0.3, 0.5, name='wave')
    return m


def qorzhyn():
    m = Model('qorzhyn')
    # saddle stand
    m.add(xf(box(0.24, 1.9, 0.24), pos=(-1.0, 0.95, 0)), WOODD, 0, 0.7, name='post')
    m.add(xf(box(0.24, 1.9, 0.24), pos=(1.0, 0.95, 0)), WOODD, 0, 0.7, name='post')
    m.add(xf(sphere(0.5, 14, 20), pos=(0, 1.95, 0), scale=(2.4, 0.32, 0.9)), WOOD, 0, 0.7, name='beam')
    # the two pockets hanging on both sides
    for s in (-1, 1):
        pocket = xf(box(1.3, 1.0, 0.18), pos=(0, 1.3, s * 0.52), rot=(s * 8, 0, 0))
        m.add(pocket, (0.68, 0.16, 0.18), 0, 0.9, name='pocket')
        m.add(xf(box(1.12, 0.82, 0.02), pos=(0, 1.3, s * 0.62), rot=(s * 8, 0, 0)), (0.82, 0.62, 0.30), 0, 0.85, name='panel')
        for i in (-1, 0, 1):
            for j in (-1, 1):
                m.add(xf(diamond(0.26, 0.3, 0.03), pos=(i * 0.36, 1.3 + j * 0.2, s * 0.64), rot=(s * 8, 0, 0)), TEAL if (i + j) % 2 else RED, 0, 0.8, name='orn')
        for k in range(6):
            x = -0.55 + k * 0.22
            m.add(tube([(x, 0.78, s * 0.47), (x, 0.55, s * 0.47)], 0.03, 5), GOLD if k % 2 else (0.82, 0.2, 0.25), 0, 0.8, name='tassel')
            m.add(xf(sphere(0.05, 6, 8), pos=(x, 0.52, s * 0.47)), GOLD if k % 2 else (0.82, 0.2, 0.25), 0, 0.8, name='tassel-end')
    # connecting band over the beam
    band = [(0, 1.8, -0.5), (0, 2.08, -0.25), (0, 2.12, 0.0), (0, 2.08, 0.25), (0, 1.8, 0.5)]
    m.add(xf(tube(band, 0.09, 8), scale=(6.5, 1, 1)), (0.68, 0.16, 0.18), 0, 0.9, name='band')
    return m


def qudyq():
    m = Model('qudyq')
    m.add(cyl(2.4, 0.04, 64), SAND, 0, 0.95, name='ground')
    rng = np.random.RandomState(1)
    for layer in range(4):
        for k in range(16):
            a = 2 * math.pi * (k + 0.5 * (layer % 2)) / 16
            m.add(xf(box(0.36, 0.2, 0.26), rot=(0, -math.degrees(a), 0), pos=(0.8 * math.cos(a), 0.14 + 0.2 * layer, 0.8 * math.sin(a))),
                  tuple(np.clip(np.array(STONE) + rng.uniform(-0.08, 0.06), 0, 1)), 0, 0.95, name='stone')
    m.add(cyl(0.66, 0.02, 40, 0.5), (0.12, 0.2, 0.26), 0, 0.3, name='water')
    for s in (-1, 1):
        m.add(tube([(s * 1.05, 0.0, 0), (s * 1.0, 2.3, 0)], 0.07, 8), WOODD, 0, 0.7, name='post')
    m.add(tube([(-1.15, 2.2, 0), (1.15, 2.2, 0)], 0.06, 8), WOOD, 0, 0.7, name='beam')
    m.add(xf(torus(0.14, 0.04, 20, 6), rot=(90, 0, 0), pos=(0, 2.2, 0)), IRON, 0.5, 0.4, name='pulley')
    m.add(tube([(0, 2.06, 0), (0, 1.3, 0)], 0.012, 4), (0.7, 0.6, 0.42), 0, 0.9, name='rope')
    # qauga: leather bucket
    m.add(xf(lathe([(0.0005, 0.0), (0.18, 0.0), (0.24, 0.3), (0.26, 0.42), (0.22, 0.42), (0.0005, 0.06)], 24), pos=(0, 0.88, 0)), LEATHER, 0, 0.8, double=True, name='qauga')
    m.add(tube([(-0.25, 1.3, 0), (0, 1.38, 0), (0.25, 1.3, 0)], 0.015, 4), LEATHERD, 0, 0.8, name='bail')
    # stone trough
    m.add(xf(box(1.2, 0.3, 0.4), pos=(0.9, 0.17, 1.2), rot=(0, 30, 0)), STONE, 0, 0.9, name='trough')
    return m


def qurt():
    m = Model('qurt')
    m.add(xf(box(2.8, 0.12, 1.8), pos=(0, 0.06, 0)), WOODL, 0, 0.75, name='board')
    for x in (-1.3, 1.3):
        m.add(xf(box(0.08, 0.13, 1.8), pos=(x, 0.065, 0)), WOODD, 0, 0.75, name='board-edge')
    rng = np.random.RandomState(5)
    for i in range(5):
        for j in range(4):
            x, z = -1.0 + i * 0.5 + rng.uniform(-.05, .05), -0.6 + j * 0.4 + rng.uniform(-.05, .05)
            kind = (i + j) % 3
            if kind == 2:
                mesh = lathe([(0.0005, 0), (0.16, 0), (0.12, 0.18), (0.05, 0.3), (0.0005, 0.33)], 14)
                m.add(xf(mesh, pos=(x, 0.12, z)), (0.96, 0.94, 0.88), 0, 0.95, name='qurt-cone')
            else:
                m.add(xf(sphere(0.16, 10, 14, noise=0.08, seed=i * 4 + j), pos=(x, 0.26, z), scale=(1, 0.85, 1)),
                      (0.96, 0.94, 0.88) if kind == 0 else (0.88, 0.78, 0.62), 0, 0.95, name='qurt')
    # cloth bag
    m.add(xf(sphere(0.5, 12, 16, noise=0.05), pos=(1.6, 0.4, 0.8), scale=(0.9, 0.85, 0.9)), (0.85, 0.8, 0.7), 0, 0.95, name='bag')
    m.add(xf(torus(0.15, 0.04, 16, 6), pos=(1.6, 0.82, 0.8)), RED, 0, 0.8, name='bag-tie')
    return m


def qystau():
    m = Model('qystau')
    m.add(cyl(3.0, 0.06, 64), SNOW, 0, 0.9, name='snow')
    for x, z, r in ((-1.6, -2.3, 0.8), (0.4, -2.5, 0.9), (1.9, -2.0, 0.7)):
        m.add(xf(sphere(r, 12, 16), pos=(x, 0.0, z), scale=(1.4, 0.8, 0.55)), (0.86, 0.88, 0.92), 0, 0.9, name='hill')
    # low winter house of clay and turf
    m.add(xf(box(2.0, 0.9, 1.3), pos=(-0.5, 0.5, -0.3)), CLAY, 0, 0.95, name='house')
    m.add(xf(box(2.15, 0.14, 1.45), pos=(-0.5, 1.0, -0.3)), (0.55, 0.42, 0.28), 0, 0.95, name='roof')
    m.add(xf(box(2.1, 0.06, 1.4), pos=(-0.5, 1.09, -0.3)), SNOW, 0, 0.8, name='roof-snow')
    m.add(xf(box(0.42, 0.66, 0.05), pos=(-0.9, 0.39, 0.37)), WOODD, 0, 0.7, name='door')
    m.add(xf(box(0.34, 0.26, 0.05), pos=(-0.15, 0.62, 0.37)), (0.95, 0.82, 0.45), 0, 0.4, name='window')
    m.add(xf(box(0.16, 0.4, 0.16), pos=(0.1, 1.3, -0.5)), CLAY, 0, 0.9, name='chimney')
    # pen for the animals
    pen = [(0.9, 0.2), (2.3, 0.2), (2.3, 1.6), (0.9, 1.6)]
    for (x0, z0), (x1, z1) in zip(pen, pen[1:] + pen[:1]):
        n = int(max(abs(x1 - x0), abs(z1 - z0)) / 0.35) + 1
        for t in np.linspace(0, 1, n, endpoint=False):
            m.add(tube([(x0 + (x1 - x0) * t, 0.0, z0 + (z1 - z0) * t), (x0 + (x1 - x0) * t, 0.7, z0 + (z1 - z0) * t)], 0.035, 6), WOODD, 0, 0.8, name='fence-post')
        for y in (0.3, 0.6):
            m.add(tube([(x0, y, z0), (x1, y, z1)], 0.025, 5), WOOD, 0, 0.8, name='rail')
    m.add(xf(sphere(0.55, 10, 14, noise=0.06), pos=(-1.9, 0.4, 0.9), scale=(1, 1.1, 1)), (0.82, 0.72, 0.38), 0, 0.95, name='haystack')
    m.add(xf(sphere(0.3, 10, 14), pos=(-1.9, 0.95, 0.9), scale=(1, 0.5, 1)), SNOW, 0, 0.8, name='hay-snow')
    for i, (x, z) in enumerate(((1.3, 0.6), (1.7, 1.0), (1.9, 0.5))):
        m.add(xf(sphere(0.14, 8, 12, noise=0.1, seed=i), pos=(x, 0.25, z), scale=(1.3, 0.85, 0.9)), (0.88, 0.85, 0.78), 0, 0.95, name='sheep')
        m.add(xf(sphere(0.06, 6, 8), pos=(x + 0.19, 0.28, z)), HORSED, 0, 0.8, name='sheep-head')
    return m


def saba():
    m = Model('saba')
    m.add(xf(box(1.5, 0.3, 1.1), pos=(0, 0.15, 0)), WOODD, 0, 0.7, name='stand')
    for s in (-1, 1):
        m.add(xf(box(1.6, 0.06, 0.08), pos=(0, 0.33, s * 0.4)), WOOD, 0, 0.7, name='stand-bar')
    prof = [(0.0005, 0.3), (0.45, 0.3), (0.62, 0.55), (0.68, 1.0), (0.62, 1.45), (0.45, 1.85), (0.26, 2.15), (0.2, 2.45), (0.24, 2.5), (0.0005, 2.5)]
    m.add(lathe(prof, 48, scale=(1, 1, 0.82)), (0.34, 0.20, 0.11), 0, 0.75, name='saba')
    seam = [(0.0, y, ((0.6 if y < 1.6 else 0.35) * 0.82 + 0.02)) for y in np.linspace(0.4, 2.2, 2)]
    seam = [(0, 0.35 + t * 1.85, 0.82 * np.interp(0.35 + t * 1.85, [p[1] for p in prof[:-1]], [p[0] for p in prof[:-1]]) + 0.01) for t in np.linspace(0, 1, 30)]
    m.add(tube(seam, 0.018, 5), CREAM, 0, 0.8, name='seam')
    for y in (0.75, 1.25):
        r = np.interp(y, [p[1] for p in prof[:-1]], [p[0] for p in prof[:-1]])
        m.add(xf(torus(r, 0.025, 48, 6), pos=(0, y, 0), scale=(1, 1, 0.82)), GOLD, 0.4, 0.5, name='band')
        for k in range(10):
            a = 2 * math.pi * k / 10
            m.add(xf(diamond(0.08, 0.12, 0.02), rot=(0, -math.degrees(a) + 90, 0), pos=((r + 0.01) * math.cos(a), y + 0.18, (r + 0.01) * math.sin(a) * 0.82)), GOLD, 0.4, 0.5, name='stud')
    # pispek: wooden plunger sticking out of the neck
    m.add(tube([(0, 1.1, 0), (0.06, 3.35, 0)], 0.035, 8), WOODL, 0, 0.6, name='pispek')
    m.add(xf(sphere(0.06, 8, 10), pos=(0.06, 3.38, 0)), WOODD, 0, 0.6, name='pispek-top')
    m.add(xf(torus(0.21, 0.04, 24, 6), pos=(0, 2.47, 0)), LEATHERD, 0, 0.7, name='neck-rim')
    return m


def shanyraq():
    m = Model('shanyraq')
    m.add(xf(torus(1.2, 0.13, 72, 14), scale=(1, 0.75, 1)), WOODD, 0, 0.55, name='ring')
    m.add(xf(torus(1.2, 0.135, 72, 14), pos=(0, 0.02, 0), scale=(1, 0.2, 1)), (0.66, 0.42, 0.22), 0, 0.55, name='ring-top')
    for k in range(48):
        a = 2 * math.pi * k / 48
        m.add(xf(cyl(0.035, 0.03, 8), rot=(0, 0, 90), pos=(1.33 * math.cos(a), 0, 1.33 * math.sin(a))), (0.18, 0.11, 0.06), 0, 0.8, name='socket')
    # kuldiresh: two families of arched cross-bars
    for fam, (axis, n) in enumerate((('x', 3), ('z', 3))):
        for i in range(n):
            off = (i - (n - 1) / 2) * 0.42
            L = math.sqrt(max(1.2 ** 2 - off ** 2, 0.01))
            pts = []
            for t in np.linspace(-1, 1, 26):
                u = t * L
                y = 0.55 * (1 - t ** 2)
                pts.append((u, y, off) if axis == 'x' else (off, y + 0.01 * fam, u))
            m.add(tube(pts, 0.05, 8), (0.80, 0.55, 0.30), 0, 0.55, name='kuldiresh')
    # a few roof poles (uyk) leaving the ring
    for k in range(12):
        a = 2 * math.pi * k / 12
        m.add(tube([(1.3 * math.cos(a), 0, 1.3 * math.sin(a)), (2.3 * math.cos(a), -0.75, 2.3 * math.sin(a))], 0.035, 6), (0.75, 0.38, 0.22), 0, 0.6, name='uyk')
    for k in range(24):
        a = 2 * math.pi * k / 24
        m.add(xf(diamond(0.12, 0.08, 0.02), rot=(0, -math.degrees(a) + 90, 0), pos=(1.34 * math.cos(a), 0.0, 1.34 * math.sin(a))), GOLD, 0.6, 0.35, name='inlay')
    return m


def sheber():
    m = Model('sheber')
    # sandyq: carved wooden chest with gold fittings
    m.add(xf(box(2.0, 1.0, 1.0), pos=(0, 0.62, 0)), WOOD, 0, 0.65, name='chest')
    m.add(xf(box(2.06, 0.18, 1.06), pos=(0, 1.2, 0)), WOODD, 0, 0.6, name='lid')
    for x in (-0.85, 0.85):
        m.add(xf(box(0.16, 0.24, 1.06), pos=(x, 0.12, 0)), WOODD, 0, 0.6, name='foot')
    for x in (-0.6, 0.0, 0.6):
        m.add(xf(diamond(0.42, 0.5, 0.04), pos=(x, 0.64, 0.51)), (0.62, 0.38, 0.2), 0, 0.6, name='carving')
        for s in (-1, 1):
            pts = [(x + s * (0.05 + 0.03 * t * math.cos(t)), 0.64 + 0.03 * t * math.sin(t), 0.54) for t in np.linspace(0, 8, 20)]
            m.add(tube(pts, 0.012, 4), GOLD, 0.6, 0.35, name='ram-horn')
    for sx in (-1, 1):
        for sy in (0.2, 1.1):
            m.add(xf(box(0.16, 0.16, 1.04), pos=(sx * 0.95, sy, 0)), GOLD, 0.7, 0.3, name='corner')
    m.add(xf(box(0.2, 0.26, 0.05), pos=(0, 1.0, 0.53)), GOLD, 0.7, 0.3, name='lock')
    # tools: chisel and mallet on the lid
    m.add(tube([(-0.7, 1.33, 0.1), (-0.15, 1.33, 0.25)], 0.04, 8), WOODL, 0, 0.6, name='chisel-handle')
    m.add(xf(box(0.3, 0.02, 0.07), pos=(0.0, 1.32, 0.29), rot=(0, -15, 0)), SILVER, 0.8, 0.3, name='chisel-blade')
    m.add(tube([(0.25, 1.35, -0.25), (0.75, 1.35, -0.05)], 0.035, 8), WOODL, 0, 0.6, name='mallet-handle')
    m.add(xf(cyl(0.12, 0.34, 16), rot=(90, -22, 0), pos=(0.82, 1.42, 0.13)), WOODD, 0, 0.6, name='mallet-head')
    m.add(xf(lathe(bowl_profile(0.32, 0.22), 32), pos=(1.5, 0.0, 0.5)), WOODL, 0, 0.6, double=True, name='carved-bowl')
    for k in range(10):
        a = 2 * math.pi * k / 10
        m.add(xf(diamond(0.05, 0.07, 0.015), rot=(0, -math.degrees(a) + 90, 0), pos=(1.5 + 0.31 * math.cos(a), 0.14, 0.5 + 0.31 * math.sin(a))), WOODD, 0, 0.6, name='bowl-carving')
    return m


def usta():
    m = Model('usta')
    m.add(lathe([(0.0005, 0.0), (0.55, 0.0), (0.5, 0.9), (0.0005, 0.9)], 28), WOODD, 0, 0.8, name='stump')
    for k in range(4):
        m.add(xf(torus(0.5 - k * 0.1, 0.008, 28, 4), pos=(0, 0.905, 0)), (0.6, 0.4, 0.22), 0, 0.8, name='rings')
    m.add(xf(box(0.9, 0.3, 0.42), pos=(0, 1.05, 0)), IRON, 0.7, 0.45, name='anvil-waist')
    m.add(xf(box(1.15, 0.24, 0.5), pos=(0.05, 1.32, 0)), IRON, 0.7, 0.4, name='anvil-face')
    horn = lathe([(0.0005, 0.0), (0.2, 0.0), (0.12, 0.45), (0.0005, 0.62)], 20)
    m.add(xf(horn, rot=(0, 0, -90), pos=(0.62, 1.34, 0)), IRON, 0.7, 0.4, name='horn')
    m.add(xf(box(0.7, 0.14, 0.62), pos=(0, 0.97, 0)), IRON, 0.7, 0.45, name='anvil-foot')
    # hammer
    m.add(tube([(-0.9, 1.48, 0.35), (-0.15, 1.5, 0.22)], 0.035, 8), WOODL, 0, 0.6, name='hammer-handle')
    m.add(xf(box(0.14, 0.14, 0.34), pos=(-0.12, 1.52, 0.22), rot=(0, -10, 0)), IRON, 0.8, 0.35, name='hammer-head')
    # glowing horseshoe
    shoe = [(0.25 * math.cos(a) - 0.1, 1.47, 0.25 * math.sin(a) * 1.1 - 0.05) for a in np.linspace(-0.35 * math.pi, 1.35 * math.pi, 30)]
    m.add(tube(shoe, 0.04, 8), (0.95, 0.45, 0.12), 0.4, 0.4, name='horseshoe')
    # tongs on the ground
    for s in (-1, 1):
        m.add(tube([(0.9, 0.05, 0.6), (1.5, 0.05, 0.6 + s * 0.08), (1.9, 0.05, 0.6 + s * 0.2)], 0.025, 6), IRON, 0.7, 0.4, name='tongs')
    return m


def zerger():
    m = Model('zerger')
    m.add(xf(cyl(1.7, 0.1, 56), scale=(1, 1, 0.72)), (0.12, 0.28, 0.3), 0, 0.85, name='velvet')
    # bilezik: wide hinged bracelet
    band = ring_loft([0.0, 0.42], [0.62, 0.62], [0.52, 0.52], 64)
    m.add(xf(band, rot=(0, 0, 70), pos=(-0.45, 0.65, 0.0)), SILVER, 0.9, 0.25, double=True, name='bracelet')
    for k in range(10):
        a = 2 * math.pi * k / 10
        p = np.array([0.63 * math.cos(a), 0.21, 0.53 * math.sin(a)])
        V, F, s = xf(sphere(0.07, 8, 10), pos=tuple(p))
        V, F, s = xf((V, F, s), rot=(0, 0, 70), pos=(-0.45, 0.65, 0.0))
        m.add((V, F, s), (0.70, 0.18, 0.14) if k % 2 else TURQ, 0.1, 0.25, name='stone')
    for y in (0.03, 0.39):
        m.add(xf(xf(torus(0.62, 0.02, 64, 6), pos=(0, y, 0), scale=(1, 1, 0.84)), rot=(0, 0, 70), pos=(-0.45, 0.65, 0.0)), SILVER, 0.9, 0.2, name='filigree')
    # ring with a carnelian
    m.add(xf(torus(0.22, 0.04, 32, 8), rot=(80, 0, 0), pos=(0.75, 0.33, 0.3)), SILVER, 0.9, 0.25, name='ring')
    m.add(xf(sphere(0.12, 12, 14, scale=(1.2, 0.7, 1)), pos=(0.75, 0.56, 0.32)), (0.78, 0.25, 0.12), 0.1, 0.2, name='carnelian')
    m.add(xf(torus(0.13, 0.02, 24, 6), pos=(0.75, 0.53, 0.32), scale=(1.2, 1, 1)), SILVER, 0.9, 0.25, name='bezel')
    # earring
    m.add(xf(torus(0.1, 0.015, 20, 6), rot=(90, 0, 0), pos=(0.9, 0.6, -0.55)), SILVER, 0.9, 0.25, name='ear-hook')
    m.add(xf(diamond(0.28, 0.4, 0.04), pos=(0.9, 0.3, -0.55)), SILVER, 0.9, 0.25, name='ear-plate')
    for k in range(3):
        m.add(tube([(0.82 + 0.08 * k, 0.12, -0.55), (0.82 + 0.08 * k, -0.0, -0.55)], 0.008, 4), SILVER, 0.9, 0.25, name='ear-chain')
    m.add(xf(sphere(0.05, 8, 10), pos=(0.9, 0.3, -0.52)), TURQ, 0.1, 0.25, name='ear-stone')
    return m


def zhyr():
    m = Model('zhyr')
    carpet(m, 3.0, 2.0)
    k = m2.kobyz()
    embed(m, k, rot=(0, 25, 12), pos=(-0.55, 0.05, -0.1), scale=(0.6, 0.6, 0.6))
    # open book of verse on a low stand
    m.add(xf(box(0.9, 0.35, 0.6), pos=(0.85, 0.22, 0.25)), WOODD, 0, 0.7, name='stand')
    for s in (-1, 1):
        m.add(xf(box(0.5, 0.05, 0.62), rot=(0, 0, s * -12), pos=(0.85 + s * 0.25, 0.47, 0.25)), CREAM, 0, 0.9, name='page')
        for j in range(5):
            m.add(xf(box(0.36, 0.006, 0.02), rot=(0, 0, s * -12), pos=(0.85 + s * 0.25, 0.5 + 0.0 * j, 0.06 + 0.09 * j)), (0.35, 0.25, 0.2), 0, 0.9, name='line')
    m.add(xf(box(1.04, 0.04, 0.66), pos=(0.85, 0.42, 0.25)), RED, 0, 0.8, name='cover')
    return m


BUILD = {
    'khan-shatyr': khan_shatyr, 'kyz-zhibek': kyz_zhibek, 'aisha-bibi': aisha_bibi, 'karakhan': karakhan, 'airan': airan,
    'aitys': aitys, 'asyk': asyk, 'at-arba': at_arba, 'baige': baige, 'baursak': baursak, 'zhailau': zhailau,
    'kazakh-kuresi': kazakh_kuresi, 'keruen': keruen, 'kosh': kosh, 'kymyz': kymyz, 'kui': kui, 'qorzhyn': qorzhyn,
    'qudyq': qudyq, 'qurt': qurt, 'qystau': qystau, 'saba': saba, 'shanyraq': shanyraq, 'sheber': sheber,
    'usta': usta, 'zerger': zerger, 'zhyr': zhyr,
}

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    sheet = []
    for n in args or list(BUILD):
        mdl = BUILD[n]()
        path = os.path.join(OUT, f'{n}.glb')
        mdl.write(path)
        print(n, os.path.getsize(path) // 1024, 'KB', sum(len(p['F']) for p in mdl.parts), 'triangles', len(mdl.parts), 'parts')
        if '--preview' in sys.argv:
            sheet.append(np.hstack([mm.render_preview(mdl, 360, 35, 18), mm.render_preview(mdl, 360, 150, 12)]))
    if sheet:
        import cv2
        out = '/tmp/claude-0/-home-claude/9aeb0818-3582-592f-950e-7bc1bd7b9514/scratchpad/_models3.png'
        for i in range(0, len(sheet), 6):
            cv2.imwrite(out.replace('.png', f'_{i // 6}.png'), np.vstack(sheet[i:i + 6]))
