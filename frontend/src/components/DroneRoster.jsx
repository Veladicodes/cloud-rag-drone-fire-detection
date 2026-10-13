import { useEffect, useState } from "react";
import { colorForCallSign } from "../lib/droneIdentity.js";

function batteryClass(pct) {
  if (pct < 20) return "low";
  if (pct < 50) return "mid";
  return "ok";
}

function secondsAgo(ts) {
  return Math.max(0, Math.round((Date.now() - ts) / 1000));
}

// Text-form answer to "which drone is which" — color swatch matches the map marker.
export default function DroneRoster({ drones }) {
  const list = Object.values(drones);
  const [, setTick] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setTick((n) => n + 1), 1000);
    return () => clearInterval(t);
  }, []);

  if (list.length === 0) {
    return <div className="empty">no drones connected</div>;
  }

  return (
    <div className="roster">
      {list.map((d) => (
        <div className="roster-row" key={d.call_sign}>
          <span className="roster-swatch" style={{ background: colorForCallSign(d.call_sign) }} />
          <b>{d.call_sign}</b>
          <span className={`battery ${batteryClass(d.battery_pct)}`}>
            {Number(d.battery_pct).toFixed(0)}%
          </span>
          <span className="roster-meta">{Number(d.altitude_m).toFixed(0)}m</span>
          <span
            className="roster-meta bearing-arrow"
            style={{ transform: `rotate(${d.bearing_deg}deg)` }}
          >
            ↑
          </span>
          <span className="roster-meta faint">
            {d.lastSeen ? `${secondsAgo(d.lastSeen)}s ago` : "—"}
          </span>
        </div>
      ))}
    </div>
  );
}
