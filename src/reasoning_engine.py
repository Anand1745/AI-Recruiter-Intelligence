class ReasoningEngine:

    def generate(self, candidate):

        score = candidate["final_score"]

        # Recommendation
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

        # Experience
        if candidate["experience_match"]:
            strengths.append("Meets required experience")
        else:
            gaps.append("Does not meet required experience")

        # Skills
        if candidate["matched_skills"]:
            strengths.append(
                f"Matched {len(candidate['matched_skills'])} required skill(s): "
                + ", ".join(candidate["matched_skills"])
            )

        if candidate["missing_skills"]:
            gaps.append(
                f"Missing {len(candidate['missing_skills'])} required skill(s): "
                + ", ".join(candidate["missing_skills"])
            )

        # Semantic
        semantic = candidate["semantic_score"]

        if semantic >= 0.70:
            strengths.append("Excellent semantic alignment with job description")
        elif semantic >= 0.60:
            strengths.append("Good semantic alignment with job description")
        else:
            gaps.append("Weak semantic alignment with job description")

        summary = (
            f"The candidate achieved an overall match score of "
            f"{score:.2%}. Based on semantic relevance, "
            f"experience and technical skills, the recommendation "
            f"is '{recommendation}'."
        )

        return {

            "candidate_name": candidate["name"],

            "overall_match": round(score * 100, 2),

            "recommendation": recommendation,

            "confidence": confidence,

            "summary": summary,

            "strengths": strengths,

            "gaps": gaps,

            "metrics": {

                "semantic_score": round(
                    candidate["semantic_score"] * 100,
                    2
                ),

                "skill_match": round(
                    candidate["skill_match"] * 100,
                    2
                ),

                "experience_match":
                    candidate["experience_match"]

            }

        }