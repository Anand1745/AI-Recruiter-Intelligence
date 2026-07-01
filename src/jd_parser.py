import re


class JDParser:

    def __init__(self):

        # -----------------------------
        # Skill Aliases
        # -----------------------------

        self.skill_aliases = {

            # Programming
            "Python": ["python", "python3", "py"],
            "Java": ["java"],
            "C++": ["c++", "cpp"],
            "JavaScript": ["javascript", "js"],
            "TypeScript": ["typescript", "ts"],
            "Go": ["go", "golang"],
            "Rust": ["rust"],
            "SQL": ["sql"],

            # Cloud
            "AWS": ["aws", "amazon web services", "aws cloud"],
            "Azure": ["azure", "microsoft azure"],
            "GCP": ["gcp", "google cloud", "google cloud platform"],

            # Data Engineering
            "Spark": ["spark", "apache spark"],
            "Hadoop": ["hadoop"],
            "Kafka": ["kafka", "apache kafka"],
            "Airflow": ["airflow", "apache airflow"],
            "Databricks": ["databricks"],
            "Apache Beam": ["apache beam", "beam"],
            "Apache Flink": ["apache flink", "flink"],
            "Snowflake": ["snowflake"],
            "BigQuery": ["bigquery", "big query"],
            "dbt": ["dbt"],
            "ETL": ["etl"],

            # Databases
            "PostgreSQL": ["postgres", "postgresql", "postgre sql"],
            "MySQL": ["mysql", "my sql"],
            "Redis": ["redis"],

            # Backend
            "Docker": ["docker", "docker containers", "containerization"],
            "Kubernetes": ["kubernetes", "k8s"],
            "Flask": ["flask"],
            "FastAPI": ["fastapi", "fast api"],
            "REST APIs": [
                "rest",
                "rest api",
                "rest apis",
                "restful api",
                "restful apis"
            ],
            "GraphQL": ["graphql", "graph ql"],
            "gRPC": ["grpc"],

            # Frontend
            "React": ["react", "reactjs", "react.js"],
            "Next.js": ["next.js", "nextjs", "next js"],
            "Angular": ["angular"],
            "Vue.js": ["vue", "vuejs", "vue.js"],
            "HTML": ["html"],
            "CSS": ["css"],

            # DevOps
            "Git": ["git"],
            "CI/CD": ["ci/cd", "ci cd", "continuous integration"],
            "Terraform": ["terraform"],

            # AI / ML
            "TensorFlow": ["tensorflow", "tensor flow"],
            "PyTorch": ["pytorch", "py torch"],
            "Machine Learning": [
                "machine learning",
                "ml"
            ],
            "Deep Learning": [
                "deep learning",
                "dl"
            ],
            "NLP": [
                "nlp",
                "natural language processing"
            ],
            "LLMs": [
                "llm",
                "llms",
                "large language model",
                "large language models"
            ],
            "Fine-tuning LLMs": [
                "fine tuning",
                "fine-tuning",
                "llm fine tuning"
            ],
            "GANs": [
                "gan",
                "gans"
            ],
            "LoRA": [
                "lora",
                "low rank adaptation"
            ],

            # Analytics
            "Excel": ["excel", "ms excel"],
            "Tableau": ["tableau"],
            "Power BI": ["power bi", "powerbi"],

            # Design
            "Figma": ["figma"],
            "Photoshop": ["photoshop"],
            "Illustrator": ["illustrator"],

            # Business
            "Salesforce CRM": [
                "salesforce",
                "salesforce crm"
            ],
            "Project Management": [
                "project management"
            ],
            "Agile": ["agile"],
            "Scrum": ["scrum"],
            "Six Sigma": [
                "six sigma"
            ],
            "SEO": ["seo"],
            "Marketing": ["marketing"],
            "Accounting": ["accounting"],
            "Tally": ["tally"]
        }

        self.soft_skill_list = [

            "Leadership",
            "Communication",
            "Teamwork",
            "Problem Solving",
            "Analytical Thinking",
            "Stakeholder Management"

        ]

        self.job_titles = [

            "Backend Engineer",
            "Software Engineer",
            "Data Scientist",
            "Machine Learning Engineer",
            "Frontend Engineer",
            "Full Stack Developer",
            "Data Engineer",
            "DevOps Engineer",
            "Cloud Engineer",
            "AI Engineer",
            "ML Engineer",
            "Analytics Engineer"

        ]

    # --------------------------------------------------------

    def extract_skills(self, text):

        text = text.lower()

        skills = []

        for skill, aliases in self.skill_aliases.items():

            for alias in aliases:

                pattern = rf"\b{re.escape(alias.lower())}\b"

                if re.search(pattern, text):

                    skills.append(skill)
                    break

        return sorted(set(skills))

    # --------------------------------------------------------

    def parse(self, jd_text):

        text = jd_text.strip()

        # -----------------------------
        # Experience
        # -----------------------------

        experience = re.search(

            r"(\d+)\+?\s*years?",

            text,

            re.IGNORECASE

        )

        minimum_experience = (

            int(experience.group(1))

            if experience

            else 0

        )

        # -----------------------------
        # Preferred Skills
        # -----------------------------

        preferred_text = ""

        preferred_match = re.search(

            r"preferred.*",

            text,

            re.IGNORECASE | re.DOTALL

        )

        if preferred_match:

            preferred_text = preferred_match.group()

        preferred_skills = self.extract_skills(preferred_text)

        # -----------------------------
        # Required Skills
        # -----------------------------

        required_skills = self.extract_skills(text)

        required_skills = [

            skill

            for skill in required_skills

            if skill not in preferred_skills

        ]

        # -----------------------------
        # Soft Skills
        # -----------------------------

        soft_skills = []

        lower_text = text.lower()

        for skill in self.soft_skill_list:

            if skill.lower() in lower_text:

                soft_skills.append(skill)

        # -----------------------------
        # Job Title
        # -----------------------------

        title = None

        for job in self.job_titles:

            if re.search(

                rf"\b{re.escape(job)}\b",

                text,

                re.IGNORECASE

            ):

                title = job
                break

        # -----------------------------
        # Keywords
        # -----------------------------

        keywords = sorted(

            set(

                required_skills +

                preferred_skills +

                soft_skills

            )

        )

        # -----------------------------
        # Return
        # -----------------------------

        return {

            "raw_text": text,

            "job_title": title,

            "minimum_experience": minimum_experience,

            "required_skills": required_skills,

            "preferred_skills": preferred_skills,

            "soft_skills": soft_skills,

            "keywords": keywords

        }