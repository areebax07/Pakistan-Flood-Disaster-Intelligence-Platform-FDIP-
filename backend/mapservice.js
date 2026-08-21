const API_BASE_URL = 'http://203.135.4.150:3638';

/**
 * Fetches real-time hazard and flood telemetry data from the designated port.
 * @returns {Promise<Object>} GeoJSON or structured hazard alert data
 */
export async function fetchFloodTelemetry() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/telemetry/hazards`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Network response failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch map telemetry data:', error);
    throw error;
  }
}