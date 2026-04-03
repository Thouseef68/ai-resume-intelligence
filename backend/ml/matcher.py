from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pickle

model = pickle.load(open("ml/model.pkl", "rb"))
vectorizer = pickle.load(open("ml/vectorizer.pkl", "rb"))

from ml.embedding_matcher import compute_embedding_score

def compute_similarity(resume, job):

    text = resume + " " + job
    X = vectorizer.transform([text])

    ml_score = model.predict_proba(X)[0][1] * 100
    emb_score = compute_embedding_score(resume, job)
    final_score = (0.6 * ml_score) + (0.4 * emb_score)

    return final_score