from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticMatcher:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model loaded.")

    def get_embedding(self, text):
        return self.model.encode(
            text,
            convert_to_numpy=True
        )

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