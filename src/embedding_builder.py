import os
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from src.data_loader import CandidateDataLoader
from src.candidate_processor import CandidateProcessor


class EmbeddingBuilder:

    def __init__(
        self,
        data_path,
        model_name="all-MiniLM-L6-v2"
    ):

        self.loader = CandidateDataLoader(data_path)
        self.processor = CandidateProcessor()

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            model_name
        )

        print("Model loaded.")

    # --------------------------------------------------
    # Build Candidate Text
    # --------------------------------------------------

    def build_candidate_text(
        self,
        candidate
    ):

        profile = self.processor.process_profile(
            candidate
        )

        skills = self.processor.process_skills(
            candidate
        )

        text = " ".join([

            profile["headline"] or "",

            profile["summary"] or "",

            skills["skills_text"]

        ])

        return text.strip()

    # --------------------------------------------------
    # Build Embeddings
    # --------------------------------------------------

    def build(
        self,
        output_dir="embeddings",
        batch_size=256
    ):

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        candidates = self.loader.load_candidates()

        print(f"\nLoaded {len(candidates)} candidates.\n")

        texts = []
        ids = []

        for candidate in candidates:

            ids.append(
                candidate["candidate_id"]
            )

            texts.append(
                self.build_candidate_text(
                    candidate
                )
            )

        print("Generating embeddings...\n")

        embeddings = self.model.encode(

            texts,

            batch_size=batch_size,

            show_progress_bar=True,

            convert_to_numpy=True

        )

        np.save(

            os.path.join(
                output_dir,
                "candidate_embeddings.npy"
            ),

            embeddings

        )

        with open(

            os.path.join(
                output_dir,
                "candidate_ids.pkl"
            ),

            "wb"

        ) as f:

            pickle.dump(
                ids,
                f
            )

        print("\nEmbedding generation complete!")

        print(
            f"Embeddings shape : {embeddings.shape}"
        )

        print(
            f"Saved to : {output_dir}"
        )