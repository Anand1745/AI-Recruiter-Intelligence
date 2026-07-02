class ProfileValidator:

    # --------------------------------------------------
    # Profile Consistency Score
    # --------------------------------------------------

    def evaluate(
        self,
        profile,
        skills,
        redrob
    ):

        risk = 0.0
        reasons = []

        years = profile.get(
            "years_experience",
            0
        )

        title = (
            profile.get(
                "current_title",
                ""
            ).lower()
        )

        num_skills = skills.get(
            "num_skills",
            0
        )

        profile_score = max(
            redrob.get(
                "profile_score",
                0
            ),
            0
        )

        recruiter_rate = max(
            redrob.get(
                "recruiter_response_rate",
                0
            ),
            0
        )

        interview_rate = max(
            redrob.get(
                "interview_completion_rate",
                0
            ),
            0
        )

        offer_rate = max(
            redrob.get(
                "offer_acceptance_rate",
                0
            ),
            0
        )

        github = max(
            redrob.get(
                "github_score",
                0
            ),
            0
        )

        # ----------------------------------------
        # Seniority vs Experience
        # ----------------------------------------

        if any(

            word in title

            for word in [

                "principal",

                "staff",

                "lead",

                "architect"

            ]

        ) and years < 4:

            risk += 0.20

            reasons.append(

                "Senior title inconsistent with experience"

            )

        # ----------------------------------------
        # Skill Inflation
        # ----------------------------------------

        if years < 2 and num_skills > 30:

            risk += 0.15

            reasons.append(

                "Very large skill set for limited experience"

            )

        # ----------------------------------------
        # Sparse Profile
        # ----------------------------------------

        if profile_score < 30:

            risk += 0.10

            reasons.append(

                "Low profile completeness"

            )

        # ----------------------------------------
        # Recruiter Signals
        # ----------------------------------------

        if recruiter_rate > 0.90 and profile_score < 20:

            risk += 0.10

            reasons.append(

                "Recruiter engagement unusually high"

            )

        # ----------------------------------------
        # Interview vs Offer
        # ----------------------------------------

        if (

            interview_rate < 0.20

            and

            offer_rate > 0.90

        ):

            risk += 0.10

            reasons.append(

                "Offer acceptance inconsistent"

            )

        # ----------------------------------------
        # GitHub
        # ----------------------------------------

        if github > 90 and years == 0:

            risk += 0.05

            reasons.append(

                "Exceptional GitHub activity without experience"

            )

        # ----------------------------------------

        risk = min(
            risk,
            1.0
        )

        consistency = round(
            1.0 - risk,
            4
        )

        return {

            "risk_score": round(
                risk,
                4
            ),

            "consistency_score": consistency,

            "reasons": reasons

        }