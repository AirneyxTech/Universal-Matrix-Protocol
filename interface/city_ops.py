import streamlit as st
import pandas as pd
import time

def render(grok, deepseek, midas, nepa, oracle, news_bot, bio_bot):
    st.sidebar.markdown("---")
    st.sidebar.markdown("📡 **SURVEILLANCE CONTROLS**")
    scan_mode = st.sidebar.radio("SCAN MODE", ["SENTINEL (Auto)", "MANUAL"])
    target_input = st.sidebar.selectbox("TARGET ZONE", [
        "Lekki-Epe Expressway", "Third Mainland Bridge", "Ikorodu Road", 
        "Apapa-Oshodi", "Lagos-Ibadan"
    ])
    
    st.sidebar.markdown("🚨 **ALERT THRESHOLDS**")
    alert_speed = st.sidebar.slider("Min Speed (km/h)", 0, 40, 10)
    fuel_price = st.sidebar.number_input("Fuel Price (₦/L)", value=1250)

    c1, c2 = st.columns([3, 1])
    with c1: st.markdown("# :: CITY OPERATIONS CENTER ::")
    with c2: st.markdown("🟢 **SYSTEM ONLINE**")

    tab_traffic, tab_finance, tab_energy, tab_sim = st.tabs(["🚦 TRAFFIC", "💰 FINANCE", "⚡ POWER", "🕹️ SIM"])

    with tab_traffic:
        st.subheader(f"📍 SECTOR: {target_input}")
        try:
            found_lat, found_lng, addr = grok.find_coordinates(target_input + " Lagos")
            if found_lat:
                t_data = grok.get_traffic_data(found_lat, found_lng)
                cong = t_data.get('congestion', 0)
                est_speed = max(5, 80 * (1 - cong))
                est_delay = int(cong * 60)
                loss = deepseek.compute_precise_loss(target_input, cong, fuel_price)

                c1, c2, c3, c4 = st.columns(4)
                c1.metric("AVG SPEED", f"{int(est_speed)} km/h", "-Slow" if est_speed < 20 else "Fast")
                c2.metric("DELAY", f"+{est_delay} min", "High" if est_delay > 20 else "Normal")
                c3.metric("CONGESTION", f"{int(cong*100)}%", f"{loss['cars_stuck']} Cars")
                c4.metric("MONEY BURN", f"₦ {loss['total_burn']:,.0f}/hr", "Waste")
                
                if est_speed < alert_speed:
                    st.error(f"🚨 CRITICAL TRAFFIC STOPPAGE DETECTED ON {target_input}")

                st.map(pd.DataFrame({'lat': [found_lat], 'lon': [found_lng]}), zoom=12)
        except: st.error("Satellite Link Unstable")

    with tab_finance:
        c1, c2 = st.columns(2)
        news_data = news_bot.scan_network()
        with c1: st.metric("BTC PRICE", "$98,420")
        with c2: st.metric("SOCIAL PANIC", f"{news_data['panic_factor']*100:.0f}%")
        st.markdown("### 📰 INTELLIGENCE FEED")
        for story in news_data['stories']:
            st.markdown(f"👉 **[{story['source']}]** [{story['title']}]({story['link']})")

    with tab_energy:
        st.metric("GRID STATUS", "🟢 STABLE", "100MW Delivered")
        
    with tab_sim:
        st.info("🔮 Reality Simulator Active")
