import os
import tempfile
import shutil

import streamlit as st
import pandas as pd
import altair as alt


from matching.ranking import rank_resumes
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


.stApp {

    background-color:#2E1065;

}


h1 {

    color:white;
    font-weight:900;

}


p,label,h2,h3 {

    color:white !important;
    font-weight:600;

}



/* Upload Area */

section[data-testid="stFileUploader"] {


    background-color:#FDBA74;

    padding:20px;

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

}



/* Text Area */

textarea {


    background-color:#312E81 !important;

    color:white !important;

    border-radius:15px !important;

    border:2px solid #A855F7 !important;

}



/* Button */

.stButton button {


    background-color:#9333EA;

    color:white;

    border-radius:15px;

    font-weight:bold;

}


.stButton button:hover {


    background-color:#7E22CE;

    color:white;

}



/* Cards */

div[data-testid="metric-container"] {


    background-color:#4C1D95;

    padding:20px;

    border-radius:15px;

    border-left:8px solid #22C55E;

}


div[data-testid="metric-container"] * {

    color:white !important;

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
            "AI analyzing resumes..."
        ):



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



            # AI Ranking directly

            results = rank_resumes(

                temp_folder,

                job_description

            )




        st.success(
            "✅ Ranking Completed!"
        )



        # -----------------------------
        # DataFrame
        # -----------------------------


        df=pd.DataFrame(results)


        df.index+=1


        df.index.name="Rank"



        # -----------------------------
        # Dashboard
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

            str(
                round(
                    df["score"].mean(),
                    2
                )
            )+"%"

        )


        c4.metric(

            "🥇 Top Candidate",

            df.iloc[0]["resume"]

        )



        st.divider()



        # Ranking Table


        st.subheader(
            "🏆 Candidate Ranking"
        )


        st.dataframe(

            df,

            use_container_width=True

        )



        # Green Chart


        st.subheader(
            "📊 Candidate Scores"
        )


        chart=(

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

            chart,

            use_container_width=True

        )




        # Download CSV


        csv=df.to_csv(
            index=False
        ).encode(
            "utf-8"
        )


        st.download_button(

            "⬇ Download Ranking CSV",

            csv,

            "ranking_results.csv",

            "text/csv"

        )




        st.divider()



        # -----------------------------
        # Explanation
        # -----------------------------


        st.subheader(
            "📑 Resume Explanations"
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


                st.write(

                    ", ".join(
                        explanation["matched"]
                    )

                    if explanation["matched"]

                    else "None"

                )



                st.write(
                    "### ❌ Missing Skills"
                )


                st.write(

                    ", ".join(
                        explanation["missing"]
                    )

                    if explanation["missing"]

                    else "None"

                )




        shutil.rmtree(
            temp_folder
        )