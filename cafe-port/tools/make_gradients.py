#!/usr/bin/env python3
"""Bake the same vertical CafeStyle gradients into narrow PNG textures."""

from pathlib import Path
import math
import struct
import zlib


HEIGHT = 480
PALETTES = {
    "title": ("#be10f2", "#5665dc", "#03b9e9", 0.59),
    "plains": ("#49dc7c", "#13b5ad", "#138ee0", 0.55),
    "pinball": ("#f332b7", "#a033dc", "#4b21b1", 0.52),
    "frying": ("#ffce41", "#ff8845", "#ef4151", 0.52),
    "magnet": ("#42dce8", "#348dcf", "#3745a8", 0.52),
    "sticky": ("#c5ea45", "#74c75d", "#408b68", 0.52),
    "wind": ("#b1edff", "#65b9f0", "#468bdc", 0.52),
    "portal": ("#10247a", "#3c4cbd", "#b046d7", 0.54),
    "final": ("#050209", "#170520", "#5a0a83", 0.68),
}


def cave_color(value, gray_weight):
    """Mix a biome color with slightly dark gray for its cave background."""
    original = bytes.fromhex(value[1:])
    return "#" + "".join(f"{round(112 * gray_weight + channel * (1 - gray_weight)):02x}"
                         for channel in original)


CAVE_BLUE = ("#168bff", "#075ddc", "#123bb4", 0.55)
for cave_name, palette, gray_weight in (
    ("cave", CAVE_BLUE, 0.80),
    ("frying-cave", PALETTES["frying"], 0.80),
    ("portal-cave", PALETTES["portal"], 0.60),
):
    top, middle, bottom, middle_at = palette
    PALETTES[cave_name] = (
        cave_color(top, gray_weight), cave_color(middle, gray_weight),
        cave_color(bottom, gray_weight), middle_at
    )


def rgb(value):
    return tuple(bytes.fromhex(value[1:]))


def pixel(top, middle, bottom, middle_at, row):
    t = row / HEIGHT
    left, right, portion = (
        (top, middle, t / middle_at)
        if t <= middle_at
        else (middle, bottom, (t - middle_at) / (1 - middle_at))
    )
    return bytes(round(a + (b - a) * portion) for a, b in zip(left, right)) + b"\xff"


def chunk(kind, data):
    return struct.pack(">I", len(data)) + kind + data + struct.pack(
        ">I", zlib.crc32(kind + data) & 0xFFFFFFFF
    )


def main():
    assets = Path(__file__).resolve().parent.parent / "assets"
    for name, (top, middle, bottom, middle_at) in PALETTES.items():
        scanlines = b"".join(
            b"\x00" + pixel(rgb(top), rgb(middle), rgb(bottom), middle_at, row)
            for row in range(HEIGHT)
        )
        image = (
            b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, HEIGHT, 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(scanlines, 9))
            + chunk(b"IEND", b"")
        )
        (assets / f"gradient-{name}.png").write_bytes(image)
    # A small tangential slice matching shockwave-visible.png: violet arcs
    # with a strong outer edge that fades toward the center.
    width, height = 30, 30
    rows = []
    for y in range(height):
        row = bytearray(b"\x00")
        base = max(0.0, (250 - max(0, y - 2) * 9.15) / 255) * min(1.0, y / 2)
        for x in range(width):
            if x < 14:
                previous = base * (1 - x / 14)
                opacity = (base - previous) / (1 - previous)
            elif x >= 16:
                opacity = base * (1 - (x - 16) / 14)
            else:
                opacity = base
            row.extend((165, 0, 255, round(opacity * 255)))
        rows.append(bytes(row))
    image = (b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
        + chunk(b"IEND", b""))
    (assets / "shockwave-segment.png").write_bytes(image)

    width, height = 48, 32
    rows = []
    rim_stops = (
        (0.0, (142, 25, 194), 230),
        (3.0, (124, 20, 179), 192),
        (6.0, (101, 15, 151), 138),
        (10.0, (69, 9, 111), 65),
        (15.5, (46, 5, 79), 0),
    )
    for y in range(height):
        row = bytearray(b"\x00")
        distance = abs(y - (height - 1) / 2)
        for index in range(1, len(rim_stops)):
            low, high = rim_stops[index - 1], rim_stops[index]
            if distance <= high[0]:
                t = (distance - low[0]) / (high[0] - low[0])
                color = tuple(round(a + (b - a) * t) for a, b in zip(low[1], high[1]))
                alpha = round(low[2] + (high[2] - low[2]) * t)
                break
        base = alpha / 255
        for x in range(width):
            if x < 14:
                previous = base * (1 - x / 14)
                opacity = (base - previous) / (1 - previous)
            elif x >= 34:
                opacity = base * (1 - (x - 34) / 14)
            else:
                opacity = base
            row.extend((*color, round(opacity * 255)))
        rows.append(bytes(row))
    image = (b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
        + chunk(b"IEND", b""))
    (assets / "black-hole-rim.png").write_bytes(image)

    # Bake the full void into one small texture. Its size changes at runtime,
    # but Cafe Engine no longer has to redraw a vector circle and rim sprites.
    size = 256
    rows = []
    center = (size - 1) / 2
    for y in range(size):
        row = bytearray(b"\x00")
        for x in range(size):
            radius = math.hypot(x - center, y - center) / (size / 2)
            if radius <= 0.75:
                color, alpha = (3, 0, 8), 255
            elif radius <= 0.83:
                t = (radius - 0.75) / 0.08
                t = t * t * (3 - 2 * t)
                color = tuple(round(a + (b - a) * t)
                              for a, b in zip((3, 0, 8), (165, 0, 255)))
                alpha = 255
            elif radius <= 0.92:
                t = (radius - 0.83) / 0.09
                t = t * t * (3 - 2 * t)
                color = (round(165 - 70 * t), 0, round(255 - 90 * t))
                alpha = round(255 * (1 - t))
            else:
                color, alpha = (0, 0, 0), 0
            row.extend((*color, alpha))
        rows.append(bytes(row))
    image = (b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(b"".join(rows), 9))
        + chunk(b"IEND", b""))
    (assets / "black-hole.png").write_bytes(image)


if __name__ == "__main__":
    main()
