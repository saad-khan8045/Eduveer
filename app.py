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
    {"name":"DY Patil Online", "programs":["MBA","BBA","BCA"], "energy":["Creator","Influencer","Catalyst"], "fees":"₹60,000–1,60,000", "accreditation":"UGC-Entitled", "story":"DY Patil's MBA student interned with an international logistics team and now manages projects across continents."},
    {"name":"NMIMS Online", "programs":["MBA","BCom","MCA"], "energy":["Influencer","Analyst"], "fees":"₹50,000–2,25,000", "accreditation":"UGC-Entitled, NAAC A+", "story":"An Influencer at NMIMS led college events and now works in multinational corporate HR."},
    {"name":"Chandigarh University Online", "programs":["MBA","BBA","BCA"], "energy":["Creator","Catalyst","Analyst"], "fees":"₹52,000–1,50,000", "accreditation":"UGC-Entitled", "story":"A Creator at CU’s MBA launched a tech forum that turned into a full-time job."},
    # Add more as needed...
]

energy_types = {
    "Creator": "People who love innovating, starting new things, dreaming big.",
    "Influencer": "Those with a knack for leading, networking, and inspiring others.",
    "Catalyst": "Helpers who shine when organizing and delivering practical value.",
    "Analyst": "Detail-oriented minds who thrive in logic, tech, and analysis."
}

# --- HEADER ---
st.set_page_config(page_title="Distoversity - Eduveer AI", page_icon="🎓", layout="centered")
st.title("🎓 Distoversity: Eduveer – Your Mentor & Friend")
st.markdown("""Hey 👋 I'm Eduveer.  
No boring forms here... just honest, friendly advice.  
Want to chat about your dreams, university plans, or online degrees?  
I'm here to help you find the *best fit* for your strengths – and budget.  
""")

# --- WARM WELCOME, GENTLE PROFILE SETUP ---
if "energy" not in st.session_state:
    st.markdown("#### Let's start simple!  
    I know every learner is different.  
    If you like, pick which description feels closest (but you can skip and just chat too!)")
    energy_choice = st.selectbox("Which sounds most like you?", list(energy_types.keys()), index=0)
    st.session_state.energy = energy_choice
    st.markdown(f"That’s awesome! {energy_types[energy_choice]}")
    status_choice = st.selectbox("Are you currently a:", ["Student", "Working Learner"], index=0)
    st.session_state.status = status_choice
    st.markdown("---")

if "chat_log" not in st.session_state:
    st.session_state.chat_log = [
        {"role":"assistant", "content":
         f"Hi! I'm Eduveer, your mentor and friend.  
         I’ve seen Creators, Influencers, Catalysts, and Analysts make amazing journeys.  
         Whatever your style, I’ll help you map universities and degrees that really fit.  
         Just type any question below, or tell me about your goals – let’s chat!"}
    ]

for msg in st.session_state.chat_log:
    avatar = "🧑‍🎓" if msg["role"]=="user" else "🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if prompt := st.chat_input("Type anything: dreams, doubts, goals, or ask about degrees..."):
    st.session_state.chat_log.append({"role": "user", "content": prompt})
    user_energy = st.session_state.energy
    reply = ""
    # Friend/Mentor tone: gentle suggestion & story
    matches = [uni for uni in universities if user_energy in uni["energy"]]
    if matches:
        reply = f"Hey friend, since you have a bit of **{user_energy}** vibe, I’ve helped people like you succeed:\n\n"
        for uni in matches:
            reply += f"- At **{uni['name']}**, students with your style study {', '.join(uni['programs'])}. {uni['story']}\n"
        reply += "\nThe trick is matching your goals to the right program.  
                 Want to see a step-by-step map for your journey? I’d love to help you book a free career session below!"
    else:
        reply = "Let's explore together – just tell me what excites you, and I’ll share some options!"

    st.session_state.chat_log.append({"role":"assistant","content":reply})

if len([m for m in st.session_state.chat_log if m["role"]=="user"]) >= 2:
    st.info("Curious about next steps, personalized matches, or a career map? [Book a free expert session!](https://forms.gle/YourFormLinkHere)")

st.caption("© 2025 Distoversity Pvt Ltd | Friendly Mentor, Real Career Results")
