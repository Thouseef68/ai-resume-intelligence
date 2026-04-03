import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


# 🔥 GENERATE QUESTIONS
def generate_questions(missing_skills):

    prompt = f"""
    You are a technical interviewer.

    Based on these skills:
    {missing_skills}

    Generate 3 real-world technical interview questions.

    Rules:
    - Only questions
    - No explanation
    - Numbered (1,2,3)
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        

        start = time.time()

        response = model.generate_content(prompt)

        # ⏱ STOP if too slow
        if time.time() - start > 10:
            raise Exception("Timeout")

        if response and hasattr(response, "text"):
            return response.text

    except Exception as e:
        print("Gemini failed:", e)

    # fallback
    return f"""
1. Explain how you would use {missing_skills[0] if missing_skills else 'microservices'} in a real project?
2. How would you implement {missing_skills[1] if len(missing_skills)>1 else 'CI/CD'}?
3. What are best practices for {missing_skills[2] if len(missing_skills)>2 else 'system design'}?
"""


# 🔥 EVALUATE ANSWER
def evaluate_answer(question, answer):

    prompt = f"""
    You are a strict technical interviewer.

    Question: {question}
    Answer: {answer}

    Evaluate:
    - Is it correct?
    - What is missing?
    - Give correct answer

    Keep it short.
    """

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text

    except Exception as e:
        print("Evaluation failed:", e)

    return "Evaluation not available."