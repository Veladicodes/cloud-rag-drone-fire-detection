// HTTP + WS client for the local FastAPI backend.
// LOCAL STAND-IN FOR: calls to the Azure Container Apps-hosted API gateway.
const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export const WS_TELEMETRY = BASE.replace(/^http/, "ws") + "/ws/telemetry";

async function j(path) {
  const r = await fetch(BASE + path);
  if (!r.ok) throw new Error(`${path} -> ${r.status}`);
  return r.json();
}

export const api = {
  incidents: () => j("/api/v1/incidents"),
  alerts: () => j("/api/v1/alerts"),
  plan: (id) => j(`/api/v1/plans/${id}`),
  health: () => j("/health"),
};
