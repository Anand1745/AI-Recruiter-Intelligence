from src.embedding_builder import EmbeddingBuilder

DATA_PATH = "data/candidates.jsonl"

builder = EmbeddingBuilder(DATA_PATH)

builder.build(
    batch_size=256
)