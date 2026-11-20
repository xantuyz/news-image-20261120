#!/usr/bin/env python3
"""Draw the world news of Friday 20 November 2026 as a one-page
newspaper front page, 1024x1024 PNG.

Pure Pillow: flat spot illustrations drawn with polygons, arcs and
ellipses, copy set in DejaVu. Run: python3 render.py
Writes entry.png beside this script.

Stories (each verified against live reporting on the morning of
20 Nov 2026; Thursday events are dated Thursday on the page):
  1. Cyclone Akvan is due ashore on India's east coast today,
     near Gopalpur, Odisha, around noon IST; 300,000+ evacuated.
  2. Trump, aboard Air Force One on Thursday, says he is in no
     hurry to decide on Iran; he will talk about it after the
     start of the year.
  3. The Trump-Xi-Putin "peace declaration" text is released on
     Friday: nuclear war "cannot be won"; no mention of Ukraine
     or Iran.
  4. Russian strikes damage the Austrian and Dutch embassies in
     Kyiv on Thursday; on Friday the EU says it will summon
     Russia's ambassador.
  5. Engine trouble forces Japan's Hayabusa2 probe to drop its
     planned asteroid landing (Friday report).
  6. Rohingya cheer the ICJ's Thursday finding that Myanmar is
     responsible for genocide; the court ordered reparations.
  (Berlin — Europe saying it is ready for talks with Russia — was
  verified but left out for space; the diplomacy arc is carried
  by the Shenzhen and Kyiv stories.)
"""
import os

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 44
GUTTER = 24
CONTENT = PAGE - 2 * MARGIN
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette --------------------------------------------------------------
PAPER = (250, 246, 238)
INK = (22, 22, 22)
RUST = (172, 48, 36)
TEAL = (36, 110, 96)
NAVY = (24, 38, 58)
FAINT = (112, 106, 96)
RULEC = (205, 197, 180)
TINT = (238, 230, 214)
SEA = (46, 120, 110)
SAND = (233, 216, 180)
IVORY = (252, 252, 250)
SKY = (214, 232, 228)
LEMON = (240, 196, 60)

FONTS = "/usr/share/fonts/truetype/dejavu/"


def face(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def serif(size):
    return face("DejaVuSerif-Bold.ttf", size)


def sans_bold(size):
    return face("DejaVuSans-Bold.ttf", size)


def sans(size):
    return face("DejaVuSans.ttf", size)


class Sheet:
    """A 1024x1024 page with wrapping and story helpers."""

    def __init__(self):
        self.img = Image.new("RGB", (PAGE, PAGE), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def width(self, text, font):
        return self.d.textlength(text, font=font)

    def split(self, text, font, limit):
        """Greedy word wrap; returns a list of lines."""
        lines, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            if self.width(trial, font) <= limit or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def lines(self, x, y, text, font, limit, step, colour=INK):
        for line in self.split(text, font, limit):
            self.d.text((x, y), line, font=font, fill=colour)
            y += step
        return y

    def head_lines(self, x, y, lines, font, step, colour=INK):
        """Headline from explicit lines (no wrapping surprises)."""
        for line in lines:
            self.d.text((x, y), line, font=font, fill=colour)
            y += step
        return y

    def centred(self, y, text, font, colour=INK):
        w = self.width(text, font)
        self.d.text(((PAGE - w) / 2, y), text, font=font, fill=colour)
        return y

    def hrule(self, x0, x1, y, weight=2, colour=INK):
        self.d.line([(x0, y), (x1, y)], fill=colour, width=weight)

    def kicker(self, x, y, text, colour=RUST, size=17):
        self.d.text((x, y), text, font=sans_bold(size), fill=colour)
        return y + size + 8



# --- spot illustrations ---------------------------------------------------
# Each takes (draw, (x, y, w, h)) and draws a flat silhouette inside it.


def art_cyclone(d, box):
    x, y, w, h = box
    d.rectangle([x, y, x + w, y + h], fill=SEA)
    # sandy coastline, diagonal
    d.polygon([(x + w * 0.62, y), (x + w, y), (x + w, y + h),
               (x + w * 0.42, y + h)], fill=SAND)
    cx, cy = x + w * 0.42, y + h * 0.48
    for r, lw in ((96, 10), (72, 9), (48, 8)):
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 130, fill=IVORY, width=lw)
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=NAVY)
    d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=PAPER)


def art_jet(d, box):
    x, y, w, h = box
    # fuselage: long bar with a rounded nose, in profile
    d.rectangle([x + 6, y + h * 0.44, x + w * 0.80, y + h * 0.56],
                fill=NAVY)
    d.ellipse([x + w * 0.74, y + h * 0.42, x + w * 0.96, y + h * 0.58],
              fill=NAVY)
    # swept wing below the fuselage
    d.polygon([(x + w * 0.34, y + h * 0.54), (x + w * 0.52, y + h * 0.92),
               (x + w * 0.66, y + h * 0.92), (x + w * 0.52, y + h * 0.56)],
              fill=NAVY)
    # tail fin at the rear
    d.polygon([(x + w * 0.10, y + h * 0.46), (x + w * 0.18, y + h * 0.14),
               (x + w * 0.28, y + h * 0.14), (x + w * 0.26, y + h * 0.46)],
              fill=NAVY)
    # cabin windows
    for i in range(4):
        wx = x + w * (0.30 + i * 0.10)
        d.ellipse([wx, y + h * 0.47, wx + 5, y + h * 0.52], fill=IVORY)
    # rust hourglass, top right, clear of the jet: time running out
    hx = x + w * 0.76
    hy = y + h * 0.04
    d.polygon([(hx, hy), (hx + 26, hy), (hx + 13, hy + 15)], fill=RUST)
    d.polygon([(hx, hy + 30), (hx + 26, hy + 30), (hx + 13, hy + 15)],
              fill=RUST)
    d.ellipse([hx + 8, hy + 22, hx + 18, hy + 28], fill=LEMON)


def art_document(d, box):
    x, y, w, h = box
    # ivory sheet with a folded corner
    d.polygon([(x + 6, y + 4), (x + w - 22, y + 4), (x + w - 6, y + 20),
               (x + w - 6, y + h - 4), (x + 6, y + h - 4)], fill=IVORY,
              outline=NAVY)
    d.polygon([(x + w - 22, y + 4), (x + w - 6, y + 20),
               (x + w - 22, y + 20)], fill=SAND)
    # three navy bars of text
    for i, bw in enumerate((w * 0.62, w * 0.70, w * 0.48)):
        d.rectangle([x + 14, y + 18 + i * 14, x + 14 + bw, y + 26 + i * 14],
                    fill=NAVY)
    # teal arcs around a rust dot: nuclear risk
    cx, cy = x + w * 0.72, y + h * 0.72
    for r in (26, 18):
        d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=TEAL, width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RUST)


def art_embassy(d, box):
    x, y, w, h = box
    # two navy facades with peaked roofs and ivory windows
    for i, fx in enumerate((x + 4, x + w * 0.52)):
        fw = w * 0.44
        d.polygon([(fx, y + h * 0.30), (fx + fw / 2, y + h * 0.08),
                   (fx + fw, y + h * 0.30)], fill=NAVY)
        d.rectangle([fx, y + h * 0.30, fx + fw, y + h - 4], fill=NAVY)
        for wy in (y + h * 0.42, y + h * 0.62):
            for wx in (fx + fw * 0.18, fx + fw * 0.58):
                d.ellipse([wx, wy, wx + fw * 0.24, wy + h * 0.14],
                          fill=IVORY)
    # rust zigzag cracking the left facade
    zx = x + w * 0.26
    d.line([(zx, y + h * 0.30), (zx - 12, y + h * 0.48),
            (zx + 10, y + h * 0.62), (zx - 10, y + h * 0.80)],
           fill=RUST, width=6)


def art_table(d, box):
    x, y, w, h = box
    # teal oval conference table, navy chairs, ivory papers
    d.ellipse([x + 6, y + h * 0.34, x + w - 6, y + h * 0.66], fill=TEAL)
    for cx in (x + w * 0.16, x + w * 0.38, x + w * 0.62, x + w * 0.84):
        d.ellipse([cx - 9, y + h * 0.10, cx + 9, y + h * 0.30], fill=NAVY)
    d.polygon([(x + w * 0.30, y + h * 0.44), (x + w * 0.46, y + h * 0.44),
               (x + w * 0.46, y + h * 0.56), (x + w * 0.30, y + h * 0.56)],
              fill=IVORY)
    d.polygon([(x + w * 0.56, y + h * 0.44), (x + w * 0.72, y + h * 0.44),
               (x + w * 0.72, y + h * 0.56), (x + w * 0.56, y + h * 0.56)],
              fill=IVORY)
    d.ellipse([x + w * 0.44, y + h * 0.74, x + w * 0.56, y + h * 0.90],
              fill=NAVY)


def art_probe(d, box):
    x, y, w, h = box
    # faceted rust asteroid, left, with crater dots
    d.polygon([(x + 10, y + h * 0.42), (x + w * 0.26, y + h * 0.30),
               (x + w * 0.38, y + h * 0.46), (x + w * 0.34, y + h * 0.78),
               (x + w * 0.16, y + h * 0.86), (x + w * 0.06, y + h * 0.64)],
              fill=RUST)
    d.polygon([(x + w * 0.14, y + h * 0.46), (x + w * 0.24, y + h * 0.42),
               (x + w * 0.28, y + h * 0.56), (x + w * 0.18, y + h * 0.60)],
              fill=(196, 90, 60))
    d.ellipse([x + w * 0.20, y + h * 0.62, x + w * 0.25, y + h * 0.70],
              fill=(196, 90, 60))
    # navy probe body with flat teal solar wings, right
    bx, by = x + w * 0.62, y + h * 0.34
    d.rectangle([bx - 34, by + 8, bx - 4, by + 18], fill=TEAL)
    d.rectangle([bx + 30, by + 8, bx + 60, by + 18], fill=TEAL)
    d.rectangle([bx, by, bx + 26, by + 26], fill=NAVY)
    d.arc([bx + 6, by - 16, bx + 32, by + 8], 200, 340, fill=NAVY, width=4)
    # bold arc passing beside the asteroid, never touching it
    d.arc([x + w * 0.30, y - h * 0.10, x + w * 0.95, y + h * 0.95], 250, 80,
          fill=NAVY, width=4)


def art_scales(d, box):
    x, y, w, h = box
    # navy scales: post, crossbar, two hanging pans, base
    px = x + w * 0.30
    d.rectangle([px - 3, y + h * 0.10, px + 3, y + h * 0.82], fill=NAVY)
    d.line([(x + w * 0.06, y + h * 0.22), (x + w * 0.54, y + h * 0.22)],
           fill=NAVY, width=4)
    for cx in (x + w * 0.06, x + w * 0.54):
        d.line([(cx, y + h * 0.22), (cx, y + h * 0.46)], fill=NAVY, width=3)
        d.pieslice([cx - 16, y + h * 0.46, cx + 16, y + h * 0.70], 0, 180,
                   fill=NAVY)
    d.rectangle([px - 22, y + h * 0.82, px + 22, y + h * 0.90], fill=NAVY)
    # teal speech bubble, right: the reaction is the Friday news
    bx0, by0 = x + w * 0.66, y + h * 0.08
    d.ellipse([bx0, by0, bx0 + w * 0.28, by0 + h * 0.42], fill=TEAL)
    d.polygon([(bx0 + 8, by0 + h * 0.34), (bx0 - 2, by0 + h * 0.58),
               (bx0 + 20, by0 + h * 0.38)], fill=TEAL)


# --- page -----------------------------------------------------------------

def build():
    s = Sheet()
    d = s.d
    x0, x1 = MARGIN, PAGE - MARGIN

    # masthead
    s.centred(24, "THE WORLD TODAY", serif(76))
    s.centred(106, "Friday, 20 November 2026", sans_bold(26), colour=FAINT)
    s.hrule(x0, x1, 142, weight=4)
    s.hrule(x0, x1, 150, weight=1, colour=RULEC)

    # --- lead: cyclone ----------------------------------------------------
    ly = 166
    s.kicker(x0, ly, "LANDFALL TODAY  ·  INDIA")
    s.head_lines(x0, ly + 28, ["CYCLONE AKVAN", "DUE ASHORE", "TODAY"],
                 sans_bold(43), 48)
    art_cyclone(d, (x0 + 566, ly + 28, 390, 262))
    s.lines(x0, ly + 28 + 3 * 48 + 8,
            "The storm is due ashore near Gopalpur, Odisha, around "
            "noon IST on Friday, with winds of 90–100 km/h. More than "
            "300,000 evacuated.",
            sans(20), 536, 26)
    s.hrule(x0, x1, 458, weight=1, colour=RULEC)

    # --- second row: Trump + Shenzhen (halves) ----------------------------
    ry = 474
    half = (CONTENT - GUTTER) // 2
    gx = x0 + half + GUTTER
    s.kicker(x0, ry, "WASHINGTON  ·  IRAN")
    s.head_lines(x0, ry + 28, ["TRUMP: NO RUSH", "ON IRAN"],
                 sans_bold(28), 32)
    s.lines(x0, ry + 96,
            "Aboard Air Force One on Thursday, Trump said he was in no "
            "hurry to decide on Iran, and would discuss it after the "
            "start of 2027.",
            sans(17), 300, 22)
    art_jet(d, (x0 + 308, ry + 90, 158, 122))

    d.line([(gx - 12, ry), (gx - 12, ry + 190)], fill=RULEC, width=1)
    s.kicker(gx, ry, "SHENZHEN  ·  NUCLEAR")
    s.head_lines(gx, ry + 28, ["SHENZHEN", "DECLARATION OUT"],
                 sans_bold(28), 32)
    s.lines(gx, ry + 96,
            "The declaration's text was published on Friday, calling "
            "for talks to reduce nuclear risk. It does not mention "
            "Ukraine or Iran.",
            sans(17), 300, 22)
    art_document(d, (gx + 308, ry + 90, 158, 122))
    s.hrule(x0, x1, 688, weight=1, colour=RULEC)

    # --- bottom row: Kyiv + Hayabusa2 + ICJ (thirds) ----------------------
    by = 704
    bw = (CONTENT - 2 * GUTTER) // 3
    c1, c2, c3 = x0, x0 + bw + GUTTER, x0 + 2 * bw + 2 * GUTTER

    s.kicker(c1, by, "KYIV  ·  UKRAINE", size=15)
    s.head_lines(c1, by + 24, ["KYIV STRIKES HIT", "TWO EMBASSIES"],
                 sans_bold(23), 26)
    art_embassy(d, (c1, by + 82, bw, 74))
    s.lines(c1, by + 166,
            "One killed in Kyiv on Thursday as strikes hit the "
            "Austrian and Dutch embassies. On Friday, the EU said it "
            "would summon Russia's envoy.",
            sans(17), bw, 22)

    d.line([(c2 - 12, by), (c2 - 12, by + 258)], fill=RULEC, width=1)
    s.kicker(c2, by, "SPACE  ·  JAPAN", size=15)
    s.head_lines(c2, by + 24, ["HAYABUSA2 DROPS", "LANDING PLAN"],
                 sans_bold(23), 26)
    art_probe(d, (c2, by + 82, bw, 74))
    s.lines(c2, by + 166,
            "Engine trouble forced Japan's asteroid probe to revise "
            "its mission. The planned touchdown is off, a Friday "
            "report says.",
            sans(17), bw, 22)

    d.line([(c3 - 12, by), (c3 - 12, by + 258)], fill=RULEC, width=1)
    s.kicker(c3, by, "THE HAGUE  ·  JUSTICE", size=15)
    s.head_lines(c3, by + 24, ["ROHINGYA CHEER", "GENOCIDE VERDICT"],
                 sans_bold(23), 26)
    art_scales(d, (c3, by + 82, bw, 74))
    s.lines(c3, by + 166,
            "The UN's top court found Myanmar responsible for genocide "
            "on Thursday. Refugees cheered; reparations were ordered.",
            sans(17), bw, 22)

    # --- footer -----------------------------------------------------------
    s.hrule(x0, x1, by + 258, weight=2)
    foot = "Friday 20 November 2026 — world news in one page."
    s.centred(by + 268, foot, sans(16), colour=FAINT)

    s.img.save(OUT, format="PNG", optimize=True)
    print("wrote", OUT, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    build()
