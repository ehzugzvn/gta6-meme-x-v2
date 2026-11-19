#!/usr/bin/env python3
"""Download Day — GTA 6 meme v2 for make.fun gta6-meme-x-01.

Composes meme.png (1080x1080) entirely with PIL:
a Leonida living room at night, a huge TV showing a GTA VI download
stuck at 99% / 3 days, and the make.fun ghost sitting on the couch
staring at the bar, its magenta star coin beside it.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "meme.png")

MAGENTA = (236, 0, 140)
CYAN = (0, 229, 255)
YELLOW = (255, 210, 63)
BLACK = (8, 8, 12)
WHITE = (255, 255, 255)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansDisplay-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
]


def font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def sparkle_points(cx, cy, r):
    """Four-pointed sparkle: tall diamond with concave sides."""
    inner = r * 0.22
    pts = [
        (cx, cy - r),
        (cx + inner, cy - inner),
        (cx + r * 0.62, cy),
        (cx + inner, cy + inner),
        (cx, cy + r),
        (cx - inner, cy + inner),
        (cx - r * 0.62, cy),
        (cx - inner, cy - inner),
    ]
    return pts


def star_points(cx, cy, r_outer, r_inner, n=5, rot=-90):
    pts = []
    for i in range(n * 2):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_coin(d, cx, cy, r):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=MAGENTA, outline=BLACK, width=7)
    d.ellipse([cx - r + 13, cy - r + 13, cx + r - 13, cy + r - 13], outline=WHITE, width=4)
    d.polygon(star_points(cx, cy, r * 0.52, r * 0.22), fill=WHITE)


def draw_ghost(d, cx, top, w, h):
    """make.fun ghost per spec: white, thick black outline, sparkle eyes,
    wavy 3-bump bottom, a round little hand, magenta disc underneath."""
    left, right = cx - w // 2, cx + w // 2
    # magenta disc it sits on
    d.ellipse([left - 18, top + h - 26, right + 18, top + h + 22], fill=MAGENTA, outline=BLACK, width=6)
    # body outline as a sampled path
    pts = []
    dome_cy = top + w // 2
    for i in range(31):
        a = math.pi + (math.pi * i / 30)
        pts.append((cx + (w / 2) * math.cos(a), dome_cy + (w / 2) * math.sin(a)))
    bottom_line = top + h - 34
    pts.append((right, bottom_line))
    bumps = 3
    bump_w = w / bumps
    bump_r = bump_w / 2
    for b in range(bumps):
        bcx = right - bump_r - b * bump_w
        for i in range(1, 21):
            a = 0 + (math.pi * i / 20)  # downward semicircle
            pts.append((bcx - bump_r * math.cos(a), bottom_line + bump_r * 0.62 * math.sin(a)))
    pts.append((left, bottom_line))
    d.polygon(pts, fill=WHITE)
    d.line(pts + [pts[0]], fill=BLACK, width=9, joint="curve")
    # sparkle eyes, fixed upward on the progress bar
    eye_y = top + int(h * 0.34)
    for ex in (cx - int(w * 0.19), cx + int(w * 0.19)):
        d.polygon(sparkle_points(ex, eye_y, int(w * 0.13)), fill=BLACK)
    # stunned little open mouth
    mx, my, mr = cx, top + int(h * 0.56), 17
    d.ellipse([mx - mr, my - mr - 4, mx + mr, my + mr + 4], fill=BLACK)
    d.ellipse([mx - mr + 6, my - mr + 4, mx + mr - 6, my + mr - 2], fill=(255, 120, 170))
    # round little hand on the left side
    hx, hy, hr = left + 6, top + int(h * 0.62), 30
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=WHITE, outline=BLACK, width=7)


def text_center(d, cx, y, s, fnt, fill=WHITE, stroke=0, stroke_fill=BLACK, anchor_top=True):
    box = d.textbbox((0, 0), s, font=fnt, stroke_width=stroke)
    tw = box[2] - box[0]
    x = cx - tw // 2 - box[0]
    d.text((x, y), s, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
    return box[3] - box[1]


def rounded(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def label(d, xy, s, size, fill):
    """Small plain label used for props (router, snacks, chips)."""
    d.text(xy, s, font=font(size), fill=fill)


def main():
    img = Image.new("RGB", (W, H), (18, 20, 48))
    d = ImageDraw.Draw(img, "RGBA")

    # ---- room wall: vertical night gradient bands ----
    for y in range(H):
        t = y / H
        col = (int(24 + 18 * t), int(22 + 10 * t), int(58 + 30 * t))
        d.line([(0, y), (W, y)], fill=col)
    # floor
    d.rectangle([0, 950, W, H], fill=(38, 24, 38))
    d.line([(0, 950), (W, 950)], fill=BLACK, width=4)

    # ---- window (left) with palm silhouette + moon ----
    rounded(d, [36, 196, 268, 452], 18, fill=(10, 26, 66), outline=BLACK, width=8)
    d.ellipse([178, 222, 232, 276], fill=(245, 240, 200))
    # palm silhouette: curved trunk + five drooping fronds
    d.line([(78, 452), (96, 356), (128, 282)], fill=BLACK, width=15)
    fronds = [
        [(128, 282), (88, 252), (48, 258)],
        [(128, 282), (96, 232), (58, 216)],
        [(128, 282), (140, 226), (128, 200)],
        [(128, 282), (176, 238), (220, 232)],
        [(128, 282), (184, 272), (228, 286)],
    ]
    for fr in fronds:
        d.line(fr, fill=BLACK, width=9, joint="curve")
    d.rectangle([36, 318, 268, 330], fill=BLACK)
    d.rectangle([146, 196, 158, 452], fill=BLACK)
    text_center(d, 152, 462, "LEONIDA", font(26), fill=(140, 220, 255))

    # ---- standing fan (left of TV, drawn later over the wall) ----
    # pole/base are drawn after the TV so the TV bezel cannot hide the fan

    # ---- TV ----
    rounded(d, [292, 196, 1010, 586], 26, fill=(5, 5, 10), outline=BLACK, width=10)
    rounded(d, [312, 216, 990, 566], 16, fill=(11, 14, 38))
    # Vice City sunset backdrop for the WHOLE download screen (Gemini note):
    # pink -> orange -> deep purple gradient behind the UI itself, so the
    # screen alone screams GTA 6 / Leonida, not a generic download.
    sunset_top, sunset_mid, sunset_bot = (255, 62, 142), (255, 148, 64), (38, 16, 74)
    for i in range(346):
        y = 220 + i
        t = i / 346
        if t < 0.45:
            u = t / 0.45
            col = tuple(int(sunset_top[c] + (sunset_mid[c] - sunset_top[c]) * u) for c in range(3))
        else:
            u = (t - 0.45) / 0.55
            col = tuple(int(sunset_mid[c] + (sunset_bot[c] - sunset_mid[c]) * u) for c in range(3))
        d.line([(316, y), (986, y)], fill=col)
    # low sun disc behind the title
    d.ellipse([561, 232, 741, 412], fill=(255, 224, 138))
    for sy in (322, 344, 366):  # retro sun slits
        d.rectangle([561, sy, 741, sy + 7], fill=sunset_mid)
    # palm silhouettes framing the screen (dark against the sunset)
    for trunk, flip in ([(338, 566), (366, 420), (398, 330)], 1), ([(964, 566), (936, 420), (904, 330)], -1):
        d.line(trunk, fill=(24, 8, 34), width=17)
        px, py = trunk[-1]
        for dx, dy in ((-86, -34), (-58, -62), (0, -74), (58, -62), (86, -34)):
            d.line([(px, py), (px + dx * flip, py + dy + 30)], fill=(24, 8, 34), width=10, joint="curve")
    # Leonida skyline silhouette along the screen bottom
    sky = [(316, 566), (316, 512), (372, 512), (372, 488), (428, 488), (428, 522),
           (492, 522), (492, 472), (548, 472), (548, 566)]
    d.polygon(sky, fill=(24, 8, 34))
    d.polygon([(x, y) for x, y in [(754, 566), (754, 500), (806, 500), (806, 478),
                                   (868, 478), (868, 516), (930, 516), (930, 566)]], fill=(24, 8, 34))
    text_center(d, 651, 226, "VICE CITY  •  LEONIDA", font(30), fill=WHITE, stroke=3)
    text_center(d, 651, 288, "GRAND THEFT AUTO VI", font(54), fill=WHITE, stroke=5)
    text_center(d, 651, 354, "Downloading…  99%", font(42), fill=WHITE, stroke=5)
    # progress bar at 99% — dark track + white rim so magenta pops on sunset
    rounded(d, [352, 412, 950, 472], 14, fill=(16, 10, 34), outline=WHITE, width=6)
    fill_w = int((950 - 352 - 16) * 0.99)
    rounded(d, [360, 420, 360 + fill_w, 464], 10, fill=MAGENTA)
    d.text((868, 424), "99%", font=font(32), fill=WHITE, stroke_width=2, stroke_fill=BLACK)
    text_center(d, 651, 482, "Time remaining:  3 DAYS", font(48), fill=YELLOW, stroke=5)

    # standing fan, left wall — head, blades, pole (visible, not behind TV)
    fx, fy = 128, 566
    d.line([(fx, fy + 40), (fx, 690)], fill=(200, 200, 210), width=10)
    d.ellipse([fx - 52, 682, fx + 52, 706], fill=(200, 200, 210), outline=BLACK, width=4)
    d.ellipse([fx - 56, fy - 56, fx + 56, fy + 56], fill=(24, 30, 62), outline=(200, 200, 210), width=6)
    for ang in (90, 210, 330):
        a = math.radians(ang)
        bx, by = fx + 40 * math.cos(a), fy + 40 * math.sin(a)
        d.line([(fx, fy), (bx, by)], fill=(200, 200, 210), width=13)
    d.ellipse([fx - 10, fy - 10, fx + 10, fy + 10], fill=WHITE, outline=BLACK, width=3)

    # TV stand + router with red light — moved right so the ghost
    # (centre couch) cannot hide it; the red LED must read at a glance
    d.rectangle([380, 586, 922, 606], fill=(16, 14, 22))
    d.rectangle([420, 606, 460, 664], fill=(16, 14, 22))
    d.rectangle([842, 606, 882, 664], fill=(16, 14, 22))
    rounded(d, [716, 610, 986, 658], 10, fill=(18, 18, 24), outline=BLACK, width=5)
    d.ellipse([736, 624, 764, 652], fill=(255, 40, 40), outline=BLACK, width=3)
    d.line([(946, 610), (972, 570)], fill=BLACK, width=6)
    d.line([(972, 610), (972, 564)], fill=BLACK, width=6)
    d.text((782, 620), "WiFi OFF", font=font(28), fill=(255, 120, 120))

    # ---- couch ----
    rounded(d, [52, 700, 1028, 1036], 44, fill=(13, 116, 122), outline=BLACK, width=9)
    rounded(d, [52, 700, 1028, 852], 44, fill=(16, 140, 148), outline=BLACK, width=7)
    # cushions
    d.line([(360, 716), (360, 1018)], fill=BLACK, width=6)
    d.line([(724, 716), (724, 1018)], fill=BLACK, width=6)
    # arms
    rounded(d, [36, 790, 168, 1040], 36, fill=(255, 92, 168), outline=BLACK, width=8)
    rounded(d, [912, 790, 1044, 1040], 36, fill=(255, 92, 168), outline=BLACK, width=8)

    # snacks: popcorn bowl (left cushion), soda + chips (right)
    d.polygon([(196, 884), (316, 884), (292, 956), (220, 956)], fill=(240, 240, 240), outline=BLACK)
    for px, py in [(214, 866), (246, 852), (278, 866), (232, 878), (264, 878)]:
        d.ellipse([px - 17, py - 17, px + 17, py + 17], fill=(255, 226, 130), outline=BLACK, width=3)
    d.text((224, 902), "SNACKS", font=font(20), fill=BLACK)
    # soda can on the right cushion, clear of the coin so neither is cluttered
    rounded(d, [848, 846, 904, 944], 10, fill=(220, 30, 50), outline=BLACK, width=5)
    d.rectangle([848, 888, 904, 906], fill=WHITE)
    text_center(d, 876, 858, "COLA", font(15), fill=WHITE)

    # dropped controller on the couch, left of the ghost
    rounded(d, [150, 972, 292, 1026], 26, fill=(22, 22, 30), outline=BLACK, width=6)
    d.ellipse([172, 988, 196, 1012], fill=CYAN)
    d.ellipse([248, 988, 266, 1006], fill=MAGENTA)
    d.ellipse([266, 1008 - 18, 284, 1008], fill=YELLOW)

    # ---- the ghost, sitting centre-couch, staring up at the bar ----
    draw_ghost(d, 520, 612, 318, 372)

    # its hand reaches to the coin resting on the couch beside it
    hx, hy = 706, 902
    d.ellipse([hx - 30, hy - 30, hx + 30, hy + 30], fill=WHITE, outline=BLACK, width=7)
    draw_coin(d, 768, 918, 60)
    d.text((664, 992), "still waiting…", font=font(25), fill=WHITE, stroke_width=2, stroke_fill=BLACK)

    # ---- caption band on top ----
    d.rectangle([0, 0, W, 178], fill=BLACK)
    d.rectangle([0, 172, W, 178], fill=MAGENTA)
    text_center(d, 540, 16, "150 GB. MY WIFI", font(76), fill=WHITE, stroke=3)
    text_center(d, 540, 96, "JUST GAVE UP.", font(76), fill=YELLOW, stroke=3)

    img.save(OUT, "PNG")
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
