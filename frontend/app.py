import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Matcher", layout="wide")

st.markdown("## 🚀 AI Resume Intelligence System")
st.caption("Smart Matching • Adaptive Interview • Real ML Engine")

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)")

with col2:
    job_desc = st.text_area("💼 Paste Job Description", height=200)

if st.button("🔍 Analyze Resume"):

    if uploaded_file and job_desc:

        files = {"resume": (uploaded_file.name, uploaded_file, "application/pdf")}
        data = {"job_desc": job_desc}

        response = requests.post("http://127.0.0.1:8000/analyze", files=files, data=data)
        result = response.json()
        st.session_state.analysis_done = True
        st.session_state.result = result
        st.session_state.resume_text = job_desc

if "analysis_done" in st.session_state and st.session_state.analysis_done:

    result = st.session_state.result

    st.subheader("📊 Match Score")
    st.progress(int(result["match_score"]))
    score = round(result["match_score"], 2)

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
        st.subheader("✅ Your Skills")
        st.markdown("### 🧠 Skills Detected")
        st.markdown(" ".join([f"`{skill}`" for skill in result["resume_skills"]]))

    with col4:
        st.subheader("❌ Missing Skills")
        if result["missing_skills"]:
            st.markdown("### ❌ Missing Skills")
            st.markdown(" ".join([f"`{skill}`" for skill in result["missing_skills"]]))
        else:
            st.success("🎉 No Missing Skills — Strong Match!")

    
    st.markdown("### 🤖 AI Feedback")
    st.info(result["feedback"])


    # =========================
    # 🎤 INTERVIEW MODE (FIXED)
    # =========================

    st.subheader("🎤 AI Interview Mode")

    if "history" not in st.session_state:
        st.session_state.history = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    if "evaluation" not in st.session_state:
        st.session_state.evaluation = None

    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

    # Load first question
    if st.session_state.current_question is None:
        response = requests.post(
            "http://127.0.0.1:8000/next_question",
            json={
                "resume_text": st.session_state.resume_text,
                "history": st.session_state.history
            }
        )
        st.session_state.current_question = response.json()["question"]

    # Show question
    st.write("### Question:")
    st.markdown(f"### 🎯 {st.session_state.current_question}")

    answer = st.text_area("Your Answer", key="answer_box")

    # Submit
    if st.button("Submit Answer") and answer:

        eval_res = requests.post(
            "http://127.0.0.1:8000/evaluate",
            json={
                "question": st.session_state.current_question,
                "answer": answer
            }
        )

        st.session_state.evaluation = eval_res.json()["evaluation"]
        st.session_state.answer_submitted = True

        st.session_state.history.append({
            "question": st.session_state.current_question,
            "answer": answer
        })

    # Show evaluation
    if st.session_state.answer_submitted:
        st.write("### 🧠 Evaluation:")
        evaluation = st.session_state.evaluation.lower()

        if "correct" in evaluation:
            st.success("✅ Correct Answer!")
            st.balloons()
        elif "wrong" in evaluation:
            st.error("❌ Incorrect Answer")
            st.snow()
        else:
            st.info("🧠 Feedback:")
            
        st.write(st.session_state.evaluation)

    # Next question
    if st.session_state.answer_submitted:
        if st.button("Next Question"):

            with st.spinner("⏳ Generating next question..."):

                next_q = requests.post(
                "http://127.0.0.1:8000/next_question",
                json={
                    "resume_text": st.session_state.resume_text,
                    "history": st.session_state.history
                }
            )

            st.session_state.current_question = next_q.json()["question"]

            st.session_state.answer_submitted = False
            st.session_state.evaluation = None
            st.session_state.answer_box = ""