class ComparisonEngine:

    def compare(
        self,
        candidate_a,
        candidate_b
    ):

        advantages = []

        # ---------------------------------------
        # Overall Winner
        # ---------------------------------------

        if candidate_a["final_score"] >= candidate_b["final_score"]:

            winner = candidate_a

        else:

            winner = candidate_b

        # ---------------------------------------
        # Semantic Similarity
        # ---------------------------------------

        if candidate_a["semantic_score"] > candidate_b["semantic_score"]:

            advantages.append(

                f"{candidate_a['name']} has stronger semantic alignment."

            )

        elif candidate_b["semantic_score"] > candidate_a["semantic_score"]:

            advantages.append(

                f"{candidate_b['name']} has stronger semantic alignment."

            )

        # ---------------------------------------
        # Direct Skill Match
        # ---------------------------------------

        if candidate_a["skill_match"] > candidate_b["skill_match"]:

            advantages.append(

                f"{candidate_a['name']} matches more required skills."

            )

        elif candidate_b["skill_match"] > candidate_a["skill_match"]:

            advantages.append(

                f"{candidate_b['name']} matches more required skills."

            )

        # ---------------------------------------
        # Experience
        # ---------------------------------------

        if (
            candidate_a["experience_match"]
            and
            not candidate_b["experience_match"]
        ):

            advantages.append(

                f"{candidate_a['name']} satisfies the required experience."

            )

        elif (
            candidate_b["experience_match"]
            and
            not candidate_a["experience_match"]
        ):

            advantages.append(

                f"{candidate_b['name']} satisfies the required experience."

            )

        # ---------------------------------------
        # Talent Intelligence
        # ---------------------------------------

        if (
            candidate_a["num_transferable_matches"]
            >
            candidate_b["num_transferable_matches"]
        ):

            advantages.append(

                f"{candidate_a['name']} demonstrates stronger transferable technical skills."

            )

        elif (
            candidate_b["num_transferable_matches"]
            >
            candidate_a["num_transferable_matches"]
        ):

            advantages.append(

                f"{candidate_b['name']} demonstrates stronger transferable technical skills."

            )

        # ---------------------------------------
        # Final Recommendation
        # ---------------------------------------

        recommendation = (

            f"Recommend interviewing "

            f"{winner['name']} first based on the "

            f"highest overall evaluation score."

        )
        
        advantages.insert(

            0,

            "Highest overall candidate score."

        )

        return {

            "winner": winner["name"],

            "winner_score": round(
                winner["final_score"] * 100,
                2
            ),

            "recommendation": recommendation,

            "advantages": advantages

        }