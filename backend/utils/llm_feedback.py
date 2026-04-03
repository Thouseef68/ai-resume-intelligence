import os
import google.generativeai as genai
import time
import requests
from dotenv import load_dotenv
import requests

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
# ---------------- GEMINI ----------------
def gemini_call(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    if response and hasattr(response, "text"):
        return response.text


def groq_call(prompt):
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    data = response.json()

    print("Groq response:", data)  # 🔍 DEBUG

    if "choices" in data:
        return data["choices"][0]["message"]["content"]

    raise Exception(f"Groq API failed: {data}")


def openrouter_call(prompt):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model":"openrouter/auto",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    data = response.json()

    print("OpenRouter response:", data)  # 🔍 DEBUG

    if "choices" in data:
        return data["choices"][0]["message"]["content"]

    raise Exception(f"OpenRouter API failed: {data}")




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

    # 1️⃣ GEMINI
    try:
        print("👉 Trying Gemini...")
        return gemini_call(prompt)
    except Exception as e:
        print("❌ Gemini failed:", e)

    # 2️⃣ GROQ
    try:
        print("👉 Trying Groq...")
        return groq_call(prompt)
    except Exception as e:
        print("❌ Groq failed:", e)

    # 3️⃣ OPENROUTER
    try:
        print("👉 Trying OpenRouter...")
        return openrouter_call(prompt)
    except Exception as e:
        print("❌ OpenRouter failed:", e)

    # 4️⃣ FINAL FALLBACK
    print("⚠️ Using fallback")

    return f"""
    Evaluation:

    Strong skills: {', '.join(resume_skills[:3])}

    Focus on improving:
    {', '.join(missing_skills[:5])}

    Keep building real-world projects.
    """