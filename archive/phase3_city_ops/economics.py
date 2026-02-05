import random

class EconomicMatrix:
    def __init__(self):
        self.base_burn_rate = 0.03 # Liters per minute idling
        
    def compute_precise_loss(self, target_location, congestion_level, fuel_price):
        """
        Calculates money lost based on REAL fuel prices.
        """
        # 1. Estimate Cars Stuck (Based on Congestion %)
        # If congestion is 0.5 (50%), we assume 800 cars. Max 2000.
        cars_stuck = int(congestion_level * 2500)
        if cars_stuck < 100: cars_stuck = 150 # Minimum traffic
        
        # 2. Calculate Fuel Burned
        # Cars * Liters/Min * 60 mins
        total_liters_per_hour = cars_stuck * self.base_burn_rate * 60
        
        # 3. Calculate Naira Lost
        money_lost = total_liters_per_hour * fuel_price
        
        return {
            "cars_stuck": cars_stuck,
            "liters_burned": int(total_liters_per_hour),
            "total_burn": int(money_lost)
        }