"""Interactive console entry point for floor tile pagination."""

from __future__ import annotations

import re
from pathlib import Path

from pagination import LayoutConfig, TilePosition, compose_layout


UNITS = {"centimeters", "meters", "millimeters"}
GRIDS = {"2x2": (2, 2), "2x3": (2, 3), "3x2": (3, 2), "3x3": (3, 3)}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg"}
HEX_COLOR_PATTERN = re.compile(r"^#[0-9A-Fa-f]{6}$")


def prompt(message: str) -> str:
    return input(message).strip()


def parse_grid(value: str) -> tuple[int, int]:
    normalized = value.lower().strip()
    if normalized not in GRIDS:
        allowed = ", ".join(GRIDS)
        raise ValueError(f"Invalid grid. Allowed values: {allowed}.")
    return GRIDS[normalized]


def prompt_unit() -> str:
    while True:
        value = prompt("Unit of measure (centimeters/meters/millimeters): ").lower()
        if value in UNITS:
            return value
        print("Invalid unit. Use centimeters, meters, or millimeters.")


def prompt_grid() -> tuple[int, int]:
    while True:
        value = prompt("Grid size (2x2, 2x3, 3x2, 3x3): ")
        try:
            return parse_grid(value)
        except ValueError as error:
            print(error)


def prompt_image_path(label: str) -> str:
    while True:
        value = prompt(f"Imagem {label} path (png/jpg/jpeg): ")
        path = Path(value)
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            print("Invalid image format. Use png, jpg, or jpeg.")
            continue
        if not path.is_file():
            print("File not found or not readable. Enter an existing image path.")
            continue
        return str(path)


def prompt_positive_number(message: str) -> float:
    while True:
        value = prompt(message)
        try:
            number = float(value)
        except ValueError:
            print("Invalid number. Enter a numeric value.")
            continue
        if number > 0:
            return number
        print("Value must be greater than zero.")


def prompt_non_negative_number(message: str) -> float:
    while True:
        value = prompt(message)
        try:
            number = float(value)
        except ValueError:
            print("Invalid number. Enter a numeric value.")
            continue
        if number >= 0:
            return number
        print("Value must be zero or greater.")


def prompt_hex_color() -> str:
    while True:
        value = prompt("Grout color (#RRGGBB): ")
        if HEX_COLOR_PATTERN.fullmatch(value):
            return value
        print("Invalid color. Use #RRGGBB, for example #CECECE.")


def prompt_output_path() -> str:
    while True:
        value = prompt("Output PNG path: ")
        if value:
            return value
        print("Output path cannot be empty.")


def prompt_confirmation() -> bool:
    while True:
        value = prompt("Generate this layout? (yes/no): ").lower()
        if value == "yes":
            return True
        if value == "no":
            return False
        print("Please answer yes or no.")


def collect_config() -> LayoutConfig:
    unit = prompt_unit()
    rows, cols = prompt_grid()

    positions = []
    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            positions.append(TilePosition(row, col, prompt_image_path(f"{row}x{col}")))

    tile_height = prompt_positive_number(f"Tile height in {unit}: ")
    tile_width = prompt_positive_number(f"Tile width in {unit}: ")
    grout_size = prompt_non_negative_number(f"Grout thickness in {unit}: ")
    grout_color = prompt_hex_color() if grout_size > 0 else None
    output_path = prompt_output_path()

    return LayoutConfig(
        unit=unit,
        rows=rows,
        cols=cols,
        positions=positions,
        tile_height=tile_height,
        tile_width=tile_width,
        grout_size=grout_size,
        grout_color=grout_color,
        output_path=output_path,
    )


def print_header() -> None:
    print("Floor Tile Pagination Generator")
    print("Units: centimeters, meters, millimeters")
    print("Grids: 2x2, 2x3, 3x2, 3x3")
    print("Images: png, jpg, jpeg")
    print()


def print_summary(config: LayoutConfig) -> None:
    print()
    print("Summary")
    print(f"Unit: {config.unit}")
    print(f"Grid: {config.rows}x{config.cols}")
    for position in config.positions:
        print(f"Imagem {position.row}x{position.col}: {position.image_path}")
    print(f"Tile size: {config.tile_height} x {config.tile_width} {config.unit}")
    print(f"Grout thickness: {config.grout_size} {config.unit}")
    if config.grout_color:
        print(f"Grout color: {config.grout_color}")
    print(f"Output path: {config.output_path}")
    print()


def main() -> None:
    print_header()
    config = collect_config()
    print_summary(config)

    if not prompt_confirmation():
        print("No output generated.")
        return

    compose_layout(config)
    print(f"Saved to {config.output_path}")


if __name__ == "__main__":
    main()
