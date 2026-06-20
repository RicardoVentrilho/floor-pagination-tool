# Implementation Plan: Floor Tile Pagination Generator

**Branch**: `001-floor-pagination` | **Date**: 2026-06-20 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/001-floor-pagination/spec.md`

## Summary

An interactive Python console program that guides the user through entering
layout parameters (unit of measure, grid size 2x2–3x3, one image per cell,
physical tile size, grout thickness, and grout color), shows a summary for
confirmation, and then composes the per-cell images into a single output image
with proportional grout spacing. The pixel-to-unit ratio is derived from the
first (reference) image; grout in pixels = grout × ratio (rounded), and the
layout size per axis = n × (tile_px + grout_px). Image composition uses Pillow.

## Technical Context

**Language/Version**: Python 3.10+

**Primary Dependencies**: Pillow (PIL) for image loading, resizing, and
composition. Standard library `input()` for the console flow.

**Storage**: Local filesystem — reads source tile images, writes one output
image to a user-supplied path.

**Testing**: None required (prototype). Per the constitution, automated tests
are optional and skipped; validation is manual via `quickstart.md`.

**Target Platform**: Cross-platform local CLI (macOS/Linux/Windows terminal).

**Project Type**: Single-project command-line tool.

**Performance Goals**: Interactive; a single layout (≤ 9 images) composes in
well under a second. No throughput targets.

**Constraints**: Must stay simple and fast to iterate (prototype). No outer
framework, no build pipeline beyond `pip install pillow`.

**Scale/Scope**: Grids from 2x2 up to 3x3 (max 9 tiles); single user, single
run, single output file.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Assessment |
|-----------|------------|
| I. Ship Fast, Iterate Later | PASS — flat module layout, Pillow does the heavy lifting, no premature abstractions. |
| II. Prototype Mindset (YAGNI) | PASS — only the requested grids/units/formats; no config files, plugins, or GUI. |
| III. Testing Is Optional | PASS — no test suite planned; manual verification via quickstart. |
| IV. Working Software Over Process | PASS — definition of done is "run it and an image is produced"; no review gates. |
| V. Minimal Dependencies & Simplicity | PASS — exactly one third-party dependency (Pillow), which clearly saves far more time than hand-rolling image composition. |

**Result**: All gates pass. No violations; Complexity Tracking not required.

## Project Structure

### Documentation (this feature)

```text
specs/001-floor-pagination/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── cli.md           # Phase 1 output — console interaction + composition contract
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (/speckit-tasks — NOT created here)
```

### Source Code (repository root)

```text
main.py                # Interactive console flow: prompts, validation, summary,
                       # confirmation, then invokes composition
pagination.py          # Core logic: ratio calc, grout-px calc, image resize,
                       # and layout composition (Pillow)
requirements.txt       # Pillow
```

**Structure Decision**: Flat two-module layout at the repository root, per the
prototype constitution (Principles I, II, V). `main.py` owns all console I/O and
input validation; `pagination.py` owns the pure composition logic so it can be
exercised directly without the prompt loop. No `src/` package nesting and no
`tests/` directory — both would be over-engineering for this prototype.

## Complexity Tracking

> No constitution violations. Section intentionally empty.
