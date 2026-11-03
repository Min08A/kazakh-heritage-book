"""Flat-style illustrations for the 26 chapters added in the two-part edition.

Same conventions as art.py: each build_<slug>() returns a Scene of timed layers (720x640) + 4 captions.
Everything is drawn from code - no external art.
"""
import math

import numpy as np

from art import (Cv, L, Scene, label_layer, bez, rotpt, prof_poly, spiral,
                 IVORY, CREAM, SAND, BEIGE, BROWN, BROWNSOFT, TURQ, TURQD, GOLD, GOLDL,
                 WOOD, WOODL, WOODD, RED, REDL, LEATHER, LEATHERD, FELT)

SKY = (214, 232, 232)
GRASS = (122, 168, 96)
GRASSD = (92, 138, 74)
WATER = (110, 168, 196)
SNOW = (244, 246, 250)
SNOWS = (214, 222, 232)
GLASS = (196, 222, 226)
GLASSD = (150, 186, 192)
BRICK = (204, 146, 100)
BRICKD = (164, 106, 70)
CLAY = (206, 176, 136)
STONE = (168, 160, 150)
STONED = (128, 120, 112)
CAMEL = (196, 150, 98)
CAMELD = (150, 110, 70)
HORSE = (128, 76, 44)
HORSED = (60, 38, 24)
MILK = (250, 248, 240)
SILVER = (214, 216, 222)
SILVERD = (150, 154, 164)
IRON = (82, 84, 90)
IRONL = (120, 124, 132)
GLOW = (244, 140, 50)
BLUE = (52, 104, 160)
CARN = (190, 64, 36)
FRY = (214, 150, 70)
FRYD = (176, 112, 46)


def shadow(c, cx, y, w, h=40, a=55):
    c.ell((cx - w / 2, y - h / 2, cx + w / 2, y + h / 2), fill=(60, 40, 30, a))


def diamond(c, x, y, w, h, fill, outline=None, ow=0):
    c.poly([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], fill=fill, outline=outline, w=ow)


def ram_horn(c, x, y, s, col, w=2.5, flip=1):
    c.line(spiral(x + flip * 6 * s, y - 2 * s, 9 * s, 1.5 * s, 1.3, start=math.pi, cw=flip), col, w, False)
    c.line(spiral(x - flip * 6 * s, y - 2 * s, 9 * s, 1.5 * s, 1.3, start=0, cw=-flip), col, w, False)


def draw_dombra(c, cx, cy, ang, s=1.0):
    """Small dombra; (cx, cy) is the body centre, ang rotates on screen (deg, counter-clockwise)."""
    d = Cv()
    body = prof_poly(360, [(330, 24), (350, 36), (380, 66), (420, 102), (470, 124), (520, 122), (560, 100), (588, 56), (600, 0)])
    d.poly(body, fill=WOODL, outline=BROWN, w=3.5)
    d.circle(360, 495, 28, fill=BROWN)
    d.circle(360, 495, 35, outline=GOLD, w=3)
    d.rrect((337, 118, 383, 345), 6, fill=WOODD, outline=BROWN, w=3)
    for y in range(172, 340, 22):
        d.line([(344, y), (376, y)], BEIGE, 3, False)
    d.rrect((326, 58, 394, 130), 20, fill=WOOD, outline=BROWN, w=3)
    d.ell((296, 80, 316, 96), fill=TURQ, outline=BROWN, w=2.5)
    d.ell((404, 100, 424, 116), fill=GOLD, outline=BROWN, w=2.5)
    for x in (352, 368):
        d.line([(x, 112), (x, 552)], (250, 246, 232), 2.2, False)
    img = d.img
    W2, H2 = img.size
    img = img.resize((int(W2 * s), int(H2 * s)))
    img = img.rotate(ang, center=(360 * 2 * s, 470 * 2 * s), resample=3)
    ox, oy = int(cx * 2 - 360 * 2 * s), int(cy * 2 - 470 * 2 * s)
    c.img.alpha_composite(img, dest=(max(ox, 0), max(oy, 0)), source=(max(-ox, 0), max(-oy, 0)))


def draw_camel(c, x, y, s=1.0, col=CAMEL, cold=CAMELD, facing=1):
    """Side view camel; (x, y) = ground point under the body centre."""
    f = facing
    P = lambda px, py: (x + f * px * s, y + py * s)
    for lx, ph in ((-62, 0), (-40, 8), (52, -6), (74, 4)):
        c.line([P(lx, -120), P(lx + ph * f * 0.2, -60), P(lx, -4)], cold, 11 * s)
        c.ell((P(lx, 0)[0] - 10 * s, y - 8 * s, P(lx, 0)[0] + 10 * s, y + 2 * s), fill=cold)
    body = [P(-98, -118), P(-104, -150), P(-80, -176), P(-58, -214), P(-30, -200), P(-6, -172), P(16, -206), P(46, -214), P(74, -180), P(96, -152), P(102, -124), P(70, -106), P(-60, -104)]
    c.poly(body, fill=col, outline=BROWN, w=3 * s)
    neck = [P(90, -150), P(118, -150), P(132, -190), P(146, -232), P(132, -244), P(114, -206), P(96, -128)]
    c.poly(neck, fill=col, outline=BROWN, w=3 * s)
    c.poly([P(126, -246), P(168, -240), P(176, -226), P(160, -218), P(128, -224)], fill=col, outline=BROWN, w=3 * s)
    c.circle(*P(148, -236), 2.6 * s, fill=BROWN)
    c.line([P(-100, -136), P(-112, -110), P(-108, -86)], cold, 4 * s)
    return P


def draw_yurt(c, cx, gy, s=1.0):
    w = 150 * s
    h = 70 * s
    c.poly([(cx - w, gy), (cx - w, gy - h), (cx + w, gy - h), (cx + w, gy)], fill=FELT, outline=BROWN, w=3 * s)
    c.poly([(cx - w - 8 * s, gy - h), (cx - w * 0.3, gy - h - 70 * s), (cx + w * 0.3, gy - h - 70 * s), (cx + w + 8 * s, gy - h)], fill=(236, 226, 204), outline=BROWN, w=3 * s)
    c.rrect((cx - w * 0.3, gy - h - 82 * s, cx + w * 0.3, gy - h - 66 * s), 6 * s, fill=WOOD, outline=BROWN, w=2.5 * s)
    c.rrect((cx - w - 1, gy - h * 0.62, cx + w + 1, gy - h * 0.42), 2, fill=TURQ)
    for k in range(-5, 6):
        diamond(c, cx + k * w / 6, gy - h * 0.52, 10 * s, 10 * s, GOLDL)
    c.rrect((cx - 22 * s, gy - 56 * s, cx + 22 * s, gy), 4 * s, fill=RED, outline=BROWN, w=2.5 * s)
    diamond(c, cx, gy - 30 * s, 14 * s, 18 * s, GOLD)


def draw_sheep(c, x, y, s=1.0, flip=1):
    c.line([(x - 10 * s, y), (x - 10 * s, y + 18 * s)], BROWN, 4 * s)
    c.line([(x + 10 * s, y), (x + 10 * s, y + 18 * s)], BROWN, 4 * s)
    for dx, dy, r in ((-12, -4, 14), (0, -10, 15), (12, -4, 14), (0, 2, 15)):
        c.circle(x + dx * s, y + dy * s, r * s, fill=MILK, outline=BROWNSOFT, w=1.8 * s)
    c.ell((x + flip * 18 * s, y - 14 * s, x + flip * 34 * s, y + 2 * s) if flip > 0 else (x - 34 * s, y - 14 * s, x - 18 * s, y + 2 * s), fill=(70, 50, 40))


# ============================================================== PART 1
def build_khan_shatyr():
    cx = 360
    c = Cv()
    shadow(c, cx, 572, 600, 60, 45)
    c.ell((70, 520, 650, 610), fill=(214, 212, 204), outline=BROWNSOFT, w=2.5)
    c.ell((140, 500, 580, 586), fill=(234, 230, 220), outline=BROWNSOFT, w=2.5)
    for x in (110, 175, 545, 610):
        c.circle(x, 560, 18, fill=GRASSD, outline=BROWN, w=2)
    plaza = L('plaza', c, 4.0, 1.2, 'rise')

    c = Cv()
    left = bez((150, 548), (270, 520), (330, 300), (352, 96))
    right = bez((368, 96), (390, 300), (450, 520), (570, 548))
    c.poly(left + right + [(570, 548), (150, 548)], fill=GLASS, outline=BROWN, w=3.5)
    c.poly(bez((178, 540), (260, 500), (310, 340), (340, 160)) + [(352, 140), (340, 540)], fill=(222, 238, 240, 150))
    tent = L('tent', c, 7.5, 1.4, 'rise')

    c = Cv()
    for k in range(1, 12):
        t = k / 12
        xb = 150 + 420 * t
        c.line(bez((xb, 548), (xb, 420), (358 + (xb - 360) * 0.15, 260), (360, 100)), GLASSD, 1.8, False)
    for y in (500, 440, 370, 290, 210):
        sp = (548 - y) / 452
        half = 210 * (1 - sp) ** 1.9 + 8
        c.arc((360 - half, y - 10, 360 + half, y + 10), 0, 180, GLASSD, 1.8)
    cables = L('cables', c, 12.0, 1.4, 'fade')

    c = Cv()
    c.line([(360, 104), (346, 22)], (120, 124, 130), 7)
    c.line([(360, 104), (346, 22)], (200, 204, 210), 3, False)
    c.circle(346, 20, 5, fill=GOLD)
    mast = L('mast', c, 15.5, 1.0, 'drop')

    c = Cv()
    c.rrect((316, 500, 404, 546), 8, fill=(82, 102, 112), outline=BROWN, w=2.5)
    for x in (338, 360, 382):
        c.line([(x, 504), (x, 544)], (150, 170, 178), 2, False)
    c.ell((240, 470, 300, 486), fill=(238, 214, 150))
    c.ell((420, 470, 480, 486), fill=(130, 180, 120))
    inside = L('inside', c, 19.5, 1.2, 'fade')

    labels = [
        label_layer('Transparent\nroof', (250, 430), (20, 330), 8.4),
        label_layer('Cable net', (430, 330), (500, 300), 12.6),
        label_layer('Tilted mast', (352, 60), (420, 40), 16.0),
        label_layer('Shops, parks\nand a beach inside', (440, 478), (470, 560 - 60), 20.2),
    ]
    return Scene('khan-shatyr', [plaza, tent, cables, mast, inside] + labels, [
        'Khan Shatyr, "the khan’s tent", rises over the city of Astana.',
        'Its shape recalls a nomadic tent, with a light, transparent roof.',
        'A tall mast and a net of cables hold the roof in place.',
        'Inside, it stays warm all year: shops, cafés, a park and even a beach.',
    ], 'Хан Шатыр', 'Khan Shatyr', 'The royal tent of Astana')


def build_kyz_zhibek():
    cx = 360
    c = Cv()
    shadow(c, cx, 560, 460)
    c.poly(bez((110, 520), (200, 470), (300, 600), (420, 540)) + bez((420, 540), (520, 490), (580, 560), (630, 520))[1:] +
           [(630, 548), (420, 572)] + bez((420, 572), (300, 630), (200, 500), (110, 550))[1:], fill=(226, 190, 120), outline=GOLD, w=2)
    silk = L('silk', c, 4.0, 1.4, 'fade', sway=(4, 5))

    c = Cv()
    cap = prof_poly(cx, [(250, 2), (270, 90), (310, 150), (360, 182), (420, 196), (446, 198)])
    c.poly(cap, fill=RED, outline=BROWN, w=4)
    c.rrect((cx - 200, 430, cx + 200, 470), 10, fill=GOLD, outline=BROWN, w=3)
    for k in range(-6, 7):
        diamond(c, cx + k * 30, 450, 16, 22, RED)
    cap_l = L('cap', c, 7.5, 1.3, 'rise')

    c = Cv()
    for k in range(-3, 4):
        x0 = cx + k * 52
        c.line(bez((x0, 430), (x0 * 0.85 + cx * 0.15, 360), (cx + (x0 - cx) * 0.4, 290), (cx, 252)), GOLDL, 3, False)
    for x, y in ((cx - 100, 360), (cx + 100, 360), (cx, 320)):
        ram_horn(c, x, y, 1.3, GOLD, 3)
    emb = L('embroidery', c, 11.5, 1.3, 'fade')

    c = Cv()
    for k in range(9):
        a = math.radians(-60 + k * 15)
        base = (cx, 250)
        tip = (cx + 150 * math.sin(a), 250 - 170 * math.cos(a))
        mid = ((base[0] + tip[0]) / 2 + 10 * math.cos(a), (base[1] + tip[1]) / 2)
        col = (238, 236, 228) if k % 3 else (150, 140, 128)
        c.poly([base, (mid[0] - 9, mid[1]), tip, (mid[0] + 9, mid[1])], fill=col, outline=BROWNSOFT, w=1.5)
        c.line([base, tip], BROWNSOFT, 1.2, False)
    c.circle(cx, 252, 12, fill=GOLD, outline=BROWN, w=2.5)
    uki = L('feathers', c, 15.5, 1.2, 'drop', sway=(3, 4.2))

    c = Cv()
    for sgn in (-1, 1):
        for k in range(6):
            col = MILK if k % 2 else REDL
            c.circle(cx + sgn * 196, 482 + k * 16, 7, fill=col, outline=BROWN, w=1.5)
    for k in range(-9, 10):
        c.circle(cx + k * 21, 476, 5, fill=MILK, outline=BROWNSOFT, w=1)
    beads = L('beads', c, 19.5, 1.0, 'drop')

    labels = [
        label_layer('Silk: zhibek', (500, 530), (480, 580), 5.0),
        label_layer('Girl’s takiya cap', (300, 380), (20, 330), 8.4),
        label_layer('Gold embroidery', (cx + 100, 360), (470, 300), 12.4),
        label_layer('Owl feathers', (cx + 60, 150), (470, 90), 16.4),
        label_layer('Pearls and coral', (cx - 196, 530), (20, 470), 20.4),
    ]
    return Scene('kyz-zhibek', [silk, cap_l, emb, uki, beads] + labels, [
        'Kyz Zhibek, "the silk maiden", is the heroine of a Kazakh love epic.',
        'The hero Tolegen travels across the steppe to find her.',
        'Their love story ends in tragedy and is told in verse by akyns.',
        'It became the first Kazakh opera and a much-loved film.',
    ], 'Қыз Жібек', 'Kyz Zhibek', 'The silk maiden of the great love epic')


def tiles(c, x0, y0, x1, y1, step, col, skip=None):
    j = 0
    y = y0
    while y < y1:
        x = x0 + (step / 2 if j % 2 else 0)
        while x < x1:
            if not (skip and skip(x, y)):
                diamond(c, x, y, step * 0.7, step * 0.7, col)
            x += step
        y += step * 0.6
        j += 1


def pointed(cx, base, w, h):
    return [(cx - w / 2, base)] + bez((cx - w / 2, base - h * 0.6), (cx - w / 2, base - h * 0.9), (cx - w * 0.15, base - h), (cx, base - h)) + \
        bez((cx, base - h), (cx + w * 0.15, base - h), (cx + w / 2, base - h * 0.9), (cx + w / 2, base - h * 0.6))[1:] + [(cx + w / 2, base)]


def build_aisha_bibi():
    cx = 360
    c = Cv()
    shadow(c, cx, 572, 560, 50)
    c.rrect((100, 548, 620, 580), 6, fill=STONE, outline=BROWN, w=2.5)
    c.rrect((140, 210, 580, 552), 4, fill=BRICK, outline=BROWN, w=3.5)
    walls = L('walls', c, 4.0, 1.3, 'rise')

    c = Cv()
    tiles(c, 160, 236, 570, 540, 34, BRICKD, skip=lambda x, y: abs(x - cx) < 120)
    pattern = L('pattern', c, 8.0, 1.4, 'fade')

    c = Cv()
    c.poly(pointed(cx, 552, 220, 300), fill=BRICKD, outline=BROWN, w=3)
    c.poly(pointed(cx, 552, 150, 236), fill=(110, 70, 46), outline=BROWN, w=3)
    for y in range(300, 540, 30):
        diamond(c, cx - 96, y, 12, 16, GOLDL)
        diamond(c, cx + 96, y, 12, 16, GOLDL)
    portal = L('portal', c, 12.0, 1.3, 'rise')

    c = Cv()
    for x in (150, 570):
        c.poly(prof_poly(x, [(180, 30), (220, 40), (400, 36), (552, 40)]), fill=BRICKD, outline=BROWN, w=3)
        for y in range(220, 550, 26):
            c.line([(x - 34, y), (x + 34, y)], BRICK, 3, False)
    columns = L('columns', c, 15.5, 1.2, 'rise')

    c = Cv()
    c.rrect((126, 186, 594, 220), 4, fill=BRICKD, outline=BROWN, w=3)
    for x in range(146, 580, 26):
        c.circle(x, 203, 6, fill=GOLDL)
    frieze = L('frieze', c, 19.5, 1.0, 'drop')

    labels = [
        label_layer('Terracotta tiles', (230, 330), (20, 250), 8.6),
        label_layer('Pointed portal', (cx, 380), (450, 600 - 40), 12.6),
        label_layer('Fluted corner\ncolumns', (570, 420), (480, 300), 16.2),
        label_layer('Carved frieze', (480, 203), (470, 120), 20.2),
    ]
    return Scene('aisha-bibi', [walls, pattern, portal, columns, frieze] + labels, [
        'The mausoleum of Aisha Bibi stands near Taraz.',
        'Its walls are covered with carved terracotta tiles in dozens of patterns.',
        'Massive fluted columns stand at the corners.',
        'Legend says Karakhan built it in memory of his beloved Aisha.',
    ], 'Айша бибі', 'Aisha Bibi', 'A monument to faithful love')


def build_karakhan():
    cx = 360
    c = Cv()
    shadow(c, cx, 572, 560, 50)
    c.rrect((100, 548, 620, 580), 6, fill=STONE, outline=BROWN, w=2.5)
    c.rrect((130, 330, 590, 552), 4, fill=CLAY, outline=BROWN, w=3.5)
    tiles(c, 150, 350, 580, 540, 30, BRICKD, skip=lambda x, y: abs(x - cx) < 130)
    walls = L('walls', c, 4.0, 1.3, 'rise')

    c = Cv()
    c.rrect((cx - 120, 300, cx + 120, 340), 4, fill=CLAY, outline=BROWN, w=3)
    dome = [(cx - 116, 302)] + bez((cx - 116, 200), (cx - 70, 130), (cx - 20, 118), (cx, 116)) + bez((cx, 116), (cx + 20, 118), (cx + 70, 130), (cx + 116, 200))[1:] + [(cx + 116, 302)]
    c.poly(dome, fill=(118, 170, 168), outline=BROWN, w=3.5)
    for k in range(-3, 4):
        c.line(bez((cx + k * 32, 302), (cx + k * 30, 220), (cx + k * 14, 140), (cx, 118)), (88, 134, 132), 2, False)
    c.line([(cx, 116), (cx, 70)], GOLD, 4)
    c.circle(cx, 66, 8, fill=GOLD, outline=BROWN, w=2)
    dome_l = L('dome', c, 8.0, 1.3, 'drop')

    c = Cv()
    c.rrect((cx - 130, 240, cx + 130, 552), 4, fill=CLAY, outline=BROWN, w=3.5)
    c.poly(pointed(cx, 552, 170, 250), fill=BRICKD, outline=BROWN, w=3)
    c.poly(pointed(cx, 552, 110, 190), fill=(104, 70, 46), outline=BROWN, w=3)
    for x in (cx - 110, cx + 110):
        c.rrect((x - 12, 250, x + 12, 552), 6, fill=BRICKD, outline=BROWN, w=2.5)
    for x in range(cx - 120, cx + 130, 24):
        diamond(c, x, 258, 14, 14, GOLDL)
    pishtaq = L('portal', c, 12.0, 1.3, 'rise')

    c = Cv()
    for x in (140, 580):
        c.poly(prof_poly(x, [(300, 16), (320, 24), (552, 26)]), fill=BRICKD, outline=BROWN, w=3)
        c.circle(x, 296, 12, fill=CLAY, outline=BROWN, w=2.5)
    towers = L('towers', c, 15.5, 1.2, 'rise')

    c = Cv()
    for k in range(3):
        c.line(spiral(600 - k * 30, 90 + k * 10, 4, 22, 1.1, start=0), GOLDL, 2, False)
    c.circle(130, 100, 34, fill=(248, 222, 150, 220))
    sky = L('light', c, 19.5, 1.5, 'fade')

    labels = [
        label_layer('Square base', (170, 470), (20, 400), 5.0),
        label_layer('Ribbed dome', (cx + 60, 180), (470, 140), 8.6),
        label_layer('High portal', (cx + 60, 400), (470, 400), 12.6),
        label_layer('Corner towers', (580, 330), (470, 250), 16.2),
    ]
    return Scene('karakhan', [walls, dome_l, pishtaq, towers, sky] + labels, [
        'The mausoleum of Karakhan stands in the centre of Taraz.',
        'It honours a medieval ruler remembered as Aulie-Ata, "the holy father".',
        'A square base, a high portal and a dome crown the tomb.',
        'Legend links Karakhan with Aisha Bibi, the bride he lost.',
    ], 'Қарахан', 'Karakhan', 'The mausoleum of the holy ruler of Taraz')


def build_airan():
    c = Cv()
    c.ell((70, 470, 650, 610), fill=RED, outline=GOLD, w=4)
    c.ell((110, 490, 610, 590), outline=GOLDL, w=2)
    cloth = L('cloth', c, 4.0, 1.2, 'fade')

    c = Cv()
    jug = prof_poly(470, [(170, 34), (210, 40), (260, 88), (330, 104), (420, 96), (500, 72), (540, 56)])
    c.poly(jug, fill=(178, 116, 72), outline=BROWN, w=3.5)
    c.line(bez((510, 200), (600, 190), (600, 380), (530, 400)), BROWN, 12)
    c.line(bez((510, 200), (600, 190), (600, 380), (530, 400)), (178, 116, 72), 6)
    c.rrect((380, 300, 560, 316), 6, fill=(238, 224, 190))
    jug_l = L('jug', c, 7.5, 1.3, 'rise')

    c = Cv()
    c.poly([(150, 420), (390, 420)] + bez((390, 420), (380, 500), (330, 540), (270, 540)) + bez((270, 540), (210, 540), (160, 500), (150, 420))[1:], fill=MILK, outline=BROWN, w=3.5)
    c.ell((150, 400, 390, 440), fill=(244, 242, 232), outline=BROWN, w=3)
    c.ell((168, 406, 372, 434), fill=(252, 251, 246))
    for k in range(6):
        diamond(c, 190 + k * 32, 470, 16, 22, BLUE)
    c.line(bez((160, 450), (220, 455), (320, 455), (382, 450)), BLUE, 2.5, False)
    bowl = L('bowl', c, 11.5, 1.3, 'rise')

    c = Cv()
    c.line(bez((430, 150), (360, 140), (300, 250), (282, 418)), (250, 250, 244), 12)
    c.line(bez((430, 150), (360, 140), (300, 250), (282, 418)), (226, 226, 216), 3, False)
    pour = L('pour', c, 15.5, 1.0, 'fade')

    c = Cv()
    for k, (x, y) in enumerate(((240, 360), (270, 330), (300, 360))):
        c.line(bez((x, y), (x - 12, y - 20), (x + 12, y - 40), (x, y - 60)), (170, 200, 210), 2.5, False)
    cool = L('cool', c, 19.5, 1.2, 'fade', float_=(4, 3))

    labels = [
        label_layer('Clay jug', (470, 240), (520, 120), 8.4),
        label_layer('Kese bowl', (200, 480), (20, 520), 12.4),
        label_layer('Thick, sour\nfermented milk', (282, 420), (20, 230), 16.4),
    ]
    return Scene('airan', [cloth, jug_l, bowl, pour, cool] + labels, [
        'Ayran is a cool, sour drink made from fermented milk.',
        'A little old ayran is stirred into warm boiled milk as a starter.',
        'A few hours later it thickens and becomes pleasantly sour.',
        'Mixed with cold water, it is the favourite drink of hot summer days.',
    ], 'Айран', 'Ayran', 'The cool sour milk of summer')


# ============================================================== PART 2
def carpet(c, y0=470, y1=600, x0=60, x1=660):
    c.rrect((x0, y0, x1, y1), 10, fill=RED, outline=BROWN, w=3)
    c.rrect((x0 + 20, y0 + 16, x1 - 20, y1 - 16), 6, outline=GOLD, w=3)
    for k in range(5):
        diamond(c, x0 + (x1 - x0) * (k + 0.5) / 5, (y0 + y1) / 2, 50, 50, GOLD, BROWN, 2)
        diamond(c, x0 + (x1 - x0) * (k + 0.5) / 5, (y0 + y1) / 2, 22, 22, TURQ)


def build_aitys():
    c = Cv()
    carpet(c)
    rug = L('carpet', c, 4.0, 1.2, 'fade')
    c = Cv()
    draw_dombra(c, 210, 430, 28, 0.62)
    left = L('akyn1', c, 7.5, 1.3, 'rise', rock=(2.5, 3.0, 210, 430))
    c = Cv()
    draw_dombra(c, 510, 430, -28, 0.62)
    right = L('akyn2', c, 11.0, 1.3, 'rise', rock=(2.5, 3.4, 510, 430))
    c = Cv()
    for k in range(3):
        c.arc((250 - 40 * k, 120 - 20 * k, 470 + 40 * k, 340 + 20 * k), 200, 340, GOLD, 4)
    c.rrect((110, 60, 300, 130), 30, fill=IVORY, outline=TURQ, w=3)
    c.poly([(220, 126), (240, 160), (250, 126)], fill=IVORY, outline=TURQ, w=3)
    c.rrect((420, 60, 610, 130), 30, fill=IVORY, outline=RED, w=3)
    c.poly([(470, 126), (480, 160), (500, 126)], fill=IVORY, outline=RED, w=3)
    for x0, col in ((140, TURQD), (450, RED)):
        for k in range(3):
            c.line([(x0 + 10, 80 + k * 15), (x0 + 130 - k * 20, 80 + k * 15)], col, 3)
    verses = L('verses', c, 15.0, 1.3, 'fade', float_=(4, 3.5))
    c = Cv()
    for k, (x, y) in enumerate(((120, 230), (600, 230), (360, 60), (80, 140), (640, 140))):
        for a in range(4):
            ang = math.pi / 4 * a
            c.line([(x - 14 * math.cos(ang), y - 14 * math.sin(ang)), (x + 14 * math.cos(ang), y + 14 * math.sin(ang))], GOLD, 3)
    crowd = L('applause', c, 19.0, 1.0, 'fade')
    labels = [
        label_layer('First akyn', (160, 340), (20, 230), 8.4),
        label_layer('Rival akyn', (560, 340), (560, 230), 12.0),
        label_layer('Improvised\nverses', (360, 160), (300, 190), 16.0),
    ]
    return Scene('aitys', [rug, left, right, verses, crowd] + labels, [
        'Aitys is a duel of poets, sung to the dombyra.',
        'Two akyns face each other and improvise verses on the spot.',
        'Each must answer quickly, wittily and in rhyme.',
        'The audience decides who was wiser. Aitys is UNESCO heritage.',
    ], 'Айтыс', 'Aitys', 'A duel of poets')


def asyk_shape(c, x, y, s, fill, rot=0):
    pts = []
    for k in range(40):
        a = 2 * math.pi * k / 40
        r = 1 + 0.12 * math.cos(2 * a) - 0.22 * math.exp(-((a - math.pi / 2) % (2 * math.pi) - 0) ** 2 * 4)
        px, py = 46 * r * math.cos(a), 30 * r * math.sin(a)
        rr = math.radians(rot)
        pts.append((x + s * (px * math.cos(rr) - py * math.sin(rr)), y + s * (px * math.sin(rr) + py * math.cos(rr))))
    c.poly(pts, fill=fill, outline=BROWN, w=3 * s)
    c.ell((x - 14 * s, y - 8 * s, x + 14 * s, y + 8 * s), outline=BROWNSOFT, w=2 * s)
    c.arc((x - 30 * s, y - 20 * s, x + 30 * s, y + 20 * s), 200, 340, BROWNSOFT, 2 * s)


def build_asyk():
    c = Cv()
    c.ell((30, 400, 690, 620), fill=(228, 208, 168), outline=BEIGE, w=3)
    c.line([(80, 470), (640, 470)], BROWNSOFT, 3, False)
    ground = L('ground', c, 4.0, 1.2, 'fade')
    c = Cv()
    cols = [MILK, (238, 220, 180), RED, MILK, BLUE, (238, 220, 180), MILK]
    for i, col in enumerate(cols):
        shadow(c, 140 + i * 72, 478, 70, 16, 45)
        asyk_shape(c, 140 + i * 72, 450, 0.72, col, rot=(i % 3) * 15)
    row = L('row', c, 7.5, 1.4, 'rise')
    c = Cv()
    shadow(c, 470, 590, 120, 22)
    asyk_shape(c, 470, 556, 1.2, (204, 154, 86), rot=-10)
    c.circle(470, 556, 9, fill=IRON)
    saqa = L('saqa', c, 11.5, 1.2, 'drop')
    c = Cv()
    for k in range(4):
        c.line([(520 + k * 10, 540 - k * 12), (600 + k * 14, 520 - k * 18)], BROWNSOFT, 2.5, False)
    c.line(bez((470, 540), (420, 470), (380, 460), (360, 452)), TURQD, 3, False)
    c.poly([(352, 446), (370, 444), (362, 462)], fill=TURQD)
    shot = L('shot', c, 15.5, 1.0, 'fade')
    c = Cv()
    for i, (name, x) in enumerate((('alshy', 120), ('taiqy', 260), ('tompaq', 400), ('buk', 540))):
        asyk_shape(c, x + 55, 190, 0.75, MILK, rot=i * 45)
    sides = L('sides', c, 19.5, 1.2, 'fade')
    labels = [
        label_layer('Row of asyks', (300, 450), (20, 340), 8.4),
        label_layer('Heavy shooter:\nsaqa', (500, 570), (520, 400), 12.4),
        label_layer('Four sides: alshy, taiqy,\ntompaq, buk', (300, 210), (130, 30), 20.4),
    ]
    return Scene('asyk', [ground, row, saqa, shot, sides] + labels, [
        'An asyk is the small knucklebone of a sheep.',
        'In asyk atu, players set asyks in a row on the ground.',
        'They try to knock them out with a heavier shooter called the saqa.',
        'Each side of an asyk has its own name. The game is UNESCO heritage.',
    ], 'Асық', 'Asyk', 'The knucklebone game')


def draw_wheel(c, x, y, r):
    c.circle(x, y, r, outline=BROWN, w=16)
    c.circle(x, y, r, outline=WOODD, w=10)
    for k in range(12):
        a = 2 * math.pi * k / 12
        c.line([(x + 16 * math.cos(a), y + 16 * math.sin(a)), (x + (r - 6) * math.cos(a), y + (r - 6) * math.sin(a))], WOOD, 6, False)
    c.circle(x, y, 22, fill=WOOD, outline=BROWN, w=3)
    c.circle(x, y, 7, fill=IRON)


def build_at_arba():
    c = Cv()
    c.ell((20, 540, 700, 620), fill=(228, 208, 168))
    shadow(c, 300, 590, 420, 30)
    ground = L('ground', c, 4.0, 1.0, 'fade')
    c = Cv()
    c.rrect((90, 330, 470, 372), 6, fill=WOOD, outline=BROWN, w=3.5)
    c.rrect((90, 260, 470, 338), 4, fill=WOODL, outline=BROWN, w=3.5)
    for x in range(110, 470, 60):
        c.rrect((x - 6, 240, x + 6, 340), 3, fill=WOODD, outline=BROWN, w=2)
    body = L('body', c, 7.5, 1.3, 'rise')
    c = Cv()
    draw_wheel(c, 260, 452, 132)
    wheel = L('wheel', c, 11.0, 1.3, 'rise')
    c = Cv()
    for dy in (0, 18):
        c.line([(440, 352 + dy), (560, 372 + dy), (690, 380 + dy)], BROWN, 12)
        c.line([(440, 352 + dy), (560, 372 + dy), (690, 380 + dy)], WOODD, 7)
    shafts = L('shafts', c, 15.0, 1.2, 'fade')
    c = Cv()
    c.poly(bez((110, 270), (140, 160), (380, 140), (440, 260)), fill=(222, 196, 112), outline=(160, 130, 60), w=3)
    for k in range(14):
        x = 140 + k * 21
        c.line([(x, 250), (x + 10, 180 + (k % 3) * 10)], (180, 150, 70), 2, False)
    hay = L('hay', c, 19.0, 1.3, 'drop')
    labels = [
        label_layer('Wooden body', (150, 300), (20, 180), 8.4),
        label_layer('Tall spoked\nwheel', (330, 470), (480, 470), 11.8),
        label_layer('Shafts for\nthe horse', (620, 382), (540, 250), 15.8),
        label_layer('A load of hay', (300, 190), (280, 60), 19.8),
    ]
    return Scene('at-arba', [ground, body, wheel, shafts, hay] + labels, [
        'An at arba is a cart drawn by a horse.',
        'Tall wooden wheels roll over rough roads, mud and shallow rivers.',
        'Two long shafts fasten the cart to the horse’s harness.',
        'It carried hay, water, firewood and people to market and celebrations.',
    ], 'Ат арба', 'At Arba', 'The horse-drawn cart')


def draw_horse(c, x, y, s=1.0, col=HORSE, gallop=True):
    P = lambda px, py: (x + px * s, y + py * s)
    if gallop:
        legs = [((60, -120), (120, -70), (150, -40)), ((40, -120), (80, -60), (60, -10)), ((-90, -120), (-150, -80), (-190, -70)), ((-80, -120), (-90, -60), (-60, -12))]
    else:
        legs = [((x0, -120), (x0 + 4, -60), (x0, 0)) for x0 in (70, 40, -80, -100)]
    for a, b, d in legs:
        c.line([P(*a), P(*b), P(*d)], HORSED, 14 * s)
        c.line([P(*a), P(*b), P(*d)], col, 9 * s)
    c.ell((x - 130 * s, y - 200 * s, x + 110 * s, y - 100 * s), fill=col, outline=BROWN, w=3.5 * s)
    neck = [P(60, -190), P(110, -230), P(150, -280), P(176, -262), P(140, -200), P(104, -140)]
    c.poly(neck, fill=col, outline=BROWN, w=3.5 * s)
    c.poly([P(146, -286), P(176, -296), P(226, -250), P(214, -232), P(168, -246)], fill=col, outline=BROWN, w=3.5 * s)
    c.circle(*P(180, -270), 3 * s, fill=BROWN)
    c.poly([P(150, -290), P(156, -312), P(166, -292)], fill=col, outline=BROWN, w=2 * s)
    c.line([P(60, -200), P(100, -240), P(146, -290)], HORSED, 9 * s)
    c.line(bez(P(-126, -170), P(-170, -170), P(-200, -150), P(-226, -110)), HORSED, 14 * s)
    return P


def build_baige():
    c = Cv()
    c.rrect((0, 520, 720, 640), 0, fill=GRASS)
    c.line([(0, 520), (720, 520)], GRASSD, 3, False)
    for x in range(30, 720, 80):
        c.line([(x, 560), (x + 30, 560)], GRASSD, 3, False)
    track = L('steppe', c, 4.0, 1.2, 'fade')
    c = Cv()
    P = draw_horse(c, 330, 560, 1.15)
    c.ell((P(-30, -230)[0], P(-30, -230)[1], P(50, -196)[0], P(50, -196)[1]), fill=RED, outline=BROWN, w=3)
    horse_l = L('horse', c, 7.5, 1.3, 'rise', float_=(4, 0.9))
    c = Cv()
    hx, hy = P(10, -250)
    c.poly([(hx - 22, hy + 20), (hx + 20, hy + 16), (hx + 30, hy - 40), (hx - 8, hy - 52)], fill=BLUE, outline=BROWN, w=3)
    c.circle(hx + 18, hy - 70, 18, fill=(236, 200, 170), outline=BROWN, w=2.5)
    c.ell((hx, hy - 100, hx + 38, hy - 74), fill=RED, outline=BROWN, w=2.5)
    c.line([(hx + 26, hy - 30), (hx + 70, hy - 70), (hx + 96, hy - 110)], LEATHERD, 5)
    rider = L('rider', c, 11.5, 1.2, 'drop', float_=(4, 0.9))
    c = Cv()
    for x in (600, 690):
        c.line([(x, 520), (x, 280)], WOODD, 8)
    c.poly([(600, 284), (560, 300), (600, 316)], fill=RED)
    c.poly([(690, 284), (650, 300), (690, 316)], fill=TURQ)
    c.line(bez((600, 340), (630, 360), (660, 360), (690, 340)), GOLD, 4, False)
    finish = L('finish', c, 15.5, 1.0, 'fade')
    c = Cv()
    for k in range(8):
        c.circle(60 + k * 22, 520 - (k % 3) * 18, 14 + (k % 3) * 4, fill=(214, 196, 160, 140))
    dust = L('dust', c, 19.0, 1.0, 'fade', sway=(6, 1.2))
    labels = [
        label_layer('Race horse', (240, 470), (20, 330), 8.4),
        label_layer('Young rider', (hx, hy - 30), (20, 150), 12.2),
        label_layer('Qamshy whip', (hx + 90, hy - 104), (330, 60), 13.8),
        label_layer('Finish line', (645, 350), (520, 200), 16.2),
    ]
    return Scene('baige', [track, horse_l, rider, finish, dust] + labels, [
        'Baige is the traditional Kazakh horse race.',
        'It can run for many kilometres across the open steppe.',
        'Light, skilful young riders guide horses trained for weeks.',
        'Winning a baige brings honour to the horse’s owner.',
    ], 'Бәйге', 'Baige', 'The long-distance horse race')


def build_baursak():
    c = Cv()
    shadow(c, 360, 560, 600)
    c.ell((60, 430, 660, 600), fill=MILK, outline=BROWN, w=3.5)
    c.ell((120, 455, 600, 575), outline=BLUE, w=3)
    for k in range(18):
        a = 2 * math.pi * k / 18
        diamond(c, 360 + 270 * math.cos(a), 515 + 74 * math.sin(a), 12, 10, BLUE)
    plate = L('plate', c, 4.0, 1.2, 'rise')
    rng = np.random.RandomState(4)
    piles = []
    for layer, (n, rx, ry, y) in enumerate(((9, 200, 34, 500), (6, 130, 22, 450), (3, 64, 10, 405))):
        c = Cv()
        for k in range(n):
            a = math.pi * (k + 0.5) / n
            x = 360 - rx * math.cos(a)
            yy = y - ry * math.sin(a) * 0.4
            sz = 36 + rng.randint(-4, 6)
            if (k + layer) % 3 == 0:
                c.poly([(x - sz, yy + sz * 0.6), (x + sz, yy + sz * 0.6), (x + 4, yy - sz * 0.9)], fill=FRY, outline=FRYD, w=3)
            else:
                c.rrect((x - sz, yy - sz * 0.7, x + sz, yy + sz * 0.7), 16, fill=FRY, outline=FRYD, w=3)
            c.ell((x - sz * 0.5, yy - sz * 0.45, x, yy - sz * 0.1), fill=(240, 196, 120))
        piles.append(L(f'pile{layer}', c, 7.5 + layer * 3.5, 1.2, 'drop'))
    c = Cv()
    c.poly([(560, 300), (680, 300), (664, 380), (576, 380)], fill=MILK, outline=BROWN, w=3)
    c.ell((558, 290, 682, 312), fill=(196, 132, 80), outline=BROWN, w=2.5)
    for k in range(3):
        c.line(bez((590 + k * 25, 280), (580 + k * 25, 250), (600 + k * 25, 230), (590 + k * 25, 200)), (200, 200, 200), 2.5, False)
    tea = L('tea', c, 19.0, 1.2, 'fade')
    labels = [
        label_layer('Fried dough', (300, 460), (20, 320), 8.4),
        label_layer('Square or\ntriangular', (400, 400), (450, 210), 12.4),
        label_layer('Served with tea', (620, 340), (480, 120), 19.6),
    ]
    return Scene('baursak', [plate] + piles + [tea] + labels, [
        'Baursak is dough fried until golden and puffy.',
        'It is cut into squares, triangles or circles before frying.',
        'Piled high, it is served with tea at every dastarkhan.',
        'Many families fry baursak on Fridays to remember their ancestors.',
    ], 'Бауырсақ', 'Baursak', 'Golden bread of the dastarkhan')


def build_zhailau():
    c = Cv()
    c.poly([(0, 380), (90, 230), (170, 300), (280, 150), (390, 300), (470, 210), (560, 290), (640, 200), (720, 300), (720, 420), (0, 420)], fill=(150, 178, 178), outline=BROWNSOFT, w=2.5)
    c.poly([(250, 196), (280, 150), (312, 196), (296, 190), (280, 206), (264, 190)], fill=SNOW)
    c.poly([(614, 236), (640, 200), (664, 236), (640, 230)], fill=SNOW)
    mountains = L('mountains', c, 4.0, 1.4, 'fade')
    c = Cv()
    c.poly(bez((0, 380), (200, 340), (500, 400), (720, 360)) + [(720, 640), (0, 640)], fill=GRASS)
    c.poly(bez((0, 470), (240, 440), (480, 500), (720, 460)) + [(720, 640), (0, 640)], fill=GRASSD)
    rng = np.random.RandomState(3)
    for k in range(40):
        x, y = rng.randint(10, 710), rng.randint(420, 630)
        c.circle(x, y, 4, fill=(250, 220, 90) if k % 3 else (230, 120, 160))
    meadow = L('meadow', c, 6.5, 1.3, 'rise')
    c = Cv()
    c.poly(bez((0, 600), (180, 540), (360, 620), (720, 560)) + bez((720, 590), (360, 650), (180, 570), (0, 630)), fill=WATER, outline=(80, 130, 160), w=2)
    stream = L('stream', c, 10.0, 1.2, 'fade')
    c = Cv()
    draw_yurt(c, 300, 440, 0.8)
    draw_yurt(c, 520, 410, 0.5)
    yurts = L('yurts', c, 13.5, 1.3, 'rise')
    c = Cv()
    for i, (x, y) in enumerate(((120, 490), (170, 510), (90, 530), (600, 500), (640, 520))):
        draw_sheep(c, x, y, 0.9, 1 if i % 2 else -1)
    sheep = L('sheep', c, 17.5, 1.2, 'fade', sway=(3, 4))
    labels = [
        label_layer('Mountain meadows', (420, 330), (430, 60), 7.2),
        label_layer('Cool stream', (300, 595), (20, 570 - 40), 10.6),
        label_layer('White yurts', (300, 380), (20, 300), 14.2),
        label_layer('Herds grow strong', (620, 500), (480, 420), 18.2),
    ]
    return Scene('zhailau', [mountains, meadow, stream, yurts, sheep] + labels, [
        'The zhailau is the summer pasture of the nomads.',
        'In late spring, families moved to cool mountain meadows.',
        'There the grass was rich and water was plentiful.',
        'Summer on the zhailau was the season of kymyz, songs and weddings.',
    ], 'Жайлау', 'Zhailau', 'The green summer pasture')


def build_kazakh_kuresi():
    cx = 360
    c = Cv()
    c.ell((40, 380, 680, 620), fill=BLUE, outline=BROWN, w=3)
    c.ell((140, 420, 580, 580), outline=GOLDL, w=5)
    mat = L('mat', c, 4.0, 1.2, 'fade')
    c = Cv()
    pts = [(220 + 120 * math.cos(t) * (1 - t / 30), 500 + 40 * math.sin(t) * (1 - t / 30)) for t in np.linspace(0, 4 * math.pi, 80)]
    c.line(pts, BROWN, 20)
    c.line(pts, RED, 14)
    c.rrect((320, 486, 356, 512), 4, fill=GOLD, outline=BROWN, w=2)
    belt1 = L('belt-red', c, 7.5, 1.3, 'fade')
    c = Cv()
    pts = [(500 + 120 * math.cos(t) * (1 - t / 30), 500 + 40 * math.sin(t) * (1 - t / 30)) for t in np.linspace(math.pi, 5 * math.pi, 80)]
    c.line(pts, BROWN, 20)
    c.line(pts, (40, 90, 170), 14)
    c.rrect((364, 486, 400, 512), 4, fill=GOLD, outline=BROWN, w=2)
    belt2 = L('belt-blue', c, 11.5, 1.3, 'fade')
    c = Cv()
    cup = prof_poly(cx, [(140, 90), (190, 92), (240, 70), (280, 24), (320, 22), (340, 60), (360, 70)])
    c.poly(cup, fill=GOLD, outline=BROWN, w=3.5)
    for sgn in (-1, 1):
        c.line(bez((cx + sgn * 86, 160), (cx + sgn * 140, 160), (cx + sgn * 140, 240), (cx + sgn * 60, 250)), BROWN, 10)
        c.line(bez((cx + sgn * 86, 160), (cx + sgn * 140, 160), (cx + sgn * 140, 240), (cx + sgn * 60, 250)), GOLD, 5)
    c.ell((cx - 92, 128, cx + 92, 152), fill=(220, 180, 90), outline=BROWN, w=3)
    diamond(c, cx, 210, 30, 40, RED, BROWN, 2)
    cup_l = L('trophy', c, 15.5, 1.2, 'drop')
    c = Cv()
    for k in range(10):
        a = 2 * math.pi * k / 10
        c.line([(cx + 120 * math.cos(a), 200 + 120 * math.sin(a)), (cx + 150 * math.cos(a), 200 + 150 * math.sin(a))], GOLDL, 4)
    shine = L('shine', c, 19.5, 1.0, 'fade')
    labels = [
        label_layer('Wrestling belt', (180, 470), (20, 380), 8.6),
        label_layer('Grip the\nopponent’s belt', (560, 500), (520, 380), 12.6),
        label_layer('The winner’s prize', (cx, 200), (480, 100), 16.6),
    ]
    return Scene('kazakh-kuresi', [mat, belt1, belt2, cup_l, shine] + labels, [
        'Kazakh kuresi is the national form of wrestling.',
        'Two paluans take hold of each other’s belts.',
        'They try to throw the opponent onto his back with strength and skill.',
        'Kazhymukan Munaitpasov became a world champion and a national hero.',
    ], 'Қазақ күресі', 'Kazakh Kuresi', 'The wrestling of the steppe')


def caravan_pack(c, P, col):
    c.poly([P(-70, -200), P(60, -200), P(70, -170), P(-80, -170)], fill=col, outline=BROWN, w=3)
    c.rrect(sorted_box(P(-60, -260), P(40, -200)), 8, fill=(222, 204, 160), outline=BROWN, w=3)
    c.line([P(-50, -250), P(30, -205)], LEATHERD, 3, False)


def sorted_box(a, b):
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


def build_keruen():
    c = Cv()
    c.rrect((0, 0, 720, 640), 0, fill=(250, 232, 196, 0))
    c.circle(600, 110, 60, fill=(246, 210, 120))
    c.poly(bez((0, 470), (180, 400), (360, 480), (720, 420)) + [(720, 640), (0, 640)], fill=(228, 200, 150))
    c.poly(bez((0, 560), (240, 500), (480, 580), (720, 520)) + [(720, 640), (0, 640)], fill=(214, 184, 132))
    desert = L('desert', c, 4.0, 1.4, 'fade')
    layers = [desert]
    for i, (x, col) in enumerate(((540, RED), (330, TURQ), (120, (140, 60, 90)))):
        c = Cv()
        P = draw_camel(c, x, 560, 0.75)
        caravan_pack(c, P, col)
        if i > 0:
            c.line([P(150, -230), P(210, -160), P(260, -200)], LEATHERD, 2.5, False)
        layers.append(L(f'camel{i}', c, 7.0 + i * 3.5, 1.3, 'rise', sway=(3, 2.4)))
    c = Cv()
    for k in range(5):
        c.ell((20 + k * 40, 590, 40 + k * 40, 598), fill=(190, 160, 110))
    tracks = L('tracks', c, 18.5, 1.0, 'fade')
    layers.append(tracks)
    labels = [
        label_layer('Bactrian camel', (540, 440), (480, 300 - 40), 7.8),
        label_layer('Packs of silk\nand spices', (330, 380), (180, 180), 11.4),
        label_layer('A long line\nof travellers', (120, 450), (20, 280), 15.0),
    ]
    return Scene('keruen', layers + labels, [
        'A keruen is a caravan of camels, horses and people.',
        'Caravans followed the Great Silk Road across present-day Kazakhstan.',
        'Two-humped camels carried silk, spices and cloth between East and West.',
        'They rested at wells and caravanserais along the road.',
    ], 'Керуен', 'Keruen', 'The camel caravan of the Silk Road')


def build_kosh():
    c = Cv()
    c.poly(bez((0, 520), (240, 480), (480, 540), (720, 500)) + [(720, 640), (0, 640)], fill=GRASS)
    c.poly([(0, 420), (120, 340), (240, 410), (380, 330), (520, 420), (720, 380), (720, 470), (0, 470)], fill=(180, 196, 190))
    land = L('steppe', c, 4.0, 1.3, 'fade')
    c = Cv()
    P = draw_camel(c, 330, 590, 1.05)
    c.poly([P(-100, -200), P(90, -200), P(100, -165), P(-110, -165)], fill=RED, outline=BROWN, w=3)
    for k in range(4):
        c.line([P(110 + k * 8, -170), P(110 + k * 8, -130)], GOLD if k % 2 else RED, 4)
    camel = L('camel', c, 7.5, 1.3, 'rise', sway=(3, 2.6))
    c = Cv()
    for side in (-1, 1):
        x0 = -100 if side < 0 else 10
        box = sorted_box(P(x0, -300), P(x0 + 90, -200))
        c.rrect(box, 4, fill=WOODL, outline=BROWN, w=3)
        for k in range(5):
            xa = box[0] + k * (box[2] - box[0]) / 4
            c.line([(xa, box[1]), (xa + 22, box[3])], WOODD, 2.5, False)
            c.line([(xa + 22, box[1]), (xa, box[3])], WOODD, 2.5, False)
    kerege = L('kerege', c, 11.0, 1.2, 'drop', sway=(3, 2.6))
    c = Cv()
    for k in range(2):
        b = sorted_box(P(-110, -350 - k * 34), P(110, -312 - k * 34))
        c.rrect(b, 18, fill=FELT, outline=BROWN, w=3)
        c.ell((b[2] - 24, b[1], b[2] + 8, b[3]), fill=(230, 220, 196), outline=BROWN, w=2.5)
    for k in range(6):
        c.line([P(-140, -404 + k * 4), P(140, -416 + k * 4)], (188, 98, 60), 3, False)
    felt = L('felt', c, 14.5, 1.2, 'drop', sway=(3, 2.6))
    c = Cv()
    sx, sy = P(0, -440)
    c.ell((sx - 70, sy - 22, sx + 70, sy + 22), outline=BROWN, w=12)
    c.ell((sx - 70, sy - 22, sx + 70, sy + 22), outline=WOODD, w=7)
    c.arc((sx - 60, sy - 50, sx + 60, sy + 20), 200, 340, WOODD, 5)
    shan = L('shanyraq', c, 18.0, 1.2, 'drop', sway=(3, 2.6))
    labels = [
        label_layer('Decorated\nlead camel', P(110, -150), (540, 450), 8.4),
        label_layer('Lattice walls', P(50, -250), (500, 260), 11.8),
        label_layer('Felt and roof poles', P(-90, -330), (20, 200), 15.4),
        label_layer('The shanyraq\nrides on top', (sx, sy), (420, 60), 18.8),
    ]
    return Scene('kosh', [land, camel, kerege, felt, shan] + labels, [
        'Kosh is the seasonal move of a nomadic aul.',
        'Yurts were taken down and tied onto camels and horses.',
        'Walls, roof poles, felt and the shanyraq all travelled together.',
        'At the new pasture, the yurts were raised again within hours.',
    ], 'Көш', 'Kosh', 'The great seasonal move')


def draw_tostagan(c, cx, y, w, liquid=MILK):
    c.poly([(cx - w, y), (cx + w, y)] + bez((cx + w, y), (cx + w * 0.95, y + w * 0.6), (cx + w * 0.5, y + w * 0.8), (cx, y + w * 0.8)) + bez((cx, y + w * 0.8), (cx - w * 0.5, y + w * 0.8), (cx - w * 0.95, y + w * 0.6), (cx - w, y))[1:], fill=WOOD, outline=BROWN, w=3.5)
    c.ell((cx - w, y - w * 0.18, cx + w, y + w * 0.18), fill=WOODD, outline=BROWN, w=3)
    c.ell((cx - w * 0.88, y - w * 0.13, cx + w * 0.88, y + w * 0.13), fill=liquid)
    c.line(bez((cx - w * 0.97, y + w * 0.25), (cx - w * 0.4, y + w * 0.4), (cx + w * 0.4, y + w * 0.4), (cx + w * 0.97, y + w * 0.25)), GOLD, 4, False)
    for k in range(-3, 4):
        diamond(c, cx + k * w * 0.24, y + w * 0.45, 12, 16, GOLD)


def build_kymyz():
    c = Cv()
    c.ell((40, 470, 680, 620), fill=WOODD, outline=GOLD, w=4)
    table = L('table', c, 4.0, 1.2, 'fade')
    c = Cv()
    sab = prof_poly(560, [(110, 20), (140, 30), (200, 70), (300, 92), (380, 84), (440, 60)])
    c.poly(sab, fill=(96, 56, 32), outline=BROWN, w=3)
    c.line([(560, 130), (566, 30)], WOODL, 6)
    saba_l = L('saba', c, 7.0, 1.2, 'fade')
    c = Cv()
    draw_tostagan(c, 300, 430, 170)
    big = L('bowl', c, 10.5, 1.3, 'rise')
    c = Cv()
    draw_tostagan(c, 580, 500, 70)
    small = L('bowls', c, 13.5, 1.2, 'rise')
    c = Cv()
    c.line([(90, 300), (300, 380), (420, 420)], BROWN, 12)
    c.line([(90, 300), (300, 380), (420, 420)], WOODL, 7)
    c.ell((400, 400, 470, 440), fill=WOODL, outline=BROWN, w=3)
    c.circle(88, 300, 10, fill=GOLD, outline=BROWN, w=2)
    ladle = L('ozhau', c, 17.0, 1.2, 'drop')
    labels = [
        label_layer('Leather saba', (560, 220), (520, 40), 7.8),
        label_layer('Tostagan bowl', (200, 480), (20, 560), 11.2),
        label_layer('Fermented\nmare’s milk', (300, 430), (40, 160), 14.2),
        label_layer('Ozhau ladle', (150, 322), (20, 280), 17.8),
    ]
    return Scene('kymyz', [table, saba_l, big, small, ladle] + labels, [
        'Kymyz is fermented mare’s milk, the treasured drink of the steppe.',
        'Fresh milk is stirred again and again in a leather saba.',
        'It becomes slightly fizzy, sour and refreshing.',
        'It is served in wooden bowls with a ladle to honoured guests.',
    ], 'Қымыз', 'Kymyz', 'The fermented mare’s milk')


def draw_note(c, x, y, col, flag=True):
    c.ell((x - 16, y - 11, x + 14, y + 11), fill=col, outline=BROWN, w=2)
    c.line([(x + 12, y), (x + 12, y - 70)], BROWN, 4, False)
    if flag:
        c.line(bez((x + 12, y - 70), (x + 30, y - 60), (x + 34, y - 44), (x + 26, y - 30)), BROWN, 4, False)


def build_kui():
    c = Cv()
    draw_dombra(c, 250, 470, 30, 0.95)
    dom = L('dombyra', c, 4.0, 1.3, 'rise')
    layers = [dom]
    groups = [((420, 260, GOLD), (480, 200, TURQ)), ((540, 300, RED), (600, 220, GOLD)), ((470, 380, TURQ), (630, 360, RED))]
    for i, g in enumerate(groups):
        c = Cv()
        for x, y, col in g:
            draw_note(c, x, y, col, (x // 10) % 2 == 0)
        layers.append(L(f'notes{i}', c, 8.0 + i * 3.5, 1.2, 'fade', float_=(8, 3 + i)))
    c = Cv()
    for k in range(3):
        pts = [(330 + t * 380, 470 + k * 28 + 22 * math.sin(t * 12 + k)) for t in np.linspace(0, 1, 60)]
        c.line(pts, (GOLD, TURQ, REDL)[k], 3, False)
    waves = L('waves', c, 19.0, 1.4, 'fade', sway=(6, 3))
    labels = [
        label_layer('Played on the dombyra', (250, 470), (20, 560), 5.0),
        label_layer('Music without words', (480, 220), (420, 60), 8.6),
        label_layer('A story: a gallop,\na storm, a legend', (560, 500), (420, 560), 19.6),
    ]
    return Scene('kui', layers + [waves] + labels, [
        'A kui is an instrumental piece, most often played on the dombyra.',
        'It has no words, but it tells a story.',
        'Galloping horses, a storm or a legend come alive in the music.',
        'Kurmangazy’s kui "Sary-Arka" is one of the best-known melodies.',
    ], 'Күй', 'Kui', 'A story told without words')


def build_qorzhyn():
    c = Cv()
    c.rrect((70, 120, 650, 150), 12, fill=WOOD, outline=BROWN, w=3.5)
    for x in (90, 630):
        c.rrect((x - 10, 120, x + 10, 620), 4, fill=WOODD, outline=BROWN, w=3)
    beam = L('beam', c, 4.0, 1.2, 'fade')
    c = Cv()
    c.rrect((160, 110, 560, 170), 20, fill=(150, 40, 46), outline=BROWN, w=3.5)
    band = L('band', c, 7.0, 1.0, 'drop')
    layers = [beam, band]
    for i, x0 in enumerate((130, 380)):
        c = Cv()
        c.rrect((x0, 160, x0 + 210, 470), 14, fill=(150, 40, 46), outline=BROWN, w=3.5)
        c.rrect((x0 + 18, 180, x0 + 192, 450), 8, fill=(210, 160, 80), outline=BROWN, w=2.5)
        for j, y in enumerate((230, 315, 400)):
            diamond(c, x0 + 105, y, 120, 70, RED if j % 2 else TURQ, BROWN, 2)
            ram_horn(c, x0 + 105, y + 4, 1.0, GOLDL, 2.5)
        for k in range(6):
            tx = x0 + 18 + k * 35
            c.line([(tx, 470), (tx, 520)], (RED, GOLD)[k % 2], 6)
            c.circle(tx, 526, 8, fill=(RED, GOLD)[k % 2])
        layers.append(L(f'pocket{i}', c, 10.0 + i * 3.5, 1.3, 'drop', rock=(1.5, 3.2, x0 + 105, 160)))
    labels = [
        label_layer('Two pockets', (240, 300), (20, 560 - 20), 10.8),
        label_layer('Woven ornaments', (485, 230), (470, 560 - 20), 14.4),
        label_layer('Tassels', (600, 520), (500, 30), 18.0),
    ]
    return Scene('qorzhyn', layers + labels, [
        'A qorzhyn is a double bag joined by a band.',
        'It hangs over a horse or camel, one pocket on each side.',
        'It is woven from wool and decorated with ornaments and tassels.',
        'At home, it hung on the wall of the yurt as a storage bag.',
    ], 'Қоржын', 'Qorzhyn', 'The double saddlebag')


def build_qudyq():
    cx = 360
    c = Cv()
    c.ell((40, 470, 680, 620), fill=(226, 206, 166))
    ground = L('ground', c, 4.0, 1.0, 'fade')
    c = Cv()
    c.rrect((cx - 170, 400, cx + 170, 560), 10, fill=STONE, outline=BROWN, w=3.5)
    for j, y in enumerate(range(400, 560, 32)):
        for x in range(cx - 170 + (20 if j % 2 else 0), cx + 170, 56):
            c.rrect((x + 2, y + 2, min(x + 54, cx + 168), y + 30), 6, fill=STONE if (x // 56 + j) % 2 else STONED, outline=BROWN, w=2)
    c.ell((cx - 170, 380, cx + 170, 420), fill=(40, 52, 60), outline=BROWN, w=3.5)
    wall = L('well', c, 7.5, 1.3, 'rise')
    c = Cv()
    for x in (cx - 200, cx + 200):
        c.rrect((x - 12, 120, x + 12, 560), 5, fill=WOODD, outline=BROWN, w=3)
    c.rrect((cx - 230, 120, cx + 230, 146), 8, fill=WOOD, outline=BROWN, w=3)
    c.circle(cx, 150, 22, fill=IRON, outline=BROWN, w=3)
    frame = L('frame', c, 11.0, 1.2, 'drop')
    c = Cv()
    c.line([(cx, 170), (cx, 300)], (200, 170, 120), 3, False)
    c.poly([(cx - 40, 300), (cx + 40, 300), (cx + 30, 370), (cx - 30, 370)], fill=LEATHER, outline=BROWN, w=3)
    c.ell((cx - 40, 292, cx + 40, 308), fill=LEATHERD, outline=BROWN, w=2.5)
    bucket = L('qauga', c, 15.0, 1.2, 'drop', float_=(6, 2.8))
    c = Cv()
    for k in range(4):
        c.circle(cx - 12 + k * 8, 380 + k * 14, 4, fill=WATER)
    c.rrect((470, 540, 680, 590), 10, fill=STONED, outline=BROWN, w=3)
    c.rrect((484, 548, 666, 566), 6, fill=WATER)
    water = L('water', c, 19.0, 1.0, 'fade')
    labels = [
        label_layer('Stone-lined wall', (cx - 120, 480), (20, 360), 8.4),
        label_layer('Wooden frame\nand pulley', (cx + 20, 150), (430, 30), 11.8),
        label_layer('Qauga: leather\nbucket', (cx + 40, 330), (460, 230), 15.8),
        label_layer('Trough for herds', (580, 560), (420, 600 - 30), 19.8),
    ]
    return Scene('qudyq', [ground, wall, frame, bucket, water] + labels, [
        'A qudyq is a well, and on the dry steppe a well meant life.',
        'Skilled masters knew where to dig and lined the walls with stone.',
        'Water was raised in a leather bucket called a qauga.',
        'Digging a well for others was considered a great good deed.',
    ], 'Құдық', 'Qudyq', 'The well that gives life')


def build_qurt():
    c = Cv()
    c.poly([(70, 420), (650, 420), (690, 560), (30, 560)], fill=WOODL, outline=BROWN, w=3.5)
    c.poly([(30, 560), (690, 560), (690, 584), (30, 584)], fill=WOODD, outline=BROWN, w=3)
    board = L('board', c, 4.0, 1.2, 'rise')
    rng = np.random.RandomState(6)
    layers = [board]
    for row in range(3):
        c = Cv()
        y = 450 + row * 40
        for k in range(8):
            x = 120 + k * 64 + (row % 2) * 30 + rng.randint(-6, 6)
            if (k + row) % 3 == 2:
                c.poly([(x - 20, y + 16), (x + 20, y + 16), (x + 4, y - 30)], fill=(244, 240, 228), outline=BROWNSOFT, w=2.5)
            else:
                col = (244, 240, 228) if (k + row) % 2 else (226, 206, 168)
                c.circle(x, y, 22, fill=col, outline=BROWNSOFT, w=2.5)
                c.circle(x - 7, y - 7, 5, fill=(255, 255, 255, 160))
        layers.append(L(f'row{row}', c, 7.5 + row * 3.5, 1.2, 'drop'))
    c = Cv()
    c.poly(bez((540, 420), (500, 300), (540, 220), (590, 230)) + bez((590, 230), (640, 220), (680, 300), (640, 420))[1:], fill=(220, 206, 180), outline=BROWN, w=3)
    c.rrect((560, 222, 620, 238), 6, fill=RED)
    bag = L('bag', c, 18.5, 1.2, 'fade')
    c = Cv()
    c.circle(120, 120, 46, fill=(248, 220, 130))
    for k in range(8):
        a = 2 * math.pi * k / 8
        c.line([(120 + 56 * math.cos(a), 120 + 56 * math.sin(a)), (120 + 76 * math.cos(a), 120 + 76 * math.sin(a))], (240, 200, 110), 4)
    sun = L('sun', c, 6.0, 1.2, 'fade')
    layers.insert(1, sun)
    labels = [
        label_layer('Dried in the sun', (150, 150), (200, 70), 6.6),
        label_layer('Salty curd balls', (250, 450), (20, 300), 8.4),
        label_layer('Hand-shaped\ncones', (330, 476), (300, 220), 12.0),
        label_layer('Bag for the road', (590, 300), (470, 130), 19.0),
    ]
    return Scene('qurt', layers + [bag] + labels, [
        'Qurt is a dried dairy food made from strained sour milk.',
        'The curd is salted and shaped by hand into balls or cones.',
        'It dries in the sun and wind until it is as hard as stone.',
        'Qurt keeps for months, so nomads carried it on long journeys.',
    ], 'Құрт', 'Qurt', 'The dried cheese of the road')


def build_qystau():
    c = Cv()
    c.poly([(0, 330), (140, 240), (290, 320), (450, 210), (600, 300), (720, 250), (720, 440), (0, 440)], fill=SNOWS, outline=BROWNSOFT, w=2)
    c.poly(bez((0, 420), (240, 380), (480, 440), (720, 400)) + [(720, 640), (0, 640)], fill=SNOW)
    land = L('valley', c, 4.0, 1.3, 'fade')
    c = Cv()
    c.rrect((100, 330, 400, 500), 6, fill=CLAY, outline=BROWN, w=3.5)
    c.rrect((86, 306, 414, 338), 6, fill=(140, 104, 70), outline=BROWN, w=3)
    c.rrect((92, 294, 408, 312), 8, fill=SNOW, outline=SNOWS, w=2)
    c.rrect((140, 380, 200, 500), 4, fill=WOODD, outline=BROWN, w=3)
    c.rrect((260, 370, 340, 430), 4, fill=(250, 214, 120), outline=BROWN, w=3)
    c.line([(300, 370), (300, 430)], BROWN, 2.5, False)
    c.rrect((330, 250, 360, 306), 4, fill=CLAY, outline=BROWN, w=2.5)
    house = L('house', c, 7.5, 1.3, 'rise')
    c = Cv()
    for k in range(6):
        c.circle(345 + k * 6, 230 - k * 22, 10 + k * 3, fill=(230, 230, 236, 170))
    smoke = L('smoke', c, 10.5, 1.4, 'fade', float_=(6, 3), sway=(4, 4))
    c = Cv()
    for x in range(440, 690, 30):
        c.rrect((x, 400, x + 10, 520), 3, fill=WOODD, outline=BROWN, w=2)
    for y in (430, 480):
        c.rrect((430, y, 690, y + 10), 3, fill=WOOD, outline=BROWN, w=2)
    for i, x in enumerate((490, 560, 620)):
        draw_sheep(c, x, 500, 0.8, 1 if i % 2 else -1)
    pen = L('pen', c, 13.5, 1.2, 'rise')
    c = Cv()
    c.poly(bez((10, 560), (20, 420), (130, 420), (150, 560)), fill=(214, 190, 100), outline=BROWN, w=3)
    c.ell((30, 410, 130, 450), fill=SNOW)
    hay = L('hay', c, 17.5, 1.2, 'rise')
    labels = [
        label_layer('Sheltered valley', (450, 260), (480, 120), 5.0),
        label_layer('Clay and turf house', (230, 340), (40, 200), 8.4),
        label_layer('Pen for the herds', (560, 440), (440, 560 - 10), 14.2),
        label_layer('Hay for the winter', (80, 480), (20, 590 - 10), 18.2),
    ]
    return Scene('qystau', [land, house, smoke, pen, hay] + labels, [
        'The qystau is the winter home of a nomadic family.',
        'It lies in a sheltered valley, away from wind and deep snow.',
        'Houses of clay, stone or turf stood beside pens for the animals.',
        'The same family returned to its qystau year after year.',
    ], 'Қыстау', 'Qystau', 'The sheltered winter home')


def build_saba():
    cx = 360
    c = Cv()
    shadow(c, cx, 590, 420)
    c.rrect((cx - 200, 520, cx + 200, 584), 8, fill=WOODD, outline=BROWN, w=3.5)
    for x in (cx - 180, cx + 150):
        c.rrect((x, 584, x + 30, 600), 4, fill=WOODD, outline=BROWN, w=2.5)
    stand = L('stand', c, 4.0, 1.2, 'rise')
    c = Cv()
    body = prof_poly(cx, [(150, 44), (190, 60), (240, 110), (330, 160), (430, 168), (500, 150), (530, 110)])
    c.poly(body, fill=(102, 60, 34), outline=BROWN, w=4)
    c.ell((cx - 120, 300, cx - 40, 460), fill=(150, 98, 60, 90))
    c.line([(cx + 4, 160), (cx + 4, 528)], (226, 210, 180), 3, False)
    vessel = L('saba', c, 7.5, 1.3, 'rise')
    c = Cv()
    for y in (330, 430):
        half = 162 if y == 330 else 166
        c.line(bez((cx - half, y), (cx - half / 2, y + 22), (cx + half / 2, y + 22), (cx + half, y)), GOLD, 6, False)
        for k in range(-3, 4):
            diamond(c, cx + k * 44, y + 46 - abs(k) * 4, 18, 24, GOLD)
    deco = L('ornament', c, 11.5, 1.2, 'fade')
    c = Cv()
    c.line([(cx + 10, 300), (cx + 22, 40)], BROWN, 12)
    c.line([(cx + 10, 300), (cx + 22, 40)], WOODL, 7)
    c.circle(cx + 22, 36, 10, fill=WOODD, outline=BROWN, w=2)
    pispek = L('pispek', c, 15.5, 1.2, 'drop', rock=(4, 1.6, cx + 10, 200))
    c = Cv()
    for k in range(4):
        c.circle(cx + 60 + k * 20, 140 - k * 8, 6, fill=(250, 248, 236))
    foam = L('foam', c, 19.5, 1.0, 'fade', float_=(5, 2))
    labels = [
        label_layer('Smoked horse hide', (cx - 90, 380), (20, 260), 8.4),
        label_layer('Decorated bands', (cx + 120, 340), (470, 380), 12.0),
        label_layer('Pispek plunger', (cx + 18, 100), (430, 60), 16.0),
        label_layer('Wooden stand', (cx - 120, 550), (20, 600 - 30), 5.0),
    ]
    return Scene('saba', [stand, vessel, deco, pispek, foam] + labels, [
        'A saba is a large vessel made of smoked horse hide.',
        'Mare’s milk is poured inside to become kymyz.',
        'The family stirs it many times a day with a wooden pispek.',
        'A full saba was a sign of a generous, welcoming home.',
    ], 'Саба', 'Saba', 'The leather vessel for kymyz')


def build_shanyraq():
    cx, cy = 360, 320
    c = Cv()
    c.circle(cx, cy, 300, fill=(234, 222, 196))
    for k in range(36):
        a = 2 * math.pi * k / 36
        c.line([(cx + 150 * math.cos(a), cy + 150 * math.sin(a)), (cx + 310 * math.cos(a), cy + 310 * math.sin(a))], (180, 92, 56), 7)
    poles = L('uyk', c, 4.0, 1.4, 'fade')
    c = Cv()
    c.circle(cx, cy, 150, outline=BROWN, w=34)
    c.circle(cx, cy, 150, outline=WOODD, w=26)
    for k in range(36):
        a = 2 * math.pi * k / 36 + 0.09
        diamond(c, cx + 150 * math.cos(a), cy + 150 * math.sin(a), 10, 10, GOLD)
    ring = L('ring', c, 8.0, 1.3, 'drop')
    c = Cv()
    for off in (-60, 0, 60):
        L2 = math.sqrt(140 ** 2 - off ** 2)
        c.line([(cx - L2, cy + off), (cx + L2, cy + off)], BROWN, 18)
        c.line([(cx - L2, cy + off), (cx + L2, cy + off)], WOODL, 12)
    bars1 = L('kuldiresh1', c, 12.0, 1.2, 'fade')
    c = Cv()
    for off in (-60, 0, 60):
        L2 = math.sqrt(140 ** 2 - off ** 2)
        c.line([(cx + off, cy - L2), (cx + off, cy + L2)], BROWN, 18)
        c.line([(cx + off, cy - L2), (cx + off, cy + L2)], WOODL, 12)
    bars2 = L('kuldiresh2', c, 15.0, 1.2, 'fade')
    c = Cv()
    for k in range(12):
        a = 2 * math.pi * k / 12
        c.line([(cx, cy), (cx + 120 * math.cos(a), cy + 120 * math.sin(a))], (255, 240, 190, 70), 10, False)
    c.circle(cx, cy, 30, fill=(255, 240, 190, 120))
    light = L('light', c, 19.0, 1.4, 'fade')
    labels = [
        label_layer('Roof poles: uyk', (cx + 240, cy + 160), (480, 580 - 10), 5.0),
        label_layer('Crown ring', (cx - 150, cy + 20), (20, 120), 8.8),
        label_layer('Crossed bars:\nkuldiresh', (cx + 60, cy - 60), (470, 60), 15.6),
        label_layer('Light and air', (cx, cy), (20, 500), 19.6),
    ]
    return Scene('shanyraq', [poles, ring, bars1, bars2, light] + labels, [
        'The shanyraq is the wooden crown ring at the top of the yurt.',
        'The curved roof poles rest against it all around.',
        'Crossed bars, the kuldiresh, let in light and let out smoke.',
        'It is the symbol of the family and appears on Kazakhstan’s coat of arms.',
    ], 'Шаңырақ', 'Shanyraq', 'The crown of the yurt')


def build_sheber():
    c = Cv()
    shadow(c, 360, 580, 560)
    c.rrect((110, 300, 610, 560), 8, fill=WOOD, outline=BROWN, w=4)
    c.rrect((96, 260, 624, 310), 8, fill=WOODD, outline=BROWN, w=3.5)
    for x in (130, 570):
        c.rrect((x, 556, x + 30, 584), 4, fill=WOODD, outline=BROWN, w=3)
    chest = L('chest', c, 4.0, 1.3, 'rise')
    c = Cv()
    for x in (210, 360, 510):
        diamond(c, x, 430, 110, 150, (172, 112, 64), BROWN, 2.5)
        ram_horn(c, x, 430, 2.0, GOLDL, 3.5)
    carving = L('carving', c, 7.5, 1.4, 'fade')
    c = Cv()
    for x, y in ((110, 260), (580, 260), (110, 520), (580, 520)):
        c.poly([(x, y), (x + 40, y), (x, y + 40)] if x < 300 else [(x + 44, y), (x + 4, y), (x + 44, y + 40)], fill=GOLD, outline=BROWN, w=2)
    c.rrect((340, 300, 380, 350), 6, fill=GOLD, outline=BROWN, w=2.5)
    fittings = L('fittings', c, 11.5, 1.0, 'fade')
    c = Cv()
    c.line([(170, 230), (330, 250)], BROWN, 16)
    c.line([(170, 230), (330, 250)], WOODL, 10)
    c.poly([(330, 242), (400, 248), (400, 258), (330, 258)], fill=SILVER, outline=BROWN, w=2)
    c.line([(440, 240), (560, 220)], BROWN, 12)
    c.line([(440, 240), (560, 220)], WOODL, 7)
    c.rrect((540, 180, 600, 250), 10, fill=WOODD, outline=BROWN, w=3)
    tools = L('tools', c, 15.5, 1.2, 'drop')
    c = Cv()
    for k in range(10):
        c.line([(400 + k * 8, 120 + (k % 3) * 6), (420 + k * 8, 150)], (200, 160, 110), 3, False)
    shav = L('shavings', c, 19.5, 1.0, 'fade', float_=(4, 2))
    labels = [
        label_layer('Wooden chest', (160, 520), (20, 600 - 10), 5.0),
        label_layer('Ram’s horn carving', (210, 430), (20, 140), 8.6),
        label_layer('Gold fittings', (600, 280), (500, 330), 12.0),
        label_layer('Chisel and mallet', (480, 236), (420, 60), 16.0),
    ]
    return Scene('sheber', [chest, carving, fittings, tools, shav] + labels, [
        'A sheber is a master craftsman with "golden hands".',
        'Shebers made yurt frames, chests, saddles, bowls and felt.',
        'They decorated their work with ornaments such as the ram’s horn.',
        'Their skill passed from master to apprentice through generations.',
    ], 'Шебер', 'Sheber', 'The master craftsman')


def build_usta():
    cx = 360
    c = Cv()
    shadow(c, cx, 600, 420)
    c.poly(prof_poly(cx, [(430, 120), (600, 130)]), fill=WOODD, outline=BROWN, w=3.5)
    c.ell((cx - 120, 410, cx + 120, 450), fill=(170, 116, 70), outline=BROWN, w=3)
    for r in (30, 60, 90):
        c.ell((cx - r, 430 - r / 6, cx + r, 430 + r / 6), outline=(140, 92, 56), w=2)
    stump = L('stump', c, 4.0, 1.3, 'rise')
    c = Cv()
    c.poly([(cx - 70, 430), (cx + 70, 430), (cx + 40, 360), (cx - 40, 360)], fill=IRON, outline=BROWN, w=3.5)
    c.poly([(cx - 160, 300), (cx + 120, 300), (cx + 280, 330), (cx + 120, 362), (cx - 160, 362)], fill=IRON, outline=BROWN, w=3.5)
    c.poly([(cx - 160, 300), (cx + 120, 300), (cx + 120, 312), (cx - 160, 312)], fill=IRONL)
    anvil = L('anvil', c, 7.5, 1.3, 'drop')
    c = Cv()
    pts = [(cx - 20 + 70 * math.cos(a), 290 + 26 * math.sin(a)) for a in np.linspace(-0.2 * math.pi, 1.2 * math.pi, 30)]
    pts = [(cx - 20 + 70 * math.cos(a), 280 - 16 * math.sin(a)) for a in np.linspace(-0.25 * math.pi, 1.25 * math.pi, 30)]
    c.line(pts, (120, 40, 10), 18)
    c.line(pts, GLOW, 12)
    shoe = L('horseshoe', c, 11.0, 1.0, 'fade')
    c = Cv()
    c.line([(cx + 60, 120), (cx + 250, 40)], BROWN, 14)
    c.line([(cx + 60, 120), (cx + 250, 40)], WOODL, 8)
    c.rrect((cx + 10, 80, cx + 90, 150), 8, fill=IRON, outline=BROWN, w=3)
    hammer = L('hammer', c, 14.5, 1.0, 'drop', rock=(8, 1.2, cx + 250, 40))
    c = Cv()
    for k in range(14):
        a = math.radians(-160 + k * 10)
        r0, r1 = 40, 90 + (k % 3) * 20
        c.line([(cx - 20 + r0 * math.cos(a), 270 + r0 * math.sin(a)), (cx - 20 + r1 * math.cos(a), 270 + r1 * math.sin(a))], (250, 190, 70), 3, False)
    sparks = L('sparks', c, 18.5, 0.6, 'fade', float_=(4, 0.6))
    labels = [
        label_layer('Anvil', (cx + 200, 330), (520, 420), 8.4),
        label_layer('Red-hot horseshoe', (cx - 80, 278), (20, 160), 11.6),
        label_layer('Hammer', (cx + 160, 76), (500, 120), 15.2),
        label_layer('Tree-stump base', (cx - 100, 520), (20, 560), 5.0),
    ]
    return Scene('usta', [stump, anvil, shoe, hammer, sparks] + labels, [
        'An usta is a master, and above all a blacksmith.',
        'He heated iron in the forge until it glowed.',
        'Then he shaped it on the anvil with a hammer.',
        'Horseshoes, knives and tools: every aul needed its usta.',
    ], 'Ұста', 'Usta', 'The blacksmith master')


def build_zerger():
    c = Cv()
    c.ell((40, 400, 680, 620), fill=(36, 84, 90), outline=GOLD, w=3)
    cloth = L('velvet', c, 4.0, 1.2, 'fade')
    c = Cv()
    c.ell((120, 200, 420, 540), outline=SILVERD, w=60)
    c.ell((120, 200, 420, 540), outline=SILVER, w=48)
    c.ell((150, 230, 390, 510), outline=SILVERD, w=3)
    c.ell((92, 172, 448, 568), outline=SILVERD, w=3)
    bracelet = L('bilezik', c, 7.5, 1.3, 'rise')
    c = Cv()
    for k in range(10):
        a = 2 * math.pi * k / 10
        x, y = 270 + 150 * math.cos(a), 370 + 170 * math.sin(a)
        c.ell((x - 14, y - 12, x + 14, y + 12), fill=CARN if k % 2 else TURQ, outline=SILVERD, w=3)
    for k in range(40):
        a = 2 * math.pi * k / 40
        c.circle(270 + 172 * math.cos(a), 370 + 194 * math.sin(a), 3, fill=SILVERD)
    stones = L('stones', c, 11.5, 1.2, 'fade')
    c = Cv()
    c.ell((470, 420, 590, 520), outline=SILVERD, w=18)
    c.ell((470, 420, 590, 520), outline=SILVER, w=12)
    c.ell((496, 370, 564, 430), fill=CARN, outline=SILVERD, w=6)
    c.ell((510, 380, 530, 396), fill=(240, 150, 120))
    ring = L('ring', c, 15.5, 1.2, 'drop')
    c = Cv()
    c.circle(560, 130, 18, outline=SILVERD, w=5)
    diamond(c, 560, 220, 80, 110, SILVER, SILVERD, 3)
    c.circle(560, 220, 12, fill=TURQ, outline=SILVERD, w=2)
    for k in range(3):
        c.line([(536 + k * 24, 275), (536 + k * 24, 320)], SILVERD, 3, False)
        c.circle(536 + k * 24, 324, 6, fill=CARN)
    earring = L('earring', c, 19.0, 1.2, 'drop', rock=(4, 2.4, 560, 130))
    labels = [
        label_layer('Bilezik bracelet', (130, 380), (20, 100), 8.4),
        label_layer('Carnelian and\nturquoise', (420, 370), (430, 290), 12.0),
        label_layer('Ring', (530, 470), (600, 540), 16.0),
        label_layer('Earring', (600, 200), (620, 60), 19.8),
    ]
    return Scene('zerger', [cloth, bracelet, stones, ring, earring] + labels, [
        'A zerger is a jeweller, a master of silver and gold.',
        'Zergers made bracelets, rings, earrings and pendants.',
        'Fine wire, tiny metal balls and stones decorate the silver.',
        'Silver was believed to protect its wearer.',
    ], 'Зергер', 'Zerger', 'The silver jeweller')


def build_zhyr():
    c = Cv()
    carpet(c, 480, 610)
    rug = L('carpet', c, 4.0, 1.2, 'fade')
    c = Cv()
    body = prof_poly(220, [(330, 40), (380, 60), (440, 70), (500, 62), (540, 40)])
    c.poly(body, fill=WOOD, outline=BROWN, w=3.5)
    c.ell((180, 450, 260, 520), fill=(236, 222, 196), outline=BROWN, w=3)
    c.rrect((204, 120, 236, 340), 8, fill=WOODD, outline=BROWN, w=3)
    c.poly([(200, 120), (250, 70), (262, 90), (226, 128)], fill=WOODD, outline=BROWN, w=3)
    for x in (214, 226):
        c.line([(x, 130), (x, 520)], (240, 230, 210), 2, False)
    c.line(bez((300, 200), (330, 300), (330, 420), (300, 520)), BROWN, 5)
    c.line([(300, 205), (300, 515)], (240, 230, 210), 2, False)
    kobyz = L('kobyz', c, 7.5, 1.3, 'rise')
    c = Cv()
    c.poly([(400, 470), (520, 420), (520, 520), (400, 560)], fill=IVORY, outline=BROWN, w=3)
    c.poly([(520, 420), (640, 470), (640, 560), (520, 520)], fill=IVORY, outline=BROWN, w=3)
    for k in range(5):
        c.line([(416, 490 + k * 14 - k * 2), (504, 452 + k * 14)], BROWNSOFT, 2, False)
        c.line([(536, 452 + k * 14), (624, 490 + k * 14 - k * 2)], BROWNSOFT, 2, False)
    book = L('book', c, 11.5, 1.3, 'drop')
    c = Cv()
    for k in range(3):
        y = 120 + k * 70
        c.rrect((380, y, 660, y + 46), 22, fill=IVORY, outline=GOLD, w=2.5)
        for j in range(3):
            c.line([(400 + j * 86, y + 23), (460 + j * 86, y + 23)], (TURQD, RED, GOLD)[(k + j) % 3], 4)
    lines = L('lines', c, 15.5, 1.3, 'fade', float_=(5, 3.5))
    c = Cv()
    for k in range(3):
        c.circle(560 + k * 30, 70, 8, fill=GOLD)
    stars = L('stars', c, 19.5, 1.0, 'fade')
    labels = [
        label_layer('Kobyz', (220, 300), (20, 220), 8.4),
        label_layer('Verses of heroes', (520, 470), (440, 590 - 10), 12.0),
        label_layer('Thousands of lines\nby heart', (500, 190), (390, 30), 16.0),
    ]
    return Scene('zhyr', [rug, kobyz, book, lines, stars] + labels, [
        'Zhyr is epic poetry about heroes, battles and history.',
        'It is sung or recited to the dombyra or the kobyz.',
        'The zhyrau knew thousands of lines by heart.',
        'Epics such as "Koblandy Batyr" lived on through zhyr for centuries.',
    ], 'Жыр', 'Zhyr', 'The epic song of heroes')


BUILDERS2 = {
    'khan-shatyr': build_khan_shatyr, 'kyz-zhibek': build_kyz_zhibek, 'aisha-bibi': build_aisha_bibi, 'karakhan': build_karakhan,
    'airan': build_airan, 'aitys': build_aitys, 'asyk': build_asyk, 'at-arba': build_at_arba, 'baige': build_baige,
    'baursak': build_baursak, 'zhailau': build_zhailau, 'kazakh-kuresi': build_kazakh_kuresi, 'keruen': build_keruen,
    'kosh': build_kosh, 'kymyz': build_kymyz, 'kui': build_kui, 'qorzhyn': build_qorzhyn, 'qudyq': build_qudyq,
    'qurt': build_qurt, 'qystau': build_qystau, 'saba': build_saba, 'shanyraq': build_shanyraq, 'sheber': build_sheber,
    'usta': build_usta, 'zerger': build_zerger, 'zhyr': build_zhyr,
}
