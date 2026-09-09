"""Edge YOLO detector wrapper.

IMPORTANT: in this prototype the detector runs **pretrained COCO `yolov8n.pt`**,
NOT a wildfire-fine-tuned model. It is a structural placeholder so the rest of
the pipeline (incident creation, alerting, RAG context) can be built and tested
end-to-end against realistic-shaped output. Real fine-tuning on FLAME/FireNet
per ADR-001 / `docs/research/yolo-detection.md` is Review-2 work.

Modes (YOLO_MODE):
    auto -> ultralytics yolov8n.pt if importable, else STUB
    stub -> deterministic synthetic detection (no ML deps), clearly labelled

Output contract (matches the fields `database.models.Incident` expects):
    [{ "bbox": [x1, y1, x2, y2], "cls": "smoke"|"fire", "confidence": float,
       "backend": "yolov8n-coco-placeholder" | "stub" }]
"""
from __future__ import annotations

import hashlib
import logging
from pathlib import Path

log = logging.getLogger(__name__)

# COCO class ids we loosely map onto wildfire proxy classes for the placeholder.
_COCO_PROXY = {0: "smoke", 2: "smoke", 7: "fire", 9: "fire"}


class _StubDetector:
    backend = "stub"

    def detect(self, image_ref: str | bytes) -> list[dict]:
        seed = hashlib.md5(image_ref if isinstance(image_ref, bytes) else str(image_ref).encode())
        h = int(seed.hexdigest(), 16)
        # ~60% of frames produce a detection; deterministic per input.
        if h % 10 < 4:
            return []
        conf = 0.35 + (h % 60) / 100.0
        cls = "fire" if h % 3 == 0 else "smoke"
        x = h % 300
        y = (h // 7) % 300
        return [{
            "bbox": [float(x), float(y), float(x + 120), float(y + 90)],
            "cls": cls,
            "confidence": round(conf, 3),
            "backend": self.backend,
        }]


class _UltralyticsDetector:
    backend = "yolov8n-coco-placeholder"

    def __init__(self) -> None:
        from ultralytics import YOLO

        self._model = YOLO("yolov8n.pt")  # auto-downloads once to repo root

    def detect(self, image_ref: str | bytes) -> list[dict]:
        import io

        import numpy as np
        from PIL import Image

        if isinstance(image_ref, bytes):
            src = np.array(Image.open(io.BytesIO(image_ref)).convert("RGB"))
        else:
            src = str(image_ref)

        out: list[dict] = []
        for res in self._model.predict(src, verbose=False):
            for box in res.boxes:
                cls_id = int(box.cls[0])
                out.append({
                    "bbox": [float(v) for v in box.xyxy[0].tolist()],
                    "cls": _COCO_PROXY.get(cls_id, "smoke"),
                    "confidence": round(float(box.conf[0]), 3),
                    "backend": self.backend,
                })
        return out


_cached = None


def get_detector():
    global _cached
    if _cached is not None:
        return _cached

    from backend.core.config import get_settings

    mode = get_settings().yolo_mode.lower()
    if mode != "stub":
        try:
            _cached = _UltralyticsDetector()
            log.info("YOLO detector: %s (PLACEHOLDER — not wildfire-fine-tuned)", _cached.backend)
            return _cached
        except Exception as exc:  # noqa: BLE001
            log.warning("ultralytics unavailable (%s) -> STUB detector", exc)

    _cached = _StubDetector()
    log.warning("YOLO detector: STUB (synthetic detections)")
    return _cached


def detect(image_ref: str | bytes) -> list[dict]:
    return get_detector().detect(image_ref)
