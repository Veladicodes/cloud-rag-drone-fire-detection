import { useEffect, useState } from "react";
import { useTelemetrySocket } from "./hooks/useTelemetrySocket.js";
import { api } from "./services/api.js";
import TelemetryMap from "./components/TelemetryMap.jsx";
import AlertFeed from "./components/AlertFeed.jsx";
import ResponsePlanViewer from "./components/ResponsePlanViewer.jsx";
import StatTiles from "./components/StatTiles.jsx";
import ConnectionStatus from "./components/ConnectionStatus.jsx";
import DroneRoster from "./components/DroneRoster.jsx";
import IncidentTimeline from "./components/IncidentTimeline.jsx";
import OnboardingBanner from "./components/OnboardingBanner.jsx";
import IdleState from "./components/IdleState.jsx";
import RecipientSettingsPanel from "./components/RecipientSettingsPanel.jsx";

export default function App() {
  const { drones, events, isConnected } = useTelemetrySocket();
  const [alerts, setAlerts] = useState([]);
  const [incidents, setIncidents] = useState([]);
  const [health, setHealth] = useState(null);
  const [focusedIncidentId, setFocusedIncidentId] = useState(null);

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
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark">🔥</div>
          <div>
            <h1>FireWatch</h1>
            <span className="sub">
              Wildfire Drone Operator Dashboard ·{" "}
              {health
                ? `llm=${health.llm_mode} · yolo=${health.yolo_mode} · storage=${health.storage_mode}`
                : "connecting…"}
            </span>
          </div>
        </div>
        <ConnectionStatus isConnected={isConnected} droneCount={Object.keys(drones).length} />
      </header>

      <OnboardingBanner />

      <StatTiles liveIncidentCount={incidentEvents.length} liveAlertCount={alerts.length} />

      <div className="grid">
        <div className="panel">
          <h2>
            Telemetry &amp; active incident
            <span className="count">{Object.keys(drones).length} live</span>
          </h2>
          {Object.keys(drones).length === 0 ? (
            <IdleState />
          ) : (
            <TelemetryMap
              drones={drones}
              incidents={incidentEvents}
              focusedIncidentId={focusedIncidentId}
              onFocusIncident={setFocusedIncidentId}
            />
          )}
          <div className="panel" style={{ marginTop: 12 }}>
            <h2>Drone roster</h2>
            <DroneRoster drones={drones} />
          </div>
          <div className="panel" style={{ marginTop: 12 }}>
            <h2>
              Incident timeline
              <span className="count">{incidentEvents.length}</span>
            </h2>
            <IncidentTimeline
              incidents={incidentEvents}
              focusedIncidentId={focusedIncidentId}
              onFocusIncident={setFocusedIncidentId}
            />
          </div>
        </div>
        <div style={{ display: "grid", gap: 14 }}>
          <div className="panel">
            <h2>
              Alert feed
              <span className="count">{alerts.length}</span>
            </h2>
            <AlertFeed alerts={alerts} focusIncidentId={focusedIncidentId} />
          </div>
          <div className="panel">
            <h2>RAG response plan</h2>
            <ResponsePlanViewer
              incidents={incidents}
              focusIncidentId={focusedIncidentId}
              onFocusIncident={setFocusedIncidentId}
            />
          </div>
          <div className="panel">
            <h2>Alert recipients</h2>
            <RecipientSettingsPanel />
          </div>
        </div>
      </div>
    </>
  );
}
