#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: one front page summing up the world
news of Monday 23 November 2026.

Six verified stories, each drawn as its own panel with a small scene, a
headline and a two-sentence summary. Nothing is random and nothing carries a
timestamp, so re-running this script always writes the same PNG bytes.

Run:  python3 draw.py        (writes entry.png beside this file)
"""

import hashlib
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (22, 21, 18)
MUTED = (96, 90, 80)
RULE = (22, 21, 18)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width` pixels."""
    lines = []
    for raw in text.split("\n"):
        words = raw.split()
        cur = ""
        for word in words:
            trial = (cur + " " + word).strip()
            if d.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def scene_gulf(d, x, y, w, h):
    """Red Sea dusk: refinery towers, a flare flame and a missile arc."""
    sky = [(58, 44, 62), (96, 52, 58), (150, 74, 52), (206, 122, 62)]
    band = h // 4
    for i, c in enumerate(sky):
        d.rectangle([x, y + i * band, x + w, y + (i + 1) * band], fill=c)
    # sea
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(24, 48, 66))
    d.rectangle([x, y + h - 26, x + w, y + h - 24], fill=(220, 150, 60))
    # refinery towers
    for tx, th, tw in [(18, 62, 26), (58, 84, 30), (104, 70, 26)]:
        d.rectangle([x + tx, y + h - 26 - th, x + tx + tw, y + h - 26],
                    fill=(30, 28, 30))
        d.polygon([(x + tx - 3, y + h - 26 - th), (x + tx + tw + 3, y + h - 26 - th),
                   (x + tx + tw // 2, y + h - 26 - th - 12)], fill=(30, 28, 30))
        for wy in range(y + h - 26 - th + 8, y + h - 30, 12):
            d.rectangle([x + tx + 5, wy, x + tx + tw - 5, wy + 4],
                        fill=(214, 164, 62))
    # flare stack flame
    fx = x + w - 52
    d.rectangle([fx, y + h - 26 - 96, fx + 8, y + h - 26], fill=(30, 28, 30))
    d.polygon([(fx - 8, y + h - 26 - 96), (fx + 16, y + h - 26 - 96),
               (fx + 4, y + h - 26 - 128)], fill=(255, 176, 32))
    d.polygon([(fx - 2, y + h - 26 - 96), (fx + 10, y + h - 26 - 96),
               (fx + 4, y + h - 26 - 114)], fill=(255, 232, 130))
    # missile arc with dotted smoke trail
    pts = []
    for i in range(21):
        t = i / 20.0
        px = x + 150 + t * 140
        py = y + 78 - 58 * (1 - (2 * t - 1) ** 2)
        pts.append((px, py))
    for i in range(0, len(pts) - 1, 2):
        d.line([pts[i], pts[i + 1]], fill=(240, 236, 224), width=3)
    hx, hy = pts[-1]
    d.ellipse([hx - 4, hy - 4, hx + 10, hy + 4], fill=(240, 236, 224))
    d.polygon([(hx + 10, hy), (hx + 22, hy - 3), (hx + 22, hy + 3)],
              fill=(255, 176, 32))


def scene_cop(d, x, y, w, h):
    """A globe over cracked earth, with a row of summit flags above."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 208))
    flag_cols = [(0, 90, 160), (200, 40, 40), (0, 120, 70), (230, 180, 0),
                 (120, 60, 140), (220, 120, 30)]
    for i, c in enumerate(flag_cols):
        fx = x + 14 + i * 50
        d.rectangle([fx, y + 12, fx + 34, y + 30], fill=c)
        d.line([fx + 2, y + 12, fx + 2, y + 44], fill=(60, 60, 60), width=2)
    # globe
    cx, cy, r = x + w // 2, y + h // 2 + 12, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 180),
              outline=(22, 60, 90), width=3)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=(22, 60, 90),
              width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(22, 60, 90), width=2)
    d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 200, 340,
          fill=(22, 60, 90), width=2)
    # land blobs
    d.ellipse([cx - 34, cy - 26, cx - 6, cy - 2], fill=(96, 160, 90))
    d.ellipse([cx + 2, cy + 8, cx + 30, cy + 30], fill=(96, 160, 90))
    # cracked earth at the bottom
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(168, 132, 92))
    d.line([x + 40, y + h - 30, x + 90, y + h - 8, x + 150, y + h - 26,
            x + 210, y + h - 6, x + 280, y + h - 22], fill=(90, 60, 36), width=3)
    # red NO-DEAL stamp
    d.rectangle([x + w - 108, y + h - 78, x + w - 12, y + h - 50],
                outline=(178, 34, 34), width=3)
    d.text((x + w - 102, y + h - 76), "NO DEAL", font=font(SANS_B, 17),
           fill=(178, 34, 34))


def scene_house(d, x, y, w, h):
    """The US Capitol dome above rising blue bars, with the 258 figure."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 234, 246))
    # rising bars
    bars = [34, 52, 44, 70, 88, 108]
    bw = 26
    for i, bh in enumerate(bars):
        bx = x + 16 + i * 34
        d.rectangle([bx, y + h - 18 - bh, bx + bw, y + h - 18],
                    fill=(38, 84, 160) if i < 5 else (24, 52, 110))
    # capitol dome, right side
    cx = x + w - 78
    base = y + h - 18
    d.rectangle([cx - 52, base - 34, cx + 52, base], fill=(250, 250, 246),
                outline=(120, 120, 120))
    for i in range(-2, 3):
        d.rectangle([cx + i * 20 - 4, base - 30, cx + i * 20 + 4, base - 6],
                    fill=(180, 180, 175))
    d.pieslice([cx - 46, base - 84, cx + 46, base - 8], 180, 360,
               fill=(250, 250, 246), outline=(120, 120, 120))
    d.rectangle([cx - 4, base - 104, cx + 4, base - 84], fill=(120, 120, 120))
    d.ellipse([cx - 5, base - 110, cx + 5, base - 100], fill=(200, 170, 60))
    d.text((x + 16, y + 10), "258", font=font(SANS_B, 46), fill=(24, 52, 110))
    d.text((x + 118, y + 26), "SEATS", font=font(SANS_B, 20), fill=(24, 52, 110))


def scene_dymer(d, x, y, w, h):
    """A five-storey block with its middle stairwell collapsed to rubble."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 198, 200))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(120, 118, 112))
    bx, by = x + 52, y + 8
    bw, bh = 218, 108
    d.rectangle([bx, by, bx + bw, by + bh], fill=(168, 164, 156),
                outline=(90, 88, 82), width=2)
    # windows, five floors
    for row in range(5):
        for col in range(6):
            wx = bx + 10 + col * 34
            wy = by + 8 + row * 20
            if col in (2, 3) and row >= 2:
                continue  # collapsed stairwell: no windows, just a hole
            d.rectangle([wx, wy, wx + 20, wy + 12], fill=(70, 90, 110))
    # collapsed section: jagged hole + rubble
    d.polygon([(bx + 74, by + 48), (bx + 144, by + 48), (bx + 152, by + 78),
               (bx + 128, by + 108), (bx + 92, by + 108), (bx + 66, by + 78)],
              fill=(52, 50, 48))
    for rx, ry, rw, rh in [(bx + 60, by + 108, 26, 10), (bx + 92, by + 112, 30, 12),
                           (bx + 126, by + 108, 24, 10), (bx + 108, by + 122, 34, 10),
                           (bx + 70, by + 124, 30, 8)]:
        d.rectangle([rx, ry, rx + rw, ry + rh], fill=(110, 106, 98),
                    outline=(70, 66, 60))
    # rescue ladder leaning on the block
    d.line([bx + 210, by + bh + 22, bx + 178, by + 12], fill=(200, 60, 40),
           width=4)
    for i in range(6):
        t = i / 5.0
        lx = bx + 210 - 32 * t
        ly = by + bh + 22 - (bh + 10) * t
        d.line([lx - 7, ly, lx + 7, ly], fill=(200, 60, 40), width=3)
    # smoke
    for sx, sy, sr in [(bx + 90, by - 2, 12), (bx + 120, by - 8, 16),
                       (bx + 150, by - 2, 11)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 138, 134))


def scene_merkury(d, x, y, w, h):
    """A warship capsized in harbour: only the bow shows above the water."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
    d.rectangle([x, y + h - 58, x + w, y + h], fill=(44, 88, 110))
    for i in range(4):
        d.line([x + 10 + i * 78, y + h - 40, x + 60 + i * 78, y + h - 40],
               fill=(120, 170, 190), width=2)
    # capsized hull: dark shape mostly under water, bow jutting up
    d.polygon([(x + 60, y + h - 58), (x + 210, y + h - 58),
               (x + 236, y + h - 30), (x + 40, y + h - 30)],
              fill=(58, 58, 62))
    d.polygon([(x + 210, y + h - 58), (x + 258, y + h - 96),
               (x + 272, y + h - 58)], fill=(74, 74, 78))
    d.rectangle([x + 238, y + h - 108, x + 246, y + h - 96], fill=(74, 74, 78))
    d.ellipse([x + 236, y + h - 114, x + 248, y + h - 102], fill=(200, 60, 40))
    # fire glow on the waterline
    d.polygon([(x + 96, y + h - 58), (x + 128, y + h - 58),
               (x + 112, y + h - 84)], fill=(255, 176, 32))
    d.polygon([(x + 106, y + h - 58), (x + 122, y + h - 58),
               (x + 114, y + h - 74)], fill=(255, 232, 130))
    # smoke plumes
    for sx, sy, sr in [(x + 120, y + 26, 18), (x + 150, y + 14, 24),
                       (x + 184, y + 26, 16)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 118, 114))


def scene_factory(d, x, y, w, h):
    """A candy factory with flames breaking through a sawtooth roof."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 214, 186))
    # smoke columns
    for sx, sy, sr in [(x + 60, y + 16, 16), (x + 92, y + 8, 20),
                       (x + 240, y + 14, 18), (x + 268, y + 6, 14)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(110, 106, 100))
    # factory block with sawtooth roof
    fx, fy = x + 30, y + 62
    d.rectangle([fx, fy, fx + 262, fy + 66], fill=(150, 128, 104),
                outline=(80, 66, 52), width=2)
    for i in range(4):
        sx = fx + i * 66
        d.polygon([(sx, fy), (sx + 33, fy - 22), (sx + 66, fy)],
                  fill=(120, 100, 80), outline=(80, 66, 52))
    for i in range(6):
        d.rectangle([fx + 14 + i * 40, fy + 18, fx + 34 + i * 40, fy + 40],
                    fill=(70, 84, 96))
    # flames through the roof
    for px, pw, ph in [(fx + 40, 26, 52), (fx + 120, 34, 66), (fx + 200, 26, 48)]:
        d.polygon([(px, fy), (px + pw, fy), (px + pw // 2, fy - ph)],
                  fill=(255, 120, 20))
        d.polygon([(px + 7, fy), (px + pw - 7, fy), (px + pw // 2, fy - ph + 18)],
                  fill=(255, 214, 80))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 84, 76))


STORIES = [
    dict(num="1", kicker="THE GULF WAR", color=(178, 34, 34),
         scene=scene_gulf,
         headline="Houthis claim refinery hit as Saudi defences stop a missile",
         body=("Yemen's Houthis said they struck Saudi Arabia's Rabigh oil "
               "refinery on the Red Sea coast on Sunday, claiming a direct "
               "hit. Riyadh gave no confirmation; its coalition said it shot "
               "down a ballistic missile aimed at the kingdom's west."),
         sources="Reuters · AP"),
    dict(num="2", kicker="COP31 · ANTALYA", color=(34, 110, 60),
         scene=scene_cop,
         headline="Climate talks collapse — the longest COP ends with no deal",
         body=("UN climate talks in Antalya ended without agreement on Sunday "
               "after the EU and others rejected a draft that never mentioned "
               "fossil fuels. The summit ran two days into overtime, the "
               "longest COP on record; talks resume next year."),
         sources="Reuters · AP · edie"),
    dict(num="3", kicker="WASHINGTON", color=(24, 52, 110),
         scene=scene_house,
         headline="Democrats clinch 258 House seats — biggest majority since 1992",
         body=("Democrats secured their 258th House seat on Sunday as Chuck "
               "Hubbard beat Virginia Foxx in North Carolina — a 44-seat gain "
               "and the largest House majority for either party in three "
               "decades. Four races remain uncalled."),
         sources="AP · Reuters · CBS"),
    dict(num="4", kicker="KYIV REGION", color=(60, 80, 130),
         scene=scene_dymer,
         headline="Drone strike flattens apartment block; 14 missing in Dymer",
         body=("A Russian drone strike collapsed part of a five-storey "
               "apartment block in Dymer, north of Kyiv, on Sunday. Two people "
               "were killed and 14 residents, including two children, were "
               "unaccounted for as rescuers dug through the rubble."),
         sources="Reuters · France 24 · The Hindu"),
    dict(num="5", kicker="BENGHAZI, LIBYA", color=(20, 90, 96),
         scene=scene_merkury,
         headline="Russian warship sunk in port after suspected drone attack",
         body=("The Russian Navy corvette Merkury capsized and mostly sank at "
               "Benghazi naval base on Sunday after a suspected drone attack. "
               "Ten Russians and Libyans were hurt; Libya asked the UN to "
               "investigate the strike."),
         sources="Reuters · AP · AAP"),
    dict(num="6", kicker="WEST JAVA", color=(196, 96, 20),
         scene=scene_factory,
         headline="Candy factory fire kills 3; about 50 workers missing",
         body=("Fire tore through the PT Fonusa Agung Mulia candy factory in "
               "Cikande, Banten, on Saturday evening. Seven body bags were "
               "recovered on Sunday as rescuers searched for about 50 missing "
               "workers; DNA tests may take weeks."),
         sources="Reuters · AP · AFP"),
]

TICKER = ("ALSO:  SPARTA II STILL BURNING OFF FINLAND   •   "
          "TRUMP: NO IRAN DECISION UNTIL 2027   •   "
          "VERSTAPPEN WINS LAS VEGAS GP")


def draw_panel(d, story, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    # kicker band
    d.rectangle([x, y, x + w, y + 30], fill=story["color"])
    d.text((x + 10, y + 6), story["num"] + "  " + story["kicker"],
           font=font(SANS_B, 15), fill=WHITE)
    # illustration
    story["scene"](d, x + 2, y + 32, w - 4, 148)
    # headline
    hx, hy = x + 12, y + 190
    for line in wrap(d, story["headline"], font(SANS_B, 20), w - 24):
        d.text((hx, hy), line, font=font(SANS_B, 20), fill=INK)
        hy += 25
    # body
    by = hy + 6
    for line in wrap(d, story["body"], font(SANS, 14), w - 24):
        d.text((x + 12, by), line, font=font(SANS, 14), fill=(52, 50, 46))
        by += 19
    # source line pinned to the panel bottom
    d.text((x + 12, y + h - 22), "Sources: " + story["sources"],
           font=font(SANS, 11), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 4], fill=INK)
    d.text((512, 12), "THE WORLD IN ONE DAY", font=font(SERIF_B, 42),
           fill=INK, anchor="ma")
    d.text((512, 62), "MONDAY, 23 NOVEMBER 2026  —  SIX STORIES, ONE DAY",
           font=font(SANS_B, 17), fill=(120, 40, 40), anchor="ma")
    d.line([16, 96, W - 16, 96], fill=RULE, width=3)
    d.line([16, 101, W - 16, 101], fill=RULE, width=1)

    # ---- story grid: 3 columns x 2 rows ----
    margin, gutter = 16, 12
    pw = (W - 2 * margin - 2 * gutter) // 3
    ph = 404
    top = 112
    for i, story in enumerate(STORIES):
        col, row = i % 3, i // 3
        px = margin + col * (pw + gutter)
        py = top + row * (ph + gutter)
        draw_panel(d, story, px, py, pw, ph)

    # ---- footer ticker ----
    ty = top + 2 * ph + gutter + 8
    d.rectangle([margin, ty, W - margin, ty + 34], fill=INK)
    d.text((margin + 10, ty + 8), TICKER, font=font(SANS_B, 13), fill=(240, 230, 200))

    img.save(OUT, format="PNG", optimize=True)
    data = open(OUT, "rb").read()
    print("wrote", OUT, len(data), "bytes",
          "sha256", hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
