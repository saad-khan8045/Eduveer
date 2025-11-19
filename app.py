import streamlit as st
import time
import random

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Distoversity | Eduveer",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Brand Colors
PRIMARY_BLUE = "#00AEEF"
DARK_BLUE = "#0077A3"
LIGHT_BLUE_BG = "#E0F2FE"
WHITE = "#FFFFFF"
TEXT_DARK = "#1E293B"
TEXT_GRAY = "#64748B"

# --- PREMIUM STYLING (CSS) ---
st.markdown(f"""
    <style>
    /* IMPORT GOOGLE FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    /* GLOBAL SETTINGS */
    .stApp {{
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3 {{
        font-family: 'Poppins', sans-serif;
        color: {TEXT_DARK};
    }}
    
    p, div {{
        color: {TEXT_DARK};
        line-height: 1.6;
    }}

    /* HEADER STYLES */
    .main-header {{
        color: {PRIMARY_BLUE};
        text-align: center;
        font-weight: 700;
        font-size: 3rem;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }}
    
    .sub-header {{
        color: {TEXT_GRAY};
        text-align: center;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 3rem;
    }}

    /* CHAT INTERFACE IMPROVEMENTS */
    .stChatMessage {{
        background-color: transparent;
        border: none;
    }}
    
    /* User Bubble */
    .stChatMessage.user {{
        background: linear-gradient(135deg, {LIGHT_BLUE_BG} 0%, #FFFFFF 100%);
        border: 1px solid #BAE6FD;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }}
    
    /* Bot Bubble */
    .stChatMessage.assistant {{
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }}

    /* BUTTONS */
    .stButton>button {{
        font-family: 'Poppins', sans-serif;
        background-color: #FFFFFF;
        color: {PRIMARY_BLUE};
        border-radius: 50px;
        border: 2px solid {PRIMARY_BLUE};
        padding: 12px 28px;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 6px rgba(0, 174, 239, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    .stButton>button:hover {{
        background-color: {PRIMARY_BLUE};
        color: #FFFFFF;
        box-shadow: 0 10px 15px rgba(0, 174, 239, 0.3);
        transform: translateY(-2px);
        border-color: {PRIMARY_BLUE};
    }}
    
    /* INPUT FIELDS */
    .stTextInput>div>div>input {{
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        padding: 10px 15px;
    }}
    .stTextInput>div>div>input:focus {{
        border-color: {PRIMARY_BLUE};
        box-shadow: 0 0 0 2px rgba(0, 174, 239, 0.2);
    }}

    /* UNIVERSITY CARDS - PREMIUM DESIGN */
    .university-card {{
        background: #FFFFFF;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        margin-bottom: 24px;
        border: 1px solid #F1F5F9;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .university-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }}
    
    .university-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: {PRIMARY_BLUE};
    }}

    .card-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
    }}

    .card-badge {{
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background-color: #F0F9FF;
        color: {DARK_BLUE};
        margin-bottom: 1rem;
    }}

    .success-story {{
        background-color: #F8FAFC;
        padding: 12px 16px;
        border-radius: 12px;
        border-left: 3px solid #CBD5E1;
        font-style: italic;
        color: {TEXT_GRAY};
        font-size: 0.9rem;
        margin-top: 1rem;
    }}

    /* FOOTER */
    .footer {{
        text-align: center;
        margin-top: 60px;
        padding-top: 20px;
        border-top: 1px solid #E2E8F0;
        color: #94A3B8;
        font-size: 0.85rem;
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA: KNOWLEDGE BASE ---
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
        "accreditation": "UGC-DEB | NAAC A+",
        "success_story": "Rohan (Analyst) shifted from Sales to Data Analytics with a 40% hike.",
        "best_for": ["Analyst", "Influencer"]
    },
    {
        "name": "Manipal University Jaipur",
        "programs": ["MBA", "B.Com", "M.Com", "BCA"],
        "fees": "₹1.2L - ₹3.0L",
        "accreditation": "NAAC A+ | AICTE",
        "success_story": "Priya (Creator) launched her digital agency post their Digital Marketing elective.",
        "best_for": ["Creator", "Influencer"]
    },
    {
        "name": "LPU Online",
        "programs": ["M.Sc CS", "MBA", "BA", "MA"],
        "fees": "₹80k - ₹1.8L",
        "accreditation": "UGC Entitled | WES",
        "success_story": "Amit (Catalyst) manages operations for a logistics giant now.",
        "best_for": ["Catalyst", "Analyst"]
    },
    {
        "name": "NMIMS Global",
        "programs": ["MBA (Executive)", "Diploma in Business"],
        "fees": "₹1.0L - ₹4.0L",
        "accreditation": "NAAC A+ | UGC-DEB",
        "success_story": "Sonia (Influencer) fast-tracked to VP HR within 18 months.",
        "best_for": ["Influencer", "Catalyst"]
    },
    {
        "name": "Chandigarh University",
        "programs": ["MCA", "MBA", "MA Journalism"],
        "fees": "₹50k - ₹1.5L",
        "accreditation": "NAAC A+ | QS Ranked",
        "success_story": "Rahul (Creator) now leads content strategy for a top OTT platform.",
        "best_for": ["Creator", "Influencer"]
    },
     {
        "name": "DY Patil Online",
        "programs": ["BBA", "MBA in Hospital Mgmt"],
        "fees": "₹1.1L - ₹2.2L",
        "accreditation": "NAAC A++ | UGC",
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
st.markdown("<p class='sub-header'><b>Eduveer</b> | The AI Career Architect</p>", unsafe_allow_html=True)

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
            "I'm here to help you construct your perfect career path. "
            "We don't just look at grades; we look at your **Natural Energy**.\n\n"
            "Are you a **Creator**, **Influencer**, **Catalyst**, or **Analyst**?\n\n"
            "Let's find out in 60 seconds. Ready to unlock your profile?"
        )
        add_bot_message(intro)
        st.rerun()

    # Button to start
    if st.button("🚀 Start My Discovery", key="start_btn"):
        add_user_message("I'm ready! Let's start.")
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
    st.write("") # Spacer
    
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
        msg = "🎉 **Fantastic! Analysis Complete.**\n\nI have calculated your unique Energy Profile. To unlock your detailed Career Report and University matches, please verify your identity."
        st.session_state.messages.append({"role": "assistant", "content": msg, "id": "gate_shown"})
        st.rerun()

    with st.form("lead_gate"):
        st.markdown("### 🔐 Verification")
        name = st.text_input("Full Name")
        phone = st.text_input("Mobile / WhatsApp")
        email = st.text_input("Email Address")
        utype = st.radio("I am currently:", ["Student", "Working Professional"], horizontal=True)
        
        submitted = st.form_submit_button("🔓 Unlock My Report")
        if submitted:
            if name and phone and email:
                st.session_state.user_info = {"name": name, "phone": phone, "email": email, "type": utype}
                add_user_message(f"Shared my details: {name}")
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please fill in all fields to proceed.")

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

        msg = f"### 🎯 Profile Match: {primary}\n\n{insight}\n\nBased on this, I have curated the **Top 3 Online Universities** that align with your strengths:"
        add_bot_message(msg)
        st.rerun()

    # Show Recommendations (PREMIUM CARDS)
    matched_unis = [u for u in UNIVERSITIES if primary in u["best_for"]]
    if not matched_unis: matched_unis = UNIVERSITIES[:3]

    st.markdown("---")
    st.subheader(f"🎓 Curated for {primary}s")
    
    for uni in matched_unis:
        st.markdown(f"""
        <div class="university-card">
            <div class="card-title">{uni['name']}</div>
            <span class="card-badge">✅ {uni['accreditation']}</span>
            <p style="margin-bottom: 5px;"><b>🎓 Top Programs:</b> {", ".join(uni['programs'])}</p>
            <p style="margin-bottom: 5px;"><b>💰 Investment:</b> {uni['fees']}</p>
            <div class="success-story">
                💡 "{uni['success_story']}"
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("Tip: You can ask me questions about these universities below!")

# --- GLOBAL CHAT INPUT (Available in Step 1 & 3) ---
if st.session_state.step in [1, 3]:
    user_input = st.chat_input("Ask about UGC, Approvals, or type your answer...")
    
    if user_input:
        add_user_message(user_input)
        
        # 1. Check Knowledge Base
        kb_answer = check_knowledge_base(user_input)
        if kb_answer:
            response = f"🤖 **Eduveer Insight:** {kb_answer}"
            if st.session_state.step == 1:
                response += "\n\nNow, let's get back to the question above! 👆"
            add_bot_message(response)
            st.rerun()
        
        # 2. Step 1 Fallback
        elif st.session_state.step == 1:
            fallback = "That's interesting! I'm noting that down. To give you the best recommendation, please select one of the options above so we can complete your profile. 👇"
            add_bot_message(fallback)
            st.rerun()
            
        # 3. Step 3 Fallback
        elif st.session_state.step == 3:
            add_bot_message("I'm currently focusing on university data. Feel free to book a 1:1 session for deeper career counseling!")
            st.rerun()

# --- FOOTER ---
st.markdown("""
    <div class="footer">
        © 2025 Distoversity Pvt Ltd | AI Career Counseling<br>
        <i>Empowering India's Future</i>
    </div>
""", unsafe_allow_html=True)
