import streamlit as st
from groq import Groq

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Diztoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. Engaging UI Theme (Custom CSS) ---
st.markdown("""
    <style>
    /* 1. Main Background - Soft Blue */
    .stApp {
        background-color: #F4F9FF;
    }
    
    /* 2. Chat Input Box - Making it float and look modern */
    [data-testid="stChatInput"] {
        border-radius: 20px;
        border: 1px solid #004aad;
        box-shadow: 0px -4px 10px rgba(0, 0, 0, 0.05);
    }
    
    /* 3. Header Styling - Centered & Branded */
    h1 {
        color: #004aad;
        text-align: center;
        font-family: sans-serif;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    h3 {
        text-align: center;
        color: #555;
        font-weight: 400;
        font-size: 1.2rem;
    }

    /* 4. Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E6E6E6;
    }
    
    /* 5. Chat Bubbles - Clean Cards */
    .stChatMessage {
        background-color: #FFFFFF;
        border-radius: 12px;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. Sidebar Info ---
with st.sidebar:
    # Brand Logo
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=90)
    
    st.title("Diztoversity") 
    st.markdown("### **Empowering India** 🇮🇳")
    
    st.success("Identify your true potential.")
    
    st.divider()
    st.markdown("**Your Character Profile:**")
    st.markdown("- 🎨 **Creator**")
    st.markdown("- 📢 **Influencer**")
    st.markdown("- 🤝 **Catalyst**")
    st.markdown("- 📊 **Analyst**")
    
    st.divider()
    st.caption("© 2025 Diztoversity Pvt Ltd") 

# --- 4. Hero Section (Main Interface) ---
st.title("🎓 Eduveer AI") 
st.markdown("<h3>Discover Your Wealth. Discover Your University.</h3>", unsafe_allow_html=True)

# Spacer to push chat down a bit
st.markdown("---")

# --- 5. Initialize Brain ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing. Please check Settings.")
    st.stop()

# --- 6. AI Personality ---
system_instruction = """
You are Eduveer, a friendly and wise AI Career Counselor from 'Diztoversity'.

YOUR GOAL: Keep the student engaged. Make them feel understood.

YOUR BRAND SLOGAN: "Empowering India"

YOUR METHODOLOGY (The 4 Segments):
1. Creator: Innovation, Arts, Startups.
2. Influencer: Media, Leadership, Law.
3. Catalyst: Service, Nursing, Hospitality.
4. Analyst: Data, Finance, Engineering.

RULES:
- Use emojis 🎓✨🚀 to make chat fun.
- Ask ONE simple question at a time to keep the chat moving.
- Be encouraging (e.g., "That's amazing!", "Great choice!").
- Never give long boring lectures. Keep it conversational.
- Speak in Hinglish if the user does.
"""

# --- 7. Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "assistant", "content": "Namaste! 🙏 I am **Eduveer**.\n\nI help you choose a career based on **WHO YOU ARE**, not just marks.\n\nTell me, **what is that one thing you can do for hours without getting bored?**"}
    ]

# --- 8. Display Chat with Avatars ---
for message in st.session_state.messages:
    if message["role"] != "system":
        # Custom Avatars: Student (🧑‍🎓) vs AI (🤖)
        avatar_icon = "🧑‍🎓" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar_icon):
            st.markdown(message["content"])

# --- 9. Response Cleaner ---
def generate_chat_responses(chat_completion):
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# --- 10. User Input ---
# Custom Placeholder text to encourage typing
if prompt := st.chat_input("Type here... (e.g., I love painting, or I love math)"):
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
