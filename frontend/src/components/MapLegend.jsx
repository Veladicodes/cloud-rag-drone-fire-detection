// Fixed overlay explaining map symbols at a glance — no guessing required.
export default function MapLegend() {
  return (
    <div className="map-legend">
      <div className="legend-row">
        <span className="legend-swatch drone" /> Drone (live telemetry)
      </div>
      <div className="legend-row">
        <span className="legend-swatch incident" /> Fire / smoke detection
      </div>
      <div className="legend-row">
        <span className="legend-note">ring size = confidence</span>
      </div>
      <div className="legend-row">
        <span className="legend-swatch trail" /> Flight path (last ~20 pts)
      </div>
    </div>
  );
}
