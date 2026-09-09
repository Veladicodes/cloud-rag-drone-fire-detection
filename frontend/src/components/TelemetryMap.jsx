import { MapContainer, TileLayer, CircleMarker, Popup, Circle } from "react-leaflet";

// Live drone positions + latest incident marker.
export default function TelemetryMap({ drones, incidents }) {
  const list = Object.values(drones);
  const center = list[0] ? [list[0].lat, list[0].lon] : [34.0722, -118.2437];
  const latestIncident = incidents[0];

  return (
    <MapContainer id="map" center={center} zoom={12} scrollWheelZoom>
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {list.map((d) => (
        <CircleMarker
          key={d.call_sign}
          center={[d.lat, d.lon]}
          radius={7}
          pathOptions={{ color: "#5cbfa7", fillOpacity: 0.8 }}
        >
          <Popup>
            <b>{d.call_sign}</b>
            <br />
            battery {Number(d.battery_pct).toFixed(0)}%
            <br />
            bearing {Number(d.bearing_deg).toFixed(0)}&deg;
          </Popup>
        </CircleMarker>
      ))}
      {latestIncident && (
        <>
          <CircleMarker
            center={[latestIncident.lat, latestIncident.lon]}
            radius={10}
            pathOptions={{ color: "#f2792f", fillOpacity: 0.9 }}
          >
            <Popup>
              incident #{latestIncident.incident_id} &mdash; {latestIncident.detected_class}{" "}
              {Number(latestIncident.confidence).toFixed(2)}
            </Popup>
          </CircleMarker>
          <Circle
            center={[latestIncident.lat, latestIncident.lon]}
            radius={2000}
            pathOptions={{ color: "#f2792f", fillOpacity: 0.05 }}
          />
        </>
      )}
    </MapContainer>
  );
}
