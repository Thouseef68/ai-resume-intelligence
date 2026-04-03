import os
import google.generativeai as genai
from transformers import pipeline
import requests
from dotenv import load_dotenv


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

# 🔥 LOCAL MODEL
local_model = pipeline("text-generation", model="distilgpt2")

def local_feedback(prompt):
    try:
        result = local_model(prompt, max_length=120, num_return_sequences=1)
        return result[0]["generated_text"]
    except Exception as e:
        print("Local model failed:", e)
        return None


# 🔥 OPENROUTER
def openrouter_feedback(prompt):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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"
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
            print(f"👉 Trying model: {model_name}")

            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)

            if response and hasattr(response, "text") and response.text:
                print(f"✅ Success with: {model_name}")
                return response.text

            else:
                print(f"⚠️ Empty response from {model_name}")

        except Exception as e:
            print(f"❌ Failed with {model_name}: {e}")

    # 🔥 2. OPENROUTER
    response = openrouter_feedback(prompt)
    if response:
        print("✅ OpenRouter used")
        return response

    # 🔥 3. LOCAL MODEL
    response = local_feedback(prompt)
    if response:
        print("✅ Local model used")
        return response

    # 🔥 4. FINAL FALLBACK
    print("⚠️ Using rule-based fallback")

    return f"""
    Match Score: {score:.2f}%

    Improve:
    {', '.join(missing_skills[:5])}

    Focus on system design and core CS fundamentals.
    """