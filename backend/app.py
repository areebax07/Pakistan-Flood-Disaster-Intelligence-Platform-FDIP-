import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import requests
from supabase import create_client, Client

# Load environment variables from .env file
load_dotenv()

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))

app = Flask(__name__)
CORS(app)  # Enable CORS so your frontend can talk to this backend

# Initialize Supabase Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "success", "message": "FDIP Backend is running successfully!"})

# 1. Weather Route (Fetches live meteorological data via Open-Meteo)
@app.route("/api/weather", methods=["GET"])
def get_weather():
    lat = request.args.get("lat", "33.6844") # Default Islamabad lat
    lon = request.args.get("lon", "73.0479") # Default Islamabad lon
    
    # Open-Meteo API endpoint (Free, no key required)
    open_meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,wind_speed_10m"
    
    try:
        response = requests.get(open_meteo_url)
        data = response.json()
        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. Earthquakes Route (Fetches live seismic events from USGS)
@app.route("/api/earthquakes", methods=["GET"])
def get_earthquakes():
    usgs_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
    try:
        response = requests.get(usgs_url)
        data = response.json()
        return jsonify({"status": "success", "count": len(data.get("features", [])), "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 3. Alerts Route (Fetches active alerts from Supabase database)
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    try:
        response = supabase.table("alerts").select("*").execute()
        return jsonify({"status": "success", "data": response.data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 4. Map Overview / Live Telemetry Route (Aggregates external port feed and live data)
PORT_DATA_BASE = "http://203.135.4.150:3638/FLOOD_DATA_JSON"

@app.route("/api/map-overview", methods=["GET"])
def get_map_overview():
    """
    Aggregates all hazard points (floods, weather zones, telemetry nodes) 
    from the port directory and external APIs to populate the main map screen.
    """
    try:
        # Fetch coordinate listings or payload from the port
        port_response = requests.get(f"{PORT_DATA_BASE}/Cordinates_list/", timeout=5)
        port_data = port_response.json() if port_response.status_code == 200 else {}
        
        # Combine port data with live USGS/Open-Meteo context if necessary
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
