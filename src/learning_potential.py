class LearningPotential:

    def evaluate(self, candidate):

        transferable = candidate["num_transferable_matches"]

        experience = candidate["experience_match"]

        semantic = candidate["semantic_score"]

        score = 0

        # Experience contributes most
        if experience:
            score += 40

        # Semantic understanding
        score += semantic * 30

        # Transferable skills
        score += min(
            transferable * 15,
            30
        )

        score = round(score, 2)

        if score >= 80:
            potential = "Very High"

        elif score >= 65:
            potential = "High"

        elif score >= 50:
            potential = "Medium"

        else:
            potential = "Low"

        explanation = []

        if experience:
            explanation.append(
                "Strong professional experience."
            )

        if transferable:
            explanation.append(
                f"{transferable} transferable skill(s) identified."
            )

        if semantic >= 0.70:

            explanation.append(
                "Excellent semantic alignment with the role."
            )

        elif semantic >= 0.60:

            explanation.append(
                "Good semantic alignment with the role."
            )

        else:

            if transferable:

                explanation.append(
                    "Transferable technical skills indicate strong potential despite moderate semantic alignment."
                )

            else:

                explanation.append(
                    "Additional domain-specific experience would further improve role readiness."
                )
            
        return {

            "learning_score": score,

            "learning_potential": potential,

            "explanation": explanation

        }