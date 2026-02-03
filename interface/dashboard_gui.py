import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import time
import pandas as pd
import numpy as np # Needed for the simulator
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent
from core.bio_agent import BioMonitor # <--- NEW AGENT

# --- CONFIGURATION ---
st.set_page_config(page_title="OMNIX PROTOCOL", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# --- CYBERPUNK CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
    div[data-testid="stMetric"] { background-color: #111; border: 1px solid #333; padding: 10px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }
    div[data-testid="stMetricValue"] { font-size: 30px; color: #ffffff; text-shadow: 0 0 5px #ffffff; }
    div[data-testid="stMetricLabel"] { color: #00ff41; font-weight: bold; }
    .css-1wivap2 { color: #ff0055 !important; text-shadow: 0 0 10px #ff0055; }
    button[data-baseweb="tab"] { background-color: #1a1a1a; color: #00ff41; border: 1px solid #00ff41; margin: 0 2px; font-size: 14px; }
    button[data-baseweb="tab"]:hover { background-color: #00ff41; color: #000; box-shadow: 0 0 15px #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD AGENTS ---
@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot = load_agents()

# --- SIDEBAR (SENTINEL MODE) ---
st.sidebar.title("🎛️ COMMAND CENTER")
scan_mode = st.sidebar.radio("MODE", ["SENTINEL (Auto)", "MANUAL SCAN"])
target_input = st.sidebar.text_input("TARGET", "Lekki-Epe")
refresh_rate = st.sidebar.slider("Refresh (s)", 5, 60, 10)

# --- HEADER ---
st.title(":: OMNIX PROTOCOL ::")
col_health, col_status = st.columns([1, 3])
with col_health:
    system_health = st.empty()
with col_status:
    st.caption(":: GLOBAL STATE VECTOR S(t) ::")
    vector_display = st.empty()

# --- TABS (NOW 5 SECTORS) ---
tab_traffic, tab_finance, tab_energy, tab_bio, tab_sim = st.tabs(["🚦 MOVEMENT", "💰 VALUE", "⚡ POWER", "🧬 LIFE", "🕹️ SIM"])

with tab_traffic:
    traffic_header = st.empty()
    col1, col2 = st.columns(2)
    with col1: traffic_load = st.empty()
    with col2: traffic_burn = st.empty()

with tab_finance:
    col1, col2 = st.columns(2)
    with col1: finance_price = st.empty()
    with col2: finance_panic = st.empty()

with tab_energy:
    energy_status = st.empty()
    energy_burn = st.empty()

with tab_bio:
    st.markdown("### BIOLOGICAL HAZARD LEVEL")
    col1, col2 = st.columns(2)
    with col1: bio_aqi = st.empty()
    with col2: bio_risk = st.empty()

with tab_sim:
    st.markdown("### 🔮 REALITY SIMULATOR")
    st.caption("Perturb the System to predict outcomes.")
    
    # Simulation Controls
    sim_traffic = st.slider("Simulate Traffic Spike", 0.0, 1.0, 0.0)
    sim_blackout = st.checkbox("Simulate Blackout")
    
    st.markdown("---")
    st.caption(":: PREDICTED FUTURE (T+12 HRS) ::")
    sim_chart = st.empty()

# --- LIVE ENGINE LOOP ---
if st.button("🚀 ACTIVATE SYSTEM"):
    status_msg = st.empty()
    
    while True:
        # 1. GATHER INTELLIGENCE
        # Defaults
        t_data, f_data, e_data, b_data = {'congestion': 0}, {'panic_score': 0}, {'status': 'GRID ACTIVE'}, {'aqi': 0}
        
        # A. Traffic
        try:
            target = target_input if scan_mode == "MANUAL SCAN" else "Lekki-Epe"
            search = target + " Lagos"
            lat, lng, addr = grok.find_coordinates(search)
            if lat:
                t_data = grok.get_traffic_data(lat, lng)
                loss = deepseek.compute_precise_loss(target, t_data['congestion'], 1200)
                traffic_header.info(f"📍 {addr}")
                traffic_load.metric("Congestion", f"{int(t_data['congestion']*100)}%", delta=f"{loss['cars_stuck']} Cars")
                traffic_burn.metric("Burn Rate", f"₦ {loss['total_burn']:,.0f}/hr", delta_color="inverse")
        except: pass

        # B. Finance & News
        try:
            market = midas.get_asset_health("BTC-USD")
            news = news_bot.scan_network()
            real_panic = news['panic_factor'] * 100
            finance_price.metric("BTC Price", f"${market['price']:,.0f}")
            finance_panic.metric("Panic", f"{real_panic:.0f}%", delta=news['headline'][:20])
            f_data = {'panic_score': real_panic}
        except: pass

        # C. Energy
        try:
            # Check Sidebar for manual override
            # For this consolidated version, we assume 'ON' unless simulator says otherwise
            e_data = {'status': 'GRID ACTIVE'} 
            energy_status.metric("Grid Status", "🟢 STABLE")
            energy_burn.metric("Diesel Burn", "₦ 0 / hr")
        except: pass

        # D. Biology (NEW)
        try:
            bio_data = bio_bot.get_vital_signs()
            b_data = bio_data # Store for Oracle
            bio_aqi.metric("Air Quality (AQI)", f"{bio_data['aqi']}", delta=f"PM2.5: {bio_data['pm2_5']}")
            bio_risk.metric("Bio-Threat", bio_data['risk_level'], delta="Lungs of Lagos", delta_color="inverse")
        except: pass

        # 2. ORACLE PROCESSING (The Brain)
        try:
            # Sync Senses
            current_vector = oracle.sync_senses(t_data, f_data, e_data, b_data)
            health = oracle.get_system_health()
            
            # Update Header
            system_health.metric("SYSTEM INTEGRITY", f"{health:.1f}%", delta="STABLE" if health > 60 else "CRITICAL")
            vector_display.code(f"S(t)=[TRAFFIC:{current_vector[0]:.2f}|PANIC:{current_vector[1]:.2f}|NRG:{current_vector[2]:.2f}|BIO:{current_vector[3]:.2f}]")

            # 3. RUN SIMULATION (Tab 5)
            # Calculate impact vector based on User Sliders
            impact = [0.0, 0.0, 0.0, 0.0]
            if sim_blackout: 
                impact[2] = -1.0 # Kill Energy
            if sim_traffic > 0:
                impact[0] = sim_traffic # Spike Traffic
            
            # Predict
            futures = oracle.simulate_future(steps=12, impact_override=impact)
            future_df = pd.DataFrame(futures, columns=["Traffic", "Panic", "Energy", "Bio"])
            sim_chart.line_chart(future_df, height=250)
            
        except Exception as e:
            st.error(f"Oracle Error: {e}")

        time.sleep(refresh_rate)