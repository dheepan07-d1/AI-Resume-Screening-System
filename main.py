import os
import shutil
import tempfile

from fastapi import FastAPI, UploadFile, File, Form

from matching.ranking import rank_resumes


app = FastAPI(
    title="AI Resume Screening API"
)


@app.get("/")
def home():
    return {
        "message": "AI Resume Screening API Running"
    }


@app.post("/rank")
async def rank_candidates(
    description: str = Form(...),
    resumes: list[UploadFile] = File(...)
):

    temp_folder = tempfile.mkdtemp()

    try:

        for resume in resumes:

            path = os.path.join(
                temp_folder,
                resume.filename
            )

            with open(path, "wb") as f:
                shutil.copyfileobj(
                    resume.file,
                    f
                )


        results = rank_resumes(
            temp_folder,
            description
        )


        return {
            "candidates": results
        }


    finally:

        shutil.rmtree(
            temp_folder
        )