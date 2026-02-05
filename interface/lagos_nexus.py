import streamlit as st
import pandas as pd
import sys
import os

# Connect to Brain
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.nexus_engine import NexusEngine

engine = NexusEngine()

st.set_page_config(page_title="OMNIX: Lagos Nexus", layout="wide", page_icon="🧿")

# STYLING
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #fff; }
    .stMetric { background-color: #1a1a1a; border: 1px solid #333; padding: 10px; border-radius: 5px; }
    div.stButton > button:first-child { background-color: #00ff41; color: black; font-weight: bold; border: none; }
    </style>
""", unsafe_allow_html=True)

# SIDEBAR NAVIGATION
st.sidebar.title("🧿 OMNIX")
mode = st.sidebar.radio("SELECT MODE:", ["👤 STUDENT ACCESS", "🔐 ADMIN / HOC"])

# --- MODE 1: STUDENT (SELF-SERVICE) ---
if mode == "👤 STUDENT ACCESS":
    st.title("🚀 CAREER DIAGNOSTIC TOOL")
    st.caption("Analyze your skills against the Live Lagos Tech Market.")

    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name:")
        level = st.selectbox("Current Level:", ["Graduate", "400L", "300L", "200L", "100L"])
    
    with col2:
        # Simple Multi-Select for Skills
        st.write("Select Your Technical Skills:")
        skills = st.multiselect("Skills", 
            ["Python", "Excel", "SQL", "JavaScript", "React", "Node.js", 
             "Graphic Design", "UI/UX", "Cyber Security", "Networking", 
             "Flutter", "Digital Marketing", "Git", "PowerBI"],
            label_visibility="collapsed"
        )

    if st.button("🔍 ANALYZE MY CAREER PATH"):
        if not name or not skills:
            st.error("Please enter your name and select at least one skill.")
        else:
            with st.spinner("Scanning Live Jobs..."):
                # Create a temporary dataframe for just this one student
                student_df = pd.DataFrame([{
                    "Name": name, 
                    "Level": level, 
                    "Skills": ", ".join(skills)
                }])
                
                # Use the engine to analyze
                results = engine.analyze_student_data(student_df)
                
                # Display Result Card
                res = results.iloc[0] # Get the first (and only) row
                
                st.markdown("---")
                c1, c2 = st.columns([1, 2])
                
                with c1:
                    # SCORE CARD
                    score_val = int(res['Score'].replace('%', ''))
                    color = "green" if score_val >= 60 else "red"
                    st.markdown(f"<h1 style='color:{color}; font-size: 60px; text-align: center;'>{res['Score']}</h1>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center;'>MARKET FIT</p>", unsafe_allow_html=True)
                
                with c2:
                    st.subheader(f"🎯 BEST MATCH: {res['Best Match']}")
                    
                    if res['Status'] == 'HIRE':
                        st.success("✅ YOU ARE EMPLOYABLE! The market wants you now.")
                        st.info(f"👉 **RECOMMENDATION:** {res['Action']}")
                    else:
                        st.warning("⚠️ SKILL GAP DETECTED")
                        st.write(f"To get this job, you are missing specific skills.")
                        st.error(f"🛠️ **FIX:** {res['Action']}")

# --- MODE 2: ADMIN (BULK UPLOAD) ---
else:
    st.title("🔐 ADMIN OPS CENTER")
    st.caption("Batch Analysis for Departmental Planning")
    st.info("Upload the CSV from Google Forms here.")

    uploaded_file = st.file_uploader("", type=["csv"])

    if uploaded_file:
        with st.spinner("Connecting to Live Labor Market... Analyzing Batch..."):
            try:
                df = pd.read_csv(uploaded_file)
                results = engine.analyze_student_data(df)

                if isinstance(results, dict) and "error" in results:
                    st.error(results['error'])
                else:
                    # METRICS
                    hired = len(results[results['Status'] == 'HIRE'])
                    train = len(results[results['Status'] == 'TRAIN'])
                    
                    m1, m2, m3 = st.columns(3)
                    m1.metric("TOTAL STUDENTS", len(results))
                    m2.metric("JOB READY", hired, delta="Employable")
                    m3.metric("SKILL GAPS", train, delta="Need Training", delta_color="inverse")

                    # REPORT TABLE
                    st.markdown("### 📊 OPTIMIZATION REPORT")
                    def highlight_status(val):
                        color = '#00ff41' if val == 'HIRE' else '#ff4b4b'
                        return f'color: {color}; font-weight: bold'

                    st.dataframe(results.style.map(highlight_status, subset=['Status']), use_container_width=True)
                    
                    # DOWNLOAD
                    st.download_button(
                        "📥 DOWNLOAD REPORT FOR VC",
                        results.to_csv(index=False),
                        "lasustech_optimization_report.csv",
                        "text/csv"
                    )
            except Exception as e:
                st.error(f"Processing Error: {e}")
