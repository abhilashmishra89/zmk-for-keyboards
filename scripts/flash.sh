#!/bin/sh
# Wait for a firmware build, download it, then flash halves as they appear
# in bootloader mode (the NICENANO drive).
#
# Usage: scripts/flash.sh <run-id> left|both|reset-both
#   left       - keymap-only changes (the keymap lives on the left/central half)
#   both       - changes that affect each half (displays, power, etc.); left first, then right
#   reset-both - clear saved settings (incl. Bluetooth pairing) and reflash:
#                left settings_reset, left firmware, right settings_reset, right firmware.
#                Each step needs its own reset double-tap.

set -u
RUN="${1:?usage: scripts/flash.sh <run-id> left|both|reset-both}"
WHICH="${2:-left}"
REPO=abhilashmishra89/zmk-for-keyboards
DIR="$HOME/Downloads/corne-firmware-$RUN"

gh run watch "$RUN" -R "$REPO" --exit-status >/dev/null 2>&1 || { echo "BUILD FAILED: gh run view $RUN -R $REPO --log-failed"; exit 1; }
if [ ! -d "$DIR" ]; then
    gh run download "$RUN" -R "$REPO" -n firmware -D "$DIR" || exit 1
fi
echo "firmware ready in $DIR"

flash() {
    file="$DIR/$1-nice_nano__zmk-zmk.uf2"
    [ -f "$file" ] || { echo "missing $file"; return 1; }
    i=0
    while [ $i -lt 1500 ]; do
        if [ -d /Volumes/NICENANO ]; then
            sleep 2
            echo "--- $1: bootloader found, copying"
            # an "extended attributes / Device not configured" error is normal: the drive ejects itself
            cp "$file" /Volumes/NICENANO/ 2>&1
            j=0
            while [ -d /Volumes/NICENANO ] && [ $j -lt 30 ]; do sleep 1; j=$((j + 1)); done
            echo "--- $1: done"
            return 0
        fi
        sleep 1
        i=$((i + 1))
    done
    echo "TIMEOUT waiting for $1 (25 min)"
    return 1
}

case "$WHICH" in
    left) flash corne_left ;;
    both) flash corne_left && flash corne_right ;;
    reset-both)
        flash settings_reset && echo ">>> LEFT: double-tap reset again for the firmware" &&
        flash corne_left && echo ">>> unplug LEFT, plug in RIGHT, double-tap reset" &&
        flash settings_reset && echo ">>> RIGHT: double-tap reset again for the firmware" &&
        flash corne_right ;;
    *) echo "unknown mode: $WHICH"; exit 1 ;;
esac
