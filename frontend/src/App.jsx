import { useEffect, useState } from "react";
import { useTelemetrySocket } from "./hooks/useTelemetrySocket.js";
import { api } from "./services/api.js";
import TelemetryMap from "./components/TelemetryMap.jsx";
import AlertFeed from "./components/AlertFeed.jsx";
import ResponsePlanViewer from "./components/ResponsePlanViewer.jsx";

export default function App() {
  const { drones, events } = useTelemetrySocket();
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [health, setHealth] = useState(null);

  // Poll REST for alerts + incidents; WS events just trigger a refresh.
  useEffect(() => {
    let alive = true;
    const pull = () => {
      api.alerts().then((a) => alive && setAlerts(a)).catch(() => {});
      api.incidents().then((i) => alive && setIncidents(i)).catch(() => {});
    };
    pull();
    const t = setInterval(pull, 2000);
    api.health().then(setHealth).catch(() => {});
    return () => {
      alive = false;
      clearInterval(t);
    };
  }, [events.length]);

  const incidentEvents = events.filter((e) => e.type === "incident");

  return (
    <>
      <header>
        <h1>Wildfire Drone Operator Dashboard</h1>
        <small>
          local prototype — {Object.keys(drones).length} drones live ·{" "}
          {health ? `llm_mode=${health.llm_mode}, yolo_mode=${health.yolo_mode}` : "connecting…"} ·
          all cloud services are local stand-ins
        </small>
      </header>
      <div className="grid">
        <div className="panel">
          <h2>Telemetry & active incident</h2>
          <TelemetryMap drones={drones} incidents={incidentEvents} />
        </div>
        <div style={{ display: "grid", gap: 12 }}>
          <div className="panel">
            <h2>Alert feed ({alerts.length})</h2>
            <AlertFeed alerts={alerts} />
          </div>
          <div className="panel">
            <h2>RAG response plan</h2>
            <ResponsePlanViewer incidents={incidents} />
          </div>
        </div>
      </div>
    </>
  );
}
