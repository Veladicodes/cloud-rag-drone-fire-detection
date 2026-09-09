"""Standalone drone simulator — drives the whole pipeline with no real hardware.

Streams telemetry for N virtual drones over the WebSocket, and every few ticks
runs the (placeholder) YOLO detector on a generated frame; any detection above
the confidence threshold is POSTed to /api/v1/incidents, which triggers the
immediate mock alert, the RAG plan, and the enriched mock alert.

    python testing/simulate_drone.py --iterations 30

Run the backend (uvicorn backend.main:app --port 8000) first.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import io
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import httpx  # noqa: E402
import websockets  # noqa: E402

from ai.models.yolo_detector import detect  # noqa: E402
from backend.core.config import get_settings  # noqa: E402

SETTINGS = get_settings()
BASE_LAT, BASE_LON = 34.0722, -118.2437


def _frame(seed: int) -> bytes:
    """Generate a small synthetic RGB frame (clearly a placeholder, not real imagery)."""
    try:
        from PIL import Image, ImageDraw

        rng = random.Random(seed)
        img = Image.new("RGB", (416, 416), (30 + rng.randint(0, 40), 60, 30))
        d = ImageDraw.Draw(img)
        for _ in range(rng.randint(2, 6)):
            x, y = rng.randint(0, 380), rng.randint(0, 380)
            grey = rng.randint(120, 220)
            d.ellipse([x, y, x + rng.randint(20, 90), y + rng.randint(20, 90)], fill=(grey, grey, grey))
        buf = io.BytesIO()
        img.save(buf, format="JPEG")
        return buf.getvalue()
    except Exception:
        return f"synthetic-frame-{seed}".encode()


async def stream(api: str, drones: int, iterations: int, interval: float, incident_every: int) -> None:
    ws_url = api.replace("http", "ws", 1) + "/ws/telemetry"
    positions = {
        f"SIM-{i+1}": [BASE_LAT + random.uniform(-0.05, 0.05), BASE_LON + random.uniform(-0.05, 0.05)]
        for i in range(drones)
    }
    battery = {cs: 100.0 for cs in positions}

    async with websockets.connect(ws_url) as ws, httpx.AsyncClient(timeout=30) as http:
        for tick in range(1, iterations + 1):
            for cs, pos in positions.items():
                pos[0] += random.uniform(-0.002, 0.002)
                pos[1] += random.uniform(-0.002, 0.002)
                battery[cs] = max(5.0, battery[cs] - random.uniform(0.1, 0.6))
                await ws.send(json.dumps({
                    "call_sign": cs, "lat": pos[0], "lon": pos[1],
                    "altitude_m": 90 + random.uniform(-5, 5),
                    "battery_pct": round(battery[cs], 1),
                    "bearing_deg": random.uniform(0, 359),
                }))
            print(f"tick {tick:>3}: telemetry x{drones}")

            if tick % incident_every == 0:
                cs = random.choice(list(positions))
                lat, lon = positions[cs]
                dets = detect(_frame(tick))
                strong = [d for d in dets if d["confidence"] >= SETTINGS.confidence_threshold]
                if strong:
                    best = max(strong, key=lambda d: d["confidence"])
                    payload = {
                        "lat": lat, "lon": lon,
                        "confidence": best["confidence"], "detected_class": best["cls"],
                        "image_base64": base64.b64encode(_frame(tick)).decode(),
                        "wind_speed_kmh": random.choice([8, 14, 22, 28]),
                        "wind_dir_deg": random.uniform(0, 359),
                        "temperature_c": random.uniform(24, 38),
                        "fuel_dryness": random.choice(["moderate", "high", "high"]),
                    }
                    r = await http.post(f"{api}/api/v1/incidents", json=payload)
                    print(f"  -> INCIDENT posted ({best['cls']} {best['confidence']:.2f}) "
                          f"[{best['backend']}] : {r.status_code} {r.json()}")
                else:
                    print(f"  -> detector: no detection above {SETTINGS.confidence_threshold}")

            await asyncio.sleep(interval)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default="http://127.0.0.1:8000")
    ap.add_argument("--drones", type=int, default=3)
    ap.add_argument("--iterations", type=int, default=30)
    ap.add_argument("--interval", type=float, default=1.0)
    ap.add_argument("--incident-every", type=int, default=6)
    a = ap.parse_args()
    asyncio.run(stream(a.api, a.drones, a.iterations, a.interval, a.incident_every))


if __name__ == "__main__":
    main()
