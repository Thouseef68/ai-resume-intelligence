import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
from backend.utils.llm_feedback import gemini_call, groq_call, openrouter_call

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)


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

    print("🎯 Generating Questions...")

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
    print("⚠️ Using fallback questions")

    return f"""
1. How would you design a scalable system using {missing_skills[0] if missing_skills else 'microservices'}?
2. Explain how {missing_skills[1] if len(missing_skills)>1 else 'CI/CD'} works in production?
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


    except Exception as e:
        print("Evaluation failed:", e)

    return "Evaluation not available."