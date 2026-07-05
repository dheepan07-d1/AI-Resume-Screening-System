import os

from parser.pdf_parser import extract_pdf_text
from parser.docx_parser import extract_docx_text
from parser.txt_parser import extract_txt_text


def extract_resume(resume_path):

    extension = os.path.splitext(resume_path)[1].lower()

    if extension == ".pdf":
        return extract_pdf_text(resume_path)

    elif extension == ".docx":
        return extract_docx_text(resume_path)

    elif extension == ".txt":
        return extract_txt_text(resume_path)

    else:
        return ""