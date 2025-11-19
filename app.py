import streamlit as st
from groq import Groq

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Distoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. UI Styling (Professional & Clean) ---
st.markdown("""
    <style>
    /* Background */
    .stApp { background: linear-gradient(to bottom, #F0F8FF, #FFFFFF); }
    
    /* Chat Input Styling */
    [data-testid="stChatInput"] {
        border-radius: 25px;
        border: 2px solid #004aad;
        box-shadow: 0px -4px 12px rgba(0, 74, 173, 0.15);
    }
    
    /* Header */
    h1 { color: #004aad; font-family: 'Helvetica', sans-serif; font-weight: 800; }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 15px;
        border: 1px solid #Eef;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
    }
    /* User Bubble Color */
    div[data-testid="stChatMessage"]:nth-child(odd) { background-color: #E3F2FD; border: none; }
    
    /* Button Styling */
    .stButton button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }

    /* Form Container Styling */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #E0E0E0;
    }
    
    /* Sidebar Booking Button Style */
    a[href*="forms"] {
        display: inline-block;
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin-top: 10px;
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
    
    st.success("🎓 **Guidance For:**\n\n✅ Regular College\n✅ Online Degrees\n✅ Upskilling")
    
    st.divider()
    
    # --- BOOKING BUTTON ---
    st.markdown("### 📞 Talk to an Expert")
    st.info("Need personalized advice?")
    st.markdown('[📅 Book 1:1 Session](https://forms.gle/YourFormLinkHere)', unsafe_allow_html=True)
    
    st.divider()
    
    # Reset Button
    if st.button("🗑️ Start New Session", type="primary"):
        st.session_state.messages = []
        st.session_state.user_profile = None
        st.rerun()

    st.caption("© 2025 Distoversity Pvt Ltd") 

# --- 6. Main Interface Logic ---
st.title("🎓 Eduveer AI") 

# --- SCENARIO A: PROFILE FORM (Shows first) ---
if st.session_state.user_profile is None:
    st.markdown("<h3 style='text-align: center; color: #555;'>Let's get to know you first</h3>", unsafe_allow_html=True)
    st.write("")
    
    with st.form("profile_form"):
        st.markdown("**1. Current Status:**")
        status = st.radio("Select one:", ["Student (12th Pass / Undergraduate)", "Working Professional"], label_visibility="collapsed")
        
        st.markdown("**2. What are you looking for?**")
        goal = st.radio("Select goal:", ["Regular College Degree", "Online / Distance Degree (Flexible)", "Career Guidance / Upskilling"], label_visibility="collapsed")
        
        submitted = st.form_submit_button("Start Counseling 🚀")
        
        if submitted:
            st.session_state.user_profile = {"status": status, "goal": goal}
            st.rerun()

# --- SCENARIO B: CHAT INTERFACE (Shows after form) ---
else:
    user_data = st.session_state.user_profile
    
    # System Instructions with PROFESSIONAL TONE & PACING
    system_instruction = f"""
    You are **Eduveer**, a Professional Career Counselor from **Distoversity**.
    
    USER PROFILE:
    - Status: {user_data['status']}
    - Goal: {user_data['goal']}
    
    YOUR PHILOSOPHY:
    "Degree is a path, Skill is the destination. Choose what fits your budget and time."
    
    TONE GUIDELINES:
    - **Professional & Polished:** Use standard English. You can use very light Hinglish (e.g., "Bilkul", "Sahi") only to build rapport, but keep it 90% Professional English.
    - **Supportive:** Be empathetic but authoritative like an expert consultant.
    - **Concise:** Keep answers short (2-3 sentences).
    
    PACING RULE (CRITICAL):
    - **Ask ONLY ONE question at a time.** Wait for the user to answer before asking the next.
    - Do NOT ask multiple questions in one message.
    
    YOUR METHODOLOGY (The 4 Profiles):
    - Creator -> Design/Startup/Arts
    - Influencer -> Management/Law/Media
    - Catalyst -> Hospitality/HR/Service
    - Analyst -> Tech/Finance/Data
    
    START:
    Since you already know their status ({user_data['status']}) and goal ({user_data['goal']}), start immediately by asking about their **Interests** to determine their Profile.
    """

    # Initialize Chat History if empty
    if "messages" not in st.session_state or not st.session_state.messages:
        # Custom Welcome based on Form Data
        welcome_msg = f"Hello! 👋 Thank you for sharing your details.\n\nSince you are looking for a **{user_data['goal']}**, I can definitely guide you.\n\nTo suggest the best program, I need to understand your nature.\n\n**Tell me, what kind of activities make you feel most energetic and productive?**"
        
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
