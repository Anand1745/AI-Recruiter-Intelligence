import re


class JDParser:

    def parse(self, jd_text):
        jd = {}

        jd["text"] = jd_text.strip()

        experience = re.search(
            r"(\d+)\+?\s*years?",
            jd_text.lower()
        )

        jd["min_experience"] = (
            int(experience.group(1))
            if experience
            else 0
        )

        return jd