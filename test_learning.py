from src.learning_potential import LearningPotential

candidate = {

    "num_transferable_matches": 2,

    "experience_match": True,

    "semantic_score": 0.78

}

engine = LearningPotential()

print(engine.evaluate(candidate))