import json
from pathlib import Path


class CandidateDataLoader:
    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def load_candidates(self):
        candidates = []

        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                candidates.append(json.loads(line))

        return candidates

    def stream_candidates(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                yield json.loads(line)