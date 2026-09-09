# Sample images

`synthetic_placeholder_*.jpg` are **generated test frames** (grey blobs on a
green field) — **not real wildfire imagery**. They exist so the pipeline runs
end to end with no dataset:

- `python -m ai.evaluation.run_yolo_eval` uses them to produce a real (CPU,
  placeholder-detector) throughput number; `mAP` stays `PENDING`.
- `testing/simulate_drone.py` can feed them through the detector instead of
  generating frames in memory.

**Before Review-2:** drop the real FLAME / FireNet data into `data/flame/`
(images + YOLO-format labels). `run_yolo_eval.py` picks it up automatically and
then reports real mAP / FPS.

Regenerate the placeholders:
```bash
python testing/sample_images/generate.py
```
