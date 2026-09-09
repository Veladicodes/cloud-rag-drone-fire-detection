"""The detector must always return the right *shape* of output, in every mode,
so the rest of the pipeline can depend on it."""
from __future__ import annotations

from ai.models.yolo_detector import detect, get_detector


def test_detector_output_contract():
    dets = detect(b"any-bytes-frame-0007")
    assert isinstance(dets, list)
    for d in dets:
        assert set(d) >= {"bbox", "cls", "confidence", "backend"}
        assert len(d["bbox"]) == 4
        assert 0.0 <= d["confidence"] <= 1.0
        assert d["cls"] in {"smoke", "fire"}


def test_detector_is_deterministic_in_stub_mode():
    # conftest pins YOLO_MODE=stub
    assert get_detector().backend == "stub"
    assert detect(b"frame-A") == detect(b"frame-A")


def test_some_frames_produce_a_detection():
    hits = sum(len(detect(f"frame-{i}".encode())) for i in range(40))
    assert hits > 0, "stub detector should fire on at least some frames"
