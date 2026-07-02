from pathlib import Path
import time

import psutil
import os

from src.pipeline import RecruiterPipeline
from src.submission_exporter import SubmissionExporter


DATA_PATH = "data/candidates.jsonl"
JD_PATH = "job_description.txt"

pipeline = RecruiterPipeline()
exporter = SubmissionExporter()


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
    
    process = psutil.Process(os.getpid())

    start_time = time.perf_counter()

    results = pipeline.run(
        job_description
    )
    
    end_time = time.perf_counter()

    memory_mb = process.memory_info().rss / (1024 * 1024)

    print("\n" + "=" * 60)
    print("PERFORMANCE BENCHMARK")
    print("=" * 60)

    print(f"Candidates Ranked : {len(results['ranked_candidates']):,}")

    print(f"Runtime           : {end_time - start_time:.2f} sec")

    print(f"RAM Usage         : {memory_mb:.2f} MB")

    print("=" * 60)

    # ----------------------------------------
    # Export Submission CSV
    # ----------------------------------------

    csv_path = exporter.export(
        results["ranked_candidates"]
    )

    print(f"\nSubmission CSV saved to: {csv_path}")

    # ----------------------------------------
    # Print Recruiter Report
    # ----------------------------------------

    print(results["report"])


if __name__ == "__main__":
    main()