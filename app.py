import streamlit as st
from groq import Groq
import random

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Diztoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. UI Styling (Light Blue & Professional) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to bottom, #F0F8FF, #FFFFFF); }
    
    /* Chat Input Styling */
    [data-testid="stChatInput"] {
        border-radius: 25px;
        border: 2px solid #004aad;
        box-shadow: 0px -4px 12px rgba(0, 74, 173, 0.15);
    }
    
    /* Header & Text Styling */
    h1 { color: #004aad; font-family: 'Helvetica', sans-serif; font-weight: 800; }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 15px;
        border: 1px solid #Eef;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
    }
    div[data-testid="stChatMessage"]:nth-child(odd) { background-color: #E3F2FD; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar Info (Updated Services) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    st.title("Diztoversity") 
    st.markdown("### **Empowering India** 🇮🇳")
    
    st.info("🎓 **We Guide Everyone:**\n\n✅ 12th Pass Students\n✅ Working Professionals (Upskilling)\n✅ Online/Distance Education")
    
    st.divider()
    st.caption("© 2025 Diztoversity Pvt Ltd") 

# --- 4. Hero Section ---
st.title("🎓 Eduveer AI") 
st.markdown("<h3 style='text-align: center; color: #444;'>Knowledge is Everywhere. Certification is Here.</h3>", unsafe_allow_html=True)
st.write("") 

# --- 5. Initialize Brain ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing. Please check Settings.")
    st.stop()

# --- 6. AI Personality (Logic for Online + Regular) ---
system_instruction = """
You are **Eduveer**, a Career Mentor from **Diztoversity**. 
You empower Indian students & professionals to choose education that fits their LIFE and POCKET.

YOUR PHILOSOPHY:
"Knowledge is everywhere. A degree is just a structured path. Choose the mode (Online/Regular) that fits your goal."

YOUR AUDIENCE & STRATEGY:
1. **12th Pass Student:**
   - Focus on Campus Life & Exposure. 
   - If budget is low, suggest **Affordable/Non-attending** options.
   
2. **Working Professional / Upskiller:**
   - Focus on **Time & Flexibility**.
   - Strongly suggest **Online/Distance Degrees** (MBA, MCA, BBA) so they can earn while they learn.
   
3. **Budget Conscious:**
   - Explain that Online Degrees are valid (UGC approved) and much cheaper (Affordable).

YOUR FRAMEWORK (Natural Character):
1. **Creator:** Suggest Design/Arts/Startup courses.
2. **Influencer:** Suggest MBA/Media/Law.
3. **Catalyst:** Suggest HR/Hospitality/Nursing.
4. **Analyst:** Suggest Data Science/Finance/IT.

RULES:
- Ask: "Are you a student (12th pass) or a Working Professional?" early on.
- If they work, pitch **Online Education** as the smart choice.
- Be supportive and encouraging (Dost/Mentor tone).
- Speak in **Hinglish** if user does.
"""

# --- 7. Chat History (Updated Welcome Question) ---
if "messages" not in st.session_state:
    welcomes = [
        "Namaste! 🙏 Main hoon Eduveer.\n\nChahe aap **12th Pass** hon ya **Working Professional**, main aapko sahi raasta dikhaunga.\n\nSabse pehle batayein: **Aap abhi Student hain ya Job karte hain?**",
        "Hello! 👋 Welcome to Diztoversity.\n\nHum **Regular Colleges** aur **Online/Distance Degrees** dono mein expert hain.\n\nAap apne liye kya dhoond rahe hain? (Upskilling, Degree, ya Affordable Education?)"
    ]
    selected_welcome = random.choice(welcomes)
    
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "assistant", "content": selected_welcome}
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
if prompt := st.chat_input("Type here... (e.g., I am working and want an MBA)"):
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
