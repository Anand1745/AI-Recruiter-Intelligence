from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model loaded.")

        self.embedding_cache = {}

    # --------------------------------------------------
    # Get Embedding
    # --------------------------------------------------

    def get_embedding(
        self,
        text
    ):

        if text in self.embedding_cache:
            return self.embedding_cache[text]

        embedding = self.model.encode(
            text,
            convert_to_numpy=True
        )

        self.embedding_cache[text] = embedding

        return embedding

    # --------------------------------------------------
    # Existing Similarity (Keep for Compatibility)
    # --------------------------------------------------

    def similarity(
        self,
        text1,
        text2
    ):

        emb1 = self.get_embedding(text1)
        emb2 = self.get_embedding(text2)

        score = cosine_similarity(
            [emb1],
            [emb2]
        )[0][0]

        return float(score)

    # --------------------------------------------------
    # NEW : Batch Similarity
    # --------------------------------------------------

    def batch_similarity(
        self,
        job_description,
        candidate_embeddings
    ):

        jd_embedding = self.get_embedding(
            job_description
        )

        scores = cosine_similarity(

            [jd_embedding],

            candidate_embeddings

        )[0]

        return scores