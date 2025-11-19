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
        background-color: {PRIMARY_BLUE};
        color: white;
        border-radius: 30px;
        border: none;
        padding: 10px 25px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #008CC2;
        transform: scale(1.02);
    }}
    .university-card {{
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 15px;
        border-left: 5px solid {PRIMARY_BLUE};
    }}
    .energy-badge {{
        background-color: {LIGHT_BLUE_BG};
        color: {PRIMARY_BLUE};
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA: UNIVERSITIES & ENERGIES ---
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

# Questions Mapping: (Option A -> Energy 1, Option B -> Energy 2...)
QUESTIONS = [
    {
        "q": "When solving a problem, what's your first instinct?",
        "options": [
            ("Brainstorm a new, unique solution.", "Creator"),
            ("Call a team meeting to discuss.", "Influencer"),
            ("Look at the data and facts first.", "Analyst"),
            ("Just start fixing it immediately.", "Catalyst")
        ]
    },
    {
        "q": "Which workspace sounds perfect to you?",
        "options": [
            ("A design studio with music and art.", "Creator"),
            ("A busy room full of people talking.", "Influencer"),
            ("A quiet room with multiple monitors.", "Analyst"),
            ("On-site, moving around, getting things done.", "Catalyst")
        ]
    },
    {
        "q": "Friends usually describe you as...",
        "options": [
            ("The Creative Visionary.", "Creator"),
            ("The Social Butterfly / Leader.", "Influencer"),
            ("The Logical Thinker.", "Analyst"),
            ("The Reliable Doer.", "Catalyst")
        ]
    },
    {
        "q": "What motivates you most?",
        "options": [
            ("Creating something that didn't exist before.", "Creator"),
            ("Leading and inspiring others.", "Influencer"),
            ("Understanding how things work (Logic).", "Analyst"),
            ("Checking items off my to-do list.", "Catalyst")
        ]
    },
    {
        "q": "Pick a role in a movie production:",
        "options": [
            ("Director/Scriptwriter.", "Creator"),
            ("Lead Actor/PR Manager.", "Influencer"),
            ("Editor/CGI Specialist.", "Analyst"),
            ("Producer/Stunt Coordinator.", "Catalyst")
        ]
    }
]

# --- SESSION STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "step" not in st.session_state:
    st.session_state.step = 0  # 0: Intro, 1: Questions, 2: Lead Gen, 3: Results
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "scores" not in st.session_state:
    st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "user_info" not in st.session_state:
    st.session_state.user_info = {}

# --- HELPER FUNCTIONS ---
def type_text(text):
    """Simulates typing effect for the bot"""
    message_placeholder = st.empty()
    full_response = ""
    for chunk in text.split():
        full_response += chunk + " "
        time.sleep(0.05) # Adjust speed here
        # In a real app, you'd yield this to the stream, but for st.chat_message we just print
    return text

def add_bot_message(text):
    st.session_state.messages.append({"role": "assistant", "content": text})

def add_user_message(text):
    st.session_state.messages.append({"role": "user", "content": text})

def get_primary_energy():
    return max(st.session_state.scores, key=st.session_state.scores.get)

# --- UI LAYOUT ---

# Header
st.markdown("<h1 class='main-header'>Distoversity</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Unlock Your Potential with <b>Eduveer</b> | AI Career Architect</p>", unsafe_allow_html=True)

# Chat Container
chat_container = st.container()

# Display Chat History
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- LOGIC FLOW ---

# STEP 0: INTRO
if st.session_state.step == 0:
    if not st.session_state.messages:
        intro_msg = (
            "**Namaste! I am Eduveer.** 👋\n\n"
            "I'm here to help you construct your perfect career blueprint. "
            "At **Distoversity**, we don't just look at grades; we look at your **Energy**.\n\n"
            "Are you a **Creator**, **Influencer**, **Catalyst**, or **Analyst**?\n\n"
            "Let's find out in 60 seconds. Ready to unlock your profile?"
        )
        add_bot_message(intro_msg)
        st.rerun()
    
    if st.button("🚀 Start My Discovery"):
        add_user_message("I'm ready! Let's start.")
        st.session_state.step = 1
        st.rerun()

# STEP 1: ASSESSMENT (5 Questions)
elif st.session_state.step == 1:
    q_data = QUESTIONS[st.session_state.q_index]
    
    # Ask the question if it hasn't been asked in the last message
    last_msg = st.session_state.messages[-1]["content"]
    if q_data["q"] not in last_msg:
        add_bot_message(f"**Q{st.session_state.q_index + 1}:** {q_data['q']}")
        st.rerun()

    # Display Options
    cols = st.columns(2)
    for idx, (option_text, energy_type) in enumerate(q_data["options"]):
        col = cols[idx % 2]
        if col.button(option_text, key=f"q{st.session_state.q_index}_opt{idx}"):
            # Logic when clicked
            st.session_state.scores[energy_type] += 1
            add_user_message(option_text)
            
            # Move to next question or finish
            if st.session_state.q_index < len(QUESTIONS) - 1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.session_state.step = 2
                st.rerun()

# STEP 2: THE GATE (Lead Gen)
elif st.session_state.step == 2:
    if "gate_msg" not in [m.get("id", "") for m in st.session_state.messages]: # Prevent duplicate msg
        msg = "⚡ **Brilliant! Analysis Complete.**\n\nI have calculated your unique Energy Profile and selected 3 top universities that match your DNA.\n\n**Please enter your details to generate your detailed Career Report.**"
        add_bot_message(msg)
        st.session_state.messages[-1]["id"] = "gate_msg" # Flag to ensure single execution
        st.rerun()

    with st.form("lead_gen_form"):
        name = st.text_input("Full Name", placeholder="e.g. Veer Sharma")
        phone = st.text_input("Mobile Number", placeholder="e.g. 9876543210")
        email = st.text_input("Email Address", placeholder="e.g. veer@gmail.com")
        is_student = st.radio("Are you currently:", ["Student", "Working Professional"])
        
        submitted = st.form_submit_button("🔓 Unlock My Report")
        
        if submitted:
            if name and phone and email:
                st.session_state.user_info = {
                    "name": name, 
                    "phone": phone, 
                    "email": email, 
                    "type": is_student
                }
                add_user_message(f"Details shared. Name: {name}, Type: {is_student}")
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please fill in all fields to proceed.")

# STEP 3: THE REVELATION (Results)
elif st.session_state.step == 3:
    # Calculate Result
    primary_energy = get_primary_energy()
    user_name = st.session_state.user_info['name']
    
    # Display Results only once
    if "result_shown" not in st.session_state:
        st.session_state.result_shown = True
        
        # Personalized Insight
        insight = ""
        if primary_energy == "Creator":
            insight = "You are built for **Innovation**. You see things others miss. Your ideal career involves design, strategy, or entrepreneurship."
        elif primary_energy == "Influencer":
            insight = "You are a natural **Leader**. Your power lies in communication. Sales, HR, and Management are your playgrounds."
        elif primary_energy == "Analyst":
            insight = "You are driven by **Logic**. Data is your weapon. Tech, Finance, and Research are where you will thrive."
        elif primary_energy == "Catalyst":
            insight = "You are the **Engine**. You get things done. Operations, Logistics, and Project Management need you."

        final_msg = (
            f"### 🎯 Analysis for {user_name}\n\n"
            f"**Dominant Energy:** 🌟 **{primary_energy}**\n\n"
            f"{insight}\n\n"
            "Based on your profile, here are the **Top University Programs** that align with your natural strengths:"
        )
        add_bot_message(final_msg)
        st.rerun()

    # --- DISPLAY RECOMMENDATIONS (Outside Chat Bubble for better UI) ---
    st.markdown("---")
    st.subheader(f"🎓 Curated for {primary_energy}s")
    
    # Filter Logic (Simple Recommendation Engine)
    recommended = [u for u in UNIVERSITIES if primary_energy in u["best_for"]]
    
    # Fallback if not enough specific matches, show top rated
    if len(recommended) < 2:
        recommended = UNIVERSITIES[:3]

    for uni in recommended:
        with st.container():
            st.markdown(f"""
            <div class="university-card">
                <h3>{uni['name']} <span style="font-size:0.8rem; color:#777;">({uni['accreditation']})</span></h3>
                <p><b>Recommended Degrees:</b> {", ".join(uni['programs'])}</p>
                <p><b>Investment:</b> {uni['fees']}</p>
                <p style="background-color: #E0F2FE; padding: 8px; border-radius: 8px; font-style: italic; color: #005f85;">
                    💡 <b>Real Success:</b> {uni['success_story']}
                </p>
            </div>
            """, unsafe_allow_html=True)

    # --- FINAL CTA ---
    st.markdown("---")
    st.info("Want to map out your exact roadmap with a human expert?")
    
    col1, col2 = st.columns([1, 4])
    with col2:
        st.button("📅 Book Free 1:1 Career Strategy Session", type="primary")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; margin-top: 50px; color: #aaa; font-size: 0.8rem;">
        © 2025 Distoversity Pvt Ltd | AI Career Counseling<br>
        <i>Empowering India's Future</i>
    </div>
""", unsafe_allow_html=True)
