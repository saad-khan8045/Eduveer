import streamlit as st

# --- THEME & UI COLORS ---
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

# --- DATA: Expand as Needed ---
universities = [
    {"name":"AMITY Online", "programs":["MBA","BCA","BBA","MCA"], "energy":["Creator","Influencer","Analyst"], "fees":"₹65,000–2,50,000", "accreditation":"UGC-Entitled, NAAC A+", "example":"Amity’s MBA in Entrepreneurship helps Creators launch real-world projects."},
    {"name":"Manipal Online", "programs":["MBA","BCA","BSc Data Science"], "energy":["Creator","Influencer","Analyst"], "fees":"₹80,000–2,75,000", "accreditation":"UGC-Entitled, NAAC A+", "example":"Manipal’s BSc Data Science gives Analysts hands-on experience, leading to analytics jobs."},
    {"name":"LPU Online", "programs":["MBA","BCA","BCom"], "energy":["Creator","Influencer","Analyst","Catalyst"], "fees":"₹70,000–2,10,000", "accreditation":"UGC-Entitled", "example":"LPU’s BCA program is excellent for Analysts and Creators interested in tech innovation."},
    {"name":"DY Patil Online", "programs":["MBA","BBA","BCA"], "energy":["Creator","Influencer","Catalyst"], "fees":"₹60,000–1,60,000", "accreditation":"UGC-Entitled", "example":"DY Patil’s MBA includes industry internships for Catalysts who value practical service."},
    {"name":"NMIMS Online", "programs":["MBA","BCom","MCA"], "energy":["Influencer","Analyst"], "fees":"₹50,000–2,25,000", "accreditation":"UGC-Entitled, NAAC A+", "example":"NMIMS’s MBA in HR/Marketing helps Influencers build careers in leadership."},
    {"name":"Chandigarh University Online", "programs":["MBA","BBA","BCA"], "energy":["Creator","Catalyst","Analyst"], "fees":"₹52,000–1,50,000", "accreditation":"UGC-Entitled", "example":"CU’s MBA is hands-on, ideal for Catalysts looking to manage real projects."},
    # Add more universities for full coverage
]

energy_types = {
    "Creator": "You love innovation, building new things, dreaming up ideas.",
    "Influencer": "You thrive on leading teams, networking, and communication.",
    "Catalyst": "You excel at service, reliability, and operational success.",
    "Analyst": "You enjoy working with data, logic, solving technical challenges."
}

# --- HEADER ---
st.set_page_config(page_title="Distoversity - Eduveer AI Counselor", page_icon="🎓", layout="centered")
st.title("🎓 Distoversity: Eduveer AI Career Counselor")
st.markdown("**Education that fits your genius, goals, and budget.**\n\nDiscover your natural energy—I'll connect you to the RIGHT online universities in India.")

# --- FRIENDLY, SOFT ONBOARDING ---
if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:
    st.markdown("### Before we begin, what describes you best?")
    energy = st.radio("What's your Distoversity Natural Energy?",
        ["Creator", "Influencer", "Catalyst", "Analyst"])
    st.session_state.energy = energy
    st.markdown(f"Awesome! {energy_types[energy]}")
    status = st.radio("Are you a:", ["Student", "Working Learner"])
    st.session_state.status = status
    st.markdown(f"Welcome, {status.lower()}!")
    st.markdown("---")
    st.markdown("You can now ask me about online degrees, universities, or your personalized career path. Just type below!")
    st.session_state.started = True
else:
    st.markdown(f"**You are a {st.session_state.energy} ({energy_types[st.session_state.energy]})**")
    st.markdown(f"*Status: {st.session_state.status}*")

    if "chat_log" not in st.session_state:
        st.session_state.chat_log = [
            {"role":"assistant", "content":
             f"Hi there! Based on your profile, I’m ready to suggest universities, online programs, and career paths tailored for a {st.session_state.energy}. Ask me anything!"}
        ]

    for msg in st.session_state.chat_log:
        avatar = "🧑‍🎓" if msg["role"]=="user" else "🎓"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Type your question or interest (e.g., MBA, BCA, data science jobs...)"):
        st.session_state.chat_log.append({"role": "user", "content": prompt})
        user_energy = st.session_state.energy
        reply = ""
        # Recommend universities/programs by energy
        matches = [uni for uni in universities if user_energy in uni["energy"]]
        if matches:
            reply = f"As a {user_energy}, here are some recommended online universities and programs:\n"
            reply += "\n".join([
                f"- **{uni['name']}**: {', '.join(uni['programs'])} | Fees: {uni['fees']} ({uni['accreditation']})\n  *Example:* {uni['example']}"
                for uni in matches
            ])
            reply += "\n\nMatching your energy and ambitions to the right degree and university leads to a successful, satisfying career."
            reply += "\nWant customized guidance for your goals? Book a free 1:1 career session below."
        else:
            reply = "I couldn't find a direct match, but let's explore more options together!"
        st.session_state.chat_log.append({"role":"assistant","content":reply})

    if len([m for m in st.session_state.chat_log if m["role"]=="user"]) >= 2:
        st.info("🔎 Want a step-by-step personalized university and career map? [Book your free expert session!](https://forms.gle/YourFormLinkHere)")

st.caption("© 2025 Distoversity Pvt Ltd | AI Career Counseling")
