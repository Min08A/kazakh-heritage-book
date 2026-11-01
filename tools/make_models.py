"""Procedurally build simple stylised 3D models (GLB) for the objects that have no
embeddable Sketchfab model: shapan, beshbarmak, besik, torsyk.

No external assets are used. Run:  python3 make_models.py [slug ...] [--preview]
"""
import json
import math
import os
import struct
import sys

import numpy as np

OUT = os.path.join(os.path.dirname(__file__), '..', 'models')


# ------------------------------------------------------------------ mesh helpers
def normals_smooth(V, F):
    n = np.zeros_like(V)
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    for k in range(3):
        np.add.at(n, F[:, k], fn)
    ln = np.linalg.norm(n, axis=1, keepdims=True)
    ln[ln == 0] = 1
    return n / ln


def orient_outward(V, F, center=None):
    c = V.mean(axis=0) if center is None else np.asarray(center, float)
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    cen = V[F].mean(axis=1) - c
    if (fn * cen).sum() < 0:
        F = F[:, ::-1].copy()
    return F


def grid_mesh(P, wrap_u=True, wrap_v=False, center=None):
    R, C, _ = P.shape
    V = P.reshape(-1, 3).astype(np.float64)
    F = []
    rows = R if wrap_v else R - 1
    for i in range(rows):
        i2 = (i + 1) % R
        for j in range(C if wrap_u else C - 1):
            j2 = (j + 1) % C
            a, b, c, d = i * C + j, i * C + j2, i2 * C + j, i2 * C + j2
            F.append((a, c, b))
            F.append((b, c, d))
    F = np.array(F, dtype=np.int64)
    F = orient_outward(V, F, center)
    return V, F, True


def flat_mesh(V, F):
    V = np.asarray(V, float)
    F = np.asarray(F, np.int64)
    V2 = V[F].reshape(-1, 3)
    F2 = np.arange(len(V2)).reshape(-1, 3)
    return V2, F2, False


def lathe(profile, seg=56, scale=(1, 1, 1)):
    """profile: list of (radius, y). Revolves around Y."""
    prof = np.array(profile, float)
    ang = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    P = np.zeros((len(prof), seg, 3))
    for i, (r, y) in enumerate(prof):
        P[i, :, 0] = r * np.cos(ang) * scale[0]
        P[i, :, 1] = y * scale[1]
        P[i, :, 2] = r * np.sin(ang) * scale[2]
    return grid_mesh(P, True, False, center=(0, np.mean(prof[:, 1]) * scale[1], 0))


def sphere(r=1.0, lat=18, lon=28, scale=(1, 1, 1), noise=0.0, seed=0):
    rng = np.random.RandomState(seed)
    th = np.linspace(0, math.pi, lat + 1)
    ph = np.linspace(0, 2 * math.pi, lon, endpoint=False)
    P = np.zeros((lat + 1, lon, 3))
    base = rng.uniform(-1, 1, (lat + 1, lon))
    for i, t in enumerate(th):
        for j, p in enumerate(ph):
            rr = r * (1 + noise * base[i, j]) if 0 < i < lat else r
            P[i, j] = (rr * math.sin(t) * math.cos(p) * scale[0], rr * math.cos(t) * scale[1], rr * math.sin(t) * math.sin(p) * scale[2])
    return grid_mesh(P, True, False, center=(0, 0, 0))


def tube(points, radius, sides=14, taper=None):
    pts = np.asarray(points, float)
    K = len(pts)
    T = np.gradient(pts, axis=0)
    T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
    rings = []
    for k in range(K):
        ref = np.array([0, 0, 1.0]) if abs(T[k][2]) < 0.9 else np.array([0, 1.0, 0])
        N = np.cross(T[k], ref)
        N /= np.linalg.norm(N)
        B = np.cross(T[k], N)
        r = radius * (taper(k / (K - 1)) if taper else 1.0)
        a = np.linspace(0, 2 * math.pi, sides, endpoint=False)
        rings.append(pts[k] + r * (np.outer(np.cos(a), N) + np.outer(np.sin(a), B)))
    rings = [np.tile(pts[0], (sides, 1))] + rings + [np.tile(pts[-1], (sides, 1))]
    P = np.array(rings)
    return grid_mesh(P, True, False, center=pts.mean(axis=0))


def torus(R, r, seg=40, sides=14):
    u = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    v = np.linspace(0, 2 * math.pi, sides, endpoint=False)
    P = np.zeros((seg, sides, 3))
    for i, a in enumerate(u):
        for j, b in enumerate(v):
            P[i, j] = ((R + r * math.cos(b)) * math.cos(a), r * math.sin(b), (R + r * math.cos(b)) * math.sin(a))
    return grid_mesh(P, True, True, center=(0, 0, 0))


def ring_loft(heights, rx, rz, seg=44, cx=None):
    ang = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    P = np.zeros((len(heights), seg, 3))
    for i, y in enumerate(heights):
        c = 0 if cx is None else cx[i]
        P[i, :, 0] = c + rx[i] * np.cos(ang)
        P[i, :, 1] = y
        P[i, :, 2] = rz[i] * np.sin(ang)
    return grid_mesh(P, True, False, center=(0, np.mean(heights), 0))


def box(w, h, d):
    x, y, z = w / 2, h / 2, d / 2
    V = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z], [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]])
    F = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (2, 3, 7), (2, 7, 6), (1, 2, 6), (1, 6, 5), (3, 0, 4), (3, 4, 7)]
    V2, F2, s = flat_mesh(V, F)
    return V2, orient_outward(V2, F2, V.mean(axis=0)), s


def extrude(poly, t):
    """Extrude a convex 2D polygon (list of (x,y)) along z, thickness t. Flat shaded."""
    poly = np.asarray(poly, float)
    n = len(poly)
    c = poly.mean(axis=0)
    V = [(c[0], c[1], t / 2), (c[0], c[1], -t / 2)]
    for p in poly:
        V.append((p[0], p[1], t / 2))
    for p in poly:
        V.append((p[0], p[1], -t / 2))
    F = []
    for i in range(n):
        j = (i + 1) % n
        F.append((0, 2 + i, 2 + j))
        F.append((1, 2 + n + j, 2 + n + i))
        a, b, cc, d = 2 + i, 2 + j, 2 + n + i, 2 + n + j
        F.append((a, cc, b))
        F.append((b, cc, d))
    V = np.array(V)
    V2, F2, s = flat_mesh(V, F)
    return V2, orient_outward(V2, F2, V.mean(axis=0)), s


def xf(mesh, rot=(0, 0, 0), pos=(0, 0, 0), scale=(1, 1, 1)):
    V, F, s = mesh
    V = np.asarray(V, float) * np.asarray(scale)
    rx, ry, rz = [math.radians(a) for a in rot]
    Rx = np.array([[1, 0, 0], [0, math.cos(rx), -math.sin(rx)], [0, math.sin(rx), math.cos(rx)]])
    Ry = np.array([[math.cos(ry), 0, math.sin(ry)], [0, 1, 0], [-math.sin(ry), 0, math.cos(ry)]])
    Rz = np.array([[math.cos(rz), -math.sin(rz), 0], [math.sin(rz), math.cos(rz), 0], [0, 0, 1]])
    V = V @ (Rz @ Ry @ Rx).T + np.asarray(pos)
    return V, F, s


class Model:
    def __init__(self, name):
        self.name = name
        self.parts = []

    def add(self, mesh, color, metal=0.0, rough=0.7, double=False, name='part'):
        V, F, smooth = mesh
        N = normals_smooth(V, F) if smooth else flat_normals(V, F)
        self.parts.append(dict(name=name, V=V.astype(np.float32), N=N.astype(np.float32), F=F.astype(np.uint32),
                               color=color, metal=metal, rough=rough, double=double))

    def write(self, path):
        bins = bytearray()
        views, accs, meshes, mats, nodes = [], [], [], [], []

        def add_view(arr, target):
            off = len(bins)
            bins.extend(arr.tobytes())
            while len(bins) % 4:
                bins.append(0)
            views.append(dict(buffer=0, byteOffset=off, byteLength=arr.nbytes, target=target))
            return len(views) - 1

        for k, p in enumerate(self.parts):
            vp = add_view(p['V'], 34962)
            vn = add_view(p['N'], 34962)
            vi = add_view(p['F'].reshape(-1), 34963)
            mn, mx = p['V'].min(axis=0).tolist(), p['V'].max(axis=0).tolist()
            a0 = len(accs)
            accs.append(dict(bufferView=vp, componentType=5126, count=len(p['V']), type='VEC3', min=mn, max=mx))
            accs.append(dict(bufferView=vn, componentType=5126, count=len(p['N']), type='VEC3'))
            accs.append(dict(bufferView=vi, componentType=5125, count=int(p['F'].size), type='SCALAR'))
            mats.append(dict(name=p['name'], doubleSided=bool(p['double']), pbrMetallicRoughness=dict(
                baseColorFactor=[*p['color'], 1.0], metallicFactor=p['metal'], roughnessFactor=p['rough'])))
            meshes.append(dict(name=p['name'], primitives=[dict(attributes=dict(POSITION=a0, NORMAL=a0 + 1), indices=a0 + 2, material=k)]))
            nodes.append(dict(mesh=k, name=p['name']))
        gltf = dict(asset=dict(version='2.0', generator='kazakh-heritage tools/make_models.py'),
                    scene=0, scenes=[dict(nodes=list(range(len(nodes))))], nodes=nodes, meshes=meshes, materials=mats,
                    accessors=accs, bufferViews=views, buffers=[dict(byteLength=len(bins))])
        js = json.dumps(gltf, separators=(',', ':')).encode()
        while len(js) % 4:
            js += b' '
        total = 12 + 8 + len(js) + 8 + len(bins)
        with open(path, 'wb') as f:
            f.write(struct.pack('<III', 0x46546C67, 2, total))
            f.write(struct.pack('<II', len(js), 0x4E4F534A))
            f.write(js)
            f.write(struct.pack('<II', len(bins), 0x004E4942))
            f.write(bytes(bins))


def flat_normals(V, F):
    fn = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    ln = np.linalg.norm(fn, axis=1, keepdims=True)
    ln[ln == 0] = 1
    fn = fn / ln
    N = np.zeros_like(V)
    for k in range(3):
        N[F[:, k]] = fn
    return N


# ------------------------------------------------------------------ colours
LEATHER = (0.56, 0.34, 0.19)
LEATHERD = (0.38, 0.22, 0.12)
WOOD = (0.76, 0.52, 0.30)
WOODD = (0.46, 0.29, 0.16)
GOLD = (0.78, 0.60, 0.26)
CREAM = (0.95, 0.91, 0.80)
TEAL = (0.12, 0.45, 0.43)
TEALD = (0.09, 0.33, 0.32)
RED = (0.58, 0.16, 0.18)
MEAT = (0.50, 0.27, 0.17)
BROTH = (0.84, 0.66, 0.27)
ONION = (0.97, 0.95, 0.88)
DOUGH = (0.95, 0.88, 0.66)
PLATE = (0.97, 0.96, 0.92)
TURQ = (0.18, 0.56, 0.54)


# ------------------------------------------------------------------ models
def torsyk():
    m = Model('torsyk')
    th = np.linspace(0, math.pi, 40)
    prof = [(1.25 * math.sin(t), 1.0 - 0.95 * math.cos(t)) for t in th]
    prof[0] = (0.0005, prof[0][1])
    prof[-1] = (0.0005, prof[-1][1])
    m.add(lathe(prof, 64, scale=(1, 1, 0.52)), LEATHER, 0.0, 0.8, name='body')
    # seam: tube along the silhouette in the z=0 plane
    seam = [(1.25 * math.sin(t) * 1.002, 1.0 - 0.95 * math.cos(t), 0) for t in np.linspace(0.12, math.pi - 0.12, 60)]
    seam += [(-p[0], p[1], 0) for p in seam[::-1]]
    m.add(tube(seam, 0.028, 8), CREAM, 0, 0.9, name='seam')
    # neck, rim, stopper
    m.add(lathe([(0.001, 1.9), (0.23, 1.9), (0.23, 2.45), (0.001, 2.45)], 32), LEATHERD, 0, 0.8, name='neck')
    m.add(xf(torus(0.26, 0.05, 32, 10), pos=(0, 2.43, 0)), LEATHERD, 0, 0.7, name='rim')
    m.add(lathe([(0.001, 2.4), (0.17, 2.4), (0.19, 2.9), (0.001, 2.93)], 32), WOOD, 0, 0.6, name='stopper')
    # handles and strap
    for s in (-1, 1):
        m.add(xf(torus(0.26, 0.055, 32, 10), rot=(90, 0, 0), pos=(s * 1.18, 1.5, 0)), LEATHERD, 0, 0.7, name='handle')
    strap = [(s * 1.18 * math.cos(a), 1.62 + 1.55 * math.sin(a), 0) for a, s in [(a, 1) for a in np.linspace(0, math.pi, 50)]]
    strap = [(1.18 * math.cos(a), 1.7 + 1.25 * math.sin(a), 0) for a in np.linspace(0, math.pi, 50)]
    m.add(tube(strap, 0.045, 10), LEATHERD, 0, 0.7, name='strap')
    # embossed medallion on both faces
    for s in (-1, 1):
        z = s * 0.52 * 1.25 * 0.99
        m.add(xf(torus(0.55, 0.035, 48, 8), rot=(90, 0, 0), pos=(0, 1.0, z)), LEATHERD, 0, 0.6, name='emboss')
        m.add(xf(torus(0.36, 0.025, 40, 8), rot=(90, 0, 0), pos=(0, 1.0, z)), LEATHERD, 0, 0.6, name='emboss2')
        m.add(xf(extrude([(0, 0.2), (0.12, 0), (0, -0.2), (-0.12, 0)], 0.05), pos=(0, 1.0, z)), GOLD, 0.4, 0.4, name='diamond')
        for k in range(12):
            a = k * math.pi / 6
            m.add(xf(sphere(0.035, 6, 8), pos=(0.7 * math.cos(a), 1.0 + 0.7 * math.sin(a), z)), GOLD, 0.4, 0.4, name='stud')
    return m


def besik():
    m = Model('besik')
    xs = np.linspace(-1.5, 1.5, 40)
    rail_y = lambda x: 0.1 + 0.5 * (x / 1.5) ** 2
    for z in (-0.42, 0.42):
        m.add(tube([(x, rail_y(x), z) for x in xs], 0.06, 12), WOODD, 0, 0.6, name='runner')
        for x in (-1.0, -0.35, 0.35, 1.0):
            m.add(tube([(x, rail_y(x), z), (x, 0.95, z)], 0.05, 10), WOOD, 0, 0.6, name='leg')
    # bed and side boards
    m.add(xf(box(2.5, 0.06, 0.8), pos=(0, 0.93, 0)), WOOD, 0, 0.6, name='bed')
    for z in (-0.42, 0.42):
        m.add(xf(box(2.5, 0.34, 0.06), pos=(0, 1.1, z), rot=(0, 0, 0)), WOOD, 0, 0.6, name='side')
        for k in range(8):
            x = -1.05 + k * 0.3
            m.add(xf(extrude([(0, 0.07), (0.07, 0), (0, -0.07), (-0.07, 0)], 0.075), pos=(x, 1.1, z)), WOODD, 0, 0.6, name='cutout')
    # head and foot boards (arched)
    arch = [(-0.45, 0)] + [(0.45 * math.cos(a), 0.55 * math.sin(a) * 0.55 + 0.0) for a in np.linspace(math.pi, 0, 14)] + [(0.45, 0)]
    arch = [(-0.45, -0.1), (0.45, -0.1)] + [(0.45 * math.cos(a), 0.12 + 0.34 * math.sin(a)) for a in np.linspace(0, math.pi, 16)]
    for x in (-1.27, 1.27):
        m.add(xf(extrude(arch, 0.07), rot=(0, 90, 0), pos=(x, 1.22, 0)), WOOD, 0, 0.6, name='board')
        m.add(xf(sphere(0.07, 10, 14), pos=(x, 1.62, 0)), GOLD, 0.4, 0.4, name='knob')
    # arched bar (belagash)
    bar = [(1.27 * math.cos(a), 1.2 + 0.95 * math.sin(a), 0) for a in np.linspace(math.pi, 0, 40)]
    m.add(tube(bar, 0.055, 12), WOODD, 0, 0.6, name='bar')
    for a in (math.pi * 0.7, math.pi * 0.5, math.pi * 0.3):
        m.add(xf(sphere(0.07, 10, 14), pos=(1.27 * math.cos(a), 1.2 + 0.95 * math.sin(a), 0)), GOLD, 0.4, 0.4, name='bead')
    # swaddled baby
    body = [(-0.55 + 1.1 * t, 1.12, 0) for t in np.linspace(0, 1, 20)]
    m.add(tube(body, 0.2, 18, taper=lambda t: 0.55 + 0.45 * math.sin(math.pi * min(max(t, 0), 1)) ** 0.5), CREAM, 0, 0.9, name='swaddle')
    m.add(xf(sphere(0.17, 16, 20), pos=(-0.62, 1.16, 0)), (0.93, 0.78, 0.66), 0, 0.8, name='head')
    for x in (-0.15, 0.2, 0.55):
        m.add(xf(torus(0.2, 0.025, 28, 8), rot=(0, 0, 90), pos=(x, 1.12, 0)), TURQ, 0, 0.6, name='ribbon')
    # charm hanging from the bar
    m.add(tube([(0, 2.15, 0), (0, 1.75, 0)], 0.012, 6), LEATHERD, 0, 0.8, name='cord')
    m.add(xf(sphere(0.1, 12, 16), pos=(0, 1.68, 0)), TURQ, 0.1, 0.4, name='charm')
    for dx in (-0.1, 0, 0.1):
        m.add(xf(extrude([(0, 0.3), (0.045, 0), (0, -0.3), (-0.045, 0)], 0.01), pos=(dx, 1.43, 0), rot=(0, 0, dx * 80)), CREAM, 0, 0.9, name='feather', double=True)
    return m


def beshbarmak():
    m = Model('beshbarmak')
    m.add(lathe([(0.001, 0.0), (1.35, 0.0), (1.6, 0.07), (1.72, 0.2), (1.68, 0.22), (1.55, 0.13), (1.25, 0.1), (0.001, 0.1)], 72), PLATE, 0.0, 0.35, name='plate')
    for k in range(40):
        a = k * 2 * math.pi / 40
        m.add(xf(extrude([(0, 0.05), (0.04, 0), (0, -0.05), (-0.04, 0)], 0.02), rot=(90, 0, 0), pos=(1.5 * math.cos(a), 0.17, 1.5 * math.sin(a))), TURQ, 0.1, 0.5, name='rimdot')
    rng = np.random.RandomState(4)
    sheets = [(-0.7, -0.2, 20), (0.0, -0.5, -15), (0.7, -0.15, 30), (-0.35, 0.45, -10), (0.45, 0.5, 15), (-0.9, 0.35, 5), (0.95, 0.4, -25), (0.0, 0.0, 40)]
    for i, (x, z, a) in enumerate(sheets):
        poly = [(-0.55, 0), (0, -0.4), (0.55, 0), (0, 0.4)]
        mesh = xf(extrude(poly, 0.025), rot=(90, a, 0), pos=(x, 0.12 + 0.012 * i, z))
        m.add(mesh, DOUGH, 0, 0.8, name='noodle', double=True)
    pieces = [(-0.6, -0.05, 0.3), (0.05, -0.38, 0.34), (0.7, -0.05, 0.3), (-0.3, 0.38, 0.32), (0.4, 0.4, 0.34), (-0.95, 0.3, 0.24), (0.98, 0.35, 0.24)]
    for i, (x, z, r) in enumerate(pieces):
        m.add(xf(sphere(r, 14, 20, scale=(1.2, 0.78, 0.95), noise=0.09, seed=i), pos=(x, 0.32 + 0.02 * (i % 3), z), rot=(0, i * 40, 0)), MEAT, 0, 0.6, name='meat')
    for i in range(10):
        a = i * 0.9
        R = 0.28 + 0.06 * (i % 3)
        m.add(xf(torus(R, 0.035, 26, 8), pos=(-0.15 + 0.35 * math.cos(a) * (0.3 + 0.07 * i), 0.56 + 0.012 * i, 0.05 + 0.3 * math.sin(a) * (0.3 + 0.05 * i)), rot=(rng.uniform(-14, 14), rng.uniform(0, 360), rng.uniform(-14, 14))), ONION, 0, 0.5, name='onion')
    bowl = [(0.001, 0.0), (0.35, 0.0), (0.55, 0.12), (0.72, 0.45), (0.76, 0.5), (0.7, 0.5), (0.52, 0.17), (0.001, 0.1)]
    m.add(xf(lathe(bowl, 56), pos=(2.55, 0, 0.2)), TEAL, 0.0, 0.4, name='bowl')
    m.add(xf(lathe([(0.001, 0.0), (0.66, 0.0), (0.66, 0.015), (0.001, 0.015)], 56), pos=(2.55, 0.42, 0.2)), BROTH, 0.0, 0.2, name='broth')
    for k in range(8):
        a = k * math.pi / 4
        m.add(xf(extrude([(0, 0.05), (0.035, 0), (0, -0.05), (-0.035, 0)], 0.02), rot=(0, -math.degrees(a), 0), pos=(2.55 + 0.7 * math.cos(a), 0.3, 0.2 + 0.7 * math.sin(a))), GOLD, 0.3, 0.4, name='bowldeco')
    return m


def shapan():
    m = Model('shapan')
    hs = [0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.25, 2.4]
    rx = [1.05, 0.96, 0.82, 0.66, 0.6, 0.62, 0.4, 0.2]
    rz = [0.42, 0.38, 0.33, 0.29, 0.28, 0.28, 0.2, 0.16]
    m.add(ring_loft(hs, rx, rz, 48), TEAL, 0, 0.85, double=True, name='robe')
    # hem band, waist-less trim and collar
    m.add(ring_loft([0.0, 0.17], [1.075, 1.04], [0.44, 0.425], 48), GOLD, 0.35, 0.45, double=True, name='hem')
    m.add(ring_loft([2.3, 2.46], [0.34, 0.24], [0.23, 0.19], 40), GOLD, 0.35, 0.45, double=True, name='collar')
    # centre front placket
    m.add(xf(box(0.16, 2.2, 0.03), pos=(0, 1.1, 0.4 + 0.01 * 0)), GOLD, 0.35, 0.45, name='placket')
    for k in range(9):
        y = 0.35 + k * 0.23
        m.add(xf(extrude([(0, 0.06), (0.04, 0), (0, -0.06), (-0.04, 0)], 0.04), pos=(0, y, 0.42 - 0.01 * abs(y - 1.2) * 0.2 + 0.0)), RED, 0, 0.6, name='placketdiamond')
    # sleeves
    for s in (-1, 1):
        d = np.array([s * 0.82, -0.57])
        ang = math.degrees(math.atan2(-d[0], d[1]))
        sl = ring_loft([0.0, 0.5, 1.0, 1.5], [0.24, 0.26, 0.29, 0.31], [0.22, 0.24, 0.26, 0.28], 36)
        m.add(xf(sl, rot=(0, 0, ang), pos=(s * 0.55, 2.02, 0)), (0.10, 0.40, 0.39), 0, 0.85, double=True, name='sleeve')
        cuff = ring_loft([1.42, 1.58], [0.315, 0.325], [0.285, 0.295], 36)
        m.add(xf(cuff, rot=(0, 0, ang), pos=(s * 0.55, 2.02, 0)), GOLD, 0.35, 0.45, double=True, name='cuff')
        end = np.array([s * 0.55, 2.02]) + 1.5 * np.array([math.sin(math.radians(-ang)) * -1, 0])
    # ram-horn ornaments (small spirals) on the hem
    for k in range(-3, 4):
        x = k * 0.28
        pts = [(x + 0.05 * math.cos(t) * t * 0.35, 0.34 + 0.05 * math.sin(t) * t * 0.35, 0.435) for t in np.linspace(0, 9, 30)]
        m.add(tube(pts, 0.012, 6), GOLD, 0.35, 0.4, name='ram')
    return m


BUILD = {'torsyk': torsyk, 'besik': besik, 'beshbarmak': beshbarmak, 'shapan': shapan}


# ------------------------------------------------------------------ preview (software renderer)
def render_preview(model, size=520, yaw=35, pitch=18):
    import cv2
    img = np.full((size, size, 3), (232, 238, 238), np.uint8)
    allv = np.concatenate([p['V'] for p in model.parts])
    c = (allv.min(axis=0) + allv.max(axis=0)) / 2
    rad = np.linalg.norm(allv - c, axis=1).max()
    ya, pa = math.radians(yaw), math.radians(pitch)
    Ry = np.array([[math.cos(ya), 0, math.sin(ya)], [0, 1, 0], [-math.sin(ya), 0, math.cos(ya)]])
    Rx = np.array([[1, 0, 0], [0, math.cos(pa), -math.sin(pa)], [0, math.sin(pa), math.cos(pa)]])
    R = Rx @ Ry
    light = np.array([0.4, 0.8, 0.6])
    light /= np.linalg.norm(light)
    tris = []
    for p in model.parts:
        V = ((p['V'] - c) @ R.T)
        F = p['F']
        Nf = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
        ln = np.linalg.norm(Nf, axis=1, keepdims=True)
        ln[ln == 0] = 1
        Nf = Nf / ln
        dep = V[F][:, :, 2].mean(axis=1)
        for fi in range(len(F)):
            n = Nf[fi]
            if n[2] < 0 and not p['double']:
                continue
            shade = 0.35 + 0.65 * abs(n @ light)
            col = np.array(p['color']) * shade * 255
            tris.append((dep[fi], V[F[fi]], col))
    tris.sort(key=lambda t: t[0])
    sc = size * 0.42 / rad
    for _, v, col in tris:
        pts = np.array([[size / 2 + v[k][0] * sc, size / 2 - v[k][1] * sc] for k in range(3)], np.int32)
        cv2.fillConvexPoly(img, pts, (int(col[2]), int(col[1]), int(col[0])), lineType=cv2.LINE_AA)
    return img


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    names = args or list(BUILD)
    sheet = []
    for n in names:
        mdl = BUILD[n]()
        path = os.path.join(OUT, f'{n}.glb')
        mdl.write(path)
        tri = sum(len(p['F']) for p in mdl.parts)
        print(n, os.path.getsize(path) // 1024, 'KB', tri, 'triangles')
        if '--preview' in sys.argv:
            sheet.append(np.hstack([render_preview(mdl, 440, 35, 18), render_preview(mdl, 440, 150, 12)]))
    if sheet:
        import cv2
        cv2.imwrite(os.path.join(os.path.dirname(__file__), '_models.png'), np.vstack(sheet))
