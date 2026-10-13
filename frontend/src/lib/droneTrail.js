// Pure helper for appending to a capped flight-trail array, used by
// useTelemetrySocket.js to keep a bounded recent-position history per drone.
export const MAX_TRAIL_POINTS = 20;

export function pushTrailPoint(trail, point) {
  const next = [...trail, point];
  if (next.length > MAX_TRAIL_POINTS) {
    return next.slice(next.length - MAX_TRAIL_POINTS);
  }
  return next;
}
