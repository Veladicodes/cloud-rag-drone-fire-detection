"""Real-MAVLink telemetry bridge.

LOCAL STAND-IN FOR: a Jetson companion computer's MAVLink relay into the cloud
ingestion API. Listens on a UDP MAVLink endpoint (real wire-format packets -
HEARTBEAT / GLOBAL_POSITION_INT / SYS_STATUS / ATTITUDE - decoded with
pymavlink, the same library ground-control software uses), and feeds decoded
telemetry into the same persistence + broadcast path as the JSON WebSocket
ingestion (telemetry_ingest.persist_telemetry).

Full ArduPilot SITL (a flight-dynamics model + autopilot binary) needs a Linux
build toolchain this project doesn't assume; testing/simulate_mavlink_drone.py
instead emits genuine MAVLink packets directly via pymavlink, which is what
this bridge actually has to parse - the protocol boundary this integration is
about, without requiring a full simulated airframe.

Off by default (MAVLINK_ENABLED=false). Enable locally with:
    MAVLINK_ENABLED=true python -m backend.services.mavlink_ingest
or let backend.main start it as a background thread when the env var is set.
"""
from __future__ import annotations

import logging
import threading
import time

logger = logging.getLogger(__name__)


def _lat_lon_from_int(value: int) -> float:
    """MAVLink packs lat/lon as int32 degrees * 1e7."""
    return value / 1e7


def run_bridge(endpoint: str = "udp:0.0.0.0:14550", broadcaster=None, stop_event: threading.Event | None = None) -> None:
    """Blocking loop: connect to a MAVLink endpoint and persist decoded telemetry.

    Call from a background thread (see backend.main). `broadcaster` is
    ws.manager.broadcast_threadsafe, kept injectable so tests don't need a
    running event loop.
    """
    from pymavlink import mavutil

    from backend.services.telemetry_ingest import persist_telemetry

    conn = mavutil.mavlink_connection(endpoint)
    logger.info("mavlink_ingest: listening on %s", endpoint)

    call_signs: dict[int, str] = {}  # MAVLink system_id -> call_sign
    last_fix: dict[int, dict] = {}

    while stop_event is None or not stop_event.is_set():
        msg = conn.recv_match(blocking=True, timeout=1.0)
        if msg is None:
            continue

        sys_id = msg.get_srcSystem()
        call_sign = call_signs.setdefault(sys_id, f"MAV-{sys_id}")
        mtype = msg.get_type()

        if mtype == "GLOBAL_POSITION_INT":
            fix = last_fix.setdefault(sys_id, {"call_sign": call_sign})
            fix["lat"] = _lat_lon_from_int(msg.lat)
            fix["lon"] = _lat_lon_from_int(msg.lon)
            fix["altitude_m"] = msg.relative_alt / 1000.0
            fix["bearing_deg"] = msg.hdg / 100.0 if msg.hdg != 65535 else fix.get("bearing_deg", 0.0)
        elif mtype == "SYS_STATUS":
            fix = last_fix.setdefault(sys_id, {"call_sign": call_sign})
            if msg.battery_remaining != -1:
                fix["battery_pct"] = float(msg.battery_remaining)
        else:
            continue

        fix = last_fix.get(sys_id)
        if fix and "lat" in fix and "lon" in fix:
            packet = dict(fix)
            persist_telemetry(packet)
            if broadcaster is not None:
                broadcaster({"type": "telemetry", **packet})


def start_background(endpoint: str = "udp:0.0.0.0:14550", broadcaster=None) -> threading.Event:
    """Start run_bridge in a daemon thread; returns the stop_event to signal shutdown."""
    stop_event = threading.Event()
    t = threading.Thread(
        target=run_bridge, args=(endpoint, broadcaster, stop_event), daemon=True, name="mavlink-ingest",
    )
    t.start()
    return stop_event


if __name__ == "__main__":
    import sys

    endpoint = sys.argv[1] if len(sys.argv) > 1 else "udp:0.0.0.0:14550"
    try:
        run_bridge(endpoint)
    except KeyboardInterrupt:
        time.sleep(0)
