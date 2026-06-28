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

        for required_skill in required_skills:

            if required_skill in candidate_skills:
                continue

            for category, technologies in self.skill_graph.items():

                if required_skill not in technologies:
                    continue

                required_weight = technologies[required_skill]

                for candidate_skill in candidate_skills:

                    if candidate_skill not in technologies:
                        continue

                    candidate_weight = technologies[candidate_skill]

                    confidence = round(
                        min(required_weight, candidate_weight),
                        2
                    )

                    transferable_matches.append({

                        "required_skill": required_skill,

                        "candidate_skill": candidate_skill,

                        "category": category,

                        "confidence": confidence,

                        "reason":
                            f"{candidate_skill.title()} experience suggests "
                            f"transferable knowledge for "
                            f"{required_skill.title()}."

                    })

        return transferable_matches