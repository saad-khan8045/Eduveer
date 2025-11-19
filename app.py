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
PRIMARY_BLUE = "#00AEEF"       # Distoversity Blue
DEEP_BLUE = "#003366"          # Trust/Corporate Blue
ACCENT_ORANGE = "#FF6B6B"      # "Apply Now" Action Color
BG_COLOR = "#F4F7F6"           # Clean, modern background
CARD_BG = "#FFFFFF"
TEXT_MAIN = "#2D3748"
SUCCESS_GREEN = "#38A169"

# --- CSS STYLING (TRUST & CLARITY) ---
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

    /* TRUST BAR */
    .trust-bar {{
        display: flex;
        justify-content: space-around;
        background: white;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        font-size: 0.8rem;
        color: #555;
        font-weight: 600;
    }}
    .trust-item span {{
        color: {SUCCESS_GREEN};
        font-size: 1.1rem;
        margin-right: 5px;
    }}

    /* HERO SECTION */
    .hero-box {{
        text-align: center;
        padding: 30px 20px;
        background: linear-gradient(135deg, {DEEP_BLUE} 0%, {PRIMARY_BLUE} 100%);
        color: white;
        border-radius: 0 0 20px 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0, 51, 102, 0.15);
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

    /* COLLEGE VIDYA STYLE CARDS */
    .cv-card {{
        background: white;
        border-radius: 12px;
        padding: 0;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #E2E8F0;
        overflow: hidden;
        transition: transform 0.2s;
    }}
    .cv-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }}
    .cv-header {{
        padding: 15px 20px;
        border-bottom: 1px solid #EDF2F7;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    .cv-body {{
        padding: 15px 20px;
    }}
    .cv-footer {{
        background: #F7FAFC;
        padding: 12px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-top: 1px solid #EDF2F7;
    }}
    
    /* DATA POINTS IN CARD */
    .data-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 15px 0;
        font-size: 0.85rem;
        color: #4A5568;
    }}
    .data-point strong {{
        display: block;
        color: {DEEP_BLUE};
        font-weight: 700;
    }}

    /* BUTTONS */
    .primary-btn {{
        background-color: {ACCENT_ORANGE};
        color: white;
        font-weight: 600;
        border: none;
        padding: 8px 20px;
        border-radius: 6px;
        cursor: pointer;
        text-decoration: none;
        font-size: 0.9rem;
    }}
    .stButton>button {{
        background-color: {ACCENT_ORANGE} !important;
        color: white !important;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(255, 107, 107, 0.2);
        width: 100%;
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
        text-transform: uppercase;
    }}
    </style>
""", unsafe_allow_html=True)

# --- DATA: UNIVERSITIES (Enriched with EMI & Duration) ---
UNIVERSITIES = [
    {
        "name": "Amity University Online",
        "programs": ["MBA", "MCA", "BBA"],
        "max_fee": 350000,
        "fees_display": "₹1.75 Lakhs",
        "emi": "Starts ₹4,999/mo",
        "duration": "24 Months",
        "badges": ["UGC-DEB", "NAAC A+", "WES"],
        "success_story": "Top choice for Corporate jobs.",
        "best_for": ["Analyst", "Influencer"],
        "logo": "🅰️"
    },
    {
        "name": "Manipal University Jaipur",
        "programs": ["MBA", "BCA", "B.Com"],
        "max_fee": 300000,
        "fees_display": "₹1.50 Lakhs",
        "emi": "Starts ₹3,500/mo",
        "duration": "24/36 Months",
        "badges": ["NAAC A+", "AICTE", "NIRF"],
        "success_story": "Best for Digital Careers.",
        "best_for": ["Creator", "Influencer"],
        "logo": "Ⓜ️"
    },
    {
        "name": "LPU Online",
        "programs": ["M.Sc CS", "MBA", "BA"],
        "max_fee": 180000,
        "fees_display": "₹98,000 Total",
        "emi": "Starts ₹2,500/mo",
        "duration": "24 Months",
        "badges": ["UGC Entitled", "AICTE"],
        "success_story": "Most Affordable & Valid.",
        "best_for": ["Catalyst", "Analyst"],
        "logo": "🏫"
    },
    {
        "name": "NMIMS Global",
        "programs": ["MBA (Ex)", "Diploma"],
        "max_fee": 400000,
        "fees_display": "₹4.0 Lakhs",
        "emi": "No Cost EMI",
        "duration": "24 Months",
        "badges": ["NAAC A+", "Top B-School"],
        "success_story": "For Management Leadership.",
        "best_for": ["Influencer", "Catalyst"],
        "logo": "📈"
    },
    {
        "name": "Chandigarh University",
        "programs": ["MCA", "MBA"],
        "max_fee": 150000,
        "fees_display": "₹1.10 Lakhs",
        "emi": "Starts ₹3,000/mo",
        "duration": "24 Months",
        "badges": ["NAAC A+", "QS Ranked"],
        "success_story": "Great for IT Placements.",
        "best_for": ["Creator", "Influencer"],
        "logo": "🏛️"
    },
    {
        "name": "DY Patil Online",
        "programs": ["BBA", "MBA"],
        "max_fee": 220000,
        "fees_display": "₹1.30 Lakhs",
        "emi": "Starts ₹4,000/mo",
        "duration": "36 Months",
        "badges": ["NAAC A++", "UGC"],
        "success_story": "Best for Healthcare/Ops.",
        "best_for": ["Catalyst", "Analyst"],
        "logo": "🏥"
    }
]

QUESTIONS = [
    {"q": "When you face a problem, you:", "options": [("Create a new solution", "Creator"), ("Ask the team", "Influencer"), ("Analyze the data", "Analyst"), ("Just fix it", "Catalyst")]},
    {"q": "Your dream workspace is:", "options": [("Artistic Studio", "Creator"), ("Busy Meeting Room", "Influencer"), ("Quiet Lab", "Analyst"), ("On the Field", "Catalyst")]},
    {"q": "Friends call you:", "options": [("The Visionary", "Creator"), ("The Leader", "Influencer"), ("The Brains", "Analyst"), ("The Rock", "Catalyst")]},
    {"q": "You are driven by:", "options": [("Innovation", "Creator"), ("People", "Influencer"), ("Logic", "Analyst"), ("Results", "Catalyst")]},
    {"q": "In a movie, you are:", "options": [("Director", "Creator"), ("Hero", "Influencer"), ("Editor", "Analyst"), ("Producer", "Catalyst")]}
]

# --- STATE ---
if "messages" not in st.session_state: st.session_state.messages = []
if "step" not in st.session_state: st.session_state.step = 0
if "q_index" not in st.session_state: st.session_state.q_index = 0
if "scores" not in st.session_state: st.session_state.scores = {"Creator": 0, "Influencer": 0, "Analyst": 0, "Catalyst": 0}
if "filter" not in st.session_state: st.session_state.filter = {"budget": 1000000, "course": "All"}

# --- FUNCTIONS ---
def add_bot_msg(text): st.session_state.messages.append({"role": "assistant", "content": text})
def add_user_msg(text): st.session_state.messages.append({"role": "user", "content": text})
def get_energy(): return max(st.session_state.scores, key=st.session_state.scores.get)

# --- UI HEADER ---
st.markdown(f"""
    <div class="hero-box">
        <h1 style="color:white; margin:0; font-size:2rem;">Distoversity</h1>
        <p style="opacity:0.9;">The Only <b>Unbiased</b> AI Career Architect</p>
    </div>
    <div class="trust-bar">
        <div class="trust-item"><span>✔</span>UGC-DEB Verified</div>
        <div class="trust-item"><span>✔</span>100% Unbiased</div>
        <div class="trust-item"><span>✔</span>Free Counseling</div>
    </div>
""", unsafe_allow_html=True)

# --- CHAT DISPLAY ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- LOGIC ---

# STEP 0: START
if st.session_state.step == 0:
    if not st.session_state.messages:
        add_bot_msg("👋 **Namaste! I am Eduveer.**\n\nI don't just give you a list of colleges. I understand **YOU** first.\n\nLet's analyze your **Career Energy** to find a university that respects your goals. Ready?")
        st.rerun()
    
    if st.button("🚀 Find My Perfect Match"):
        st.session_state.step = 1
        st.rerun()

# STEP 1: ASSESSMENT (Recognize Learner)
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

# STEP 2: MOTIVATION + TRUST + GATE
elif st.session_state.step == 2:
    primary = get_energy()
    if "gate_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        # HYPE UP / MOTIVATE before asking details
        hype_msg = (
            f"🌟 **Wow! You are a true {primary}.**\n\n"
            f"Students with this energy usually excel in high-growth roles. "
            f"I have found **3 UGC-Approved Universities** that are perfect for {primary}s like you.\n\n"
            "**I want to send your detailed Career Roadmap & University List to your WhatsApp.**"
        )
        st.session_state.messages.append({"role": "assistant", "content": hype_msg, "id": "gate_msg"})
        st.rerun()

    with st.form("lead_gen"):
        st.markdown("### 🔒 Secure Access to Your Report")
        st.caption("We respect your privacy. No spam, only career growth.")
        name = st.text_input("Full Name")
        phone = st.text_input("WhatsApp Number (for Report)")
        
        if st.form_submit_button("✅ Send My Roadmap"):
            if name and len(phone) >= 10:
                st.session_state.user_info = {"name": name}
                add_user_msg(f"Details: {name}, {phone}")
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("Please enter a valid Name and Phone Number.")

# STEP 3: THE CALM PROBE (Understand Constraints)
elif st.session_state.step == 3:
    if "probe_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        st.session_state.messages.append({"role": "assistant", "content": "One last thing to ensure I don't suggest something out of budget. **What are you looking for?**", "id": "probe_msg"})
        st.rerun()

    st.markdown("""<div style="background:white; padding:20px; border-radius:10px; border-left:5px solid #00AEEF;">
        <h4 style="margin:0;">🎯 Refine Your Search</h4>
    </div>""", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1: course = st.selectbox("Course Preference", ["MBA", "MCA", "BBA", "BCA", "M.Com", "MA", "Other"])
    with col2: budget = st.select_slider("Max Budget", ["1 Lakh", "2 Lakhs", "3 Lakhs", "4 Lakhs", "No Limit"])
    
    if st.button("🔍 Show Matched Universities"):
        b_map = {"1 Lakh": 100000, "2 Lakhs": 200000, "3 Lakhs": 300000, "4 Lakhs": 400000, "No Limit": 1000000}
        st.session_state.filter = {"budget": b_map[budget], "course": course}
        add_user_msg(f"Looking for {course} under {budget}.")
        st.session_state.step = 4
        st.rerun()

# STEP 4: RECOMMENDATIONS (College Vidya Style)
elif st.session_state.step == 4:
    primary = get_energy()
    filt = st.session_state.filter
    
    if "res_msg" not in [m.get("id", "") for m in st.session_state.messages]:
        st.session_state.messages.append({"role": "assistant", "content": f"🎉 **Here are the Top Matches for {st.session_state.user_info['name']}!**\n\nThese universities are **UGC-DEB Approved**, match your **{primary} Energy**, and fit your **{filt['course']}** goal.", "id": "res_msg"})
        st.rerun()

    # Filter
    matches = [u for u in UNIVERSITIES if (u["max_fee"] <= filt["budget"]) and (filt["course"] in u["programs"] or filt["course"] == "Other" or "Other" in u["programs"])]
    if not matches: matches = [u for u in UNIVERSITIES if primary in u["best_for"]][:2] # Fallback

    st.markdown("---")
    
    # RENDER CARDS
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
                <div class="data-grid">
                    <div class="data-point"><strong>Total Fee</strong>{u['fees_display']}</div>
                    <div class="data-point"><strong>EMI Options</strong>{u['emi']}</div>
                    <div class="data-point"><strong>Duration</strong>{u['duration']}</div>
                    <div class="data-point"><strong>Programs</strong>{", ".join(u['programs'][:3])}</div>
                </div>
                <div style="background:#F0FFF4; padding:8px; border-radius:5px; font-size:0.8rem; color:#2F855A;">
                    ✔ Placement Support Available
                </div>
            </div>
            <div class="cv-footer">
                <div style="font-size:0.8rem; color:#A0AEC0;">Matched for {primary}</div>
                <button class="primary-btn">View Brochure →</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.info("💡 Tip: These are government-approved universities. You can apply directly or ask me for a comparison.")

# --- FOOTER ---
st.markdown("<div style='text-align:center; color:#CBD5E0; margin-top:30px; font-size:0.8rem;'>© 2025 Distoversity | Unbiased Career Intelligence</div>", unsafe_allow_html=True)
