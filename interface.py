import os
import time

# ---------- ANSI COLORS ----------
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear_screen():
    os.system("clear")

def show_logo():
    clear_screen()
    logo = f"""
{CYAN}{BOLD}
██╗      █████╗  ██████╗  ██████╗ ███████╗
██║     ██╔══██╗██╔════╝ ██╔═══██╗██╔════╝
██║     ███████║██║  ███╗██║   ██║███████╗
██║     ██╔══██║██║   ██║██║   ██║╚════██║
███████╗██║  ██║╚██████╔╝╚██████╔╝███████║
╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝
{RESET}
    """
    print(logo)
    print(f"{GREEN}System Ready • Universal Matrix CLI{RESET}")
    print(f"{CYAN}Phase 1 Status: LIVE SIGNAL ACQUISITION{RESET}\n")

def get_user_choice():
    """Displays menu and captures user input for Grok."""
    show_logo()
    print(f"{BOLD}{YELLOW}Select an action:{RESET}")
    print("[1] 📡 Connect to Live Lagos Satellites")
    print("[2] Run 5-Day Simulation")
    print("[3] Propose a Solution (Optimize)")
    print("[4] Exit")
    
    choice = input(f"\n{BOLD}>>> {RESET}").strip()
    
    # Map numbers to Grok's expected strings
    if choice == '1': return 'Option 1' # Not used in main yet, but good to have
    if choice == '2': return 'Option 2'
    if choice == '3': return 'Option 3'
    if choice == '4': return 'exit'
    return choice

def show_loading():
    """Visual feedback for satellite connection."""
    print(f"\n{CYAN}Establishing uplink to Lagos satellites...{RESET}")
    bar_length = 20
    for i in range(bar_length + 1):
        percent = int((i / bar_length) * 100)
        bar = "█" * i + "-" * (bar_length - i)
        print(f"\r[{bar}] {percent}%", end="", flush=True)
        time.sleep(0.1) # Fast simulation
    print(f"\n{GREEN}Connection established.{RESET}\n")

def display_result(result):
    """Outputs the final data to the user."""
    # Since oracle_core handles the printing, we just pause here
    print(f"\n{YELLOW}[ SYSTEM ] Cycle Complete.{RESET}")
    input("Press Enter to continue...")
