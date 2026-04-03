import os
import google.generativeai as genai
import time
import requests
from dotenv import load_dotenv



load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)





# 🔥 OPENROUTER
def openrouter_feedback(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            },
            json={
                "model": "mistral/mixtral-8x7b",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        data = response.json()

        if "choices" in data:
            return data["choices"][0]["message"]["content"]

        return None

    except Exception as e:
        print("OpenRouter failed:", e)
        return None


# 🔥 MODEL LIST (CLEANED)
GENAI_MODELS = [
    "Gemini 1.5 Flash",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]

def generate_feedback(resume_skills, missing_skills, score):

    prompt = f"""
    You are an AI career coach.

    Candidate Skills: {resume_skills}
    Missing Skills: {missing_skills}
    Match Score: {score}

    Give short evaluation and improvement advice.
    """

    print("🔍 Starting LLM fallback system...")

    # 🔥 1. GEMINI
    for model_name in GENAI_MODELS:
        try:
            start = time.time()

            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt)

            # ⏱ timeout check (10 sec max)
            if time.time() - start > 10:
                raise Exception("Timeout")

            if response and hasattr(response, "text"):
                return response.text

        except Exception as e:
            print("Gemini slow/fail:", e)

        # 🔥 FAST FALLBACK (instant)
        return f"""
    Evaluation:

    Strong skills: {', '.join(resume_skills[:3])}

    Focus on improving:
    {', '.join(missing_skills[:5])}

    Keep building real-world projects.
    """