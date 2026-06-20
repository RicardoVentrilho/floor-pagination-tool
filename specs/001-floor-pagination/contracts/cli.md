# CLI Contract: Floor Tile Pagination Generator

This is an interactive console tool. The "contract" is the ordered prompt
sequence, the accepted inputs/validation, and the composition algorithm.

## Invocation

```bash
python main.py
```

No command-line flags. All input is collected interactively.

## Prompt sequence

| # | Prompt | Accepted input | On invalid input |
|---|--------|----------------|------------------|
| 1 | Unit of measure | `centimeters` \| `meters` \| `millimeters` | Message + re-prompt (FR-002, FR-017) |
| 2 | Grid size | `2x2` \| `2x3` \| `3x2` \| `3x3` | Message naming allowed values + re-prompt (FR-003) |
| 3..(3+N−1) | Image path for each position `RxC` (N = rows×cols, reading order) | Existing file with extension png/jpg/jpeg | Message (not found / bad format) + re-prompt (FR-004, FR-005, FR-006) |
| next | Tile height (in chosen unit) | number > 0 | Message + re-prompt (FR-007) |
| next | Tile width (in chosen unit) | number > 0 | Message + re-prompt (FR-007) |
| next | Grout thickness (in chosen unit) | number ≥ 0 | Message + re-prompt (FR-009) |
| next | Grout color (hex) — **only if grout > 0** | `#RRGGBB` | Message + re-prompt (FR-012); skipped entirely when grout = 0 (FR-013) |
| next | Output file path | non-empty path | Message + re-prompt (FR-019) |
| last | Confirmation of summary | yes / no | `no` → abort without writing (FR-016) |

### Summary + confirmation (FR-014)

Before composing, print a summary of all collected values (unit, grid, each
image path by position, tile height×width, grout size, grout color if any,
output path) and ask the user to confirm. Only on explicit confirmation does the
program write the output file (FR-015). On decline, exit without writing.

## Composition algorithm (contract)

Inputs: validated `LayoutConfig` (see [data-model.md](../data-model.md)).

1. Open the reference image (position 1x1); read `cell_w`, `cell_h`.
2. `ratio_w = cell_w / tile_width`; `ratio_h = cell_h / tile_height`.
3. `grout_px_w = round(grout_size × ratio_w)`; `grout_px_h = round(grout_size × ratio_h)`.
4. `canvas_w = cols × (cell_w + grout_px_w)`; `canvas_h = rows × (cell_h + grout_px_h)`.
5. Create an RGB canvas of `(canvas_w, canvas_h)` filled with the grout color
   (any color when grout is 0, since it is fully covered).
6. For each position (row r in 0..rows−1, col c in 0..cols−1):
   - Open its image; resize to `(cell_w, cell_h)` if it differs.
   - Paste at `(grout_px_w + c × (cell_w + grout_px_w),
     grout_px_h + r × (cell_h + grout_px_h))`.
7. Save the canvas as PNG to `output_path` (overwrite if it exists).

## Worked examples (must hold)

| Case | Unit | Grid | Tile | Image | Grout | ratio | grout_px | Output size |
|------|------|------|------|-------|-------|-------|----------|-------------|
| 1 | mm | 2x2 | 1000×1000 | 150×150 | 1.5 | 0.15 | round(0.225)=0 | 300×300 |
| 2 | cm | 2x2 | 100×100 | 150×150 | 2 | 1.5 | round(3.0)=3 | 306×306 |

(Both from the spec's reference use cases; the 306 total is authoritative per the
clarification: `2 × (150 + 3) = 306`.)

## Exit behavior

- Success: output PNG written; print the saved path.
- User declined confirmation: no file written; clean exit.
- The program never crashes on bad input; it always re-prompts (FR-017).
