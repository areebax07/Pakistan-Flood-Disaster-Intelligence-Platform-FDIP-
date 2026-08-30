import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

# Define the absolute path to your frontend folder
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))

app = Flask(__name__, static_folder=frontend_dir, static_url_path='')
CORS(app)  # Enable CORS so your frontend can talk to this backend

# Initialize Supabase Client safely
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key) if url and key else None

# 1. Frontend Root Route (Serves your index.html user interface)
@app.route("/", methods=["GET"])
def home():
    return send_from_directory(frontend_dir, 'index.html')

# 2. Weather Route (Fetches live meteorological data via Open-Meteo)[cite: 1]
@app.route("/api/weather", methods=["GET"])
def get_weather():
    lat = request.args.get("lat", "33.6844") # Default Islamabad lat[cite: 1]
    lon = request.args.get("lon", "73.0479") # Default Islamabad lon[cite: 1]
    
    # Open-Meteo API endpoint (Free, no key required)[cite: 1]
    open_meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
    
    try:
        response = requests.get(open_meteo_url)
        data = response.json()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 3. Earthquakes Route (Fetches live seismic events from USGS)[cite: 1]
@app.route("/api/earthquakes", methods=["GET"])
def get_earthquakes():
    usgs_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"[cite: 1]
    try:
        response = requests.get(usgs_url)
        data = response.json()
        return jsonify({"status": "success", "count": len(data.get("features", [])), "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 4. Alerts Route (Fetches active alerts from Supabase database)[cite: 1]
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    try:
        if not supabase:
            return jsonify({"status": "error", "message": "Supabase credentials not configured"}), 500
        response = supabase.table("alerts").select("*").execute()[cite: 1]
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 5. Map Overview / Live Telemetry Route (Aggregates external port feed and live data)[cite: 1]
PORT_DATA_BASE = "http://203.135.4.150:3638/FLOOD_DATA_JSON"[cite: 1]

@app.route("/api/map-overview", methods=["GET"])
def get_map_overview():
    """
    Aggregates all hazard points (floods, weather zones, telemetry nodes) 
    from the port directory and external APIs to populate the main map screen.[cite: 1]
    """
    try:
        # Fetch coordinate listings or payload from the port[cite: 1]
        port_response = requests.get(f"{PORT_DATA_BASE}/Cordinates_list/", timeout=5)[cite: 1]
        port_data = port_response.json() if port_response.status_code == 200 else {}[cite: 1]
        
        # Combine port data with live USGS/Open-Meteo context if necessary[cite: 1]
        return jsonify({
            "status": "success",
            "message": "Telemetry data fetched successfully",
            "port_endpoint": PORT_DATA_BASE,
            "port_payload": port_data
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to reach telemetry port: {str(e)}"
        }), 500

# 6. Static Asset Server (Serves CSS, JS, GeoJSON maps, and other frontend assets)
@app.route("/<path:path>", methods=["GET"])
def serve_static_assets(path):
    file_path = os.path.join(frontend_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(frontend_dir, path)
    # Fallback to index.html for client-side routing
    return send_from_directory(frontend_dir, 'index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
