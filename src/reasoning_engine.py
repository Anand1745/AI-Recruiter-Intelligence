class ReasoningEngine:

    def generate(self, candidate):

        score = candidate["final_score"]

        # ----------------------------------
        # Recommendation
        # ----------------------------------
        
        if score >= 0.85:
            recommendation = "Strong Hire"
            confidence = "Very High"

        elif score >= 0.75:
            recommendation = "Interview"
            confidence = "High"

        elif score >= 0.65:
            recommendation = "Consider"
            confidence = "Medium"

        elif score >= 0.50:
            recommendation = "Review"
            confidence = "Low"

        else:
            recommendation = "Reject"
            confidence = "Low"

        strengths = []
        gaps = []

        # ----------------------------------
        # Experience
        # ----------------------------------

        if candidate["experience_match"]:

            strengths.append(
                "Meets required experience."
            )

        else:

            gaps.append(
                "Does not meet the required experience."
            )

        # ----------------------------------
        # Direct Skill Matches
        # ----------------------------------

        if candidate["matched_skills"]:

            strengths.append(

                f"Direct skill matches ({len(candidate['matched_skills'])}): "

                + ", ".join(candidate["matched_skills"])

            )

        # ----------------------------------
        # Transferable Skill Intelligence
        # ----------------------------------

        if candidate["transferable_matches"]:

            for match in candidate["transferable_matches"]:

                if match["category"] == "Cloud":

                    explanation = (
                        "Cloud platform knowledge is highly transferable."
                    )

                elif match["category"] == "Python Web":

                    explanation = (
                        "Python web framework experience suggests a short learning curve."
                    )

                elif match["category"] == "Databases":

                    explanation = (
                        "Relational database concepts are highly transferable."
                    )

                elif match["category"] == "Containers":

                    explanation = (
                        "Containerization experience transfers effectively."
                    )

                elif match["category"] == "ML Frameworks":

                    explanation = (
                        "Deep learning framework experience is transferable."
                    )

                else:

                    explanation = (
                        "Related technical knowledge identified."
                    )

                strengths.append(

                    f"{match['candidate_skill'].title()} → "

                    f"{match['required_skill'].title()} "

                    f"({int(match['confidence'] * 100)}%) - "

                    f"{explanation}"

                )
        
        # ----------------------------------
        # Production Experience
        # ----------------------------------

        if candidate.get("production_score", 0) >= 0.30:

            strengths.append(
                "Demonstrates evidence of building production AI/search systems."
            )

            evidence = candidate.get(
                "production_evidence",
                []
            )

            if evidence:

                strengths.append(

                    "Production indicators: "

                    + ", ".join(
                        evidence[:5]
                    )

                )        

        # ----------------------------------
        # Missing Skills
        # ----------------------------------

        if candidate["missing_skills"]:

            gaps.append(

                "Missing skills: "

                + ", ".join(candidate["missing_skills"])

            )

        # ----------------------------------
        # Semantic Alignment
        # ----------------------------------

        semantic = candidate["semantic_score"]

        if semantic >= 0.70:

            strengths.append(
                "Excellent semantic alignment with the job description."
            )

        elif semantic >= 0.60:

            strengths.append(
                "Good semantic alignment with the job description."
            )

        else:

            if candidate["num_transferable_matches"] > 0:

                strengths.append(
                    "Transferable technical expertise helps compensate for moderate semantic alignment."
                )

            else:

                gaps.append(
                    "Resume shows limited alignment with the overall job requirements."
                )

        # ----------------------------------
        # Behavioral Intelligence
        # ----------------------------------

        behavior = candidate.get(
            "behavior_score",
            0
        )

        if behavior >= 0.80:

            strengths.append(
                "Excellent recruiter engagement and profile activity."
            )

        elif behavior >= 0.60:

            strengths.append(
                "Good recruiter engagement."
            )

        elif behavior <= 0.30:

            gaps.append(
                "Weak recruiter engagement signals."
            )
            
        # ----------------------------------
        # Profile Consistency
        # ----------------------------------

        consistency = candidate.get(
            "profile_consistency",
            1.0
        )

        validation = candidate.get(
            "profile_validation",
            []
        )

        if consistency >= 0.95:

            strengths.append(
                "Profile information appears internally consistent."
            )

        elif validation:

            gaps.extend(validation)
        
        # ----------------------------------
        # Executive Summary
        # ----------------------------------
        
        summary = (

            f"The candidate achieved an overall match score of "

            f"{score:.2%}. "

            f"The recommendation considers semantic similarity, "

            f"technical skill alignment, production engineering "

            f"experience, behavioral hiring signals, "

            f"profile consistency validation, and transferable "

            f"technical expertise to estimate both immediate "

            f"suitability and long-term hiring potential."

        )
        
        # ----------------------------------
        # Submission Reasoning
        # ----------------------------------

        submission_reasons = []

        if candidate["matched_skills"]:

            submission_reasons.append(

                "Direct skill match: "

                + ", ".join(
                    candidate["matched_skills"]
                )

            )

        if candidate.get(
            "production_evidence",
            []
        ):

            submission_reasons.append(

                "Production AI experience in "

                + ", ".join(
                    candidate["production_evidence"][:3]
                )

            )

        elif candidate["num_transferable_matches"] > 0:

            submission_reasons.append(

                f"{candidate['num_transferable_matches']} transferable technical skill(s)"

            )

        if candidate["experience_match"]:

            submission_reasons.append(

                "Meets required experience"

            )

        if semantic >= 0.70:

            submission_reasons.append(

                "Strong semantic alignment"

            )

        elif semantic >= 0.60:

            submission_reasons.append(

                "Good semantic alignment"

            )

        if candidate.get(
            "behavior_score",
            0
        ) >= 0.60:

            submission_reasons.append(

                "Positive recruiter engagement"

            )

        if candidate["missing_skills"]:

            submission_reasons.append(

                "Primary gap: "

                + ", ".join(
                    candidate["missing_skills"]
                )

            )

        if candidate.get(
            "profile_risk",
            0
        ) > 0.20:

            submission_reasons.append(

                "Minor profile consistency concerns"

            )

        submission_reasoning = ". ".join(
            submission_reasons
        ) + "."

        # ----------------------------------
        # Return Evaluation
        # ----------------------------------

        return {

            "candidate_name": candidate["name"],

            "overall_match": round(
                score * 100,
                2
            ),

            "recommendation": recommendation,

            "confidence": confidence,

            "summary": summary,

            "strengths": strengths,
            
            "submission_reasoning": submission_reasoning,

            "gaps": gaps,

            "metrics": {

                "semantic_score": round(
                    semantic * 100,
                    2
                ),

                "skill_match": round(
                    candidate["skill_match"] * 100,
                    2
                ),
                
                                "behavior_score": round(
                    candidate["behavior_score"] * 100,
                    2
                ),

                "production_score": round(
                    candidate.get(
                        "production_score",
                        0
                    ) * 100,
                    2
                ),

                "profile_consistency": round(
                    candidate.get(
                        "profile_consistency",
                        1.0
                    ) * 100,
                    2
                ),

                "transferable_matches":
                    candidate[
                        "num_transferable_matches"
                    ],

                "experience_match":
                    candidate[
                        "experience_match"
                    ]

            }

        }