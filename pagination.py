"""Image composition helpers for floor tile pagination."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image


@dataclass
class TilePosition:
    row: int
    col: int
    image_path: str


@dataclass
class Grout:
    size: float
    color: str | None
    pixels_w: int
    pixels_h: int


@dataclass
class LayoutConfig:
    unit: str
    rows: int
    cols: int
    positions: list[TilePosition]
    tile_height: float
    tile_width: float
    grout_size: float
    grout_color: str | None
    output_path: str


def compute_ratio(
    ref_image_size: tuple[int, int], tile_height: float, tile_width: float
) -> tuple[float, float]:
    cell_w, cell_h = ref_image_size
    return cell_h / tile_height, cell_w / tile_width


def grout_pixels(grout_size: float, ratio_h: float, ratio_w: float) -> tuple[int, int]:
    return round(grout_size * ratio_h), round(grout_size * ratio_w)


def compose_layout(config: LayoutConfig) -> Image.Image:
    reference = config.positions[0]

    with Image.open(reference.image_path) as ref_image:
        cell_w, cell_h = ref_image.size

    ratio_h, ratio_w = compute_ratio((cell_w, cell_h), config.tile_height, config.tile_width)
    grout_h, grout_w = grout_pixels(config.grout_size, ratio_h, ratio_w)
    grout = Grout(config.grout_size, config.grout_color, grout_w, grout_h)

    canvas_w = config.cols * (cell_w + grout.pixels_w)
    canvas_h = config.rows * (cell_h + grout.pixels_h)
    fill_color = grout.color if grout.color else "#FFFFFF"
    canvas = Image.new("RGB", (canvas_w, canvas_h), fill_color)

    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.LANCZOS

    for position in config.positions:
        with Image.open(position.image_path) as source:
            tile = source.convert("RGB")
            if tile.size != (cell_w, cell_h):
                tile = tile.resize((cell_w, cell_h), resample_filter)

            x = grout.pixels_w + (position.col - 1) * (cell_w + grout.pixels_w)
            y = grout.pixels_h + (position.row - 1) * (cell_h + grout.pixels_h)
            canvas.paste(tile, (x, y))

    output_path = Path(config.output_path)
    if output_path.parent != Path("."):
        output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, format="PNG")
    return canvas
