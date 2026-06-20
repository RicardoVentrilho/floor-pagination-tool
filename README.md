# Floor Tile Pagination Generator

A command-line floor tile pagination generator. The program interactively
collects the image for each grid position plus the floor's physical measurements,
and composes a single PNG image with proportional grout applied between and
around the tiles.

> ⚠️ Prototype. The focus is a working result that is fast to iterate on; there
> is no automated test suite (see `.specify/memory/constitution.md`).

## How it works

- The `1x1` position image is the **reference**: its pixel size defines the cell
  size. All other images are resized to that size.
- The **ratio** (pixel ↔ physical measure proportion) is `image pixels ÷ physical
  tile size`, computed per axis.
- The **grout in pixels** is `grout size × ratio`, rounded.
- The final size per axis is `n × (cell_px + grout_px)`, where `n` is the number
  of tiles on that axis. The grout is drawn as the canvas background (between the
  tiles and on the outer border).

### Examples

| Unit | Grid | Tile | Image | Grout | ratio | grout_px | Output |
|------|------|------|-------|-------|-------|----------|--------|
| mm | 2x2 | 1000×1000 | 150×150 | 1.5 | 0.15 | round(0.225) = 0 | 300×300 |
| cm | 2x2 | 100×100 | 150×150 | 2 | 1.5 | round(3.0) = 3 | 306×306 |

When the grout rounds to 0, the tiles sit edge to edge (no spacing).

## Requirements

- Python 3.10+
- Pillow

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

The program asks, in sequence:

1. **Unit of measure**: `centimeters`, `meters` or `millimeters`
2. **Grid size**: `2x2`, `2x3`, `3x2` or `3x3` (format `rows x columns`)
3. **Image path** for each position (`png`, `jpg` or `jpeg`), in reading order
   (`1x1`, `1x2`, …)
4. **Height** and **width** of the tile (in the chosen unit)
5. **Grout thickness** (in the chosen unit)
6. **Grout color** in hexadecimal `#RRGGBB` — *only requested if the grout is
   greater than zero*
7. **Output PNG file path**

A summary is then displayed and confirmation is requested (`yes`/`no`). Only with
`yes` is the file generated (overwrites if it already exists); with `no` nothing
is written.

### Sample session

```
Floor Tile Pagination Generator
Units: centimeters, meters, millimeters
Grids: 2x2, 2x3, 3x2, 3x3
Images: png, jpg, jpeg

Unit of measure (centimeters/meters/millimeters): centimeters
Grid size (2x2, 2x3, 3x2, 3x3): 2x2
Imagem 1x1 path (png/jpg/jpeg): ./image1.png
Imagem 1x2 path (png/jpg/jpeg): ./image2.png
Imagem 2x1 path (png/jpg/jpeg): ./image3.png
Imagem 2x2 path (png/jpg/jpeg): ./image4.png
Tile height in centimeters: 100
Tile width in centimeters: 100
Grout thickness in centimeters: 2
Grout color (#RRGGBB): #CECECE
Output PNG path: out_cm.png

Summary
...
Generate this layout? (yes/no): yes
Saved to out_cm.png
```

## Validation

Every invalid input is rejected with a message and re-prompted (without exiting
the program): a grid outside the allowed set, an unknown unit, an image format
other than png/jpg/jpeg, a non-existent file, an invalid number, and a color
outside the `#RRGGBB` pattern.

## Structure

```
main.py            # Console flow: prompts, validation, summary and confirmation
pagination.py      # Composition logic: ratio, grout in pixels and assembly (Pillow)
requirements.txt   # Pillow
specs/             # Specification, plan and tasks (Spec Kit)
```

## License

See [LICENSE](./LICENSE).
