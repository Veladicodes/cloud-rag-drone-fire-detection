"""Build a YOLO *classification* dataset from FLAME's frame-level Fire/No_Fire folders.

FLAME's frame-level set has NO bounding boxes — the label is the folder name. So this
pass trains a yolov8n-CLS classifier, which the detector wrapper then adapts into a
single-box-per-frame "detection" (honest approximation, documented in results/README.md).

Split (see ADR-001 outcome addendum, dated 2026-09-10):
  * Phase-1 documented a 70/15/15 split "chronological by flight" to prevent frame
    leakage. The downloaded FLAME *classification* sub-item carries NO flight id or
    timestamp, so a true chronological partition is impossible on this data.
  * Substitute: a **seeded (seed=0) random, class-stratified** 70/15/15 split.
      - train + val are drawn from data/flame/Training/
      - test is data/flame/Test/ (a genuinely separate FLAME release folder), used
        untouched as the held-out set.
    The lexical-order slice used in the first attempt caused a catastrophic
    train/val mismatch (val acc ~= chance); the seeded random split fixes that.

Output: data/flame_cls/{train,val,test}/{Fire,No_Fire}/  (hardlink to originals)

Env knobs (CPU-bounded runs — the subsample size is logged and reported honestly):
  FLAME_MAX_PER_CLASS   cap images per class per split (default: no cap)
"""
from __future__ import annotations

import os
import random
import shutil
from pathlib import Path

from backend.core.config import REPO_ROOT

SRC = REPO_ROOT / "data" / "flame"
DST = REPO_ROOT / "data" / "flame_cls"
CLASSES = ["Fire", "No_Fire"]
SEED = 0
VAL_FRAC_OF_TRAINING = 0.15 / 0.85  # 15% of the whole, from the 85% that Training represents


def _link(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        return
    try:
        dst.hardlink_to(src)
    except OSError:
        shutil.copy2(src, dst)


def _emit(split: str, cls: str, imgs: list[Path], cap: int | None) -> int:
    if cap:
        imgs = imgs[:cap]
    for p in imgs:
        _link(p, DST / split / cls / p.name)
    return len(imgs)


def main() -> Path:
    if not SRC.exists():
        raise FileNotFoundError(f"{SRC} not found - download FLAME first (see data/README.md)")
    cap = int(os.environ["FLAME_MAX_PER_CLASS"]) if os.environ.get("FLAME_MAX_PER_CLASS") else None
    rng = random.Random(SEED)

    counts = {"train": 0, "val": 0, "test": 0}
    for cls in CLASSES:
        tr_frames = sorted((SRC / "Training" / cls).glob("*.jpg"))
        rng.shuffle(tr_frames)  # seeded -> deterministic
        n_val = int(len(tr_frames) * VAL_FRAC_OF_TRAINING)
        counts["val"] += _emit("val", cls, tr_frames[:n_val], cap)
        counts["train"] += _emit("train", cls, tr_frames[n_val:], cap)
        counts["test"] += _emit("test", cls, sorted((SRC / "Test" / cls).glob("*.jpg")), cap)

    print(f"FLAME-cls (seed={SEED} stratified random): {counts}"
          + (f"  [capped {cap}/class/split]" if cap else "  [full data]"))
    return DST


if __name__ == "__main__":
    main()
