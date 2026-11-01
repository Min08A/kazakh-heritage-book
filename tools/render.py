"""Render one animated explainer video per chapter (MP4 + WebM) and a cover image.

Usage:  python3 render.py [slug ...] [--still-only] [--no-webm]

Everything is drawn and synthesised by code (illustrations from art.py,
music from Karplus-Strong plucked strings). Requires: Pillow, numpy, opencv, ffmpeg.
"""
import math
import os
import subprocess
import sys
import wave

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import art

FW, FH, FPS = 1280, 720, 24
DUR = 40.0
SEGS = [3.5, 11.5, 19.5, 27.5, 35.5]
OUT_V = os.path.join(os.path.dirname(__file__), '..', 'media', 'videos')
OUT_I = os.path.join(os.path.dirname(__file__), '..', 'media', 'images')
SCENE_X, SCENE_Y = 30, 40
PANEL_X = 800

LORA = '/usr/share/fonts/truetype/google-fonts/Lora-Variable.ttf'
LORA_I = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
POP = '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf'


def lora(size, weight=400, italic=False):
    f = ImageFont.truetype(LORA_I if italic else LORA, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def ease(p):
    p = min(max(p, 0.0), 1.0)
    return p * p * (3 - 2 * p)


def pre(img):
    a = np.asarray(img.convert('RGBA'), dtype=np.float32) / 255.0
    al = a[..., 3:4]
    return np.concatenate([a[..., :3] * al, al], axis=2)


# ------------------------------------------------------------------ background
def make_bg():
    img = Image.new('RGB', (FW, FH), art.CREAM)
    d = ImageDraw.Draw(img)
    for y in range(10, FH, 24):
        for x in range(10 + (y // 24 % 2) * 12, FW, 24):
            d.ellipse([x - 1, y - 1, x + 1, y + 1], fill=art.BEIGE)
    # stage behind the object
    d.ellipse([SCENE_X + 20, SCENE_Y - 10, SCENE_X + 700, SCENE_Y + 650], fill=(238, 226, 200))
    d.ellipse([SCENE_X + 40, SCENE_Y + 10, SCENE_X + 680, SCENE_Y + 630], outline=art.GOLD, width=2)
    # panel card
    d.rounded_rectangle([PANEL_X, 70, FW - 30, FH - 70], radius=28, fill=art.IVORY, outline=art.BEIGE, width=2)
    # ornament rows
    for y0 in (14, FH - 34):
        for x in range(10, FW, 20):
            d.polygon([(x, y0 + 10), (x + 10, y0), (x + 20, y0 + 10), (x + 10, y0 + 20)], outline=art.GOLD)
    return np.asarray(img, dtype=np.float32) / 255.0


def text_wrap(d, text, font, width):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def spaced(d, xy, text, font, fill, spacing=3):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill)
        x += d.textlength(ch, font=font) + spacing


PW, PH = FW - 30 - PANEL_X - 0, FH - 140     # panel text area
PADX = 34


def panel_layers(sc, num):
    """Returns (header, [4 captions], outro) as premultiplied float arrays of the panel size."""
    size = (FW - PANEL_X, FH)  # draw in panel coords, full height
    tw = FW - 30 - PANEL_X - 2 * PADX

    def new():
        im = Image.new('RGBA', size, (0, 0, 0, 0))
        return im, ImageDraw.Draw(im)

    # header
    im, d = new()
    spaced(d, (PADX, 104), f'CHAPTER {num:02d}', ImageFont.truetype(POP, 20), art.GOLD, 4)
    fs = 66
    while True:
        f = lora(fs, 700)
        if d.textlength(sc.title, font=f) <= tw or fs <= 34:
            break
        fs -= 2
    d.text((PADX, 138), sc.title, font=f, fill=art.BROWN)
    d.text((PADX, 138 + fs + 10), sc.native, font=lora(30, 400, False), fill=art.BROWNSOFT)
    y = 138 + fs + 62
    d.line([(PADX, y), (PADX + 90, y)], fill=art.GOLD, width=3)
    d.polygon([(PADX + 100, y), (PADX + 108, y - 6), (PADX + 116, y), (PADX + 108, y + 6)], fill=art.GOLD)
    header = pre(im)
    cap_y = y + 34

    caps = []
    for text in sc.captions:
        im, d = new()
        f = lora(31, 500)
        for i, line in enumerate(text_wrap(d, text, f, tw)):
            d.text((PADX, cap_y + i * 44), line, font=f, fill=art.BROWN)
        caps.append(pre(im))

    im, d = new()
    f = lora(31, 600)
    lines = text_wrap(d, f'Scan the QR code in the book to explore the {sc.title} in 3D.', f, tw)
    for i, line in enumerate(lines):
        d.text((PADX, cap_y + i * 44), line, font=f, fill=art.TURQD)
    yy = cap_y + len(lines) * 44 + 18
    q = 64
    d.rounded_rectangle([PADX, yy, PADX + q + 24, yy + q + 24], radius=14, outline=art.TURQ, width=3)
    rng = np.random.RandomState(3)
    cell = q // 8
    for gy in range(8):
        for gx in range(8):
            finder = (gx < 3 and gy < 3) or (gx > 4 and gy < 3) or (gx < 3 and gy > 4)
            if finder:
                on = not (gx % 7 in (1, 6) and False) and ((gx in (0, 2, 5, 7) or gy in (0, 2, 5, 7)) or (gx in (1, 6) and gy in (1, 6)) or True)
                ring = (gx in (0, 2, 5, 7) or gy in (0, 2, 5, 7))
                on = ring or (gx in (1, 6) and gy in (1, 6))
            else:
                on = rng.rand() > 0.5
            if on:
                d.rectangle([PADX + 12 + gx * cell, yy + 12 + gy * cell, PADX + 12 + (gx + 1) * cell - 1, yy + 12 + (gy + 1) * cell - 1], fill=art.TURQ)
    outro = pre(im)
    return header, caps, outro


# ------------------------------------------------------------------ scene compositing
def prep_layers(sc):
    out = []
    for l in sc.layers:
        p = pre(l.img)
        ys, xs = np.where(p[..., 3] > 0.004)
        pad = 90
        x0, x1 = max(xs.min() - pad, 0), min(xs.max() + pad + 1, art.W)
        y0, y1 = max(ys.min() - pad, 0), min(ys.max() + pad + 1, art.H)
        out.append((l, p[y0:y1, x0:x1].copy(), (x0, y0, x1, y1)))
    return out


def scene_at(prepped, t):
    acc = np.zeros((art.H, art.W, 4), np.float32)
    for l, crop, (x0, y0, x1, y1) in prepped:
        if t < l.t0:
            continue
        loc = t - l.t0
        e = ease(loc / l.dur)
        dx = dy = 0.0
        if l.effect == 'rise':
            dy += (1 - e) * 26
        elif l.effect == 'drop':
            dy -= (1 - e) * 30
        ramp = min(1.0, loc / 1.5)
        if l.sway:
            dx += l.sway[0] * math.sin(2 * math.pi * loc / l.sway[1]) * ramp
        if l.float_:
            dy += l.float_[0] * math.sin(2 * math.pi * loc / l.float_[1]) * ramp - 0
        rot = 0.0
        pv = (0, 0)
        if l.rock:
            rot = l.rock[0] * math.sin(2 * math.pi * loc / l.rock[1]) * ramp
            pv = (l.rock[2], l.rock[3])
        h, w = crop.shape[:2]
        if dx == 0 and dy == 0 and rot == 0:
            src = crop
        else:
            M = cv2.getRotationMatrix2D((pv[0], pv[1]), rot, 1.0) if rot else np.array([[1, 0, 0], [0, 1, 0]], np.float64)
            M = M.astype(np.float64)
            M[0, 2] += dx
            M[1, 2] += dy
            # convert global-coordinate transform to crop-local coordinates
            Tin = np.array([[1, 0, x0], [0, 1, y0], [0, 0, 1]], np.float64)
            Tout = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]], np.float64)
            Mg = np.vstack([M, [0, 0, 1]])
            Ml = (Tout @ Mg @ Tin)[:2]
            src = cv2.warpAffine(crop, Ml, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
        reg = acc[y0:y1, x0:x1]
        acc[y0:y1, x0:x1] = src * e + reg * (1 - src[..., 3:4] * e)
    return acc


def over(dst, src_pre, x, y):
    h, w = src_pre.shape[:2]
    reg = dst[y:y + h, x:x + w]
    dst[y:y + h, x:x + w] = src_pre[..., :3] + reg * (1 - src_pre[..., 3:4])


def frame_at(bg, prepped, header, caps, outro, t):
    f = bg.copy()
    acc = scene_at(prepped, t)
    zoom = 1.0 + 0.045 * (t / DUR)
    M = cv2.getRotationMatrix2D((art.W / 2, art.H / 2), 0, zoom)
    acc = cv2.warpAffine(acc, M, (art.W, art.H), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    over(f, acc, SCENE_X, SCENE_Y)

    ph = f[:, PANEL_X:]
    hp = header * ease(t / 1.2)
    ph[:] = hp[..., :3] + ph * (1 - hp[..., 3:4])
    for k in range(4):
        s, e = SEGS[k], SEGS[k + 1]
        a = ease((t - s) / 0.6) * ease((e - t) / 0.5)
        if a > 0.002:
            c = caps[k] * a
            ph[:] = c[..., :3] + ph * (1 - c[..., 3:4])
    a = ease((t - SEGS[4]) / 0.7)
    if a > 0.002:
        c = outro * a
        ph[:] = c[..., :3] + ph * (1 - c[..., 3:4])

    # progress bar
    x = int(FW * t / DUR)
    f[FH - 8:FH, :] = np.array(art.SAND, np.float32) / 255
    f[FH - 8:FH, :x] = np.array(art.TURQ, np.float32) / 255
    return f


# ------------------------------------------------------------------ music
SR = 44100


def pluck(freq, dur, decay=0.9965, rng=None):
    n = int(SR / freq)
    rng = rng or np.random.RandomState(1)
    buf = rng.uniform(-1, 1, n)
    for _ in range(2):  # softer attack
        buf = 0.5 * (buf + np.roll(buf, 1))
    total = int(SR * dur)
    out = np.zeros(total + n)
    prev = buf.copy()
    prev2_last = 0.0
    out[:n] = prev
    pos = n
    while pos < total:
        shifted = np.concatenate([[prev2_last], prev[:-1]])
        cur = decay * 0.5 * (prev + shifted)
        prev2_last = prev[-1]
        out[pos:pos + n] = cur[: len(out[pos:pos + n])]
        prev = cur
        pos += n
    return out[:total]


def bowed(freq, dur):
    t = np.arange(int(SR * dur)) / SR
    vib = 1 + 0.004 * np.sin(2 * math.pi * 5.2 * t) * np.minimum(t / 0.6, 1)
    ph = 2 * math.pi * np.cumsum(freq * vib) / SR
    sig = sum(np.sin(k * ph) / (k ** 1.15) for k in range(1, 12))
    env = np.minimum(t / 0.25, 1) * np.minimum((dur - t) / 0.4, 1)
    return sig * env * 0.5


MUSIC = {
    'dombra': dict(root=146.83, scale=[0, 3, 5, 7, 10], bpm=118, kind='pluck'),
    'yurt': dict(root=130.81, scale=[0, 2, 4, 7, 9], bpm=84, kind='pluck'),
    'kobyz': dict(root=110.0, scale=[0, 2, 3, 7, 8], bpm=60, kind='bow'),
    'saukele': dict(root=164.81, scale=[0, 2, 4, 7, 9], bpm=92, kind='pluck'),
    'shapan': dict(root=138.59, scale=[0, 3, 5, 7, 10], bpm=104, kind='pluck'),
    'beshbarmak': dict(root=146.83, scale=[0, 2, 4, 7, 9], bpm=124, kind='pluck'),
    'besik': dict(root=196.0, scale=[0, 2, 4, 7, 9], bpm=66, kind='pluck'),
    'torsyk': dict(root=123.47, scale=[0, 3, 5, 7, 10], bpm=112, kind='pluck'),
}


def make_music(slug, path):
    m = MUSIC[slug]
    rng = np.random.RandomState(sum(map(ord, slug)))
    total = int(SR * DUR)
    mix = np.zeros(total + SR * 3)
    beat = 60.0 / m['bpm']
    nbeats = int(DUR / beat) - 1
    deg = 2
    for b in range(nbeats):
        t0 = b * beat
        if m['kind'] == 'pluck':
            # gallop: accent on the low string, then two quick melody notes
            subs = [(0.0, 'low'), (beat / 3, 'mel'), (2 * beat / 3, 'mel')]
            for off, kind in subs:
                if kind == 'low':
                    f = m['root']
                    amp = 0.55
                else:
                    deg = int(np.clip(deg + rng.choice([-2, -1, -1, 0, 1, 1, 2]), 0, 9))
                    octv, idx = divmod(deg, 5)
                    f = m['root'] * 2 * 2 ** ((m['scale'][idx] + 12 * octv) / 12)
                    amp = 0.38
                note = pluck(f, 1.1, rng=rng)
                s = int((t0 + off) * SR)
                mix[s:s + len(note)] += note * amp
        else:
            if b % 2 == 0:
                deg = int(np.clip(deg + rng.choice([-2, -1, 0, 1, 2]), 0, 7))
                octv, idx = divmod(deg, 5)
                f = m['root'] * 2 ** ((m['scale'][idx] + 12 * octv) / 12)
                note = bowed(f, beat * 2.1)
                s = int(t0 * SR)
                mix[s:s + len(note)] += note * 0.5
    mix = mix[:total]
    # light echo
    for delay, g in ((0.18, 0.28), (0.37, 0.16)):
        d = int(delay * SR)
        mix[d:] += mix[:-d] * g
    t = np.arange(total) / SR
    mix *= np.minimum(t / 1.5, 1) * np.minimum((DUR - t) / 2.5, 1)
    mix = mix / (np.abs(mix).max() + 1e-9) * 0.62
    pcm = (mix * 32767).astype('<i2')
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ------------------------------------------------------------------ cover still
def make_cover(sc, prepped, path):
    t = 34.0
    acc = scene_at(prepped, t)
    canvas = np.zeros((640, 960, 3), np.float32)
    bg = np.array(art.CREAM, np.float32) / 255
    canvas[:] = bg
    yy, xx = np.mgrid[0:640, 0:960]
    for r, col in ((305, (238, 226, 200)),):
        mask = ((xx - 480) ** 2 + (yy - 320) ** 2) <= r * r
        canvas[mask] = np.array(col, np.float32) / 255
    ring = np.abs(np.sqrt((xx - 480) ** 2 + (yy - 320) ** 2) - 288) < 1.3
    canvas[ring] = np.array(art.GOLD, np.float32) / 255
    x0 = (960 - art.W) // 2
    over(canvas, acc, x0, 0)
    Image.fromarray((canvas * 255).clip(0, 255).astype(np.uint8)).save(path, quality=90)


# ------------------------------------------------------------------ main
def render(slug, webm=True, still_only=False):
    sc = art.BUILDERS[slug]()
    num = list(art.BUILDERS).index(slug) + 1
    prepped = prep_layers(sc)
    os.makedirs(OUT_V, exist_ok=True)
    os.makedirs(OUT_I, exist_ok=True)
    make_cover(sc, prepped, os.path.join(OUT_I, f'{slug}.jpg'))
    if still_only:
        return
    bg = make_bg()
    header, caps, outro = panel_layers(sc, num)
    wav = os.path.join(OUT_V, f'_{slug}.wav')
    make_music(slug, wav)
    mp4 = os.path.join(OUT_V, f'{slug}.mp4')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{FW}x{FH}', '-r', str(FPS), '-i', '-',
           '-i', wav, '-c:v', 'libx264', '-preset', 'medium', '-crf', '25', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
           '-movflags', '+faststart', '-c:a', 'aac', '-b:a', '112k', '-shortest', mp4]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        f = frame_at(bg, prepped, header, caps, outro, i / FPS)
        rgb = (f * 255).clip(0, 255).astype(np.uint8)
        p.stdin.write(rgb[..., ::-1].tobytes())
    p.stdin.close()
    p.wait()
    if webm:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp4, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '38',
                        '-deadline', 'good', '-cpu-used', '5', '-row-mt', '1', '-c:a', 'libopus', '-b:a', '64k',
                        os.path.join(OUT_V, f'{slug}.webm')], check=True)
    os.remove(wav)
    print('done', slug, os.path.getsize(mp4) // 1024, 'KB mp4', flush=True)


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    flags = [a for a in sys.argv[1:] if a.startswith('--')]
    for s in (args or list(art.BUILDERS)):
        render(s, webm='--no-webm' not in flags, still_only='--still-only' in flags)
