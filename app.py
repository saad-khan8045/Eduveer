import streamlit as st
import pandas as pd
import time
import random
import streamlit.components.v1 as components
import os

# Try importing Groq
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Distoversity | Empowering India",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- API KEY (Secrets) ---
API_KEY = st.secrets.get("GROQ_API_KEY", "")

# --- BRAND COLORS ---
BRAND_PRIMARY = "#0EA5E9"   
BRAND_DARK = "#0F172A"      
BRAND_LIGHT = "#F8FAFC"     
ACCENT_ORANGE = "#F97316"   
SUCCESS_GREEN = "#10B981"   
GOLD_PREMIUM = "#D97706"    
WHITE = "#FFFFFF"
ALISON_GREEN = "#83C341"

# --- AVATARS ---
BOT_AVATAR = "https://api.dicebear.com/9.x/bottts-neutral/svg?seed=EduveerSmart"
USER_AVATAR = "https://api.dicebear.com/9.x/micah/svg?seed=Felix"

# --- CSS (MAINTAINED PREMIUM LOOK) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Poppins:wght@500;600;700&display=swap');

    .stApp {{ background-color: {BRAND_LIGHT}; font-family: 'Inter', sans-serif; color: {BRAND_DARK}; }}
    #MainMenu, footer, header {{visibility: hidden;}}
    .block-container {{ max_width: 750px; padding-top: 2rem; padding-bottom: 10rem; margin: 0 auto; }}

    /* NAVBAR */
    .nav-bar {{ position: fixed; top: 0; left: 0; width: 100%; height: 60px; background: rgba(255,255,255,0.95); backdrop-filter: blur(12px); border-bottom: 1px solid #E2E8F0; display: flex; align-items: center; justify-content: center; z-index: 9999; }}
    .nav-content {{ width: 100%; max_width: 750px; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; }}
    .nav-logo {{ font-family: 'Poppins', sans-serif; font-size: 1.2rem; font-weight: 700; color: {BRAND_PRIMARY}; }}
    .nav-badge {{ background: #F0F9FF; color: {BRAND_PRIMARY}; padding: 4px 12px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; border: 1px solid #BAE6FD; text-transform: uppercase; }}
    .nav-spacer {{ height: 80px; }}

    /* HERO */
    .hero-container {{ text-align: center; padding: 40px 20px; margin-bottom: 30px; animation: fadeIn 0.8s ease-out; }}
    .hero-title {{ font-family: 'Poppins', sans-serif; font-size: 2.2rem; font-weight: 800; color: {BRAND_DARK}; margin-bottom: 10px; line-height: 1.2; }}
    .hero-sub {{ font-size: 1rem; color: #64748B; line-height: 1.6; }}

    /* CHAT BUBBLES */
    .stChatMessage {{ background: transparent; border: none; margin-bottom: 15px; }}
    .stChatMessage.assistant {{ padding-right: 15%; }}
    .stChatMessage.assistant .stMarkdown {{ background: white; border: 1px solid #E2E8F0; border-radius: 4px 16px 16px 16px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }}
    .stChatMessage.user {{ padding-left: 15%; flex-direction: row-reverse; }}
    .stChatMessage.user .stMarkdown {{ background: #E0F2FE; border: 1px solid #BAE6FD; color: {BRAND_DARK}; border-radius: 16px 4px 16px 16px; padding: 16px 20px; text-align: left; }}
    .stChatMessage.user p {{ color: {BRAND_DARK} !important; }}

    /* CARDS */
    .uni-card {{ background: white; border: 1px solid #E2E8F0; border-radius: 16px; padding: 20px; margin-bottom: 15px; transition: all 0.3s; position: relative; overflow: hidden; }}
    .uni-card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 24px -6px rgba(0,0,0,0.08); border-color: {BRAND_PRIMARY}; }}
    .uni-header {{ display: flex; gap: 12px; align-items: center; margin-bottom: 15px; }}
    .uni-logo-box {{ font-size: 1.6rem; background: #F8FAFC; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; border-radius: 10px; }}
    .uni-title h3 {{ margin: 0; font-size: 1rem; font-weight: 700; font-family: 'Poppins'; }}
    .uni-metrics {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background: #F8FAFC; padding: 12px; border-radius: 10px; margin-bottom: 15px; }}
    .metric-label {{ font-size: 0.65rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; }}
    .metric-val {{ font-size: 0.85rem; font-weight: 700; color: {BRAND_DARK}; }}
    .card-btn {{ display: block; width: 100%; padding: 10px; text-align: center; background: {BRAND_PRIMARY}; color: white; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 0.85rem; margin-top: 5px; }}
    .pill {{ font-size: 0.65rem; padding: 4px 8px; border-radius: 12px; background: #F1F5F9; color: #475569; font-weight: 600; margin-right: 4px; display: inline-block; }}
    .pill.verified {{ background: #ECFDF5; color: {SUCCESS_GREEN}; border: 1px solid #A7F3D0; }}

    /* FEATURES */
    .alison-card {{ background: white; border-left: 4px solid {ALISON_GREEN}; padding: 16px; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.04); margin-top: 15px; }}
    .premium-card {{ background: linear-gradient(135deg, #FFFBEB 0%, #FFF7ED 100%); border: 1px solid #FEF3C7; padding: 20px; border-radius: 16px; margin-top: 20px; text-align: center; box-shadow: 0 4px 12px rgba(217, 119, 6, 0.1); }}
    .why-box {{ background: linear-gradient(145deg, #0F172A, #1E293B); color: white; padding: 25px; border-radius: 16px; margin-top: 25px; }}
    .why-grid {{ display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 20px; text-align: left; }}
    .why-item h4 {{ color: {ACCENT_ORANGE}; font-size: 0.9rem; margin-bottom: 5px; font-family: 'Poppins'; }}
    .why-item p {{ font-size: 0.85rem; opacity: 0.85; line-height: 1.6; margin: 0; }}

    /* INPUT & BUTTONS */
    .stButton button {{ width: 100%; border-radius: 12px; height: auto; padding: 12px; font-weight: 600; border: 1px solid #E2E8F0; color: {BRAND_DARK}; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: all 0.2s; }}
    .stButton button:hover {{ border-color: {BRAND_PRIMARY}; color: {BRAND_PRIMARY}; background: #F0F9FF; transform: translateY(-2px); }}
    .stTextInput input {{ border-radius: 25px; border: 1px solid #CBD5E1; padding: 12px 20px; }}
    
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 12px; overflow: hidden; font-size: 0.85rem; margin-top: 15px; }}
    th {{ background: {BRAND_PRIMARY}; color: white; padding: 12px; text-align: left; }}
    td {{ padding: 12px; border-bottom: 1px solid #F1F5F9; color: {BRAND_DARK}; }}
    
    @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    .stChatMessage {{ animation: fadeIn 0.3s ease-out; }}
    </style>
""", unsafe_allow_html=True)

# --- AUTO-SCROLL ---
components.html(
    """<script>window.scrollTo(0, document.body.scrollHeight);</script>""",
    height=0, width=0
)

# --- NAV & HERO ---
def navbar():
    st.markdown(f"""
        <div class="nav-bar">
            <div class="nav-content">
                <div class="nav-logo">Distoversity<span style="color:{ACCENT_ORANGE}">.</span></div>
                <div class="nav-badge">🇮🇳 Empowering India</div>
            </div>
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

# --- PROACTIVE KNOWLEDGE BASE ---
# This is the "Brain" that drives the conversation forward
KB = {
    "placement": [
        "That is the most important question! 💼 **Amity and NMIMS** are fantastic for networking, often seeing packages around **8-10 LPA**. \n\n**Insight:** Placements depend heavily on your skills. Shall we look at the **Salary Hikes** usually seen?",
        "Great question. Top recruiters include Amazon, Deloitte, and HDFC. \n\n**Pro Tip:** These universities have dedicated placement cells. Do you want to see the **ROI (Return on Investment)** analysis?"
    ],
    "valid": [
        "I'm glad you asked. ✅ **100% of these universities are UGC-DEB verified.** \n\nThis means your degree is valid for **Govt Jobs (UPSC)** and Study Abroad. Should I show you the **Exam Process** next?",
        "Absolutely valid. We don't deal with unapproved colleges. 🛡️ Your degree will be legally equivalent to a campus degree. \n\nDo you want to check the **Fee Structure** now?"
    ],
    "fee": [
        "I know budget is key. 💰 To be financially smart, look at the EMI options. Most start at just **₹2,500/month**. \n\n**Next Step:** Should we check if you are eligible for a **Scholarship**?",
        "These are high-value investments. The total fee is often recovered in the first 6 months of a job upgrade. \n\nWould you like to compare the **Fees of the Top 3** universities side-by-side?"
    ],
    "exam": [
        "Good news! You don't need to take leave from work. 💻 **Exams are 100% Online & AI-Proctored.** \n\nYou can take them from your bedroom on weekends. Want to know about the **Syllabus**?",
        "It's designed for working professionals. No centers, no travel. Just you and your laptop. \n\nSpeaking of learning, do you want to know about the **Faculty**?"
    ],
    "salary": [
        "Let's talk numbers. 📈 Generally, an MBA/MCA from these universities yields a **30-50% salary hike** when you switch jobs. \n\nDo you want to see the **Top Recruiters** list?",
        "A degree is a signal to employers. It often unlocks the 'Manager' tag and a pay bump. \n\n**Action:** Shall we lock a **Free Strategy Session** to plan your transition?"
    ],
    "default": [
        "That's a great point. I verify everything for **transparency**. \n\nTo help you decide, would you like to know about **Placements**, **Fees**, or **Approvals**?",
        "I understand. Making a career choice is big. \n\nLet's break it down. Should we look at the **Financials (Fees)** or the **Outcomes (Placements)** first?"
    ]
}

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

# --- CONTEXTUAL HOOK LOGIC ---
# Which buttons to show based on the LAST topic discussed
RELATED_HOOKS = {
    "placement": ["📈 Salary Hike?", "💸 Check Fees", "🏆 Top Recruiters", "📊 Compare All"],
    "fee": ["📉 ROI Analysis", "💳 Scholarship?", "💼 Placement Stats?", "📝 EMI Plans"],
    "valid": ["📝 Exam Process?", "💼 Govt Jobs?", "🌍 Study Abroad?", "📊 Compare"],
    "exam": ["📚 Syllabus?", "🏫 Faculty?", "📜 Degree Validity?", "💼 Job Support?"],
    "salary": ["💰 Fee Structure", "🏢 Top Companies", "📉 ROI", "💎 Premium Session"]
}

# --- STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "step" not in st.session_state: st.session_state.step = 0
if "q_index" not in st.session_state: st.session_state.q_index = 0
if "scores" not in st.session_state: st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "user_info" not in st.session_state: st.session_state.user_info = {}
if "filter" not in st.session_state: st.session_state.filter = {"budget": 1000000, "course": "All"}
if "current_hooks" not in st.session_state: st.session_state.current_hooks = ["💰 Check Fees", "💼 Placements"]
if "last_topic" not in st.session_state: st.session_state.last_topic = "default"

# --- FUNCTIONS ---
def update_hooks(topic):
    """Updates the buttons based on the conversation context"""
    if topic in RELATED_HOOKS:
        st.session_state.current_hooks = random.sample(RELATED_HOOKS[topic], 2)
    else:
        st.session_state.current_hooks = ["💰 Check Fees", "💼 Placements"]

def add_bot_msg(text): st.session_state.messages.append({"role": "assistant", "content": text})
def add_user_msg(text): st.session_state.messages.append({"role": "user", "content": text})
def get_energy(): return max(st.session_state.scores, key=st.session_state.scores.get)

def get_bot_response(user_query):
    q = user_query.lower()
    topic = "default"
    
    # Keyword matching to determine topic
    if "placement" in q or "job" in q or "recruit" in q: topic = "placement"
    elif "valid" in q or "fake" in q or "approval" in q or "govt" in q: topic = "valid"
    elif "fee" in q or "cost" in q or "emi" in q: topic = "fee"
    elif "exam" in q or "test" in q: topic = "exam"
    elif "salary" in q or "hike" in q: topic = "salary"
    
    st.session_state.last_topic = topic # Remember context
    
    # Pick a random variation from the KB to avoid repetition
    response_list = KB.get(topic, KB["default"])
    return random.choice(response_list)

def render_matches(matches):
    for i, u in enumerate(matches):
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
            "Recruiters": u["recruiters"]
        })
    st.markdown("### 📊 Detailed Data Matrix")
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

def render_why_distoversity():
    st.markdown(f"""
        <div class="why-box">
            <h3 style="margin-bottom:10px; font-family:'Poppins',sans-serif;">🚀 The Distoversity Advantage</h3>
            <div class="why-grid">
                <div class="why-item">
                    <h4>🎯 Precision Planning</h4>
                    <p>Stop guessing. We use verified data to map your career trajectory.</p>
                </div>
                <div class="why-item">
                    <h4>📊 Raw Transparency</h4>
                    <p>We expose everything—hidden fees, real placement stats, and approval validity.</p>
                </div>
                <div class="why-item">
                    <h4>🤝 Lifetime Tribe</h4>
                    <p>Join our exclusive network of professionals to grow forever.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_premium_upsell():
    st.markdown(f"""
        <div class="premium-card">
            <div class="premium-badge">💎 PREMIUM GUIDANCE</div>
            <h4 style="color:{BRAND_DARK}; margin-bottom:5px; font-family:'Poppins';">Need 100% Certainty?</h4>
            <p style="font-size:0.9rem; color:#666; margin-bottom:15px;">
                AI is great, but sometimes you need a human strategist. 
                Get a <b>1:1 Deep-Dive Session</b> with a Veteran Counsellor to audit your choice.
            </p>
            <button style="
                background-color: {GOLD_PREMIUM}; 
                color: white; 
                border: none; 
                padding: 10px 25px; 
                border-radius: 8px; 
                font-weight: 700; 
                cursor: pointer;
                width: 100%;
            ">Book Session @ ₹499/- Only</button>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN UI ---
navbar()

if st.session_state.step == 0 and not st.session_state.messages:
    hero()
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Start Free Analysis ➔", type="primary", use_container_width=True):
            st.session_state.step = 1
            add_bot_msg("Namaste! 🙏 I am **Eduveer**. I'm here to understand your goals and match you with the perfect university. Shall we start with your work style?")
            st.rerun()

# --- CHAT STREAM ---
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]
    
    if role == "results_cards": render_matches(content)
    elif role == "comparison_chart": render_comparison(content)
    elif role == "alison_promo": render_alison_promo(content)
    elif role == "why_us": render_why_distoversity()
    elif role == "premium_upsell": render_premium_upsell()
    else:
        avatar_img = BOT_AVATAR if role == "assistant" else USER_AVATAR
        with st.chat_message(role, avatar=avatar_img):
            st.markdown(content)

# --- LOGIC CONTROLLER ---

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

# STEP 4: RESULTS & CONVERSATION
elif st.session_state.step == 4:
    primary = get_energy()
    filt = st.session_state.filter
    matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other" or "Other" in u["programs"])]
    if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2]

    # Initial Result Load
    if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        strategy_msg = (
            f"🎯 **Strategic Analysis for {st.session_state.user_info['name']}**\n\n"
            f"Listen, I've analyzed the market for your profile as a **{primary}**. "
            f"Considering your budget of **{filt['budget']/100000} Lakhs** and the need for high ROI, "
            "I have isolated these specific options.\n\n"
            "These aren't just colleges; they are **investments with proven returns**. "
            "Here is the data:"
        )
        st.session_state.messages.append({"role": "assistant", "content": strategy_msg, "id": "res_msg"})
        st.session_state.messages.append({"role": "results_cards", "content": matches})
        st.session_state.messages.append({"role": "assistant", "content": "**My Advice:** Review the placement stats below. If you are ready, we can secure your seat."})
        st.session_state.messages.append({"role": "alison_promo", "content": primary})
        st.session_state.messages.append({"role": "why_us", "content": ""})
        st.session_state.messages.append({"role": "premium_upsell", "content": ""}) 
        st.rerun()

    # --- DYNAMIC & CONTEXTUAL HOOKS ---
    st.write("")
    cols = st.columns(2)
    for i, hook in enumerate(st.session_state.current_hooks):
        if cols[i % 2].button(hook, key=f"hook_{len(st.session_state.messages)}_{i}", use_container_width=True):
            add_user_msg(hook)
            
            if "Compare" in hook:
                 compare_list = matches[:5] if len(matches) > 0 else UNIVERSITIES[:5]
                 st.session_state.messages.append({"role": "comparison_chart", "content": compare_list})
                 st.session_state.messages.append({"role": "assistant", "content": "Here is the detailed breakdown. Notice the 'Recruiters' column—that is where your value lies."})
            else:
                response = get_bot_response(hook)
                add_bot_msg(response)
            
            # UPDATE HOOKS BASED ON NEW CONTEXT
            update_hooks(st.session_state.last_topic)
            st.rerun()

# CHAT INPUT
if st.session_state.step > 0:
    user_query = st.chat_input("Ask Eduveer (e.g. 'Is LPU valid?')")
    if user_query:
        add_user_msg(user_query)
        response = get_bot_response(user_query)
        add_bot_msg(response)
        # UPDATE HOOKS BASED ON NEW CONTEXT
        update_hooks(st.session_state.last_topic)
        st.rerun()
