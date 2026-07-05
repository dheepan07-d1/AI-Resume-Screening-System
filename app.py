import os
import tempfile
import shutil

import streamlit as st
import pandas as pd
import requests
import altair as alt

from parser.parser import extract_resume
from explainability.explain import explain_match


# -----------------------------
# Page Config
# -----------------------------

st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# CSS DESIGN
# -----------------------------

st.markdown(
    """
    <style>


    /* Main App Background */
    .stApp {

        background-color:#2E1065;

    }


    /* Main Heading */
    h1 {

        color:white;
        font-size:42px;
        font-weight:900;

    }


    /* Normal Text */
    p,label,h2,h3 {

        color:white !important;
        font-weight:600;

    }



    /* =========================
       FILE UPLOADER
       ========================= */


    section[data-testid="stFileUploader"] {

        background-color:#FDBA74;
        padding:22px;
        border-radius:18px;
        border:3px solid #FB923C;

    }


    section[data-testid="stFileUploader"] * {

        color:white !important;
        font-weight:bold;

    }


    section[data-testid="stFileUploader"] button {

        background-color:#EA580C !important;
        color:white !important;
        border-radius:12px;
        border:2px solid white;

    }



    /* =========================
       JOB DESCRIPTION BOX
       ========================= */


    textarea {

        background-color:#312E81 !important;
        color:white !important;
        border-radius:18px !important;
        border:3px solid #A855F7 !important;
        font-weight:bold;

    }



    /* =========================
       BUTTON
       ========================= */


    .stButton button {

        background-color:#9333EA;
        color:white;
        border-radius:15px;
        padding:12px 30px;
        border:none;
        font-weight:bold;

    }


    .stButton button:hover {

        background-color:#7E22CE;
        color:white;

    }




    /* =========================
       DASHBOARD CARDS
       ========================= */


    div[data-testid="metric-container"] {

        background-color:#4C1D95;
        padding:25px;
        border-radius:18px;
        border-left:10px solid #22C55E;

    }


    div[data-testid="metric-container"] * {

        color:white !important;

    }




    /* =========================
       DATA TABLE
       ========================= */


    div[data-testid="stDataFrame"] {

        background-color:#312E81;
        border-radius:15px;

    }




    /* =========================
       EXPANDER
       ========================= */


    div[data-testid="stExpander"] {

        background-color:#1E1B4B;
        border-radius:18px;
        border:2px solid #A855F7;

    }


    div[data-testid="stExpander"] * {

        color:white;

    }



    /* Success / Info boxes */
    div[data-testid="stAlert"] {

        border-radius:15px;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# -----------------------------
# TITLE
# -----------------------------

st.title(
    "📄 AI Resume Screening & Job Matching System"
)

st.write(
    "Upload resumes, enter Job Description and get AI-powered candidate ranking."
)



# -----------------------------
# Upload
# -----------------------------

uploaded_files = st.file_uploader(

    "Upload Resume(s)",

    type=[
        "pdf",
        "docx",
        "txt"
    ],

    accept_multiple_files=True

)



# -----------------------------
# Job Description
# -----------------------------

job_description = st.text_area(

    "Paste Job Description",

    height=220

)



# -----------------------------
# Button
# -----------------------------

if st.button(
    "🚀 Rank Candidates"
):


    if not uploaded_files:


        st.warning(
            "Please upload resumes"
        )



    elif not job_description.strip():


        st.warning(
            "Please enter job description"
        )



    else:



        with st.spinner(
            "Processing Resumes..."
        ):



            files=[]


            for file in uploaded_files:


                files.append(

                    (

                        "resumes",

                        (

                            file.name,

                            file.getvalue(),

                            file.type

                        )

                    )

                )



            response=requests.post(


                "http://127.0.0.1:8000/rank",


                data={

                    "description":
                    job_description

                },


                files=files

            )



            results=response.json()["candidates"]




        st.success(
            "✅ Ranking Completed!"
        )



        # -----------------------------
        # DATAFRAME
        # -----------------------------


        df=pd.DataFrame(
            results
        )


        df.index+=1


        df.index.name="Rank"




        # -----------------------------
        # DASHBOARD
        # -----------------------------


        c1,c2,c3,c4=st.columns(4)


        c1.metric(

            "📄 Total Resumes",

            len(df)

        )


        c2.metric(

            "🏆 Highest Score",

            str(df["score"].max())+"%"

        )


        c3.metric(

            "📊 Average Score",

            str(round(
                df["score"].mean(),
                2
            ))+"%"

        )


        c4.metric(

            "🥇 Top Candidate",

            df.iloc[0]["resume"]

        )



        st.divider()



        # -----------------------------
        # TABLE
        # -----------------------------


        st.subheader(
            "🏆 Candidate Ranking"
        )


        st.dataframe(

            df,

            use_container_width=True

        )



        # -----------------------------
        # GREEN CHART
        # -----------------------------


        st.subheader(
            "📊 Candidate Scores"
        )


        green_chart = (

            alt.Chart(
                df.reset_index()
            )

            .mark_bar(
                color="#22C55E"
            )

            .encode(

                x="resume",

                y="score"

            )

        )


        st.altair_chart(

            green_chart,

            use_container_width=True

        )



        # -----------------------------
        # CSV
        # -----------------------------


        csv=(

            df.to_csv(
                index=False
            )

            .encode(
                "utf-8"
            )

        )



        st.download_button(

            "⬇ Download Ranking CSV",

            csv,

            "ranking_results.csv",

            "text/csv"

        )




        st.divider()



        # -----------------------------
        # EXPLANATION
        # -----------------------------


        st.subheader(
            "📑 Resume Explanations"
        )



        temp_folder=tempfile.mkdtemp()



        for file in uploaded_files:


            path=os.path.join(

                temp_folder,

                file.name

            )


            with open(path,"wb") as f:


                f.write(
                    file.getbuffer()
                )




        for candidate in results:



            resume_path=os.path.join(

                temp_folder,

                candidate["resume"]

            )



            resume_text=extract_resume(
                resume_path
            )



            explanation=explain_match(

                resume_text,

                job_description

            )




            with st.expander(

                candidate["resume"]

            ):



                score=candidate["score"]


                st.write(

                    f"### Match Score: {score}%"

                )




                if score>=35:


                    st.success(
                        "⭐⭐ Highly Recommended"
                    )


                elif score>=20:


                    st.info(
                        "✅ Recommended"
                    )


                elif score>=10:


                    st.warning(
                        "⚠ Consider"
                    )


                else:


                    st.error(
                        "❌ Not Recommended"
                    )




                st.write(
                    "### ✅ Matched Skills"
                )



                if explanation["matched"]:


                    st.write(

                        ", ".join(
                            explanation["matched"]
                        )

                    )


                else:


                    st.write(
                        "None"
                    )




                st.write(
                    "### ❌ Missing Skills"
                )



                if explanation["missing"]:


                    st.write(

                        ", ".join(
                            explanation["missing"]
                        )

                    )


                else:


                    st.write(
                        "None"
                    )




        shutil.rmtree(
            temp_folder
        )