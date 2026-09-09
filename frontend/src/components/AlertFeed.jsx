// Live list of dispatched alerts (immediate = raw SMS, enriched = post-RAG).
// These rows come from the `alerts` table the mock Alert Service writes to.
export default function AlertFeed({ alerts }) {
  return (
    <div className="feed">
      {alerts.length === 0 && <div className="row">no alerts yet — run the simulator</div>}
      {alerts.map((a) => (
        <div className="row" key={a.id}>
          <span className={`tag ${a.alert_class}`}>{a.alert_class}</span>{" "}
          <b>{a.recipient_role}</b> <small>via {a.channel}</small>
          <div>
            <small>{a.body}</small>
          </div>
        </div>
      ))}
    </div>
  );
}
