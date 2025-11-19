import streamlit as st
from groq import Groq

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Eduveer - Diztoversity",
    page_icon="🎓",
    layout="centered"
)

# --- 2. Sidebar Info (Updated with Diztoversity Segments) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=100)
    st.title("Diztoversity")
    st.markdown("""
    **Eduveer** is your AI Career Counselor.
    
    **The Diztoversity Framework:**
    First, we identify your natural character, then we map you to the right University Segment.
    
    - 🎨 **Diztoversity Creator:** Innovation & Ideas
    - 📢 **Diztoversity Influencer:** People & Leadership
    - 🤝 **Diztoversity Catalyst:** Service & Timing
    - 📊 **Diztoversity Analyst:** Systems & Data
    """)
    st.divider()
    st.caption("© 2025 Diztoversity")

# --- 3. Main Interface ---
st.title("🎓 Eduveer")
st.subheader("Education meets Wealth Creation.")
st.write("Most people choose universities based on specifications. We choose based on **WHO YOU ARE**.")

# --- 4. Initialize the Brain (Groq) ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ **Setup Required:** Please add your `GROQ_API_KEY` in the Streamlit Secrets settings.")
    st.stop()

# --- 5. Eduveer's Personality (Updated System Prompt) ---
system_instruction = """
You are Eduveer, the expert AI Career Counselor for 'Diztoversity'.

YOUR CORE PHILOSOPHY:
"Education is essential, but Wealth is most important. Both are interconnected. We do not select universities based on specifications alone; we first identify the student's Natural Character (Profile)."

YOUR METHODOLOGY (The 4 Diztoversity Segments):
1. **Diztoversity Creator**:
   - Character: Loves innovation, creating from scratch, artistic, dislikes details. High energy for new ideas.
   - University Segment: Suggest universities famous for Design, Arts, Startups, and R&D.
   
2. **Diztoversity Influencer**:
   - Character: Loves talking, connecting with people, leadership, stage presence. The star of the show.
   - University Segment: Suggest universities famous for Media, Management, Law, Mass Comm, and Politics.

3. **Diztoversity Catalyst**:
   - Character: Grounded, sensory, excellent sense of timing, loves serving/helping others, patient. Connects people and resources.
   - University Segment: Suggest universities famous for Hospitality, Nursing, Customer Relations, Supply Chain.

4. **Diztoversity Analyst**:
   - Character: Loves data, calculation, systems, working alone, detailed-oriented. Focuses on efficiency.
   - University Segment: Suggest universities famous for Engineering, Finance, Accounting, Data Science.

YOUR RULES:
- **Step 1:** Always start by asking questions to identify which of the 4 profiles the student belongs to.
- **Step 2:** Once the profile is clear, explicitly tell them: "You seem to be a [Diztoversity Profile Name]."
- **Step 3:** Only THEN suggest the specific "University Segment" that fits their nature.
- Be empathetic, wise, and focus on the connection between their nature and their future wealth/career.
- Keep responses concise and conversational.
- **POLICY:** Do NOT mention any external frameworks or third-party names. Use ONLY the Diztoversity terms above.
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

# --- 8. Handle User Input ---
if prompt := st.chat_input("e.g., I love talking to people, or I prefer solving math problems alone..."):
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"An error occurred: {e}")
