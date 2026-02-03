import requests
import urllib.parse
import streamlit as st  # <--- Essential for accessing Secrets

class SatelliteUplink:
    def __init__(self):
        # 🔒 SECURE CONNECTION: Tries to get key from Cloud Vault first
        try:
            self.api_key = st.secrets["tomtom"]["api_key"]
        except FileNotFoundError:
            # Fallback for local testing if secrets.toml isn't found
            self.api_key = "9ejSySwpBOXEAnPkPpjbv8LuVmBmenrQ"
        
        self.base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

    def find_coordinates(self, location_name):
        # ... (Rest of your code stays exactly the same) ...
        # If you don't have the rest of the code handy, I can reprint the whole file.
        # But usually, you just need to change the __init__ part above.
        
        # JUST IN CASE, HERE IS THE COMPLETE STANDARD FUNCTION:
        try:
            search_url = f"https://api.tomtom.com/search/2/search/{urllib.parse.quote(location_name)}.json"
            response = requests.get(search_url, params={'key': self.api_key})
            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    best_match = results[0]
                    return best_match['position']['lat'], best_match['position']['lon'], best_match['address']['freeformAddress']
            return None, None, None
        except:
            return None, None, None

    def get_traffic_data(self, lat, lon):
        try:
            url = f"{self.base_url}?key={self.api_key}&point={lat},{lon}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                flow = data.get('flowSegmentData', {})
                
                # Extract Speed
                current_speed = flow.get('currentSpeed', 60)
                free_flow_speed = flow.get('freeFlowSpeed', 60)
                
                # Calculate Congestion (0.0 to 1.0)
                if free_flow_speed > 0:
                    congestion = 1 - (current_speed / free_flow_speed)
                else:
                    congestion = 0
                
                # Extract Delay
                delay = flow.get('currentTravelTime', 0) - flow.get('freeFlowTravelTime', 0)
                
                return {
                    'current_speed': current_speed,
                    'free_flow_speed': free_flow_speed,
                    'congestion': max(0, congestion),
                    'delay_seconds': max(0, delay)
                }
            return {'congestion': 0, 'delay_seconds': 0}
        except:
            return {'congestion': 0, 'delay_seconds': 0}