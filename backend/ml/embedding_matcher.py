
from sklearn.metrics.pairwise import cosine_similarity


def compute_embedding_score(resume, job):
    # simple fallback similarity
    resume_words = set(resume.split())
    job_words = set(job.split())

    if len(job_words) == 0:
        return 0

    score = len(resume_words.intersection(job_words)) / len(job_words)

    return score * 100