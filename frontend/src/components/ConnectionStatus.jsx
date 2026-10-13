// Small live/reconnecting indicator for the telemetry WebSocket.
export default function ConnectionStatus({ isConnected, droneCount }) {
  return (
    <div className="status-pill">
      <span className={`status-dot ${isConnected ? "live" : "down"}`} />
      {isConnected ? `live · ${droneCount} drone${droneCount === 1 ? "" : "s"}` : "reconnecting…"}
    </div>
  );
}
