"""Gera os GIFs em pixel art do perfil do GitHub.

Tudo é desenhado pixel a pixel em baixa resolução, com paleta fixa
(indexada) e fonte bitmap própria, e depois ampliado sem suavização.
Uso: python gerar_assets.py   (requer Pillow)
"""
import math
import os
import random

from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SCALE = 4

# ---------------------------------------------------------------- paleta
PAL_HEX = [
    "150F26",  # 0  transparente
    "150F26",  # 1  fundo
    "1E1538",  # 2  fundo 2
    "2A1D4F",  # 3  fundo 3
    "4C3A8A",  # 4  apagado
    "7C5CD6",  # 5  médio
    "A78BFA",  # 6  lilás
    "C4B5FD",  # 7  lilás claro
    "EDE7FF",  # 8  texto
    "FFFFFF",  # 9  branco
    "F472B6",  # 10 rosa (alerta)
    "9D2E6B",  # 11 rosa escuro
    "7EE7C7",  # 12 menta (ok)
    "0D0919",  # 13 silhueta
    "FFC97A",  # 14 luz quente
    "1B1336",  # 15 rio
    "241A47",  # 16 prédios distantes
]
(T, BG, BG2, BG3, DIM, MID, LIL, LIGHT, TXT, WHITE,
 PINK, PINKD, MINT, DEEP, WARM, RIVER, SIL) = range(17)
PAL = []
for h in PAL_HEX:
    PAL += [int(h[i:i + 2], 16) for i in (0, 2, 4)]
PAL += [0] * (768 - len(PAL))

BAYER = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def canvas(w, h, fill=T):
    im = Image.new("P", (w, h), fill)
    im.putpalette(PAL)
    return im


def px(im, x, y, c):
    if 0 <= x < im.width and 0 <= y < im.height:
        im.putpixel((int(x), int(y)), c)


def gradient(im, y0, y1, cols):
    """Degradê vertical com dithering ordenado (Bayer 4x4)."""
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1) * (len(cols) - 1)
        i = min(int(t), len(cols) - 2)
        f = t - i
        for x in range(im.width):
            c = cols[i + 1] if f * 16 > BAYER[y % 4][x % 4] else cols[i]
            im.putpixel((x, y), c)


def frame(im, col=DIM):
    """Moldura de 1 px com cantos chanfrados (transparentes)."""
    w, h = im.size
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=col)
    for cx, cy, sx, sy in ((0, 0, 1, 1), (w - 1, 0, -1, 1),
                           (0, h - 1, 1, -1), (w - 1, h - 1, -1, -1)):
        px(im, cx, cy, T)
        px(im, cx + sx, cy, T)
        px(im, cx, cy + sy, T)
        px(im, cx + sx, cy + sy, col)


def save(frames, name, ms):
    big = [f.resize((f.width * SCALE, f.height * SCALE), Image.NEAREST)
           for f in frames]
    path = os.path.join(OUT, name)
    big[0].save(path, save_all=True, append_images=big[1:], duration=ms,
                loop=0, transparency=0, disposal=2, optimize=False)
    print(f"{name}: {len(frames)} quadros, {os.path.getsize(path) // 1024} KB")


# ------------------------------------------------------------ fonte 5x7
G = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#",
    "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".###.|#...#|#....|#....|#....|#...#|.###.",
    "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####",
    "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".###.|#...#|#....|#.###|#...#|#...#|.####",
    "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": ".###.|..#..|..#..|..#..|..#..|..#..|.###.",
    "J": "..###|...#.|...#.|...#.|...#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#",
    "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#",
    "N": "#...#|#...#|##..#|#.#.#|#..##|#...#|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.",
    "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#",
    "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.",
    "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.",
    "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|#.#.#|.#.#.",
    "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..",
    "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.",
    "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####",
    "3": "####.|....#|....#|.###.|....#|....#|####.",
    "4": "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.",
    "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": ".###.|#....|#....|####.|#...#|#...#|.###.",
    "7": "#####|....#|...#.|..#..|.#...|.#...|.#...",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.",
    "9": ".###.|#...#|#...#|.####|....#|....#|.###.",
    " ": ".....|.....|.....|.....|.....|.....|.....",
    ",": ".....|.....|.....|.....|.....|..#..|.#...",
    ".": ".....|.....|.....|.....|.....|.....|..#..",
    "·": ".....|.....|.....|..#..|.....|.....|.....",
    ">": "#....|.#...|..#..|...#.|..#..|.#...|#....",
    ":": ".....|..#..|.....|.....|.....|..#..|.....",
    "!": "..#..|..#..|..#..|..#..|..#..|.....|..#..",
    "-": ".....|.....|.....|.###.|.....|.....|.....",
    "_": ".....|.....|.....|.....|.....|.....|#####",
}
MARKS = {
    "acute": (-3, ["...#.", "..#.."]),
    "tilde": (-3, [".##.#", "#.##."]),
    "circ": (-3, ["..#..", ".#.#."]),
    "ced": (7, ["..#..", ".##.."]),
}
ACC = {"Á": ("A", "acute"), "É": ("E", "acute"), "Í": ("I", "acute"),
       "Ó": ("O", "acute"), "Ú": ("U", "acute"), "Ã": ("A", "tilde"),
       "Õ": ("O", "tilde"), "Ê": ("E", "circ"), "Ô": ("O", "circ"),
       "Ç": ("C", "ced")}


def glyph(ch):
    pts = []
    base, mark = ACC.get(ch, (ch, None))
    for y, row in enumerate(G[base].split("|")):
        pts += [(x, y) for x, c in enumerate(row) if c == "#"]
    if mark:
        y0, rows = MARKS[mark]
        for dy, row in enumerate(rows):
            pts += [(x, y0 + dy) for x, c in enumerate(row) if c == "#"]
    return pts


def text_w(s, scale=1):
    return (len(s) * 6 - 1) * scale


def text(im, x, y, s, col, scale=1, shadow=None, cols=None):
    d = ImageDraw.Draw(im)
    for layer in ((shadow, 1), (None, 0)) if shadow is not None else ((None, 0),):
        off = layer[1]
        for i, ch in enumerate(s):
            c = layer[0] if off else (cols[i] if cols else col)
            if c is None:
                continue
            gx = x + i * 6 * scale
            for px_, py_ in glyph(ch):
                X, Y = gx + px_ * scale + off, y + py_ * scale + off
                d.rectangle([X, Y, X + scale - 1, Y + scale - 1], fill=c)


# --------------------------------------------------------- elementos
def stars_layer(im, stars, f, n):
    for x, y, ph, big in stars:
        v = (math.sin(2 * math.pi * (f / n * 2 + ph)) + 1) / 2
        c = WHITE if v > 0.85 else LIGHT if v > 0.6 else LIL if v > 0.35 else DIM
        px(im, x, y, c)
        if big and v > 0.8:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                px(im, x + dx, y + dy, LIL)


def canoe(im, x, y, f):
    d = ImageDraw.Draw(im)
    d.line([x, y, x + 9, y], fill=DEEP)
    d.line([x + 1, y + 1, x + 8, y + 1], fill=DEEP)
    px(im, x - 1, y - 1, DEEP)
    px(im, x + 10, y - 1, DEEP)
    px(im, x + 5, y - 3, DEEP)          # cabeça
    d.line([x + 5, y - 2, x + 5, y - 1], fill=DEEP)
    if (f // 4) % 2:                     # remo
        d.line([x + 7, y - 3, x + 3, y + 2], fill=DEEP)
    else:
        d.line([x + 6, y - 3, x + 8, y + 2], fill=DEEP)
    for i in range(0, 10, 2):            # reflexo
        px(im, x + i + (y % 2), y + 3, BG3)


def palm(im, bx, by, h, lean, f, n, ph):
    sway = round(math.sin(2 * math.pi * f / n + ph))
    top = (bx, by)
    for i in range(h):
        t = i / h
        x = bx + round(lean * t * t + (sway if t > 0.8 else 0))
        px(im, x, by - i, DEEP)
        if i % 3 == 0:
            px(im, x + 1, by - i, SIL)
        top = (x, by - i)
    tx, ty = top
    fronds = [(-7, 2), (-5, 4), (-3, 5), (3, 5), (5, 4), (7, 2), (-1, -3), (2, -3)]
    for k, (dx, dy) in enumerate(fronds):
        s = sway if k % 2 else 0
        for j in range(1, 9):
            u = j / 8
            fx = tx + round(dx * u) + (s if u > 0.6 else 0)
            fy = ty + round(-2 * u + (dy + 2) * u * u) if dy > 0 else ty + round(dy * u)
            px(im, fx, fy, DEEP)
            if j > 3 and dy > 0:
                px(im, fx, fy + 1, DEEP)
    px(im, tx, ty, SIL)
    px(im, tx + 1, ty + 1, PINKD)        # cacho de açaí
    px(im, tx - 1, ty + 1, PINKD)


# ------------------------------------------------------------ header
def header():
    W, H, N = 200, 72, 100
    rnd = random.Random(7)
    WY = 60
    stars = []
    while len(stars) < 46:
        x, y = rnd.randint(2, W - 3), rnd.randint(2, 46)
        if not (174 <= x <= 191 and 6 <= y <= 23) and \
                not (16 <= x <= 166 and 4 <= y <= 28) and \
                not (16 <= x <= 142 and 29 <= y <= 53):
            stars.append((x, y, rnd.random(), rnd.random() < 0.15))
    far = []
    x = 1
    while x < W - 1:
        w = rnd.randint(4, 9)
        hmax = 16 if x > 140 else 8
        far.append((x, w, rnd.randint(3, hmax)))
        x += w + rnd.choice((0, 0, 1))
    tallest = max(far, key=lambda b: b[2])
    windows = []
    for bx, bw, bh in far:
        for wy in range(WY - bh + 2, WY - 1, 2):
            for wx in range(bx + 1, bx + bw - 1, 2):
                if rnd.random() < 0.22:
                    windows.append((wx, wy, rnd.randint(0, N - 1), rnd.choice((20, 25, 50))))
    title = "> OLÁ, MUNDO"
    l1, l2 = "ESTUDANTE · IOT · IA", "BELÉM · PA"
    TX, TY, Y1, Y2 = 20, 12, 33, 45
    frames = []
    for f in range(N):
        im = canvas(W, H)
        d = ImageDraw.Draw(im)
        gradient(im, 0, WY, [BG, BG, BG2, BG3])
        stars_layer(im, stars, f, N)
        # estrela cadente
        if 58 <= f < 66:
            k = f - 58
            for t, c in enumerate((WHITE, LIGHT, LIL, DIM, DIM)):
                px(im, 150 - k * 12 + t * 3, 2 + k + t // 2 * -1 + (t > 0), c)
        # lua com halo pontilhado
        mx, my, r = 182, 14, 7
        for yy in range(my - r - 4, my + r + 5):
            for xx in range(mx - r - 4, mx + r + 5):
                dd = math.hypot(xx - mx, yy - my)
                if dd <= r:
                    px(im, xx, yy, LIGHT)
                elif dd <= r + 3 and (xx + yy) % 2 == 0:
                    px(im, xx, yy, BG3 if dd > r + 1.5 else DIM)
        for cx, cy in ((180, 11), (181, 12), (185, 17), (186, 17), (179, 18), (184, 10)):
            px(im, cx, cy, LIL)
        for yy in range(my - r, my + r + 1):  # sombra lateral
            xx = mx + r - 1 + (abs(yy - my) > 4) * -1 - (abs(yy - my) > 6)
            px(im, xx, yy, LIL)
        # skyline distante
        for bx, bw, bh in far:
            d.rectangle([bx, WY - bh, bx + bw - 1, WY - 1], fill=SIL)
        ax = tallest[0] + tallest[1] // 2
        d.line([ax, WY - tallest[2] - 4, ax, WY - tallest[2] - 1], fill=SIL)
        if (f // 10) % 2:
            px(im, ax, WY - tallest[2] - 5, PINK)
        for wx, wy, ph, per in windows:
            if (f + ph) % per < per * 0.8:
                px(im, wx, wy, WARM if (wx + wy) % 3 else LIL)
        # Ver-o-Peso
        vx0, vx1 = 94, 132
        d.rectangle([vx0, WY - 6, vx1, WY - 1], fill=BG3)
        d.line([vx0, WY - 6, vx1, WY - 6], fill=DIM)
        for tx in (vx0 + 1, vx0 + 12, vx1 - 14, vx1 - 3):
            d.rectangle([tx, WY - 9, tx + 2, WY - 6], fill=BG3)
            px(im, tx + 1, WY - 10, DIM)
            px(im, tx + 1, WY - 11, DIM)
            px(im, tx, WY - 9, DIM)
            px(im, tx + 2, WY - 9, DIM)
        for k, wx in enumerate(range(vx0 + 2, vx1 - 1, 3)):
            if (f // 6 + k) % 7:
                px(im, wx, WY - 3, WARM)
                px(im, wx, WY - 4, WARM if k % 2 else LIL)
        # rio
        d.rectangle([0, WY, W - 1, H - 1], fill=RIVER)
        d.line([0, WY, W - 1, WY], fill=BG3)
        for row in range(WY + 2, H - 1, 2):
            for k in range(0, W, 13 + row % 5):
                xo = k + (row * 7) % 11 + round(math.sin(2 * math.pi * f / N * 2 + k + row) * 1.5)
                ln = 2 + (k + row) % 3
                d.line([xo, row, xo + ln, row], fill=BG3 if row < 66 else DIM)
        for i, row in enumerate(range(WY + 1, H - 1)):
            half = max(1, 5 - i // 2)
            j = round(math.sin(2 * math.pi * f / N * 4 + i * 1.3) * 1.5)
            if (i + f // 3) % 3 != 2:
                d.line([mx - half + j, row, mx + half + j, row],
                       fill=LIGHT if i < 4 else LIL if i < 8 else MID)
        canoe(im, -14 + round((W + 28) * f / N), WY + 3, f)
        palm(im, 6, H - 2, 31, 2, f, N, 0)
        palm(im, 194, H - 2, 23, -2, f, N, 1.7)
        # vagalumes
        for k in range(6):
            a = 2 * math.pi * (f / N + k / 6)
            fx = 14 + k * 30 + round(math.sin(a * 2) * 4)
            fy = 50 + round(math.cos(a) * 3)
            if (f + k * 7) % 20 < 12 and not (60 <= fx <= 140):
                px(im, fx, fy, MINT if k % 2 else WARM)
        # texto digitando
        n0 = min(len(title), f // 2)
        n1 = min(len(l1), max(0, f - 28))
        n2 = min(len(l2), max(0, f - 52))
        text(im, TX, TY, title[:n0], TXT, 2, shadow=DEEP,
             cols=[LIL] + [TXT] * (len(title) - 1))
        text(im, TX, Y1, l1[:n1], LIGHT, 1, shadow=DEEP,
             cols=[PINK if c == "·" else LIGHT for c in l1])
        text(im, TX, Y2, l2[:n2], LIL, 1, shadow=DEEP,
             cols=[PINK if c == "·" else LIL for c in l2])
        if n1 == 0 and f < 28:
            cx, cy, cs = TX + n0 * 12, TY, 2
        elif n2 == 0 and f < 52:
            cx, cy, cs = TX + n1 * 6, Y1, 1
        else:
            cx, cy, cs = TX + n2 * 6, Y2, 1
        if (f // 4) % 2 == 0:
            d.rectangle([cx, cy, cx + 5 * cs - 1, cy + 7 * cs - 1], fill=LIL)
        frame(im)
        frames.append(im)
    save(frames, "header.gif", 80)


# ------------------------------------------------------------- pulse
def signal(L=300, spike=168):
    rnd = random.Random(3)
    s = []
    for i in range(L):
        walk = 1 + 0.12 * math.sin(2 * math.pi * i / 25) + rnd.uniform(-0.07, 0.07)
        if 155 <= i < spike:
            v = 1 - (i - 155) / 13 * 0.8 + rnd.uniform(-0.03, 0.03)
        elif spike <= i < spike + 8:
            v = [3.7, 2.1, 3.1, 1.3, 2.0, 0.7, 1.4, 0.9][i - spike]
        elif spike + 8 <= i < 262:
            v = 1 + rnd.uniform(-0.02, 0.02)
        elif 262 <= i < 280:
            u = (i - 262) / 18
            v = 1 + u * (walk - 1)
        else:
            v = walk
        s.append(v)
    return s


def pulse():
    W, H, N, STEP = 200, 80, 100, 3
    L, SPIKE = 300, 168
    sig = signal(L, SPIKE)
    SX0, SY0, SX1, SY1 = 62, 4, 193, 58
    IX0, IY0 = SX0 + 2, SY0 + 2
    frames = []
    for f in range(N):
        im = canvas(W, H)
        d = ImageDraw.Draw(im)
        gradient(im, 0, H, [BG, BG, BG2])
        s0 = f * STEP
        newest = (s0 + 127) % L
        if SPIKE <= newest < SPIKE + 45:
            state = "queda"
        elif SPIKE + 45 <= newest < SPIKE + 105:
            state = "enviado"
        else:
            state = "ok"
        blink = (f // 2) % 2 == 0
        # --- ESP32
        bx, by = 8, 18
        text(im, 26, 6, "ESP32", LIL, shadow=DEEP)
        for k in range(14):
            d.rectangle([bx + 2 + k * 3, by - 2, bx + 2 + k * 3, by - 1], fill=MID)
            d.rectangle([bx + 2 + k * 3, by + 20, bx + 2 + k * 3, by + 21], fill=MID)
        d.rectangle([bx, by, bx + 43, by + 19], fill=BG3, outline=DIM)
        d.rectangle([bx + 11, by + 3, bx + 32, by + 16], fill=MID, outline=LIL)
        d.line([bx + 12, by + 4, bx + 31, by + 4], fill=LIGHT)
        for k in range(3):
            d.line([bx + 14, by + 8 + k * 3, bx + 29, by + 8 + k * 3], fill=LIL)
        for k in range(4):                                   # antena
            x = bx + 2 + k * 2
            d.line([x, by + 3, x, by + 15], fill=LIL)
            px(im, x + 1, by + 3 if k % 2 else by + 15, LIL)
        d.rectangle([bx + 41, by + 7, bx + 44, by + 12], fill=LIGHT)  # usb
        led = PINK if state == "queda" and blink else MINT if (f // 6) % 2 else BG2
        px(im, bx + 37, by + 4, led)
        px(im, bx + 38, by + 4, led)
        if state == "enviado":                               # ondas wi-fi
            for k, rr in enumerate((3, 6, 9)):
                if (f // 3) % 4 > k:
                    for a in range(200, 341, 12):
                        t = math.radians(a)
                        px(im, bx + 5 + round(math.cos(t) * rr),
                           by - 1 + round(math.sin(t) * rr), MINT)
        # --- MPU6050
        shake = (f % 2 * 2 - 1) if state == "queda" and newest < SPIKE + 12 else 0
        mx, my = 15 + shake, 50
        for k, c in enumerate((WARM, MINT, LIL, PINK)):
            x = bx + 8 + k * 4
            d.line([x, by + 22, x, my - 3], fill=c)
            d.line([x, my - 3, mx + 3 + k * 4, my - 1], fill=c)
        d.rectangle([mx, my, mx + 18, my + 12], fill=BG3, outline=DIM)
        d.rectangle([mx + 6, my + 3, mx + 12, my + 9], fill=DEEP)
        for k in range(4):
            px(im, mx + 5, my + 4 + k * 1.5, MID)
            px(im, mx + 13, my + 4 + k * 1.5, MID)
        px(im, mx + 7, my + 4, LIL)
        text(im, 6, 68, "MPU6050", LIL, shadow=DEEP)
        # --- osciloscópio
        border = PINK if state == "queda" and blink else DIM
        d.rectangle([SX0, SY0, SX1, SY1], fill=DEEP, outline=border)
        for gy in range(IY0, SY1 - 1, 6):
            for gx in range(IX0, SX1 - 1, 8):
                px(im, gx, gy, BG3)
        sy = IY0 + (f * 2) % (SY1 - IY0 - 1)                 # varredura
        d.line([IX0, sy, SX1 - 2, sy], fill=BG)
        ymap = lambda v: round(SY1 - 4 - v * 11)
        ty = ymap(2.5)
        for gx in range(IX0, SX1 - 1, 4):
            d.line([gx, ty, gx + 1, ty], fill=PINKD)
        text(im, IX0 + 2, ty + 3, "LIMIAR", PINKD)
        text(im, SX1 - 2 - text_w("SIMULAÇÃO"), IY0 + 4, "SIMULAÇÃO", DIM)
        prev = None
        for i in range(128):
            y = max(IY0, min(SY1 - 2, ymap(sig[(s0 + i) % L])))
            x = IX0 + i
            c = MID if i < 28 else LIL if i < 110 else LIGHT
            if prev is None:
                px(im, x, y, c)
            else:
                d.line([x, prev, x, y], fill=c)
            prev = y
        hx = IX0 + 127
        for dx, dy in ((-1, 0), (0, -1), (0, 1)):
            px(im, hx + dx, prev + dy, LIL)
        px(im, hx, prev, WHITE)
        # --- status
        d.rectangle([SX0, 62, SX1, 75], fill=BG2, outline=DIM)
        if state == "queda":
            c = PINK if blink else PINKD
            d.rectangle([SX0 + 4, 66, SX0 + 8, 70], fill=c)
            text(im, SX0 + 13, 65, "QUEDA DETECTADA!", c)
        elif state == "enviado":
            for p in ((0, 2), (1, 3), (2, 4), (3, 3), (4, 2), (5, 1), (6, 0)):
                px(im, SX0 + 4 + p[0], 66 + p[1], MINT)
                px(im, SX0 + 4 + p[0], 67 + p[1], MINT)
            text(im, SX0 + 15, 65, "ALERTA ENVIADO", MINT)
        else:
            if (f // 5) % 2:
                d.rectangle([SX0 + 5, 67, SX0 + 7, 69], fill=MINT)
            text(im, SX0 + 13, 65, "MONITORANDO", LIGHT)
        frame(im)
        frames.append(im)
    save(frames, "pulse.gif", 80)


# ----------------------------------------------------------- divider
def divider():
    W, H, N = 200, 5, 50
    frames = []
    for f in range(N):
        im = canvas(W, H)
        for x in range(2, W - 2, 4):
            px(im, x, 2, DIM)
        head = round(-10 + (W + 20) * f / N)
        for t, c in enumerate((WHITE, LIGHT, LIGHT, LIL, LIL, MID, MID, DIM)):
            x = head - t * 2
            px(im, x, 2, c)
            px(im, x - 1, 2, c if t else LIGHT)
        for dy in (-1, 1):
            px(im, head, 2 + dy, LIL)
        frames.append(im)
    save(frames, "divider.gif", 60)


# ------------------------------------------------------------- ícones
def card():
    im = canvas(32, 32)
    gradient(im, 1, 31, [BG, BG2])
    frame(im)
    return im


def icon_queda():
    N, frames = 24, []
    for f in range(N):
        im = card()
        d = ImageDraw.Draw(im)
        d.rectangle([7, 17, 24, 27], fill=BG3, outline=DIM)
        d.rectangle([13, 19, 22, 25], fill=MID, outline=LIL)
        d.line([14, 20, 21, 20], fill=LIGHT)
        for k in range(3):
            d.line([9 + k * 1, 19, 9 + k * 1, 25], fill=LIL if k != 1 else BG3)
        for k in range(6):
            px(im, 9 + k * 3, 16, MID)
            px(im, 9 + k * 3, 28, MID)
        for k, rr in enumerate((4, 7, 10)):
            if (f // 3) % 4 > k:
                for a in range(215, 330, 14):
                    t = math.radians(a)
                    px(im, 10 + round(math.cos(t) * rr), 15 + round(math.sin(t) * rr), LIL)
        beat = f % 12 < 2
        hx, hy = 21, 5
        heart = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
        if beat:
            heart = ["##.##..", "#####..", ".###...", "..#...."]
            hx, hy = 22, 6
        for y, row in enumerate(heart):
            for x, c in enumerate(row):
                if c == "#":
                    px(im, hx + x, hy + y, PINK)
        if not beat:
            px(im, hx + 1, hy + 1, WHITE)
        frames.append(im)
    save(frames, "icon_queda.gif", 90)


def icon_roda():
    N, frames = 32, []
    for f in range(N):
        im = card()
        d = ImageDraw.Draw(im)
        sel = (f // 4) % 8
        for k in range(8):
            a = math.radians(k * 45 - 90)
            cx, cy = 16 + round(math.cos(a) * 10), 16 + round(math.sin(a) * 10)
            if k == sel:
                d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=LIL)
                d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=WHITE if f % 4 < 2 else LIGHT)
            else:
                d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=DIM)
                px(im, cx, cy, MID)
        d.ellipse([12, 12, 20, 20], fill=BG3, outline=DIM)
        a = math.radians(sel * 45 - 90)
        kx, ky = 16 + round(math.cos(a) * 2), 16 + round(math.sin(a) * 2)
        d.line([16, 16, kx, ky], fill=MID)
        d.rectangle([kx - 1, ky - 1, kx + 1, ky + 1], fill=PINK)
        px(im, kx - 1, ky - 1, WHITE)
        frames.append(im)
    save(frames, "icon_roda.gif", 90)


def icon_inventario():
    N, frames = 36, []
    boxes = [(6, 9, 6, 5, MID), (13, 7, 7, 7, LIL), (21, 10, 5, 4, MID),
             (6, 21, 8, 5, LIL), (15, 22, 5, 4, MID), (21, 20, 6, 6, LIL)]
    for f in range(N):
        im = card()
        d = ImageDraw.Draw(im)
        scan = 4 + round((1 - math.cos(2 * math.pi * f / N)) / 2 * 23)
        for y in (14, 26):
            d.line([4, y, 27, y], fill=DIM)
            d.line([4, y + 1, 27, y + 1], fill=BG3)
        for bx, by, bw, bh, c in boxes:
            hit = by <= scan <= by + bh
            d.rectangle([bx, by, bx + bw - 1, by + bh - 1], fill=MINT if hit else c)
            d.line([bx + bw // 2, by, bx + bw // 2, by + bh - 1], fill=LIGHT if not hit else WHITE)
            d.line([bx, by, bx + bw - 1, by], fill=LIGHT if c == LIL else LIL)
        d.line([3, scan, 28, scan], fill=PINK)
        px(im, 2, scan, WHITE)
        px(im, 29, scan, WHITE)
        frames.append(im)
    save(frames, "icon_inventario.gif", 70)


# ------------------------------------------------------------ rodapé
def footer():
    W, H, N, WY = 200, 30, 100, 20
    rnd = random.Random(11)
    stars = [(rnd.randint(2, W - 3), rnd.choice((2, 3, 15, 16, 17)), rnd.random(), False)
             for _ in range(22)]
    msg = "OBRIGADO PELA VISITA"
    frames = []
    for f in range(N):
        im = canvas(W, H)
        d = ImageDraw.Draw(im)
        gradient(im, 0, WY, [BG, BG2, BG3])
        stars_layer(im, stars, f, N)
        d.rectangle([0, WY, W - 1, H - 1], fill=RIVER)
        d.line([0, WY, W - 1, WY], fill=BG3)
        for row in range(WY + 2, H - 1, 2):
            for k in range(0, W, 11 + row % 4):
                xo = k + (row * 5) % 9 + round(math.sin(2 * math.pi * f / N * 3 + k * 0.7 + row) * 1.5)
                d.line([xo, row, xo + 2, row], fill=BG3 if row < 25 else DIM)
        canoe(im, W + 14 - round((W + 28) * f / N), WY + 3, f)
        x0 = (W - text_w(msg)) // 2
        wave = [round(math.sin(2 * math.pi * f / N * 2 - i * 0.45) * 1.2) for i in range(len(msg))]
        for i, ch in enumerate(msg):
            text(im, x0 + i * 6, 6 + wave[i], ch, LIGHT if i % 2 else LIL, shadow=DEEP)
        frame(im)
        frames.append(im)
    save(frames, "footer.gif", 80)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    header()
    pulse()
    divider()
    icon_queda()
    icon_roda()
    icon_inventario()
    footer()
