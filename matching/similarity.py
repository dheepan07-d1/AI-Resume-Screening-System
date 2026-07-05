from sentence_transformers import SentenceTransformer, util

# Load the model once
model = SentenceTransformer("all-MiniLM-L6-v2")

def calculate_similarity(resume_text, job_description):
    """
    Returns semantic similarity score between resume and job description.
    """

    resume_embedding = model.encode(resume_text, convert_to_tensor=True)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)

    score = util.cos_sim(resume_embedding, jd_embedding).item()

    return round(score * 100, 2)