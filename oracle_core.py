import numpy as np
import time

# ANSI COLORS
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

class OracleCore:
    def __init__(self):
        # The Rules of Lagos (Transition Matrix)
        self.transition_matrix = np.array([
            [0.9, 0.0, 0.1],   # Traffic Persistence
            [0.3, 0.8, 0.0],   # Pollution Persistence
            [-0.1, -0.05, 1.05] # Economic Resilience
        ])

    def simulate(self, start_vector):
        """ Runs prediction based on LIVE input vector. """
        state = np.array(start_vector)
        
        # REAL-TIME ALERT SYSTEM
        if state[2] < 0.3:
            print(f"\n{RED}{BOLD}[ WARNING ] 📉 REAL-TIME MARKET CRASH SIGNAL DETECTED.{RESET}")
            time.sleep(1)
        elif state[2] > 0.8:
            print(f"\n{GREEN}{BOLD}[ INFO ] 📈 MARKET MOMENTUM IS STRONG.{RESET}")

        print(f"\n{YELLOW}--- 5-DAY FORECAST START ---{RESET}")
        print(f" Day 0 (NOW): Traffic={state[0]:.2f} | Poll={state[1]:.2f} | Econ={state[2]:.2f}")
        
        for day in range(1, 6):
            # The Matrix Calculation
            state = np.dot(self.transition_matrix, state)
            state = np.clip(state, 0.0, 1.0) # Keep realistic
            
            # Visual formatting
            econ_fmt = RED if state[2] < 0.3 else GREEN
            print(f" Day {day}:       Traffic={state[0]:.2f} | Poll={state[1]:.2f} | {econ_fmt}Econ={state[2]:.2f}{RESET}")
            time.sleep(0.5)
            
        print(f"{YELLOW}--- FORECAST END ---{RESET}")
    def optimize(self, current_vector):
        """ Tests a solution to fix the predicted decline. """
        print(f"\n{CYAN}[ OPTIMIZER ] Testing: 'Intelligent Traffic Lights'...{RESET}")
        time.sleep(1)
        
        # Proposed Fix: Reduce Traffic by 0.2, but costs 0.05 Economy
        intervention = np.array([-0.2, 0.0, -0.05])
        new_state = current_vector + intervention
        
        # Predict Result
        future_state = np.dot(self.transition_matrix, new_state)
        
        print(f" [ RESULT ] Traffic drops to {future_state[0]:.2f}")
        print(f" [ RESULT ] Economy adjusts to {future_state[2]:.2f}")
        
        if future_state[2] > 0.8:
            print(f"{GREEN}[ DECISION ] APPROVED. Net benefit positive.{RESET}")
        else:
            print(f"{RED}[ DECISION ] REJECTED. Economy damaged.{RESET}")

