# Phase 1 Data Model: Floor Tile Pagination Generator

The prototype is in-memory only; these "entities" are simple value structures
(plain objects/dataclasses or dicts) used during a single run. No persistence
beyond the output image file.

## Entity: LayoutConfig

The complete set of validated parameters for one run.

| Field | Type | Validation |
|-------|------|------------|
| `unit` | enum: `centimeters` \| `meters` \| `millimeters` | Must be one of the three accepted values (FR-002). |
| `rows` | int | Derived from grid size; 2 or 3 (FR-003). |
| `cols` | int | Derived from grid size; 2 or 3 (FR-003). |
| `positions` | list[TilePosition] | Exactly `rows × cols` entries, one per cell (FR-004). |
| `tile_height` | float | Physical tile height in `unit`, > 0 (FR-007). |
| `tile_width` | float | Physical tile width in `unit`, > 0 (FR-007). |
| `grout_size` | float | Grout thickness in `unit`, ≥ 0 (FR-009). |
| `grout_color` | str \| None | `#RRGGBB`; present iff `grout_size > 0` (FR-012/FR-013). |
| `output_path` | str | User-supplied destination path for the PNG (FR-019). |

**Accepted grid sizes** (FR-003): `2x2`, `2x3`, `3x2`, `3x3`. Reject everything
else (e.g., `3x4`, `5x5`). Grid string format is `ROWSxCOLS` (height × width).

## Entity: TilePosition

One cell in the grid and its source image.

| Field | Type | Validation |
|-------|------|------------|
| `row` | int | 1-based row index (1..rows). |
| `col` | int | 1-based column index (1..cols). |
| `image_path` | str | File must exist and be readable (FR-006); extension in {png, jpg, jpeg} (FR-005). |

Positions are requested in reading order: 1x1, 1x2, …, 2x1, … (FR-004). The
position `1x1` image is the **reference** (see DerivedValues).

## Entity: Grout

Internal + border spacing between tiles.

| Field | Type | Notes |
|-------|------|-------|
| `size` | float | In `unit`; from `LayoutConfig.grout_size`. |
| `color` | str \| None | `#RRGGBB` when `size > 0`, else None. |
| `pixels_w` | int | `round(size × ratio_w)` (FR-010). |
| `pixels_h` | int | `round(size × ratio_h)`. |

## Entity: GeneratedLayout

The composed output.

| Field | Type | Notes |
|-------|------|-------|
| `width_px` | int | `cols × (cell_w + grout.pixels_w)` (FR-011). |
| `height_px` | int | `rows × (cell_h + grout.pixels_h)`. |
| `image` | Pillow Image | RGB canvas filled with grout color, tiles pasted in. |

## Derived values

- `cell_w`, `cell_h`: pixel dimensions of the reference image (position 1x1).
- `ratio_w = cell_w / tile_width`, `ratio_h = cell_h / tile_height` (FR-008).
- All non-reference images are resized to `(cell_w, cell_h)` before pasting
  (FR-018).

## Validation summary (maps to functional requirements)

- Unit ∈ {centimeters, meters, millimeters} — FR-002
- Grid ∈ {2x2, 2x3, 3x2, 3x3} — FR-003
- Image extension ∈ {png, jpg, jpeg} — FR-005
- Image file exists/readable — FR-006
- `grout_size ≥ 0`; color required only when `> 0` — FR-009/FR-012/FR-013
- `grout_color` matches `#RRGGBB` — FR-012
- Any invalid value triggers a clear message + re-prompt, never a crash — FR-017
