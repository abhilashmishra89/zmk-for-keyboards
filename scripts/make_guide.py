import sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white

OUT = sys.argv[1]
W, H = landscape(letter)

INK = HexColor("#1f2933")
MUTED = HexColor("#6b7280")
MOD = HexColor("#dbeafe")      # modifiers
LAYER = HexColor("#fde68a")    # layer keys
HELD = HexColor("#f59e0b")     # key you are holding
EMPTY = HexColor("#f3f4f6")
NORMAL = white

MODS = {"Ctrl", "Shift", "Opt", "Cmd"}
# what Shift + key gives, drawn small in the corner on the BASE layer
SHIFTED = {";": ":", "'": '"', ",": "<", ".": ">", "/": "?"}

LAYERS = [
    ("BASE - normal typing", None, [
        ["Tab", "Q", "W", "E", "R", "T",   "Y", "U", "I", "O", "P", "Bksp"],
        ["Ctrl", "A", "S", "D", "F", "G",  "H", "J", "K", "L", ";", "'"],
        ["Shift", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "Shift"],
        ["Opt", "Cmd", "LOWER",            "RAISE", "Space", "Enter"],
    ]),
    ("LOWER - hold LOWER (left thumb, innermost)", {"LOWER"}, [
        ["Esc", "F1", "F2", "F3", "F4", "F5",      "F6", "F7", "F8", "F9", "F10", "Bksp"],
        ["Ctrl", "Vol-", "Vol+", "Mute", "Bri-", "Bri+", "Left", "Up", "Down", "Right", "F11", "Del"],
        ["Shift", "Prev", "Play", "Next", "", "",  "PgUp", "PgDn", "Home", "End", "F12", "Shift"],
        ["Opt", "Cmd", "LOWER",                    "RAISE", "Space", "Enter"],
    ]),
    ("RAISE - hold RAISE (right thumb, innermost)", {"RAISE"}, [
        ["`", "1", "2", "3", "4", "5",    "6", "7", "8", "9", "0", "Del"],
        ["Ctrl", "!", "@", "#", "$", "%",  "^", "&", "*", "(", ")", "~"],
        ["Shift", "-", "=", "[", "]", "\\", "_", "+", "{", "}", "|", "Shift"],
        ["Opt", "Cmd", "LOWER",           "RAISE", "Space", "Enter"],
    ]),
    ("ADJUST - hold LOWER + RAISE together", {"LOWER", "RAISE"}, [
        ["", "", "", "", "", "",                          "", "", "", "", "", ""],
        ["BT 0", "BT 1", "BT 2", "BT 3", "BT clr", "",     "Screen", "", "", "", "", ""],
        ["USB/BT", "Boot", "", "", "", "",                "", "", "", "", "Boot", ""],
        ["Opt", "Cmd", "LOWER",                           "RAISE", "Space", "Enter"],
    ]),
]


def key(c, x, y, w, h, label, held, shifted=None):
    if label in held:
        fill = HELD
    elif label in ("LOWER", "RAISE"):
        fill = LAYER
    elif label in MODS:
        fill = MOD
    elif label == "":
        fill = EMPTY
    else:
        fill = NORMAL
    c.setFillColor(fill)
    c.setStrokeColor(HexColor("#9ca3af"))
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)
    c.setFillColor(INK)
    size = 10
    while size > 6 and c.stringWidth(label, "Helvetica-Bold", size) > w - 4:
        size -= 0.5
    if shifted:
        c.setFillColor(MUTED)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + w / 2, y + h - 10, shifted)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", size)
        c.drawCentredString(x + w / 2, y + 5, label)
        return
    c.setFont("Helvetica-Bold", size)
    c.drawCentredString(x + w / 2, y + h / 2 - size / 3, label)


def board(c, ox, oy, title, held, rows, k=32, gap=3, split=26, shifted=None):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(ox, oy + 4, title)
    y = oy - k - 6
    for r in rows[:3]:
        for i, label in enumerate(r):
            x = ox + i * (k + gap) + (split if i >= 6 else 0)
            key(c, x, y, k, k, label, held or set(), (shifted or {}).get(label))
        y -= k + gap
    # thumbs sit under columns 3-5 (left) and 6-8 (right)
    for i, label in enumerate(rows[3]):
        col = 3 + i
        x = ox + col * (k + gap) + (split if col >= 6 else 0)
        key(c, x, y, k, k, label, held or set())


def page_keys(c):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(36, H - 44, "Corne - what every key does")
    c.setFont("Helvetica", 10)
    c.setFillColor(MUTED)
    c.drawString(36, H - 60, "Same physical keys on every layer. Hold a thumb key, then press the key shown.  "
                 "Orange = the key you hold.  Grey = does nothing.  Small grey symbol = with Shift.")
    k, gap, split = 26, 2, 14
    bw = 12 * (k + gap) + split
    cols = [36, W - 36 - bw]
    tops = [H - 96, H - 96 - 4 * (k + gap) - 52]
    for idx, (title, held, rows) in enumerate(LAYERS):
        board(c, cols[idx % 2], tops[idx // 2], title, held, rows, k, gap, split,
              SHIFTED if idx == 0 else None)


def page_usage(c):
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(36, H - 44, "Corne - how to use it")
    sections = [
        ("Normal typing", [
            "Letters, Tab, Bksp, Ctrl, Shift work like a laptop.",
            "Left thumbs: Opt, Cmd, LOWER.   Right thumbs: RAISE, Space, Enter.",
            "Cmd / Opt / Ctrl / Shift work on every layer, so Cmd + arrows etc. work.",
            "Shift + ; ' , . /  =  : \" < > ?   (same as a laptop).",
        ]),
        ("Hold LOWER  (left thumb, innermost)", [
            "Esc = LOWER + Tab key.",
            "F1-F10 on the top row.  F11 / F12 = the ; and / keys (right under F10).",
            "Arrows in a row on the right hand: Left / Up / Down / Right = H J K L keys.",
            "PgUp / PgDn / Home / End right below them (N M , . keys).  Del = LOWER + ' key.",
            "Left hand: volume, mute, screen brightness, prev / play / next.",
        ]),
        ("Hold RAISE  (right thumb, innermost)", [
            "Top row: numbers 1-0.",
            "Middle row: ! @ # $ % ^ & * ( )   (each symbol right under its number).",
            "Bottom row: - = [ ] \\  and  _ + { } |",
            "` = RAISE + Tab key.   ~ = RAISE + ' key.   Del = RAISE + Bksp key.",
        ]),
        ("Hold LOWER + RAISE together", [
            "Bluetooth: BT 0-3 = pick device slot (Ctrl A S D keys).  BT clr (F key) forgets that slot.",
            "Screens on/off = H key.  (If a screen stays blank after turning on, switch that half off and on.)",
            "Boot (Z key on left half, / key on right half) = flashing mode for that half.",
        ]),
    ]
    y = H - 84
    for head, lines in sections:
        c.setFillColor(HELD)
        c.rect(36, y - 2, 4, 16, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 13)
        c.drawString(48, y, head)
        y -= 20
        c.setFont("Helvetica", 11)
        for line in lines:
            c.drawString(48, y, "-  " + line)
            y -= 16
        y -= 14
    c.setFont("Helvetica-Oblique", 10)
    c.setFillColor(MUTED)
    c.drawString(36, y, "Key-by-key pictures of every layer are on the next page.")


c = canvas.Canvas(OUT, pagesize=landscape(letter))
c.setTitle("Corne Quick Guide")
page_usage(c)
c.showPage()
page_keys(c)
c.showPage()
c.save()
