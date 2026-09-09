"""Scriptable YOLO evaluation.

The moment a real dataset is dropped into ``data/flame/`` (images + YOLO-format
labels), this script produces real mAP/FPS numbers into ``results/yolo-metrics/``.
Until then it runs the placeholder detector over whatever sample images exist and
prints ``PENDING`` for anything that needs the real dataset.

    python -m ai.evaluation.run_yolo_eval
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from ai.models.yolo_detector import get_detector
from backend.core.config import REPO_ROOT

FLAME_DIR = REPO_ROOT / "data" / "flame"
SAMPLE_DIR = REPO_ROOT / "testing" / "sample_images"
OUT_DIR = REPO_ROOT / "results" / "yolo-metrics"


def _images(d: Path) -> list[Path]:
    return sorted(p for p in d.glob("**/*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"})


def main() -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    detector = get_detector()
    backend = getattr(detector, "backend", "unknown")

    have_flame = FLAME_DIR.exists() and any(_images(FLAME_DIR))
    imgs = _images(FLAME_DIR) if have_flame else _images(SAMPLE_DIR)

    report: dict = {
        "detector_backend": backend,
        "dataset": "FLAME" if have_flame else "sample_images (placeholder)",
        "num_images": len(imgs),
        "mAP@0.5": "PENDING — requires FLAME/FireNet dataset + fine-tuned weights",
        "mAP@0.5:0.95": "PENDING — requires FLAME/FireNet dataset + fine-tuned weights",
    }

    if imgs:
        t0 = time.perf_counter()
        detections = sum(len(detector.detect(str(p))) for p in imgs)
        elapsed = time.perf_counter() - t0
        report["measured_fps"] = round(len(imgs) / elapsed, 2) if elapsed else None
        report["total_detections"] = detections
        report["note"] = (
            "measured_fps is wall-clock throughput of the PLACEHOLDER detector on "
            "CPU over sample images — not a Jetson/TensorRT figure and not comparable "
            "to the CV-2 gate (>=30 FPS)."
        )
    else:
        report["measured_fps"] = "PENDING — no images available"

    (OUT_DIR / "last_run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
