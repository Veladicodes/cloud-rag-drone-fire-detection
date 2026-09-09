"""Seed the local database with mock drones (+ optionally a sample incident).

    python -m database.seed            # drones only
    python -m database.seed --incident # also insert one sample incident + plan

LOCAL STAND-IN FOR: an Azure SQL seed/migration data step.
"""
from __future__ import annotations

import argparse

from backend.core.db import SessionLocal, init_db
from backend.services.pipeline import create_incident, run_rag_and_notify
from database.models import Drone

MOCK_DRONES = [
    {"call_sign": "SIM-1", "model": "sim-quad", "battery_pct": 96.0},
    {"call_sign": "SIM-2", "model": "sim-quad", "battery_pct": 88.0},
    {"call_sign": "SIM-3", "model": "sim-fixedwing", "battery_pct": 73.0},
]


def main(with_incident: bool = False) -> None:
    init_db()
    db = SessionLocal()
    try:
        created = 0
        for spec in MOCK_DRONES:
            if not db.query(Drone).filter_by(call_sign=spec["call_sign"]).one_or_none():
                db.add(Drone(**spec))
                created += 1
        db.commit()
        print(f"drones: {created} inserted, {db.query(Drone).count()} total")

        if with_incident:
            inc = create_incident(db, {
                "lat": 34.0722, "lon": -118.2437, "confidence": 0.91,
                "detected_class": "smoke", "wind_speed_kmh": 18, "wind_dir_deg": 200,
                "temperature_c": 33, "fuel_dryness": "high",
            })
            run_rag_and_notify(db, inc.id)
            print(f"sample incident #{inc.id} inserted with response plan")
    finally:
        db.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--incident", action="store_true", help="also insert a sample incident + plan")
    main(with_incident=ap.parse_args().incident)
