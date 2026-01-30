import sys
import time
from oracle_core import OracleCore
from data_parser import get_lagos_data
from interface import get_user_choice, show_loading, display_result
from safety_guard import validate_state

def main():
    oracle = OracleCore()
    
    while True:
        choice = get_user_choice()

        if choice == 'exit':
            sys.exit(0)

        # OPTION 1: Just View Data (No Sim)
        elif choice == 'Option 1':
            show_loading()
            print("\n[ NETLINK ] Fetching Live Status...")
            get_lagos_data() # This prints the data
            input("\nPress Enter to continue...")

        # OPTION 2: Run Simulation
        elif choice == 'Option 2':
            show_loading()
            print("\n[ NETLINK ] Activating Sensors...")
            live_vector = get_lagos_data()
            if validate_state({"Traffic": live_vector[0], "Pollution": live_vector[1]}):
                oracle.simulate(start_vector=live_vector)
                display_result(None)

        # OPTION 3: Propose Solution
        elif choice == 'Option 3':
            print("\n[ INPUT ] Fetching current state for optimization...")
            live_vector = get_lagos_data()
            oracle.optimize(current_vector=live_vector)
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()

