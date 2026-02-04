import sys
import os
import streamlit as st
import requests
from streamlit_lottie import st_lottie

sys.path.append(os.path.dirname(__file__))
import city_ops
import citizen_portal

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from infrastructure.tomtom_client import SatelliteUplink
from core.economics import EconomicMatrix
from core.midas import FinancialOracle
from core.energy import EnergyGrid
from core.oracle import OracleCore
from core.news_agent import NewsAgent
from core.bio_agent import BioMonitor
from core.skills_agent import SkillsAgent

st.set_page_config(page_title="OMNIX v5.1 (Linked)", page_icon="🧿", layout="wide", initial_sidebar_state="expanded")

@st.cache_resource
def load_agents():
    return SatelliteUplink(), EconomicMatrix(), FinancialOracle(), EnergyGrid(), OracleCore(), NewsAgent(), BioMonitor(), SkillsAgent()

grok, deepseek, midas, nepa, oracle, news_bot, bio_bot, skills_bot = load_agents()

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #00ff41; font-family: 'Courier New'; }
    div[data-testid="stMetric"] { background-color: #1a1a1a; border: 1px solid #00ff41; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.title("🧿 OMNIX PROTOCOL")
    st.markdown("---")
    app_mode = st.radio("SELECT SYSTEM:", ["🏙️ CITY OPERATIONS", "👤 CITIZEN PORTAL"])
    
    def load_lottieurl(url):
        try: return requests.get(url).json()
        except: return None
    lottie = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
    if lottie: st_lottie(lottie, height=100)

if app_mode == "🏙️ CITY OPERATIONS":
    city_ops.render(grok, deepseek, midas, nepa, oracle, news_bot, bio_bot)
else:
    citizen_portal.render(skills_bot)
