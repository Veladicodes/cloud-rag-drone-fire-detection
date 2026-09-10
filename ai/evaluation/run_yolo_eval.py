"""YOLO evaluation — real metrics on the held-out data.

  * detect : ultralytics model.val() on the FireNet YOLO val split -> real
             mAP@0.5, mAP@0.5:0.95, precision, recall, and a measured CPU FPS.
  * cls    : (if FLAME classifier weights exist) top-1 accuracy on the held-out
             FLAME Test/ slice. Whole-frame classifier, NOT a bounding-box
             detector — reported separately and labelled as such.

If no fine-tuned weights exist yet, falls back to timing the COCO placeholder
over the synthetic sample frames and writes PENDING for mAP (Phase-2 behaviour).

    python -m ai.evaluation.run_yolo_eval             # auto: whatever weights exist
    python -m ai.evaluation.run_yolo_eval --task detect
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from backend.core.config import REPO_ROOT, get_settings

OUT_DIR = REPO_ROOT / "results" / "yolo-metrics"
FIRENET_YAML = REPO_ROOT / "data" / "firenet_yolo" / "firenet.yaml"
FIRENET_VAL_IMG = REPO_ROOT / "data" / "firenet_yolo" / "images" / "val"
FLAME_CLS_DIR = REPO_ROOT / "data" / "flame_cls"
DET_WEIGHTS = REPO_ROOT / "ai" / "models" / "weights" / "wildfire_yolov8n.pt"
CLS_WEIGHTS = REPO_ROOT / "ai" / "models" / "weights" / "wildfire_yolov8n_cls.pt"
SAMPLE_DIR = REPO_ROOT / "testing" / "sample_images"

# CV-1 / CV-2 gates (docs/management/milestones.md)
GATE_MAP50 = 0.88
GATE_FPS = 30.0


def _fps(model, images: list[Path], imgsz: int) -> float:
    if not images:
        return 0.0
    t0 = time.perf_counter()
    for p in images:
        model.predict(str(p), imgsz=imgsz, verbose=False, device="cpu")
    dt = time.perf_counter() - t0
    return round(len(images) / dt, 2) if dt else 0.0


def eval_detect() -> dict:
    from ultralytics import YOLO

    if not (DET_WEIGHTS.exists() and FIRENET_YAML.exists()):
        return {"status": "PENDING",
                "reason": "no fine-tuned detector yet -- run `python -m ai.models.train_yolo detect`"}
    model = YOLO(str(DET_WEIGHTS))
    m = model.val(data=str(FIRENET_YAML), split="val", device="cpu", imgsz=512, verbose=False)
    fps = _fps(model, sorted(FIRENET_VAL_IMG.glob("*.jpg")), imgsz=512)
    map50, map5095 = float(m.box.map50), float(m.box.map)
    return {
        "status": "MEASURED",
        "task": "detect", "dataset": "FireNet YOLO val (90 images, class 'fire')",
        "weights": str(DET_WEIGHTS.relative_to(REPO_ROOT)),
        "command": "python -m ai.evaluation.run_yolo_eval --task detect",
        "mAP@0.5": round(map50, 4),
        "mAP@0.5:0.95": round(map5095, 4),
        "precision": round(float(m.box.mp), 4),
        "recall": round(float(m.box.mr), 4),
        "measured_fps_cpu": fps,
        "gate_CV1_mAP50_target": GATE_MAP50,
        "gate_CV1_met": bool(map50 >= GATE_MAP50),
        "gate_CV2_fps_target": GATE_FPS,
        "gate_CV2_met_on_cpu": bool(fps >= GATE_FPS),
        "gate_CV2_note": "measured on CPU; CV-2 is defined for Jetson Orin + TensorRT, so a "
                         "CPU FPS below 30 is expected and is not a like-for-like miss.",
    }


def eval_cls() -> dict:
    from ultralytics import YOLO

    if not (CLS_WEIGHTS.exists() and (FLAME_CLS_DIR / "test").exists()):
        return {"status": "PENDING",
                "reason": "no FLAME classifier yet -- run `python -m ai.models.train_yolo cls`"}
    model = YOLO(str(CLS_WEIGHTS))
    m = model.val(data=str(FLAME_CLS_DIR), split="test", device="cpu", imgsz=224, verbose=False)
    return {
        "status": "MEASURED",
        "task": "classify",
        "dataset": "FLAME frame-level Fire/No_Fire, held-out Test/ folder "
                   "(8,617 img; Fire capped at 4000/class here for a balanced eval)",
        "weights": str(CLS_WEIGHTS.relative_to(REPO_ROOT)),
        "command": "python -m ai.evaluation.run_yolo_eval --task cls",
        "top1_acc": round(float(m.top1), 4),
        "top5_acc": round(float(m.top5), 4),
        "note": "FLAME frame set is classification-only (no boxes) -> whole-frame classifier used "
                "as an approximation, NOT a real detector; not comparable to the CV-1 mAP gate.",
    }


def eval_placeholder() -> dict:
    from ai.models.yolo_detector import get_detector

    det = get_detector()
    imgs = sorted(p for p in SAMPLE_DIR.glob("**/*") if p.suffix.lower() in {".jpg", ".jpeg", ".png"})
    t0 = time.perf_counter()
    hits = sum(len(det.detect(str(p))) for p in imgs)
    dt = time.perf_counter() - t0
    return {
        "status": "PLACEHOLDER",
        "detector_backend": getattr(det, "backend", "unknown"),
        "num_images": len(imgs), "total_detections": hits,
        "measured_fps_cpu": round(len(imgs) / dt, 2) if (imgs and dt) else None,
        "mAP@0.5": "PENDING -- train a real detector first",
        "note": "placeholder COCO detector over synthetic sample frames; not a real metric.",
    }


def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", choices=["auto", "detect", "cls", "placeholder"], default="auto")
    a = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    report: dict = {"generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "config_yolo_mode": get_settings().yolo_mode}
    if a.task in ("auto", "detect"):
        report["detect"] = eval_detect()
    if a.task in ("auto", "cls"):
        report["classify"] = eval_cls()
    if a.task == "placeholder" or (
        a.task == "auto" and report.get("detect", {}).get("status") != "MEASURED"
    ):
        report["placeholder"] = eval_placeholder()

    (OUT_DIR / "last_run.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    main()
