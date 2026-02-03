import sys
import os
# 🛠️ PATH PATCH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import pandas as pd
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid

# --- CONFIGURATION ---
st.set_page_config(
    page_title="OMNIX PROTOCOL", 
    page_icon="👁️", 
    layout="wide",
    initial_sidebar_state="collapsed" # Collapsed makes it cleaner on mobile
)

# CYBERPUNK CSS (Mobile Optimized)
st.markdown("""
    <style>
    .stApp {background-color: #0e1117;}
    div[data-testid="stMetricValue"] {color: #ff4444; font-family: 'Courier New', monospace;}
    
    /* Bigger Tabs for Fingers */
    button[data-baseweb="tab"] {
        font-size: 20px;
        margin: 0 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALIZE AGENTS ---
@st.cache_resource
def load_agents():
    # The SatelliteUplink now automatically checks st.secrets!
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid()

grok, deepseek, midas, nepa = load_agents()

# --- SIDEBAR CONTROL ---
st.sidebar.title("🎛️ COMMAND CENTER")
scan_mode = st.sidebar.radio("MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
target_input = st.sidebar.text_input("TARGET", "Ikorodu")
st.sidebar.markdown("---")
manual_blackout = st.sidebar.checkbox("🚨 REPORT BLACKOUT", value=False)
st.sidebar.markdown("---")
fuel_price = st.sidebar.number_input("Fuel Price (₦/L)", value=1250)
refresh_rate = st.sidebar.slider("Refresh (s)", 5, 60, 10)

# --- MAIN DASHBOARD (MOBILE TABS) ---
st.title(":: OMNIX PROTOCOL ::")

# 📱 THIS IS THE MOBILE MAGIC: TABS
tab_traffic, tab_finance, tab_energy, tab_map = st.tabs(["🚦 TRAFFIC", "💰 FINANCE", "⚡ POWER", "🗺️ MAP"])

with tab_traffic:
    st.markdown("### TRAFFIC SECTOR")
    # We create empty slots here to update later
    traffic_header = st.empty()
    traffic_load = st.empty()
    traffic_burn = st.empty()

with tab_finance:
    st.markdown("### FINANCIAL SECTOR")
    finance_price = st.empty()
    finance_panic = st.empty()

with tab_energy:
    st.markdown("### POWER GRID")
    energy_status = st.empty()
    energy_burn = st.empty()

with tab_map:
    st.markdown("### LIVE SATELLITE")
    map_display = st.empty()

# --- LIVE ENGINE ---
if st.button("🚀 ACTIVATE SYSTEM"):
    status_msg = st.empty()
    status_msg.markdown("`SYSTEM INITIALIZED. SCANNING...`")
    
    while True:
        # 1. TRAFFIC LOGIC
        target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe Expressway"
        search_term = target if "lagos" in target.lower() else target + " Lagos"
        
        try:
            lat, lng, addr = grok.find_coordinates(search_term)
            if lat:
                # Get Traffic Data
                data = grok.get_traffic_data(lat, lng)
                metrics = deepseek.compute_precise_loss(target, data['congestion'], fuel_price)
                
                # Update GUI (Inside the Tabs)
                traffic_header.info(f"📍 {addr}")
                traffic_load.metric("Congestion", f"{int(data['congestion']*100)}%", delta=f"{metrics['cars_stuck']:,} Cars")
                traffic_burn.metric("Traffc Burn", f"₦ {metrics['total_burn']:,.0f}/hr", delta_color="inverse")
                
                # Update Map
                map_data = pd.DataFrame({'lat': [lat], 'lon': [lng]})
                map_display.map(map_data, zoom=12)
        except Exception as e:
            traffic_header.error(f"Signal Lost: {e}")

        # 2. FINANCE LOGIC
        try:
            market = midas.get_asset_health("BTC-USD")
            finance_price.metric("BTC Price", f"${market['price']:,.0f}")
            finance_panic.metric("Panic Score", f"{market['panic_score']:.1f}%", delta="CRASH WARNING" if market['panic_score']>80 else "STABLE")
        except: 
            finance_price.warning("Market Offline")

        # 3. ENERGY LOGIC
        try:
            status = "OFF" if manual_blackout else "ON"
            power_data = nepa.calculate_burn_rate(status)
            
            if status == "OFF":
                energy_status.metric("Grid Status", "🔴 SYSTEM COLLAPSE", delta="BLACKOUT DETECTED", delta_color="inverse")
                energy_burn.metric("Diesel Burn Rate", f"₦ {power_data['burn_rate']:,.0f}/hr", delta=f"{power_data['generators_on']:,} Gens", delta_color="inverse")
            else:
                energy_status.metric("Grid Status", "🟢 GRID STABLE", delta="POWER RESTORED")
                energy_burn.metric("Diesel Burn Rate", "₦ 0 / hr", delta="Generators Offline")
        except: 
            pass

        time.sleep(refresh_rate)