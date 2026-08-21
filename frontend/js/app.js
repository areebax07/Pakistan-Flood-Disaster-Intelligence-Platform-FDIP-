// frontend/js/app.js

document.addEventListener("DOMContentLoaded", () => {
    console.log("[FDIP] Initializing tactical map application...");
    initMap();
});

let map;
let markerLayers = {
    flood: L.layerGroup(),
    earthquake: L.layerGroup(),
    weather: L.layerGroup(),
    aviation: L.layerGroup(),
    agriculture: L.layerGroup()
};

function initMap() {
    // Initialize Leaflet map centered over Pakistan matching prototype specs
    map = L.map('map', { zoomControl: false }).setView([30.3753, 69.3451], 6);

    // Dark theme tactical tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }).addTo(map);

    L.control.zoom({ position: 'bottomright' }).addTo(map);

    // Add default layers to map
    Object.values(markerLayers).forEach(layer => layer.addTo(map));

    // Fetch initial telemetry data from backend
    fetchMapData();
}

async function fetchMapData() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/map-overview');
        const result = await response.json();
        
        if (result.status === 'success') {
            console.log("[FDIP] Connected to telemetry server:", result.port_endpoint);
            // Render dynamic prototype markers here based on fetched response
        }
    } catch (error) {
        console.error("[FDIP] Error loading telemetry data:", error);
    }
}

// Layer filtering toggle matching prototype buttons
function toggleLayer(layerName) {
    if (markerLayers[layerName]) {
        if (map.hasLayer(markerLayers[layerName])) {
            map.removeLayer(markerLayers[layerName]);
        } else {
            map.addLayer(markerLayers[layerName]);
        }
    }
}