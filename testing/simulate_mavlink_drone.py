"""Protocol-realistic drone simulator - emits real MAVLink wire-format packets
over UDP using pymavlink (the library used by QGroundControl / Mission Planner
/ ArduPilot itself), instead of the hand-rolled JSON in simulate_drone.py.

This is NOT full ArduPilot SITL (no flight-dynamics model, no autopilot
binary - that needs a Linux build toolchain this project doesn't assume). It
sends genuine HEARTBEAT / GLOBAL_POSITION_INT / SYS_STATUS messages so the
receiving side (backend/services/mavlink_ingest.py) exercises real MAVLink
decoding, which is the protocol boundary this simulator exists to cover.

    python testing/simulate_mavlink_drone.py --iterations 60

Run backend/services/mavlink_ingest.py (or the backend with MAVLINK_ENABLED=true)
first so something is listening on udp:127.0.0.1:14550.
"""
from __future__ import annotations

import argparse
import random
import time

from pymavlink import mavutil

BASE_LAT, BASE_LON = 34.0722, -118.2437


def stream(endpoint: str, system_id: int, iterations: int, interval: float) -> None:
    conn = mavutil.mavlink_connection(endpoint, source_system=system_id)

    lat, lon, alt, battery, heading = BASE_LAT, BASE_LON, 90.0, 100.0, 0.0

    for tick in range(1, iterations + 1):
        conn.mav.heartbeat_send(
            mavutil.mavlink.MAV_TYPE_QUADROTOR,
            mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
            0, 0, mavutil.mavlink.MAV_STATE_ACTIVE,
        )

        lat += random.uniform(-0.0005, 0.0005)
        lon += random.uniform(-0.0005, 0.0005)
        heading = (heading + random.uniform(-10, 10)) % 360
        battery = max(5.0, battery - random.uniform(0.05, 0.3))

        conn.mav.global_position_int_send(
            int(time.time() * 1000) & 0xFFFFFFFF,
            int(lat * 1e7), int(lon * 1e7),
            int(alt * 1000), int(alt * 1000),
            0, 0, 0,
            int(heading * 100),
        )
        conn.mav.sys_status_send(
            0, 0, 0, 0,
            int(random.uniform(1150, 1260)),  # voltage_battery (mV)
            -1,
            int(battery),  # battery_remaining %
            0, 0, 0, 0, 0, 0,
        )

        print(f"[MAV-{system_id}] tick {tick:>3}: lat={lat:.5f} lon={lon:.5f} "
              f"alt={alt:.0f}m battery={battery:.1f}% hdg={heading:.0f}")
        time.sleep(interval)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--endpoint", default="udpout:127.0.0.1:14550",
                     help="MAVLink endpoint to send to - udpout: connects out to mavlink_ingest's udp: (bind/listen) socket")
    ap.add_argument("--system-id", type=int, default=1)
    ap.add_argument("--iterations", type=int, default=60)
    ap.add_argument("--interval", type=float, default=1.0)
    a = ap.parse_args()
    stream(a.endpoint, a.system_id, a.iterations, a.interval)


if __name__ == "__main__":
    main()
