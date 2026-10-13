import { useEffect, useRef, useState } from "react";
import { WS_TELEMETRY } from "../services/api.js";
import { pushTrailPoint } from "../lib/droneTrail.js";

// Live telemetry + incident events over the backend WebSocket.
export function useTelemetrySocket() {
  const [drones, setDrones] = useState({}); // call_sign -> {lat, lon, battery_pct, trail, lastSeen, ...}
  const [events, setEvents] = useState([]); // incident / plan_ready notifications
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);

  useEffect(() => {
    let stop = false;
    function connect() {
      const ws = new WebSocket(WS_TELEMETRY);
      wsRef.current = ws;
      ws.onopen = () => setIsConnected(true);
      ws.onmessage = (m) => {
        const msg = JSON.parse(m.data);
        if (msg.type === "telemetry") {
          setDrones((d) => {
            const prevTrail = d[msg.call_sign]?.trail ?? [];
            return {
              ...d,
              [msg.call_sign]: {
                ...msg,
                trail: pushTrailPoint(prevTrail, [msg.lat, msg.lon]),
                lastSeen: Date.now(),
              },
            };
          });
        } else if (msg.type === "incident" || msg.type === "plan_ready") {
          setEvents((e) => [{ ...msg, at: Date.now() }, ...e].slice(0, 50));
        }
      };
      ws.onclose = () => {
        setIsConnected(false);
        if (!stop) setTimeout(connect, 1500);
      };
    }
    connect();
    return () => {
      stop = true;
      wsRef.current?.close();
    };
  }, []);

  return { drones, events, isConnected };
}
