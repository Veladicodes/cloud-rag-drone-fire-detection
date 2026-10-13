// Shown inside the map panel when no drones are connected yet — teaches
// instead of looking broken.
export default function IdleState() {
  return (
    <div className="idle-state">
      <div className="idle-icon">🛰️</div>
      <div className="idle-title">Waiting for drone telemetry</div>
      <div className="idle-desc">Start the simulator to bring the fleet online:</div>
      <code className="idle-cmd">python testing/simulate_drone.py --iterations 30 --incident-every 6</code>
    </div>
  );
}
