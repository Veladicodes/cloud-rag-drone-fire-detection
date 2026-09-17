// HTTP + WS client for the local FastAPI backend.
// LOCAL STAND-IN FOR: calls to the Azure Container Apps-hosted API gateway.
const BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
// Viewer key for the read-only telemetry stream (see backend/core/auth.py).
// NOTE: baked into the built bundle, so this is a "shared link" level boundary,
// not a real secret - it only guards the demo WS endpoint from randos, not
// from anyone who can view the deployed dashboard's JS.
const API_KEY = import.meta.env.VITE_API_KEY || "";

export const WS_TELEMETRY =
  BASE.replace(/^http/, "ws") + "/ws/telemetry" + (API_KEY ? `?api_key=${encodeURIComponent(API_KEY)}` : "");

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
