import os

from parser.parser import extract_resume
from preprocessing.cleaner import clean_text

from matching.similarity import calculate_similarity

from extraction.skill_extractor import extract_skills


def rank_resumes(folder_path, job_description):

    results = []


    job_clean = clean_text(
        job_description
    )


    job_skills = set(
        extract_skills(
            job_description
        )
    )


    for file in os.listdir(folder_path):


        print(
            "Processing:",
            file
        )


        path = os.path.join(
            folder_path,
            file
        )


        resume_text = extract_resume(
            path
        )


        resume_clean = clean_text(
            resume_text
        )


        # AI similarity

        ai_score = calculate_similarity(
            resume_clean,
            job_clean
        )


        # skill similarity

        resume_skills = set(
            extract_skills(
                resume_text
            )
        )


        matched = (
            resume_skills
            &
            job_skills
        )


        if len(job_skills) > 0:

            skill_score = (
                len(matched)
                /
                len(job_skills)
            ) * 100

        else:

            skill_score = 0


        final_score = (

            (0.7 * ai_score)

            +

            (0.3 * skill_score)

        )


        final_score = round(
            final_score,
            2
        )


        print(
            "Score =",
            final_score
        )


        results.append(
            {
                "resume": file,

                "score": final_score
            }
        )



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    return results