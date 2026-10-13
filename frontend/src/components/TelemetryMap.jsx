import { MapContainer, TileLayer, Marker, Popup, Circle, Polyline } from "react-leaflet";
import { divIcon } from "leaflet";
import { colorForCallSign, shortLabel } from "../lib/droneIdentity.js";
import MapLegend from "./MapLegend.jsx";

function droneIcon(callSign) {
  const color = colorForCallSign(callSign);
  return divIcon({
    className: "",
    html: `<div class="drone-icon" style="background:${color}"></div><div class="drone-label">${shortLabel(callSign)}</div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7],
  });
}

// confidence 0.35 -> 1.0 maps to ring size 14px -> 26px, floored so nothing is unclickable.
function incidentIcon(confidence, isFocused) {
  const size = Math.round(14 + Math.max(0, Math.min(1, (confidence - 0.35) / 0.65)) * 12);
  return divIcon({
    className: "",
    html: `<div class="incident-icon${isFocused ? " focused" : ""}" style="width:${size}px;height:${size}px"></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });
}

// Live drone positions (with trails) + up to 10 recent incidents, confidence-scaled.
export default function TelemetryMap({ drones, incidents, focusedIncidentId, onFocusIncident }) {
  const list = Object.values(drones);
  const center = list[0] ? [list[0].lat, list[0].lon] : [34.0722, -118.2437];
  const recentIncidents = incidents.slice(0, 10);

  return (
    <div style={{ position: "relative" }}>
      <MapContainer id="map" center={center} zoom={12} scrollWheelZoom>
        <TileLayer
          attribution='&copy; OpenStreetMap &copy; CARTO'
          url="https://{s}.basemaps.cartocdn.com/dark_matter/{z}/{x}/{y}{r}.png"
        />
        {list.map((d) => (
          <div key={d.call_sign}>
            {d.trail?.length > 1 && (
              <Polyline
                positions={d.trail}
                pathOptions={{ color: colorForCallSign(d.call_sign), weight: 2, opacity: 0.4 }}
              />
            )}
            <Marker position={[d.lat, d.lon]} icon={droneIcon(d.call_sign)}>
              <Popup>
                <b>{d.call_sign}</b>
                <br />
                altitude {Number(d.altitude_m).toFixed(0)} m
                <br />
                battery {Number(d.battery_pct).toFixed(0)}%
                <br />
                bearing {Number(d.bearing_deg).toFixed(0)}&deg;
              </Popup>
            </Marker>
          </div>
        ))}
        {recentIncidents.map((inc) => {
          const isFocused = focusedIncidentId === inc.incident_id;
          const dimmed = focusedIncidentId != null && !isFocused;
          return (
            <div key={inc.incident_id} style={{ opacity: dimmed ? 0.25 : 1 }}>
              <Marker
                position={[inc.lat, inc.lon]}
                icon={incidentIcon(inc.confidence, isFocused)}
                eventHandlers={{ click: () => onFocusIncident?.(inc.incident_id) }}
              >
                <Popup>
                  incident #{inc.incident_id} &mdash; {inc.detected_class}{" "}
                  {Number(inc.confidence).toFixed(2)}
                </Popup>
              </Marker>
              {isFocused && (
                <Circle
                  center={[inc.lat, inc.lon]}
                  radius={2000}
                  pathOptions={{ color: "#ff7a33", fillOpacity: 0.08, weight: 1 }}
                />
              )}
            </div>
          );
        })}
      </MapContainer>
      <MapLegend />
    </div>
  );
}
