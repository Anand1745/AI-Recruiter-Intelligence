from src.pipeline import RecruiterPipeline


class RecruiterService:

    def __init__(self, data_path=None):

        self.pipeline = RecruiterPipeline()

        self.results = None


    # --------------------------------------------------
    # Analyze Job Description
    # --------------------------------------------------

    def analyze_job_description(
        self,
        job_description
    ):

        self.results = self.pipeline.run(
            job_description
        )

        return self.results


    # --------------------------------------------------
    # Get Results
    # --------------------------------------------------

    def get_results(self):

        return self.results


    # --------------------------------------------------
    # Get Ranked Candidates
    # --------------------------------------------------

    def get_ranked_candidates(self):

        if self.results is None:

            return []

        return self.results["ranked_candidates"]


    # --------------------------------------------------
    # Get Candidate
    # --------------------------------------------------

    def get_candidate(
        self,
        index
    ):

        candidates = self.get_ranked_candidates()

        if index < 0:

            return None

        if index >= len(candidates):

            return None

        return candidates[index]