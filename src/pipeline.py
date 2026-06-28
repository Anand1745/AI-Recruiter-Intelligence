from src.data_loader import CandidateDataLoader
from src.candidate_processor import CandidateProcessor
from src.jd_parser import JDParser
from src.semantic_matcher import SemanticMatcher
from src.ranking_engine import RankingEngine
from src.reasoning_engine import ReasoningEngine
from src.comparison_engine import ComparisonEngine
from src.report_generator import ReportGenerator
from src.learning_potential import LearningPotential


class RecruiterPipeline:

    def __init__(
        self,
        data_path
    ):

        self.loader = CandidateDataLoader(data_path)

        self.processor = CandidateProcessor()

        self.parser = JDParser()

        self.matcher = SemanticMatcher()

        self.ranker = RankingEngine()

        self.reasoner = ReasoningEngine()

        self.comparer = ComparisonEngine()

        self.reporter = ReportGenerator()

        self.learning = LearningPotential()

    def run(
        self,
        job_description,
        limit=100
    ):

        # ----------------------------------------
        # Parse Job Description
        # ----------------------------------------

        parsed_jd = self.parser.parse(
            job_description
        )

        # ----------------------------------------
        # Load Candidates
        # ----------------------------------------

        candidates = self.loader.load_candidates()

        candidates = candidates[:limit]

        scores = []

        # ----------------------------------------
        # Rank Every Candidate
        # ----------------------------------------

        for candidate in candidates:

            profile = self.processor.process_profile(
                candidate
            )

            skills = self.processor.process_skills(
                candidate
            )

            candidate_text = " ".join([

                profile["headline"],

                profile["summary"],

                skills["skills_text"]

            ])

            semantic_score = self.matcher.similarity(

                job_description,

                candidate_text

            )

            ranking = self.ranker.rank(

                semantic_score,

                profile,

                skills,

                parsed_jd

            )

            scores.append({

                "candidate_id": candidate["candidate_id"],

                "name": profile["name"],

                **ranking

            })

        # ----------------------------------------
        # Sort Candidates
        # ----------------------------------------

        ranked = sorted(

            scores,

            key=lambda x: x["final_score"],

            reverse=True

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
        # Best Candidate
        # ----------------------------------------

        top_candidate = ranked[0]

        # ----------------------------------------
        # AI Evaluation
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
        # Candidate Comparison
        # ----------------------------------------

        comparison = None

        if len(ranked) > 1:

            comparison = self.comparer.compare(

                ranked[0],

                ranked[1]

            )

        # ----------------------------------------
        # Recruiter Report
        # ----------------------------------------

        report = self.reporter.generate(

            evaluation,

            comparison,
            
            learning

        )

        # ----------------------------------------
        # Return Complete Pipeline
        # ----------------------------------------

        return {

            "ranked_candidates": ranked,

            "top_candidate": top_candidate,

            "evaluation": evaluation,

            "comparison": comparison,

            "learning": learning,

            "report": report

        }