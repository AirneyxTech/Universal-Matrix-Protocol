import streamlit as st
import time

def render(skills_bot):
    st.sidebar.markdown("---")
    st.sidebar.info("ℹ️ **PRIVACY MODE:** Data is processed locally.")
    
    c1, c2 = st.columns([3, 1])
    with c1: st.markdown("# :: CITIZEN SKILLS ORACLE ::")
    with c2: st.markdown("🛡️ **ID SECURE**")

    st.markdown("### 🔑 Identity Verification")
    col_input, col_verify = st.columns([3, 1])
    with col_input:
        nin_input = st.text_input("Enter NIN / Digital ID:", placeholder="11-Digit NIN")
    with col_verify:
        st.write("") 
        verify_btn = st.button("🔐 VERIFY & FETCH")

    if verify_btn and nin_input:
        with st.spinner("Decrypting Biometric Hash... Connecting to Cisco/Credly..."):
            identity = skills_bot.verify_identity(nin_input)
            if identity:
                st.success(f"✅ IDENTITY CONFIRMED: {identity['name']}")
                st.info(f"🎓 **Academic Record:** {identity['academic_record']}")
                
                st.markdown("---")
                st.subheader("🏆 Verified Badges")
                certs = skills_bot.fetch_certificates(nin_input)
                cols = st.columns(3)
                for i, cert in enumerate(certs):
                    with cols[i % 3]:
                        st.markdown(f"<div style='border:1px solid #444; padding:10px; border-radius:5px; text-align:center;'><h1>{cert['badge']}</h1><b>{cert['name']}</b><br><small>{cert['issuer']}</small></div>", unsafe_allow_html=True)
                
                st.markdown("---")
                st.subheader("💼 Career Matching")
                matches = skills_bot.match_jobs(certs)
                for job in matches:
                    st.markdown(f"**{job['role']}** at *{job['company']}*")
                    st.progress(job['match']/100)
                    st.markdown(f"💰 {job['salary']} | Match: **{job['match']}%**")
                    st.markdown("---")
            else:
                st.error("❌ NIN Not Found")
