# Quickstart & Validation: Floor Tile Pagination Generator

How to run the tool and validate it works end to end. (Prototype — validation is
manual; there is no automated test suite per the project constitution.)

## Prerequisites

- Python 3.10+
- Pillow

```bash
pip install -r requirements.txt   # contains: Pillow
```

## Run

```bash
python main.py
```

Follow the interactive prompts (see [contracts/cli.md](./contracts/cli.md) for
the exact sequence and accepted values).

## Validation Scenario 1 — millimeters, grout rounds to 0 (→ 300×300)

Prepare four 150×150 px PNG images. Then run and answer:

- Unit: `millimeters`
- Grid: `2x2`
- 1x1 / 1x2 / 2x1 / 2x2: paths to the four PNGs
- Tile height: `1000`, Tile width: `1000`
- Grout: `1.5`, Color: `#CECECE`
- Output path: `out_mm.png`
- Confirm: `yes`

**Expected**: `out_mm.png` is created at **300×300 px** (grout 1.5 × 0.15 = 0.225
→ rounds to 0, so tiles sit edge to edge). Verify with:

```bash
python -c "from PIL import Image; print(Image.open('out_mm.png').size)"
# -> (300, 300)
```

## Validation Scenario 2 — centimeters, 3px grout (→ 306×306)

Same four 150×150 px PNGs. Run and answer:

- Unit: `centimeters`
- Grid: `2x2`
- four image paths
- Tile height: `100`, Tile width: `100`
- Grout: `2`, Color: `#CECECE`
- Output path: `out_cm.png`
- Confirm: `yes`

**Expected**: `out_cm.png` is **306×306 px** (grout 2 × 1.5 = 3 px;
2 × (150 + 3) = 306), with `#CECECE` grout visible between/around the tiles.

```bash
python -c "from PIL import Image; print(Image.open('out_cm.png').size)"
# -> (306, 306)
```

## Validation Scenario 3 — input validation

While running, confirm each is rejected with a clear message and re-prompts
(does not crash):

- Grid `3x4` or `5x5` → rejected (only 2x2, 2x3, 3x2, 3x3 allowed)
- Unit `inches` → rejected
- An image path ending in `.gif` → rejected (only png/jpg/jpeg)
- A non-existent image path → "file not found", re-prompt
- Grout color `ZZZZZZ` (with grout > 0) → rejected

## Validation Scenario 4 — zero grout

- Grout: `0` → the program must **not** ask for a color, and the output has no
  spacing between tiles (2×2 of 150 px → 300×300).

## Validation Scenario 5 — decline confirmation

- Answer `no` at the summary → no output file is written.

## Validation Scenario 6 — larger grid

- Grid `3x3` with nine images → program asks for exactly nine paths and produces
  a 3×3 layout sized `3 × (cell + grout_px)` per axis.
