import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';


const POPUP_STYLE = `
  .leaflet-popup-content-wrapper {
    background: rgba(4, 14, 28, 0.95) !important;
    border: 1px solid rgba(0, 212, 255, 0.35) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 24px rgba(0, 212, 255, 0.18), 0 8px 32px rgba(0,0,0,0.7) !important;
    color: #c8e8f8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    padding: 0 !important;
  }
  .leaflet-popup-tip { background: rgba(4, 14, 28, 0.95) !important; }
  .leaflet-popup-content { margin: 12px 16px !important; }
  .leaflet-popup-close-button { color: #00d4ff !important; font-size: 18px !important; top: 6px !important; right: 8px !important; }
  .leaflet-popup-close-button:hover { color: #fff !important; }
  .leaflet-bar a { background: #040e1c !important; border-color: #0a3d52 !important; color: #00d4ff !important; }
  .leaflet-bar a:hover { background: #071828 !important; }
  .leaflet-control-attribution { background: rgba(2, 8, 16, 0.75) !important; color: #2e6a86 !important; font-size: 10px !important; }
  .leaflet-control-attribution a { color: #00d4ff !important; }
`;
if (typeof document !== 'undefined' && !document.getElementById('eld-map-style')) {
  const style = document.createElement('style');
  style.id = 'eld-map-style';
  style.textContent = POPUP_STYLE;
  document.head.appendChild(style);
}


const svgMarker = (color, glow, symbol) => {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="44" viewBox="0 0 32 44">
      <defs>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2.5" result="blur"/>
          <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
        </filter>
      </defs>
      <!-- drop shadow -->
      <ellipse cx="16" cy="42" rx="6" ry="2" fill="rgba(0,0,0,0.5)"/>
      <!-- pin body -->
      <path d="M16 2 C8 2 2 8 2 16 C2 26 16 42 16 42 C16 42 30 26 30 16 C30 8 24 2 16 2Z"
            fill="${color}" stroke="${glow}" stroke-width="1.5" filter="url(#glow)"/>
      <!-- inner circle -->
      <circle cx="16" cy="16" r="7" fill="rgba(2,8,16,0.8)" stroke="${glow}" stroke-width="1"/>
      <!-- symbol -->
      <text x="16" y="21" text-anchor="middle" font-size="10" font-weight="bold"
            font-family="monospace" fill="${glow}">${symbol}</text>
    </svg>`;
  return new L.DivIcon({
    html: svg,
    className: '',
    iconSize:   [32, 44],
    iconAnchor: [16, 44],
    popupAnchor:[0, -42],
  });
};

const currentIcon  = svgMarker('#0044aa', '#00d4ff', 'CUR');
const pickupIcon   = svgMarker('#006633', '#00ff99', 'PU');
const dropoffIcon  = svgMarker('#880022', '#ff3060', 'DO');
const restIcon     = svgMarker('#552200', '#ffaa00', 'REST');


const RouteMap = ({ route }) => {
  if (!route || !route.coordinates) {
    return (
      <div style={{
        height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center',
        background: 'rgba(4,14,28,0.6)', borderRadius: 14, color: '#2e6a86',
        fontFamily: 'monospace', fontSize: '0.85rem', letterSpacing: '0.08em',
        border: '1px solid rgba(0,212,255,0.1)'
      }}>
        NO ROUTE DATA AVAILABLE
      </div>
    );
  }

  const { current, pickup, dropoff } = route.coordinates;
  const waypoints  = route.waypoints  || [];
  const restStops  = route.rest_stops || [];

  
  const allPts = [current, pickup, dropoff, ...restStops.map(s => s.location)].filter(Boolean);
  const lats   = allPts.map(p => p[0]);
  const lngs   = allPts.map(p => p[1]);
  const center = [
    (Math.min(...lats) + Math.max(...lats)) / 2,
    (Math.min(...lngs) + Math.max(...lngs)) / 2,
  ];

  const PopupLabel = ({ title, sub }) => (
    <div>
      <div style={{ color: '#00d4ff', fontWeight: 700, fontSize: 12,
                    letterSpacing: '0.08em', textTransform: 'uppercase',
                    fontFamily: 'monospace', marginBottom: 2 }}>{title}</div>
      {sub && <div style={{ color: '#4a7a96', fontSize: 11 }}>{sub}</div>}
    </div>
  );

  return (
    <MapContainer center={center} zoom={6}
      style={{ height: 500, width: '100%', borderRadius: 14, background: '#020810' }}>

      {}
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        maxZoom={19}
      />

      {}
      {waypoints.length > 0 && (
        <Polyline positions={waypoints} color="#00d4ff" weight={3} opacity={0.85} />
      )}

      {}
      {waypoints.length > 0 && (
        <Polyline positions={waypoints} color="#00aacc" weight={8} opacity={0.15} />
      )}

      {}
      <Marker position={current} icon={currentIcon}>
        <Popup>
          <PopupLabel title="Current Location"
            sub={`${current[0].toFixed(4)}, ${current[1].toFixed(4)}`} />
        </Popup>
      </Marker>

      {}
      <Marker position={pickup} icon={pickupIcon}>
        <Popup>
          <PopupLabel title="Pickup Location"
            sub={`${pickup[0].toFixed(4)}, ${pickup[1].toFixed(4)}`} />
        </Popup>
      </Marker>

      {}
      <Marker position={dropoff} icon={dropoffIcon}>
        <Popup>
          <PopupLabel title="Dropoff Location"
            sub={`${dropoff[0].toFixed(4)}, ${dropoff[1].toFixed(4)}`} />
        </Popup>
      </Marker>

      {}
      {restStops.map((stop, i) => (
        <React.Fragment key={i}>
          {}
          <CircleMarker center={stop.location} radius={14}
            pathOptions={{ color: '#ffaa00', weight: 1, opacity: 0.25, fillOpacity: 0 }} />
          <Marker position={stop.location} icon={restIcon}>
            <Popup>
              <PopupLabel title={`Rest Stop ${i + 1}`}
                sub={`${stop.distance_from_start.toFixed(1)} mi from start`} />
            </Popup>
          </Marker>
        </React.Fragment>
      ))}
    </MapContainer>
  );
};

export default RouteMap;
