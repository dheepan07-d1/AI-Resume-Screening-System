from extraction.skill_extractor import extract_skills
from preprocessing.preprocess import preprocess_text

def explain_match(resume_text, job_description):
    """
    Compare resume skills with job description skills.
    """

    clean_resume = preprocess_text(resume_text)
    clean_jd = preprocess_text(job_description)

    resume_skills = set(extract_skills(clean_resume))
    jd_skills = set(extract_skills(clean_jd))

    matched = sorted(list(resume_skills & jd_skills))
    missing = sorted(list(jd_skills - resume_skills))

    return {
        "matched": matched,
        "missing": missing
    }