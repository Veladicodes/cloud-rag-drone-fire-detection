# Results & Metrics

**Rule (from the implementation brief): no fabricated numbers.** Every value here
comes from an actual run of actual code, or it is marked `PENDING` with the reason.

## Measured (local prototype)

| Metric | How it is produced | Where |
| :--- | :--- | :--- |
| End-to-end pipeline works | `pytest testing/unit/test_incidents_route.py` — POST incident ⇒ `alerts` row + `response_plans` row created, immediate alert ≤ enriched alert | CI / local |
| RAG retrieval returns k ranked chunks with non-decreasing true-L2 distance | `pytest testing/unit/test_rag_retrieve.py` | CI / local |
| Detector output contract (bbox / cls / confidence) holds in every mode | `pytest testing/unit/test_yolo_detector.py` | CI / local |
| Placeholder-detector throughput on CPU over sample frames | `python -m ai.evaluation.run_yolo_eval` → `results/yolo-metrics/last_run.json` | local |
| Detection → first mock-SMS log line latency | timestamp delta in `logs/alerts.log` after a simulator run | local |

## PENDING (needs resources this pass does not have)

| Metric | Blocked on |
| :--- | :--- |
| Real YOLO mAP@0.5 / mAP@0.5:0.95 (gate CV-1) | FLAME + FireNet dataset download and fine-tuning per ADR-001 |
| Real edge FPS on Jetson + TensorRT (gate CV-2) | physical/emulated Jetson hardware |
| Bandwidth reduction ≥ 70 % (gate CL-1) | a measured raw-video baseline to compare against |
| RAG retrieval recall ≥ 90 % (gate CG-1) | a labelled query→SOP relevance set |
| Hallucination rate ≤ 1 % (gate CG-2) | a real LLM (`LLM_MODE=azure`) + a scored test-prompt set; the current pipeline runs `[MOCK LLM OUTPUT]` |
| AL-1 (detection → SMS ≤ 15 s) against a *real* provider | Azure Communication Services credentials; the local number is mock-dispatch only |

Subfolders `yolo-metrics/`, `rag-metrics/`, `latency/` hold machine-written run
outputs (git-ignored except for this README and `.gitkeep`).
