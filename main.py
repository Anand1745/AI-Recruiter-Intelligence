from pathlib import Path

from src.pipeline import RecruiterPipeline


DATA_PATH = "data/candidates.jsonl"
JD_PATH = "job_description.txt"

pipeline = RecruiterPipeline(DATA_PATH)


def load_job_description():

    jd_file = Path(JD_PATH)

    if not jd_file.exists():
        raise FileNotFoundError(
            f"Job description file not found: {JD_PATH}"
        )

    return jd_file.read_text(
        encoding="utf-8"
    )


def main():

    print("=" * 60)
    print("AI Recruiter Intelligence")
    print("=" * 60)

    print("\nLoading job description...\n")

    job_description = load_job_description()

    results = pipeline.run(
        job_description,
        limit=100
    )

    print(results["report"])


if __name__ == "__main__":
    main()