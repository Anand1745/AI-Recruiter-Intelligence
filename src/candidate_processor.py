class CandidateProcessor:

    # --------------------------------------------------
    # Profile
    # --------------------------------------------------

    def process_profile(self, candidate):

        profile = candidate.get("profile", {})

        return {

            "name": profile.get("anonymized_name"),

            "headline": profile.get("headline"),

            "summary": profile.get("summary"),

            "location": profile.get("location"),

            "country": profile.get("country"),

            "years_experience": profile.get(
                "years_of_experience",
                0
            ),

            "current_title": profile.get(
                "current_title"
            ),

            "current_company": profile.get(
                "current_company"
            ),

            "industry": profile.get(
                "current_industry"
            )

        }

    # --------------------------------------------------
    # Skills
    # --------------------------------------------------

    def process_skills(self, candidate):

        skills = [

            s["name"]

            for s in candidate.get(
                "skills",
                []
            )

        ]

        return {

            "skills_list": skills,

            "skills_text": " ".join(skills),

            "num_skills": len(skills)

        }

    # --------------------------------------------------
    # Education
    # --------------------------------------------------

    def process_education(self, candidate):

        education = candidate.get(
            "education",
            []
        )

        degrees = []

        for e in education:

            degree = e.get("degree")

            if degree:

                degrees.append(degree)

        return degrees

    # --------------------------------------------------
    # Certifications
    # --------------------------------------------------

    def process_certifications(self, candidate):

        certs = candidate.get(
            "certifications",
            []
        )

        return [

            c.get("name")

            for c in certs

            if c.get("name")

        ]

    # --------------------------------------------------
    # Redrob Behavioral Signals
    # --------------------------------------------------

    def process_redrob(self, candidate):

        signals = candidate.get(
            "redrob_signals",
            {}
        )

        return {

            "profile_score":
                signals.get(
                    "profile_completeness_score",
                    0
                ),

            "recruiter_response_rate":
                signals.get(
                    "recruiter_response_rate",
                    0
                ),

            "github_score":
                signals.get(
                    "github_activity_score",
                    -1
                ),

            "connection_count":
                signals.get(
                    "connection_count",
                    0
                ),

            "interview_completion_rate":
                signals.get(
                    "interview_completion_rate",
                    0
                ),

            "offer_acceptance_rate":
                signals.get(
                    "offer_acceptance_rate",
                    -1
                ),

            # -------- Added --------

            "open_to_work":
                signals.get(
                    "open_to_work_flag",
                    False
                ),

            "last_active_date":
                signals.get(
                    "last_active_date",
                    None
                )

        }