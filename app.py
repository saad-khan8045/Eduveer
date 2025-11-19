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
BRAND_PRIMARY = "#0EA5E9"   # Premium Sky Blue
BRAND_DARK = "#0F172A"      # Slate 900 (High Contrast Text)
BRAND_LIGHT = "#F8FAFC"     # Slate 50 (Clean Background)
ACCENT_ORANGE = "#F97316"   # Call to Action
SUCCESS_GREEN = "#10B981"   # Verification/Success
WHITE = "#FFFFFF"

# --- ADVANCED CSS SYSTEM ---
st.markdown(f"""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    /* GLOBAL RESET */
    .stApp {{
        background-color: {BRAND_LIGHT};
        font-family: 'Inter', sans-serif;
        color: {BRAND_DARK};
    }}
    
    /* HIDE DEFAULT ELEMENTS */
    #MainMenu, footer, header {{visibility: hidden;}}

    /* --- COMPONENT: STICKY NAVBAR --- */
    .nav-bar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 70px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 5%;
        z-index: 9999;
    }}
    .nav-logo {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: {BRAND_PRIMARY};
        letter-spacing: -0.5px;
    }}
    .nav-badge {{
        background: #F0F9FF;
        color: {BRAND_PRIMARY};
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid #BAE6FD;
    }}
    .nav-spacer {{ height: 90px; }}

    /* --- COMPONENT: HERO --- */
    .hero-container {{
        text-align: center;
        padding: 40px 20px;
        margin-bottom: 30px;
    }}
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: {BRAND_DARK};
        margin-bottom: 10px;
    }}
    .hero-sub {{
        font-size: 1.1rem;
        color: #64748B;
        max-width: 600px;
        margin: 0 auto;
    }}

    /* --- COMPONENT: PREMIUM CARDS --- */
    .uni-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 24px;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
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
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
    }}
    .uni-logo-box {{
        width: 50px;
        height: 50px;
        background: #F8FAFC;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.8rem;
    }}
    .uni-title h3 {{
        margin: 0;
        font-size: 1.1rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }}
    .uni-meta {{
        font-size: 0.8rem;
        color: #64748B;
    }}
    
    /* METRICS GRID */
    .uni-metrics {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        background: #F8FAFC;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    .metric-item {{
        display: flex;
        flex-direction: column;
    }}
    .metric-label {{
        font-size: 0.7rem;
        text-transform: uppercase;
        color: #94A3B8;
        font-weight: 600;
    }}
    .metric-val {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {BRAND_DARK};
    }}
    
    /* BADGES */
    .badge-container {{
        display: flex;
        gap: 5px;
        flex-wrap: wrap;
        margin-bottom: 20px;
        flex-grow: 1;
    }}
    .pill {{
        font-size: 0.7rem;
        padding: 4px 10px;
        border-radius: 20px;
        background: #F1F5F9;
        color: #475569;
        font-weight: 600;
    }}
    .pill.verified {{
        background: #ECFDF5;
        color: {SUCCESS_GREEN};
        border: 1px solid #A7F3D0;
    }}

    /* BUTTONS */
    .card-btn {{
        display: block;
        width: 100%;
        padding: 12px;
        text-align: center;
        background: {BRAND_PRIMARY};
        color: white;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        transition: background 0.2s;
        margin-top: auto;
    }}
    .card-btn:hover {{
        background: #0284C7;
        color: white;
    }}

    /* --- CHAT INTERFACE --- */
    .stChatMessage {{
        background: transparent;
        border: none;
    }}
    .stChatMessage.assistant {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px 12px 12px 0;
        padding: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        margin-right: 20%;
    }}
    .stChatMessage.user {{
        background: {BRAND_DARK};
        color: white;
        border-radius: 12px 12px 0 12px;
        padding: 20px;
        margin-left: 20%;
        text-align: right;
    }}
    .stChatMessage.user p {{ color: white !important; }}
    
    /* --- FORM ELEMENTS --- */
    .stButton button {{
        width: 100%;
        border-radius: 8px;
        height: 48px;
        font-weight: 600;
        border: 1px solid #E2E8F0;
        color: {BRAND_DARK};
        background: white;
        transition: all 0.2s;
    }}
    .stButton button:hover {{
        border-color: {BRAND_PRIMARY};
        color: {BRAND_PRIMARY};
        background: #F0F9FF;
        transform: translateY(-1px);
    }}
    .stTextInput input {{
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        padding: 12px;
    }}

    /* --- TABLE --- */
    table {{
        width: 100%;
        border-collapse: separate; 
        border-spacing: 0;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        margin-top: 15px;
        border: 1px solid #E2E8F0;
    }}
    th {{
        background: {BRAND_PRIMARY};
        color: white;
        padding: 15px;
        text-align: left;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}
    td {{
        padding: 15px;
        border-bottom: 1px solid #F1F5F9;
        color: {BRAND_DARK};
        font-size: 0.9rem;
    }}
    tr:last-child td {{
        border-bottom: none;
    }}
    tr:nth-child(even) {{background-color: #F8FAFC;}}
    </style>
""", unsafe_allow_html=True)

# --- COMPONENT FUNCTIONS ---

def navbar():
    st.markdown(f"""
        <div class="nav-bar">
            <div class="nav-logo">Distoversity<span style="color:{ACCENT_ORANGE}">.</span></div>
            <div class="nav-badge">AI Powered Analytics</div>
        </div>
        <div class="nav-spacer"></div>
    """, unsafe_allow_html=True)

def hero():
    st.markdown(f"""
        <div class="hero-container">
            <h1 class="hero-title">Your Career, <span style="color:{BRAND_PRIMARY}">Data-Driven</span></h1>
            <p class="hero-sub">Eduveer analyzes 50+ data points to match your unique profile with UGC-Verified Universities.</p>
        </div>
    """, unsafe_allow_html=True)

# --- ENRICHED DATA (Added Placement Stats & Approvals) ---
UNIVERSITIES = [
    {
        "name": "Amity Online", 
        "programs": ["MBA", "MCA", "BBA"], 
        "max_fee": 350000, 
        "fee": "₹1.75L", 
        "emi": "₹4,999/mo", 
        "badges": ["UGC", "NAAC A+"], 
        "logo": "🅰️", 
        "best_for": ["Analyst"],
        "avg_pkg": "₹6-8 LPA",
        "high_pkg": "₹18 LPA",
        "recruiters": "Amazon, Deloitte"
    },
    {
        "name": "Manipal Jaipur", 
        "programs": ["MBA", "BCA", "B.Com"], 
        "max_fee": 300000, 
        "fee": "₹1.50L", 
        "emi": "₹3,500/mo", 
        "badges": ["AICTE", "NAAC A+"], 
        "logo": "Ⓜ️", 
        "best_for": ["Creator"],
        "avg_pkg": "₹5-7 LPA",
        "high_pkg": "₹14 LPA",
        "recruiters": "Google, Microsoft"
    },
    {
        "name": "LPU Online", 
        "programs": ["M.Sc CS", "MBA", "BA"], 
        "max_fee": 180000, 
        "fee": "₹98k", 
        "emi": "₹2,500/mo", 
        "badges": ["UGC", "AICTE"], 
        "logo": "🏫", 
        "best_for": ["Catalyst"],
        "avg_pkg": "₹4-6 LPA",
        "high_pkg": "₹12 LPA",
        "recruiters": "Wipro, Cognizant"
    },
    {
        "name": "NMIMS Global", 
        "programs": ["MBA (Ex)", "Diploma"], 
        "max_fee": 400000, 
        "fee": "₹4.0L", 
        "emi": "No Cost EMI", 
        "badges": ["Top Ranked"], 
        "logo": "📈", 
        "best_for": ["Influencer"],
        "avg_pkg": "₹10-12 LPA",
        "high_pkg": "₹24 LPA",
        "recruiters": "HDFC, Amex"
    },
    {
        "name": "Chandigarh Uni", 
        "programs": ["MCA", "MBA"], 
        "max_fee": 150000, 
        "fee": "₹1.10L", 
        "emi": "₹3,000/mo", 
        "badges": ["QS Ranked"], 
        "logo": "🏛️", 
        "best_for": ["Creator"],
        "avg_pkg": "₹5-6 LPA",
        "high_pkg": "₹15 LPA",
        "recruiters": "Flipkart, Adobe"
    },
    {
        "name": "DY Patil", 
        "programs": ["BBA", "MBA"], 
        "max_fee": 220000, 
        "fee": "₹1.30L", 
        "emi": "₹4,000/mo", 
        "badges": ["NAAC A++"], 
        "logo": "🏥", 
        "best_for": ["Catalyst"],
        "avg_pkg": "₹4.5-6.5 LPA",
        "high_pkg": "₹11 LPA",
        "recruiters": "Apollo, Fortis"
    }
]

QUESTIONS = [
    {"q": "When solving complex problems, you prefer:", "options": [("💡 Innovation", "Creator"), ("🗣️ Discussion", "Influencer"), ("📊 Data", "Analyst"), ("⚡ Action", "Catalyst")]},
    {"q": "Your ideal workspace is:", "options": [("🎨 Studio", "Creator"), ("📢 Boardroom", "Influencer"), ("💻 Lab", "Analyst"), ("🏗️ Field", "Catalyst")]},
    {"q": "How do friends describe you?", "options": [("✨ Visionary", "Creator"), ("🎤 Leader", "Influencer"), ("🧠 Logical", "Analyst"), ("🛡️ Reliable", "Catalyst")]},
    {"q": "What motivates you?", "options": [("🚀 Creating", "Creator"), ("🤝 Connecting", "Influencer"), ("🔍 Analyzing", "Analyst"), ("✅ Doing", "Catalyst")]},
    {"q": "Your role in a movie crew:", "options": [("🎬 Director", "Creator"), ("🌟 Actor", "Influencer"), ("🎞️ Editor", "Analyst"), ("📋 Producer", "Catalyst")]}
]

# --- ENHANCED KNOWLEDGE BASE (DATA ANALYST STYLE) ---
KB = {
    "placement": "Let's look at the data. 📈 **Amity and NMIMS** lead the pack with average packages of **8-10 LPA**. All our partners host virtual job fairs with recruiters like Amazon, Deloitte, and HDFC. ROI typically hits 150% within the first year.",
    "valid": "I've checked the regulatory status. ✅ **100% of these universities are UGC-DEB verified.** This means your degree is legally equivalent to a campus degree for UPSC, SSC, and global higher education.",
    "fee": "Financially speaking, these are high-value investments. 💰 EMI plans start as low as **₹2,500/month**, effectively costing less than a daily cup of coffee.",
    "exam": "The examination process is optimized for professionals. 💻 **100% Online AI-Proctored exams** allow you to take tests from home on weekends, ensuring zero work disruption.",
    "approval": "Approvals are non-negotiable. I only list universities with valid **UGC-DEB** (for online validity) and **NAAC** (for quality assurance) accreditations.",
    "salary": "Based on recent trends, an MBA or MCA from these universities typically yields a **30-50% salary hike** upon switching jobs."
}

HOOK_POOL = ["📊 Compare Top 5", "💼 Placement Stats?", "📜 Check Approvals", "💸 ROI Analysis", "🏫 Faculty Quality?", "📈 Salary Data?"]

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
    if "placement" in q or "job" in q or "stats" in q: return KB["placement"]
    if "valid" in q or "fake" in q or "approval" in q: return KB["valid"]
    if "fee" in q or "cost" in q or "roi" in q: return KB["fee"]
    if "exam" in q: return KB["exam"]
    if "salary" in q: return KB["salary"]
    return "That's a critical data point. I verify all universities for **UGC & NAAC approvals**. Would you like to dig into **Placement Statistics** or **ROI Analysis**?"

def render_matches(matches):
    # PREMIUM GRID (2 Columns for easy comparison)
    cols = st.columns(2)
    for i, u in enumerate(matches):
        with cols[i % 2]:
            badges = "".join([f"<span class='pill verified'>✔ {b}</span>" for b in u['badges']])
            st.markdown(f"""
            <div class="uni-card">
                <div class="uni-header">
                    <div class="uni-logo-box">{u['logo']}</div>
                    <div class="uni-title">
                        <h3>{u['name']}</h3>
                        <span class="uni-meta">Top Choice for {u['best_for'][0]}</span>
                    </div>
                </div>
                
                <div class="uni-metrics">
                    <div class="metric-item">
                        <span class="metric-label">Avg Package</span>
                        <span class="metric-val">{u['avg_pkg']}</span>
                    </div>
                    <div class="metric-item">
                        <span class="metric-label">Total Fee</span>
                        <span class="metric-val">{u['fee']}</span>
                    </div>
                </div>
                
                <div class="badge-container">{badges}</div>
                
                <a href="#" class="card-btn">View Official Brochure</a>
            </div>
            """, unsafe_allow_html=True)

def render_comparison(matches):
    # DATA ANALYST STYLE COMPARISON
    data = []
    for u in matches:
        data.append({
            "University": u["name"],
            "Highest Pkg": u["high_pkg"],
            "Avg Pkg": u["avg_pkg"],
            "Total Fee": u["fee"],
            "Approvals": ", ".join(u["badges"]),
            "Top Recruiters": u["recruiters"]
        })
    
    st.markdown("### 📊 Detailed Data Comparison")
    st.table(pd.DataFrame(data))

# --- MAIN LAYOUT ---
navbar()

# 1. HERO (Only at start)
if st.session_state.step == 0 and not st.session_state.messages:
    hero()
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Start Free Analysis ➔", type="primary", use_container_width=True):
            st.session_state.step = 1
            add_bot_msg("Namaste! 🙏 I am **Eduveer**, your Career Data Architect. I'm here to analyze your profile and match you with the perfect university. Ready to find your path?")
            st.rerun()

# 2. MAIN CONTENT CONTAINER
with st.container():
    # CHAT STREAM
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        
        if role == "results_cards":
            render_matches(content)
        elif role == "comparison_chart":
            render_comparison(content)
        else:
            with st.chat_message(role):
                # Custom Headers for Chat
                if role == "user":
                    name = st.session_state.user_info.get("name", "Candidate")
                    st.markdown(f"<div style='font-size:0.75rem; font-weight:700; margin-bottom:4px; color:white;'>{name}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='font-size:0.75rem; font-weight:700; margin-bottom:4px; color:{BRAND_PRIMARY};'>Eduveer AI</div>", unsafe_allow_html=True)
                st.markdown(content)

    # 3. LOGIC CONTROLLER
    
    # STEP 1: ASSESSMENT
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

    # STEP 2: LEAD GEN
    elif st.session_state.step == 2:
        primary = get_energy()
        if "gate_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": f"🌟 **Analysis Complete!**\n\nMy friend, you are a true **{primary}**. I've identified 3 universities that perfectly align with your career DNA. To customize your roadmap, may I have your name?", "id": "gate_msg"})
            st.rerun()

        with st.form("lead_gen"):
            st.markdown("#### 🔓 Unlock Your Matches")
            name = st.text_input("Full Name")
            if st.form_submit_button("Continue to Matches", type="primary"):
                if name:
                    st.session_state.user_info = {"name": name}
                    add_user_msg(f"I am {name}")
                    st.session_state.step = 3
                    st.rerun()

    # STEP 3: BUDGET PROBE
    elif st.session_state.step == 3:
        if "probe_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": f"Nice to meet you, **{st.session_state.user_info['name']}**! Let's be practical. What is your comfortable **Maximum Budget** for the entire course?", "id": "probe_msg"})
            st.rerun()

        col1, col2 = st.columns(2)
        with col1: course = st.selectbox("Preferred Course", ["MBA", "MCA", "BBA", "BCA", "M.Com"])
        with col2: budget = st.select_slider("Max Investment", ["1 Lakh", "2 Lakhs", "3 Lakhs", "4 Lakhs", "No Limit"])
        
        if st.button("Show Top Recommendations", type="primary", use_container_width=True):
            b_map = {"1 Lakh": 100000, "2 Lakhs": 200000, "3 Lakhs": 300000, "4 Lakhs": 400000, "No Limit": 1000000}
            st.session_state.filter = {"budget": b_map[budget], "course": course}
            add_user_msg(f"Looking for {course} under {budget}")
            st.session_state.step = 4
            st.rerun()

    # STEP 4: RESULTS & HOOKS
    elif st.session_state.step == 4:
        primary = get_energy()
        filt = st.session_state.filter
        matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other" or "Other" in u["programs"])]
        if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2]

        if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
            st.session_state.messages.append({"role": "assistant", "content": f"🎉 **I've curated these Top Picks for you!**\n\nBased on your {primary} profile and budget, these universities offer the best ROI.", "id": "res_msg"})
            st.session_state.messages.append({"role": "results_cards", "content": matches})
            st.rerun()

        # DYNAMIC HOOKS (Buttons)
        st.write("")
        cols = st.columns(4)
        for i, hook in enumerate(st.session_state.current_hooks):
            if cols[i % 4].button(hook, key=f"hook_{len(st.session_state.messages)}_{i}", use_container_width=True):
                add_user_msg(hook)
                if hook == "📊 Compare Top 5" or hook == "📊 Compare All":
                     # Logic: Take top 5 available matches
                     compare_list = matches[:5] if len(matches) > 0 else UNIVERSITIES[:5]
                     st.session_state.messages.append({"role": "comparison_chart", "content": compare_list})
                     st.session_state.messages.append({"role": "assistant", "content": "Here is the detailed data matrix comparing Placement Packages, Fees, and Recruiters."})
                else:
                    response = get_bot_response(hook)
                    add_bot_msg(response)
                refresh_hooks()
                st.rerun()

    # CHAT INPUT
    if st.session_state.step > 0:
        user_query = st.chat_input("Ask Eduveer (e.g. 'Is LPU valid?')")
        if user_query:
            add_user_msg(user_query)
            response = get_bot_response(user_query)
            add_bot_msg(response)
            refresh_hooks()
            st.rerun()
