import streamlit as st
from groq import Groq
import time
import json
import streamlit.components.v1 as components

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Distoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. FLASHING TAB TITLE SCRIPT ---
flashing_script = """
<script>
    var titles = ["Distoversity Guide", "Your Career Mentor", "Distoversity AI"];
    var i = 0;
    setInterval(function() {
        document.title = titles[i % titles.length];
        i++;
    }, 2000);
</script>
"""
components.html(flashing_script, height=0)

# --- 3. WEBSITE-MATCHED UI Styling ---
st.markdown("""
    <style>
    /* Import 'Inter' font to match your website typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF; /* Clean White Background */
        color: #1F2937; /* Dark Grey Text for readability */
    }
    
    /* Main App Background */
    .stApp {
        background-color: #F9FAFB; /* Very light grey/blue tint from your dashboard background */
    }
    
    /* Headers - Matching the dark blue/black form headers */
    h1, h2, h3 {
        color: #0D1B2A; /* Deep Navy/Black from screenshots */
        font-weight: 700;
        text-align: center;
    }
    
    /* --- BUTTONS (Matching the "Start Assessment" / "Request Demo" buttons) --- */
    .stButton button {
        background-color: #00AEEF; /* The vibrant Cyan-Blue from your buttons */
        color: white !important;
        border: none;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 4px; /* Slightly sharper corners as seen in 'Start Assessment' */
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 174, 239, 0.2);
        width: 100%; /* Full width on mobile, responsive */
    }
    .stButton button:hover {
        background-color: #0095CC; /* Slightly darker on hover */
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 174, 239, 0.3);
    }
    
    /* --- FORM & CARDS (Matching "Genius Profile" cards) --- */
    [data-testid="stForm"], [data-testid="stChatInput"], .report-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0; /* Subtle border */
        border-radius: 8px; /* Rounded corners like the profile cards */
        padding: 32px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); /* Soft shadow */
        margin-bottom: 20px;
    }

    /* --- CHAT BUBBLES --- */
    
    /* Eduveer (AI) - Clean White Card Style */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        margin-bottom: 16px;
    }
    
    /* User (Student) - Light Blue Accent matching site theme */
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #F0F9FF; /* Very light blue background #F0F9FF */
        border: 1px solid #BAE6FD;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Sidebar Booking Button */
    a[href*="forms"] {
        display: inline-block;
        width: 100%;
        background-color: #00AEEF; /* Matching Primary Brand Color */
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 10px;
        transition: background-color 0.3s;
    }
    a[href*="forms"]:hover {
        background-color: #0095CC;
    }

    /* Radio Button Selection Color */
    div[role="radiogroup"] label > div:first-child {
        background-color: #00AEEF !important;
    }
    
    /* Hide Streamlit branding for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. Initialize Brain ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing.")
    st.stop()

# --- 5. Session State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []
if "contact_info" not in st.session_state:
    st.session_state.contact_info = {}
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

# --- 6. Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80)
    st.markdown("### **Distoversity**") 
    st.caption("Empowering India's Future Leaders 🇮🇳")
    
    if st.session_state.step > 1:
        progress = (len(st.session_state.quiz_answers) / 5) if st.session_state.step == 2 else 1.0
        st.progress(progress)
        st.caption(f"Career Analysis Progress")

    st.divider()
    if st.button("↻ Restart"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.caption("© 2025 Distoversity Pvt Ltd") 

# --- 7. Main Logic ---

st.title("Discover Your Genius Profile") 

# --- STEP 1: INITIAL PROFILE FORM ---
if st.session_state.step == 1:
    st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.1rem;'>Unlock personalized university recommendations based on your unique strengths.</p>", unsafe_allow_html=True)
    st.write("")
    
    with st.form("profile_form"):
        st.markdown("### Let's get started")
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Current Status**")
            status = st.radio("Status", ["Student (12th/Grad)", "Working Professional"], label_visibility="collapsed")
        with col2:
            st.markdown("**Your Goal**")
            goal = st.radio("Goal", ["Regular College Degree", "Online/Distance Degree", "Upskilling/Certificate"], label_visibility="collapsed")
        
        st.write("")
        submitted = st.form_submit_button("Begin Assessment ➔")
        
        if submitted:
            st.session_state.user_profile = {"status": status, "goal": goal}
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: THE GUIDED ASSESSMENT (Chat Interface) ---
elif st.session_state.step == 2:
    
    # Questions designed to feel like a conversation
    questions = [
        "**Let's start.** When you think about your ideal work day, what are you doing? (Brainstorming new ideas, Leading a team discussion, Organizing a complex plan, or Analyzing data alone?)",
        "**Interesting.** Now, in a group project, what role do you naturally fall into? (The 'Idea Person', The 'Speaker/Presenter', The 'Support/Organizer', or The 'Fact-Checker'?)",
        "**Got it.** Everyone has tasks they dislike. What drains your energy the most? (Repetitive details, Working in isolation, Chaos/Uncertainty, or Emotional conflicts?)",
        "**That makes sense.** If you could have one superpower to help you succeed, what would it be? (Limitless Creativity, Magnetic Persuasion, Perfect Timing, or Instant Calculation?)",
        "**Final question.** How do you prefer to make big decisions? (Trusting your gut/vision, talking it out with others, waiting for the right moment, or analyzing the data first?)"
    ]
    
    current_q_index = len(st.session_state.quiz_answers)
    
    if current_q_index < 5:
        # Dynamic Header
        st.markdown(f"### Insight {current_q_index + 1} of 5")
        
        # Use chat message to ask
        with st.chat_message("assistant", avatar="🎓"):
            st.write(questions[current_q_index])
        
        # Chat input for the answer
        if answer := st.chat_input("Type your answer here..."):
            st.session_state.quiz_answers.append(answer)
            st.rerun()
            
        # Display previous conversation for context
        for i, ans in enumerate(st.session_state.quiz_answers):
            with st.chat_message("assistant", avatar="🎓"):
                st.markdown(questions[i])
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.markdown(ans)
                
    else:
        st.session_state.step = 3
        st.rerun()

# --- STEP 3: CONTACT INFO FORM ---
elif st.session_state.step == 3:
    st.markdown("### Analysis Complete! 🎉")
    st.markdown("I have analyzed your responses. To provide you with a **Personalized Guidance Report** and a list of universities that match your energy, please share your details.")
    
    with st.form("contact_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Mobile Number")
        
        st.info("🔒 Your data is secure. We use this only to send your career report.")
        
        submit_contact = st.form_submit_button("View My Career Report ➔")
        
        if submit_contact and name and email and phone:
            st.session_state.contact_info = {"name": name, "email": email, "phone": phone}
            st.session_state.step = 4
            st.rerun()
        elif submit_contact:
            st.error("Please fill in all fields to unlock your report.")

# --- STEP 4: GUIDANCE REPORT GENERATION ---
elif st.session_state.step == 4:
    if not st.session_state.final_report:
        with st.spinner("Synthesizing your profile... Matching universities..."):
            
            user_data_str = f"""
            User Status: {st.session_state.user_profile['status']}
            User Goal: {st.session_state.user_profile['goal']}
            
            Quiz Answers:
            1. {st.session_state.quiz_answers[0]}
            2. {st.session_state.quiz_answers[1]}
            3. {st.session_state.quiz_answers[2]}
            4. {st.session_state.quiz_answers[3]}
            5. {st.session_state.quiz_answers[4]}
            """
            
            prompt = f"""
            Act as a Senior Career Strategist at Distoversity.
            Analyze the user based on the 4 Energies: Creator, Influencer, Catalyst, Analyst.

            USER DATA:
            {user_data_str}

            TASK:
            1. Calculate Profile % (Estimate based on answers).
            2. Identify DOMINANT profile.
            3. Provide **GUIDANCE**, not just a label. Explain *HOW* they should study and *WHAT* kind of career environment suits them.
            4. Suggest 3 specific paths/courses.

            OUTPUT FORMAT (Markdown):
            # 🎓 Career Guidance Report for [Name]
            
            ## ⚡ Your Energy Profile
            - **Creator:** [X]%
            - **Influencer:** [X]%
            - **Catalyst:** [X]%
            - **Analyst:** [X]%
            
            ## 🏆 Your Core Strength: [Profile Name]
            
            ### 🧭 Expert Guidance
            [Write 3-4 sentences explaining their working style. Focus on their STRENGTHS. Example: "You thrive in environments where... You should avoid roles that are too rigid..."]
            
            ### 🚀 Recommended Career Paths
            1. **[Path 1]**: [Brief reason why]
            2. **[Path 2]**: [Brief reason why]
            3. **[Path 3]**: [Brief reason why]
            
            ---
            *Guidance by Distoversity AI*
            """
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                st.session_state.final_report = completion.choices[0].message.content
            except Exception as e:
                st.error(f"Error generating report: {e}")

    # Display Report
    if st.session_state.final_report:
        st.success(" Your Career Roadmap is Ready!")
        
        st.markdown("""
        <div class="report-card">
            """ + st.session_state.final_report.replace("\n", "<br>") + """
        </div>
        """, unsafe_allow_html=True)
        
        # Data Capture String
        capture_data = f"""
        NEW LEAD:
        Name: {st.session_state.contact_info['name']}
        Phone: {st.session_state.contact_info['phone']}
        Email: {st.session_state.contact_info['email']}
        Profile: {st.session_state.user_profile['status']} - {st.session_state.user_profile['goal']}
        
        REPORT:
        {st.session_state.final_report}
        """
        
        st.download_button(
            label="📥 Download & Save Report",
            data=capture_data,
            file_name=f"Distoversity_Guidance_{st.session_state.contact_info['name']}.txt",
            mime="text/plain"
        )
        
        st.markdown("### 📞 Take the Next Step")
        st.info("This report is just the beginning. Our counselors can help you apply to the universities that match this profile.")
        
        google_form_link = "https://forms.gle/YourFormLinkHere"
        st.markdown(f'<a href="{google_form_link}" target="_blank">Connect with a Counselor ➔</a>', unsafe_allow_html=True)
