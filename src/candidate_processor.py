class CandidateProcessor:

    def process_profile(self, candidate):
        profile = candidate.get("profile", {})

        return {
            "candidate_id": candidate.get("candidate_id"),
            "name": profile.get("anonymized_name"),
            "headline": profile.get("headline"),
            "summary": profile.get("summary"),
            "location": profile.get("location"),
            "country": profile.get("country"),
            "years_experience": profile.get("years_of_experience"),
            "current_title": profile.get("current_title"),
            "current_company": profile.get("current_company"),
            "industry": profile.get("current_industry"),
        }

    def process_skills(self, candidate):

        skills = [
            s["name"]
            for s in candidate.get("skills", [])
        ]

        return {
            "skills_list": skills,
            "skills_text": " ".join(skills),
            "num_skills": len(skills)
        }
    

    def process_education(self, candidate):
        education = candidate.get("education", [])

        degrees = []

        for e in education:
            degree = e.get("degree")
            if degree:
                degrees.append(degree)

        return degrees

    def process_certifications(self, candidate):
        certs = candidate.get("certifications", [])

        return [
            c.get("name")
            for c in certs
            if c.get("name")
        ]
        
    def process_redrob(self, candidate):
        signals = candidate.get("redrob_signals", {})

        return {
            "profile_score":
                signals.get("profile_completeness_score"),

            "recruiter_response_rate":
                signals.get("recruiter_response_rate"),

            "github_score":
                signals.get("github_activity_score"),

            "connection_count":
                signals.get("connection_count"),

            "interview_completion_rate":
                signals.get("interview_completion_rate"),

            "offer_acceptance_rate":
                signals.get("offer_acceptance_rate"),
        }