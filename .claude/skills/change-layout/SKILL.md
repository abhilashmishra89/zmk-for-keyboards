---
name: change-layout
description: Change the Corne keyboard layout end to end - edit the ZMK keymap, keep the picture, PDF cheat sheet and README in sync, push, build the firmware on GitHub and flash it onto the keyboard. Use whenever the user wants to move, add, remove or swap keys, layers or shortcuts on this keyboard, or asks to reflash it.
---

# Change the Corne layout

The user is not a keyboard expert. Keep messages short: say what changes, then do the hands-on work yourself. Never leave the keymap, picture, PDF and README out of sync.

## 0. Setup (only if `.venv/` is missing)

```sh
python3 -m venv .venv
.venv/bin/pip install keymap-drawer "tree-sitter==0.23.2" "tree-sitter-devicetree<0.15" reportlab pypdf
```

The tree-sitter pins matter: newer combinations break `keymap parse`.

Run `git pull --rebase` first: a bot pushes a redrawn picture after every keymap push.

## 1. Agree on the change

- Restate the change as a small before/after grid of only the affected keys. If the request is ambiguous (which layer? replace or add?), ask one short question.
- Physical positions (42 keys), the same on every layer:
  ```
  Row 0:  0  1  2  3  4  5    6  7  8  9  10 11
  Row 1: 12 13 14 15 16 17   18 19 20 21 22 23
  Row 2: 24 25 26 27 28 29   30 31 32 33 34 35
  Thumb:          36 37 38   39 40 41
  ```
- Layers: BASE, LOWER (hold the left inner thumb), RAISE (hold the right inner thumb), ADJUST (LOWER+RAISE, a conditional layer).
- Keep modifiers and thumbs explicit on every layer (no `&trans`), so the picture shows real names.
- Don't remove the `&bootloader` keys from ADJUST: they're how the board gets flashed without the reset button.

## 2. Edit, in this order

1. `config/corne.keymap`: the bindings, plus the layer summary comment at the top if a layer's purpose changes.
2. `scripts/make_guide.py`: the `LAYERS` tables (page 2, key grids) and the `page_usage` text (page 1). Both must match the keymap.
3. `keymap_drawer.config.yaml`: only if a new binding needs a friendlier label (e.g. `"&ext_power EP_TOG": Screen`).
4. `README.md`: the one-line layer summary near the top, if a layer's purpose changed.

## 3. Regenerate and check visually

```sh
.venv/bin/python -I scripts/make_guide.py corne-quick-guide.pdf
.venv/bin/keymap -c keymap_drawer.config.yaml parse -z config/corne.keymap > .venv/corne.yaml
.venv/bin/keymap -c keymap_drawer.config.yaml draw .venv/corne.yaml > corne_keymap.svg
mkdir -p .venv/preview
.venv/bin/python -I -c "from pypdf import PdfReader,PdfWriter;import sys;w=PdfWriter();w.add_page(PdfReader(sys.argv[1]).pages[1]);w.write(sys.argv[2])" corne-quick-guide.pdf .venv/preview/p2.pdf
qlmanage -t -s 1400 -o .venv/preview .venv/preview/p2.pdf corne-quick-guide.pdf >/dev/null 2>&1
```

Read both PNGs in `.venv/preview/` and confirm every changed key looks right. Check each layer has 42 keys (`.venv/corne.yaml`).

## 4. Publish

```sh
cp corne-quick-guide.pdf ~/Desktop/corne-quick-guide.pdf
git add -A config scripts keymap_drawer.config.yaml README.md corne_keymap.svg corne-quick-guide.pdf
git commit -m "feat: <what moved>"
git push
gh run list -R abhilashmishra89/zmk-for-keyboards --workflow "Build ZMK firmware" --limit 1
```

The commit email must be the repo-local one already configured; don't change git identity. Never push any branch other than `zmk-for-corne`.

## 5. Flash

- **Keymap-only changes** (most changes): only the **left** half needs flashing, since the keymap lives there. Use `left`.
- **Changes that affect each half** (screens, power, per-half behaviours, Kconfig): flash both, left then right. Use `both`.

Start the flasher in the background (`run_in_background`) with the build run id:

```sh
scripts/flash.sh <run-id> left    # or: both
```

Then tell the user, briefly:
1. Plug in the **left half** only, and **double-tap its reset button**. It's fine to do this before the build finishes; the board waits.
2. For `both`: once you confirm the left half is done, tell them to **unplug it**, plug in the right half and double-tap its reset button.

When the output shows `done`, check `ioreg -p IOUSB -l -w0 | grep '"USB Product Name" = "Corne"'` to confirm the board restarted.

## 6. Verify with the user

Suggest a concrete test in a text box or at https://www.keyboardtester.com/tester.html. F-keys from an external keyboard show nothing visible on macOS, so use the tester for those.

## Troubleshooting

- **Boot key (LOWER+RAISE+Z) does nothing:** the right half must be on, because RAISE is there. Use the reset double-tap instead.
- **Mac doesn't see the half at all:** the cable is probably charge-only, or it's going through a hub. Use a data cable straight into the Mac.
- **Halves stop talking to each other:** flash `settings_reset-nice_nano__zmk-zmk.uf2` to both halves, then the normal firmware to both.
- **§ instead of `:** macOS detected the board as ISO. Fix in Keyboard settings → Change Keyboard Type → ANSI.
- **Screen stays black after the Screen key turns it back on:** power-cycle that half with its switch. This is expected with `&ext_power`.
