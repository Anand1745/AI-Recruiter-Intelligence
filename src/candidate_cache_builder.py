import os
import pickle

from src.data_loader import CandidateDataLoader
from src.candidate_processor import CandidateProcessor


class CandidateCacheBuilder:

    def __init__(self, data_path):

        self.loader = CandidateDataLoader(data_path)
        self.processor = CandidateProcessor()

    def build(self, output_dir="embeddings"):

        os.makedirs(
            output_dir,
            exist_ok=True
        )

        candidates = self.loader.load_candidates()

        runtime_cache = []

        print(f"Building runtime cache for {len(candidates)} candidates...\n")

        for candidate in candidates:

            runtime_cache.append({

                "candidate_id":
                    candidate["candidate_id"],

                "profile":
                    self.processor.process_profile(candidate),

                "skills":
                    self.processor.process_skills(candidate),

                "education":
                    self.processor.process_education(candidate),

                "certifications":
                    self.processor.process_certifications(candidate),

                "redrob":
                    self.processor.process_redrob(candidate)

            })

        output_file = os.path.join(

            output_dir,

            "candidate_runtime_cache.pkl"

        )

        with open(
            output_file,
            "wb"
        ) as f:

            pickle.dump(
                runtime_cache,
                f
            )

        print()

        print("Runtime cache generated successfully.")

        print(
            f"Total candidates : {len(runtime_cache)}"
        )