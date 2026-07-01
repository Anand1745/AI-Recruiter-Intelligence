import io
import pandas as pd


def generate_excel(results):

    candidates = results["ranked_candidates"]

    rows = []

    for rank, candidate in enumerate(candidates, start=1):

        score = round(candidate["final_score"] * 100, 2)

        if score >= 80:
            recommendation = "Strong Hire"
        elif score >= 65:
            recommendation = "Interview"
        elif score >= 50:
            recommendation = "Consider"
        else:
            recommendation = "Reject"

        rows.append({

            "Rank": rank,

            "Candidate": candidate["name"],

            "Overall Match (%)": score,

            "Semantic Score (%)": round(
                candidate["semantic_score"] * 100,
                2
            ),

            "Matched Skills": ", ".join(
                candidate["matched_skills"]
            ),

            "Transferable Skills": candidate[
                "num_transferable_matches"
            ],

            "Recommendation": recommendation

        })

    df = pd.DataFrame(rows)

    output = io.BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Rankings"

        )

    return output.getvalue()