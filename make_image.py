"""Render entry.png: the world's news of Wednesday 25 November 2026 in one image.

Run once at build time (needs Pillow and the fonts named below); main.py only copies
the committed PNG, so the entry itself is deterministic and needs no network.
"""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
FONTS = "C:/Windows/Fonts/"
rng = random.Random(20261125)


def font(name, size):
    return ImageFont.truetype(FONTS + name, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


img = Image.new("RGB", (W, H), (12, 10, 14))

# ---------- hero: night sky glowing orange over a burning refinery ----------
HERO_TOP, HERO_BOT = 70, 640
sky = Image.new("RGB", (W, HERO_BOT - HERO_TOP))
sd = ImageDraw.Draw(sky)
for y in range(sky.height):
    t = y / sky.height
    sd.line([(0, y), (W, y)], fill=lerp((14, 12, 24), (150, 52, 14), t ** 1.6))
img.paste(sky, (0, HERO_TOP))

# smoke plumes (blurred dark blobs rising and drifting right)
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
smd = ImageDraw.Draw(smoke)
for cx0 in (300, 560, 820):
    for k in range(26):
        t = k / 26
        cx = cx0 + t * 260 + rng.uniform(-30, 30)
        cy = 470 - t * 420 + rng.uniform(-15, 15)
        r = 40 + t * 120
        a = int(200 * (1 - t) + 30)
        g = rng.randint(18, 40)
        smd.ellipse([cx - r, cy - r * 0.7, cx + r, cy + r * 0.7], fill=(g, g - 4, g - 6, a))
smoke = smoke.filter(ImageFilter.GaussianBlur(18))
img.paste(smoke, (0, 0), smoke)

# fire glow
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for cx, cy, r in ((300, 520, 230), (560, 500, 280), (820, 520, 220)):
    gd.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=(255, 120, 20, 110))
glow = glow.filter(ImageFilter.GaussianBlur(60))
img.paste(glow, (0, 0), glow)

d = ImageDraw.Draw(img)

# flames: layered jagged tongues
def flame(cx, base, width, height, seed):
    r = random.Random(seed)
    for color, scale in (((200, 40, 10), 1.0), ((255, 110, 20), 0.75), ((255, 200, 60), 0.5), ((255, 245, 190), 0.25)):
        pts = [(cx - width * scale / 2, base)]
        n = 9
        for i in range(1, n):
            x = cx - width * scale / 2 + width * scale * i / n
            peak = height * scale * (1 - abs(i - n / 2) / (n / 2)) ** 0.6
            y = base - peak * r.uniform(0.55, 1.0) - (r.uniform(0, 25) if i % 2 else 0)
            pts.append((x, y))
            pts.append((x + width * scale / (2 * n), base - peak * r.uniform(0.25, 0.5)))
        pts.append((cx + width * scale / 2, base))
        d.polygon(pts, fill=color)

flame(300, 560, 220, 250, 1)
flame(560, 545, 300, 330, 2)
flame(820, 560, 200, 220, 3)

# refinery silhouette: tanks, towers, pipes, stacks
SIL = (8, 6, 8)
GROUND = 560
d.rectangle([0, GROUND, W, 600], fill=SIL)
for x, w, h in ((40, 110, 70), (170, 90, 55), (420, 120, 75), (690, 100, 60), (930, 120, 70)):
    d.rectangle([x, GROUND - h, x + w, GROUND], fill=SIL)
    d.ellipse([x, GROUND - h - 14, x + w, GROUND - h + 14], fill=SIL)
for x, h, w in ((140, 210, 18), (360, 280, 22), (390, 180, 14), (640, 240, 20), (760, 300, 16), (880, 190, 18)):
    d.rectangle([x, GROUND - h, x + w, GROUND], fill=SIL)
    for yy in range(GROUND - h + 20, GROUND, 34):  # ladders / platforms
        d.rectangle([x - 8, yy, x + w + 8, yy + 4], fill=SIL)
d.rectangle([0, GROUND - 26, W, GROUND - 20], fill=SIL)  # pipe rack
for x in range(0, W, 46):
    d.rectangle([x, GROUND - 26, x + 4, GROUND], fill=SIL)

# sea with a burning tanker
SEA_TOP = 600
for y in range(SEA_TOP, HERO_BOT):
    t = (y - SEA_TOP) / (HERO_BOT - SEA_TOP)
    d.line([(0, y), (W, y)], fill=lerp((70, 30, 14), (16, 14, 22), t))
for k in range(40):  # fire reflections
    x = rng.randint(150, 950)
    y = rng.randint(SEA_TOP + 3, HERO_BOT - 4)
    d.line([(x, y), (x + rng.randint(15, 60), y)], fill=(230, 120, 40), width=2)
# tanker hull + bridge
hull = [(600, 612), (980, 612), (960, 634), (620, 634)]
d.polygon(hull, fill=(6, 5, 7))
d.rectangle([920, 588, 958, 612], fill=(6, 5, 7))
d.rectangle([934, 574, 944, 588], fill=(6, 5, 7))
flame(700, 612, 90, 90, 4)
flame(790, 612, 70, 70, 5)

# drones in the sky
for x, y, s in ((150, 160, 1.0), (230, 120, 0.8), (930, 210, 0.9)):
    d.polygon([(x, y), (x - 26 * s, y + 6 * s), (x - 6 * s, y + 2 * s), (x - 12 * s, y + 14 * s), (x + 4 * s, y + 4 * s)], fill=(10, 8, 12))
    d.line([(x - 28 * s, y + 7 * s), (x + 30 * s, y - 14 * s)], fill=(255, 190, 120), width=1)

# ---------- masthead ----------
d.rectangle([0, 0, W, HERO_TOP], fill=(242, 236, 222))
d.text((32, 16), "THE WORLD IN ONE PICTURE", font=font("georgiab.ttf", 34), fill=(20, 18, 18))
dt = "WEDNESDAY · 25 NOVEMBER 2026"
f = font("arialbd.ttf", 20)
d.text((W - 32 - d.textlength(dt, font=f), 26), dt, font=f, fill=(150, 30, 20))
d.line([(0, HERO_TOP - 1), (W, HERO_TOP - 1)], fill=(20, 18, 18), width=3)

# headline over hero
head = "THE WORLD'S OIL IS ON FIRE"
hf = font("impact.ttf", 74)
hx = (W - d.textlength(head, font=hf)) / 2
d.text((hx + 3, 100 + 3), head, font=hf, fill=(0, 0, 0))
d.text((hx, 100), head, font=hf, fill=(255, 244, 228))

# place tags pinned in the hero
def tag(x, y, text):
    tf = font("arialbd.ttf", 19)
    tw = d.textlength(text, font=tf)
    d.rectangle([x, y, x + tw + 20, y + 30], fill=(190, 28, 22))
    d.text((x + 10, y + 4), text, font=tf, fill=(255, 255, 255))

tag(170, 205, "RAS TANURA, SAUDI ARABIA: HOUTHI ATTACK")
tag(560, 262, "STRAIT OF HORMUZ: TANKERS HIT MINES")
tag(90, 305, "RUSSIA: 14 REFINERIES STRUCK IN NOVEMBER")

# ---------- briefs band ----------
d.rectangle([0, HERO_BOT, W, H], fill=(242, 236, 222))
d.rectangle([0, HERO_BOT, W, HERO_BOT + 6], fill=(190, 28, 22))

briefs = [
    ("SAUDI ARABIA", "Houthis say they struck the Ras Tanura refinery, days after hitting Riyadh's financial district."),
    ("HORMUZ", "Iran's Guard says two oil tankers hit naval mines and caught fire on an unauthorised route."),
    ("RUSSIA / UKRAINE", "Putin calls a response to Ukraine's refinery strikes inevitable; Trump had asked Kyiv to stop."),
    ("LIBYA", "Haftar's army vows to retaliate after a Ukrainian drone hits a Russian warship, killing two officers."),
    ("GAZA", "An Israeli strike kills a Hamas security chief along with his wife and two children."),
    ("HUNGER", "The World Food Programme warns the wars put food aid for millions at risk."),
]

tf = font("arialbd.ttf", 17)
bf = font("georgia.ttf", 20)


def wrap(text, fnt, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


cols, colw, pad = 3, W // 3, 22
for i, (title, body) in enumerate(briefs):
    cx = (i % cols) * colw + pad
    cy = HERO_BOT + 26 + (i // cols) * 182
    d.text((cx, cy), title, font=tf, fill=(190, 28, 22))
    for j, line in enumerate(wrap(body, bf, colw - 2 * pad)):
        d.text((cx, cy + 30 + j * 27), line, font=bf, fill=(28, 24, 24))
    if i % cols:
        d.line([(cx - pad, cy), (cx - pad, cy + 150)], fill=(190, 180, 165), width=1)
d.line([(pad, HERO_BOT + 198), (W - pad, HERO_BOT + 198)], fill=(190, 180, 165), width=1)

img.save("entry.png", optimize=True)
print("wrote entry.png")
