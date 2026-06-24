class FeatureEngineer:

    def create_features(
        self,
        profile,
        skills,
        education,
        certs,
        redrob
    ):
        return {
            **profile,

            "num_skills": len(skills),
            "skills_text": " ".join(skills),

            "num_degrees": len(education),
            "education_text": " ".join(education),

            "num_certifications": len(certs),

            **redrob
        }