from src.recruiter_intelligence import RecruiterIntelligence

ri = RecruiterIntelligence()

candidate = [
    "Python",
    "Flask",
    "Azure"
]

required = [
    "Python",
    "FastAPI",
    "AWS"
]

matches = ri.infer_transferable_skills(
    candidate,
    required
)

for match in matches:
    print(match)