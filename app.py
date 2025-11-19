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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF; /* Clean White Background */
        color: #1F2937; /* Dark Grey Text */
    }
    
    /* Main App Background */
    .stApp {
        background-color: #F9FAFB; /* Very light grey like the assessment page */
    }
    
    /* Headers (Matching your "Discover Your Genius Profile" text) */
    h1, h2, h3 {
        color: #111827; /* Almost Black */
        font-weight: 700;
        text-align: center;
    }
    
    /* --- BUTTONS (Matching "Start Assessment" style) --- */
    .stButton button {
        background-color: #0099FF; /* Vibrant Site Blue */
        color: white !important;
        border: none;
        padding: 12px 28px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 6px; /* Slightly squared corners like your site */
        transition: background-color 0.3s;
        box-shadow: none;
    }
    .stButton button:hover {
        background-color: #007ACC; /* Darker blue on hover */
        transform: translateY(-1px);
    }
    
    /* --- FORM & CARDS (Matching "Genius Profile" cards) --- */
    [data-testid="stForm"], [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB; /* Light border */
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* --- CHAT BUBBLES --- */
    
    /* Eduveer (AI) - Clean White Card */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 16px;
    }
    
    /* User (Student) - Light Blue Accent */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #F0F9FF; /* Very light blue background */
        border: 1px solid #BAE6FD;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Sidebar Booking Button (Orange/Red accent) */
    a[href*="forms"] {
        display: inline-block;
        width: 100%;
        background-color: #EF4444; /* Red/Orange for CTA */
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
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
    # Logo
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    
    st.markdown("### **Distoversity**") 
    st.caption("Empowering India 🇮🇳")
    
    st.info("📊 **Analytics:**\nData is captured via the Booking Form below.")

    # --- DATA CAPTURE LINK ---
    google_form_link = "https://forms.gle/YourFormLinkHere" 
    
    st.markdown(f"""
        <a href="{google_form_link}" target="_blank">
        📝 Fill Admission Form
        </a>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- DOWNLOAD CHAT BUTTON ---
    if "messages" in st.session_state and len(st.session_state.messages) > 2:
        chat_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages])
        st.download_button("📥 Download Chat History", chat_text, file_name="counseling_session.txt")

    if st.button("↻ Start New Session"):
        st.session_state.messages = []
        st.session_state.user_profile = None
        st.session_state.msg_count = 0
        st.rerun()

    st.caption("© 2025 Distoversity Pvt Ltd") 

# --- 6. Main Interface ---
st.title("Eduveer AI") 
st.markdown("<p style='text-align: center; color: #6B7280;'>Your Personal Career Guide by Distoversity</p>", unsafe_allow_html=True)

# --- SCENARIO A: PROFILE FORM ---
if st.session_state.user_profile is None:
    st.write("")
    st.markdown("<h3 style='font-size: 1.2rem;'>Let's get to know you</h3>", unsafe_allow_html=True)
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Current Status**")
            status = st.radio("Status", ["Student (12th/Grad)", "Working Professional"], label_visibility="collapsed")
        with col2:
            st.markdown("**Your Goal**")
            goal = st.radio("Goal", ["Regular College Degree", "Online/Distance Degree", "Upskilling/Certificate"], label_visibility="collapsed")
        
        st.write("")
        # Center the button using columns
        b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
        with b_col2:
            submitted = st.form_submit_button("Start Assessment 🚀")
        
        if submitted:
            st.session_state.user_profile = {"status": status, "goal": goal}
            st.rerun()

# --- SCENARIO B: CHAT INTERFACE ---
else:
    user_data = st.session_state.user_profile
    
    system_instruction = f"""
    You are **Eduveer**, a Career Mentor from **Distoversity**.
    USER PROFILE: Status: {user_data['status']}, Goal: {user_data['goal']}
    
    PHILOSOPHY: "Degree is a path, Skill is the destination."
    
    RULES:
    - Tone: Professional, encouraging, and polite.
    - Ask ONE question at a time.
    - If user is Working -> Pitch Online Degree.
    - If Student -> Pitch Regular or Affordable Online.
    - Keep answers SHORT.
    """

    if "messages" not in st.session_state or not st.session_state.messages:
        welcome_msg = f"Hello! 👋 Thanks for your details.\n\nSince you are interested in **{user_data['goal']}**, I can help you find the perfect match.\n\nFirst, tell me: **What subjects or real-world activities do you enjoy the most?**"
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
        st.markdown(f'<a href="{google_form_link}" target="_blank" style="text-decoration:none; color: #0099FF; font-weight:bold;">Click here to Book a Free Session &rarr;</a>', unsafe_allow_html=True)

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
