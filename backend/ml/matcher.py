from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pickle

import os

BASE_DIR = os.path.dirname(__file__)

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

model = pickle.load(open(model_path, "rb"))
vectorizer = pickle.load(open(vectorizer_path, "rb"))
from backend.ml.embedding_matcher import compute_embedding_score

def compute_similarity(resume, job):

    text = resume + " " + job
    X = vectorizer.transform([text])

    ml_score = model.predict_proba(X)[0][1] * 100
    emb_score = compute_embedding_score(resume, job)
    final_score = (0.6 * ml_score) + (0.4 * emb_score)

    return final_score