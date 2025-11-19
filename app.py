import streamlit as st
from groq import Groq
import random

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Diztoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. Engaging UI Theme (Soft & Welcoming) ---
st.markdown("""
    <style>
    /* Main Background - Soft Blue Gradient feel */
    .stApp {
        background: linear-gradient(to bottom, #F4F9FF, #FFFFFF);
    }
    
    /* Chat Input Box - Modern & Floating */
    [data-testid="stChatInput"] {
        border-radius: 25px;
        border: 2px solid #004aad;
        box-shadow: 0px -5px 15px rgba(0, 74, 173, 0.1);
        padding: 5px;
    }
    
    /* Header Styling */
    h1 {
        color: #004aad;
        text-align: center;
        font-family: 'Helvetica', sans-serif;
        font-weight: 800;
    }
    
    /* Chat Bubbles - Rounder & Friendlier */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 18px;
        padding: 15px;
        margin-bottom: 12px;
        border: 1px solid #Eef;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.04);
    }
    
    /* User Bubble Color (Light Blue) */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #E3F2FD;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar Info ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    
    st.title("Diztoversity") 
    st.markdown("### **Empowering India** 🇮🇳")
    
    st.info("💡 **Tip:** Talk to Eduveer like a friend. Be honest about your dreams!")
    
    st.divider()
    st.caption("© 2025 Diztoversity Pvt Ltd") 

# --- 4. Hero Section ---
st.title("🎓 Eduveer AI") 
st.markdown("<h3 style='text-align: center; color: #444;'>Discover the career you were BORN to do.</h3>", unsafe_allow_html=True)
st.write("") # Spacer

# --- 5. Initialize Brain ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing. Please check Settings.")
    st.stop()

# --- 6. AI Personality (The "Dost/Mentor" Upgrade) ---
system_instruction = """
You are **Eduveer**, a warm, wise, and encouraging Career Mentor from **Diztoversity**.
You are NOT a robot. You are a supportive guide (like a thoughtful elder brother or wise friend).

YOUR GOAL:
To Empower Indian students. Help them realize that their unique nature is their superpower.

YOUR TONE:
- **Warm & Welcoming:** Use phrases like "Don't worry," "I hear you," "That's a brilliant thought."
- **Hinglish Friendly:** Use natural Indian English (e.g., "Bilkul," "Great choice," "Samajh gaya").
- **Curious, Not Pushy:** Don't interrogate. Say things like, "Tell me more about that," or "What do you love doing in your free time?"
- **Empowering:** When they share something, validate it. "Wow, that shows you have a creative mind!"

YOUR FRAMEWORK (Keep this logic hidden, just use it to guide them):
1. **Creator:** Likes starting new things, ideas, art.
2. **Influencer:** Likes leading, speaking, people.
3. **Catalyst:** Likes helping, timing, connecting.
4. **Analyst:** Likes data, logic, details.

RULES:
1. Keep replies SHORT (2-3 sentences max).
2. Ask ONE open-ended question at a time.
3. Use emojis 🌟🎓💪 to keep the vibe positive.
4. If the user is confused, say: "Koi baat nahi (No problem). Let's figure it out together."
"""

# --- 7. Chat History (With a Warm Welcome) ---
if "messages" not in st.session_state:
    # Random welcome message to feel alive
    welcomes = [
        "Namaste! 🙏 Main hoon Eduveer. \n\nMarks aur ranks se pare, main aapke **Asli Talent** ko dhoondne mein madad karunga.\n\nBataiye, aaj kal kis cheez mein sabse zyada maza aa raha hai?",
        "Hello! 👋 Welcome to Diztoversity.\n\nMain yahan aapko judge karne nahi, **Support** karne aaya hoon.\n\nDil se bataiye, wo kaunsa kaam hai jo aap bina thake ghanton kar sakte hain?"
    ]
    selected_welcome = random.choice(welcomes)
    
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "assistant", "content": selected_welcome}
    ]

# --- 8. Display Chat with Avatars ---
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
if prompt := st.chat_input("Dil khol ke baat karein..."):
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
