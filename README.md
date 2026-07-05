# AI Resume Screening & Job Matching System

## Project Overview

The AI Resume Screening & Job Matching System is an intelligent recruitment application that automatically ranks resumes based on a given job description. It uses Natural Language Processing (NLP) and Sentence Transformers to compare resumes with job requirements and provide candidate rankings with explainable results.

---

## Features

* Upload multiple resumes (PDF, DOCX, TXT)
* Enter a job description
* AI-based resume ranking
* Resume parsing and text extraction
* NLP preprocessing
* Semantic similarity using Sentence Transformers
* Skill extraction
* Matched and missing skills
* Candidate ranking dashboard
* Candidate score visualization
* Download ranking results as CSV

---

## Technologies Used

### Programming Language

* Python

### Libraries

* Streamlit
* Sentence Transformers
* spaCy
* Pandas
* Scikit-learn
* PDFPlumber
* Python-docx
* PyTorch

---

## Project Structure

AI-Resume-Screening-System/

* app.py
* main.py
* parser/
* preprocessing/
* extraction/
* matching/
* explainability/
* dataset/
* models/
* utils/
* requirements.txt
* README.md

---

## How to Run

1. Create a virtual environment

```
python -m venv venv
```

2. Activate the virtual environment

Windows:

```
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Run the application

```
streamlit run app.py
```

---

## Workflow

1. Upload resumes
2. Enter job description
3. Resume parsing
4. Text preprocessing
5. Skill extraction
6. Semantic similarity calculation
7. Resume ranking
8. Explainability generation
9. Display dashboard

---

## Future Enhancements

* Dynamic skill extraction
* Experience extraction
* Education matching
* Recruiter login
* Database integration
* Resume upload history
* FastAPI backend

---

## Developed By

Dhana Rani

B.Tech Artificial Intelligence & Data Science

Sri Krishna College of Engineering and Technology (SKCET)
