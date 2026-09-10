"""Fine-tune YOLOv8n on the real datasets (replaces the Phase-2 COCO placeholder).

Two real training targets, because the two datasets carry different labels:

  detect  -> FireNet (real Pascal-VOC bounding boxes, class 'fire')  [the true detector]
  cls     -> FLAME frame-level Fire/No_Fire (whole-image labels, NO boxes) [approximation]

Both start from `yolov8n.pt` / `yolov8n-cls.pt` (ADR-001's chosen architecture).
Fine-tuned weights are written to ai/models/weights/ ; the Phase-2 placeholder
yolov8n.pt is left untouched. `YOLO_MODE` (backend/core/config.py) switches the
runtime detector between 'placeholder' and 'finetuned'.

Usage:
    python -m ai.models.train_yolo detect --epochs 40 --imgsz 512
    python -m ai.models.train_yolo cls    --epochs 3  --imgsz 224
CPU-only is supported (slow); pass --fraction to subsample for a bounded run
(the fraction is recorded in the run's args.yaml and must be reported honestly).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from backend.core.config import REPO_ROOT

WEIGHTS_DIR = REPO_ROOT / "ai" / "models" / "weights"
RESULTS_DIR = REPO_ROOT / "results" / "yolo-metrics"


def _train_detect(a: argparse.Namespace) -> dict:
    from ultralytics import YOLO

    from ai.models.prepare_firenet import main as prep

    data_yaml = prep()
    model = YOLO("yolov8n.pt")
    r = model.train(
        data=str(data_yaml), epochs=a.epochs, imgsz=a.imgsz, batch=a.batch,
        device="cpu", workers=a.workers, fraction=a.fraction, seed=0,
        project=str(REPO_ROOT / "runs"), name="firenet_det", exist_ok=True, verbose=True,
        patience=a.epochs,  # no early stop — we want the honest full run
    )
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    best = Path(r.save_dir) / "weights" / "best.pt"
    out = WEIGHTS_DIR / "wildfire_yolov8n.pt"
    out.write_bytes(best.read_bytes())
    m = model.metrics or r
    box = getattr(m, "box", None)
    summary = {
        "task": "detect", "dataset": "FireNet (Pascal-VOC -> YOLO)", "base": "yolov8n.pt",
        "epochs": a.epochs, "imgsz": a.imgsz, "fraction": a.fraction,
        "mAP@0.5": float(box.map50) if box else None,
        "mAP@0.5:0.95": float(box.map) if box else None,
        "precision": float(box.mp) if box else None,
        "recall": float(box.mr) if box else None,
        "weights": str(out.relative_to(REPO_ROOT)),
        "run_dir": str(Path(r.save_dir).relative_to(REPO_ROOT)),
    }
    return summary


def _train_cls(a: argparse.Namespace) -> dict:
    from ultralytics import YOLO

    from ai.models.prepare_flame import main as prep

    data_dir = prep()
    model = YOLO("yolov8n-cls.pt")
    r = model.train(
        data=str(data_dir), epochs=a.epochs, imgsz=a.imgsz, batch=a.batch,
        device="cpu", workers=a.workers, fraction=a.fraction, seed=0,
        project=str(REPO_ROOT / "runs"), name="flame_cls", exist_ok=True, verbose=True,
        patience=a.epochs,
    )
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)
    best = Path(r.save_dir) / "weights" / "best.pt"
    out = WEIGHTS_DIR / "wildfire_yolov8n_cls.pt"
    out.write_bytes(best.read_bytes())
    top1 = getattr(model.metrics, "top1", None)
    summary = {
        "task": "classify", "dataset": "FLAME frame-level Fire/No_Fire", "base": "yolov8n-cls.pt",
        "epochs": a.epochs, "imgsz": a.imgsz, "fraction": a.fraction,
        "val_top1_acc": float(top1) if top1 is not None else None,
        "weights": str(out.relative_to(REPO_ROOT)),
        "run_dir": str(Path(r.save_dir).relative_to(REPO_ROOT)),
        "note": "FLAME frame set is classification-only; this is a whole-frame classifier, "
                "NOT a real bounding-box detector.",
    }
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("task", choices=["detect", "cls"])
    ap.add_argument("--epochs", type=int, default=40)
    ap.add_argument("--imgsz", type=int, default=512)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--fraction", type=float, default=1.0,
                    help="fraction of the training set to use (report honestly if < 1.0)")
    a = ap.parse_args()

    summary = _train_detect(a) if a.task == "detect" else _train_cls(a)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = RESULTS_DIR / f"train_{a.task}.json"
    dest.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\n=== training summary ===")
    print(json.dumps(summary, indent=2))
    print(f"written: {dest}")


if __name__ == "__main__":
    main()
