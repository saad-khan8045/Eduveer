import streamlit as st
import pandas as pd
import time
import random
import streamlit.components.v1 as components

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Distoversity | Empowering India",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- BRAND IDENTITY ---
BRAND_PRIMARY = "#0EA5E9"   # Premium Sky Blue
BRAND_DARK = "#0F172A"      # Slate 900
BRAND_LIGHT = "#F8FAFC"     # Slate 50
ACCENT_ORANGE = "#F97316"   # Action Orange
SUCCESS_GREEN = "#10B981"   # Verification Green
WHITE = "#FFFFFF"
ALISON_GREEN = "#83C341"

# --- ADVANCED CSS SYSTEM ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    /* 1. GLOBAL LAYOUT & RESPONSIVENESS */
    .stApp {{
        background-color: {BRAND_LIGHT};
        font-family: 'Inter', sans-serif;
        color: {BRAND_DARK};
    }}
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {{visibility: hidden;}}
    
    /* Center the Main Content Container - Responsive Fix */
    /* On Desktop: Limit width and center */
    /* On Mobile: Full width */
    .block-container {{
        max_width: 800px;
        padding-top: 2rem;
        padding-bottom: 10rem; /* Space for chat input */
        margin: 0 auto;
    }}

    /* 2. STICKY NAVBAR */
    .nav-bar {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 60px;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid #E2E8F0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 20px;
        z-index: 9999;
    }}
    .nav-logo {{
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        color: {BRAND_PRIMARY};
        letter-spacing: -0.5px;
    }}
    .nav-badge {{
        background: #F0F9FF;
        color: {BRAND_PRIMARY};
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        border: 1px solid #BAE6FD;
        text-transform: uppercase;
    }}
    
    /* Spacer to push content below fixed nav */
    .nav-spacer {{ height: 70px; }}

    /* 3. HERO SECTION */
    .hero-container {{
        text-align: center;
        padding: 30px 10px;
        margin-bottom: 20px;
    }}
    .hero-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        color: {BRAND_DARK};
        margin-bottom: 10px;
        line-height: 1.2;
    }}
    .hero-sub {{
        font-size: 0.95rem;
        color: #64748B;
        line-height: 1.5;
    }}

    /* 4. CHAT INTERFACE - OPTIMIZED COLORS */
    .stChatMessage {{
        background: transparent;
        border: none;
        margin-bottom: 0px;
    }}
    
    /* EDUVEER (ASSISTANT) */
    .stChatMessage.assistant {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 0 16px 16px 16px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-right: 10%;
    }}
    
    /* STUDENT (USER) */
    .stChatMessage.user {{
        background: #E0F2FE; /* Soft Blue */
        border: 1px solid #BAE6FD;
        color: {BRAND_DARK};
        border-radius: 16px 0 16px 16px;
        padding: 15px;
        margin-left: 10%;
        text-align: left;
    }}
    .stChatMessage.user p {{ color: {BRAND_DARK} !important; }}

    /* 5. UNIVERSITY CARDS & WIDGETS */
    .uni-card {{
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }}
    .uni-header {{ display: flex; gap: 10px; align-items: center; margin-bottom: 10px; }}
    .uni-logo-box {{ font-size: 1.5rem; background: #F8FAFC; width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; border-radius: 8px; }}
    .uni-title h3 {{ margin: 0; font-size: 0.95rem; font-weight: 700; font-family: 'Poppins'; }}
    
    .uni-metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; background: #F8FAFC; padding: 10px; border-radius: 8px; margin-bottom: 10px; }}
    .metric-label {{ font-size: 0.6rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; }}
    .metric-val {{ font-size: 0.8rem; font-weight: 700; color: {BRAND_DARK}; }}
    
    .pill {{ font-size: 0.6rem; padding: 2px 6px; border-radius: 10px; background: #F1F5F9; color: #475569; font-weight: 600; margin-right: 4px; display: inline-block; }}
    .pill.verified {{ background: #ECFDF5; color: {SUCCESS_GREEN}; border: 1px solid #A7F3D0; }}
    
    .card-btn {{ display: block; width: 100%; padding: 8px; text-align: center; background: {BRAND_PRIMARY}; color: white; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.8rem; margin-top: 5px; }}
    
    /* ALISON CARD */
    .alison-card {{ background: white; border-left: 4px solid {ALISON_GREEN}; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.03); margin-top: 10px; }}

    /* WHY US BOX */
    .why-box {{ background: linear-gradient(145deg, #0F172A, #1E293B); color: white; padding: 20px; border-radius: 16px; margin-top: 20px; }}
    .why-grid {{ display: grid; grid-template-columns: 1fr; gap: 15px; margin-top: 15px; text-align: left; }} /* Stack on mobile */
    @media (min-width: 600px) {{ .why-grid {{ grid-template-columns: 1fr 1fr 1fr; }} }}
    
    .why-item h4 {{ color: {ACCENT_ORANGE}; font-size: 0.9rem; margin-bottom: 5px; font-family: 'Poppins'; }}
    .why-item p {{ font-size: 0.8rem; opacity: 0.85; line-height: 1.5; margin: 0; }}

    /* 6. INTERACTIVE ELEMENTS */
    .stButton button {{ 
        width: 100%; 
        border-radius: 8px; 
        height: auto; 
        padding: 10px; 
        font-weight: 600; 
        border: 1px solid #E2E8F0; 
        color: {BRAND_DARK}; 
        background: white; 
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }}
    .stButton button:hover {{ 
        border-color: {BRAND_PRIMARY}; 
        color: {BRAND_PRIMARY}; 
        background: #F0F9FF; 
    }}
    .stTextInput input {{ border-radius: 25px; border: 1px solid #CBD5E1; padding: 10px 20px; }}
    
    /* TABLE */
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; font-size: 0.8rem; }}
    th {{ background: {BRAND_PRIMARY}; color: white; padding: 10px; text-align: left; }}
    td {{ padding: 10px; border-bottom: 1px solid #F1F5F9; color: {BRAND_DARK}; }}
    </style>
""", unsafe_allow_html=True)

# --- AUTO-SCROLL JAVASCRIPT (Fixes the scroll issue) ---
# This script forces the browser to scroll to the bottom of the page on every reload.
components.html(
    """
    <script>
        window.scrollTo(0, document.body.scrollHeight);
    </script>
    """,
    height=0,
    width=0,
)

# --- COMPONENT FUNCTIONS ---

def navbar():
    st.markdown(f"""
        <div class="nav-bar">
            <div class="nav-logo">Distoversity<span style="color:{ACCENT_ORANGE}">.</span></div>
            <div class="nav-badge">🇮🇳 Empowering India</div>
        </div>
        <div class="nav-spacer"></div>
    """, unsafe_allow_html=True)

def hero():
    st.markdown(f"""
        <div class="hero-container">
            <h1 class="hero-title">Meet <span style="color:{BRAND_PRIMARY}">Eduveer</span><br>Your AI Career Architect</h1>
            <p class="hero-sub">I analyze your profile to find the perfect university match. No guessing, just data-backed career planning.</p>
        </div>
    """, unsafe_allow_html=True)

def render_why_distoversity():
    st.markdown(f"""
        <div class="why-box">
            <h3 style="margin-bottom:10px; font-family:'Poppins',sans-serif;">🚀 Why Distoversity?</h3>
            <div class="why-grid">
                <div class="why-item">
                    <h4>🎯 Planning, Not Guessing</h4>
                    <p>We give you verified data so you make a calculated career move, not a gamble.</p>
                </div>
                <div class="why-item">
                    <h4>📊 Data-Driven</h4>
                    <p>Decisions backed by placement records and approvals. We are your friends in this journey.</p>
                </div>
                <div class="why-item">
                    <h4>🤝 Community</h4>
                    <p>Join our exclusive network of learners to network and grow long after you graduate.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- DATA ---
UNIVERSITIES = [
    {"name": "Amity Online", "programs": ["MBA", "MCA", "BBA"], "max_fee": 350000, "fee": "₹1.75L", "emi": "₹4,999/mo", "badges": ["UGC", "NAAC A+"], "logo": "🅰️", "best_for": ["Analyst"], "avg_pkg": "₹6-8 LPA", "high_pkg": "₹18 LPA", "recruiters": "Amazon, Deloitte"},
    {"name": "Manipal Jaipur", "programs": ["MBA", "BCA", "B.Com"], "max_fee": 300000, "fee": "₹1.50L", "emi": "₹3,500/mo", "badges": ["AICTE", "NAAC A+"], "logo": "Ⓜ️", "best_for": ["Creator"], "avg_pkg": "₹5-7 LPA", "high_pkg": "₹14 LPA", "recruiters": "Google, Microsoft"},
    {"name": "LPU Online", "programs": ["M.Sc CS", "MBA", "BA"], "max_fee": 180000, "fee": "₹98k", "emi": "₹2,500/mo", "badges": ["UGC", "AICTE"], "logo": "🏫", "best_for": ["Catalyst"], "avg_pkg": "₹4-6 LPA", "high_pkg": "₹12 LPA", "recruiters": "Wipro, Cognizant"},
    {"name": "NMIMS Global", "programs": ["MBA (Ex)", "Diploma"], "max_fee": 400000, "fee": "₹4.0L", "emi": "No Cost EMI", "badges": ["Top Ranked"], "logo": "📈", "best_for": ["Influencer"], "avg_pkg": "₹10-12 LPA", "high_pkg": "₹24 LPA", "recruiters": "HDFC, Amex"},
    {"name": "Chandigarh Uni", "programs": ["MCA", "MBA"], "max_fee": 150000, "fee": "₹1.10L", "emi": "₹3,000/mo", "badges": ["QS Ranked"], "logo": "🏛️", "best_for": ["Creator"], "avg_pkg": "₹5-6 LPA", "high_pkg": "₹15 LPA", "recruiters": "Flipkart, Adobe"},
    {"name": "DY Patil", "programs": ["BBA", "MBA"], "max_fee": 220000, "fee": "₹1.30L", "emi": "₹4,000/mo", "badges": ["NAAC A++"], "logo": "🏥", "best_for": ["Catalyst"], "avg_pkg": "₹4.5-6.5 LPA", "high_pkg": "₹11 LPA", "recruiters": "Apollo, Fortis"}
]

ALISON_COURSES = {
    "Creator": {"title": "Diploma in Graphic Design", "desc": "Master visual storytelling.", "link": "https://alison.com/topic/graphic-design"},
    "Influencer": {"title": "Public Speaking Mastery", "desc": "Learn to command the room.", "link": "https://alison.com/topic/public-speaking"},
    "Analyst": {"title": "Data Analytics Essentials", "desc": "Excel, Python & SQL basics.", "link": "https://alison.com/topic/data-analytics"},
    "Catalyst": {"title": "Project Management (PMP)", "desc": "Agile & Scrum methods.", "link": "https://alison.com/topic/project-management"}
}

QUESTIONS = [
    {"q": "When solving complex problems, you prefer:", "options": [("💡 Innovation", "Creator"), ("🗣️ Discussion", "Influencer"), ("📊 Data", "Analyst"), ("⚡ Action", "Catalyst")]},
    {"q": "Your ideal workspace is:", "options": [("🎨 Studio", "Creator"), ("📢 Boardroom", "Influencer"), ("💻 Lab", "Analyst"), ("🏗️ Field", "Catalyst")]},
    {"q": "How do friends describe you?", "options": [("✨ Visionary", "Creator"), ("🎤 Leader", "Influencer"), ("🧠 Logical", "Analyst"), ("🛡️ Reliable", "Catalyst")]},
    {"q": "What motivates you?", "options": [("🚀 Creating", "Creator"), ("🤝 Connecting", "Influencer"), ("🔍 Analyzing", "Analyst"), ("✅ Doing", "Catalyst")]},
    {"q": "Your role in a movie crew:", "options": [("🎬 Director", "Creator"), ("🌟 Actor", "Influencer"), ("🎞️ Editor", "Analyst"), ("📋 Producer", "Catalyst")]}
]

# --- KNOWLEDGE BASE ---
KB = {
    "placement": "That is the most important question! Let's be honest—a degree is about the job. 💼 **Amity and NMIMS** are fantastic for networking, often seeing packages around **8-10 LPA**. But honestly, placements also depend on *your* skills. That's why our community helps you upskill while you study.",
    "valid": "I'm glad you asked. ✅ **100% of these universities are UGC-DEB verified.** I would never recommend a blacklisted uni. Your degree here is legally equivalent to a regular campus degree for Govt jobs (UPSC, Bank PO) and higher studies.",
    "fee": "I know fees can be a stress point. 💰 To be financially smart, look at the EMI options. Most of these universities allow you to start for just **₹2,500/month**. It's like the cost of a weekend outing, but it builds your future.",
    "exam": "Good news! You don't need to take leave from work. 💻 **Exams are 100% Online & AI-Proctored.** You can take them from your bedroom on weekends. It's designed for working professionals like us.",
    "approval": "Approvals are my #1 filter. I only list universities with valid **UGC-DEB** and **NAAC** accreditations. No fake degrees here, my friend.",
    "salary": "Let's talk numbers. 📈 Generally, an MBA/MCA from these universities yields a **30-50% salary hike** when you switch jobs. It's a strong signal to employers that you are ambitious and skilled."
}

HOOK_POOL = ["📊 Compare Top 5", "💼 Real Placement Stats?", "📜 Is this Valid for Govt Jobs?", "💸 Can I pay in EMI?", "🏫 Faculty Quality?", "📈 What's the Salary Hike?"]

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
    if "valid" in q or "fake" in q or "approval" in q or "govt" in q: return KB["valid"]
    if "fee" in q or "cost" in q or "roi" in q or "emi" in q: return KB["fee"]
    if "exam" in q: return KB["exam"]
    if "salary" in q or "hike" in q: return KB["salary"]
    return "That's a great question. I verify everything for **transparency**. Would you like to know about the **Fee Structure** or **Placement Records**?"

def render_matches(matches):
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
    data = []
    for u in matches:
        data.append({
            "University": u["name"],
            "Highest Pkg": u["high_pkg"],
            "Avg Pkg": u["avg_pkg"],
            "Total Fee": u["fee"],
            "Approvals": ", ".join(u["badges"])
        })
    st.markdown("### 📊 Detailed Comparison")
    st.table(pd.DataFrame(data))

def render_alison_promo(profile):
    course = ALISON_COURSES.get(profile, ALISON_COURSES["Analyst"])
    st.markdown(f"""
        <div class="alison-card">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="color:{BRAND_DARK}; font-weight:700; font-size:0.9rem;">💡 Skill Upgrade: {course['title']}</div>
                    <div style="color:#64748B; font-size:0.8rem;">{course['desc']} | Powered by <b>ALISON</b></div>
                </div>
                <a href="{course['link']}" target="_blank" style="background:#83C341; color:white; padding:6px 12px; border-radius:20px; text-decoration:none; font-weight:600; font-size:0.75rem;">Start Free</a>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN LAYOUT ---
navbar()

# 1. HERO (Only at start)
if st.session_state.step == 0 and not st.session_state.messages:
    hero()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Start Free Analysis ➔", type="primary", use_container_width=True):
            st.session_state.step = 1
            add_bot_msg("Namaste! 🙏 I am **Eduveer**. I'm here to understand your goals and match you with the perfect university. Shall we start with your work style?")
            st.rerun()

# 2. CHAT STREAM & LOGIC
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    
    if role == "results_cards":
        render_matches(content)
    elif role == "comparison_chart":
        render_comparison(content)
    elif role == "alison_promo":
        render_alison_promo(content)
    elif role == "why_us":
        render_why_distoversity()
    else:
        with st.chat_message(role):
            if role == "user":
                name = st.session_state.user_info.get("name", "Candidate").split()[0]
                st.markdown(f"<div style='font-size:0.7rem; font-weight:700; margin-bottom:4px; color:{BRAND_DARK};'>👤 {name}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='font-size:0.7rem; font-weight:700; margin-bottom:4px; color:{BRAND_PRIMARY};'>🤖 Eduveer</div>", unsafe_allow_html=True)
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
        st.session_state.messages.append({"role": "assistant", "content": f"🌟 **Brilliant! You are a {primary}.**\n\nI've found 3 universities that fit your DNA. To generate your custom roadmap, what should I call you?", "id": "gate_msg"})
        st.rerun()
    with st.form("lead_gen"):
        st.markdown("#### 🔓 Unlock Your Roadmap")
        name = st.text_input("Full Name")
        if st.form_submit_button("Continue", type="primary"):
            if name:
                st.session_state.user_info = {"name": name}
                add_user_msg(f"I am {name}")
                st.session_state.step = 3
                st.rerun()

# STEP 3: BUDGET PROBE
elif st.session_state.step == 3:
    if "probe_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        st.session_state.messages.append({"role": "assistant", "content": f"Nice to meet you, **{st.session_state.user_info['name']}**! 👋\n\nLet's be practical about this investment. What is your comfortable **Maximum Budget** for the entire course?", "id": "probe_msg"})
        st.rerun()
    col1, col2 = st.columns(2)
    with col1: course = st.selectbox("Preferred Course", ["MBA", "MCA", "BBA", "BCA", "M.Com"])
    with col2: budget = st.select_slider("Max Investment", ["1 Lakh", "2 Lakhs", "3 Lakhs", "4 Lakhs", "No Limit"])
    if st.button("Show My Strategic Plan", type="primary", use_container_width=True):
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
        st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Strategy Ready!**\n\nMy friend, I've curated these universities for you. They align with your {primary} strengths and budget. This isn't just a degree; it's your career launchpad.", "id": "res_msg"})
        st.session_state.messages.append({"role": "results_cards", "content": matches})
        st.session_state.messages.append({"role": "assistant", "content": "To help you start immediately, I also found this **Free Certification**:"})
        st.session_state.messages.append({"role": "alison_promo", "content": primary})
        st.session_state.messages.append({"role": "why_us", "content": ""})
        st.rerun()

    st.write("")
    cols = st.columns(2)
    for i, hook in enumerate(st.session_state.current_hooks):
        if cols[i % 2].button(hook, key=f"hook_{len(st.session_state.messages)}_{i}", use_container_width=True):
            add_user_msg(hook)
            if hook == "📊 Compare Top 5" or hook == "📊 Compare All":
                 compare_list = matches[:5] if len(matches) > 0 else UNIVERSITIES[:5]
                 st.session_state.messages.append({"role": "comparison_chart", "content": compare_list})
                 st.session_state.messages.append({"role": "assistant", "content": "Here is the transparency matrix. We believe in full disclosure."})
            else:
                response = get_bot_response(hook)
                add_bot_msg(response)
            refresh_hooks()
            st.rerun()

# CHAT INPUT (Bottom Fixed)
if st.session_state.step > 0:
    user_query = st.chat_input("Ask Eduveer (e.g. 'Is LPU valid?')")
    if user_query:
        add_user_msg(user_query)
        response = get_bot_response(user_query)
        add_bot_msg(response)
        refresh_hooks()
        st.rerun()
