import os
import geopandas as gpd

# Define paths matching your project directory structure
GDB_PATH = os.path.join("data", "HydroRIVERS_v10_as.gdb")
OUTPUT_DIR = os.path.join("frontend", "data")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "pakistan_rivers.geojson")

# Pakistan Bounding Box [Min Longitude, Min Latitude, Max Longitude, Max Latitude]
PAKISTAN_BOUNDS = (60.87, 23.63, 77.84, 37.08)

def extract_pakistan_rivers():
    print(f"Reading dataset from: {GDB_PATH}...")

    # Load spatial data using pyogrio engine (fast & no fiona dependency)
    gdf = gpd.read_file(
        GDB_PATH, 
        bbox=PAKISTAN_BOUNDS, 
        engine="pyogrio"
    )
    print(f"Features loaded within Pakistan region: {len(gdf)}")

    # Filter out minor stream tributaries using Strahler Stream Order (ORD_STRA)
    # Stream order >= 3 retains primary rivers (Indus, Jhelum, Chenab, etc.) and major tributaries
    if "ORD_STRA" in gdf.columns:
        gdf = gdf[gdf["ORD_STRA"] >= 3]
        print(f"Filtered main river segments (ORD_STRA >= 3): {len(gdf)}")

    # Reproject to standard WGS84 coordinates (EPSG:4326) for Web Maps / Leaflet
    if gdf.crs is not None and gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs(epsg=4326)

    # Ensure output directory exists and export GeoJSON
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    gdf.to_file(OUTPUT_FILE, driver="GeoJSON", engine="pyogrio")
    print(f"Successfully generated: {OUTPUT_FILE}")

if __name__ == "__main__":
    extract_pakistan_rivers()