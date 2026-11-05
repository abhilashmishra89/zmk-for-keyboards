# ZMK Keymap Visualizer
# Reusable Makefile for generating keymap visuals from any ZMK config
#
# Usage:
#   make install    - Install dependencies (keymap-drawer)
#   make svg        - Generate SVG from keymap
#   make all        - Install + generate SVG + open it
#   make clean      - Remove generated files
#
# Override for other keyboards:
#   make svg KEYMAP=config/my_board.keymap OUT_DIR=build

# --- Configuration (override these for different keyboards) ---
KEYMAP      ?= config/corne.keymap
OUT_DIR     ?= .
BOARD_NAME  ?= $(basename $(notdir $(KEYMAP)))
SVG_FILE    ?= $(OUT_DIR)/$(BOARD_NAME)_keymap.svg
YAML_FILE   ?= /tmp/$(BOARD_NAME)_keymap.yaml
BROWSER     ?= Google Chrome

# --- Python / pip detection ---
PYTHON      := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)
PIP         := $(shell command -v pip3 2>/dev/null || command -v pip 2>/dev/null)
KEYMAP_DRAW := $(shell command -v keymap 2>/dev/null)

.PHONY: all install svg open clean check-deps help

all: install svg open

help:
	@echo "ZMK Keymap Visualizer"
	@echo ""
	@echo "Targets:"
	@echo "  make install     Install keymap-drawer via pip"
	@echo "  make svg         Parse keymap and generate SVG"
	@echo "  make open        Open the SVG"
	@echo "  make clean       Remove generated SVG and YAML"
	@echo "  make all         install + svg + open"
	@echo ""
	@echo "Variables (override for other boards):"
	@echo "  KEYMAP=$(KEYMAP)"
	@echo "  BOARD_NAME=$(BOARD_NAME)"
	@echo "  OUT_DIR=$(OUT_DIR)"
	@echo "  SVG_FILE=$(SVG_FILE)"

check-deps:
ifndef PYTHON
	$(error "python3 not found. Install Python 3 first.")
endif
ifndef PIP
	$(error "pip not found. Install pip first.")
endif

install: check-deps
	@echo "==> Installing keymap-drawer..."
	$(PIP) install --upgrade keymap-drawer
	@echo "==> Done."

svg: $(SVG_FILE)

$(SVG_FILE): $(KEYMAP)
	@echo "==> Parsing $(KEYMAP)..."
	keymap -c keymap_drawer.config.yaml parse -z $(KEYMAP) > $(YAML_FILE)
	@echo "==> Drawing SVG -> $(SVG_FILE)..."
	keymap -c keymap_drawer.config.yaml draw $(YAML_FILE) > $(SVG_FILE)
	@echo "==> Generated $(SVG_FILE) ($$(wc -c < $(SVG_FILE) | tr -d ' ') bytes)"

open: svg
	@echo "==> Opening SVG..."
	open -a "$(BROWSER)" $(SVG_FILE) 2>/dev/null || open $(SVG_FILE) 2>/dev/null || xdg-open $(SVG_FILE)

clean:
	@echo "==> Cleaning generated files..."
	rm -f $(SVG_FILE) $(YAML_FILE)
	@echo "==> Clean."
