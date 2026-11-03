#!/usr/bin/env python3
"""Convert a PNG to An EgG's editable 42x42 GamePad paint import.

Usage: python3 png_to_paint.py image.png /path/to/an-egg-paint-import.txt
Copy the output into sd:/wiiu/apps/cafe-engine/saves/ for IMPORT SD.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

WIDTH = HEIGHT = 42


def convert(source: Path, output: Path) -> None:
    result = subprocess.run(
        [
            "ffmpeg", "-v", "error", "-i", str(source), "-frames:v", "1",
            "-vf", "scale=42:42:force_original_aspect_ratio=decrease:flags=lanczos,"
            "pad=42:42:(ow-iw)/2:(oh-ih)/2:color=black@0",
            "-pix_fmt", "rgba", "-f", "rawvideo", "-",
        ],
        check=True,
        capture_output=True,
    )
    pixels = result.stdout
    if len(pixels) != WIDTH * HEIGHT * 4:
        raise ValueError(f"Expected {WIDTH * HEIGHT * 4} RGBA bytes, got {len(pixels)}")
    cells = []
    for index in range(0, len(pixels), 4):
        r, g, b, a = pixels[index : index + 4]
        cells.append("______0000" if a < 128 else f"{r:02x}{g:02x}{b:02x}0000")
    output.write_text("ANEGG-PAINT-1\n" + "".join(cells) + "\n", encoding="ascii")
    print(f"Wrote editable paint import: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="PNG artwork to convert")
    parser.add_argument("output", type=Path, help="Destination paint import text file")
    arguments = parser.parse_args()
    convert(arguments.source, arguments.output)
