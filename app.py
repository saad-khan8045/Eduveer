import streamlit as st
from groq import Groq

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="My Career AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. Sidebar Info ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.title("My Brand Name") 
    st.markdown("""
    **Eduveer** is your AI Career Counselor.
    
    **Our Framework:**
    First, we identify your natural character, then we map you to the right University Segment.
    
    - 🎨 **Creator:** Innovation & Ideas
    - 📢 **Influencer:** People & Leadership
    - 🤝 **Catalyst:** Service & Timing
    - 📊 **Analyst:** Systems & Data
    """)
    st.divider()
    st.caption("© 2025 My Brand Name Pvt Ltd") 

# --- 3. Main Interface ---
st.title("🎓 Eduveer AI") 
st.subheader("Education meets Wealth Creation.")
st.write("Most people choose universities based on specifications. We choose based on **WHO YOU ARE**.")

# --- 4. Initialize the Brain (Groq) ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ **Setup Required:** Please add your `GROQ_API_KEY` in the Streamlit Secrets settings.")
    st.stop()

# --- 5. AI Personality ---
system_instruction = """
You are Eduveer, the expert AI Career Counselor.

YOUR CORE PHILOSOPHY:
"Education is essential, but Wealth is most important. Both are interconnected. We do not select universities based on specifications alone; we first identify the student's Natural Character (Profile)."

YOUR METHODOLOGY (The 4 Segments):
1. **Creator**: Loves innovation, creating from scratch, artistic, dislikes details. Suggest: Design, Arts, Startups.
2. **Influencer**: Loves talking, connecting with people, leadership. Suggest: Media, Management, Law.
3. **Catalyst**: Grounded, sensory, timing, serving others. Suggest: Hospitality, Nursing, Supply Chain.
4. **Analyst**: Loves data, calculation, systems, working alone. Suggest: Engineering, Finance, Accounting.

YOUR RULES:
- Start by asking questions to identify the profile.
- Be empathetic and wise.
- Keep responses concise.
- Do NOT mention external frameworks.
"""

# --- 6. Chat History Setup ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction},
        {"role": "assistant", "content": "Namaste! I am Eduveer. Before we look at universities, I need to understand your natural character.\n\n**Tell me, what kind of work makes you feel most alive and energetic?**"}
    ]

# --- 7. Display Chat ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- 8. Function to clean the AI Output ---
def generate_chat_responses(chat_completion):
    """Filters the computer code and returns only text."""
    for chunk in chat_completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# --- 9. Handle User Input ---
if prompt := st.chat_input("e.g., I love talking to people..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True,
            )
            # Use the cleaning function here
            response = st.write_stream(generate_chat_responses(stream))
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")
