from src.jd_parser import JDParser
from src.runtime_ranker import RuntimeRanker
from src.reasoning_engine import ReasoningEngine
from src.comparison_engine import ComparisonEngine
from src.report_generator import ReportGenerator
from src.learning_potential import LearningPotential
from src.submission_exporter import SubmissionExporter


class RecruiterPipeline:

    def __init__(self):

        self.parser = JDParser()

        self.runtime_ranker = RuntimeRanker()

        self.reasoner = ReasoningEngine()

        self.comparer = ComparisonEngine()

        self.reporter = ReportGenerator()

        self.learning = LearningPotential()

        self.exporter = SubmissionExporter()

    # --------------------------------------------------

    def run(
        self,
        job_description,
        limit=None
    ):

        # ----------------------------------------
        # Parse JD
        # ----------------------------------------

        parsed_jd = self.parser.parse(
            job_description
        )

        # ----------------------------------------
        # Rank Candidates
        # ----------------------------------------

        ranked = self.runtime_ranker.rank_candidates(

            job_description,

            parsed_jd,

            limit

        )

        if not ranked:

            return {

                "ranked_candidates": [],

                "top_candidate": None,

                "evaluation": None,

                "comparison": None,

                "learning": None,

                "report": "No candidates found."

            }

        # ----------------------------------------
        # Top Candidate
        # ----------------------------------------

        top_candidate = ranked[0]

        # ----------------------------------------
        # Evaluation
        # ----------------------------------------

        evaluation = self.reasoner.generate(

            top_candidate

        )

        # ----------------------------------------
        # Learning Potential
        # ----------------------------------------

        learning = self.learning.evaluate(

            top_candidate

        )

        # ----------------------------------------
        # Comparison
        # ----------------------------------------

        comparison = None

        if len(ranked) > 1:

            comparison = self.comparer.compare(

                ranked[0],

                ranked[1]

            )

        # ----------------------------------------
        # Report
        # ----------------------------------------

        report = self.reporter.generate(

            evaluation,

            comparison,

            learning

        )

        # ----------------------------------------
        # Export
        # ----------------------------------------

        self.exporter.export(

            ranked

        )

        # ----------------------------------------

        return {

            "ranked_candidates": ranked,

            "top_candidate": top_candidate,

            "evaluation": evaluation,

            "comparison": comparison,

            "learning": learning,

            "report": report

        }