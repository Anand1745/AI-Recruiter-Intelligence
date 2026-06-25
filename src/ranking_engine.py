class RankingEngine:

    def rank(
        self,
        semantic_score,
        profile,
        skills,
        parsed_jd
    ):

        score = semantic_score

        candidate_exp = profile["years_experience"]
        required_exp = parsed_jd["minimum_experience"]

        if candidate_exp >= required_exp:
            score += 0.05
        else:
            score -= 0.05

        candidate_skills = {
            s.lower()
            for s in skills["skills_list"]
        }

        required_skills = {
            s.lower()
            for s in parsed_jd["required_skills"]
        }

        matched = len(candidate_skills & required_skills)

        if len(required_skills) > 0:
            score += 0.10 * matched / len(required_skills)

        return round(min(score, 1.0), 4)