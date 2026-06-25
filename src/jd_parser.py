import re


class JDParser:

    def __init__(self):
        self.skill_list = [
            "Python",
            "Java",
            "C++",
            "SQL",
            "AWS",
            "Azure",
            "GCP",
            "Docker",
            "Kubernetes",
            "Spark",
            "Hadoop",
            "TensorFlow",
            "PyTorch",
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "Cloud",
            "Flask",
            "FastAPI",
            "React",
            "Node.js",
            "Git"
        ]

        self.soft_skill_list = [
            "Leadership",
            "Communication",
            "Teamwork",
            "Problem Solving",
            "Analytical Thinking",
            "Stakeholder Management"
        ]

    def parse(self, jd_text):

        text = jd_text.strip()

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

        required_skills = []

        for skill in self.skill_list:
            if skill.lower() in text.lower():
                required_skills.append(skill)

        soft_skills = []

        for skill in self.soft_skill_list:
            if skill.lower() in text.lower():
                soft_skills.append(skill)

        title = None

        title_match = re.search(
            r"(Backend Engineer|Software Engineer|Data Scientist|Machine Learning Engineer|Frontend Engineer|Full Stack Developer)",
            text,
            re.IGNORECASE
        )

        if title_match:
            title = title_match.group(1)

        keywords = list(
            set(
                required_skills +
                soft_skills
            )
        )

        return {

            "raw_text": text,

            "job_title": title,

            "minimum_experience": minimum_experience,

            "required_skills": required_skills,

            "preferred_skills": [],

            "soft_skills": soft_skills,

            "keywords": keywords
        }