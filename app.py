import streamlit as st
from groq import Groq
import time

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Distoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. ATTRACTIVE UI Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #F5F7FA 0%, #C3CFE2 100%); }
    
    /* Header */
    h1 { color: #004aad; font-weight: 800; text-align: center; }
    
    /* Form & Chat Input */
    [data-testid="stForm"], [data-testid="stChatInput"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    /* Chat Bubbles */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border-radius: 0px 20px 20px 20px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #004aad;
        margin-bottom: 15px;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #E3F2FD;
        border-left: none;
        border-right: 5px solid #0078ff;
        border-radius: 20px 0px 20px 20px;
    }
    
    /* CTA Button in Chat */
    .cta-button {
        display: block;
        width: 100%;
        background: linear-gradient(45deg, #FF512F, #DD2476);
        color: white !important;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin: 10px 0;
        box-shadow: 0 5px 15px rgba(221, 36, 118, 0.3);
    }
    .cta-button:hover { opacity: 0.9; transform: scale(1.02); }
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
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    st.title("Distoversity") 
    st.markdown("### **Empowering India** 🇮🇳")
    
    st.info("📊 **For Data Analysis:**\nCurrently, data is NOT saved automatically. Please use the Booking Form to capture leads.")

    # --- DATA CAPTURE LINK ---
    # Yahan apna Google Form Link dalein
    google_form_link = "https://forms.gle/YourFormLinkHere" 
    
    st.markdown(f"""
        <a href="{google_form_link}" target="_blank" class="cta-button">
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
st.title("🎓 Eduveer AI") 

# --- SCENARIO A: PROFILE FORM ---
if st.session_state.user_profile is None:
    st.markdown("<h3 style='text-align: center; color: #555;'>Let's build your future together.</h3>", unsafe_allow_html=True)
    st.write("")
    
    with st.form("profile_form"):
        st.subheader("👤 Quick Profile Check")
        col1, col2 = st.columns(2)
        with col1:
            status = st.radio("Current Status:", ["Student (12th/Grad)", "Working Professional"])
        with col2:
            goal = st.radio("Your Goal:", ["Regular College Degree", "Online/Distance Degree", "Upskilling/Certificate"])
        
        submitted = st.form_submit_button("Start Counseling 🚀")
        
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
    - Professional & Supportive Tone.
    - Ask ONE question at a time.
    - If user is Working -> Pitch Online Degree.
    - If Student -> Pitch Regular or Affordable Online.
    - Keep answers SHORT.
    """

    if "messages" not in st.session_state or not st.session_state.messages:
        welcome_msg = f"Hello! 👋 Thanks for sharing details.\n\nSince you are interested in **{user_data['goal']}**, I can guide you perfectly.\n\nTo start, tell me: **What subjects or activities do you enjoy the most?**"
        st.session_state.messages = [
            {"role": "system", "content": system_instruction},
            {"role": "assistant", "content": welcome_msg}
        ]

    # Display Chat
    for message in st.session_state.messages:
        if message["role"] != "system":
            avatar_icon = "🧑‍🎓" if message["role"] == "user" else "🤖"
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

    # --- CONVERSION HOOK (After 4 messages) ---
    # Ye logic check karega ki chat lambi ho gayi hai, to "Book Session" ka button dikhayega
    if st.session_state.msg_count > 3 and st.session_state.msg_count < 5:
        st.info("💡 **Finding this helpful?** Get a personalized University Shortlist from our Experts.")
        st.markdown(f'<a href="{google_form_link}" target="_blank" class="cta-button">📅 Book Free 1:1 Session</a>', unsafe_allow_html=True)

    def generate_chat_responses(chat_completion):
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    if prompt := st.chat_input("Type here..."):
        st.chat_message("user", avatar="🧑‍🎓").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.msg_count += 1 # Count badhao

        with st.chat_message("assistant", avatar="🤖"):
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
