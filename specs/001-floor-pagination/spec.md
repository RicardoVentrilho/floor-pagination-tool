# Feature Specification: Floor Tile Pagination Generator

**Feature Branch**: `001-floor-pagination`

**Created**: 2026-06-20

**Status**: Draft

**Input**: User description: "Criar um prompt que receba parametros de entrada via console para criar uma paginacao de piso de 2x2 ateh 3x3 em python."

## Clarifications

### Session 2026-06-20

- Q: For a 2×2 grid of 150px tiles with 3px grout, should the total be 303px (internal seams only) or 306px? → A: Internal + outer border — the layout size per axis equals n × (tile_px + grout_px), yielding 306px for the 2×2 example.
- Q: How should position images with differing pixel sizes be handled? → A: Resize to reference — the first image's pixel size sets the tile cell size, and all other images are resized to match it; the ratio is derived from that reference size.
- Q: Where/how is the generated layout saved? → A: Prompt the user for the output file path/name as part of the console flow.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate a 2x2 tile layout with grout (Priority: P1)

A user runs the program from the console and is guided step by step to provide
the layout parameters: unit of measure, grid size, one image per grid position,
the physical tile dimensions, the grout thickness, and the grout color. After
confirming a summary of the entered data, the program produces an output image
that arranges the tile images into the grid with proportional grout spacing
between them.

**Why this priority**: This is the core purpose of the tool — turning a set of
tile images plus physical measurements into a single composed layout image. It
delivers the complete value on its own and is the smallest viable product.

**Independent Test**: Run the program, choose millimeters, choose a 2x2 grid,
supply four PNG paths, enter floor tile size 1000x1000, grout 1.5, color
#CECECE, confirm the summary, and verify an output image is produced with the
four tiles arranged in a 2x2 grid and grout applied proportionally.

**Acceptance Scenarios**:

1. **Given** the user selected millimeters and a 2x2 grid with four 150x150 px
   PNG images, a tile size of 1000x1000 mm, grout 1.5 mm, and color #CECECE,
   **When** the user confirms the summary, **Then** an output image is generated
   arranging the four tiles in a 2x2 grid where the grout thickness in pixels is
   the grout measure multiplied by the pixel-to-unit ratio (1.5 × 0.15 = 0.225,
   which rounds to 0 px).
2. **Given** the user selected centimeters and a 2x2 grid with four 150x150 px
   PNG images, a tile size of 100x100 cm, grout 2 cm, and color #CECECE,
   **When** the user confirms the summary, **Then** an output image is generated
   where the grout in pixels is the grout measure multiplied by the ratio
   (2 × 1.5 = 3 px) and the total layout size per axis equals n × (tile_px +
   grout_px), i.e. 2 × (150 + 3) = 306 px, producing a 306×306 px layout.
3. **Given** all required parameters have been entered, **When** the program
   reaches the end of input, **Then** it displays a summary of every entered
   value and asks the user to confirm before generating the file.
4. **Given** the summary is shown, **When** the user declines confirmation,
   **Then** no output file is generated.

---

### User Story 2 - Generate larger layouts up to 3x3 (Priority: P2)

A user composes layouts using any supported non-square or square grid size:
2x2, 2x3, 3x2, or 3x3. The program asks for one image per cell in the chosen
grid and composes them accordingly.

**Why this priority**: Extends the core capability to the full supported range
of grid sizes. Valuable but builds directly on Story 1.

**Independent Test**: Run the program, choose a 3x3 grid, supply nine valid
images plus the remaining parameters, confirm, and verify a 3x3 composed output
image with two internal grout seams per axis.

**Acceptance Scenarios**:

1. **Given** the user chose a 2x3 grid, **When** prompted for images, **Then**
   the program asks for exactly six images, one per grid position.
2. **Given** the user chose a 3x3 grid, **When** the layout is generated,
   **Then** the total size per axis equals n × (tile_px + grout_px) with n = 3,
   placing grout between tiles and along the outer border.

---

### User Story 3 - Input validation and guided correction (Priority: P2)

While entering parameters, the user receives immediate, clear validation
feedback for invalid input (unsupported grid size, unsupported unit, invalid
image format, missing image file, malformed hex color) and is re-prompted
rather than having the program crash or produce a bad file.

**Why this priority**: The program is interactive and depends entirely on
user-supplied values; without validation the tool is unreliable. Important but
secondary to producing output for valid input.

**Independent Test**: Enter invalid values at each prompt (e.g., grid 3x4, unit
"inches", a `.gif` image, a non-existent path, color "ZZZZZZ") and verify the
program rejects each with a clear message and re-prompts.

**Acceptance Scenarios**:

1. **Given** the grid-size prompt, **When** the user enters `3x4` or `5x5`,
   **Then** the program rejects it and explains that only 2x2, 2x3, 3x2, and 3x3
   are allowed.
2. **Given** the image prompt, **When** the user supplies a file that is not
   PNG, JPG, or JPEG, **Then** the program rejects it and re-prompts.
3. **Given** the image prompt, **When** the supplied path does not exist,
   **Then** the program reports the file was not found and re-prompts.
4. **Given** the grout thickness is greater than zero, **When** the user enters
   a grout color that is not a valid hex color, **Then** the program rejects it
   and re-prompts.

---

### User Story 4 - Skip grout color when there is no grout (Priority: P3)

When the user enters a grout thickness of zero, the program does not ask for a
grout color and composes the tiles with no spacing between them.

**Why this priority**: A small but well-defined conditional behavior that
improves the input flow; not required for the primary success path.

**Independent Test**: Enter grout size 0 and verify the program never prompts
for a grout color and produces a layout with tiles placed edge to edge.

**Acceptance Scenarios**:

1. **Given** the grout-thickness prompt, **When** the user enters `0`, **Then**
   the program does not ask for a grout color.
2. **Given** grout thickness is `0`, **When** the layout is generated, **Then**
   tiles are placed directly adjacent with no grout spacing.

---

### Edge Cases

- **Grout rounds to zero**: When grout-thickness × ratio rounds to 0 px (e.g.,
  1.5 mm × 0.15 = 0.225), the layout is composed as if there were no grout
  spacing, even though a non-zero grout measure was entered.
- **Non-square ratio for height vs width**: When the tile's physical height and
  width produce different pixel-to-unit ratios for height and width, each axis
  uses its own ratio.
- **Grout color entered but grout is zero**: Color is never requested when grout
  is zero, so this combination cannot occur through the guided flow.
- **Unit conversion expectations**: All measurements in a single run are entered
  in the unit the user selected at the start; the program does not mix units.
- **Output path already exists**: When the user-supplied output path already
  points to an existing file, the program overwrites it (see Assumptions).
- **Images of differing sizes**: When position images have different pixel
  dimensions, every image is resized to the first image's size before composing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The program MUST run as an interactive console flow that prompts
  the user for each parameter in sequence.
- **FR-002**: The program MUST ask the user to choose a unit of measure, and
  MUST accept only: centimeters, meters, or millimeters. All subsequent measures
  in the run are interpreted in the chosen unit.
- **FR-003**: The program MUST ask for the grid (pagination) size and MUST
  accept only 2x2, 2x3, 3x2, and 3x3. The minimum is 2x2 and the maximum is 3x3.
  Values such as 3x4 or 5x5 MUST be rejected.
- **FR-004**: The program MUST request one image path for each position in the
  chosen grid, identified by its row/column position (e.g., 1x1, 1x2, …).
- **FR-005**: The program MUST accept only image files with the extensions PNG,
  JPG, or JPEG, and MUST reject any other format.
- **FR-006**: The program MUST verify that each supplied image path exists and
  is readable, and MUST re-prompt if it does not.
- **FR-007**: The program MUST request the physical floor tile size as height ×
  width in the selected unit.
- **FR-008**: The program MUST compute the proportion (ratio) between the tile's
  pixel dimensions and its physical size, where ratio = image pixels ÷ physical
  size (e.g., a 150 px image for a 1000 mm tile yields a ratio of 0.15; a 150 px
  image for a 100 cm tile yields a ratio of 1.5).
- **FR-009**: The program MUST request the grout thickness as a measure in the
  selected unit, used as internal spacing between tiles.
- **FR-010**: The program MUST convert the grout thickness to pixels by
  multiplying it by the ratio, and MUST round the result to a whole number of
  pixels.
- **FR-011**: The program MUST apply grout both between adjacent tiles and along
  the outer border of the layout, such that the total layout size per axis equals
  n × (tile_px + grout_px), where n is the number of tiles on that axis (e.g., a
  2×2 grid of 150 px tiles with 3 px grout yields 306×306 px).
- **FR-012**: When the grout thickness is greater than zero, the program MUST
  request a grout color as a hexadecimal color value and MUST validate it.
- **FR-013**: When the grout thickness is zero, the program MUST NOT request a
  grout color and MUST compose tiles with no spacing.
- **FR-014**: Before generating output, the program MUST display a summary of
  all entered values and MUST require explicit user confirmation.
- **FR-015**: Upon confirmation, the program MUST generate an output image file
  that arranges each position's image into the grid with the computed grout
  spacing and color applied.
- **FR-016**: If the user declines confirmation, the program MUST NOT generate
  an output file.
- **FR-017**: For any invalid input, the program MUST display a clear message
  and re-prompt for that value rather than terminating.
- **FR-018**: The program MUST use the first supplied image's pixel dimensions as
  the reference tile cell size, derive the ratio from that reference size, and
  resize every other position image to match the reference cell size before
  composing the layout.
- **FR-019**: Before generating output, the program MUST prompt the user for the
  output file path/name where the generated layout image will be saved.

### Key Entities *(include if feature involves data)*

- **Layout configuration**: The complete set of user-entered parameters for one
  run — unit of measure, grid size, the per-position image references, physical
  tile height and width, grout thickness, and grout color (when applicable).
- **Tile position**: A single cell in the grid identified by its row and column
  (e.g., 1x1, 2x3), associated with one source image.
- **Grout**: The internal spacing between tiles, defined by a thickness (in the
  selected unit, converted to pixels via the ratio) and, when non-zero, a
  hexadecimal color.
- **Generated layout**: The resulting composed image file arranging all tile
  positions with grout applied.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can complete the full guided input flow for a 2x2 layout
  and produce an output file in under 3 minutes.
- **SC-002**: 100% of unsupported grid sizes, unsupported units, unsupported
  image formats, missing files, and malformed hex colors are rejected with a
  re-prompt rather than causing a crash or a bad output file.
- **SC-003**: For the provided reference cases, the grout thickness in the output
  equals the entered grout measure multiplied by the ratio, rounded to whole
  pixels (e.g., 2 cm at ratio 1.5 yields 3 px; 1.5 mm at ratio 0.15 yields 0 px).
- **SC-004**: When grout thickness is zero, the user is never asked for a color
  and the output contains no spacing between tiles, in 100% of such runs.
- **SC-005**: No output file is ever generated when the user declines the final
  confirmation.

## Assumptions

- This is a prototype tool prioritizing a fast, working result over robustness
  (per the project constitution); production-grade edge-case handling is out of
  scope.
- Position images may have different pixel dimensions; the first supplied image
  sets the reference tile cell size and all others are resized to match it. The
  ratio is derived from that reference size and the physical tile size.
- The ratio is derived per axis (height ratio from height; width ratio from
  width); for square tiles with square images the two ratios are equal.
- The output is a single raster image file (PNG); the program prompts the user
  for the output path/name, and if a file already exists at that path it is
  overwritten.
- The 306 px total in the second reference case is authoritative: the governing
  rule is that the layout size per axis equals n × (tile_px + grout_px) (grout
  applied between tiles and along the outer border), which yields 306 px for the
  2×2 example and 300 px when grout rounds to 0.
- Hexadecimal grout color is accepted in standard `#RRGGBB` form.
- Measurements are entered using the decimal conventions the user types (e.g.,
  `1.5`); locale-specific decimal separators are not a concern for the prototype.
