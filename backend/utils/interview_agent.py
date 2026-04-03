import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


# 🔥 1. GENERATE DYNAMIC QUESTION
def generate_interview_question(resume_text, history):

    prompt = f"""
    You are a senior technical interviewer.

    Candidate Resume:
    {resume_text}

    Previous Q&A:
    {history}

    Task:
    - Ask ONE high-quality technical interview question
    - Adjust difficulty based on candidate level
    - Ask industry-level question

    Rules:
    - Only ONE question
    - No explanation
    """
    
    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

    except Exception as e:
        print("❌ Question generation failed:", e)

        if "quota" in str(e).lower() or "429" in str(e):
            return "⚠️ API limit reached. Please wait a few seconds and try again."

        return "Explain how you would design a scalable backend system?"

    # 🔥 fallback (no LLM)
    return "Explain how you would design a scalable backend system using microservices?"


# 🔥 2. EVALUATE ANSWER
def evaluate_answer(question, answer):

    prompt = f"""
    You are a strict technical interviewer.

    Question: {question}
    Candidate Answer: {answer}

    Evaluate:
    1. Is answer correct?
    2. What is missing?
    3. Provide correct answer

    Keep it structured and clear.
    """

    try:
        response = model.generate_content(prompt)

        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

    except Exception as e:
        print("❌ Evaluation failed:", e)

    return "Evaluation unavailable. Please try again."