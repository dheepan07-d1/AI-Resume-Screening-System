import re


SKILLS = {

    # ======================
    # IT / Software
    # ======================

    "python",
    "java",
    "c++",
    "sql",
    "mysql",
    "mongodb",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "nlp",

    "tensorflow",
    "pytorch",
    "keras",

    "html",
    "css",
    "javascript",
    "react",

    "flask",
    "fastapi",
    "streamlit",

    "git",
    "github",
    "docker",
    "aws",


    # ======================
    # Teacher / Education
    # ======================

    "teacher",
    "teaching",
    "education",
    "lecturer",
    "professor",
    "academic",
    "training",
    "curriculum",
    "lesson planning",
    "student management",
    "research",
    "communication",


    # ======================
    # Accountant / Finance
    # ======================

    "accountant",
    "accounting",
    "finance",
    "financial analysis",
    "taxation",
    "auditing",
    "gst",
    "tally",
    "payroll",
    "excel",
    "bookkeeping",


    # ======================
    # Advocate / Legal
    # ======================

    "advocate",
    "lawyer",
    "legal",
    "litigation",
    "contract law",
    "legal research",
    "legal drafting",
    "court",
    "criminal law",
    "civil law",
    "arbitration",


    # ======================
    # Banking
    # ======================

    "banking",
    "loan processing",
    "mortgage banking",
    "risk management",
    "underwriting",
    "compliance",
    "quality assurance",


    # ======================
    # HR
    # ======================

    "human resources",
    "hr",
    "recruitment",
    "talent acquisition",
    "employee management",
    "interviewing",


    # ======================
    # Marketing
    # ======================

    "marketing",
    "digital marketing",
    "seo",
    "sales",
    "advertising",
    "social media",


    # ======================
    # Medical
    # ======================

    "doctor",
    "medicine",
    "healthcare",
    "patient care",
    "clinical",
    "nursing"
}



def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        if re.search(
            r"\b" + re.escape(skill) + r"\b",
            text
        ):
            found.append(skill)


    return sorted(
        list(set(found))
    )