import streamlit as st
import pandas as pd
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Distoversity | AI Career Architect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- BRAND COLORS ---
HERO_BLUE = "#0EA5E9"       # The bright blue from your banner
DARK_TEXT = "#0F172A"       # Deep navy for readability
LIGHT_TEXT = "#475569"      # Soft grey for subtitles
BG_COLOR = "#F8FAFC"        # Very light cool grey/white
CARD_WHITE = "#FFFFFF"
ACCENT_ORANGE = "#F97316"   # For highlights 
SUCCESS_GREEN = "#10B981"

# --- ADVANCED CSS (CLONING YOUR SITE UI) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    /* GLOBAL SETTINGS */
    .stApp {{
        background-color: {BG_COLOR};
        font-family: 'Inter', sans-serif;
    }}
    
    /* HIDE DEFAULT STREAMLIT UI */
    #MainMenu, footer, header {{visibility: hidden;}}
    
    /* NAVIGATION BAR */
    .nav-container {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: white;
        padding: 15px 40px;
        border-bottom: 1px solid #E2E8F0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 1000;
    }}
    .nav-logo {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: {HERO_BLUE};
    }}
    .nav-btn {{
        background-color: {HERO_BLUE};
        color: white;
        padding: 10px 20px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
    }}
    .nav-spacer {{ height: 80px; }}

    /* HERO SECTION */
    .hero-section {{
        background-color: {HERO_BLUE};
        padding: 60px 20px;
        text-align: center;
        color: white;
        border-radius: 0 0 24px 24px;
        margin-bottom: 40px;
    }}
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 15px;
    }}
    .hero-sub {{
        font-size: 1.1rem;
        opacity: 0.9;
        max-width: 700px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }}
    
    /* CHAT INTERFACE */
    .stChatMessage {{
        background: transparent;
        border: none;
    }}
    .stChatMessage.assistant {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 0 20px 20px 20px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-right: 20%;
    }}
    .stChatMessage.user {{
        background: {HERO_BLUE};
        color: white;
        border-radius: 20px 0 20px 20px;
        padding: 20px;
        margin-left: 20%;
        box-shadow: 0 4px 6px -1px rgba(0, 174, 239, 0.2);
    }}
    .stChatMessage.user p {{ color: white !important; }}

    /* UNIVERSITY CARDS */
    .uni-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 30px;
        text-align: left;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 100%;
    }}
    .uni-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: {HERO_BLUE};
    }}
    .card-icon-box {{
        width: 50px;
        height: 50px;
        background: #F0F9FF;
        color: {HERO_BLUE};
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 20px;
    }}
    .card-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: {DARK_TEXT};
        margin-bottom: 10px;
    }}
    .card-detail {{
        color: {LIGHT_TEXT};
        font-size: 0.9rem;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .card-btn {{
        display: block;
        width: 100%;
        background: {HERO_BLUE};
        color: white;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        margin-top: 20px;
        font-weight: 600;
    }}
    
    /* BUTTONS & INPUTS */
    .stButton button {{
        border-radius: 8px;
        font-weight: 600;
        border: 1px solid #E2E8F0;
        color: {DARK_TEXT};
    }}
    .stButton button:hover {{
        border-color: {HERO_BLUE};
        color: {HERO_BLUE};
    }}
    .stTextInput input {{
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 12px;
    }}
    
    /* BADGE PILLS */
    .pill {{
        background: #F1F5F9;
        color: {LIGHT_TEXT};
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    </style>
""", unsafe_allow_html=True)

# --- NAVIGATION ---
st.markdown(f"""
    <div class="nav-container">
        <div class="nav-logo">Distoversity</div>
        <a href="#" class="nav-btn">Start Assessment</a>
    </div>
    <div class="nav-spacer"></div>
""", unsafe_allow_html=True)

# --- DATA (Restored logic keys: 'max_fee' and 'programs') ---
UNIVERSITIES = [
    {"name": "Amity Online", "fee": "₹1.75L", "max_fee": 350000, "emi": "₹4,999/mo", "programs": ["MBA", "MCA", "BBA"], "badges": ["UGC", "NAAC A+"], "logo": "🅰️", "best_for": ["Analyst"]},
    {"name": "Manipal Jaipur", "fee": "₹1.50L", "max_fee": 300000, "emi": "₹3,500/mo", "programs": ["MBA", "BCA", "B.Com"], "badges": ["AICTE", "NAAC A+"], "logo": "Ⓜ️", "best_for": ["Creator"]},
    {"name": "LPU Online", "fee": "₹98k", "max_fee": 180000, "emi": "₹2,500/mo", "programs": ["M.Sc CS", "MBA", "BA"], "badges": ["UGC", "AICTE"], "logo": "🏫", "best_for": ["Catalyst"]},
    {"name": "NMIMS Global", "fee": "₹4.0L", "max_fee": 400000, "emi": "No Cost EMI", "programs": ["MBA (Ex)", "Diploma"], "badges": ["Top Ranked"], "logo": "📈", "best_for": ["Influencer"]},
    {"name": "Chandigarh Uni", "fee": "₹1.10L", "max_fee": 150000, "emi": "₹3,000/mo", "programs": ["MCA", "MBA"], "badges": ["QS Ranked"], "logo": "🏛️", "best_for": ["Creator"]},
    {"name": "DY Patil", "fee": "₹1.30L", "max_fee": 220000, "emi": "₹4,000/mo", "programs": ["BBA", "MBA"], "badges": ["NAAC A++"], "logo": "🏥", "best_for": ["Catalyst"]}
]

QUESTIONS = [
    {"q": "Problem solving style?", "options": [("💡 Creative", "Creator"), ("🗣️ Discussion", "Influencer"), ("📊 Analytical", "Analyst"), ("⚡ Action", "Catalyst")]},
    {"q": "Ideal workspace?", "options": [("🎨 Studio", "Creator"), ("📢 Boardroom", "Influencer"), ("💻 Lab", "Analyst"), ("🏗️ Field", "Catalyst")]},
    {"q": "Friend's description?", "options": [("✨ Visionary", "Creator"), ("🎤 Leader", "Influencer"), ("🧠 Brain", "Analyst"), ("🛡️ Rock", "Catalyst")]},
    {"q": "Motivator?", "options": [("🚀 Innovation", "Creator"), ("🤝 Connection", "Influencer"), ("🔍 Truth", "Analyst"), ("✅ Impact", "Catalyst")]},
    {"q": "Role?", "options": [("🎬 Director", "Creator"), ("🌟 Star", "Influencer"), ("🎞️ Editor", "Analyst"), ("📋 Producer", "Catalyst")]}
]

KB = {
    "placement": "All listed universities host Virtual Job Fairs. Top recruiters include Amazon, Deloitte, and HDFC.",
    "valid": "Yes, 100% UGC-DEB Approved. Valid for Govt Jobs and Higher Education.",
    "fee": "EMI plans start at ₹3,000/month with 0% interest options.",
    "exam": "Exams are 100% Online & Proctored (Weekend slots available)."
}

HOOK_POOL = ["💰 Check Placements", "📜 Is this Valid?", "📊 Compare All", "💸 EMI Options", "🏫 Faculty?", "📈 Salary?"]

# --- STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "step" not in st.session_state: st.session_state.step = 0
if "q_index" not in st.session_state: st.session_state.q_index = 0
if "scores" not in st.session_state: st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "user_info" not in st.session_state: st.session_state.user_info = {}
if "filter" not in st.session_state: st.session_state.filter = {"budget": 1000000, "course": "All"}
if "current_hooks" not in st.session_state: st.session_state.current_hooks = random.sample(HOOK_POOL, 4)

# --- FUNCTIONS ---
def refresh_hooks(): st.session_state.current_hooks = random.sample(HOOK_POOL, 4)
def add_bot_msg(text): st.session_state.messages.append({"role": "assistant", "content": text})
def add_user_msg(text): st.session_state.messages.append({"role": "user", "content": text})
def get_energy(): return max(st.session_state.scores, key=st.session_state.scores.get)

def get_bot_response(q):
    q = q.lower()
    if "placement" in q or "job" in q: return KB["placement"]
    if "valid" in q or "fake" in q: return KB["valid"]
    if "fee" in q or "cost" in q: return KB["fee"]
    if "exam" in q: return KB["exam"]
    return "I verify all universities for UGC approval. Do you want to check **Placements** or **Fees**?"

def render_matches(matches):
    # Using Streamlit columns to create a Grid Layout like your site
    cols = st.columns(2)
    for i, u in enumerate(matches):
        with cols[i % 2]:
            badges = "".join([f"<span class='pill'>{b}</span>" for b in u['badges']])
            st.markdown(f"""
            <div class="uni-card">
                <div class="card-icon-box">{u['logo']}</div>
                <div class="card-title">{u['name']}</div>
                <div class="card-detail">💰 {u['fee']} Total</div>
                <div class="card-detail">📅 {u['emi']}</div>
                <div style="margin-top:10px;">{badges}</div>
                <a href="#" class="card-btn">View Brochure</a>
            </div>
            """, unsafe_allow_html=True)

def render_comparison(matches):
    data = [{"Uni": u["name"], "Fee": u["fee"], "EMI": u["emi"], "Badges": ", ".join(u["badges"])} for u in matches]
    st.table(pd.DataFrame(data))

# --- MAIN LAYOUT ---

with st.container():
    
    # 1. HERO SECTION (Only show at start)
    if st.session_state.step == 0 and not st.session_state.messages:
        st.markdown(f"""
        <div class="hero-section">
            <h1 class="hero-title">Ready to Discover<br>Your Genius?</h1>
            <p class="hero-sub">Our AI-powered platform analyzes your unique personality profile and matches you with universities designed for your success.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Start Free Assessment ➔", type="primary", use_container_width=True):
                st.session_state.step = 1
                add_bot_msg("Hello! I am **Eduveer**. I'm ready to analyze your profile. Let's start with a quick question.")
                st.rerun()

    # 2. CHAT HISTORY
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "results_cards":
            render_matches(content)
        elif role == "comparison_chart":
            render_comparison(content)
        else:
            with st.chat_message(role):
                # Headers
                if role == "user":
                    name = st.session_state.user_info.get("name", "You")
                    st.markdown(f"<div style='font-size:0.8rem; font-weight:700; color:white; margin-bottom:4px;'>{name}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size:0.8rem; font-weight:700; color:#0EA5E9; margin-bottom:4px;'>Eduveer</div>", unsafe_allow_html=True)
                st.markdown(content)

    # 3. LOGIC CONTROLLER
    
    # Step 1: Assessment
    if st.session_state.step == 1:
        curr = QUESTIONS[st.session_state.q_index]
        last_bot = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "")
        
        if curr["q"] not in last_bot:
            add_bot_msg(f"**Q{st.session_state.q_index + 1}:** {curr['q']}")
            st.rerun()
            
        cols = st.columns(2)
        for i, (txt, en) in enumerate(curr["options"]):
            if cols[i%2].button(txt, key=f"q{st.session_state.q_index}_{i}", use_container_width=True):
                st.session_state.scores[en] += 1
                add_user_msg(txt)
                if st.session_state.q_index < 4:
                    st.session_state.q_index += 1
                else:
                    st.session_state.step = 2
                st.rerun()

    # Step 2: Lead Gen
    elif st.session_state.step == 2:
        primary = get_energy()
        if "gate_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": f"🌟 **You are a {primary}!**\n\nI have found universities that fit your {primary} profile perfectly. To customize the roadmap, please share your name.", "id": "gate_msg"})
            st.rerun()

        with st.form("lead_gen"):
            st.markdown("#### 🔓 Unlock Matches")
            name = st.text_input("Full Name")
            if st.form_submit_button("Continue", type="primary"):
                if name:
                    st.session_state.user_info = {"name": name}
                    add_user_msg(f"I am {name}")
                    st.session_state.step = 3
                    st.rerun()

    # Step 3: Budget Probe
    elif st.session_state.step == 3:
        if "probe_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": "Got it. What is your **Maximum Budget** for the entire course?", "id": "probe_msg"})
            st.rerun()

        col1, col2 = st.columns(2)
        with col1: course = st.selectbox("Course", ["MBA", "MCA", "BBA", "BCA", "M.Com"])
        with col2: budget = st.select_slider("Budget", ["1 Lakh", "2 Lakhs", "3 Lakhs", "4 Lakhs", "No Limit"])
        
        if st.button("Show My Universities", type="primary", use_container_width=True):
            b_map = {"1 Lakh": 100000, "2 Lakhs": 200000, "3 Lakhs": 300000, "4 Lakhs": 400000, "No Limit": 1000000}
            st.session_state.filter = {"budget": b_map[budget], "course": course}
            add_user_msg(f"Looking for {course} under {budget}")
            st.session_state.step = 4
            st.rerun()

    # Step 4: Results & Chat
    elif st.session_state.step == 4:
        primary = get_energy()
        filt = st.session_state.filter
        
        # --- RESTORED ROBUST LOGIC HERE ---
        matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other" or "Other" in u["programs"])]
        if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2] # Fallback if no budget match

        if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Top Picks for {primary} profile!**", "id": "res_msg"})
            st.session_state.messages.append({"role": "results_cards", "content": matches})
            st.rerun()

        # DYNAMIC HOOKS
        st.write("")
        cols = st.columns(2)
        for i, hook in enumerate(st.session_state.current_hooks):
            if cols[i % 2].button(hook, key=f"hook_{len(st.session_state.messages)}_{i}", use_container_width=True):
                add_user_msg(hook)
                if hook == "📊 Compare All":
                     st.session_state.messages.append({"role": "comparison_chart", "content": matches})
                     st.session_state.messages.append({"role": "assistant", "content": "Comparison generated."})
                else:
                    response = get_bot_response(hook)
                    add_bot_msg(response)
                refresh_hooks()
                st.rerun()

    # CHAT INPUT
    if st.session_state.step > 0:
        user_query = st.chat_input("Ask Eduveer anything...")
        if user_query:
            add_user_msg(user_query)
            response = get_bot_response(user_query)
            add_bot_msg(response)
            refresh_hooks()
            st.rerun()
