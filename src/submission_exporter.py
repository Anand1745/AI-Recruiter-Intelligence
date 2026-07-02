import csv
import os


class SubmissionExporter:

    def __init__(self, output_dir="submissions"):

        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    # --------------------------------------------------
    # Build Short Reasoning
    # --------------------------------------------------

    def build_reasoning(
        self,
        candidate
    ):

        reasons = []

        # Skills
        matched = candidate.get(
            "matched_skills",
            []
        )

        if matched:

            reasons.append(

                f"Matched {len(matched)} required skill(s)"

            )

        # Experience
        if candidate.get(
            "experience_match",
            False
        ):

            reasons.append(
                "Meets experience requirement"
            )

        # Transferable Skills
        transfer = candidate.get(
            "num_transferable_matches",
            0
        )

        if transfer:

            reasons.append(

                f"{transfer} transferable skill(s)"

            )

        # Behavioral Intelligence
        behavior = candidate.get(
            "behavior_score",
            0
        )

        if behavior >= 0.75:

            reasons.append(
                "Strong behavioral signals"
            )

        elif behavior >= 0.50:

            reasons.append(
                "Good recruiter engagement"
            )

        # Semantic
        semantic = candidate.get(
            "semantic_score",
            0
        )

        if semantic >= 0.80:

            reasons.append(
                "Excellent semantic alignment"
            )

        elif semantic >= 0.60:

            reasons.append(
                "Good semantic alignment"
            )

        if not reasons:

            reasons.append(
                "General profile match"
            )

        return "; ".join(reasons)

    # --------------------------------------------------
    # Export CSV
    # --------------------------------------------------

    def export(
        self,
        ranked_candidates,
        filename="submission.csv",
        top_k=100
    ):

        filepath = os.path.join(
            self.output_dir,
            filename
        )

        with open(
            filepath,
            "w",
            newline="",
            encoding="utf-8"
        ) as csvfile:

            writer = csv.writer(csvfile)

            writer.writerow(

                [
                    "candidate_id",
                    "rank",
                    "score",
                    "reasoning"
                ]

            )

            for rank, candidate in enumerate(

                ranked_candidates[:top_k],

                start=1

            ):

                writer.writerow(

                    [

                        candidate["candidate_id"],

                        rank,

                        round(
                            candidate["final_score"],
                            6
                        ),

                        candidate.get(
                            "submission_reasoning",
                            self.build_reasoning(candidate)
                        )

                    ]

                )

        return filepath