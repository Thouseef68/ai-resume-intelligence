import streamlit as st
import sys

# ✅ IMPORTANT: path first
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.utils.parser import extract_text_from_pdf
from backend.ml.preprocess import clean_text
from backend.ml.matcher import compute_similarity
from backend.utils.skills import extract_skills
from backend.utils.llm_feedback import generate_feedback
from backend.utils.interview_agent import generate_questions, evaluate_answer

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.markdown("## 🚀 AI Resume Intelligence System")
st.caption("Smart Matching • Adaptive Interview • Real ML Engine")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)")

with col2:
    job_desc = st.text_area("💼 Paste Job Description", height=200)


# =========================
# 🔍 ANALYZE
# =========================
if st.button("🔍 Analyze Resume"):

    if uploaded_file and job_desc:

        with st.spinner("🤖 AI is analyzing your resume..."):

            text = extract_text_from_pdf(uploaded_file)

            clean_resume = clean_text(text)
            clean_job = clean_text(job_desc)

            score = compute_similarity(clean_resume, clean_job)

            resume_skills = extract_skills(clean_resume)
            job_skills = extract_skills(clean_job)

            missing = list(set(job_skills) - set(resume_skills))

            feedback = generate_feedback(resume_skills, missing, score)
            questions = generate_questions(missing)

            result = {
                "match_score": score,
                "resume_skills": resume_skills,
                "missing_skills": missing,
                "feedback": feedback,
                "questions": questions.split("\n")
            }

            st.session_state.analysis_done = True
            st.session_state.result = result
            st.session_state.current_q = 0


# =========================
# 📊 RESULTS
# =========================
if "analysis_done" in st.session_state:

    result = st.session_state.result

    st.subheader("📊 Match Score")
    score = round(result["match_score"], 2)

    st.progress(int(score))

    if score >= 75:
        st.success(f"🔥 Excellent Match: {score}%")
    elif score >= 50:
        st.info(f"👍 Good Match: {score}%")
    elif score >= 30:
        st.warning(f"⚠️ Moderate Match: {score}%")
    else:
        st.error(f"❌ Low Match: {score}%")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("### 🧠 Skills")
        st.markdown(" ".join([f"`{s}`" for s in result["resume_skills"]]))

    with col4:
        if result["missing_skills"]:
            st.markdown("### ❌ Missing")
            st.markdown(" ".join([f"`{s}`" for s in result["missing_skills"]]))
        else:
            st.success("🎉 No Missing Skills!")

    st.markdown("### 🤖 AI Feedback")
    st.info(result["feedback"])


# =========================
# 🎤 INTERVIEW MODE
# =========================
    st.subheader("🎤 AI Interview Mode")

    questions = result["questions"]

    if st.session_state.current_q < len(questions):

        question = questions[st.session_state.current_q]

        st.markdown(f"### 🎯 Q{st.session_state.current_q+1}: {question}")

        answer = st.text_area("Your Answer")

        if st.button("Submit Answer"):

            evaluation = evaluate_answer(question, answer)

            st.session_state.evaluation = evaluation
            st.session_state.answered = True

    # show evaluation
    if "answered" in st.session_state and st.session_state.answered:

        eval_text = st.session_state.evaluation.lower()

        if "correct" in eval_text:
            st.success("✅ Correct!")
            st.balloons()
        elif "wrong" in eval_text:
            st.error("❌ Incorrect")
            st.snow()
        else:
            st.info("🧠 Feedback")

        st.write(st.session_state.evaluation)

        if st.button("Next Question"):
            st.session_state.current_q += 1
            st.session_state.answered = False