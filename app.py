import streamlit as st
from groq import Groq
import time

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Distoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. WEBSITE-MATCHED UI Styling ---
st.markdown("""
    <style>
    /* Import 'Inter' font to match your website typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF; /* Clean White Background */
        color: #1F2937; /* Dark Grey Text for readability */
    }
    
    /* Main App Background */
    .stApp {
        background-color: #F3F8FC; /* Very light blue/grey tint from your dashboard background */
    }
    
    /* Headers - Matching the dark blue/black form headers */
    h1, h2, h3 {
        color: #0D1B2A; /* Deep Navy/Black from screenshots */
        font-weight: 700;
        text-align: center;
    }
    
    /* --- BUTTONS (Matching the "Start Assessment" / "Request Demo" buttons) --- */
    .stButton button {
        background-color: #00AEEF; /* The vibrant Cyan-Blue from your buttons */
        color: white !important;
        border: none;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 4px; /* Slightly sharper corners as seen in 'Start Assessment' */
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 174, 239, 0.2);
        width: 100%; /* Full width on mobile, responsive */
    }
    .stButton button:hover {
        background-color: #0095CC; /* Slightly darker on hover */
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 174, 239, 0.3);
    }
    
    /* --- FORM & CARDS (Matching "Genius Profile" cards) --- */
    [data-testid="stForm"], [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0; /* Subtle border */
        border-radius: 12px; /* Rounded corners like the profile cards */
        padding: 32px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03); /* Soft shadow */
        margin-bottom: 20px;
    }

    /* --- CHAT BUBBLES --- */
    
    /* Eduveer (AI) - Clean White Card Style */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    
    /* User (Student) - Light Blue Accent matching site theme */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #E0F2FE; /* Very light blue background */
        border: 1px solid #BAE6FD;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #F1F5F9;
    }
    
    /* Sidebar Booking Button */
    a[href*="forms"] {
        display: inline-block;
        width: 100%;
        background-color: #00AEEF; /* Matching Primary Brand Color */
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 10px;
        transition: background-color 0.3s;
    }
    a[href*="forms"]:hover {
        background-color: #0095CC;
    }

    /* Radio Button Selection Color */
    div[role="radiogroup"] label > div:first-child {
        background-color: #00AEEF !important;
    }
    
    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Initialize Brain ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing.")
    st.stop()

# --- 4. Session State ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None
if "msg_count" not in st.session_state:
    st.session_state.msg_count = 0

# --- 5. Sidebar (Data & Tools) ---
with st.sidebar:
    # Using your logo placeholder (Update link if you have hosted logo)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80)
    
    st.markdown("### **Distoversity**") 
    st.caption("Empowering India's Future Leaders 🇮🇳")
    
    st.info("📊 **Admissions Open**\nConnect with top universities matched to your profile.")

    # --- DATA CAPTURE LINK ---
    google_form_link = "https://forms.gle/YourFormLinkHere" 
    
    st.markdown(f"""
        <a href="{google_form_link}" target="_blank">
        📝 Start Application
        </a>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- DOWNLOAD CHAT BUTTON ---
    if "messages" in st.session_state and len(st.session_state.messages) > 2:
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("📥 Save Recommendations", chat_text, file_name="my_career_roadmap.txt")

    if st.button("↻ Start New Session"):
        st.session_state.messages = []
        st.session_state.user_profile = None
        st.session_state.msg_count = 0
        st.rerun()

    st.caption("© 2025 Distoversity Pvt Ltd") 

# --- 6. Main Interface ---
# Header matching your site style
st.title("Discover Your Genius Profile") 
st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.1rem;'>Unlock personalized university recommendations based on your unique strengths.</p>", unsafe_allow_html=True)

# --- SCENARIO A: PROFILE FORM (Aligned & Responsive) ---
if st.session_state.user_profile is None:
    st.write("")
    
    # Container for alignment
    with st.form("profile_form"):
        st.markdown("### Let's get started")
        st.write("")
        
        # Responsive Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Current Status**")
            st.caption("Select what describes you best")
            status = st.radio("Status", 
                            ["Student (12th/Grad)", "Working Professional"], 
                            label_visibility="collapsed")
        
        with col2:
            st.markdown("**Your Goal**")
            st.caption("What are you looking for?")
            goal = st.radio("Goal", 
                          ["Regular College Degree", "Online/Distance Degree", "Upskilling/Certificate"], 
                          label_visibility="collapsed")
        
        st.write("")
        st.write("")
        
        # Centered Button
        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            submitted = st.form_submit_button("Start Free Assessment ➔")
        
        if submitted:
            st.session_state.user_profile = {"status": status, "goal": goal}
            st.rerun()

# --- SCENARIO B: CHAT INTERFACE ---
else:
    user_data = st.session_state.user_profile
    
    system_instruction = f"""
    You are **Eduveer**, an AI Career Mentor from **Distoversity**.
    USER PROFILE: Status: {user_data['status']}, Goal: {user_data['goal']}
    
    PHILOSOPHY: "Degree is a path, Skill is the destination."
    
    RULES:
    - Tone: Professional yet encouraging (like a mentor).
    - Ask ONLY ONE question at a time.
    - If user is Working -> Pitch Online Degree.
    - If Student -> Pitch Regular or Affordable Online.
    - Keep answers SHORT (max 3 sentences).
    """

    if "messages" not in st.session_state or not st.session_state.messages:
        welcome_msg = f"Hello! 👋 Thanks for your details.\n\nSince you are interested in **{user_data['goal']}**, I can help you find the perfect match.\n\nFirst, tell me: **What subjects or activities do you enjoy the most?** (e.g., Solving problems, Creative arts, Leading teams)"
        st.session_state.messages = [
            {"role": "system", "content": system_instruction},
            {"role": "assistant", "content": welcome_msg}
        ]

    # Display Chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            # Using simpler avatars to match the clean UI
            avatar_icon = "🧑‍🎓" if message["role"] == "user" else "🎓"
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

    # --- CONVERSION HOOK ---
    if st.session_state.msg_count > 3 and st.session_state.msg_count < 5:
        st.info("💡 **Want a personalized University Shortlist?**")
        st.markdown(f'<a href="{google_form_link}" target="_blank" style="text-decoration:none; color: #00AEEF; font-weight:bold;">Click here to Book a Free Session &rarr;</a>', unsafe_allow_html=True)

    def generate_chat_responses(chat_completion):
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    if prompt := st.chat_input("Type your answer here..."):
        st.chat_message("user", avatar="🧑‍🎓").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.msg_count += 1

        with st.chat_message("assistant", avatar="🎓"):
            try:
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages,
                    stream=True,
                )
                response = st.write_stream(generate_chat_responses(stream))
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("⚠️ Connection Error. Please refresh.")
