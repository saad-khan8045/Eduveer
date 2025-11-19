import streamlit as st
from groq import Groq

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Distoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. ATTRACTIVE UI Styling (Modern CSS) ---
st.markdown("""
    <style>
    /* Import Modern Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Background - Clean & Fresh */
    .stApp {
        background: linear-gradient(135deg, #F5F7FA 0%, #C3CFE2 100%);
    }

    /* Header Styling */
    h1 {
        color: #004aad;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* FORM CONTAINER - Glassmorphism Card Style */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }

    /* CHAT INPUT - Floating Style */
    [data-testid="stChatInput"] {
        border-radius: 30px;
        border: 2px solid #004aad;
        box-shadow: 0 5px 15px rgba(0, 74, 173, 0.15);
    }

    /* CHAT BUBBLES */
    
    /* Assistant (Eduveer) Bubble */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border-radius: 0px 20px 20px 20px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        border-left: 5px solid #004aad; /* Professional Blue Accent */
        margin-bottom: 15px;
    }
    
    /* User (Student) Bubble */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #E3F2FD; /* Soft Blue */
        border-radius: 20px 0px 20px 20px;
        border-left: none;
        border-right: 5px solid #0078ff;
    }

    /* BUTTONS - Gradient & Hover Effect */
    .stButton button {
        background: linear-gradient(90deg, #004aad 0%, #0078ff 100%);
        color: white !important;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 12px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 74, 173, 0.3);
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 74, 173, 0.4);
    }
    
    /* Sidebar Booking Button - Orange Gradient */
    a[href*="forms"] {
        display: inline-block;
        width: 100%;
        background: linear-gradient(45deg, #FF4B4B, #FF9068);
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: transform 0.2s;
    }
    a[href*="forms"]:hover {
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Initialize Brain (Groq) ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing. Please check Settings.")
    st.stop()

# --- 4. Session State Initialization ---
if "user_profile" not in st.session_state:
    st.session_state.user_profile = None

# --- 5. Sidebar (Reset & Booking) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    st.title("Distoversity") 
    st.markdown("### **Empowering India** 🇮🇳")
    
    st.info("✨ **We Guide You For:**\n\n🏫 Regular College\n💻 Online Degrees\n📈 Upskilling")
    
    st.divider()
    
    # --- BOOKING BUTTON ---
    st.markdown("### 📞 Talk to an Expert")
    st.write("Need a personal roadmap?")
    st.markdown('[📅 Book 1:1 Session](https://forms.gle/YourFormLinkHere)', unsafe_allow_html=True)
    
    st.divider()
    
    # Reset Button
    if st.button("↻ Start New Session"):
        st.session_state.messages = []
        st.session_state.user_profile = None
        st.rerun()

    st.caption("© 2025 Distoversity Pvt Ltd") 

# --- 6. Main Interface Logic ---
st.title("🎓 Eduveer AI") 

# --- SCENARIO A: PROFILE FORM (Shows first) ---
if st.session_state.user_profile is None:
    st.markdown("<h3 style='text-align: center; color: #555;'>Let's build your future together.</h3>", unsafe_allow_html=True)
    st.write("")
    
    # Using a Container for the card look
    with st.form("profile_form"):
        st.subheader("👤 Tell us about yourself")
        
        st.markdown("**1. Current Status:**")
        status = st.radio("Select one:", ["Student (12th Pass / Undergraduate)", "Working Professional"], label_visibility="collapsed")
        
        st.write("") # Spacer
        
        st.markdown("**2. What is your Goal?**")
        goal = st.radio("Select goal:", ["Regular College Degree", "Online / Distance Degree (Flexible)", "Career Guidance / Upskilling"], label_visibility="collapsed")
        
        st.write("") # Spacer
        
        # Centered Submit Button
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            submitted = st.form_submit_button("Start Counseling 🚀")
        
        if submitted:
            st.session_state.user_profile = {"status": status, "goal": goal}
            st.rerun()

# --- SCENARIO B: CHAT INTERFACE (Shows after form) ---
else:
    user_data = st.session_state.user_profile
    
    # System Instructions
    system_instruction = f"""
    You are **Eduveer**, a Professional Career Counselor from **Distoversity**.
    
    USER PROFILE:
    - Status: {user_data['status']}
    - Goal: {user_data['goal']}
    
    YOUR PHILOSOPHY:
    "Degree is a path, Skill is the destination. Choose what fits your budget and time."
    
    TONE:
    - Professional & Polished English.
    - Supportive & Wise.
    - Concise (2-3 sentences).
    
    RULE:
    - Ask ONLY ONE question at a time.
    
    START:
    Ask about their Interests to determine their Profile (Creator, Influencer, Catalyst, Analyst).
    """

    # Initialize Chat History
    if "messages" not in st.session_state or not st.session_state.messages:
        welcome_msg = f"Hello! 👋 Thank you for your details.\n\nAs you are interested in a **{user_data['goal']}**, I can guide you to the best options.\n\nTo begin, I need to understand your strengths.\n\n**Tell me, what kind of work or activities make you feel most energetic?**"
        
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

    # Response Cleaner
    def generate_chat_responses(chat_completion):
        for chunk in chat_completion:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    # User Input
    if prompt := st.chat_input("Type here..."):
        st.chat_message("user", avatar="🧑‍🎓").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

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
