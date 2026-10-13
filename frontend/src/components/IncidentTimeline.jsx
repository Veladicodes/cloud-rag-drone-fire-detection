function secondsAgo(at) {
  return Math.max(0, Math.round((Date.now() - at) / 1000));
}

// Horizontal scroll strip of recent incidents; click to enter focus mode.
export default function IncidentTimeline({ incidents, focusedIncidentId, onFocusIncident }) {
  if (incidents.length === 0) {
    return <div className="empty">no incidents yet</div>;
  }

  return (
    <div className="timeline">
      {focusedIncidentId != null && (
        <button className="timeline-reset" onClick={() => onFocusIncident(null)}>
          ← showing all
        </button>
      )}
      <div className="timeline-strip">
        {incidents.slice(0, 10).map((inc) => {
          const isFocused = focusedIncidentId === inc.incident_id;
          return (
            <button
              key={inc.incident_id}
              className={`timeline-card${isFocused ? " focused" : ""}`}
              onClick={() => onFocusIncident(isFocused ? null : inc.incident_id)}
            >
              <div className="timeline-id">#{inc.incident_id}</div>
              <div className="timeline-class">{inc.detected_class}</div>
              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{ width: `${Math.round(inc.confidence * 100)}%` }}
                />
              </div>
              <div className="timeline-time">{secondsAgo(inc.at)}s ago</div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
