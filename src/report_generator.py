class ReportGenerator:

    def generate(
        self,
        evaluation,
        comparison,
        learning
    ):

        report = []

        # ===================================================
        # Header
        # ===================================================

        report.append("=" * 60)
        report.append("AI RECRUITER INTELLIGENCE REPORT")
        report.append("=" * 60)

        report.append("")
        report.append(f"Candidate : {evaluation['candidate_name']}")
        report.append(f"Overall Match : {evaluation['overall_match']}%")
        report.append(f"Recommendation : {evaluation['recommendation']}")
        report.append(f"Confidence : {evaluation['confidence']}")

        # ===================================================
        # Summary
        # ===================================================

        report.append("")
        report.append("-" * 60)
        report.append("SUMMARY")
        report.append("-" * 60)

        report.append(evaluation["summary"])

        # ===================================================
        # Strengths
        # ===================================================

        report.append("")
        report.append("-" * 60)
        report.append("STRENGTHS")
        report.append("-" * 60)

        if evaluation["strengths"]:

            for strength in evaluation["strengths"]:
                report.append(f"✓ {strength}")

        else:
            report.append("No major strengths identified.")

        # ===================================================
        # Gaps
        # ===================================================

        report.append("")
        report.append("-" * 60)
        report.append("GAPS")
        report.append("-" * 60)

        if evaluation["gaps"]:

            for gap in evaluation["gaps"]:
                report.append(f"✗ {gap}")

        else:
            report.append("No significant gaps detected.")

        # ===================================================
        # Learning Potential
        # ===================================================

        report.append("")
        report.append("-" * 60)
        report.append("LEARNING POTENTIAL")
        report.append("-" * 60)

        report.append(
            f"Potential : {learning['learning_potential']}"
        )

        report.append(
            f"Score : {learning['learning_score']}"
        )

        report.append("")

        report.append("Reasons:")

        for item in learning["explanation"]:
            report.append(f"✓ {item}")

        # ===================================================
        # Comparison
        # ===================================================

        report.append("")
        report.append("-" * 60)
        report.append("COMPARISON")
        report.append("-" * 60)

        if comparison:

            report.append(
                comparison["recommendation"]
            )

            if comparison["advantages"]:

                report.append("")
                report.append("Reasons:")

                for item in comparison["advantages"]:
                    report.append(f"• {item}")

        else:

            report.append(
                "Only one candidate available for comparison."
            )

        # ===================================================
        # Footer
        # ===================================================

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)