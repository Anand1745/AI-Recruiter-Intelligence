class ProductionExperienceScorer:

    def __init__(self):

        self.production_keywords = {

            "production": 0.15,
            "deployed": 0.12,
            "deployment": 0.10,
            "real users": 0.15,
            "serving": 0.10,
            "inference": 0.08,
            "retrieval": 0.12,
            "ranking": 0.15,
            "recommendation": 0.15,
            "search": 0.10,
            "vector database": 0.15,
            "pinecone": 0.12,
            "weaviate": 0.12,
            "qdrant": 0.12,
            "milvus": 0.12,
            "faiss": 0.12,
            "elasticsearch": 0.10,
            "opensearch": 0.10,
            "sentence-transformers": 0.12,
            "embedding": 0.12,
            "embeddings": 0.12,
            "ab testing": 0.12,
            "a/b": 0.12,
            "ndcg": 0.10,
            "mrr": 0.10,
            "map": 0.10
        }

    def evaluate(self, profile):

        text = " ".join([

            profile.get("headline", ""),
            profile.get("summary", ""),
            profile.get("current_title", "")

        ]).lower()

        score = 0.0
        evidence = []

        for keyword, weight in self.production_keywords.items():

            if keyword in text:
                score += weight
                evidence.append(keyword)

        score = min(score, 1.0)

        return {

            "production_score": round(score, 4),
            "production_evidence": evidence

        }