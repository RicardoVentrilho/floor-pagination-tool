# Tasks: Floor Tile Pagination Generator

**Feature**: `001-floor-pagination` | **Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

**Tech**: Python 3.10+, Pillow. Flat layout at repo root: `main.py` (console I/O
+ validation), `pagination.py` (composition logic), `requirements.txt`.

**Tests**: OPTIONAL and intentionally omitted (prototype — constitution
Principle III). Validation is manual via [quickstart.md](./quickstart.md).

**Format**: `- [ ] [TaskID] [P?] [Story?] Description with file path`. `[P]` = can
run in parallel (different file / no dependency on an incomplete task).

---

## Phase 1: Setup

- [X] T001 Create `requirements.txt` at repository root with a single line: `Pillow`
- [X] T002 [P] Create core module file `pagination.py` at repository root (empty module with header comment)
- [X] T003 [P] Create entry-point file `main.py` at repository root with a `def main(): ...` and `if __name__ == "__main__": main()` guard

---

## Phase 2: Foundational (blocking prerequisites)

- [X] T004 Define in-memory data structures `LayoutConfig`, `TilePosition`, `Grout` (dataclasses) per [data-model.md](./data-model.md) in `pagination.py`
- [X] T005 Implement a generic `prompt(message)` helper that reads a line from stdin and returns the stripped string in `main.py`

**Checkpoint**: Data structures and the basic prompt helper exist; user stories can build on them.

---

## Phase 3: User Story 1 - Generate a 2x2 tile layout with grout (Priority: P1) 🎯 MVP

**Goal**: A user runs the program, supplies a 2x2 grid of images plus
measurements/grout/color/output path, confirms the summary, and gets a composed
output image with proportional grout.

**Independent Test**: Run with millimeters, 2x2, four 150×150 PNGs, tile
1000×1000, grout 1.5, color #CECECE, confirm → a 300×300 PNG is produced
(grout rounds to 0). Repeat the centimeters case → 306×306 PNG.

- [X] T006 [US1] Implement `compute_ratio(ref_image_size, tile_height, tile_width)` returning `(ratio_h, ratio_w)` per FR-008 in `pagination.py`
- [X] T007 [US1] Implement `grout_pixels(grout_size, ratio_h, ratio_w)` using `round()` per FR-010 in `pagination.py`
- [X] T008 [US1] Implement `compose_layout(config)` in `pagination.py`: open reference image (1x1) for cell size, build RGB canvas of `rows×(cell+grout)` filled with grout color, resize each image to the cell size (FR-018) and paste at `(grout_w + c×(cell_w+grout_w), grout_h + r×(cell_h+grout_h))` per FR-011 (canvas supports any rows/cols and grout_px=0)
- [X] T009 [US1] Implement saving the composed canvas as PNG to `config.output_path`, overwriting if present (FR-015) in `pagination.py`
- [X] T010 [US1] Implement the happy-path console flow in `main.py`: prompt unit, grid (assume 2x2 here), four image paths by position (1x1,1x2,2x1,2x2), tile height, tile width, grout size, grout color, output path; build a `LayoutConfig`
- [X] T011 [US1] Implement the summary printout of all entered values + confirmation prompt (yes/no); on `yes` call `compose_layout` + save, on `no` exit without writing (FR-014/FR-015/FR-016) in `main.py`
- [X] T012 [US1] Wire `main()` to run the full flow end to end and print the saved output path in `main.py`

**Checkpoint**: MVP — a 2x2 layout can be generated end to end and validated against quickstart Scenarios 1 & 2.

---

## Phase 4: User Story 2 - Generate larger layouts up to 3x3 (Priority: P2)

**Goal**: Support all accepted grid sizes (2x2, 2x3, 3x2, 3x3), requesting one
image per cell.

**Independent Test**: Choose 3x3, supply nine images plus the other parameters,
confirm → a 3×3 layout sized `3×(cell+grout)` per axis is produced; choosing 2x3
asks for exactly six images.

- [X] T013 [US2] Implement `parse_grid(value)` mapping `"RxC"` → `(rows, cols)` for the accepted set, used by the grid prompt in `main.py`
- [X] T014 [US2] Generalize the image-prompt loop in `main.py` to request `rows×cols` image paths in reading order (1x1 … rows×cols) based on the parsed grid

**Checkpoint**: Any supported grid size composes correctly (compose_layout from T008 already handles arbitrary rows/cols).

---

## Phase 5: User Story 3 - Input validation and guided correction (Priority: P2)

**Goal**: Every prompt rejects invalid input with a clear message and re-prompts
instead of crashing.

**Independent Test**: Enter invalid values at each prompt (grid 3x4, unit
inches, a .gif image, a missing path, color ZZZZZZ) and confirm each is rejected
and re-prompted.

- [X] T015 [US3] Add validation + re-prompt loop for the unit prompt (centimeters/meters/millimeters) per FR-002/FR-017 in `main.py`
- [X] T016 [US3] Add validation + re-prompt for grid size: reject anything outside {2x2,2x3,3x2,3x3} (e.g., 3x4, 5x5) with a message naming allowed values per FR-003 in `main.py`
- [X] T017 [US3] Add image-path validation + re-prompt: extension in {png,jpg,jpeg} (FR-005) and file exists/readable (FR-006) in `main.py`
- [X] T018 [US3] Add numeric validation + re-prompt for tile height/width (>0, FR-007) and grout size (≥0, FR-009) in `main.py`
- [X] T019 [US3] Add hex color validation + re-prompt for `#RRGGBB` per FR-012 in `main.py`

**Checkpoint**: The flow is crash-resistant; quickstart Scenario 3 passes.

---

## Phase 6: User Story 4 - Skip grout color when there is no grout (Priority: P3)

**Goal**: When grout size is 0, never ask for a color and compose tiles edge to
edge.

**Independent Test**: Enter grout 0 → no color prompt appears and output has no
spacing (2x2 of 150px → 300×300).

- [X] T020 [US4] In `main.py`, request the grout color only when grout size > 0; otherwise set `grout_color = None` per FR-012/FR-013
- [X] T021 [US4] Confirm `compose_layout` produces edge-to-edge tiles when grout_px = 0 (no color needed); adjust the canvas fill default in `pagination.py` if required

**Checkpoint**: quickstart Scenario 4 passes.

---

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T022 [P] Improve console UX in `main.py`: clear position labels (e.g., "Imagem 1x1") and a final "saved to <path>" confirmation message
- [X] T023 [P] Add a short usage header printed at startup describing accepted units/grids/formats in `main.py`
- [X] T024 Run all quickstart validation scenarios (1–6) manually and confirm expected output sizes (300×300, 306×306) and behaviors

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** → **Phase 2 (Foundational)** → user story phases.
- **US1 (P1)** depends only on Setup + Foundational. This is the MVP.
- **US2 (P2)** depends on US1 (reuses the prompt flow and `compose_layout`).
- **US3 (P2)** depends on US1 (hardens the prompts built in US1/US2); independent of US2 logic but easiest after the prompts exist.
- **US4 (P3)** depends on US1 (adjusts the color prompt + composition fill).
- **Polish** last.

## Parallel Opportunities

- T002 and T003 (different files) can run in parallel.
- Within US1, `pagination.py` tasks (T006, T007, T008, T009) and the `main.py`
  flow tasks (T010–T012) touch different files; the composition functions can be
  built in parallel with the prompt flow, then wired together at T012.
- Polish T022 and T023 are both in `main.py` — do sequentially (same file).

## Implementation Strategy

- **MVP = Phase 1 + Phase 2 + Phase 3 (US1)** — delivers a working 2x2 generator
  validated by quickstart Scenarios 1 & 2.
- Add US2 for full grid support, US3 for robustness, US4 for the zero-grout
  convenience, then polish. Each phase is independently demonstrable.
