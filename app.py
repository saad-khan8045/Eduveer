import streamlit as st
from groq import Groq
import time
import json

# --- 1. Web Page Configuration ---
st.set_page_config(
    page_title="Distoversity AI",
    page_icon="🎓",
    layout="centered"
)

# --- 2. WEBSITE-MATCHED UI Styling (Same as before) ---
st.markdown("""
    <style>
    /* Import 'Inter' font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background-color: #FFFFFF;
        color: #1F2937;
    }
    
    /* Main App Background */
    .stApp {
        background-color: #F3F8FC;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0D1B2A;
        font-weight: 700;
        text-align: center;
    }
    
    /* --- BUTTONS --- */
    .stButton button {
        background-color: #00AEEF;
        color: white !important;
        border: none;
        padding: 12px 32px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 4px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 174, 239, 0.2);
        width: 100%;
    }
    .stButton button:hover {
        background-color: #0095CC;
        transform: translateY(-1px);
        box-shadow: 0 4px 6px rgba(0, 174, 239, 0.3);
    }
    
    /* --- FORM & CARDS --- */
    [data-testid="stForm"], [data-testid="stChatInput"], .report-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 32px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }

    /* --- CHAT BUBBLES --- */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 16px;
    }
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #E0F2FE;
        border: 1px solid #BAE6FD;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #F1F5F9;
    }
    
    /* Sidebar Booking Button */
    a[href*="forms"] {
        display: inline-block;
        width: 100%;
        background-color: #00AEEF;
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 10px;
        transition: background-color 0.3s;
    }
    a[href*="forms"]:hover {
        background-color: #0095CC;
    }

    /* Progress Bar Color */
    .stProgress > div > div > div > div {
        background-color: #00AEEF;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. Initialize Brain ---
try:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)
except Exception:
    st.error("⚠️ API Key Missing.")
    st.stop()

# --- 4. Session State Initialization ---
if "step" not in st.session_state:
    st.session_state.step = 1  # 1: Profile Form, 2: Quiz, 3: Contact Info, 4: Report
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = []
if "contact_info" not in st.session_state:
    st.session_state.contact_info = {}
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

# --- 5. Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712009.png", width=80)
    st.markdown("### **Distoversity**") 
    st.caption("Empowering India's Future Leaders 🇮🇳")
    
    if st.session_state.step > 1:
        progress = (len(st.session_state.quiz_answers) / 5) if st.session_state.step == 2 else 1.0
        st.progress(progress)
        st.caption(f"Assessment Progress")

    st.divider()
    if st.button("↻ Restart Assessment"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.caption("© 2025 Distoversity Pvt Ltd") 

# --- 6. Main Logic ---

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
        submitted = st.form_submit_button("Start 5-Question Assessment ➔")
        
        if submitted:
            st.session_state.user_profile = {"status": status, "goal": goal}
            st.session_state.step = 2
            st.rerun()

# --- STEP 2: THE 5-QUESTION QUIZ (Chat Interface) ---
elif st.session_state.step == 2:
    
    # Define the 5 Questions directly here for control
    questions = [
        "1. When starting a new project, what do you enjoy most? (Ideating, Leading people, Organizing details, or Researching data?)",
        "2. In a group, what role do you naturally take? (The Creative Spark, The Leader/Speaker, The Reliable Helper, or The Analyzer?)",
        "3. What kind of tasks drain your energy? (Repetitive details, Being alone too long, Conflict/Pressure, or Vague ideas without data?)",
        "4. If you could have a superpower at work/study, what would it be? (Endless Creativity, Super Persuasion, Perfect Timing/Harmony, or Instant Calculation?)",
        "5. How do you make decisions? (Gut feeling/Innovation, Discussing with others, Sensing the right time, or Logic and spreadsheet?)"
    ]
    
    current_q_index = len(st.session_state.quiz_answers)
    
    if current_q_index < 5:
        st.markdown(f"### Question {current_q_index + 1} of 5")
        st.info(questions[current_q_index])
        
        # Chat input for the answer
        if answer := st.chat_input("Type your answer here..."):
            st.session_state.quiz_answers.append(answer)
            st.rerun()
            
        # Display previous Q&A for context
        for i, ans in enumerate(st.session_state.quiz_answers):
            with st.chat_message("assistant", avatar="🎓"):
                st.write(questions[i])
            with st.chat_message("user", avatar="🧑‍🎓"):
                st.write(ans)
                
    else:
        st.session_state.step = 3
        st.rerun()

# --- STEP 3: CONTACT INFO FORM ---
elif st.session_state.step == 3:
    st.markdown("### Assessment Complete! 🎉")
    st.markdown("To generate your detailed **Genius Profile Report** and university shortlist, please provide your details.")
    
    with st.form("contact_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Mobile Number")
        
        submit_contact = st.form_submit_button("Generate My Report ➔")
        
        if submit_contact and name and email and phone:
            st.session_state.contact_info = {"name": name, "email": email, "phone": phone}
            st.session_state.step = 4
            st.rerun()
        elif submit_contact:
            st.error("Please fill in all fields to get your report.")

# --- STEP 4: REPORT GENERATION & ANALYSIS ---
elif st.session_state.step == 4:
    if not st.session_state.final_report:
        with st.spinner("Analyzing your 4 Energies... Calculating percentages..."):
            
            # Prepare data for AI Analysis
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
            Act as a Veteran Career Assessment Expert at Distoversity.
            Analyze the following user answers based on the 4 Energies Framework:
            - Creator (Innovation, Ideas)
            - Influencer (People, Leadership)
            - Catalyst (Service, Timing, Grounded)
            - Analyst (Data, Systems, Logic)

            USER DATA:
            {user_data_str}

            TASK:
            1. Calculate an estimated percentage for each of the 4 energies based on the answers. (e.g., Creator: 60%, Influencer: 20%, etc.). Ensure no single profile is blindly 100% unless answers strongly suggest it.
            2. Identify the DOMINANT profile.
            3. Write a "Veteran's Insight" explaining their strengths simply (12th-grade level English).
            4. Suggest 3 specific career paths or courses suitable for this mix.

            OUTPUT FORMAT (Strictly follow this):
            # 🎓 Genius Profile Report for [User Name placeholder]
            
            ## ⚡ Energy Distribution
            - **Creator:** [X]%
            - **Influencer:** [X]%
            - **Catalyst:** [X]%
            - **Analyst:** [X]%
            
            ## 🏆 Your Dominant Profile: [Profile Name]
            
            ### 🧠 Veteran's Insight
            [Write a 3-4 sentence warm, wise analysis of why they fit this profile and how it's a superpower.]
            
            ### 🚀 Recommended Paths
            1. **[Path 1]**: [Why?]
            2. **[Path 2]**: [Why?]
            3. **[Path 3]**: [Why?]
            
            ---
            *Report generated by Distoversity AI*
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
        st.success("Analysis Complete!")
        
        # Custom CSS for Report Card
        st.markdown("""
        <div class="report-card">
            """ + st.session_state.final_report.replace("\n", "<br>") + """
        </div>
        """, unsafe_allow_html=True)
        
        # Data Capture String (For email/admin)
        capture_data = f"""
        NEW LEAD:
        Name: {st.session_state.contact_info['name']}
        Phone: {st.session_state.contact_info['phone']}
        Email: {st.session_state.contact_info['email']}
        Profile: {st.session_state.user_profile['status']} - {st.session_state.user_profile['goal']}
        
        REPORT SUMMARY:
        {st.session_state.final_report}
        """
        
        st.download_button(
            label="📥 Download Your Report",
            data=capture_data,
            file_name=f"Distoversity_Report_{st.session_state.contact_info['name']}.txt",
            mime="text/plain"
        )
        
        st.markdown("### 📞 Next Steps")
        st.info("Our expert counselors have received your profile. We will contact you shortly to discuss university admissions based on this report.")
        
        # Google Form Link for manual submission if they want
        google_form_link = "https://forms.gle/YourFormLinkHere"
        st.markdown(f'<a href="{google_form_link}" target="_blank">Submit to Counselor Directly ➔</a>', unsafe_allow_html=True)
