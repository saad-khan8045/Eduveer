import streamlit as st
import pandas as pd
import time
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Distoversity | Premium Career Architect",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- BRAND IDENTITY ---
BRAND_PRIMARY = "#0EA5E9"   # Your Brand Blue
BRAND_DARK = "#0F172A"      # Slate 900 for Text
BRAND_LIGHT = "#F1F5F9"     # Slate 100 for Backgrounds
ACCENT_ORANGE = "#F97316"   # Orange for 'Recommended'
SUCCESS_GREEN = "#10B981"   # Green for 'Verified'
WHITE = "#FFFFFF"

# --- ADVANCED CSS SYSTEM ---
st.markdown(f"""
    <style>
    /* IMPORT PREMIUM FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    /* RESET & GLOBAL */
    .stApp {{
        background-color: #F8FAFC; /* Slate 50 */
        font-family: 'Inter', sans-serif;
        color: {BRAND_DARK};
    }}
    
    /* HIDE STREAMLIT CHROME */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* --- COMPONENT: NAVBAR --- */
    .nav-bar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background: white;
        border-bottom: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 5%;
        z-index: 9999;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    .nav-logo {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: {BRAND_PRIMARY};
        letter-spacing: -0.5px;
    }}
    .nav-right {{
        font-size: 0.9rem;
        font-weight: 500;
        color: #64748B;
    }}
    .nav-spacer {{ height: 80px; }}

    /* --- COMPONENT: HERO --- */
    .hero-container {{
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(180deg, white 0%, #F8FAFC 100%);
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 40px;
    }}
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        color: {BRAND_DARK};
        line-height: 1.1;
        margin-bottom: 20px;
    }}
    .hero-subtitle {{
        font-size: 1.2rem;
        color: #64748B;
        max-width: 600px;
        margin: 0 auto 30px auto;
    }}

    /* --- COMPONENT: UNIVERSITY CARD --- */
    .uni-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        transition: all 0.3s ease;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
    }}
    .uni-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-color: {BRAND_PRIMARY};
    }}
    .uni-header {{
        display: flex;
        align-items: flex-start;
        gap: 15px;
        margin-bottom: 20px;
    }}
    .uni-logo {{
        width: 48px;
        height: 48px;
        background: #F0F9FF;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
    }}
    .uni-name {{
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        color: {BRAND_DARK};
        line-height: 1.3;
    }}
    .uni-badge-row {{
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 5px;
    }}
    .uni-pill {{
        font-size: 0.7rem;
        font-weight: 600;
        padding: 2px 8px;
        border-radius: 12px;
        background: #F1F5F9;
        color: #475569;
    }}
    .verified-pill {{
        background: #ECFDF5;
        color: {SUCCESS_GREEN};
        border: 1px solid #A7F3D0;
    }}
    
    .uni-stats {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px;
        background: #F8FAFC;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    .stat-label {{
        font-size: 0.75rem;
        text-transform: uppercase;
        color: #94A3B8;
        font-weight: 600;
        margin-bottom: 4px;
    }}
    .stat-value {{
        font-size: 0.95rem;
        font-weight: 700;
        color: {BRAND_DARK};
    }}
    
    .uni-footer {{
        margin-top: auto;
    }}
    .uni-btn {{
        display: block;
        width: 100%;
        text-align: center;
        background: {BRAND_PRIMARY};
        color: white;
        font-weight: 600;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        transition: background 0.2s;
    }}
    .uni-btn:hover {{
        background: #0284C7;
        color: white;
    }}

    /* --- COMPONENT: CHAT BUBBLES --- */
    .chat-container {{
        max-width: 800px;
        margin: 0 auto;
    }}
    .stChatMessage {{
        background: transparent;
        border: none;
    }}
    .stChatMessage.assistant {{
        background: white;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-radius: 12px 12px 12px 0;
        padding: 20px;
        margin-right: 10%;
    }}
    .stChatMessage.user {{
        background: {BRAND_DARK};
        color: white;
        border-radius: 12px 12px 0 12px;
        padding: 20px;
        margin-left: 10%;
        text-align: right;
    }}
    .stChatMessage.user p {{ color: white !important; }}
    
    /* --- COMPONENT: BUTTONS & INPUTS --- */
    .stButton button {{
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
        border: 1px solid #CBD5E1;
        color: {BRAND_DARK};
    }}
    .stButton button:hover {{
        border-color: {BRAND_PRIMARY};
        color: {BRAND_PRIMARY};
        background: #F0F9FF;
    }}
    .stTextInput input {{
        border-radius: 8px;
        border: 1px solid #CBD5E1;
        padding: 12px;
    }}

    /* --- TABLE --- */
    table {{
        width: 100%;
        border-collapse: collapse;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    th {{
        background: {BRAND_PRIMARY};
        color: white;
        padding: 12px;
        text-align: left;
    }}
    td {{
        border-bottom: 1px solid #F1F5F9;
        padding: 12px;
        color: {BRAND_DARK};
    }}
    </style>
""", unsafe_allow_html=True)

# --- LAYOUT COMPONENTS ---

def navbar():
    st.markdown(f"""
        <div class="nav-bar">
            <div class="nav-logo">Distoversity</div>
            <div class="nav-right">Premium Career Intelligence</div>
        </div>
        <div class="nav-spacer"></div>
    """, unsafe_allow_html=True)

def hero_section():
    st.markdown(f"""
        <div class="hero-container">
            <h1 class="hero-title">Discover Your<br><span style="color:{BRAND_PRIMARY}">Educational DNA</span></h1>
            <p class="hero-subtitle">Our AI analyzes your personality profile and matches you with universities designed for your specific career trajectory.</p>
        </div>
    """, unsafe_allow_html=True)

# --- DATA & LOGIC (PRESERVED) ---
UNIVERSITIES = [
    {"name": "Amity Online", "fee": "₹1.75L", "max_fee": 350000, "emi": "₹4,999/mo", "programs": ["MBA", "MCA", "BBA"], "badges": ["UGC", "NAAC A+"], "logo": "🅰️", "best_for": ["Analyst"]},
    {"name": "Manipal Jaipur", "fee": "₹1.50L", "max_fee": 300000, "emi": "₹3,500/mo", "programs": ["MBA", "BCA", "B.Com"], "badges": ["AICTE", "NAAC A+"], "logo": "Ⓜ️", "best_for": ["Creator"]},
    {"name": "LPU Online", "fee": "₹98k", "max_fee": 180000, "emi": "₹2,500/mo", "programs": ["M.Sc CS", "MBA", "BA"], "badges": ["UGC", "AICTE"], "logo": "🏫", "best_for": ["Catalyst"]},
    {"name": "NMIMS Global", "fee": "₹4.0L", "max_fee": 400000, "emi": "No Cost EMI", "programs": ["MBA (Ex)", "Diploma"], "badges": ["Top Ranked"], "logo": "📈", "best_for": ["Influencer"]},
    {"name": "Chandigarh Uni", "fee": "₹1.10L", "max_fee": 150000, "emi": "₹3,000/mo", "programs": ["MCA", "MBA"], "badges": ["QS Ranked"], "logo": "🏛️", "best_for": ["Creator"]},
    {"name": "DY Patil", "fee": "₹1.30L", "max_fee": 220000, "emi": "₹4,000/mo", "programs": ["BBA", "MBA"], "badges": ["NAAC A++"], "logo": "🏥", "best_for": ["Catalyst"]}
]

QUESTIONS = [
    {"q": "When solving problems, do you prefer:", "options": [("💡 Creative Solutions", "Creator"), ("🗣️ Group Discussion", "Influencer"), ("📊 Data Analysis", "Analyst"), ("⚡ Quick Action", "Catalyst")]},
    {"q": "Your ideal work environment is:", "options": [("🎨 Design Studio", "Creator"), ("📢 Boardroom", "Influencer"), ("💻 Tech Lab", "Analyst"), ("🏗️ On the Field", "Catalyst")]},
    {"q": "Friends describe you as:", "options": [("✨ Visionary", "Creator"), ("🎤 Leader", "Influencer"), ("🧠 Logical", "Analyst"), ("🛡️ Reliable", "Catalyst")]},
    {"q": "What drives you most?", "options": [("🚀 Innovation", "Creator"), ("🤝 Connection", "Influencer"), ("🔍 Truth", "Analyst"), ("✅ Results", "Catalyst")]},
    {"q": "In a movie production, you are:", "options": [("🎬 Director", "Creator"), ("🌟 Lead Star", "Influencer"), ("🎞️ Editor", "Analyst"), ("📋 Producer", "Catalyst")]}
]

KB = {
    "placement": "Placement support is a priority. Universities like Amity and Manipal host virtual job fairs with top recruiters.",
    "valid": "Yes. All listed universities are UGC-DEB Approved, making them valid for government jobs and higher education.",
    "fee": "We focus on ROI. Most options offer EMI plans starting at ₹3,000/month.",
    "exam": "Exams are fully online and proctored. You can schedule them on weekends."
}

HOOK_POOL = ["💰 Check Placements", "📜 Is this Valid?", "📊 Compare All", "💸 EMI Options", "🏫 Faculty Quality?", "📈 Salary Trends?"]

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
    return "I verify all universities for UGC approval. Would you like to check **Placements** or **Fees**?"

def render_matches(matches):
    # PREMIUM GRID LAYOUT
    cols = st.columns(3) # 3 Cards per row for premium feel
    for i, u in enumerate(matches):
        with cols[i % 3]:
            badges = "".join([f"<span class='uni-pill verified-pill'>✔ {b}</span>" for b in u['badges']])
            st.markdown(f"""
            <div class="uni-card">
                <div class="uni-header">
                    <div class="uni-logo">{u['logo']}</div>
                    <div>
                        <div class="uni-name">{u['name']}</div>
                        <div class="uni-badge-row">{badges}</div>
                    </div>
                </div>
                <div class="uni-stats">
                    <div>
                        <div class="stat-label">Total Fee</div>
                        <div class="stat-value">{u['fee']}</div>
                    </div>
                    <div>
                        <div class="stat-label">EMI</div>
                        <div class="stat-value">{u['emi']}</div>
                    </div>
                </div>
                <div class="uni-footer">
                    <a href="#" class="uni-btn">View Brochure</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_comparison(matches):
    # Clean Dataframe for Comparison
    data = [{"University": u["name"], "Fee": u["fee"], "EMI": u["emi"], "Approvals": ", ".join(u["badges"])} for u in matches]
    st.markdown("### 📊 Feature Comparison")
    st.table(pd.DataFrame(data))

# --- MAIN APP EXECUTION ---

navbar()

# 1. LANDING PAGE
if st.session_state.step == 0 and not st.session_state.messages:
    hero_section()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Free Assessment ➔", type="primary", use_container_width=True):
            st.session_state.step = 1
            add_bot_msg("Hello! I am **Eduveer**. I'm ready to analyze your profile. Let's start with a quick question.")
            st.rerun()

# 2. MAIN INTERFACE (CHAT + CONTENT)
with st.container():
    # Chat History
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "results_cards":
            render_matches(content)
        elif role == "comparison_chart":
            render_comparison(content)
        else:
            with st.chat_message(role):
                if role == "user":
                    name = st.session_state.user_info.get("name", "You")
                    st.markdown(f"**{name}**")
                else:
                    st.markdown(f"**Eduveer AI**")
                st.markdown(content)

    # 3. LOGIC CONTROLLER
    
    # Step 1: Assessment
    if st.session_state.step == 1:
        curr = QUESTIONS[st.session_state.q_index]
        last_bot = next((m["content"] for m in reversed(st.session_state.messages) if m["role"] == "assistant"), "")
        
        if curr["q"] not in last_bot:
            add_bot_msg(f"**Question {st.session_state.q_index + 1}/5:** {curr['q']}")
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
        
        # Logic: Filter by budget & course (restored from previous version)
        matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other" or "Other" in u["programs"])]
        if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2] # Fallback

        if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Top Picks for {primary} profile!**", "id": "res_msg"})
            st.session_state.messages.append({"role": "results_cards", "content": matches})
            st.rerun()

        # DYNAMIC HOOKS
        st.write("")
        cols = st.columns(4) # 4 Hooks per row for wide layout
        for i, hook in enumerate(st.session_state.current_hooks):
            if cols[i % 4].button(hook, key=f"hook_{len(st.session_state.messages)}_{i}", use_container_width=True):
                add_user_msg(hook)
                if hook == "📊 Compare All":
                     st.session_state.messages.append({"role": "comparison_chart", "content": matches})
                     st.session_state.messages.append({"role": "assistant", "content": "Comparison generated."})
                else:
                    response = get_bot_response(hook)
                    add_bot_msg(response)
                refresh_hooks()
                st.rerun()

    # CHAT INPUT (Bottom Fixed)
    if st.session_state.step > 0:
        user_query = st.chat_input("Ask Eduveer anything...")
        if user_query:
            add_user_msg(user_query)
            response = get_bot_response(user_query)
            add_bot_msg(response)
            refresh_hooks()
            st.rerun()
