import streamlit as st
import pandas as pd
from exporter import generate_excel


# ----------------------------------------------------------
# Header
# ----------------------------------------------------------

def show_header():

    st.markdown(
        """
        <div class="main-title">
            🧠 AI Recruiter Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sub-title">
            Reading Between the Lines of Candidate Resumes
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")


# ----------------------------------------------------------
# Job Description Input
# ----------------------------------------------------------

def show_input():

    left, right = st.columns([1.4, 1])

    with left:

        st.subheader("📂 Input Workspace")

        input_mode = st.radio(

            "Select Input Method",

            [

                "Paste Job Description",

                "Upload Job Description"

            ]

        )

        job_description = ""

        if input_mode == "Paste Job Description":

            job_description = st.text_area(

                "Job Description",

                height=320,

                placeholder="Paste the complete Job Description here..."

            )

        else:

            uploaded_file = st.file_uploader(

                "Upload Job Description",

                type=["txt", "docx"]

            )

            if uploaded_file is not None:

                if uploaded_file.type == "text/plain":

                    job_description = uploaded_file.read().decode("utf-8")

                    st.success("Text file loaded successfully.")

                else:

                    st.info(
                        "DOCX support will be added in the next milestone."
                    )

        analyze = st.button(

            "🚀 Analyze Candidates",

            use_container_width=True

        )

    return job_description, analyze, right


# ----------------------------------------------------------
# Top Candidate
# ----------------------------------------------------------

def show_top_candidate(results, container):

    with container:

        st.subheader("🏆 Selected Candidate")

        if results is None:

            st.info(
                "Run an analysis to view the best candidate."
            )
            return

        evaluation = results["evaluation"]
        learning = results["learning"]
        top = results["ranked_candidates"][0]

        st.success(
            f"👤 {evaluation['candidate_name']}"
        )

        st.progress(
            evaluation["overall_match"] / 100
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Overall Match",
                f"{evaluation['overall_match']}%"
            )

            st.metric(
                "Semantic Score",
                f"{round(top['semantic_score']*100,2)}%"
            )

            st.metric(
                "Direct Skills",
                len(top["matched_skills"])
            )

        with col2:

            st.metric(
                "Learning",
                learning["learning_potential"]
            )

            st.metric(
                "Transferable Skills",
                top["num_transferable_matches"]
            )

            st.metric(
                "Confidence",
                evaluation["confidence"]
            )

        recommendation = evaluation["recommendation"]

        if recommendation == "Strong Hire":

            st.success("🟢 STRONG HIRE")

        elif recommendation == "Interview":

            st.info("🔵 INTERVIEW")

        elif recommendation == "Consider":

            st.warning("🟡 CONSIDER")

        elif recommendation == "Review":

            st.warning("🟠 REVIEW")

        else:

            st.error("🔴 REJECT")

        st.markdown("---")

        st.subheader("🧠 AI Decision Summary")

        summary = []

        if evaluation["strengths"]:
            summary.extend(evaluation["strengths"][:3])

        if learning["explanation"]:
            summary.extend(learning["explanation"][:2])

        seen = set()

        for point in summary:

            if point not in seen:
                st.write(f"✅ {point}")
                seen.add(point)

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

def show_metrics(results):

    st.markdown("---")

    st.subheader("📊 Dashboard Metrics")

    if results is None:

        st.info(

            "Metrics will appear after analysis."

        )

        return

    ranked = results["ranked_candidates"]

    evaluation = results["evaluation"]

    learning = results["learning"]

    top = ranked[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(

            "Candidates",

            len(ranked)

        )

    with col2:

        st.metric(

            "Best Candidate Score",

            f"{evaluation['overall_match']}%"

        )

    with col3:

        st.metric(

            "Learning",

            learning["learning_potential"]

        )

    with col4:

        st.metric(

            "Transferable Skills",

            top["num_transferable_matches"]

        )


# ----------------------------------------------------------
# Ranking Table
# ----------------------------------------------------------

def show_ranking_table(results):

    st.markdown("---")

    st.subheader("🏅 Top Candidate Rankings")

    if results is None:

        st.info("Candidate rankings will appear here.")
        return

    candidates = results["ranked_candidates"]

    # ----------------------------------------------------------
    # Ranking Table
    # ----------------------------------------------------------

    rows = []

    for index, candidate in enumerate(candidates[:10], start=1):

        matched = len(candidate["matched_skills"])
        missing = len(candidate["missing_skills"])

        total_required = matched + missing

        coverage = (
            round((matched / total_required) * 100, 1)
            if total_required > 0
            else 100
        )

        rows.append({

            "Rank": index,

            "Candidate": candidate["name"],

            "Overall Score": round(
                candidate["final_score"] * 100,
                2
            ),

            "Semantic %": round(
                candidate["semantic_score"] * 100,
                2
            ),

            "Coverage %": coverage,

            "Direct": matched,

            "Transferable": candidate[
                "num_transferable_matches"
            ]

        })

    df = pd.DataFrame(rows)

    st.dataframe(

        df,

        hide_index=True,

        use_container_width=True

    )

    # ----------------------------------------------------------
    # Export
    # ----------------------------------------------------------

    excel_file = generate_excel(results)

    st.download_button(

        "📥 Export Ranked Candidates (.xlsx)",

        data=excel_file,

        file_name="recommended_candidates.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        use_container_width=True

    )

    # ----------------------------------------------------------
    # Candidate Explorer
    # ----------------------------------------------------------

    st.markdown("---")

    st.subheader("🔎 Candidate Explorer")

    selected = st.selectbox(

        "Select Candidate",

        [c["name"] for c in candidates[:10]]

    )

    candidate = next(

        c

        for c in candidates

        if c["name"] == selected

    )

    # ----------------------------------------------------------
    # Candidate Scores
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    matched = len(candidate["matched_skills"])
    missing = len(candidate["missing_skills"])

    total = matched + missing

    coverage = (

        round(

            matched / total * 100,

            1

        )

        if total

        else 100

    )

    with col1:

        st.metric(

            "Overall Score",

            f"{candidate['final_score']*100:.2f}%"

        )

        st.metric(

            "Semantic",

            f"{candidate['semantic_score']*100:.2f}%"

        )

    with col2:

        st.metric(

            "Direct Skills",

            matched

        )

        st.metric(

            "Transferable",

            candidate["num_transferable_matches"]

        )

    with col3:

        st.metric(

            "Skill Coverage",

            f"{coverage}%"

        )

    st.markdown("---")

    # ----------------------------------------------------------
    # Skills
    # ----------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown("### ✅ Direct Skill Matches")

        if candidate["matched_skills"]:

            for skill in candidate["matched_skills"]:

                st.success(skill)

        else:

            st.warning("No direct matches.")

        st.markdown("### ❌ Missing Direct Skills")

        if candidate["missing_skills"]:

            for skill in candidate["missing_skills"]:

                st.error(skill.title())

        else:

            st.success("No missing skills.")

    with right:

        st.markdown("### 🔄 Transferable Skills")

        transfer = candidate.get(

            "transferable_matches",

            []

        )

        if transfer:

            for match in transfer:

                confidence = int(

                    match["confidence"] * 100

                )

                st.info(

                    f"""**{match['candidate_skill'].title()} → {match['required_skill'].title()}**

**Confidence:** {confidence}%

**Reason:** {match['reason']}"""

                )

        else:

            st.success(

                "No transferable skills required."

            )


# ----------------------------------------------------------
# Candidate Intelligence
# ----------------------------------------------------------

def show_insights(results):

    st.markdown("---")

    st.subheader("🧠 AI Candidate Intelligence")

    if results is None:

        st.info(
            "Candidate insights will appear here."
        )

        return

    evaluation = results["evaluation"]

    learning = results["learning"]

    comparison = results["comparison"]

    tab1, tab2, tab3 = st.tabs(

        [

            "💪 Strengths & Gaps",

            "📚 Learning Potential",

            "⚖ Candidate Comparison"

        ]

    )

    # ----------------------------------------------------------
    # Strengths
    # ----------------------------------------------------------

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### ✅ Strengths")

            if evaluation["strengths"]:

                for item in evaluation["strengths"]:

                    st.success(item)

            else:

                st.info(
                    "No significant strengths identified."
                )

        with col2:

            st.markdown("### ❌ Skill Gaps")

            if evaluation["gaps"]:

                for item in evaluation["gaps"]:

                    st.error(item)

            else:

                st.success(
                    "No critical gaps detected."
                )

    # ----------------------------------------------------------
    # Learning
    # ----------------------------------------------------------

    with tab2:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Learning Potential",

                learning["learning_potential"]

            )

            st.metric(

                "Learning Score",

                learning["learning_score"]

            )

        with col2:

            st.markdown("### 📖 AI Explanation")

            if learning["explanation"]:

                for item in learning["explanation"]:

                    st.write(f"• {item}")

            else:

                st.info(
                    "No additional learning insights."
                )

    # ----------------------------------------------------------
    # Comparison
    # ----------------------------------------------------------

    with tab3:

        st.markdown("### 🤖 AI Recommendation")

        st.info(

            comparison["recommendation"]

        )

        st.markdown("### ⭐ Competitive Advantages")

        if comparison["advantages"]:

            for item in comparison["advantages"]:

                st.success(item)

        else:

            st.info(
                "No notable competitive advantages."
            )
            
# ----------------------------------------------------------
# Analytics Dashboard
# ----------------------------------------------------------

from charts import show_all_charts


def show_analytics(results):

    show_all_charts(results)