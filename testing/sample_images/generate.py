"""Regenerate the synthetic placeholder frames (not real wildfire imagery)."""
from __future__ import annotations

import random
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).parent


def main(n: int = 4) -> None:
    for i in range(n):
        rng = random.Random(1000 + i)
        im = Image.new("RGB", (416, 416), (28 + rng.randint(0, 30), 58, 30))
        d = ImageDraw.Draw(im)
        for _ in range(rng.randint(3, 7)):
            x, y = rng.randint(0, 360), rng.randint(0, 360)
            g = rng.randint(110, 225)
            d.ellipse([x, y, x + rng.randint(25, 95), y + rng.randint(25, 95)], fill=(g, g, g))
        d.text((6, 6), "SYNTHETIC PLACEHOLDER - not real imagery", fill=(230, 230, 230))
        im.save(OUT / f"synthetic_placeholder_{i + 1}.jpg", quality=70)
    print(f"wrote {n} frames to {OUT}")


if __name__ == "__main__":
    main()
