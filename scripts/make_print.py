"""One A4 portrait page: BASE, RAISE and LOWER, each centred in its own third
of the page (top, middle, bottom) and as wide as the page allows.

Usage: python3 scripts/make_print.py corne-print-a4.pdf
"""
import os
import sys

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_guide import INK, MUTED, LAYERS, SHIFTED, key  # noqa: E402

PAGE_W, PAGE_H = A4
MARGIN = 10 * mm
LAYOUT_W = PAGE_W - 2 * MARGIN

# 12 key columns, 11 gaps and the split between halves must add up to LAYOUT_W
GAP_RATIO, SPLIT_RATIO = 0.08, 0.8
K = LAYOUT_W / (12 + 11 * GAP_RATIO + SPLIT_RATIO)
GAP, SPLIT = K * GAP_RATIO, K * SPLIT_RATIO
TITLE_H = 18
BLOCK_H = TITLE_H + 4 * K + 3 * GAP   # title + 3 key rows + thumb row

PRINTED = [  # (layer name in LAYERS, title on the page)
    ("BASE", "BASE - normal typing"),
    ("RAISE", "RAISE - hold RAISE (right thumb, innermost)"),
    ("LOWER", "LOWER - hold LOWER (left thumb, innermost)"),
]


def draw_layout(c, ox, top, title, held, rows, shifted):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(ox, top - 11, title)
    y = top - TITLE_H - K
    for r in rows[:3]:
        for i, label in enumerate(r):
            x = ox + i * (K + GAP) + (SPLIT if i >= 6 else 0)
            key(c, x, y, K, K, label, held or set(), (shifted or {}).get(label))
        y -= K + GAP
    # thumbs sit under columns 3-5 (left) and 6-8 (right)
    for i, label in enumerate(rows[3]):
        col = 3 + i
        x = ox + col * (K + GAP) + (SPLIT if col >= 6 else 0)
        key(c, x, y, K, K, label, held or set())


def main(out):
    by_name = {title.split(" ")[0]: (held, rows) for title, held, rows in LAYERS}
    c = canvas.Canvas(out, pagesize=A4)
    c.setTitle("Corne Layout - Print")
    ox = (PAGE_W - LAYOUT_W) / 2
    third = PAGE_H / 3
    for n, (name, title) in enumerate(PRINTED):
        held, rows = by_name[name]
        # centre each layout vertically in its third of the page
        top = PAGE_H - n * third - (third - BLOCK_H) / 2
        draw_layout(c, ox, top, title, held, rows, SHIFTED if name == "BASE" else None)
    c.setFont("Helvetica", 7)
    c.setFillColor(MUTED)
    c.drawCentredString(PAGE_W / 2, 14, "Small grey symbol = with Shift.  Orange = the key you hold.")
    c.showPage()
    c.save()


if __name__ == "__main__":
    main(sys.argv[1])
