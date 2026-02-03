import numpy as np
import pandas as pd

class OracleCore:
    def __init__(self):
        # THE GLOBAL STATE VECTOR S(t) (4 Dimensions)
        # [0] Traffic (0-1)
        # [1] Panic (0-1)
        # [2] Energy (1=Stable, 0=Blackout)
        # [3] Biology (0=Clean, 1=Toxic)
        self.state_vector = np.array([0.2, 0.1, 1.0, 0.3]) 
        
        # THE TRANSITION MATRIX (T)
        # How sectors affect each other
        self.transition_matrix = np.array([
            [0.8,  0.0, -0.1,  0.0],  # Traffic Logic
            [0.2,  0.9, -0.3,  0.4],  # Panic rises if Energy drops (-0.3) or Bio is Toxic (0.4)
            [-0.1, -0.1, 0.9,  0.0],  # Energy Logic
            [0.4,  0.0, -0.5,  0.8]   # Bio (Pollution) rises with Traffic (0.4) & Blackouts (-0.5 Energy)
        ])

    def sync_senses(self, t_data, f_data, e_data, b_data):
        # Normalize Inputs
        t_score = t_data.get('congestion', 0)
        f_score = f_data.get('panic_score', 0) / 100.0
        e_score = 1.0 if e_data.get('status') == "GRID ACTIVE" else 0.0
        b_score = min(1.0, b_data.get('aqi', 0) / 100.0) # Normalize AQI
        
        self.state_vector = np.array([t_score, f_score, e_score, b_score])
        return self.state_vector

    def simulate_future(self, steps=12, impact_override=None):
        """
        Predicts future. 'impact_override' allows users to simulate 'What If' scenarios.
        """
        future_states = []
        current_s = self.state_vector.copy()
        
        # Apply User Override (e.g., "Simulate a Blackout")
        if impact_override:
            current_s = current_s + np.array(impact_override)
            current_s = np.clip(current_s, 0.0, 1.0)

        for _ in range(steps):
            next_s = np.dot(self.transition_matrix, current_s)
            next_s = np.clip(next_s, 0.0, 1.0)
            future_states.append(next_s)
            current_s = next_s
            
        return future_states

    def get_system_health(self):
        t, f, e, b = self.state_vector
        # Health = Low Traffic + Low Panic + High Energy + Low Pollution
        health = ((1.0 - t) + (1.0 - f) + e + (1.0 - b)) / 4.0
        return health * 100