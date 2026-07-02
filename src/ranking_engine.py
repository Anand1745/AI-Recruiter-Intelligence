from datetime import datetime

from src.recruiter_intelligence import RecruiterIntelligence
from src.profile_validator import ProfileValidator
from src.production_experience import ProductionExperienceScorer



class RankingEngine:

    def __init__(self):
        self.intelligence = RecruiterIntelligence()
        
        self.validator = ProfileValidator()
        
        self.production = ProductionExperienceScorer()

    # ---------------------------------------------------
    # Behavioral Intelligence
    # ---------------------------------------------------

    def behavior_score(self, redrob):

        score = 0.0

        # Open to Work
        if redrob["open_to_work"]:
            score += 0.20

        # Recruiter Response Rate (0-1)
        score += 0.25 * redrob["recruiter_response_rate"]

        # Profile Completeness (0-100)
        score += 0.15 * (redrob["profile_score"] / 100)

        # GitHub Activity (-1 means unavailable)
        github = max(redrob["github_score"], 0)
        score += 0.10 * (github / 100)

        # Interview Completion (0-1)
        score += 0.05 * redrob["interview_completion_rate"]

        # Offer Acceptance (-1 means unavailable)
        offer = max(redrob["offer_acceptance_rate"], 0)
        score += 0.05 * offer

        # Recent Activity

        try:

            last = datetime.strptime(
                redrob["last_active_date"],
                "%Y-%m-%d"
            )

            # Fixed reference date for reproducible scoring
            reference_date = datetime(2026, 6, 30)

            days = (reference_date - last).days

            if days <= 30:
                score += 0.20

            elif days <= 90:
                score += 0.15

            elif days <= 180:
                score += 0.10

            else:
                score += 0.05

        except Exception:
            # Unknown activity date gets a neutral score
            score += 0.10

        # ---------------------------------------------
        # Normalize and Return
        # ---------------------------------------------

        score = min(score, 1.0)

        return score
    
    # ---------------------------------------------------
    # Ranking
    # ---------------------------------------------------

    def rank(
        self,
        semantic_score,
        profile,
        skills,
        redrob,
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
        # Behavioral Intelligence
        # ---------------------------------------------------

        behavior = self.behavior_score(redrob)
        
        # ---------------------------------------------------
        # Profile Consistency
        # ---------------------------------------------------

        validation = self.validator.evaluate(

            profile,

            skills,

            redrob

        )

        risk_score = validation["risk_score"]

        consistency_score = validation["consistency_score"]
        
        # ---------------------------------------------------
        # Production Experience
        # ---------------------------------------------------

        
        production = self.production.evaluate(profile)

        production_score = production["production_score"]

        # ---------------------------------------------------
        # Weighted Components
        # ---------------------------------------------------

        semantic_component = semantic_score * 0.35

        skill_component = skill_match * 0.45

        experience_component = experience_score * 0.10

        transfer_component = transferable_bonus

        behavior_component = behavior * 0.05
        
        risk_component = risk_score * 0.05
        
        production_component = production_score * 0.05

        # ---------------------------------------------------
        # Final Score
        # ---------------------------------------------------

        final_score = (
            semantic_component
            + skill_component
            + experience_component
            + transfer_component
            + behavior_component
            + production_component
            - risk_component
        )
        
        final_score = max(
            final_score,
            0.0
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

            "behavior_score": round(
                behavior,
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

            "behavior_component": round(
                behavior_component,
                4
            ),

            "final_score": round(
                final_score,
                4
            ),
            
            "profile_risk": round(
                risk_score,
                4
            ),

            "profile_consistency": round(
                consistency_score,
                4
            ),

            "profile_validation": validation["reasons"],
            
            "production_score": round(production_score, 4),

            "production_component": round(production_component, 4),

            "production_evidence": production["production_evidence"],

        }