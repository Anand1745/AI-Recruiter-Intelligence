from src.recruiter_intelligence import RecruiterIntelligence


class RankingEngine:

    def __init__(self):

        self.intelligence = RecruiterIntelligence()

    def rank(
        self,
        semantic_score,
        profile,
        skills,
        parsed_jd
    ):

        # -------------------------
        # Experience
        # -------------------------

        candidate_exp = profile["years_experience"]
        required_exp = parsed_jd["minimum_experience"]

        experience_match = candidate_exp >= required_exp

        experience_bonus = 0.05 if experience_match else -0.05

        # -------------------------
        # Skills
        # -------------------------

        candidate_skills = {
            skill.lower().strip()
            for skill in skills["skills_list"]
        }

        required_skills = {
            skill.lower().strip()
            for skill in parsed_jd["required_skills"]
        }

        matched_skills = candidate_skills & required_skills

        # -------------------------
        # Talent Intelligence
        # -------------------------

        transferable_matches = (
            self.intelligence.infer_transferable_skills(
                candidate_skills,
                required_skills
            )
        )

        transferable_required = {
            match["required_skill"]
            for match in transferable_matches
        }

        missing_skills = (
            required_skills
            - matched_skills
            - transferable_required
        )

        # -------------------------
        # Skill Scores
        # -------------------------

        skill_match = (
            len(matched_skills) / len(required_skills)
            if required_skills else 1.0
        )

        skill_bonus = 0.10 * skill_match

        transferable_bonus = sum(
            0.03 * match["confidence"]
            for match in transferable_matches
        )

        # Prevent transferable skills from outweighing direct matches
        transferable_bonus = min(
            transferable_bonus,
            0.08
        )

        # -------------------------
        # Final Score
        # -------------------------

        final_score = (
            semantic_score
            + experience_bonus
            + skill_bonus
            + transferable_bonus
        )

        final_score = min(final_score, 1.0)

        # -------------------------
        # Return
        # -------------------------

        return {

            "semantic_score": round(
                semantic_score,
                4
            ),

            "experience_match": experience_match,

            "experience_bonus": round(
                experience_bonus,
                4
            ),

            "skill_match": round(
                skill_match,
                4
            ),

            "matched_skills": sorted(
                matched_skills
            ),

            "missing_skills": sorted(
                missing_skills
            ),

            "transferable_matches": transferable_matches,

            "num_transferable_matches": len(
                transferable_matches
            ),

            "transferable_bonus": round(
                transferable_bonus,
                4
            ),

            "final_score": round(
                final_score,
                4
            )

        }