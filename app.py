import streamlit as st
from resume_parser import extract_text_from_pdf, extract_text_from_docx
from skill_extractor import extract_skills, SKILL_LIST
from utils import normalize_text

# Streamlit page setup
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Title
st.markdown("<h1 style='text-align: center; color: #4B0082;'>AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Upload your Resume & Job Description to analyze match score and missing skills.</p>", unsafe_allow_html=True)
st.markdown("---")

# -------------------------
# Upload Section
# -------------------------
col1, col2 = st.columns(2)

with col1:
    uploaded_resume = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])

with col2:
    uploaded_jd = st.file_uploader("Upload Job Description (TXT)", type=["txt"])

# -------------------------
# PROCESSING
# -------------------------
if uploaded_resume and uploaded_jd and st.button("Run Analyzer"):

    # ======= READ RESUME =======
    if uploaded_resume.type == "application/pdf":
        resume_text = extract_text_from_pdf(uploaded_resume)
    else:
        resume_text = extract_text_from_docx(uploaded_resume)

    resume_text = normalize_text(resume_text)

    # ======= READ JOB DESCRIPTION =======
    jd_text = uploaded_jd.read().decode("utf-8")
    jd_text = normalize_text(jd_text)

    # Display JD nicely
    st.markdown("<h3 style='color: #4B0082;'>Job Requirements / Skills Needed</h3>", unsafe_allow_html=True)
    st.text(jd_text)

    # ======= EXTRACT REQUIRED SKILLS FROM JD =======
    required_skills = extract_skills(jd_text)

    # ======= EXTRACT SKILLS FROM RESUME =======
    skills_found = extract_skills(resume_text)

    st.markdown("<h3 style='color: #228B22;'>Skills Found in Resume</h3>", unsafe_allow_html=True)
    st.write(" ".join([f"✅ {skill}" for skill in skills_found]) if skills_found else "❌ No skills detected")

    # ======= MATCH SCORE (SKILL BASED ONLY) =======
    def calculate_skill_match(required_skills, skills_found):
        if len(required_skills) == 0:
            return 0.0
        return round((len(skills_found) / len(required_skills)) * 100, 2)

    match_percentage = calculate_skill_match(required_skills, skills_found)

    # ======= MISSING SKILLS =======
    missing_skills = [skill for skill in required_skills if skill not in skills_found]

    st.markdown("<br>", unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)
    colA.metric("Match Percentage", f"{match_percentage}%")
    colB.metric("Skills Found", len(skills_found))
    colC.metric("Missing Skills", len(missing_skills))

    st.markdown("<h3 style='color: #FF0000;'>Missing Skills (Required but not in Resume)</h3>", unsafe_allow_html=True)

    if missing_skills:
        st.error(" ".join([f"❌ {skill}" for skill in missing_skills]))
    else:
        st.success("🎉 No missing skills! Your resume perfectly matches the job description.")

    # Progress bar
    st.markdown("### Resume Match Progress")
    st.progress(int(match_percentage))

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: grey;'>Powered by Python, AI & Streamlit</p>", unsafe_allow_html=True)
