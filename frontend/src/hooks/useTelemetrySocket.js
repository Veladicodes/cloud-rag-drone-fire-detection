import { useEffect, useRef, useState } from "react";
import { WS_TELEMETRY } from "../services/api.js";

// Live telemetry + incident events over the backend WebSocket.
export function useTelemetrySocket() {
  const [drones, setDrones] = useState({}); // call_sign -> {lat, lon, battery_pct, ...}
  const [events, setEvents] = useState([]); // incident / plan_ready notifications
  const wsRef = useRef(null);

  useEffect(() => {
    let stop = false;
    function connect() {
      const ws = new WebSocket(WS_TELEMETRY);
      wsRef.current = ws;
      ws.onmessage = (m) => {
        const msg = JSON.parse(m.data);
        if (msg.type === "telemetry") {
          setDrones((d) => ({ ...d, [msg.call_sign]: msg }));
        } else if (msg.type === "incident" || msg.type === "plan_ready") {
          setEvents((e) => [{ ...msg, at: Date.now() }, ...e].slice(0, 50));
        }
      };
      ws.onclose = () => {
        if (!stop) setTimeout(connect, 1500);
      };
    }
    connect();
    return () => {
      stop = true;
      wsRef.current?.close();
    };
  }, []);

  return { drones, events };
}
