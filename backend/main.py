from fastapi import FastAPI, UploadFile, File, Form
from utils.parser import extract_text_from_pdf
from ml.preprocess import clean_text
from ml.matcher import compute_similarity
from utils.skills import extract_skills, EXPECTED_SKILLS
from utils.llm_feedback import generate_feedback
from utils.interview_agent import generate_interview_question, evaluate_answer

app = FastAPI()

@app.post("/analyze")
async def analyze(resume: UploadFile = File(...), job_desc: str = Form(...)):
    text = extract_text_from_pdf(resume.file)
    
    clean_resume = clean_text(text)
    clean_job = clean_text(job_desc)
    
    score = compute_similarity(clean_resume, clean_job)
    
    
    resume_skills = extract_skills(clean_resume)
    job_skills = extract_skills(clean_job)
    print("JOB SKILLS:", job_skills)
    print("RESUME SKILLS:", resume_skills)
    
    missing = list(set(job_skills) - set(resume_skills))

    
   
    feedback = generate_feedback(resume_skills, missing, score)
    

    return {
        
        "match_score": score,
        "resume_skills": resume_skills,
        "missing_skills": missing,
        "feedback": feedback
    }
from fastapi import Body

@app.post("/evaluate")
async def evaluate(data: dict = Body(...)):

    question = data["question"]
    answer = data["answer"]

    feedback = evaluate_answer(question, answer)

    return {"evaluation": feedback}

@app.post("/next_question")
async def next_question(data: dict):

    resume_text = data.get("resume_text")
    history = data.get("history", [])

    question = generate_interview_question(resume_text, history)

    return {"question": question}