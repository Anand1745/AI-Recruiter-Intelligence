class ReportGenerator:

    def generate(
        self,
        evaluation,
        comparison
    ):

        report = []

        report.append("=" * 60)
        report.append("AI RECRUITER INTELLIGENCE REPORT")
        report.append("=" * 60)

        report.append("")
        report.append(f"Candidate : {evaluation['candidate_name']}")
        report.append(f"Overall Match : {evaluation['overall_match']}%")
        report.append(f"Recommendation : {evaluation['recommendation']}")
        report.append(f"Confidence : {evaluation['confidence']}")

        report.append("")
        report.append("-" * 60)
        report.append("SUMMARY")
        report.append("-" * 60)
        report.append(evaluation["summary"])

        report.append("")
        report.append("STRENGTHS")

        for strength in evaluation["strengths"]:
            report.append(f"✓ {strength}")

        report.append("")
        report.append("GAPS")

        for gap in evaluation["gaps"]:
            report.append(f"✗ {gap}")

        report.append("")
        report.append("-" * 60)
        report.append("COMPARISON")
        report.append("-" * 60)

        report.append(
            comparison["recommendation"]
        )

        if comparison["advantages"]:

            report.append("")
            report.append("Reasons:")

            for item in comparison["advantages"]:
                report.append(f"• {item}")

        report.append("")
        report.append("=" * 60)

        return "\n".join(report)