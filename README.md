# Corne ZMK Keymap

Keyboard and original firmware config by [PARIX](https://parix.in/products/corne-choc-wireless-custom-low-profile-split-keyboard).

Split ergonomic keyboard (42 keys) running [ZMK firmware](https://zmk.dev) on Nice!Nano v2.
Simple Mac laptop-style layout: plain QWERTY, dedicated Cmd/Opt/Ctrl/Shift, and three extra layers
(LOWER: F-keys/arrows/media, RAISE: numbers/symbols, LOWER+RAISE: Bluetooth/screen on-off/Boot).
Printable cheat sheet: [`corne-quick-guide.pdf`](corne-quick-guide.pdf); one-page A4 print of BASE/RAISE/LOWER: [`corne-print-a4.pdf`](corne-print-a4.pdf).

## Keymap

Auto-generated from [`config/corne.keymap`](config/corne.keymap) via [keymap-drawer](https://github.com/caksoylar/keymap-drawer):

![Keymap](corne_keymap.svg)

The SVG updates automatically on push via the [Draw Keymap](.github/workflows/draw-keymap.yml) workflow.

## Display

- **Left (central):** Built-in ZMK status screen (layer, battery, BT)
- **Right (peripheral):** Custom P keycap logo with glitch effects + battery + BT status
- **Screens off / on:** LOWER + RAISE + H turns them off, + J turns them on. After turning back on, a screen may stay black until that half is switched off and on.

## Build Firmware

Push to `config/` or `build.yaml` triggers the [Build ZMK firmware](.github/workflows/build.yml) workflow. Download `.uf2` files from Actions artifacts.

To flash a half: hold LOWER + RAISE and press Boot (Z on the left half, / on the right half),
or double-tap its reset button, then drag that half's `.uf2` onto the NICENANO drive.

## Regenerate Keymap SVG

```sh
make install   # one-time: pip install keymap-drawer
make svg       # parse + render SVG
```

## Regenerate the PDF cheat sheet

Edit the layer tables in [`scripts/make_guide.py`](scripts/make_guide.py) to match the keymap, then:

```sh
pip install reportlab
python3 scripts/make_guide.py corne-quick-guide.pdf
```

## Hardware

- **Board:** Nice!Nano v2 (nRF52840)
- **Shield:** Corne (split, 6x3+3)
- **Display:** OLED SSD1306 128x32 / Nice!View
- **RGB:** firmware supports 27 WS2812 LEDs, but none are fitted on this board
- **Bluetooth:** 4 profiles
- **ZMK Studio:** Enabled
- **Mouse/Pointing:** enabled in firmware, no mouse keys in the keymap
