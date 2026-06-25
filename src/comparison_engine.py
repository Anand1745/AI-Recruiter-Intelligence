class ComparisonEngine:

    def compare(self, candidate1, candidate2):

        comparison = {

            "candidate_1": candidate1["name"],
            "candidate_2": candidate2["name"],
            "winner": None,
            "score_difference": round(
                abs(candidate1["final_score"] - candidate2["final_score"]),
                4
            ),
            "advantages": [],
            "recommendation": ""

        }

        if candidate1["final_score"] > candidate2["final_score"]:
            comparison["winner"] = candidate1["name"]
        else:
            comparison["winner"] = candidate2["name"]

        if (
            candidate1["experience_match"]
            and
            not candidate2["experience_match"]
        ):

            comparison["advantages"].append(
                f"{candidate1['name']} meets the required experience."
            )

        elif (
            candidate2["experience_match"]
            and
            not candidate1["experience_match"]
        ):

            comparison["advantages"].append(
                f"{candidate2['name']} meets the required experience."
            )

        if candidate1["skill_match"] > candidate2["skill_match"]:

            comparison["advantages"].append(
                f"{candidate1['name']} matches more required skills."
            )

        elif candidate2["skill_match"] > candidate1["skill_match"]:

            comparison["advantages"].append(
                f"{candidate2['name']} matches more required skills."
            )

        if candidate1["semantic_score"] > candidate2["semantic_score"]:

            comparison["advantages"].append(
                f"{candidate1['name']} has better semantic alignment."
            )

        elif candidate2["semantic_score"] > candidate1["semantic_score"]:

            comparison["advantages"].append(
                f"{candidate2['name']} has better semantic alignment."
            )

        comparison["recommendation"] = (
            f"Recommend interviewing "
            f"{comparison['winner']} first."
        )

        return comparison