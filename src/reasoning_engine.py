class ReasoningEngine:

    def generate(self, candidate):

        score = candidate["final_score"]

        # ----------------------------------
        # Recommendation
        # ----------------------------------

        if score >= 0.85:
            recommendation = "⭐⭐⭐⭐⭐ Strong Hire"
            confidence = "Very High"

        elif score >= 0.75:
            recommendation = "⭐⭐⭐⭐ Interview"
            confidence = "High"

        elif score >= 0.60:
            recommendation = "⭐⭐⭐ Consider"
            confidence = "Medium"

        else:
            recommendation = "⭐⭐ Reject"
            confidence = "Low"

        strengths = []
        gaps = []

        # ----------------------------------
        # Experience
        # ----------------------------------

        if candidate["experience_match"]:

            strengths.append(
                "Meets required experience."
            )

        else:

            gaps.append(
                "Does not meet the required experience."
            )

        # ----------------------------------
        # Direct Skill Matches
        # ----------------------------------

        if candidate["matched_skills"]:

            strengths.append(

                f"Direct skill matches ({len(candidate['matched_skills'])}): "

                + ", ".join(candidate["matched_skills"])

            )

        # ----------------------------------
        # Transferable Skill Intelligence
        # ----------------------------------

        if candidate["transferable_matches"]:

            for match in candidate["transferable_matches"]:

                if match["category"] == "Cloud":

                    explanation = (
                        "Cloud platform knowledge is highly transferable."
                    )

                elif match["category"] == "Python Web":

                    explanation = (
                        "Python web framework experience suggests a short learning curve."
                    )

                elif match["category"] == "Databases":

                    explanation = (
                        "Relational database concepts are highly transferable."
                    )

                elif match["category"] == "Containers":

                    explanation = (
                        "Containerization experience transfers effectively."
                    )

                elif match["category"] == "ML Frameworks":

                    explanation = (
                        "Deep learning framework experience is transferable."
                    )

                else:

                    explanation = (
                        "Related technical knowledge identified."
                    )

                strengths.append(

                    f"{match['candidate_skill'].title()} → "

                    f"{match['required_skill'].title()} "

                    f"({int(match['confidence'] * 100)}%) - "

                    f"{explanation}"

                )

        # ----------------------------------
        # Missing Skills
        # ----------------------------------

        if candidate["missing_skills"]:

            gaps.append(

                "Missing skills: "

                + ", ".join(candidate["missing_skills"])

            )

        # ----------------------------------
        # Semantic Alignment
        # ----------------------------------

        semantic = candidate["semantic_score"]

        if semantic >= 0.70:

            strengths.append(
                "Excellent semantic alignment with the job description."
            )

        elif semantic >= 0.60:

            strengths.append(
                "Good semantic alignment with the job description."
            )

        else:

            if candidate["num_transferable_matches"] > 0:

                strengths.append(
                    "Transferable technical expertise helps compensate for moderate semantic alignment."
                )

            else:

                gaps.append(
                    "Resume shows limited alignment with the overall job requirements."
                )

        # ----------------------------------
        # Executive Summary
        # ----------------------------------

        summary = (

            f"The candidate achieved an overall match score of "

            f"{score:.2%}. "

            f"The recommendation is based on semantic similarity, "

            f"professional experience, direct skill matches, "

            f"and AI-powered transferable skill intelligence "

            f"to assess both immediate suitability and long-term potential."

        )

        # ----------------------------------
        # Return Evaluation
        # ----------------------------------

        return {

            "candidate_name": candidate["name"],

            "overall_match": round(
                score * 100,
                2
            ),

            "recommendation": recommendation,

            "confidence": confidence,

            "summary": summary,

            "strengths": strengths,

            "gaps": gaps,

            "metrics": {

                "semantic_score": round(
                    semantic * 100,
                    2
                ),

                "skill_match": round(
                    candidate["skill_match"] * 100,
                    2
                ),

                "transferable_matches":
                    candidate[
                        "num_transferable_matches"
                    ],

                "experience_match":
                    candidate[
                        "experience_match"
                    ]

            }

        }