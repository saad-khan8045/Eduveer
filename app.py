import streamlit as st

# --- COLOR THEME ---
st.markdown("""
<style>
body, .stApp { background: #F3F8FC; }
h1, h2, h3 { color: #00AEEF; text-align: center; font-weight: 800; }
.stButton button, .cta-btn {
    background: #00AEEF; color: #FFF !important; border-radius: 8px;
    font-weight: 700; box-shadow: 0 4px 16px #00AEEF33;
    font-size: 18px; transition: background 0.3s, box-shadow 0.3s, transform 0.2s;
}
.stButton button:hover, .cta-btn:hover {
    background: #0095CC; box-shadow: 0 8px 20px #00AEEF55; transform: scale(1.04);
}
.card, .stChatMessage.assistant { background: #FFFFFF; border-radius: 16px;
    box-shadow: 0 2px 16px #CAF0F822; border: 1px solid #E0F2FE; margin-bottom: 18px;
}
.stChatMessage.user { background: #E0F2FE; border-radius: 16px; border: 1px solid #BAE6FD; }
</style>
""", unsafe_allow_html=True)

# --- DATA / EXAMPLES ---
universities = [
    {"name":"AMITY Online", "programs":["MBA","BCA","BBA","MCA"], "energy":["Creator","Influencer","Analyst"], "fees":"₹65,000–2,50,000", "accreditation":"UGC-Entitled, NAAC A+", "story":"A Creator who joined Amity's MBA built his startup during his studies and got VC funding by graduation."},
    {"name":"Manipal Online", "programs":["MBA","BCA","BSc Data Science"], "energy":["Creator","Influencer","Analyst"], "fees":"₹80,000–2,75,000", "accreditation":"UGC-Entitled, NAAC A+", "story":"An Analyst at Manipal's Data Science program started with basic skills and landed a remote job at a top tech firm."},
    {"name":"LPU Online", "programs":["MBA","BCA","BCom"], "energy":["Creator","Influencer","Analyst","Catalyst"], "fees":"₹70,000–2,10,000", "accreditation":"UGC-Entitled", "story":"A Catalyst in LPU BCom organized community finance programs and was recruited as a financial coordinator."},
    {"name":"DY Patil Online", "programs":["MBA","BBA","BCA"], "energy":["Creator","Influencer","Catalyst"], "fees":"₹60,000–1,60,000", "accreditation":"UGC-Entitled", "story":"DY Patil's MBA student interned with an international logistics team and now manages projects across
