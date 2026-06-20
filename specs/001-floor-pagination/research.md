# Phase 0 Research: Floor Tile Pagination Generator

All spec ambiguities were resolved in the Clarifications session (2026-06-20),
so there are no open `NEEDS CLARIFICATION` items. This document records the
technical decisions for the prototype.

## Decision: Image library — Pillow (PIL)

- **Decision**: Use Pillow for opening, resizing, and compositing tile images
  and for saving the output PNG.
- **Rationale**: It is the de-facto standard Python imaging library, handles
  PNG/JPG/JPEG natively, and provides `Image.open`, `Image.resize`,
  `Image.new`, and `Image.paste` — exactly the primitives needed. Hand-rolling
  raster composition would violate Principle V (Minimal Dependencies &
  Simplicity) by costing far more time than the dependency.
- **Alternatives considered**: OpenCV (heavier, BGR ordering, overkill);
  pure-Python/`numpy` pixel arrays (more code, slower to write); rejected for a
  prototype.

## Decision: Console interaction — standard library `input()`

- **Decision**: Build the guided flow with plain `input()` prompts and a
  re-prompt loop on invalid values.
- **Rationale**: No third-party CLI framework is needed for a linear,
  interactive question flow. Keeps the edit-run loop fast (Principle I).
- **Alternatives considered**: `argparse` (the requirement is interactive
  prompts, not flags); `click`/`typer` (unnecessary dependency for a prototype).

## Decision: Ratio derivation and reference image

- **Decision**: The first supplied image (position 1x1) is the reference. Its
  pixel dimensions set the tile cell size. Ratio per axis = reference image
  pixels ÷ physical tile size (height ratio from height, width ratio from
  width). All other images are resized to the reference cell size before
  compositing (per clarification "Resize to reference").
- **Rationale**: Matches the clarified spec (FR-008, FR-018) and the reference
  use cases (150 px image, 1000 mm tile → ratio 0.15; 100 cm tile → ratio 1.5).
- **Alternatives considered**: Requiring identical sizes (rejected by user);
  native per-cell sizing producing a ragged grid (rejected by user).

## Decision: Grout pixel size and rounding

- **Decision**: grout_px = round(grout_measure × ratio), computed per axis,
  using Python's built-in `round()`.
- **Rationale**: Matches both reference cases: 1.5 mm × 0.15 = 0.225 → 0 px;
  2 cm × 1.5 = 3 px. When grout_px rounds to 0, the layout is composed with no
  spacing.
- **Alternatives considered**: `math.floor`/`math.ceil` — `round()` reproduces
  the documented examples exactly.

## Decision: Layout dimensions and grout rendering

- **Decision**: Layout size per axis = n × (cell_px + grout_px). Render by
  creating a canvas of that size filled with the grout color, then pasting each
  resized tile at offset `(grout_px_w + col × (cell_w + grout_px_w),
  grout_px_h + row × (cell_h + grout_px_h))`. The grout color fill shows through
  the internal seams and the outer border; when grout_px = 0 the fill is
  irrelevant and tiles sit edge to edge.
- **Rationale**: Reproduces the authoritative 306×306 result for the 2×2 / 3 px
  case (2 × (150 + 3) = 306) and 300×300 when grout rounds to 0 (FR-011).
- **Alternatives considered**: Internal-seams-only (303 px) — explicitly
  rejected by the clarification.

## Decision: Unit of measure handling

- **Decision**: Accept centimeters, meters, millimeters as a selected unit at
  the start. All measures in a run use that unit. Because the ratio is a pure
  proportion (pixels ÷ physical), no cross-unit conversion is needed — the unit
  is informational/validation only.
- **Rationale**: Simplest correct approach (Principle II); the spec never mixes
  units within a run.
- **Alternatives considered**: Normalizing everything to millimeters internally
  — unnecessary since ratio cancels the unit.

## Decision: Hex color validation

- **Decision**: Accept `#RRGGBB` form; validate with a simple check
  (leading `#`, 6 hex digits). Only requested when grout_px-measure > 0
  (FR-012/FR-013).
- **Rationale**: Matches the `#CECECE` examples; minimal validation suffices for
  a prototype.
- **Alternatives considered**: Supporting `#RGB` shorthand or named colors —
  out of scope.

## Decision: Output format and destination

- **Decision**: Save a PNG to a user-supplied output path (FR-019); overwrite if
  the file already exists.
- **Rationale**: Matches the clarification "Prompt for output path"; PNG is
  lossless and universally supported.
- **Alternatives considered**: Fixed/derived name or timestamped name — rejected
  by the clarification.
