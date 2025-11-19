import streamlit as st
import time

# --- CONFIGURATION & THEME ---
st.set_page_config(
    page_title="Distoversity | Eduveer",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- BRAND PALETTE ---
PRIMARY_BLUE = "#00AEEF"
DEEP_BLUE = "#003366"
ACCENT_ORANGE = "#FF6B6B"
BG_COLOR = "#F4F7F6"
TEXT_MAIN = "#2D3748"
SUCCESS_GREEN = "#38A169"

# --- CSS STYLING ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;600;700&display=swap');

    .stApp {{
        background-color: {BG_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    
    h1, h2, h3 {{
        font-family: 'Poppins', sans-serif;
        color: {DEEP_BLUE};
    }}

    /* HERO & TRUST */
    .hero-box {{
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, {DEEP_BLUE} 0%, {PRIMARY_BLUE} 100%);
        color: white;
        border-radius: 0 0 20px 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0, 51, 102, 0.15);
    }}
    .trust-bar {{
        display: flex;
        justify-content: center;
        gap: 20px;
        background: white;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 0.8rem;
        color: #555;
        font-weight: 600;
    }}

    /* CHAT UI */
    .stChatMessage.assistant {{
        background: white;
        border-left: 4px solid {PRIMARY_BLUE};
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-radius: 0 12px 12px 12px;
    }}
    .stChatMessage.user {{
        background: #EBF8FF;
        border-right: 4px solid {DEEP_BLUE};
        border-radius: 12px 0 12px 12px;
        text-align: right;
    }}

    /* CARDS */
    .cv-card {{
        background: white;
        border-radius: 12px;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
        overflow: hidden;
    }}
    .cv-header {{
        padding: 15px 20px;
        border-bottom: 1px solid #EDF2F7;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .cv-body {{ padding: 15px 20px; }}
    .cv-footer {{
        background: #F7FAFC;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #EDF2F7;
    }}
    
    /* BUTTONS & HOOKS */
    .stButton>button {{
        background-color: white;
        color: {PRIMARY_BLUE};
        border: 1px solid {PRIMARY_BLUE};
        border-radius: 20px; /* Pill shape for hooks */
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }}
    .stButton>button:hover {{
        background-color: {PRIMARY_BLUE};
        color: white;
        transform: translateY(-2px);
    }}
    .primary-btn {{
        background-color: {ACCENT_ORANGE};
        color: white;
        padding: 8px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
        border: none;
        cursor: pointer;
    }}

    /* BADGES */
    .verified-badge {{
        background: #F0FFF4;
        color: {SUCCESS_GREEN};
        border: 1px solid #C6F6D5;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA ---
UNIVERSITIES = [
    {"name": "Amity Online", "programs": ["MBA", "MCA", "BBA"], "max_fee": 350000, "fees_display": "₹1.75 Lakhs", "emi": "Starts ₹4,999/mo", "badges": ["UGC-DEB", "NAAC A+"], "best_for": ["Analyst", "Influencer"], "logo": "🅰️"},
    {"name": "Manipal Jaipur", "programs": ["MBA", "BCA", "B.Com"], "max_fee": 300000, "fees_display": "₹1.50 Lakhs", "emi": "Starts ₹3,500/mo", "badges": ["NAAC A+", "AICTE"], "best_for": ["Creator", "Influencer"], "logo": "Ⓜ️"},
    {"name": "LPU Online", "programs": ["M.Sc CS", "MBA", "BA"], "max_fee": 180000, "fees_display": "₹98,000 Total", "emi": "Starts ₹2,500/mo", "badges": ["UGC Entitled", "AICTE"], "best_for": ["Catalyst", "Analyst"], "logo": "🏫"},
    {"name": "NMIMS Global", "programs": ["MBA (Ex)", "Diploma"], "max_fee": 400000, "fees_display": "₹4.0 Lakhs", "emi": "No Cost EMI", "badges": ["NAAC A+", "Top B-School"], "best_for": ["Influencer", "Catalyst"], "logo": "📈"},
    {"name": "Chandigarh Uni", "programs": ["MCA", "MBA"], "max_fee": 150000, "fees_display": "₹1.10 Lakhs", "emi": "Starts ₹3,000/mo", "badges": ["NAAC A+", "QS Ranked"], "best_for": ["Creator", "Influencer"], "logo": "🏛️"},
    {"name": "DY Patil", "programs": ["BBA", "MBA"], "max_fee": 220000, "fees_display": "₹1.30 Lakhs", "emi": "Starts ₹4,000/mo", "badges": ["NAAC A++", "UGC"], "best_for": ["Catalyst", "Analyst"], "logo": "🏥"}
]

QUESTIONS = [
    {"q": "First, how do you usually handle a crisis?", "options": [("Create a new solution", "Creator"), ("Brainstorm with team", "Influencer"), ("Analyze the data", "Analyst"), ("Just fix it fast", "Catalyst")]},
    {"q": "Your ideal workspace looks like:", "options": [("Artistic Studio", "Creator"), ("Busy Meeting Room", "Influencer"), ("Quiet Tech Lab", "Analyst"), ("On the Field", "Catalyst")]},
    {"q": "In your friend group, you are:", "options": [("The Visionary", "Creator"), ("The Leader", "Influencer"), ("The Logical One", "Analyst"), ("The Reliable One", "Catalyst")]},
    {"q": "What motivates you most?", "options": [("Innovation", "Creator"), ("People", "Influencer"), ("Facts & Truth", "Analyst"), ("Results", "Catalyst")]},
    {"q": "Pick a movie role:", "options": [("Director", "Creator"), ("Hero", "Influencer"), ("Editor", "Analyst"), ("Producer", "Catalyst")]}
]

# --- KNOWLEDGE BASE ---
KB = {
    "placement": "All the universities I recommend have dedicated placement cells. For example, Amity and Manipal conduct virtual job fairs with top recruiters like Amazon and Deloitte.",
    "valid": "Yes! Every university listed here is **UGC-DEB Approved**. The degree is legally equivalent to a regular campus degree for government jobs and further studies.",
    "exam": "Exams are conducted online with AI proctoring. You can take them from home on weekends, so your job isn't disturbed.",
    "fee": "Most universities offer EMI options starting as low as ₹3,000/month to make it affordable.",
    "lpu": "LPU is excellent for affordability and holds NAAC A++ accreditation. It's a great choice if you want a recognized degree on a budget.",
    "amity": "Amity is a premium choice known for its global recognition and strong corporate network.",
    "manipal": "Manipal Jaipur is fantastic for new-age courses like BCA and Digital Marketing with great content delivery."
}

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state: st.session_state.messages = []
if "step" not in st.session_state: st.session_state.step = 0
if "q_index" not in st.session_state: st.session_state.q_index = 0
if "scores" not in st.session_state: st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "filter" not in st.session_state: st.session_state.filter = {"budget": 1000000, "course": "All"}

# --- HELPER FUNCTIONS ---
def add_bot_msg(text, role="assistant"):
    st.session_state.messages.append({"role": role, "content": text})

def add_user_msg(text):
    st.session_state.messages.append({"role": "user", "content": text})

def get_energy():
    return max(st.session_state.scores, key=st.session_state.scores.get)

def get_bot_response(user_query):
    query = user_query.lower()
    if "placement" in query or "job" in query: return KB["placement"]
    if "valid" in query or "fake" in query or "ugc" in query: return KB["valid"]
    if "exam" in query: return KB["exam"]
    if "fee" in query or "cost" in query: return KB["fee"]
    if "lpu" in query: return KB["lpu"]
    if "amity" in query: return KB["amity"]
    if "manipal" in query: return KB["manipal"]
    return "That's a great question. I focus on finding UGC-approved universities. Would you like to know about their **Placements**, **Fees**, or **Validity**?"

def render_matches(matches):
    """Renders the university cards"""
    for u in matches:
        badges = "".join([f"<span class='verified-badge'>{b}</span> " for b in u['badges']])
        st.markdown(f"""
        <div class="cv-card">
            <div class="cv-header">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-size:1.8rem;">{u['logo']}</span>
                    <div>
                        <div style="font-weight:700; font-size:1.1rem; color:#003366;">{u['name']}</div>
                        <div style="font-size:0.8rem; color:#718096;">{badges}</div>
                    </div>
                </div>
            </div>
            <div class="cv-body">
                <div style="display:flex; justify-content:space-between; font-size:0.9rem; margin-bottom:10px;">
                    <span>💰 <b>{u['fees_display']}</b></span>
                    <span>📅 <b>{u['emi']}</b></span>
                </div>
                <div style="font-size:0.85rem; color:#555;">Best for: {", ".join(u['best_for'])}</div>
            </div>
            <div class="cv-footer">
                <button class="primary-btn" style="width:100%;">View Brochure</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN UI HEADER ---
st.markdown(f"""
    <div class="hero-box">
        <h1 style="color:white; margin:0; font-size:1.8rem;">Distoversity</h1>
        <p style="opacity:0.9; font-size:0.9rem;">AI Career Architect | <b>Ask Me Anything</b></p>
    </div>
    <div class="trust-bar">
        <div>✅ UGC Verified</div>
        <div>✅ Unbiased</div>
        <div>✅ Free Help</div>
    </div>
""", unsafe_allow_html=True)

# --- 1. DISPLAY CHAT STREAM (This handles Text AND Cards) ---
for msg in st.session_state.messages:
    # Special handler for "Card Messages" so they scroll up with history
    if msg.get("role") == "results_cards":
        render_matches(msg["content"])
    
    # Standard Text Messages
    else:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 2. LOGIC CONTROLLER ---

# STEP 0: INTRO
if st.session_state.step == 0:
    if not st.session_state.messages:
        add_bot_msg("👋 **Hi, I'm Eduveer.**\n\nI'm here to help you find the right online university. We can chat, but first, I need to understand **YOU**.\n\nReady for a quick 1-minute personality check?")
        st.rerun()
    
    if st.button("🚀 Start Assessment"):
        st.session_state.step = 1
        st.rerun()

# STEP 1: ASSESSMENT
elif st.session_state.step == 1:
    curr = QUESTIONS[st.session_state.q_index]
    last_bot = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "")
    
    if curr["q"] not in last_bot:
        add_bot_msg(f"**Q{st.session_state.q_index + 1}:** {curr['q']}")
        st.rerun()

    cols = st.columns(2)
    for i, (txt, en) in enumerate(curr["options"]):
        if cols[i%2].button(txt, key=f"q{st.session_state.q_index}_{i}"):
            st.session_state.scores[en] += 1
            add_user_msg(txt)
            if st.session_state.q_index < 4:
                st.session_state.q_index += 1
            else:
                st.session_state.step = 2
            st.rerun()

# STEP 2: LEAD GATE
elif st.session_state.step == 2:
    primary = get_energy()
    if "gate_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        st.session_state.messages.append({"role": "assistant", "content": f"🌟 **You are a {primary}!**\n\nI've found universities that match your style. To unlock the full list and enable **Chat Mode**, please share your name.", "id": "gate_msg"})
        st.rerun()

    with st.form("lead_gen"):
        name = st.text_input("Your Name")
        phone = st.text_input("WhatsApp (Optional)")
        if st.form_submit_button("Unlock Results"):
            if name:
                st.session_state.user_info = {"name": name}
                add_user_msg(f"I am {name}")
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Name is required.")

# STEP 3: PROBE (Budget)
elif st.session_state.step == 3:
    if "probe_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        st.session_state.messages.append({"role": "assistant", "content": "Got it. One last question to filter the list: **What is your comfortable budget?**", "id": "probe_msg"})
        st.rerun()

    col1, col2 = st.columns(2)
    with col1: course = st.selectbox("Course", ["MBA", "MCA", "BBA", "BCA", "M.Com", "MA"])
    with col2: budget = st.select_slider("Max Budget", ["1 Lakh", "2 Lakhs", "3 Lakhs", "4 Lakhs", "No Limit"])
    
    if st.button("Show Matches"):
        b_map = {"1 Lakh": 100000, "2 Lakhs": 200000, "3 Lakhs": 300000, "4 Lakhs": 400000, "No Limit": 1000000}
        st.session_state.filter = {"budget": b_map[budget], "course": course}
        add_user_msg(f"I need {course} under {budget}")
        st.session_state.step = 4
        st.rerun()

# STEP 4: RESULTS (Initial Generation)
elif st.session_state.step == 4:
    primary = get_energy()
    filt = st.session_state.filter
    
    if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        # 1. Add Text Message
        st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Here are your Top Matches!**\n\nI have filtered these for your **{primary}** profile and budget.", "id": "res_msg"})
        
        # 2. Add CARDS as a Message (This makes them scrollable!)
        matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other")]
        if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2]
        
        st.session_state.messages.append({"role": "results_cards", "content": matches})
        
        # 3. Add Follow-up Text
        st.session_state.messages.append({"role": "assistant", "content": "👇 **Click a question below or type your own to chat with me!**"})
        st.rerun()

# --- 3. INTERACTIVE HOOKS & INPUT ---
# Only show hooks if we are in the final chat stage
if st.session_state.step == 4:
    
    # SMART HOOKS (Buttons that act like user input)
    hooks = ["💰 Check Placements", "📜 Is this Valid?", "💸 Check EMI Options", "🏦 Compare Fees"]
    cols = st.columns(2)
    for i, hook in enumerate(hooks):
        if cols[i % 2].button(hook, key=f"hook_{i}"):
            # Treat click as user input
            add_user_msg(hook)
            response = get_bot_response(hook)
            add_bot_msg(response)
            st.rerun()

# CHAT INPUT
user_query = st.chat_input("Ask Eduveer (e.g., 'Is LPU valid?', 'How are placements?')")
if user_query:
    add_user_msg(user_query)
    
    # Logic for handling chat based on step
    if st.session_state.step < 4:
        response = get_bot_response(user_query)
        add_bot_msg(f"{response}\n\n_Let's continue with the assessment above!_ 👆")
    else:
        response = get_bot_response(user_query)
        add_bot_msg(response)
    st.rerun()
