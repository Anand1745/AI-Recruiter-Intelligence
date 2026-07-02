from src.candidate_cache_builder import CandidateCacheBuilder

builder = CandidateCacheBuilder(
    "data/candidates.jsonl"
)

builder.build()