# 🌊 Real-Time Flood & Disaster Management Portal

An advanced, real-time geospatial disaster management and environmental monitoring system designed to track floods, seismic activity, barrage water levels, and meteorological hazards. The platform integrates spatial datasets with a robust backend and cloud database infrastructure to provide instant tactical insights for disaster response teams and citizens.

---

## 📋 Table of Contents
1. [Architecture & Tech Stack](#-architecture--tech-stack)
2. [Project Directory Structure](#-project-directory-structure)
3. [Core Modules & Pages](#-core-modules--pages)
4. [Database Integration (Supabase)](#-database-integration-supabase)
5. [Deployment (Vercel)](#-deployment-vercel)
6. [Getting Started & Local Installation](#-getting-started--local-installation)

---

## 🛠️ Architecture & Tech Stack

| Component | Technology Used |
| :--- | :--- |
| **Frontend Architecture** | HTML5, CSS3, Vanilla JavaScript (`.html`, `.js`) |
| **Mapping & GIS** | Leaflet.js, Custom **GeoJSON** spatial vectors, HydroRIVERS GDB |
| **Backend Server** | Python (Flask/FastAPI via `app.py`), Node.js (`mapservice.js`) |
| **Database** | **Supabase (PostgreSQL)** for real-time telemetry and hazard logs |
| **Cloud Hosting & Deployment** | **Vercel** (Frontend & Serverless deployment) |

---
## 🌟 Core Modules & Pages

### 1. Central Command Dashboard (`index.html`)
* **Unified Overview:** Serves as the high-level operational landing page summarizing ongoing regional or national emergencies.
* **Live Telemetry Feed:** Displays active status indicators and quick-metrics across weather anomalies, rising flood levels, and recent seismic events.
* **Quick Navigation Hub:** Provides direct routing to specialized administrative and citizen portals.

### 2. Advanced GIS Mapping Interface (`map.html`)
* **GeoJSON Integration:** Utilizes custom spatial data files stored in the frontend directory to render dynamic vector boundaries, river networks, and risk zones.
* **Interactive Leaflet Layers:** Supports toggleable overlays for barrage infrastructure, seismic epicenters, and hazard zones.
* **Click-to-Inspect Telemetry:** Allows operators to click specific regional nodes to view localized hazard indicators.

### 3. Flood & Barrage Monitoring Module (`flood.html`)
* **Barrage Water-Level Tracking:** Monitors live upstream and downstream water discharge rates across critical barrage structures.
* **Geospatial Basin Routing:** Integrates processed river vectors derived from `HydroRIVERS_v10_as.gdb` and backend processing scripts to map catchment and overflow risks.
* **Inundation Warnings:** Highlights critical water thresholds and flood-prone districts using color-coded severity metrics.

### 4. Earthquake & Seismic Activity Tracker (`earthquake.html`)
* **Seismic Telemetry Feed:** Displays real-time feeds detailing recent tectonic tremors, Richter scale magnitudes, and focal depths.
* **Epicenter Visualization:** Plots epicenter markers on the interactive mapping interface with dynamic shockwave radius rings.

### 5. Weather Hazards & Alert Graphs (`weather.html` & `alerts.html`)
* **Meteorological Monitoring:** Tracks severe storms, heavy precipitation belts, and atmospheric anomalies.
* **Dynamic Alert Graphs:** Visualizes hazard escalation trends, water-level fluctuations, and emergency frequencies over customizable timeframes.
* **Notification Feed:** Maintains a live chronological log of system-generated hazard alerts.

### 6. Role-Based Portals (`admin.html` & `citizen.html`)
* **Administrative Control Panel (`admin.html`):** Empowers disaster management operators to push broadcast alerts, adjust barrage warning thresholds, and manage system data synced via Supabase.
* **Public Citizen Portal (`citizen.html`):** A streamlined, mobile-friendly interface for residents to check local safety warnings, shelter locations, and evacuation routes.

## 📂 Project Directory Structure

```text
├── backend/
│   ├── app.py                 # Core Python backend application server
│   ├── mapservice.js          # Spatial map services and routing handlers
│   ├── process_rivers.py      # Data extraction script for river vectors
│   └── data/
│       └── HydroRIVERS_v10_as.gdb # HydroRIVERS geodatabase for basin & water routing
└── frontend/
    ├── css/                   # Stylesheets for layouts, UI components, and themes
    ├── data/                  # GeoJSON spatial datasets and boundary files
    ├── images/                # Map markers, UI icons, and assets
    ├── js/                    # Client-side scripts for real-time telemetry and map rendering
    ├── admin.html             # Administrative control panel and emergency dispatch
    ├── alerts.html            # Real-time hazard notifications feed
    ├── citizen.html           # Public-facing citizen portal and local safety feeds
    ├── earthquake.html        # Seismic activity tracker and epicenter mapping
    ├── flood.html             # Flood risk assessment and barrage water-level monitor
    ├── index.html             # Central command dashboard and high-level metrics
    ├── map.html               # Advanced interactive GIS mapping interface (GeoJSON layers)
    └── weather.html           # Meteorological hazard monitoring and alert graphs
