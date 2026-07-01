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

        # ---------------------------------------------------
        # Experience
        # ---------------------------------------------------

        candidate_exp = profile["years_experience"]
        required_exp = parsed_jd["minimum_experience"]

        experience_match = candidate_exp >= required_exp
        experience_score = 1.0 if experience_match else 0.0

        # ---------------------------------------------------
        # Skills
        # ---------------------------------------------------

        candidate_skills = {
            skill.lower().strip()
            for skill in skills["skills_list"]
        }

        required_skills = {
            skill.lower().strip()
            for skill in parsed_jd["required_skills"]
        }

        matched_skills = candidate_skills & required_skills

        # ---------------------------------------------------
        # Transferable Skills
        # ---------------------------------------------------

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

        # ---------------------------------------------------
        # Skill Match
        # ---------------------------------------------------

        if required_skills:

            effective_matches = (
                len(matched_skills)
                + 0.6 * len(transferable_matches)
            )

            skill_match = min(
                effective_matches / len(required_skills),
                1.0
            )

        else:

            skill_match = 1.0

        # ---------------------------------------------------
        # Transferable Bonus
        # ---------------------------------------------------

        transferable_bonus = sum(
            0.01 * match["confidence"]
            for match in transferable_matches
        )

        transferable_bonus = min(
            transferable_bonus,
            0.05
        )

        # ---------------------------------------------------
        # Weighted Components
        # ---------------------------------------------------

        semantic_component = semantic_score * 0.35

        skill_component = skill_match * 0.50

        experience_component = experience_score * 0.10

        transfer_component = transferable_bonus

        # ---------------------------------------------------
        # Final Score
        # ---------------------------------------------------

        final_score = (
            semantic_component
            + skill_component
            + experience_component
            + transfer_component
        )

        final_score = min(final_score, 1.0)

        # ---------------------------------------------------
        # Return
        # ---------------------------------------------------

        return {

            "semantic_score": round(
                semantic_score,
                4
            ),

            "experience_match": experience_match,

            "experience_score": round(
                experience_score,
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

            "semantic_component": round(
                semantic_component,
                4
            ),

            "skill_component": round(
                skill_component,
                4
            ),

            "experience_component": round(
                experience_component,
                4
            ),

            "transfer_component": round(
                transfer_component,
                4
            ),

            "final_score": round(
                final_score,
                4
            )

        }