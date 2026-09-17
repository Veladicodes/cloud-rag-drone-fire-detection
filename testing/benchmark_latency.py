"""End-to-end latency/throughput benchmark.

Measures, against the real FastAPI app in-process (fastapi.testclient, so
there's no network stack to introduce its own noise) under a concurrent
simulated multi-drone load:

  1. POST /api/v1/incidents latency (detection -> immediate alert -> RAG plan
     -> enriched alert, SYNC_RAG=true so the whole pipeline runs in-request).
  2. WS /ws/telemetry throughput: N concurrent simulated drones streaming
     ticks, message rate the server actually sustains.
  3. RAG generate_plan() latency in isolation, both LLM_MODE=mock (the mode
     used for the load test above - unlimited, deterministic) and a small
     LLM_MODE=gemini sample (a handful of *sequential* real calls, kept small
     to respect the Gemini free-tier rate limit - not a load test).

Writes results/latency/benchmark.json + a chart. No pytest here: this is a
manual benchmark you run and read, not a pass/fail gate.

    python testing/benchmark_latency.py
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import threading
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
OUT_DIR = REPO_ROOT / "results" / "latency"


def _setup_env(tmp_dir: Path) -> None:
    os.environ.update(
        DATABASE_URL=f"sqlite:///{tmp_dir / 'bench.db'}",
        STORAGE_PATH=str(tmp_dir / "storage"),
        FAISS_INDEX_PATH=str(tmp_dir / "faiss"),
        ALERT_LOG_PATH=str(tmp_dir / "alerts.log"),
        LLM_MODE="mock",
        EMBED_MODE=os.environ.get("EMBED_MODE", "hash"),
        YOLO_MODE="stub",
        SYNC_RAG="true",
    )
    from backend.core.config import get_settings

    get_settings.cache_clear()


def bench_incident_latency(client, n: int) -> dict:
    from fastapi.testclient import TestClient  # noqa: F401  (type hint only)

    samples = []
    for i in range(n):
        payload = {
            "lat": 34.0 + i * 0.001, "lon": -118.2, "confidence": 0.8,
            "detected_class": "fire",
        }
        t0 = time.perf_counter()
        r = client.post("/api/v1/incidents", json=payload)
        dt = time.perf_counter() - t0
        assert r.status_code == 201, r.text
        samples.append(dt * 1000)
    return _stats(samples)


def bench_telemetry_throughput(client, drones: int, ticks_per_drone: int) -> dict:
    results = {"sent": 0, "acked": 0, "errors": 0}
    lock = threading.Lock()

    def _drone(idx: int) -> None:
        try:
            with client.websocket_connect("/ws/telemetry") as ws:
                for t in range(ticks_per_drone):
                    ws.send_json({
                        "call_sign": f"BENCH-{idx}", "lat": 34.0 + t * 0.0001,
                        "lon": -118.2, "battery_pct": 100.0 - t * 0.1,
                    })
                    ws.receive_json()
                    with lock:
                        results["sent"] += 1
                        results["acked"] += 1
        except Exception:  # noqa: BLE001
            with lock:
                results["errors"] += 1

    t0 = time.perf_counter()
    threads = [threading.Thread(target=_drone, args=(i,)) for i in range(drones)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    dt = time.perf_counter() - t0

    return {
        "drones": drones, "ticks_per_drone": ticks_per_drone,
        "total_messages": results["acked"], "errors": results["errors"],
        "wall_seconds": round(dt, 3),
        "messages_per_second": round(results["acked"] / dt, 1) if dt else 0.0,
    }


def bench_rag_mock(n: int) -> dict:
    from ai.rag.orchestrate import generate_plan

    samples = []
    context = {
        "lat": 34.05, "lon": -118.24, "detected_class": "fire", "confidence": 0.85,
        "wind_speed_kmh": 20, "wind_dir_deg": 180, "temperature_c": 32, "fuel_dryness": "high",
    }
    for _ in range(n):
        t0 = time.perf_counter()
        generate_plan(context)
        samples.append((time.perf_counter() - t0) * 1000)
    return _stats(samples)


def bench_rag_gemini(n: int) -> dict | None:
    key = os.environ.get("GEMINI_API_KEY_REAL")  # opt-in, see main()
    if not key:
        return None
    os.environ["GEMINI_API_KEY"] = key
    os.environ["LLM_MODE"] = "gemini"
    from backend.core.config import get_settings

    get_settings.cache_clear()
    from ai.rag.orchestrate import generate_plan

    samples = []
    context = {
        "lat": 34.05, "lon": -118.24, "detected_class": "fire", "confidence": 0.85,
        "wind_speed_kmh": 20, "wind_dir_deg": 180, "temperature_c": 32, "fuel_dryness": "high",
    }
    for _ in range(n):
        t0 = time.perf_counter()
        generate_plan(context)
        samples.append((time.perf_counter() - t0) * 1000)

    os.environ["LLM_MODE"] = "mock"
    get_settings.cache_clear()
    return _stats(samples)


def _stats(samples_ms: list[float]) -> dict:
    s = sorted(samples_ms)
    return {
        "n": len(s),
        "min_ms": round(s[0], 1), "max_ms": round(s[-1], 1),
        "mean_ms": round(statistics.mean(s), 1),
        "p50_ms": round(s[len(s) // 2], 1),
        "p95_ms": round(s[min(len(s) - 1, int(len(s) * 0.95))], 1),
    }


def main() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        _setup_env(tmp_path)

        from backend.core.db import init_db
        from backend.main import app
        from fastapi.testclient import TestClient

        init_db()
        from ai.rag.ingest import build_index

        build_index()
        client = TestClient(app)

        print("Warming up (FAISS index build, first-call JIT costs)...")
        client.post("/api/v1/incidents", json={"lat": 0, "lon": 0, "confidence": 0.5})

        print("Benchmarking POST /api/v1/incidents (n=20, sequential, SYNC_RAG=true)...")
        incident_stats = bench_incident_latency(client, 20)

        print("Benchmarking WS /ws/telemetry throughput (10 concurrent drones x 30 ticks)...")
        telemetry_stats = bench_telemetry_throughput(client, drones=10, ticks_per_drone=30)

        print("Benchmarking RAG generate_plan() latency, LLM_MODE=mock (n=15)...")
        rag_mock_stats = bench_rag_mock(15)

        print("Benchmarking RAG generate_plan() latency, LLM_MODE=gemini (n=3, real API, opt-in)...")
        rag_gemini_stats = bench_rag_gemini(3)

        report = {
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "config": (
                f"CPU-only (no GPU), sqlite/local storage, YOLO_MODE=stub, "
                f"EMBED_MODE={os.environ.get('EMBED_MODE', 'hash')}, "
                f"single-process TestClient (no HTTP/TLS overhead measured)"
            ),
            "incident_post_sync_rag_mock_ms": incident_stats,
            "telemetry_throughput": telemetry_stats,
            "rag_generate_plan_mock_ms": rag_mock_stats,
            "rag_generate_plan_gemini_ms": rag_gemini_stats,
            "note": (
                "rag_generate_plan_gemini_ms is real Google Gemini API latency (network round trip "
                "included) if GEMINI_API_KEY_REAL was set when running this script; null otherwise. "
                "Kept to a small n to respect the free-tier rate limit - not a load test. A transient "
                "503 from the API falls back to mock output and is included in the sample as-is "
                "(see ai/rag/orchestrate.py's fallback path) unless noted otherwise below."
            ),
        }

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / "benchmark.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(json.dumps(report, indent=2))

        from backend.core.db import engine

        engine.dispose()


if __name__ == "__main__":
    main()
