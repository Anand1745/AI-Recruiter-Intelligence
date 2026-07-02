import streamlit as st
import pandas as pd
from exporter import generate_excel
from docx import Document


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

                # TXT
                if uploaded_file.type == "text/plain":

                    job_description = uploaded_file.read().decode("utf-8")

                    st.success("TXT file loaded successfully.")

                # DOCX
                elif (
                    uploaded_file.type
                    == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ):

                    document = Document(uploaded_file)

                    job_description = "\n".join(

                        paragraph.text

                        for paragraph in document.paragraphs

                    )

                    st.success("DOCX file loaded successfully.")

                else:

                    st.error("Unsupported file format.")

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
            float(evaluation["overall_match"]) / 100
        )

        # ==================================================
        # Core Metrics
        # ==================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Overall Match",
                f"{evaluation['overall_match']:.2f}%"
            )

            st.metric(
                "Semantic",
                f"{top['semantic_score']*100:.1f}%"
            )

            st.metric(
                "Recommendation",
                evaluation["recommendation"]
            )

        with col2:

            st.metric(
                "Production",
                f"{top.get('production_score',0)*100:.1f}%"
            )

            st.metric(
                "Behavior",
                f"{top['behavior_score']*100:.1f}%"
            )

            st.metric(
                "Confidence",
                evaluation["confidence"]
            )

        with col3:

            st.metric(
                "Profile Consistency",
                f"{top.get('profile_consistency',1)*100:.1f}%"
            )

            st.metric(
                "Transferable Skills",
                top["num_transferable_matches"]
            )

            st.metric(
                "Direct Skills",
                len(top["matched_skills"])
            )

        # ==================================================
        # Recommendation Banner
        # ==================================================

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

        # ==================================================
        # Matched Skills
        # ==================================================

        st.markdown("---")

        left, right = st.columns(2)

        with left:

            st.markdown("### ✅ Direct Skill Matches")

            if top["matched_skills"]:

                for skill in top["matched_skills"]:

                    st.success(skill.title())

            else:

                st.info("No direct matches.")

        with right:

            st.markdown("### ❌ Missing Skills")

            if top["missing_skills"]:

                for skill in top["missing_skills"]:

                    st.error(skill.title())

            else:

                st.success("No missing skills.")

        # ==================================================
        # Production Evidence
        # ==================================================

        evidence = top.get(
            "production_evidence",
            []
        )

        if evidence:

            st.markdown("---")

            st.markdown("### 🚀 Production AI Experience")

            cols = st.columns(min(4, len(evidence)))

            for i, item in enumerate(evidence[:8]):

                cols[i % len(cols)].info(item.title())

        # ==================================================
        # AI Decision Summary
        # ==================================================

        st.markdown("---")

        st.subheader("🧠 AI Decision Summary")

        for item in evaluation["strengths"][:6]:

            st.write(f"✅ {item}")

        # ==================================================
        # Submission Reasoning
        # ==================================================

        st.markdown("---")

        st.subheader("📝 Recruiter Summary")

        st.info(
            evaluation["submission_reasoning"]
        )

# ----------------------------------------------------------
# KPI Cards
# ----------------------------------------------------------

def show_metrics(results):

    st.markdown("---")

    st.subheader("📊 Recruiter Intelligence Dashboard")

    if results is None:

        st.info(
            "Metrics will appear after analysis."
        )

        return

    ranked = results["ranked_candidates"]
    evaluation = results["evaluation"]
    top = ranked[0]

    # ----------------------------------------------------------
    # First Row
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Candidates Ranked",
            f"{len(ranked):,}"
        )

    with col2:

        st.metric(
            "Overall Match",
            f"{evaluation['overall_match']:.2f}%"
        )

    with col3:

        st.metric(
            "Recommendation",
            evaluation["recommendation"]
        )

    # ----------------------------------------------------------
    # Second Row
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Semantic Score",
            f"{top['semantic_score']*100:.1f}%"
        )

    with col2:

        st.metric(
            "Skill Match",
            f"{top['skill_match']*100:.1f}%"
        )

    with col3:

        st.metric(
            "Experience",
            "✓ Yes" if top["experience_match"] else "✗ No"
        )

    # ----------------------------------------------------------
    # Third Row
    # ----------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Production Score",
            f"{top.get('production_score',0)*100:.1f}%"
        )

    with col2:

        st.metric(
            "Behavior Score",
            f"{top['behavior_score']*100:.1f}%"
        )

    with col3:

        st.metric(
            "Profile Consistency",
            f"{top.get('profile_consistency',1)*100:.1f}%"
        )

    # ----------------------------------------------------------
    # Fourth Row
    # ----------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Transferable Skills",
            top["num_transferable_matches"]
        )

    with col2:

        matched = len(top["matched_skills"])
        missing = len(top["missing_skills"])

        total = matched + missing

        coverage = (
            matched / total * 100
            if total
            else 100
        )

        st.metric(
            "Skill Coverage",
            f"{coverage:.1f}%"
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

    recommendations = {
        "Strong Hire": "🟢",
        "Interview": "🔵",
        "Consider": "🟡",
        "Review": "🟠",
        "Reject": "🔴"
    }

    for index, candidate in enumerate(candidates[:10], start=1):

        matched = len(candidate["matched_skills"])
        missing = len(candidate["missing_skills"])

        total = matched + missing

        coverage = (
            round(matched / total * 100, 1)
            if total
            else 100
        )

        if candidate["final_score"] >= 0.85:
            recommendation = "Strong Hire"

        elif candidate["final_score"] >= 0.75:
            recommendation = "Interview"

        elif candidate["final_score"] >= 0.65:
            recommendation = "Consider"

        elif candidate["final_score"] >= 0.50:
            recommendation = "Review"

        else:
            recommendation = "Reject"

        rows.append({

            "Rank": index,

            "Candidate": candidate["name"],

            "Overall": round(
                candidate["final_score"] * 100,
                2
            ),

            "Semantic": round(
                candidate["semantic_score"] * 100,
                1
            ),

            "Production": round(
                candidate.get(
                    "production_score",
                    0
                ) * 100,
                1
            ),

            "Behavior": round(
                candidate["behavior_score"] * 100,
                1
            ),

            "Consistency": round(
                candidate.get(
                    "profile_consistency",
                    1
                ) * 100,
                1
            ),

            "Coverage": coverage,

            "Transfer": candidate[
                "num_transferable_matches"
            ],

            "Recommendation":
                recommendations[
                    recommendation
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

    # ==========================================================
    # Score Cards
    # ==========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Overall",
            f"{candidate['final_score']*100:.2f}%"
        )

        st.metric(
            "Semantic",
            f"{candidate['semantic_score']*100:.2f}%"
        )

        st.metric(
            "Production",
            f"{candidate.get('production_score',0)*100:.2f}%"
        )

    with col2:

        st.metric(
            "Behavior",
            f"{candidate['behavior_score']*100:.2f}%"
        )

        st.metric(
            "Consistency",
            f"{candidate.get('profile_consistency',1)*100:.2f}%"
        )

        st.metric(
            "Transferable",
            candidate["num_transferable_matches"]
        )

    with col3:

        st.metric(
            "Direct Skills",
            len(candidate["matched_skills"])
        )

        st.metric(
            "Missing Skills",
            len(candidate["missing_skills"])
        )

        st.metric(
            "Experience",
            "✓"
            if candidate["experience_match"]
            else "✗"
        )

    st.markdown("---")

    left, right = st.columns(2)

    with left:

        st.markdown("### ✅ Direct Skill Matches")

        if candidate["matched_skills"]:

            for skill in candidate["matched_skills"]:

                st.success(skill.title())

        else:

            st.info("No direct matches.")

        st.markdown("### ❌ Missing Skills")

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

                st.info(

                    f"{match['candidate_skill'].title()} → "

                    f"{match['required_skill'].title()} "

                    f"({int(match['confidence']*100)}%)"

                )

        else:

            st.success(
                "No transferable skills."
            )

        evidence = candidate.get(
            "production_evidence",
            []
        )

        if evidence:

            st.markdown("### 🚀 Production Evidence")

            for item in evidence:

                st.success(item.title())

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

    tab1, tab2, tab3, tab4, tab5 = st.tabs(

        [

            "💪 Strengths & Gaps",

            "📚 Learning",

            "⚖ Comparison",

            "🧠 Recruiter Intelligence",

            "🛡 Profile Validation"

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

                f"{learning['learning_score']:.2f}"

            )

        with col2:

            st.markdown("### AI Explanation")
            
            if learning.get("explanation"):

                for item in learning["explanation"]:

                    st.write(f"• {item}")

            else:

                st.info("No learning insights available.")

    # ----------------------------------------------------------
    # Comparison
    # ----------------------------------------------------------

    with tab3:

        if comparison is None:

            st.info("Only one candidate available.")

        else:

            st.markdown("### AI Recommendation")

            st.info(
                comparison["recommendation"]
            )

            st.markdown("### Competitive Advantages")

            if comparison["advantages"]:

                for item in comparison["advantages"]:

                    st.success(item)

            else:

                st.info(
                    "No major competitive advantages."
                )

    with tab4:

        top = results["ranked_candidates"][0]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(

                "Production Score",

                f"{top.get('production_score',0)*100:.1f}%"

            )

        with col2:

            st.metric(

                "Behavior Score",

                f"{top.get('behavior_score', 0)*100:.1f}%"

            )

        with col3:

            st.metric(

                "Profile Consistency",

                f"{top.get('profile_consistency',1)*100:.1f}%"

            )

        st.markdown("---")

        evidence = top.get(

            "production_evidence",

            []

        )

        st.markdown("### 🚀 Production Experience")

        if evidence:

            cols = st.columns(

                min(4, len(evidence))

            )

            for i, item in enumerate(evidence):

                cols[i % len(cols)].success(

                    item.title()

                )

        else:

            st.info(

                "No production indicators detected."

            )

        st.markdown("---")

        st.markdown("### 📝 Recruiter Summary")

        st.info(

            evaluation["submission_reasoning"]

        )

    with tab5:

        top = results["ranked_candidates"][0]

        st.metric(

            "Consistency",

            f"{top.get('profile_consistency',1)*100:.1f}%"

        )

        st.metric(

            "Risk",

            f"{top.get('profile_risk',0)*100:.1f}%"

        )

        validation = top.get(

            "profile_validation",

            []

        )

        if validation:

            st.markdown("### Validation Findings")

            for item in validation:

                st.warning(item)

        else:

            st.success(

                "No profile consistency concerns detected."

            )       
                     
# ----------------------------------------------------------
# Analytics Dashboard
# ----------------------------------------------------------

from charts import show_all_charts


def show_analytics(results):

    show_all_charts(results)