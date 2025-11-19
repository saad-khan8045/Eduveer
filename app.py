import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(page_title="Eduveer Career Chatbot", page_icon="🎓", layout="centered")

# --- CATCHY UI ---
st.markdown("""
<style>
body, .stApp { background: linear-gradient(90deg, #0077b6 0%, #00AEEF 80%, #CAF0F8 100%); }
h1, h2 { color: #0D1B2A; font-weight: 800; text-align: center; text-shadow: 0 2px 18px #00AEEF99; }
.stChatMessage { border-radius: 12px; margin-bottom:12px; }
.stChatMessage.user { background:#E0F2FE; }
.stChatMessage.assistant { background:#fff; border:2px solid #00AEEF; }
</style>
""", unsafe_allow_html=True)

st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=84)
st.title("🎓 Eduveer – Veteran Career Advisor")
st.markdown("<p style='text-align:center;color:#0077b6'>Ask me about online degree universities, admission, career options, and more!</p>", unsafe_allow_html=True)

# --- UNIVERSITIES DATA ---
universities = {
    "amity": "Amity Online: MBA, BCA, BBA. Flexible, UGC-Entitled. [Apply Now](https://www.amityonline.com/)",
    "jain": "Jain Online: MCA, BCom, MBA. Placement focus, recognized in India. [Apply Now](https://jainuniversity.ac.in/)",
    "manipal": "Manipal Online: Data Science, MBA. Best for analytics, career services. [Apply Now](https://www.onlinemanipal.com/)"
}

def eduveer_respond(user_text):
    user_text = user_text.lower()
    if "mba" in user_text:
        return f"In my experience, Amity, Jain, and Manipal all offer strong Online MBA programs. They are UGC recognized, fully online, and have great support. Want admission help for MBA?"
    if "bca" in user_text or "data science" in user_text:
        return f"For technology careers, Manipal and Amity offer BCA and Data Science programs online. They have strong industry links. Interested in placement support?"
    if "jain" in user_text:
        return universities["jain"]
    if "amity" in user_text:
        return universities["amity"]
    if "manipal" in user_text:
        return universities["manipal"]
    # General advice
    return "Eduveer recommends checking UGC-Entitled universities for online degrees: Amity, Jain, Manipal, and more. Ask me about any specific degree or university!"

# --- CHAT LOGIC ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello. I am Eduveer! Ask about online degree universities, career guidance, or admissions."}
    ]

for message in st.session_state.messages:
    avatar_icon = "🧑‍🎓" if message["role"] == "user" else "🎓"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.markdown(message["content"])

# User input field (always visible)
if prompt := st.chat_input("Type your query here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    reply = eduveer_respond(prompt)
    st.session_state.messages.append({"role": "assistant", "content": reply})

# After 2 messages, invite for session
if len([m for m in st.session_state.messages if m["role"]=="user"]) >= 2:
    st.info("💡 Want expert guidance? [Book a Free Career Session!](https://forms.gle/YourFormLinkHere)")

st.caption("© 2025 Distoversity Pvt Ltd")
