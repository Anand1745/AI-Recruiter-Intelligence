# 🧠 AI Recruiter Intelligence

> **Reading Between the Lines of Candidate Resumes**

An AI-powered recruiter intelligence system developed for the **IndiaRuns – The Data & AI Challenge**.

The platform ranks candidates by combining semantic resume understanding with recruiter-oriented intelligence such as transferable skills, behavioral signals, production AI experience, profile consistency, and explainable reasoning.

---

# 👤 Submission Information

**Submission Type:** Solo Submission

**Author:** Anand Ramesh Karunakaran

**Institution:** NSS College of Engineering

**Branch:** Electronics and Communication Engineering

---

# Overview

Traditional Applicant Tracking Systems (ATS) rely primarily on keyword matching, often overlooking candidates with transferable skills or strong practical experience.

AI Recruiter Intelligence addresses this limitation by evaluating candidates across multiple dimensions:

- Semantic similarity
- Direct skill matching
- Transferable skill intelligence
- Experience validation
- Recruiter behavioral signals
- Production AI experience
- Profile consistency
- Explainable recruiter reasoning

The result is an interpretable ranking system capable of processing **100,000 candidates** efficiently on CPU.

---

# Key Features

- Semantic Resume Ranking
- Transferable Skill Intelligence
- Recruiter Behavioral Intelligence
- Production AI Experience Detection
- Profile Consistency Validation
- Explainable AI Recommendations
- Learning Potential Estimation
- Candidate Comparison Engine
- Interactive Streamlit Dashboard
- CSV Submission Generator
- Official Submission Validation Support

---

# System Architecture

```
                    Job Description
                           │
                           ▼
                  JD Parsing & Extraction
                           │
                           ▼
            Sentence Transformer Embedding
                           │
                           ▼
              Runtime Semantic Matching
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
 Skill Matching     Transferable Skills   Behavioral Signals
      │                    │                    │
      └──────────────┬─────┴────────────────────┘
                     ▼
         Production AI Experience Detection
                     ▼
          Profile Consistency Validation
                     ▼
              Explainable Ranking Engine
                     ▼
         Dashboard + Top-100 CSV Export
```

---

# Ranking Pipeline

The ranking score combines several independent components.

| Component | Purpose |
|------------|----------|
| Semantic Similarity | Resume ↔ Job Description similarity |
| Direct Skill Match | Required technical skills |
| Transferable Skills | Related technologies with confidence scoring |
| Experience Match | Required years of experience |
| Behavioral Intelligence | Recruiter engagement signals |
| Production AI Experience | Real-world AI/search experience |
| Profile Validation | Resume consistency |
| Learning Potential | Growth estimation |

---

# Repository Structure

```
AI-Recruiter-Intelligence/

dashboard/
src/
models/
data/
embeddings/
submissions/

main.py
build_embeddings.py
build_candidate_cache.py
README.md
requirements.txt
submission_metadata.yaml
LICENSE
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Anand1745/AI-Recruiter-Intelligence.git

cd AI-Recruiter-Intelligence
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Dataset

The challenge dataset is provided by the organizers or any other dataset should be placed in(renamed to candidates.jsonl if needed):

```
data/candidates.jsonl
```

# One-Time Preprocessing

The ranking system uses precomputed embeddings for fast inference.

Generate candidate embeddings

```bash
python build_embeddings.py
```

Generate runtime cache

```bash
python build_candidate_cache.py
```

These preprocessing steps only need to be executed once for a given dataset.

---

# Generate Submission

Run the ranking pipeline

```bash
python main.py
```

Output:

```
submissions/submission.csv
```

The runtime ranking step completes within the hackathon CPU compute budget.

---

# Validate Submission

The submission was verified using the official validator supplied with the challenge.

```bash
python validate_submission.py submissions/submission.csv
```

Validation output:

```
Submission is valid.
```

---

# Dashboard

Launch the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

Features include:

- Job Description Upload
- Candidate Ranking
- Candidate Explorer
- AI Recruiter Intelligence
- Learning Potential
- Candidate Comparison
- Dashboard Analytics
- Excel Export

---

# Performance Benchmark

| Metric | Result |
|---------|--------|
| Candidate Pool | 100,000 |
| Runtime | ~7.3 seconds |
| Memory Usage | ~1.3 GB RAM |
| Embedding Model | all-MiniLM-L6-v2 |
| Hardware | Intel Core i7, 24 GB RAM |
| Inference | CPU Only |

---

# Technology Stack

- Python
- Streamlit
- Sentence Transformers
- PyTorch
- Pandas
- NumPy
- Scikit-learn
- Plotly
- OpenPyXL
- python-docx

---

# AI Usage Statement

This is a **solo submission**.

AI tools (ChatGPT) were used as engineering assistants for brainstorming, debugging, documentation, code review, and development support. The system architecture, ranking methodology, module integration, experimentation, benchmarking, testing, and final engineering decisions were implemented, validated, and verified by the author.

No online AI APIs are used during candidate ranking or inference.

---

# Reproducibility

To reproduce the submission:

1. Place the challenge dataset in `data/candidates.jsonl`
2. Generate embeddings

```bash
python build_embeddings.py
```

3. Build runtime cache

```bash
python build_candidate_cache.py
```

4. Generate rankings

```bash
python main.py
```

5. Validate the generated submission

```bash
python validate_submission.py submissions/submission.csv
```

# License

Released under the MIT License.

---

# Acknowledgements

Developed for the **IndiaRuns – The Data & AI Challenge**.

Special thanks to the organizers for providing the challenge dataset, evaluation framework, and submission guidelines.
