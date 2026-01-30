import requests
import json
from datetime import datetime
import pytz

def get_lagos_data():
    """
    Fetch real-time data for Lagos and return the normalized vector:
    [Traffic, Pollution, Economy]
    
    Traffic: Based on current hour in Lagos (Peak: 0.9, Off-Peak: 0.2)
    Pollution: Based on current temperature in Lagos from Open-Meteo API
    Economy: Based on Bitcoin price from CoinGecko API
    """
    
    try:
        # 1. TRAFFIC DATA (Based on Lagos local time)
        # Set Lagos timezone
        lagos_tz = pytz.timezone('Africa/Lagos')
        current_time = datetime.now(lagos_tz)
        current_hour = current_time.hour
        
        # Define peak hours (7-10 AM and 4-8 PM Lagos time)
        morning_peak = 7 <= current_hour <= 10
        evening_peak = 16 <= current_hour <= 20
        
        traffic_value = 0.9 if (morning_peak or evening_peak) else 0.2
        
        print(f"Lagos Time: {current_time.strftime('%H:%M')} - Traffic Score: {traffic_value}")
        
        # 2. POLLUTION DATA (Based on temperature from Open-Meteo)
        try:
            # Open-Meteo API for Lagos (6.5244° N, 3.3792° E)
            meteo_url = "https://api.open-meteo.com/v1/forecast"
            meteo_params = {
                'latitude': 6.5244,
                'longitude': 3.3792,
                'current': 'temperature_2m',
                'timezone': 'Africa/Lagos'
            }
            
            meteo_response = requests.get(meteo_url, params=meteo_params, timeout=5)
            meteo_data = meteo_response.json()
            
            if 'current' in meteo_data and 'temperature_2m' in meteo_data['current']:
                current_temp = meteo_data['current']['temperature_2m']
                
                # Normalize temperature to pollution score (Lagos temp range: 20°C to 40°C)
                # Formula: (temp - 20) / (40 - 20) -> gives 0-1 range
                pollution_value = (current_temp - 20) / 20
                
                # Clamp between 0.1 and 0.9 (never zero or max)
                pollution_value = max(0.1, min(0.9, pollution_value))
                
                print(f"Current Temperature: {current_temp}°C - Pollution Score: {pollution_value:.2f}")
            else:
                print("Warning: Could not fetch temperature data. Using fallback.")
                pollution_value = 0.5  # Fallback value
                
        except Exception as e:
            print(f"Error fetching pollution data: {e}")
            pollution_value = 0.5  # Fallback value
        
        # 3. ECONOMY DATA (Based on Bitcoin price from CoinGecko)
        try:
            # CoinGecko API for Bitcoin price
            coingecko_url = "https://api.coingecko.com/api/v3/simple/price"
            coingecko_params = {
                'ids': 'bitcoin',
                'vs_currencies': 'usd'
            }
            
            coingecko_response = requests.get(coingecko_url, params=coingecko_params, timeout=5)
            btc_data = coingecko_response.json()
            
            if 'bitcoin' in btc_data and 'usd' in btc_data['bitcoin']:
                btc_price = btc_data['bitcoin']['usd']
                
                # Normalize BTC price to economy score
                # Formula: If BTC > $90k = 1.0, else linear scale from $0-$90k
                if btc_price >= 90000:
                    economy_value = 1.0
                else:
                    economy_value = btc_price / 90000
                
                # Add slight random variation to simulate market dynamics
                import random
                economy_value += random.uniform(-0.05, 0.05)
                economy_value = max(0.1, min(1.0, economy_value))  # Clamp between 0.1-1.0
                
                print(f"Bitcoin Price: ${btc_price:,.2f} - Economy Score: {economy_value:.2f}")
            else:
                print("Warning: Could not fetch Bitcoin data. Using fallback.")
                economy_value = 0.7  # Fallback value
                
        except Exception as e:
            print(f"Error fetching economy data: {e}")
            economy_value = 0.7  # Fallback value
        
        # Return the standardized vector
        vector = [traffic_value, pollution_value, economy_value]
        print(f"Generated Vector: {vector}")
        return vector
        
    except Exception as e:
        print(f"Critical error in get_lagos_data: {e}")
        # Return fallback vector in case of total failure
        return [0.5, 0.5, 0.5]


def get_extended_lagos_data():
    """
    Advanced version that fetches more comprehensive data
    Returns dictionary with raw data and processed vector
    """
    try:
        # Get basic vector
        vector = get_lagos_data()
        
        # Fetch additional metadata
        lagos_tz = pytz.timezone('Africa/Lagos')
        current_time = datetime.now(lagos_tz)
        
        # Get day of week for traffic patterns (weekend vs weekday)
        is_weekend = current_time.weekday() >= 5  # 5=Saturday, 6=Sunday
        traffic_factor = 0.7 if is_weekend else 1.0
        
        # Adjust traffic based on weekend
        vector[0] = vector[0] * traffic_factor
        
        # Get season (rainy vs dry) for pollution adjustment
        month = current_time.month
        # Lagos rainy season: April-October
        is_rainy_season = 4 <= month <= 10
        pollution_factor = 0.8 if is_rainy_season else 1.2
        vector[1] = min(0.9, vector[1] * pollution_factor)
        
        # Create comprehensive data object
        data_package = {
            'vector': vector,
            'timestamp': current_time.isoformat(),
            'is_peak_hour': vector[0] > 0.5,
            'is_weekend': is_weekend,
            'is_rainy_season': is_rainy_season,
            'location': 'Lagos, Nigeria',
            'coordinates': {'lat': 6.5244, 'lon': 3.3792}
        }
        
        return data_package
        
    except Exception as e:
        print(f"Error in extended data: {e}")
        return {'vector': [0.5, 0.5, 0.5], 'error': str(e)}


# Test function
def test_data_fetch():
    """Test the data parser functions"""
    print("=" * 50)
    print("TESTING REAL-TIME DATA PARSER")
    print("=" * 50)
    
    # Test basic function
    print("\n1. Testing get_lagos_data():")
    vector = get_lagos_data()
    print(f"Vector: {vector}")
    
    # Test extended function
    print("\n2. Testing get_extended_lagos_data():")
    extended = get_extended_lagos_data()
    print(f"Extended Data: {json.dumps(extended, indent=2)}")
    
    # Calculate matrix health score
    health_score = sum(vector) / len(vector)
    print(f"\n3. Matrix Health Score: {health_score:.2%}")
    
    if health_score > 0.7:
        print("Status: SYSTEM OPTIMAL")
    elif health_score > 0.4:
        print("Status: SYSTEM STABLE")
    else:
        print("Status: SYSTEM STRESSED")


if __name__ == "__main__":
    # Run test when script is executed directly
    test_data_fetch()
