"""Original flat-style illustrations of the eight Kazakh objects.

Each `build_<slug>()` returns a Scene: a list of layers (RGBA images, 720x640)
with timing, plus caption texts. Everything is drawn from code - no external art.
"""
import math
from dataclasses import dataclass, field
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops
from scipy.interpolate import PchipInterpolator

W, H, S = 720, 640, 2

IVORY = (251, 247, 238)
CREAM = (246, 239, 224)
SAND = (233, 220, 195)
BEIGE = (217, 199, 164)
BROWN = (59, 42, 30)
BROWNSOFT = (107, 84, 66)
TURQ = (47, 143, 139)
TURQD = (31, 107, 104)
GOLD = (184, 146, 74)
GOLDL = (236, 220, 182)
WOOD = (176, 118, 66)
WOODL = (208, 154, 96)
WOODD = (116, 74, 42)
RED = (142, 45, 50)
REDL = (176, 70, 70)
LEATHER = (150, 92, 52)
LEATHERD = (110, 66, 36)
FELT = (243, 236, 220)

FONT_UI = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'


def ui_font(size):
    return ImageFont.truetype(FONT_UI, int(size * S))


def bez(p0, p1, p2, p3, n=48):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


def rotpt(p, deg, c):
    """Rotate point like PIL Image.rotate(deg) (counter-clockwise on screen)."""
    a = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) + y * math.sin(a), c[1] - x * math.sin(a) + y * math.cos(a))


def prof_poly(cx, prof, n=90):
    ys = [p[0] for p in prof]
    hs = [p[1] for p in prof]
    f = PchipInterpolator(ys, hs)
    yy = np.linspace(ys[0], ys[-1], n)
    left = [(cx - float(f(y)), float(y)) for y in yy]
    right = [(cx + float(f(y)), float(y)) for y in yy[::-1]]
    return left + right


def spiral(cx, cy, r0, r1, turns, start=0.0, n=40, cw=1):
    pts = []
    for i in range(n + 1):
        t = i / n
        a = start + cw * t * turns * 2 * math.pi
        r = r0 + (r1 - r0) * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class Cv:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.img = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def P(self, pts):
        return [(x * S, y * S) for x, y in pts]

    def poly(self, pts, fill=None, outline=None, w=0):
        if fill:
            self.d.polygon(self.P(pts), fill=fill)
        if outline:
            self.d.line(self.P(list(pts) + [pts[0]]), fill=outline, width=max(1, int(w * S)), joint='curve')

    def line(self, pts, fill, w=2, round_caps=True):
        self.d.line(self.P(pts), fill=fill, width=max(1, int(w * S)), joint='curve')
        if round_caps and w >= 3:
            r = w / 2
            for p in (pts[0], pts[-1]):
                self.circle(p[0], p[1], r, fill=fill)

    def circle(self, cx, cy, r, fill=None, outline=None, w=0):
        self.ell((cx - r, cy - r, cx + r, cy + r), fill, outline, w)

    def ell(self, box, fill=None, outline=None, w=0):
        b = [box[0] * S, box[1] * S, box[2] * S, box[3] * S]
        self.d.ellipse(b, fill=fill, outline=outline, width=max(1, int(w * S)) if outline else 0)

    def arc(self, box, a0, a1, fill, w=2):
        b = [box[0] * S, box[1] * S, box[2] * S, box[3] * S]
        self.d.arc(b, a0, a1, fill=fill, width=max(1, int(w * S)))

    def rrect(self, box, r, fill=None, outline=None, w=0):
        b = [box[0] * S, box[1] * S, box[2] * S, box[3] * S]
        self.d.rounded_rectangle(b, radius=r * S, fill=fill, outline=outline, width=max(1, int(w * S)) if outline else 0)

    def text(self, xy, s, font, fill):
        self.d.text((xy[0] * S, xy[1] * S), s, font=font, fill=fill)

    def clip_rect(self, rect):
        m = Image.new('L', self.img.size, 0)
        ImageDraw.Draw(m).rectangle([rect[0] * S, rect[1] * S, rect[2] * S, rect[3] * S], fill=255)
        self.img.putalpha(ImageChops.multiply(self.img.getchannel('A'), m))
        self.d = ImageDraw.Draw(self.img)

    def paste(self, other):
        self.img.alpha_composite(other.img)
        self.d = ImageDraw.Draw(self.img)

    def rotate(self, deg, center):
        self.img = self.img.rotate(deg, center=(center[0] * S, center[1] * S), resample=Image.BICUBIC)
        self.d = ImageDraw.Draw(self.img)

    def out(self):
        return self.img.resize((self.w, self.h), Image.LANCZOS)


@dataclass
class Layer:
    name: str
    img: Image.Image
    t0: float
    dur: float = 1.0
    effect: str = 'fade'   # fade | rise | drop | grow
    sway: tuple = None      # (amp_px, period_s) horizontal
    rock: tuple = None      # (deg, period_s, pivot_x, pivot_y)
    float_: tuple = None    # (amp_px, period_s) vertical drift


@dataclass
class Scene:
    slug: str
    layers: list
    captions: list          # 4 strings
    native: str
    title: str
    subtitle: str


# ---------------------------------------------------------------- labels
def label_layer(text, anchor, pos, t0, name='label'):
    """Pill label at pos (top-left) with a leader line to anchor."""
    font = ui_font(20)
    lines = text.split('\n')
    tmp = Image.new('RGBA', (10, 10))
    td = ImageDraw.Draw(tmp)
    tw = max(td.textlength(l, font=font) for l in lines) / S
    lh = 26
    pw, ph = tw + 26, lh * len(lines) + 14
    x, y = pos
    c = Cv()
    # leader line from nearest pill point to anchor
    cx = min(max(anchor[0], x + 12), x + pw - 12)
    cy = y + ph / 2 if abs(anchor[1] - (y + ph / 2)) < ph / 2 + 2 else (y if anchor[1] < y else y + ph)
    c.line([(cx, cy), anchor], GOLD, 2.5, round_caps=False)
    c.circle(anchor[0], anchor[1], 7, fill=TURQ, outline=IVORY, w=2.5)
    c.rrect((x, y, x + pw, y + ph), 13, fill=IVORY, outline=GOLD, w=2)
    for i, l in enumerate(lines):
        c.text((x + 13, y + 7 + i * lh), l, font, BROWN)
    return Layer(name, c.out(), t0, 0.7, 'rise')


def L(name, cv, t0, dur=1.0, effect='fade', **kw):
    return Layer(name, cv.out(), t0, dur, effect, **kw)


# ---------------------------------------------------------------- 1 DOMBRA
def build_dombra():
    cx = 360
    prof = [(332, 24), (350, 36), (380, 66), (420, 102), (470, 124), (520, 122), (560, 100), (588, 56), (600, 0)]
    piv = (360, 330)
    ang = -18

    c = Cv()
    body = prof_poly(cx, prof)
    c.poly(body, fill=WOODL, outline=BROWN, w=3.5)
    inner = prof_poly(cx, [(p[0] + (10 if i == 0 else 0), max(p[1] - 13, 0)) for i, p in enumerate(prof)][:-1] + [(594, 0)])
    c.line(inner + [inner[0]], GOLD, 2.2, round_caps=False)
    c.circle(cx, 495, 31, fill=BROWN)
    c.circle(cx, 495, 38, outline=GOLD, w=3)
    for k in range(10):
        a = k * 2 * math.pi / 10
        c.circle(cx + 52 * math.cos(a), 495 + 52 * math.sin(a), 4, fill=TURQ)
    for sgn in (-1, 1):
        c.line(bez((cx + sgn * 40, 420), (cx + sgn * 80, 400), (cx + sgn * 90, 440), (cx + sgn * 70, 450)), GOLD, 2.5, False)
        c.circle(cx + sgn * 66, 452, 4, fill=GOLD)
    c.rrect((322, 546, 398, 558), 4, fill=WOODD)
    c.rotate(ang, piv)
    body_l = L('body', c, 4.0, 1.2, 'rise')

    c = Cv()
    c.rrect((337, 118, 383, 345), 6, fill=WOODD, outline=BROWN, w=3)
    c.rrect((344, 140, 376, 342), 3, fill=(78, 50, 30))
    for y in range(172, 340, 22):
        c.line([(344, y), (376, y)], BEIGE, 3, False)
    c.rotate(ang, piv)
    neck_l = L('neck', c, 7.5, 1.2, 'rise')

    c = Cv()
    c.rrect((326, 58, 394, 130), 20, fill=WOOD, outline=BROWN, w=3)
    c.rect = None
    c.line([(310, 88), (332, 88)], BROWN, 4)
    c.line([(388, 108), (410, 108)], BROWN, 4)
    c.ell((296, 80, 316, 96), fill=TURQ, outline=BROWN, w=2.5)
    c.ell((404, 100, 424, 116), fill=GOLD, outline=BROWN, w=2.5)
    c.rrect((338, 124, 382, 132), 3, fill=BEIGE, outline=BROWN, w=1.5)
    c.rotate(ang, piv)
    head_l = L('head', c, 7.8, 1.0, 'drop')

    c = Cv()
    for x in (352, 368):
        c.line([(x + 1.5, 112), (x + 1.5, 552)], (60, 40, 25, 110), 2.6, False)
        c.line([(x, 112), (x, 552)], (250, 246, 232), 2.4, False)
    c.rotate(ang, piv)
    strings_l = L('strings', c, 12.0, 1.4, 'fade')

    R = lambda p: rotpt(p, ang, piv)
    labels = [
        label_layer('Wooden body', R((420, 520)), (500, 560), 5.0),
        label_layer('Long neck\nwith frets', R((378, 250)), (470, 190), 8.5),
        label_layer('Two strings', R((368, 390)), (460, 330), 12.6),
    ]
    layers = [body_l, neck_l, head_l, strings_l] + labels
    return Scene('dombra', layers, [
        'The dombra is the best-loved instrument of the Kazakh people.',
        'A small wooden body, a long neck and just two strings.',
        'The right hand strums while the left presses the frets to shape the melody.',
        'Akyns, the poet-singers, sing with it, and kuy pieces tell stories without words.',
    ], 'Домбыра', 'Dombra', 'The two-string voice of the steppe')


# ---------------------------------------------------------------- 2 YURT
def build_yurt():
    c = Cv()
    c.ell((60, 500, 660, 552), fill=(217, 199, 164, 200))
    c.line([(40, 522), (680, 522)], GOLD, 3, False)
    for x in range(70, 660, 38):
        c.line([(x, 522), (x - 5, 508)], (150, 130, 70), 2.5, False)
        c.line([(x + 6, 522), (x + 10, 506)], (150, 130, 70), 2.5, False)
    ground = L('ground', c, 0.3, 1.0)

    # kerege lattice
    sub = Cv()
    step = 46
    for k in range(-8, 18):
        x = 100 + k * step
        sub.line([(x, 330), (x + 190, 522)], WOODD, 8, False)
        sub.line([(x + 190, 330), (x, 522)], WOODD, 8, False)
    for k in range(-8, 18):
        x = 100 + k * step
        sub.line([(x, 330), (x + 190, 522)], WOODL, 4, False)
        sub.line([(x + 190, 330), (x, 522)], WOODL, 4, False)
    sub.clip_rect((120, 330, 600, 522))
    c = Cv()
    c.rrect((120, 330, 600, 522), 2, fill=(246, 239, 224, 255))
    c.paste(sub)
    c.rrect((112, 326, 128, 524), 4, fill=WOODD)
    c.rrect((592, 326, 608, 524), 4, fill=WOODD)
    kerege = L('kerege', c, 5.0, 1.4, 'rise')

    # uyk poles
    c = Cv()
    ring_c = (360, 192)
    xs = np.linspace(128, 592, 13)
    for x in xs:
        rx = 360 + (x - 360) * 0.12
        pts = bez((x, 330), (x + (360 - x) * 0.04, 262), (rx - (rx - 360) * 0.3 + (x - 360) * 0.02, 226), (rx, ring_c[1] + 6))
        c.line(pts, WOODD, 8, False)
    for x in xs:
        rx = 360 + (x - 360) * 0.12
        pts = bez((x, 330), (x + (360 - x) * 0.04, 262), (rx - (rx - 360) * 0.3 + (x - 360) * 0.02, 226), (rx, ring_c[1] + 6))
        c.line(pts, WOODL, 4, False)
    uyk = L('uyk', c, 9.0, 1.4, 'fade')

    # felt covering
    c = Cv()
    left = bez((112, 330), (126, 250), (230, 206), (310, 192))
    right = bez((410, 192), (490, 206), (594, 250), (608, 330))
    sil = [(112, 524)] + left + right + [(608, 524)]
    c.poly(sil, fill=FELT, outline=BROWN, w=4)
    for k, x in enumerate(np.linspace(150, 570, 8)):
        rx = 360 + (x - 360) * 0.1
        c.line(bez((x, 330), (x + (360 - x) * 0.05, 270), (rx - (rx - 360) * 0.3, 232), (rx, 206)), BEIGE, 2.4, False)
    for x in (230, 360, 490):
        c.line([(x, 330), (x, 524)], BEIGE, 2.4, False)
    c.line([(112, 330), (608, 330)], BEIGE, 3, False)
    # shading on lower wall
    shade = Cv()
    shade.rrect((112, 470, 608, 524), 2, fill=(160, 130, 90, 40))
    c.paste(shade)
    felt = L('felt', c, 20.0, 1.6, 'fade')

    # shanyrak (top of the felt)
    c = Cv()
    c.ell((300, 172, 420, 214), fill=(70, 56, 44), outline=WOODD, w=9)
    c.ell((306, 177, 414, 209), outline=WOODL, w=3.5)
    c.line([(306, 193), (414, 193)], WOODD, 6, False)
    c.line([(360, 177), (360, 209)], WOODD, 6, False)
    c.circle(360, 193, 7, fill=GOLD, outline=WOODD, w=2)
    shan = L('shanyrak', c, 13.0, 1.2, 'drop')

    # ornament band + door
    c = Cv()
    c.rrect((112, 372, 608, 408), 2, fill=TURQ)
    c.rrect((112, 372, 608, 380), 0, fill=TURQD)
    for x in range(132, 608, 34):
        c.poly([(x, 390), (x + 12, 378), (x + 24, 390), (x + 12, 402)], fill=GOLD, outline=IVORY, w=1.5)
    c.rrect((112, 412, 608, 420), 0, fill=RED)
    c.rrect((316, 420, 404, 524), 0, fill=WOODD)
    c.ell((316, 392, 404, 452), fill=WOODD)
    c.rrect((322, 428, 398, 524), 0, fill=WOOD)
    c.ell((322, 398, 398, 458), fill=WOOD)
    c.line([(360, 420), (360, 524)], WOODD, 3, False)
    c.poly([(360, 446), (376, 466), (360, 486), (344, 466)], outline=GOLDL, w=2.5)
    c.circle(348, 480, 3.5, fill=GOLD)
    c.circle(372, 480, 3.5, fill=GOLD)
    door = L('door', c, 24.0, 1.4, 'rise')

    labels = [
        label_layer('Kerege\nlattice walls', (150, 470), (24, 548), 5.8),
        label_layer('Uyk roof poles', (205, 262), (22, 150), 10.0),
        label_layer('Shanyrak\ncrown ring', (360, 192), (470, 96), 13.8),
        label_layer('Felt covering', (540, 300), (480, 234), 21.0),
    ]
    layers = [ground, kerege, uyk, felt, shan, door] + labels
    return Scene('yurt', layers, [
        'The yurt, kiyiz uy, is the felt house of the steppe.',
        'Kerege lattice walls fold open, and uyk poles rise to the crown ring, the shanyrak.',
        'Thick felt keeps the home warm in winter and cool in summer.',
        'A family could take it down and raise it again within hours.',
    ], 'Киіз үй', 'Kazakh Yurt', 'The portable home of the nomads')


# ---------------------------------------------------------------- 3 KOBYZ
def build_kobyz():
    cx = 360
    piv = (360, 340)
    ang = 6

    c = Cv()
    prof = [(372, 40), (398, 82), (445, 112), (505, 120), (558, 102), (588, 58), (602, 0)]
    body = prof_poly(cx, prof)
    c.poly(body, fill=WOOD, outline=BROWN, w=3.5)
    # leather lid
    lid = prof_poly(cx, [(392, 22), (420, 64), (462, 90), (510, 98), (552, 82), (576, 46), (586, 0)])
    c.poly(lid, fill=(222, 186, 132), outline=BROWNSOFT, w=2.5)
    pts = lid
    for i in range(0, len(pts), 3):
        c.circle(pts[i][0], pts[i][1], 2.2, fill=BROWNSOFT)
    for k in range(5):
        c.poly([(cx - 40 + k * 20, 540), (cx - 32 + k * 20, 532), (cx - 24 + k * 20, 540), (cx - 32 + k * 20, 548)], fill=GOLD)
    c.rrect((330, 552, 390, 566), 4, fill=WOODD)
    c.rrect((334, 506, 386, 514), 3, fill=WOODD)
    c.rotate(ang, piv)
    body_l = L('body', c, 4.0, 1.2, 'rise')

    c = Cv()
    c.poly([(340, 150), (380, 150), (390, 384), (330, 384)], fill=WOODD, outline=BROWN, w=3)
    c.line(bez((360, 150), (362, 110), (330, 84), (318, 60)), WOODD, 30)
    c.line(bez((360, 150), (362, 110), (330, 84), (318, 60)), BROWN, 3, False)
    c.circle(312, 56, 17, fill=WOODL, outline=BROWN, w=3)
    c.circle(306, 52, 3.5, fill=BROWN)
    c.line([(332, 150), (312, 150)], BROWN, 4)
    c.line([(388, 170), (408, 170)], BROWN, 4)
    c.ell((294, 140, 314, 158), fill=TURQ, outline=BROWN, w=2.5)
    c.ell((404, 160, 424, 178), fill=GOLD, outline=BROWN, w=2.5)
    c.rotate(ang, piv)
    neck_l = L('neck', c, 7.5, 1.2, 'rise')

    c = Cv()
    for x in (353, 367):
        c.line([(x + 1.5, 160), (x + 1.5, 560)], (60, 40, 25, 110), 2.6, False)
        c.line([(x, 160), (x, 560)], (235, 228, 210), 2.4, False)
    c.rotate(ang, piv)
    strings_l = L('strings', c, 11.5, 1.3, 'fade')

    c = Cv()
    stick = bez((70, 470), (250, 380), (480, 380), (650, 470))
    c.line(stick, WOODD, 9)
    c.line(stick, WOODL, 4)
    c.line([(70, 470), (650, 470)], (250, 246, 232), 5, False)
    c.line([(70, 470), (650, 470)], (190, 180, 160), 1.5, False)
    c.rrect((58, 458, 96, 482), 8, fill=GOLD, outline=BROWN, w=2.5)
    bow = L('bow', c, 15.5, 1.2, 'fade', sway=(44, 3.6))

    R = lambda p: rotpt(p, ang, piv)
    labels = [
        label_layer('Hollowed\nwooden body', R((418, 520)), (500, 560), 4.8),
        label_layer('Long neck', R((372, 260)), (452, 220), 8.2),
        label_layer('Two horsehair\nstrings', R((367, 330)), (60, 300), 12.0),
        label_layer('Horsehair bow', (190, 410), (36, 188), 16.0),
    ]
    layers = [body_l, neck_l, strings_l, bow] + labels
    return Scene('kobyz', layers, [
        'The kobyz is an ancient bowed instrument of the steppe.',
        'Its hollowed wooden body joins a long neck with two horsehair strings.',
        'A horsehair bow draws out a low, husky, haunting voice.',
        'It is linked with the baqsy healers and the legend of Korkyt Ata.',
    ], 'Қобыз', 'Kobyz', 'The ancient bowed instrument')


# ---------------------------------------------------------------- 4 SAUKELE
def build_saukele():
    cx = 360
    c = Cv()
    veil = [(cx, 120)] + bez((cx, 120), (300, 200), (200, 330), (160, 600)) + bez((160, 600), (260, 620), (460, 620), (560, 600)) + bez((560, 600), (520, 330), (420, 200), (cx, 120))
    c.poly(veil, fill=(255, 252, 244, 210), outline=(217, 199, 164), w=2.5)
    for k in range(7):
        x = 190 + k * 56
        c.line(bez((cx, 170), (cx + (x - cx) * 0.3, 300), (x, 420), (x, 600)), (217, 199, 164, 160), 1.8, False)
    veil_l = L('veil', c, 4.0, 1.4, 'fade')

    def half(y):  # half width of the cone at height y
        t = (y - 98) / (430 - 98)
        return 128 * (max(t, 0) ** 0.92)

    c = Cv()
    ys = np.linspace(98, 430, 60)
    cone = [(cx - half(y), y) for y in ys] + [(cx + half(y), y) for y in ys[::-1]]
    c.poly(cone, fill=RED, outline=BROWN, w=3.5)
    c.ell((cx - 128, 410, cx + 128, 452), fill=(110, 30, 38), outline=BROWN, w=3)
    # highlight
    hl = Cv()
    hl.poly([(cx - 20, 110), (cx - 6, 110), (cx - 70, 425), (cx - 105, 425)], fill=(255, 255, 255, 38))
    c.paste(hl)
    cone_l = L('cone', c, 6.5, 1.4, 'rise')

    c = Cv()
    for y in (180, 250, 320, 392):
        w = half(y)
        c.arc((cx - w, y - 14, cx + w, y + 14), 0, 180, GOLD, 5)
        c.arc((cx - w, y - 4, cx + w, y + 24), 0, 180, GOLDL, 2.5)
    for y in (215, 285, 356):
        w = half(y) - 14
        n = max(int(w // 22), 1)
        for k in range(-n, n + 1):
            x = cx + k * 24 * (1 if n else 0)
            c.poly([(x, y - 8 + 8), (x + 9, y + 1), (x, y + 10 + 8), (x - 9, y + 1)], fill=GOLD)
    bands_l = L('bands', c, 11.0, 1.4, 'fade')

    c = Cv()
    for (x, y, r, col) in [(cx, 200, 9, TURQ), (cx - 34, 268, 8, (200, 70, 60)), (cx + 34, 268, 8, (200, 70, 60)),
                           (cx, 270, 10, TURQ), (cx - 70, 338, 8, TURQ), (cx + 70, 338, 8, TURQ),
                           (cx, 340, 11, (200, 70, 60)), (cx - 36, 342, 7, GOLDL), (cx + 36, 342, 7, GOLDL)]:
        c.circle(x, y, r + 3, fill=GOLD)
        c.circle(x, y, r, fill=col, outline=IVORY, w=1.5)
    for k in range(-5, 6):
        x = cx + k * 21
        c.circle(x, 430 + 8 * (1 - abs(k) / 6), 5, fill=IVORY, outline=BEIGE, w=1)
    jewels = L('jewels', c, 15.0, 1.2, 'fade')

    c = Cv()
    for sgn in (-1, 1):
        for k, x0 in enumerate((128, 106, 148)):
            x = cx + sgn * x0
            top = 440 + k * 4
            n = 7 + (1 if k == 0 else 0)
            for j in range(n):
                y = top + 10 + j * 18
                c.circle(x, y, 5.5, fill=[TURQ, IVORY, (200, 70, 60), GOLD][j % 4], outline=BROWNSOFT, w=1.2)
            c.line([(x, top), (x, top + 10 + (n - 1) * 18)], (150, 130, 100), 1.5, False)
            yb = top + 10 + n * 18
            c.poly([(x, yb - 4), (x + 8, yb + 8), (x, yb + 24), (x - 8, yb + 8)], fill=GOLD, outline=BROWN, w=1.5)
    pend = L('pendants', c, 18.0, 1.5, 'drop')

    c = Cv()
    c.circle(cx, 96, 12, fill=GOLD, outline=BROWN, w=2.5)
    for sgn in (-1, 1):
        c.line(bez((cx, 90), (cx + sgn * 20, 50), (cx + sgn * 40, 30), (cx + sgn * 30, 6)), BROWNSOFT, 3)
        for k in range(6):
            t = 0.2 + k * 0.14
            p = bez((cx, 90), (cx + sgn * 20, 50), (cx + sgn * 40, 30), (cx + sgn * 30, 6))[int(t * 48)]
            c.line([p, (p[0] + sgn * 14, p[1] - 4)], BROWNSOFT, 2, False)
    crest = L('crest', c, 12.5, 1.0, 'drop')

    labels = [
        label_layer('Velvet cone', (cx + 60, 300), (500, 262), 7.0),
        label_layer('Silver and gold\nembroidery', (cx - 70, 250), (20, 200), 11.6),
        label_layer('Feather crest', (cx + 24, 30), (470, 18), 13.0),
        label_layer('Beaded pendants', (cx - 128, 520), (18, 560), 18.8),
    ]
    layers = [veil_l, cone_l, bands_l, jewels, crest, pend] + labels
    return Scene('saukele', layers, [
        'The saukele crowns a Kazakh bride on her wedding day.',
        'A tall cone of velvet, covered with silver and gilded ornament.',
        'Coral, pearls and stones sparkle, with beaded strands framing the face.',
        "Made over months, it carries the family's pride and good wishes.",
    ], 'Сәукеле', 'Saukele', "The bride's crowning headdress")


# ---------------------------------------------------------------- 5 SHAPAN
def build_shapan():
    cx = 360
    BODY = TURQD
    LINING = (240, 226, 196)

    c = Cv()
    def side(sgn):
        return [(cx + sgn * 98, 172), (cx + sgn * 140, 330), (cx + sgn * 182, 572)]
    left = [(cx - 98, 172), (cx - 130, 330), (cx - 182, 572), (cx - 6, 572)]
    right = [(cx + 98, 172), (cx + 130, 330), (cx + 182, 572), (cx + 6, 572)]
    collar = [(cx - 40, 150), (cx, 238), (cx + 40, 150)]
    c.poly(left + [(cx - 6, 238)] + [(cx - 40, 150)], fill=BODY, outline=BROWN, w=3.5)
    c.poly(right + [(cx + 6, 238)] + [(cx + 40, 150)], fill=BODY, outline=BROWN, w=3.5)
    c.poly([(cx - 40, 150), (cx, 238), (cx + 40, 150), (cx + 98, 172), (cx + 6, 238), (cx + 6, 572), (cx - 6, 572), (cx - 6, 238), (cx - 98, 172)], fill=None)
    # inner lining visible at the opening
    c.poly([(cx - 6, 238), (cx + 6, 238), (cx + 6, 572), (cx - 6, 572)], fill=LINING, outline=BROWN, w=2)
    c.poly([(cx - 40, 150), (cx, 238), (cx + 40, 150), (cx + 20, 142), (cx, 160), (cx - 20, 142)], fill=LINING, outline=BROWN, w=2.5)
    robe_body = L('robe', c, 4.5, 1.4, 'rise')

    c = Cv()
    for sgn in (-1, 1):
        sl = [(cx + sgn * 98, 172), (cx + sgn * 232, 262), (cx + sgn * 268, 470), (cx + sgn * 188, 478), (cx + sgn * 152, 336), (cx + sgn * 126, 296)]
        c.poly(sl, fill=(36, 118, 114), outline=BROWN, w=3.5)
        cuff = [(cx + sgn * 268, 470), (cx + sgn * 188, 478), (cx + sgn * 184, 446), (cx + sgn * 262, 438)]
        c.poly(cuff, fill=GOLD, outline=BROWN, w=2.5)
    sleeves = L('sleeves', c, 9.0, 1.3, 'rise')

    c = Cv()
    # trim bands: front edges, hem, collar
    for sgn in (-1, 1):
        x0, x1 = (cx + sgn * 6, cx + sgn * 24)
        c.poly([(x0, 238), (x1, 238), (x1, 572), (x0, 572)], fill=GOLD, outline=BROWN, w=2)
        for y in range(256, 566, 26):
            c.poly([(cx + sgn * 15, y), (cx + sgn * 21, y + 8), (cx + sgn * 15, y + 16), (cx + sgn * 9, y + 8)], fill=RED)
    c.poly([(cx - 182, 548), (cx + 182, 548), (cx + 184, 572), (cx - 184, 572)], fill=GOLD, outline=BROWN, w=2.5)
    for x in range(cx - 168, cx + 168, 28):
        c.poly([(x, 560), (x + 8, 552), (x + 16, 560), (x + 8, 568)], fill=RED)
    c.line([(cx - 40, 150), (cx, 238), (cx + 40, 150)], GOLD, 7)
    trim = L('trim', c, 13.5, 1.3, 'fade')

    c = Cv()
    def ram(x, y, s, sgn=1):
        a = spiral(x, y, 2, 14 * s, 1.3, start=math.pi, n=30, cw=sgn)
        b = spiral(x + 26 * s * sgn, y, 2, 14 * s, 1.3, start=0, n=30, cw=-sgn)
        c.line(a, GOLD, 3.2, False)
        c.line(b, GOLD, 3.2, False)
    for sgn in (-1, 1):
        ram(cx + sgn * 242 - 12, 400, 0.9)
        ram(cx + sgn * 80 - 12, 480, 0.9)
        ram(cx + sgn * 120 - 12, 380, 0.7)
    ram(cx - 13, 190, 0.7)
    orn = L('ornament', c, 17.5, 1.3, 'fade')

    labels = [
        label_layer('Wool, camel hair\nor velvet', (cx - 150, 430), (20, 520), 5.5),
        label_layer('Wide sleeves', (cx + 238, 330), (500, 262), 9.6),
        label_layer('Braided trim', (cx + 15, 500), (470, 574), 13.8),
        label_layer('Ram-horn\nornament', (cx + 238, 400), (540, 470), 18.0),
    ]
    layers = [robe_body, sleeves, trim, orn] + labels
    return Scene('shapan', layers, [
        'The shapan is the long outer robe of the steppe.',
        'Wool, camel hair or velvet keeps out wind and cold.',
        'Braided trim and ram-horn patterns decorate the edges.',
        "Draping a shapan over a guest's shoulders is a gesture of honour.",
    ], 'Шапан', 'Shapan', 'The robe of respect and welcome')


# ---------------------------------------------------------------- 6 BESHBARMAK
def build_beshbarmak():
    cx, cy = 340, 380
    c = Cv()
    c.ell((cx - 300, cy - 148, cx + 300, cy + 190), fill=(60, 40, 30, 45))  # shadow
    c.ell((cx - 290, cy - 170, cx + 290, cy + 140), fill=IVORY, outline=BROWN, w=3.5)
    c.ell((cx - 262, cy - 148, cx + 262, cy + 116), fill=(252, 250, 244), outline=BEIGE, w=2.5)
    for k in range(36):
        a = k * 2 * math.pi / 36
        x, y = cx + 276 * math.cos(a), cy - 15 + 140 * math.sin(a)
        c.poly([(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)], fill=TURQ)
    plate = L('plate', c, 4.0, 1.2, 'rise')

    c = Cv()
    sheets = [(-150, -10, 25), (-70, -40, -12), (30, -30, 20), (120, -4, -22), (-100, 40, -8), (0, 20, 15), (90, 50, -10), (-30, -60, 5)]
    for (dx, dy, rot) in sheets:
        sub = Cv()
        pts = [(-78, 0), (0, -46), (78, 0), (0, 46)]
        a = math.radians(rot)
        pp = [(cx + dx + x * math.cos(a) - y * math.sin(a), cy - 10 + dy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
        c.poly(pp, fill=(243, 232, 196), outline=(205, 186, 140), w=2.5)
        c.line([pp[0], pp[2]], (222, 206, 164), 1.5, False)
    noodles = L('noodles', c, 8.0, 1.4, 'rise')

    c = Cv()
    chunks = [(-110, -24, 78, 56), (-20, -46, 84, 60), (70, -20, 80, 58), (-60, 38, 74, 52), (40, 34, 84, 56), (-155, 24, 60, 44), (135, 28, 62, 44)]
    rng = np.random.RandomState(7)
    for (dx, dy, w, h) in chunks:
        x, y = cx + dx, cy - 10 + dy
        blob = []
        for k in range(14):
            a = k * 2 * math.pi / 14
            r = 1 + 0.16 * rng.uniform(-1, 1)
            blob.append((x + math.cos(a) * w / 2 * r, y + math.sin(a) * h / 2 * r))
        c.poly([(px + 3, py + 8) for px, py in blob], fill=(60, 40, 30, 70))
        c.poly(blob, fill=(138, 80, 52), outline=(92, 52, 32), w=3)
        c.poly([(x - w / 3, y - h / 5), (x - w / 8, y - h / 3), (x + w / 5, y - h / 4), (x, y - h / 12)], fill=(184, 120, 82))
        c.line([(x - w / 3, y + h / 6), (x + w / 4, y + h / 10)], (100, 58, 36), 2.2, False)
    meat = L('meat', c, 12.5, 1.4, 'rise')

    c = Cv()
    for k in range(9):
        a = k * 0.7
        x, y = cx - 40 + 74 * math.cos(a) * (0.4 + 0.12 * k), cy - 18 + 28 * math.sin(a) * (0.5 + 0.1 * k)
        c.arc((x - 24, y - 12, x + 24, y + 16), 190, 350, (190, 176, 140), 9)
        c.arc((x - 24, y - 12, x + 24, y + 16), 190, 350, (255, 252, 246), 5.5)
    onions = L('onions', c, 17.0, 1.2, 'drop')

    c = Cv()
    bx, by = 580, 460
    c.ell((bx - 78, by + 30, bx + 78, by + 70), fill=(60, 40, 30, 55))
    c.poly([(bx - 80, by - 10), (bx + 80, by - 10), (bx + 58, by + 62), (bx - 58, by + 62)], fill=TURQ, outline=BROWN, w=3.5)
    c.ell((bx - 80, by - 28, bx + 80, by + 8), fill=(214, 168, 70), outline=BROWN, w=3.5)
    c.ell((bx - 66, by - 22, bx + 66, by + 2), fill=(232, 196, 100))
    for k in range(7):
        c.poly([(bx - 64 + k * 22, by + 26), (bx - 53 + k * 22, by + 16), (bx - 42 + k * 22, by + 26), (bx - 53 + k * 22, by + 36)], fill=GOLDL)
    bowl = L('bowl', c, 21.0, 1.3, 'rise')

    steam = Cv()
    for k, x in enumerate((540, 580, 620)):
        steam.line(bez((x, 420), (x - 22, 384), (x + 22, 352), (x, 316)), (205, 194, 172, 210), 8)
    steam_l = L('steam', steam, 22.5, 1.0, 'fade', float_=(14, 2.4))

    labels = [
        label_layer('Wide sheets\nof boiled dough', (cx - 150, cy - 30), (20, 80), 8.6),
        label_layer('Boiled horse, lamb\nor beef', (cx + 70, cy - 20), (400, 96), 13.0),
        label_layer('Onions in broth', (cx - 30, cy - 4), (20, 520), 17.6),
        label_layer('Sorpa (hot broth)', (bx, by - 14), (440, 580), 21.6),
    ]
    layers = [plate, noodles, meat, onions, bowl, steam_l] + labels
    return Scene('beshbarmak', layers, [
        "Beshbarmak means 'five fingers', the way it was traditionally eaten.",
        'Boiled meat is laid over wide, thin sheets of dough.',
        'Onions simmered in broth go on top, with sorpa served alongside.',
        'The host shares the best pieces with guests and elders.',
    ], 'Бесбармақ', 'Beshbarmak', 'The dish of five fingers')


# ---------------------------------------------------------------- 7 BESIK
def build_besik():
    piv = (360, 540)
    c = Cv()
    c.ell((90, 546, 630, 584), fill=(60, 40, 30, 50))
    for off in (-1, 1):
        pass
    runner = bez((90, 480), (190, 600), (530, 600), (630, 480))
    c.line(runner, WOODD, 20)
    c.line(runner, WOOD, 11)
    for x in (160, 300, 420, 560):
        yy = 520 + 40 * math.sin((x - 90) / 540 * math.pi) * 0.9
        c.line([(x, 380), (x, yy - 6)], WOODD, 15, False)
        c.line([(x, 380), (x, yy - 6)], WOOD, 8, False)
    runner_l = L('runner', c, 4.0, 1.2, 'rise', rock=(3.2, 3.6, piv[0], piv[1]))

    c = Cv()
    top = bez((110, 340), (190, 400), (530, 400), (610, 340))
    bot = bez((110, 340), (140, 450), (580, 450), (610, 340))
    c.poly(top + bot[::-1], fill=WOOD, outline=BROWN, w=3.5)
    c.line(top, WOODL, 8)
    c.line(top, BROWN, 2, False)
    for k in range(8):
        x = 170 + k * 54
        c.poly([(x, 404), (x + 14, 392), (x + 28, 404), (x + 14, 416)], fill=WOODD)
        c.circle(x + 14, 404, 3, fill=GOLDL)
    for x in (116, 604):
        c.rrect((x - 14, 306, x + 14, 420), 10, fill=WOOD, outline=BROWN, w=3)
        c.circle(x, 322, 7, fill=GOLD, outline=BROWN, w=2)
    body_l = L('body', c, 7.5, 1.3, 'rise', rock=(3.2, 3.6, piv[0], piv[1]))

    c = Cv()
    c.ell((176, 318, 548, 392), fill=(244, 236, 220), outline=BEIGE, w=3)
    c.ell((196, 300, 330, 360), fill=(250, 244, 232), outline=BEIGE, w=3)
    for k in range(5):
        c.line(bez((340 + k * 40, 330), (350 + k * 40, 350), (350 + k * 40, 372), (340 + k * 40, 392)), (222, 206, 176), 2, False)
    c.ell((212, 304, 316, 352), fill=(238, 214, 188), outline=BROWNSOFT, w=2)  # swaddled head area
    c.circle(250, 330, 4, fill=BROWN)
    c.circle(282, 330, 4, fill=BROWN)
    c.arc((256, 332, 278, 346), 20, 160, BROWN, 2.5)
    for x in (360, 430, 500):
        c.rrect((x - 4, 322, x + 4, 396), 4, fill=TURQ)
    baby = L('baby', c, 13.0, 1.3, 'rise', rock=(3.2, 3.6, piv[0], piv[1]))

    c = Cv()
    arch = bez((116, 316), (200, 150), (520, 150), (604, 316))
    c.line(arch, WOODD, 17)
    c.line(arch, WOOD, 9)
    c.line(arch, BROWN, 1.8, False)
    for t in (0.25, 0.5, 0.75):
        p = arch[int(t * 48)]
        c.circle(p[0], p[1], 7, fill=GOLD, outline=BROWN, w=2)
    bar = L('bar', c, 16.0, 1.2, 'drop', rock=(3.2, 3.6, piv[0], piv[1]))

    c = Cv()
    mx, my = 360, 205
    c.line([(mx, my), (mx, my + 38)], BROWNSOFT, 2.5, False)
    c.circle(mx, my + 52, 13, fill=TURQ, outline=IVORY, w=3)
    c.circle(mx, my + 52, 5, fill=IVORY)
    for k, sgn in enumerate((-1, 0, 1)):
        c.poly([(mx + sgn * 16, my + 70), (mx + sgn * 16 + 8, my + 100), (mx + sgn * 16, my + 124), (mx + sgn * 16 - 8, my + 100)],
               fill=(222, 206, 176), outline=BROWNSOFT, w=1.8)
        c.line([(mx + sgn * 16, my + 72), (mx + sgn * 16, my + 122)], BROWNSOFT, 1.4, False)
    charm = L('charm', c, 19.0, 1.2, 'drop', rock=(3.2, 3.6, piv[0], piv[1]))

    labels = [
        label_layer('Rounded base\nfor rocking', (240, 546), (20, 560), 4.8),
        label_layer('Carved wooden frame', (150, 410), (20, 470), 8.0),
        label_layer('Ribbons hold\nthe baby', (432, 360), (470, 250), 13.6),
        label_layer('Bar with\nprotective charms', (460, 192), (470, 100), 19.6),
    ]
    layers = [runner_l, body_l, baby, bar, charm] + labels
    return Scene('besik', layers, [
        'The besik is the carved wooden cradle of Kazakh families.',
        'A rounded base lets it rock gently, and soft ribbons hold the baby.',
        'A bar across the top carries protective charms.',
        'At besik toi, a new life is welcomed with songs and good wishes.',
    ], 'Бесік', 'Besik', 'The cradle that welcomes a child')


# ---------------------------------------------------------------- 8 TORSYK
def build_torsyk():
    cx = 360
    c = Cv()
    c.ell((120, 560, 600, 606), fill=(60, 40, 30, 55))
    prof = [(236, 112), (270, 156), (330, 190), (420, 204), (500, 188), (548, 150), (572, 96), (582, 0)]
    # squat flask body: wide belly, flat-ish bottom
    body = prof_poly(cx, [(232, 56), (262, 130), (320, 182), (410, 206), (492, 190), (540, 150), (566, 96), (576, 0)])
    c.poly(body, fill=LEATHER, outline=BROWN, w=4)
    hl = Cv()
    hl.ell((210, 280, 330, 440), fill=(255, 220, 170, 26))
    c.paste(hl)
    body_l = L('body', c, 4.0, 1.3, 'rise')

    c = Cv()
    inner = prof_poly(cx, [(246, 50), (274, 118), (328, 166), (410, 188), (486, 174), (528, 138), (552, 90), (560, 0)])
    pts = inner + [inner[0]]
    for i in range(0, len(pts) - 1, 2):
        a, b = pts[i], pts[i + 1]
        c.line([a, b], (236, 214, 170), 3, False)
    c.line(bez((cx - 178, 360), (cx - 120, 330), (cx + 120, 330), (cx + 178, 360)), LEATHERD, 3, False)
    stitch = L('stitch', c, 8.0, 1.3, 'fade')

    c = Cv()
    c.circle(cx, 420, 74, outline=LEATHERD, w=4)
    c.circle(cx, 420, 58, outline=LEATHERD, w=2.5)
    c.poly([(cx, 372), (cx + 20, 420), (cx, 468), (cx - 20, 420)], fill=LEATHERD)
    for sgn in (-1, 1):
        for k in range(3):
            x = cx + sgn * (112 + k * 30)
            c.poly([(x, 406), (x + 11, 420), (x, 434), (x - 11, 420)], fill=LEATHERD)
        c.line([(cx + sgn * 96, 420), (cx + sgn * 176, 420)], LEATHERD, 2.5, False)
    for k in range(12):
        a = k * math.pi / 6
        c.circle(cx + 66 * math.cos(a), 420 + 66 * math.sin(a), 3.6, fill=GOLDL)
    emboss = L('emboss', c, 13.0, 1.4, 'fade')

    c = Cv()
    c.rrect((cx - 34, 150, cx + 34, 252), 14, fill=LEATHER, outline=BROWN, w=3.5)
    c.rrect((cx - 44, 236, cx + 44, 262), 8, fill=LEATHERD, outline=BROWN, w=3)
    c.rrect((cx - 30, 96, cx + 30, 160), 8, fill=WOODL, outline=BROWN, w=3.5)
    for y in (112, 128, 144):
        c.line([(cx - 28, y), (cx + 28, y)], WOODD, 2, False)
    neck = L('neck', c, 16.5, 1.2, 'drop')

    c = Cv()
    for sgn in (-1, 1):
        hx = cx + sgn * 196
        c.ell((hx - 30, 262, hx + 30, 330), outline=BROWN, w=11)
        c.ell((hx - 30, 262, hx + 30, 330), outline=LEATHER, w=6)
        c.rrect((hx - 12 - (8 if sgn < 0 else -8), 296, hx + 12 - (8 if sgn < 0 else -8), 332), 5, fill=LEATHERD, outline=BROWN, w=2.5)
    strap = bez((cx - 196, 262), (cx - 160, 70), (cx + 160, 70), (cx + 196, 262))
    c.line(strap, BROWN, 14)
    c.line(strap, LEATHER, 8)
    for i in range(0, len(strap) - 1, 3):
        c.circle(strap[i][0], strap[i][1], 1.8, fill=GOLDL)
    handles = L('handles', c, 20.0, 1.3, 'drop')

    labels = [
        label_layer('Tanned leather', (cx - 120, 480), (20, 560), 4.8),
        label_layer('Hand-stitched seam', (cx - 150, 380), (20, 330), 8.6),
        label_layer('Embossed pattern', (cx + 70, 440), (470, 540), 13.6),
        label_layer('Narrow neck\nwith stopper', (cx + 34, 200), (470, 150), 16.8),
        label_layer('Carrying strap', (cx + 150, 130), (500, 40), 20.6),
    ]
    layers = [body_l, stitch, emboss, neck, handles] + labels
    return Scene('torsyk', layers, [
        'The torsyk is a leather vessel for drinks on the road.',
        'Tanned hide is cut and sewn into a rounded flask with a narrow neck.',
        'Embossed patterns decorate the leather; handles hang it from the saddle.',
        "It often carried kumys, fermented mare's milk, across the steppe.",
    ], 'Торсық', 'Torsyk', 'The leather vessel of the road')


BUILDERS = {
    'dombra': build_dombra, 'yurt': build_yurt, 'kobyz': build_kobyz, 'saukele': build_saukele,
    'shapan': build_shapan, 'beshbarmak': build_beshbarmak, 'besik': build_besik, 'torsyk': build_torsyk,
}
