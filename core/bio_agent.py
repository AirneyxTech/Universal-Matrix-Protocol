import requests

class BioMonitor:
    def __init__(self):
        # OpenMeteo Air Quality API (Free, No Key Needed)
        self.url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        self.lat = 6.5244  # Lagos Latitude
        self.lon = 3.3792  # Lagos Longitude

    def get_vital_signs(self):
        """
        Fetches the 'Lung Capacity' of Lagos (Air Quality).
        Returns: { 'aqi': int, 'risk_level': str, 'pm2_5': float }
        """
        try:
            params = {
                "latitude": self.lat,
                "longitude": self.lon,
                "current": ["pm2_5", "european_aqi"]
            }
            response = requests.get(self.url, params=params)
            data = response.json()
            
            current = data.get('current', {})
            pm25 = current.get('pm2_5', 50.0)
            aqi = current.get('european_aqi', 50)
            
            # Determine Bio-Risk
            if aqi < 20: risk = "SAFE"
            elif aqi < 40: risk = "MODERATE"
            else: risk = "TOXIC HAZARD"
            
            return {
                "aqi": aqi,
                "risk_level": risk,
                "pm2_5": pm25
            }
        except:
            return {"aqi": 55, "risk_level": "SENSOR OFFLINE", "pm2_5": 0}