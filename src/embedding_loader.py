import os
import pickle

import numpy as np


class EmbeddingLoader:

    def __init__(self, embedding_dir="embeddings"):

        self.embedding_dir = embedding_dir

        self.embeddings = None
        self.runtime_cache = None

    # --------------------------------------------------
    # Load Runtime Files
    # --------------------------------------------------

    def load(self):

        embedding_file = os.path.join(
            self.embedding_dir,
            "candidate_embeddings.npy"
        )

        runtime_cache_file = os.path.join(
            self.embedding_dir,
            "candidate_runtime_cache.pkl"
        )

        if not os.path.exists(embedding_file):
            raise FileNotFoundError(
                embedding_file
            )

        if not os.path.exists(runtime_cache_file):
            raise FileNotFoundError(
                runtime_cache_file
            )

        print("\nLoading candidate embeddings...")

        self.embeddings = np.load(
            embedding_file
        )

        print("Loading runtime cache...")

        with open(
            runtime_cache_file,
            "rb"
        ) as f:

            self.runtime_cache = pickle.load(f)

        print("\nRuntime data loaded successfully.")

        print(
            f"Embeddings : {self.embeddings.shape}"
        )

        print(
            f"Runtime Cache : {len(self.runtime_cache)}"
        )

    # --------------------------------------------------
    # Lazy Loading
    # --------------------------------------------------

    def ensure_loaded(self):

        if self.embeddings is None:

            self.load()

    # --------------------------------------------------
    # Get Embeddings
    # --------------------------------------------------

    def get_embeddings(self):

        self.ensure_loaded()

        return self.embeddings

    # --------------------------------------------------
    # Get Runtime Cache
    # --------------------------------------------------

    def get_candidate_cache(self):

        self.ensure_loaded()

        return self.runtime_cache

    # --------------------------------------------------
    # Get Candidate
    # --------------------------------------------------

    def get_candidate(self, index):

        self.ensure_loaded()

        return self.runtime_cache[index]