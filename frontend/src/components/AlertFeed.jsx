// Live list of dispatched alerts (immediate = raw SMS, enriched = post-RAG).
// These rows come from the `alerts` table the mock Alert Service writes to.
// When focusIncidentId is set, narrows to just that incident's alerts.
export default function AlertFeed({ alerts, focusIncidentId }) {
  const visible = focusIncidentId == null ? alerts : alerts.filter((a) => a.incident_id === focusIncidentId);
  return (
    <div className="feed">
      {visible.length === 0 && (
        <div className="empty">
          {focusIncidentId == null ? "no alerts yet — run the simulator" : "no alerts for this incident"}
        </div>
      )}
      {visible.map((a) => (
        <div className="row" key={a.id}>
          <span className={`tag ${a.alert_class}`}>{a.alert_class}</span>{" "}
          <b>{a.recipient_role}</b> <small style={{ color: "var(--text-faint)" }}>via {a.channel}</small>
          <span className="body-text">{a.body}</span>
        </div>
      ))}
    </div>
  );
}
