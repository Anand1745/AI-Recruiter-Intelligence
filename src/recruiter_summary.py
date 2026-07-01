class RecruiterSummaryGenerator:

    def generate(self, candidate, evaluation, learning):

        summary = {}

        summary["candidate"] = candidate["name"]

        summary["overall_match"] = round(candidate["final_score"] * 100, 2)

        summary["recommendation"] = evaluation["recommendation"]

        summary["confidence"] = evaluation["confidence"]

        # ----------------------------------------------------
        # Overall Assessment
        # ----------------------------------------------------

        strengths = []

        if candidate["matched_skills"]:
            strengths.append(
                f"Matches {len(candidate['matched_skills'])} required technical skill(s)."
            )

        if candidate["num_transferable_matches"] > 0:
            strengths.append(
                f"Possesses {candidate['num_transferable_matches']} transferable skills."
            )

        if candidate["semantic_score"] > 0.60:
            strengths.append(
                "Resume shows strong semantic alignment with the job description."
            )
        elif candidate["semantic_score"] > 0.45:
            strengths.append(
                "Resume demonstrates moderate semantic similarity."
            )
        else:
            strengths.append(
                "Semantic similarity is below ideal."
            )

        summary["assessment"] = strengths

        # ----------------------------------------------------
        # Hiring Risk
        # ----------------------------------------------------

        score = candidate["final_score"]

        if score >= 0.80:
            risk = "Very Low"

        elif score >= 0.65:
            risk = "Low"

        elif score >= 0.50:
            risk = "Medium"

        else:
            risk = "High"

        summary["risk"] = risk

        # ----------------------------------------------------
        # Learning Curve
        # ----------------------------------------------------

        lp = learning["learning_potential"]

        if lp == "Very High":
            curve = "2-4 Weeks"

        elif lp == "High":
            curve = "1-2 Months"

        elif lp == "Medium":
            curve = "2-3 Months"

        else:
            curve = "Long"

        summary["learning_curve"] = curve

        # ----------------------------------------------------
        # Interview Recommendation
        # ----------------------------------------------------

        if score >= 0.80:

            decision = (
                "Proceed directly to the final interview."
            )

        elif score >= 0.65:

            decision = (
                "Schedule a technical interview."
            )

        elif score >= 0.50:

            decision = (
                "Consider after evaluating stronger candidates."
            )

        else:

            decision = (
                "Do not proceed."
            )

        summary["decision"] = decision

        return summary