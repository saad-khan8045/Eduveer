import streamlit as st
import time
import random
import re

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Distoversity | Eduveer",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Brand Colors
PRIMARY_BLUE = "#00AEEF"
LIGHT_BLUE_BG = "#E0F2FE"
WHITE = "#FFFFFF"

# Custom CSS for Distoversity Branding
st.markdown(f"""
    <style>
    .stApp {{
        background-color: #FAFAFA;
    }}
    .stChatMessage {{
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 10px;
    }}
    .stChatMessage.user {{
        background-color: {LIGHT_BLUE_BG};
        border: 1px solid {PRIMARY_BLUE};
    }}
    div[data-testid="stChatMessageContent"] {{
        color: #333;
        font-family: 'Sans-Serif';
    }}
    .main-header {{
        color: {PRIMARY_BLUE};
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0;
    }}
    .sub-header {{
        color: #555;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }}
    .stButton>button {{
        background-color: white;
        color: {PRIMARY_BLUE};
        border-radius: 12px;
        border: 2px solid {PRIMARY_BLUE};
        padding: 10px 20px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: {PRIMARY_BLUE};
        color: white;
        transform: scale(1.02);
    }}
    /* Primary Action Button Style (for Form) */
    .css-1he4a3e {{ 
        background-color: {PRIMARY_BLUE} !important; 
        color: white !important; 
    }}
    .university-card {{
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid {PRIMARY_BLUE};
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA: KNOWLEDGE BASE (Offline Intelligence) ---
KNOWLEDGE_BASE = {
    "ugc": "UGC stands for University Grants Commission. For any university in India (Online or Offline), UGC recognition is mandatory. It ensures the degree is valid for government jobs.",
    "deb": "DEB (Distance Education Bureau) is a specific wing of UGC. For an **Online Degree** to be valid, the university MUST have UGC-DEB approval specifically for that year.",
    "naac": "NAAC grades universities on quality (A++, A+, A, B). An 'A+' or 'A++' grade usually means top-tier faculty, infrastructure, and global recognition.",
    "aicte": "AICTE approval is technical validation. For MBA and MCA courses, AICTE approval is a gold standard, though UGC-DEB is the primary legal requirement for online degrees.",
    "fake": "A degree is valid ONLY if the university is listed on the official UGC-DEB website. Never pay fees into a personal bank account; always pay to the university directly.",
    "placement": "Online degrees now have strong acceptance. Top universities like Amity, Manipal, and NMIMS offer dedicated placement cells similar to their on-campus programs.",
    "exam": "Exams for online degrees are usually conducted online with proctoring (AI monitoring). You can take them from home on your laptop.",
    "job": "Yes, UGC-DEB entitled online degrees are treated as equivalent to regular degrees for government jobs and higher education (like PhD) in India."
}

# --- DATA: UNIVERSITIES ---
UNIVERSITIES = [
    {
        "name": "Amity University Online",
        "programs": ["MBA", "BBA", "MCA", "BCA"],
        "fees": "₹1.5L - ₹3.5L",
        "accreditation": "UGC-DEB, NAAC A+",
        "success_story": "Rohan (Analyst) shifted from Sales to Data Analytics with a 40% hike.",
        "best_for": ["Analyst", "Influencer"]
    },
    {
        "name": "Manipal University Jaipur (Online)",
        "programs": ["MBA", "B.Com", "M.Com", "BCA"],
        "fees": "₹1.2L - ₹3.0L",
        "accreditation": "NAAC A+, AICTE",
        "success_story": "Priya (Creator) launched her digital agency post their Digital Marketing elective.",
        "best_for": ["Creator", "Influencer"]
    },
    {
        "name": "LPU Online",
        "programs": ["M.Sc CS", "MBA", "BA", "MA"],
        "fees": "₹80k - ₹1.8L",
        "accreditation": "UGC Entitled, WES",
        "success_story": "Amit (Catalyst) manages operations for a logistics giant now.",
        "best_for": ["Catalyst", "Analyst"]
    },
    {
        "name": "NMIMS Global",
        "programs": ["MBA (Executive)", "Diploma in Business Mgmt"],
        "fees": "₹1.0L - ₹4.0L",
        "accreditation": "NAAC A+, UGC-DEB",
        "success_story": "Sonia (Influencer) fast-tracked to VP HR within 18 months.",
        "best_for": ["Influencer", "Catalyst"]
    },
    {
        "name": "Chandigarh University Online",
        "programs": ["MCA", "MBA", "MA Journalism"],
        "fees": "₹50k - ₹1.5L",
        "accreditation": "NAAC A+, QS Ranked",
        "success_story": "Rahul (Creator) now leads content strategy for a top OTT platform.",
        "best_for": ["Creator", "Influencer"]
    },
     {
        "name": "DY Patil Online",
        "programs": ["BBA", "MBA in Hospital Mgmt"],
        "fees": "₹1.1L - ₹2.2L",
        "accreditation": "NAAC A++, UGC",
        "success_story": "Anjali (Catalyst) streamlined hospital ops during peak demand efficiently.",
        "best_for": ["Catalyst", "Analyst"]
    }
]

# --- DATA: 5 QUESTIONS ---
QUESTIONS = [
    {
        "q": "To start, when you face a tough problem, what's your first instinct?",
        "options": [
            ("💡 Brainstorm a unique idea", "Creator"),
            ("🗣️ Discuss with a team", "Influencer"),
            ("📊 Analyze data & facts", "Analyst"),
            ("⚡ Just start fixing it", "Catalyst")
        ]
    },
    {
        "q": "Which workspace vibe do you prefer?",
        "options": [
            ("🎨 Creative Studio", "Creator"),
            ("📢 Busy Conference Room", "Influencer"),
            ("💻 Quiet Tech Setup", "Analyst"),
            ("🏗️ On-site / Field Work", "Catalyst")
        ]
    },
    {
        "q": "How do your friends describe you?",
        "options": [
            ("✨ The Visionary", "Creator"),
            ("🎤 The Leader", "Influencer"),
            ("🧠 The Logical One", "Analyst"),
            ("🛡️ The Reliable One", "Catalyst")
        ]
    },
    {
        "q": "What drives you the most?",
        "options": [
            ("🚀 Innovation", "Creator"),
            ("🤝 Leadership", "Influencer"),
            ("🔍 Logic & Truth", "Analyst"),
            ("✅ Getting Results", "Catalyst")
        ]
    },
    {
        "q": "Pick a movie role:",
        "options": [
            ("🎬 Director", "Creator"),
            ("🌟 Lead Actor", "Influencer"),
            ("🎞️ Editor/VFX", "Analyst"),
            ("📋 Producer", "Catalyst")
        ]
    }
]

# --- SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = 0  # 0: Intro, 1: Assessment Loop, 2: Gate, 3: Results
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# --- FUNCTIONS ---

def add_bot_message(text):
    st.session_state.messages.append({"role": "assistant", "content": text})

def add_user_message(text):
    st.session_state.messages.append({"role": "user", "content": text})

def check_knowledge_base(user_text):
    """Checks if user asked about a specific term and returns answer."""
    text_lower = user_text.lower()
    for key, answer in KNOWLEDGE_BASE.items():
        if key in text_lower:
            return answer
    return None

def get_primary_energy():
    return max(st.session_state.scores, key=st.session_state.scores.get)

# --- MAIN UI ---

# Header
st.markdown("<h1 class='main-header'>Distoversity</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'><b>Eduveer</b> | Your AI Career Guide</p>", unsafe_allow_html=True)

# 1. DISPLAY CHAT HISTORY
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 2. LOGIC CONTROLLER

# --- STEP 0: WELCOME ---
if st.session_state.step == 0:
    if not st.session_state.messages:
        intro = (
            "**Namaste! I am Eduveer.** 👋\n\n"
            "I'm here to help you choose the right Online University and Career Path.\n\n"
            "I can answer your questions about **UGC, DEB, Approvals, and Placements** anytime.\n\n"
            "But first, let's find your 'Career Energy' in 5 quick questions. Ready?"
        )
        add_bot_message(intro)
        st.rerun()

    # Button to start
    if st.button("🚀 Start Assessment", key="start_btn"):
        add_user_message("Let's start!")
        st.session_state.step = 1
        st.rerun()

# --- STEP 1: ASSESSMENT LOOP (Hybrid Chat) ---
elif st.session_state.step == 1:
    current_q = QUESTIONS[st.session_state.q_index]
    
    # Ensure the question is displayed as the last bot message
    last_bot_msg = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "")
    if current_q["q"] not in last_bot_msg:
        add_bot_message(f"**Q{st.session_state.q_index + 1}/5:** {current_q['q']}")
        st.rerun()

    # LAYOUT: Options on top, Chat input on bottom
    st.write("Select an option OR ask me a question below:")
    
    # Display Options as Buttons
    cols = st.columns(2)
    for idx, (opt_text, energy) in enumerate(current_q["options"]):
        if cols[idx % 2].button(opt_text, key=f"q{st.session_state.q_index}_opt{idx}"):
            st.session_state.scores[energy] += 1
            add_user_message(opt_text) # Record answer
            
            # Progress logic
            if st.session_state.q_index < len(QUESTIONS) - 1:
                st.session_state.q_index += 1
            else:
                st.session_state.step = 2 # Go to Gate
            st.rerun()

# --- STEP 2: LEAD GEN GATE ---
elif st.session_state.step == 2:
    if "gate_shown" not in [m.get("id", "") for m in st.session_state.messages]:
        msg = "🎉 **Fantastic! Assessment Complete.**\n\nI have your Energy Profile ready. To send you the detailed career roadmap and matched universities, I just need your contact details."
        st.session_state.messages.append({"role": "assistant", "content": msg, "id": "gate_shown"})
        st.rerun()

    with st.form("lead_gate"):
        name = st.text_input("Name")
        phone = st.text_input("WhatsApp Number")
        email = st.text_input("Email")
        utype = st.radio("Current Status", ["Student", "Working Professional"])
        if st.form_submit_button("🔓 Unlock My Report"):
            if name and phone and email:
                st.session_state.user_info = {"name": name, "phone": phone, "email": email, "type": utype}
                add_user_message(f"Here are my details: {name}, {utype}")
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please fill in all details to proceed.")

# --- STEP 3: RESULTS & RECOMMENDATIONS ---
elif st.session_state.step == 3:
    primary = get_primary_energy()
    if "result_shown" not in st.session_state:
        st.session_state.result_shown = True
        
        insight = ""
        if primary == "Creator": insight = "You are a **Visionary**. You thrive on innovation and design."
        elif primary == "Influencer": insight = "You are a **Leader**. People and communication are your strengths."
        elif primary == "Analyst": insight = "You are a **Thinker**. Data, logic, and systems drive you."
        elif primary == "Catalyst": insight = "You are a **Doer**. Efficiency and operations are your forte."

        msg = f"### 🎯 Profile: {primary}\n\n{insight}\n\nBased on this, here are the best Online Universities for you:"
        add_bot_message(msg)
        st.rerun()

    # Show Recommendations
    matched_unis = [u for u in UNIVERSITIES if primary in u["best_for"]]
    if not matched_unis: matched_unis = UNIVERSITIES[:3]

    st.markdown("---")
    for uni in matched_unis:
        st.markdown(f"""
        <div class="university-card">
            <h3>{uni['name']}</h3>
            <p style="font-size:0.9rem; color:#666;">✅ {uni['accreditation']}</p>
            <p><b>Best Programs:</b> {", ".join(uni['programs'])}</p>
            <p><b>Fee Range:</b> {uni['fees']}</p>
            <p style="background-color:#eef; padding:5px; border-radius:5px;"><i>"{uni['success_story']}"</i></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("Tip: You can ask me questions about these universities below!")

# --- GLOBAL CHAT INPUT (Available in Step 1 & 3) ---
# This allows the user to interrupt the flow with questions
if st.session_state.step in [1, 3]:
    user_input = st.chat_input("Ask about UGC, Approvals, or type your answer...")
    
    if user_input:
        add_user_message(user_input)
        
        # 1. Check Knowledge Base (Interrupt Logic)
        kb_answer = check_knowledge_base(user_input)
        if kb_answer:
            response = f"🤖 **Eduveer Insight:** {kb_answer}"
            if st.session_state.step == 1:
                response += "\n\nNow, let's get back to the question above! 👆"
            add_bot_message(response)
            st.rerun()
        
        # 2. If not a KB question and in Step 1, gently nudge back
        elif st.session_state.step == 1:
            fallback = "That's interesting! I'm noting that down. To give you the best recommendation, please select one of the options above so we can complete your profile. 👇"
            add_bot_message(fallback)
            st.rerun()
            
        # 3. If in Step 3 (Results), generic fallback
        elif st.session_state.step == 3:
            add_bot_message("I'm currently focusing on university data. Feel free to book a 1:1 session for deeper career counseling!")
            st.rerun()

# --- FOOTER ---
st.markdown("<div style='text-align:center; margin-top:50px; color:#aaa;'>© 2025 Distoversity | AI Career Counseling</div>", unsafe_allow_html=True)
