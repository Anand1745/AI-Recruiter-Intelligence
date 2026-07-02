from src.embedding_loader import EmbeddingLoader
from src.semantic_matcher import SemanticMatcher
from src.ranking_engine import RankingEngine


class RuntimeRanker:

    def __init__(self):

        print("\nInitializing Runtime Ranker...")

        self.loader = EmbeddingLoader()
        self.matcher = SemanticMatcher()
        self.ranker = RankingEngine()

        # Load once during startup
        self.embeddings = self.loader.get_embeddings()
        self.runtime_cache = self.loader.get_candidate_cache()

        print("Runtime Ranker Ready.\n")

    # --------------------------------------------------
    # Rank All Candidates
    # --------------------------------------------------

    def rank_candidates(
        self,
        job_description,
        parsed_jd,
        limit=None
    ):

        # Compute semantic scores for ALL candidates in one shot
        semantic_scores = self.matcher.batch_similarity(
            job_description,
            self.embeddings
        )

        total_candidates = len(self.runtime_cache)

        if limit is None or limit > total_candidates:
            limit = total_candidates

        scores = []

        cache = self.runtime_cache
        ranker = self.ranker
        semantics = semantic_scores

        for i in range(limit):

            candidate = cache[i]

            ranking = ranker.rank(

                semantics[i],

                candidate["profile"],

                candidate["skills"],

                candidate["redrob"],

                parsed_jd

            )

            scores.append({

                "candidate_id": candidate["candidate_id"],

                "name": candidate["profile"]["name"],

                **ranking

            })

        ranked = sorted(

            scores,

            key=lambda x: x["final_score"],

            reverse=True

        )

        return ranked