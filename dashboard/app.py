import os
import sys
import streamlit as st

# ----------------------------------------------------------
# Project Path
# ----------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

# ----------------------------------------------------------
# Imports
# ----------------------------------------------------------

from src.services.recruiter_service import RecruiterService

from styles import load_css

from components import (
    show_header,
    show_input,
    show_top_candidate,
    show_metrics,
    show_ranking_table,
    show_insights,
    show_analytics
)

# ----------------------------------------------------------
# Page Config
# ----------------------------------------------------------

st.set_page_config(

    page_title="AI Recruiter Intelligence",

    page_icon="🧠",

    layout="wide"

)

st.markdown(

    load_css(),

    unsafe_allow_html=True

)

# ----------------------------------------------------------
# Service Initialization
# ----------------------------------------------------------

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "candidates.jsonl"
)

if "service" not in st.session_state:

    st.session_state.service = RecruiterService()

# ----------------------------------------------------------
# Session State
# ----------------------------------------------------------

if "results" not in st.session_state:

    st.session_state.results = None

# ----------------------------------------------------------
# Header
# ----------------------------------------------------------

show_header()

# ----------------------------------------------------------
# Input Workspace
# ----------------------------------------------------------

job_description, analyze, right_panel = show_input()

# ----------------------------------------------------------
# Run Analysis
# ----------------------------------------------------------

if analyze:

    if not job_description.strip():
        
        st.session_state.results = None

        st.warning(
            "Please provide a Job Description."
        )

    else:

        with st.spinner(
            "Analyzing candidates..."
        ):

            try:

                results = (
                    st.session_state.service
                    .analyze_job_description(
                        job_description
                    )
                )

                st.session_state.results = results

            except Exception as e:

                st.error(
                    f"Analysis failed.\n\n{e}"
                )

# ----------------------------------------------------------
# Display Dashboard
# ----------------------------------------------------------

show_top_candidate(

    st.session_state.results,

    right_panel

)

show_metrics(

    st.session_state.results

)

show_ranking_table(

    st.session_state.results

)

show_insights(

    st.session_state.results

)

show_analytics(

    st.session_state.results

)