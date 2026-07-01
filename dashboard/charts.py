import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ----------------------------------------------------------
# Helper
# ----------------------------------------------------------

def create_dataframe(results):
    """
    Convert ranked candidates into a dataframe
    for Plotly charts.
    """

    rows = []

    for candidate in results["ranked_candidates"]:

        recommendation = "Reject"

        score = candidate["final_score"]

        if score >= 0.80:
            recommendation = "Strong Hire"

        elif score >= 0.70:
            recommendation = "Interview"

        elif score >= 0.50:
            recommendation = "Consider"
            
        else:
            recommendation = "Reject"

        rows.append(

            {

                "Candidate": candidate["name"],

                "Final Score": round(score * 100, 2),

                "Semantic Score": round(
                    candidate["semantic_score"] * 100,
                    2
                ),

                "Skill Match": round(
                    candidate["skill_match"] * 100,
                    2
                ),

                "Transferable Skills":
                    candidate["num_transferable_matches"],

                "Recommendation": recommendation

            }

        )

    return pd.DataFrame(rows)


# ----------------------------------------------------------
# Chart 1
# Match Score Distribution
# ----------------------------------------------------------

def score_distribution(results):

    st.subheader("📊 Candidate Match Score Distribution")

    df = create_dataframe(results)

    fig = px.histogram(

        df,

        x="Final Score",

        nbins=10,

        title="Distribution of Final Match Scores"

    )

    fig.update_layout(

        height=400,

        xaxis_title="Final Match Score (%)",

        yaxis_title="Number of Candidates"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ----------------------------------------------------------
# Chart 2
# Semantic vs Final Score
# ----------------------------------------------------------

def semantic_vs_final(results):

    st.subheader("🎯 Semantic Score vs Final Score")

    df = create_dataframe(results)

    fig = px.scatter(

        df,

        x="Semantic Score",

        y="Final Score",

        color="Recommendation",

        hover_data={
            "Final Score": True,
            "Semantic Score": True,
            "Transferable Skills": True,
            "Recommendation": True
        },

        size="Transferable Skills",

        title="Semantic Similarity vs Overall Ranking"

    )

    fig.update_layout(

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ----------------------------------------------------------
# Chart 3
# Recommendation Distribution
# ----------------------------------------------------------

def recommendation_chart(results):

    st.subheader("🥧 Recommendation Distribution")

    df = create_dataframe(results)

    chart = (

        df["Recommendation"]

        .value_counts()

        .reset_index()

    )

    chart.columns = [

        "Recommendation",

        "Count"

    ]

    fig = px.pie(

        chart,

        values="Count",

        names="Recommendation",

        hole=0.45,

        title="Candidate Recommendation Breakdown"

    )

    fig.update_layout(

        height=450

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )
# ----------------------------------------------------------
# Chart 4
# Learning Potential Distribution
# ----------------------------------------------------------

def learning_chart(results):

    st.subheader("📈 Learning Potential")

    learning = results["learning"]

    fig = go.Figure()

    fig.add_trace(

        go.Indicator(

            mode="gauge+number",

            value=learning["learning_score"],

            title={"text": "Learning Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "bar": {"color": "#2563EB"},

                "steps": [

                    {"range": [0, 40], "color": "#FECACA"},

                    {"range": [40, 70], "color": "#FDE68A"},

                    {"range": [70, 100], "color": "#BBF7D0"}

                ]

            }

        )

    )

    fig.update_layout(

        height=400

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ----------------------------------------------------------
# Chart 5
# Transferable Skills
# ----------------------------------------------------------

def transferable_chart(results):

    st.subheader("🔄 Transferable Skills")

    df = create_dataframe(results)

    top = (

        df

        .sort_values(

            "Transferable Skills",

            ascending=False

        )

        .head(10)

    )

    fig = px.bar(

        top,

        x="Candidate",

        y="Transferable Skills",

        color="Transferable Skills",

        title="Top Candidates by Transferable Skills"

    )

    fig.update_layout(

        height=450,

        xaxis_title="Candidate",

        yaxis_title="Transferable Skills"

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ----------------------------------------------------------
# Dashboard Analytics
# ----------------------------------------------------------

def show_all_charts(results):

    st.markdown("---")

    st.subheader("📈 AI Analytics Dashboard")

    if results is None:

        st.info(

            "Run an analysis to generate analytics."

        )

        return

    col1, col2 = st.columns(2)

    with col1:

        score_distribution(results)

    with col2:

        recommendation_chart(results)

    col3, col4 = st.columns(2)

    with col3:

        semantic_vs_final(results)

    with col4:

        transferable_chart(results)

    learning_chart(results)