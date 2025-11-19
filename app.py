import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Eduveer - Distoversity Career Advisor",
    page_icon="🎓",
    layout="centered"
)

# --- CATCHY UI CSS ---
st.markdown("""
<style>
body, .stApp {
    background: linear-gradient(90deg, #0077b6 0%, #00AEEF 80%, #CAF0F8 100%);
}
h1, h2, h3 {
    color: #0D1B2A;
    font-weight: 800;
    text-shadow: 0 2px 18px #00AEEF99;
    text-align: center;
}
.stButton button {
    background: linear-gradient(90deg, #00AEEF, #0077b6 60%, #CAF0F8 100%);
    color: white;
    border-radius: 8px;
    box-shadow: 0 4px 16px #00AEEF68;
    padding: 14px 38px;
    font-weight: 700;
    font-size: 18px;
    transition: box-shadow 0.3s, transform 0.2s;
}
.stButton button:hover {
    box-shadow: 0 8px 28px #00AEEF99;
    transform: scale(1.05);
}
.card {
    background-color: #fff;
    border: 2px solid #00AEEF;
    border-radius: 16px;
    box-shadow: 0 2px 16px #CAF0F844;
    padding: 26px;
    margin: 18px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# --- UNIVERSITY DATA (Expand as Needed) ---
universities = [
    {"name": "Amity Online", "logo": "https://www.amityonline.com/themes/custom/amityonline/images/favicon/apple-touch-icon.png",
     "degrees": ["MBA Online", "BCA Online", "BBA Online"], "apply": "https://www.amityonline.com/"},
    {"name": "Jain Online", "logo": "https://www.jainuniversity.ac.in/themes/custom/jain/favicon.ico",
     "degrees": ["MCA Online", "BCom Online"], "apply": "https://jainuniversity.ac.in/"},
    {"name": "Manipal Online", "logo": "https://www.onlinemanipal.com/static/favicon.ico",
     "degrees": ["BSc Data Science", "MBA Online"], "apply": "https://www.onlinemanipal.com/"},
]

energy_to_degrees = {
    "Creator": ["BBA Online", "BA Journalism", "B.Des (Design)"],
    "Influencer": ["MBA Online", "BCom Online", "BA Psychology"],
    "Catalyst": ["BA Social Work", "B.Ed Online"],
    "Analyst": ["BCA Online", "BSc Data Science", "MCA Online"]
}

# --- APP HEADER ---
st.title("🎓 Eduveer – India's Veteran Career Advisor")
st.markdown("<div style='text-align:center;color:#0077b6;font-size:1.15rem;'>Expert guidance for your online degree dream. Powered by Distoversity.</div>", unsafe_allow_html=True)
st.markdown("")

# --- USER PROFILE DEMO for QUICK TESTING ---
status = st.selectbox("Who are you?", ["Student (12th/Grad)", "Working Professional"])
goal = st.selectbox("Your Goal:", ["Online/Distance Degree", "Regular Degree", "Upskilling/Certificate"])
energy = st.selectbox("Which describes you best?", ["Creator", "Influencer", "Catalyst", "Analyst"])
st.markdown("")

# --- UNIVERSITY RECOMMENDATIONS ---
st.subheader("🔎 Top Online Universities For You")
matching_degrees = energy_to_degrees[energy]

for uni in universities:
    # Filter university's degrees by user energy type
    offered = [deg for deg in uni["degrees"] if deg in matching_degrees]
    if offered:
        st.markdown(f"""
        <div class="card">
            <img src="{uni['logo']}" width="44" style="border-radius:8px;float:left;margin-right:15px;" />
            <strong style="font-size:1.3em;">{uni['name']}</strong><br>
            <span style="color:#0077b6;font-weight:600;">Degree Programs:</span> {', '.join(offered)}<br>
            <a href="{uni['apply']}" target="_blank"><button style="
                background:linear-gradient(90deg,#00AEEF,#0077b6 70%,#CAF0F8 100%);
                color:white;padding:10px 28px;border:none;border-radius:6px;
                font-weight:700;margin-top:14px;cursor:pointer;">Apply Now</button></a>
        </div>
        """, unsafe_allow_html=True)

# --- WISE ADVISOR MESSAGE ---
st.success(f"In my 20 years, students with '{energy}' energy thrive in careers linked to these degrees. These online programs are recognized, flexible, and respected across India.\n\nWould you like a personalized career assessment or application help?")

st.markdown("<div style='text-align:center;'><a href='https://forms.gle/YourFormLinkHere' target='_blank' style='color:white;font-weight:700;background:#00AEEF;padding:10px 20px;border-radius:4px;text-decoration:none;'>Book Free Career Session</a></div>", unsafe_allow_html=True)

