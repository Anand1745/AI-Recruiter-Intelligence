from src.knowledge_base.skill_graph import SKILL_GRAPH


class RecruiterIntelligence:

    def __init__(self):

        self.skill_graph = SKILL_GRAPH

    def normalize(self, skills):

        return {
            skill.lower().strip()
            for skill in skills
        }

    def infer_transferable_skills(
        self,
        candidate_skills,
        required_skills
    ):

        candidate_skills = self.normalize(candidate_skills)
        required_skills = self.normalize(required_skills)

        transferable_matches = []

        # Avoid duplicate suggestions
        seen = set()

        for required_skill in required_skills:

            # Skip if candidate already has the skill
            if required_skill in candidate_skills:
                continue

            best_match = None

            for category, technologies in self.skill_graph.items():

                # Required skill must exist in this category
                if required_skill not in technologies:
                    continue

                required_weight = technologies[required_skill]

                for candidate_skill in candidate_skills:

                    # Candidate skill must exist in same category
                    if candidate_skill not in technologies:
                        continue

                    candidate_weight = technologies[candidate_skill]

                    confidence = round(
                        min(required_weight, candidate_weight),
                        2
                    )

                    key = (
                        required_skill,
                        candidate_skill
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    match = {

                        "required_skill": required_skill,

                        "candidate_skill": candidate_skill,

                        "category": category,

                        "confidence": confidence,

                        "reason":
                            f"{candidate_skill.title()} experience suggests "
                            f"transferable knowledge for "
                            f"{required_skill.title()}."

                    }

                    # Keep only the strongest match
                    if (
                        best_match is None
                        or confidence > best_match["confidence"]
                    ):
                        best_match = match

            if best_match:
                transferable_matches.append(best_match)

        # Highest confidence first
        transferable_matches.sort(
            key=lambda x: x["confidence"],
            reverse=True
        )

        # Show only the strongest transferable skills
        return transferable_matches[:5]