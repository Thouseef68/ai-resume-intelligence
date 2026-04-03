SKILLS = [
    # Programming
    "python", "sql",

    # ML / AI
    "machine learning", "deep learning", "nlp",
    "generative ai", "llm",

    # Frameworks
    "tensorflow", "pytorch", "scikit-learn",

    # LLM / Modern AI
    "gemini", "llama", "langchain",

    # Cloud
    "vertex ai", "cloud run", "gcp",

    # Backend
    "fastapi", "docker", "kubernetes"
]
EXPECTED_SKILLS = [
    "system design",
    "kubernetes",
    "ci/cd",
    "api development",
    "microservices",
    "data structures",
    "algorithms"
]
def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill.lower() in text.lower():
            found.append(skill)
    return list(set(found))

