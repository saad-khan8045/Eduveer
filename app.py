import streamlit as st
import pandas as pd
import time
import random

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
    /* Remove default Streamlit avatars to use our custom headers */
    .stChatMessage {{
        background-color: transparent !important;
    }}
    
    /* Assistant Bubble */
    div[data-testid="chatAvatarIcon-assistant"] {{
        display: none;
    }}
    .stChatMessage.assistant {{
        background: white;
        border-left: 5px solid {PRIMARY_BLUE};
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-radius: 0 15px 15px 15px;
        padding: 10px;
        margin-right: 20%;
    }}
    
    /* User Bubble */
    div[data-testid="chatAvatarIcon-user"] {{
        display: none;
    }}
    .stChatMessage.user {{
        background: #E3F2FD; /* Light Blue */
        border-right: 5px solid {DEEP_BLUE};
        border-radius: 15px 0 15px 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        padding: 10px;
        margin-left: 20%;
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
    
    /* DYNAMIC BUTTONS */
    .stButton>button {{
        background-color: white;
        color: {PRIMARY_BLUE};
        border: 1px solid {PRIMARY_BLUE};
        border-radius: 20px;
        font-weight: 600;
        width: 100%;
        transition: all 0.2s;
    }}
    .stButton>button:hover {{
        background-color: {PRIMARY_BLUE};
        color: white;
        transform: translateY(-2px);
    }}
    
    /* Highlight Name Header */
    .chat-header {{
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .user-header {{ color: {DEEP_BLUE}; }}
    .bot-header {{ color: {PRIMARY_BLUE}; }}

    /* COMPARISON TABLE STYLING */
    div[data-testid="stTable"] table {{
        border-collapse: separate;
        border-spacing: 0;
        width: 100%;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        overflow: hidden;
    }}
    div[data-testid="stTable"] th {{
        background-color: {PRIMARY_BLUE};
        color: white;
        font-weight: 600;
    }}
    div[data-testid="stTable"] td {{
        background-color: white;
        color: {TEXT_MAIN};
    }}
    
    /* Badges */
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

# --- EXPANDED KNOWLEDGE BASE ---
KB = {
    "placement": "All the universities I recommend have dedicated placement cells. Amity and Manipal are top-tier, often hosting virtual job fairs with companies like Amazon, Deloitte, and HDFC.",
    "valid": "100% Yes. Every university here is **UGC-DEB Approved**. In India, this is the gold standard. Your degree is legally equal to a regular campus degree for government jobs (UPSC, SSC) and higher studies.",
    "exam": "Exams are fully online with AI Proctoring. You can take them from your living room on weekends. No need to travel to centers!",
    "fee": "Most universities offer monthly EMI options (starting ₹3,000-₹5,000) so you don't have to pay the full amount upfront.",
    "lpu": "LPU is the 'Value for Money' king. NAAC A++ accredited and very affordable. Great if you want a solid degree without a huge loan.",
    "amity": "Amity is for the 'Brand Conscious'. It has global recognition and excellent networking opportunities, though it costs a bit more.",
    "manipal": "Manipal Jaipur is perfect for 'Modern Careers'. Their digital platform is slick, and they focus heavily on new-age skills like Data Science and Marketing.",
    "salary": "While it depends on your skills, an MBA/MCA from these universities can typically hike your salary by 30-50% if you are switching domains.",
    "syllabus": "The syllabus is updated regularly to match industry standards. It includes practical projects and case studies, not just theory.",
    "faculty": "You get to learn from both experienced professors and industry experts who guest lecture on weekends."
}

# --- POOL OF DYNAMIC HOOKS ---
HOOK_POOL = [
    "💰 Check Placements", "📜 Is this Valid?", "📊 Compare All", "💸 Check EMI Options",
    "🏫 Faculty Quality?", "📈 Salary Hike?", "📝 Exam Difficulty?", "🌍 Valid Abroad?",
    "📚 Syllabus Details?", "💼 Job Support?"
]

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state: st.session_state.messages = []
if "step" not in st.session_state: st.session_state.step = 0
if "q_index" not in st.session_state: st.session_state.q_index = 0
if "scores" not in st.session_state: st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "filter" not in st.session_state: st.session_state.filter = {"budget": 1000000, "course": "All"}
if "user_info" not in st.session_state: st.session_state.user_info = {}
if "current_hooks" not in st.session_state: st.session_state.current_hooks = random.sample(HOOK_POOL, 4)

# --- HELPER FUNCTIONS ---
def refresh_hooks():
    """Randomly selects 4 new hooks to keep the chat fresh"""
    st.session_state.current_hooks = random.sample(HOOK_POOL, 4)

def add_bot_msg(text, role="assistant"):
    st.session_state.messages.append({"role": role, "content": text})

def add_user_msg(text):
    st.session_state.messages.append({"role": "user", "content": text})

def get_energy():
    return max(st.session_state.scores, key=st.session_state.scores.get)

def get_bot_response(user_query):
    query = user_query.lower()
    if "placement" in query or "job" in query or "salary" in query: return KB["placement"] + " " + KB["salary"]
    if "valid" in query or "fake" in query or "ugc" in query or "abroad" in query: return KB["valid"]
    if "exam" in query: return KB["exam"]
    if "fee" in query or "cost" in query or "emi" in query: return KB["fee"]
    if "lpu" in query: return KB["lpu"]
    if "amity" in query: return KB["amity"]
    if "manipal" in query: return KB["manipal"]
    if "syllabus" in query: return KB["syllabus"]
    if "faculty" in query: return KB["faculty"]
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
                <button style="background:#FF6B6B; color:white; border:none; padding:8px; border-radius:5px; width:100%; cursor:pointer;">View Brochure</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_comparison_chart(matches):
    """Renders a pandas comparison table"""
    data = []
    for u in matches:
        data.append({
            "University": u["name"],
            "Total Fee": u["fees_display"],
            "Approvals": ", ".join(u["badges"]),
            "EMI Plan": u["emi"]
        })
    df = pd.DataFrame(data)
    st.markdown("### 📊 University Comparison Matrix")
    st.table(df)

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

# --- 1. DISPLAY CHAT STREAM ---
# This loop handles rendering messages with custom Headers for Name Flashing
for msg in st.session_state.messages:
    role = msg.get("role")
    content = msg.get("content")
    
    if role == "results_cards":
        render_matches(content)
    elif role == "comparison_chart":
        render_comparison_chart(content)
    else:
        with st.chat_message(role):
            # CUSTOM NAME HEADERS
            if role == "user":
                user_name = st.session_state.user_info.get("name", "You").split()[0].upper()
                st.markdown(f"<div class='chat-header user-header'>👤 {user_name}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-header bot-header'>🤖 Eduveer</div>", unsafe_allow_html=True)
            
            st.markdown(content)

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
    
    # Calculate matches (memoized mostly by streamlit flow)
    matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other")]
    if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2]

    if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Here are your Top Matches!**\n\nI have filtered these for your **{primary}** profile and budget.", "id": "res_msg"})
        st.session_state.messages.append({"role": "results_cards", "content": matches})
        st.session_state.messages.append({"role": "assistant", "content": "👇 **Click a question below or type your own to chat with me!**"})
        st.rerun()

    # --- DYNAMIC INTERACTIVE HOOKS ---
    # These change every time to keep it fresh
    cols = st.columns(2)
    for i, hook in enumerate(st.session_state.current_hooks):
        if cols[i % 2].button(hook, key=f"hook_{len(st.session_state.messages)}_{i}"):
            add_user_msg(hook)
            
            if hook == "📊 Compare All":
                 st.session_state.messages.append({"role": "comparison_chart", "content": matches})
                 st.session_state.messages.append({"role": "assistant", "content": "Here is the comparison. Anything else?"})
            else:
                response = get_bot_response(hook)
                add_bot_msg(response)
            
            refresh_hooks() # SHUFFLE OPTIONS FOR NEXT TURN
            st.rerun()

# CHAT INPUT
user_query = st.chat_input("Ask Eduveer (e.g., 'Is LPU valid?', 'How are placements?')")
if user_query:
    add_user_msg(user_query)
    if st.session_state.step < 4:
        response = get_bot_response(user_query)
        add_bot_msg(f"{response}\n\n_Let's continue with the assessment above!_ 👆")
    else:
        response = get_bot_response(user_query)
        add_bot_msg(response)
        refresh_hooks() # SHUFFLE OPTIONS FOR NEXT TURN
    st.rerun()
