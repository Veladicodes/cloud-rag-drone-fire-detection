// Fixed, offline-measured evaluation results (see results/README.md).
// These are NOT live metrics from this running session — labelled "measured offline"
// so the dashboard never implies they were just computed.
const STATS = [
  { label: "Detection mAP@0.5", value: "0.733", unit: "", accent: "ember", note: "FireNet, finetuned YOLOv8n" },
  { label: "CPU Throughput", value: "37.3", unit: "FPS", accent: "safe", note: "512px, Ryzen 7 5800H" },
  { label: "Pipeline Latency", value: "73.4", unit: "ms p50", accent: "safe", note: "detect → alert → RAG (mock LLM)" },
  { label: "RAG Grounding", value: "0.827", unit: "BERTScore F1", accent: "ember", note: "0.0% hallucinated sources" },
  { label: "WS Throughput", value: "198", unit: "msg/s", accent: "safe", note: "10 concurrent drones, 0 errors" },
];

export default function StatTiles({ liveIncidentCount = 0, liveAlertCount = 0 }) {
  return (
    <div className="stats">
      {STATS.map((s) => (
        <div className={`stat-tile accent-${s.accent}`} key={s.label}>
          <div className="label">{s.label}</div>
          <div className="value">
            {s.value} {s.unit && <span className="unit">{s.unit}</span>}
          </div>
          <div className="note">{s.note}</div>
        </div>
      ))}
      <div className="stat-tile accent-ember live-tile">
        <div className="label">This Session</div>
        <div className="value">
          {liveIncidentCount} <span className="unit">incidents</span>
        </div>
        <div className="note">{liveAlertCount} alerts dispatched — live, not benchmarked</div>
      </div>
    </div>
  );
}
