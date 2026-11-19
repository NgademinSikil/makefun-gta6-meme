#!/usr/bin/env python3
"""Variant D — "distracted boyfriend" meme for make.fun's gta6-meme-x-01.

The joke: on a sunny Vice City street, "ME" turns around smitten to look at
glamorous "GTA 6" (make.fun's ghost in sunglasses and a gold chain under a
pink neon sign) while "MY RESPONSIBILITIES" stands behind him, arms crossed,
glaring. Every figure is an original flat cartoon drawn with PIL — no
Rockstar artwork, no stock photo, no copied meme template image.

The picture is a pure function of the constants below: no randomness, no
wall clock, no network, so two runs write byte-identical PNGs. It writes
entry.png into $MAKEFUN_OUTPUT_DIR and copies POST.json from the repository
root ($MAKEFUN_BOT_DIR) next to it when the file exists.

Run it: mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import math
import os
import shutil
import sys

from PIL import Image, ImageDraw, ImageFont

CANVAS = 1024

# --- typefaces (system DejaVu, as shipped on this machine) ---
BOLD_FACE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PLAIN_FACE = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

# --- palette: every colour the picture uses, named once here ---
INK_WHITE = (255, 255, 255)
INK_BLACK = (0, 0, 0)
SKIN = (255, 210, 170)
SKIN_SHADE = (245, 190, 150)
DARK_LINE = (30, 30, 30)
PINK_NEON = (255, 60, 180)
PINK_EDGE = (255, 200, 230)
NEON_TEXT_EDGE = (120, 0, 60)
GOLD = (255, 210, 40)
GOLD_EDGE = (160, 110, 0)


def load_font(points, bold=True):
    """One DejaVu face at the requested size."""
    return ImageFont.truetype(BOLD_FACE if bold else PLAIN_FACE, points)


def blend(first, second, fraction):
    """Linear blend between two RGB triples."""
    return tuple(int(first[i] + (second[i] - first[i]) * fraction) for i in range(3))


def outline_text(draw, pos, string, face, ink, edge, thick=4):
    """Text in `ink` with a solid disc outline of `edge` around every glyph."""
    x, y = pos
    for dx in range(-thick, thick + 1):
        for dy in range(-thick, thick + 1):
            if dx * dx + dy * dy <= thick * thick:
                draw.text((x + dx, y + dy), string, font=face, fill=edge)
    draw.text((x, y), string, font=face, fill=ink)


def centered_text(draw, centre_x, y, string, face, ink, edge, thick=4):
    """outline_text centred on `centre_x` (measured with textbbox)."""
    box = draw.textbbox((0, 0), string, font=face)
    span = box[2] - box[0]
    outline_text(draw, (centre_x - span // 2, y), string, face, ink, edge, thick)


def palm_tree(draw, x, y, scale, lean):
    """One leaning palm: a trunk plus five drooping fronds."""
    draw.line([(x, y), (x + lean, y - 170 * scale)], fill=(120, 80, 40),
              width=int(14 * scale))
    crown = (x + lean, y - 170 * scale)
    for degrees in range(-160, 40, 40):
        angle = math.radians(degrees)
        tip_x = crown[0] + int(90 * scale * math.cos(angle))
        tip_y = crown[1] + int(40 * scale * math.sin(angle)) + 30 * scale
        draw.line([crown, (tip_x, tip_y)], fill=(40, 160, 80),
                  width=int(10 * scale))


def paint_sky(draw):
    """Daytime gradient, sun and clouds (rows 0..699; the street covers the rest)."""
    sky_top = (90, 180, 250)
    sky_bottom = (255, 214, 150)
    for row in range(700):
        draw.line([(0, row), (CANVAS, row)],
                  fill=blend(sky_top, sky_bottom, row / 700))
    draw.ellipse([820, 60, 950, 190], fill=(255, 240, 120),
                 outline=(255, 200, 60), width=5)
    for (cx, cy, size) in [(180, 120, 70), (430, 80, 55), (650, 150, 60)]:
        draw.ellipse([cx - size, cy - size // 2, cx + size, cy + size // 2],
                     fill=INK_WHITE)
        draw.ellipse([cx - size // 2, cy - size, cx + size // 2, cy + size // 3],
                     fill=INK_WHITE)


def paint_street(draw):
    """Pastel buildings with lit windows, palms, sidewalk and road."""
    blocks = [
        (30, 300, 170, 640, (255, 170, 200)),
        (190, 360, 320, 640, (140, 220, 255)),
        (700, 330, 850, 640, (255, 210, 120)),
        (870, 380, 1000, 640, (180, 255, 190)),
    ]
    for (left, top, right, bottom, colour) in blocks:
        draw.rectangle([left, top, right, bottom], fill=colour,
                       outline=(60, 60, 90), width=3)
        for wy in range(top + 30, bottom - 20, 55):
            for wx in range(left + 20, right - 20, 45):
                draw.rectangle([wx, wy, wx + 22, wy + 30],
                               fill=(255, 250, 180), outline=(60, 60, 90), width=2)
    palm_tree(draw, 60, 660, 1.0, 25)
    palm_tree(draw, 985, 660, 0.9, -25)
    draw.rectangle([0, 640, CANVAS, 700], fill=(210, 200, 190))
    draw.rectangle([0, 700, CANVAS, CANVAS], fill=(70, 70, 85))
    for x in range(20, CANVAS, 110):
        draw.rectangle([x, 830, x + 60, 844], fill=(255, 220, 80))


def paint_girlfriend(draw):
    """Left figure: "MY RESPONSIBILITIES" — red dress, crossed arms, glaring."""
    base_x, feet = 185, 700
    # long dark hair falling behind the shoulders
    draw.ellipse([base_x - 62, feet - 330, base_x + 62, feet - 190],
                 fill=(60, 30, 20))
    draw.rectangle([base_x - 62, feet - 260, base_x - 30, feet - 120],
                   fill=(60, 30, 20))
    draw.rectangle([base_x + 30, feet - 260, base_x + 62, feet - 120],
                   fill=(60, 30, 20))
    # red dress, wide at the hem
    draw.polygon([(base_x - 48, feet - 180), (base_x + 48, feet - 180),
                  (base_x + 78, feet - 10), (base_x - 78, feet - 10)],
                 fill=(220, 40, 60), outline=(120, 10, 20), width=3)
    # head
    draw.ellipse([base_x - 52, feet - 300, base_x + 52, feet - 196],
                 fill=SKIN, outline=(150, 90, 60), width=3)
    # eyes looking right, pupils hard to the right
    draw.ellipse([base_x - 30, feet - 262, base_x - 12, feet - 244],
                 fill=INK_WHITE)
    draw.ellipse([base_x + 12, feet - 262, base_x + 30, feet - 244],
                 fill=INK_WHITE)
    draw.ellipse([base_x - 22, feet - 258, base_x - 14, feet - 250],
                 fill=(20, 20, 20))
    draw.ellipse([base_x + 18, feet - 258, base_x + 26, feet - 250],
                 fill=(20, 20, 20))
    # brows slanting down toward the middle: the glare
    draw.line([(base_x - 34, feet - 276), (base_x - 8, feet - 266)],
              fill=(40, 20, 10), width=6)
    draw.line([(base_x + 34, feet - 276), (base_x + 8, feet - 266)],
              fill=(40, 20, 10), width=6)
    # frown
    draw.arc([base_x - 22, feet - 236, base_x + 22, feet - 206],
             start=200, end=340, fill=(120, 40, 30), width=5)
    # crossed arms: two thick diagonal strokes across the chest
    draw.line([(base_x - 52, feet - 168), (base_x + 52, feet - 128)],
              fill=SKIN, width=16)
    draw.line([(base_x + 52, feet - 168), (base_x - 52, feet - 128)],
              fill=SKIN_SHADE, width=16)
    # legs and shoes
    draw.rectangle([base_x - 34, feet - 12, base_x - 12, feet + 40], fill=SKIN)
    draw.rectangle([base_x + 12, feet - 12, base_x + 34, feet + 40], fill=SKIN)
    draw.rectangle([base_x - 38, feet + 38, base_x - 8, feet + 52],
                   fill=(40, 40, 40))
    draw.rectangle([base_x + 8, feet + 38, base_x + 38, feet + 52],
                   fill=(40, 40, 40))


def paint_boyfriend(draw):
    """Centre figure: "ME" — teal shirt, mid-stride, head turned right, smitten."""
    base_x, feet = 430, 700
    # walking legs and shoes
    draw.line([(base_x - 15, feet - 130), (base_x - 45, feet + 30)],
              fill=(40, 60, 120), width=26)
    draw.line([(base_x + 15, feet - 130), (base_x + 55, feet + 10)],
              fill=(40, 60, 120), width=26)
    draw.rectangle([base_x - 62, feet + 24, base_x - 28, feet + 44],
                   fill=(30, 30, 30))
    draw.rectangle([base_x + 42, feet + 4, base_x + 76, feet + 24],
                   fill=(30, 30, 30))
    # teal t-shirt
    draw.rounded_rectangle([base_x - 55, feet - 260, base_x + 55, feet - 125],
                           radius=25, fill=(30, 180, 170),
                           outline=(10, 100, 95), width=3)
    # one arm hanging, the other reaching toward the ghost
    draw.line([(base_x - 55, feet - 240), (base_x - 78, feet - 150)],
              fill=SKIN, width=18)
    draw.line([(base_x + 50, feet - 240), (base_x + 120, feet - 215)],
              fill=SKIN, width=18)
    # head, turned to the right
    draw.ellipse([base_x - 52, feet - 380, base_x + 52, feet - 276],
                 fill=SKIN, outline=(150, 90, 60), width=3)
    draw.pieslice([base_x - 52, feet - 380, base_x + 52, feet - 276],
                  start=180, end=360, fill=(50, 35, 20))
    draw.rectangle([base_x - 52, feet - 340, base_x - 20, feet - 300],
                   fill=(50, 35, 20))
    # one visible eye, looking right, plus smile and blush
    draw.ellipse([base_x + 12, feet - 340, base_x + 30, feet - 322],
                 fill=INK_WHITE)
    draw.ellipse([base_x + 20, feet - 336, base_x + 28, feet - 328],
                 fill=(20, 20, 20))
    draw.arc([base_x - 5, feet - 318, base_x + 45, feet - 288],
             start=10, end=170, fill=(150, 60, 40), width=5)
    draw.ellipse([base_x + 30, feet - 308, base_x + 48, feet - 296],
                 fill=(255, 120, 120))


def paint_heart(draw):
    """Small pink heart floating between the boyfriend and the ghost."""
    heart_x, heart_y = 610, 480
    draw.ellipse([heart_x - 26, heart_y - 14, heart_x, heart_y + 10],
                 fill=(255, 60, 110))
    draw.ellipse([heart_x, heart_y - 14, heart_x + 26, heart_y + 10],
                 fill=(255, 60, 110))
    draw.polygon([(heart_x - 24, heart_y), (heart_x + 24, heart_y),
                  (heart_x, heart_y + 34)], fill=(255, 60, 110))


def paint_sign(draw):
    """Pink neon "GTA 6" sign, hung above the ghost so it stays visible."""
    draw.rounded_rectangle([700, 300, 990, 400], radius=18,
                           fill=PINK_NEON, outline=PINK_EDGE, width=6)
    draw.rounded_rectangle([688, 288, 1002, 412], radius=22,
                           outline=PINK_NEON, width=4)
    centered_text(draw, 845, 325, "GTA 6", load_font(58), INK_WHITE,
                  NEON_TEXT_EDGE, 3)


def paint_ghost(draw):
    """Right figure: make.fun's ghost, glamorous — shades, gold chain, leaning
    on the sign. White body with a thick dark outline, scalloped hem."""
    centre, base = 830, 700
    # dome, body and wavy hem, all in white
    draw.pieslice([centre - 95, base - 330, centre + 95, base - 140],
                  start=180, end=360, fill=INK_WHITE)
    draw.rectangle([centre - 95, base - 235, centre + 95, base - 60],
                   fill=INK_WHITE)
    for offset in [-71, -24, 24, 71]:
        draw.ellipse([centre + offset - 26, base - 95,
                      centre + offset + 26, base - 45], fill=INK_WHITE)
    # the thick dark outline around dome and body
    draw.ellipse([centre - 95, base - 330, centre + 95, base - 140],
                 fill=None, outline=DARK_LINE, width=4)
    draw.rectangle([centre - 95, base - 235, centre + 95, base - 60],
                   outline=DARK_LINE, width=4)
    # cool black sunglasses and a smile underneath
    draw.rounded_rectangle([centre - 70, base - 290, centre - 8, base - 252],
                           radius=10, fill=(20, 20, 20))
    draw.rounded_rectangle([centre + 8, base - 290, centre + 70, base - 252],
                           radius=10, fill=(20, 20, 20))
    draw.line([(centre - 8, base - 272), (centre + 8, base - 272)],
              fill=(20, 20, 20), width=8)
    draw.arc([centre - 25, base - 235, centre + 25, base - 205],
             start=10, end=170, fill=(150, 60, 40), width=5)
    # gold chain draped across the chest
    for step in range(9):
        t = step / 8
        bead_x = centre - 64 + int(128 * t)
        bead_y = base - 190 + int(38 * math.sin(math.pi * t))
        draw.ellipse([bead_x - 9, bead_y - 9, bead_x + 9, bead_y + 9],
                     fill=GOLD, outline=GOLD_EDGE, width=2)
    # one little arm leaning back onto the sign
    draw.line([(centre - 90, base - 200), (centre - 130, base - 260)],
              fill=INK_WHITE, width=16)
    draw.ellipse([centre - 140, base - 275, centre - 115, base - 250],
                 fill=INK_WHITE)


def paint_labels(draw):
    """The three role labels plus the make.fun wordmark at the bottom."""
    centered_text(draw, 185, 300, "MY", load_font(46), INK_WHITE, INK_BLACK, 5)
    centered_text(draw, 185, 352, "RESPONSIBILITIES", load_font(34),
                  INK_WHITE, INK_BLACK, 4)
    centered_text(draw, 430, 250, "ME", load_font(64), INK_WHITE, INK_BLACK, 6)
    centered_text(draw, CANVAS // 2, 950, "make.fun", load_font(54),
                  INK_WHITE, INK_BLACK, 5)


def render():
    """Draw the whole scene in order; later layers cover earlier ones."""
    picture = Image.new("RGB", (CANVAS, CANVAS))
    draw = ImageDraw.Draw(picture, "RGBA")
    paint_sky(draw)
    paint_street(draw)
    paint_girlfriend(draw)
    paint_boyfriend(draw)
    paint_heart(draw)
    paint_sign(draw)
    paint_ghost(draw)
    paint_labels(draw)
    return picture


def main():
    repo_dir = os.environ.get("MAKEFUN_BOT_DIR", "/bot")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    picture = render()
    picture.save(os.path.join(out_dir, "entry.png"))
    print("wrote", os.path.join(out_dir, "entry.png"))
    post_path = os.path.join(repo_dir, "POST.json")
    if os.path.exists(post_path):
        shutil.copyfile(post_path, os.path.join(out_dir, "POST.json"))
    else:
        print("POST.json not in the repository yet: the post is made later, "
              "then POST.json is added before submitting.", file=sys.stderr)


if __name__ == "__main__":
    main()
