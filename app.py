import streamlit as st
from groq import Groq
import random

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Diztoversity AI",
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
        border-radius: 20px;
        font-weight: bold;
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

# --- 4. System Instructions (THE HOOK LOGIC) ---
system_instruction = """
You are **Eduveer**, a Career Mentor from **Diztoversity**.
Your goal is to guide students and professionals.

YOUR PHILOSOPHY:
"Degree is a path, Skill is the destination."

AUDIENCE RULES:
1. **Working Pros:** Suggest Online Degrees (MBA/MCA) for flexibility.
2. **Students:** Suggest Regular Colleges or Affordable Online options.

THE "HUMAN HOOK" (CRITICAL RULE):
If the user asks for:
- Exact admission cutoffs or exact fees (which might change).
- Deep emotional confusion or family problems.
- A personalized roadmap for the next 5 years.
- Or if you feel you cannot answer accurately...

THEN you must say:
"For a detailed personalized plan (and exact fee structure), I recommend speaking to our Human Expert."
AND tell them to click the **"Book 1:1 Session"** button in the sidebar.

TONE:
- Speak like a supportive Mentor (Dost).
- Use Hinglish (Hindi+English) naturally.
- Keep answers short and clear.
"""

# --- 5. Sidebar (Reset & Booking) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    st.title("Diztoversity") 
    st.markdown("### **Empowering India** 🇮🇳")
    
    st.success("🎓 **Modes We Guide:**\n\n✅ Regular College\n✅ Online Degrees (Job-ready)\n✅ Distance Education")
    
    st.divider()
    
    # --- NEW: BOOKING BUTTON ---
    st.markdown("### 📞 Need Expert Help?")
    st.info("Confused? Talk to a human counselor.")
    # Yahan apna Asli Link dalein (Google Form ya Calendly)
    st.markdown('[📅 Book 1:1 Session](https://forms.gle/YourFormLinkHere)', unsafe_allow_html=True)
    
    st.divider()
    
    # Reset Button
    if st.button("🗑️ Start New Chat", type="primary"):
        st.session_state.messages = [
            {"role": "system", "content": system_instruction},
            {"role": "assistant", "content": "Namaste! 🙏 Welcome to **Diztoversity**.\n\nMain hoon Eduveer. Main aapko **Regular** aur **Online Degrees** dono mein guide kar sakta hoon.\n\nSabse pehle batayein: **Aap abhi Student hain ya Job karte hain?**"}
        ]
        st.rerun()

    st.caption("© 2025 Diztoversity Pvt Ltd") 

# --- 6. Hero Section ---
st.title("🎓 Eduveer AI") 
st.markdown("<h3 style='text-align: center; color: #555;'>Sahi Career. Sahi Degree. Sahi Budget.</h3>", unsafe_allow_html=True)
st.write("") 

# --- 7. Chat History Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "assistant", "content": "Namaste! 🙏 Welcome to **Diztoversity**.\n\nMain hoon Eduveer. Main aapko **Regular** aur **Online Degrees** dono mein guide kar sakta hoon.\n\nSabse pehle batayein: **Aap abhi Student hain ya Job karte hain?**"}
    ]

# --- 8. Display Chat ---
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar_icon = "🧑‍🎓" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

# --- 9. Response Cleaner ---
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# --- 10. User Input ---
if prompt := st.chat_input("Type here... (e.g., I am confused about MBA fees)"):
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
