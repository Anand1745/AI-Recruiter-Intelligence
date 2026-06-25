class RankingEngine:

    def rank(
        self,
        semantic_score,
        profile,
        skills,
        parsed_jd
    ):

        candidate_exp = profile["years_experience"]
        required_exp = parsed_jd["minimum_experience"]

        experience_match = candidate_exp >= required_exp

        experience_bonus = 0.05 if experience_match else -0.05

        candidate_skills = {
            s.lower()
            for s in skills["skills_list"]
        }

        required_skills = {
            s.lower()
            for s in parsed_jd["required_skills"]
        }

        matched_skills = candidate_skills & required_skills
        missing_skills = required_skills - candidate_skills

        skill_match = (
            len(matched_skills) / len(required_skills)
            if required_skills else 1.0
        )

        skill_bonus = 0.10 * skill_match

        final_score = (
            semantic_score +
            experience_bonus +
            skill_bonus
        )

        final_score = min(final_score, 1.0)

        return {

            "semantic_score": round(semantic_score, 4),

            "experience_match": experience_match,

            "experience_bonus": round(experience_bonus, 4),

            "skill_match": round(skill_match, 4),

            "matched_skills": sorted(matched_skills),

            "missing_skills": sorted(missing_skills),

            "final_score": round(final_score, 4)

        }