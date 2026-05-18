class JobClassifier:

    def __init__(self):

        self.cloud_core = [
            "cloud engineer",
            "devops engineer",
            "site reliability engineer",
            "sre",
            "security engineer",
            "devsecops",
            "cloud support engineer"
        ]

        self.engineering = [
            "backend engineer",
            "software engineer",
            "systems engineer",
            "data engineer",
            "network engineer"
        ]

        self.platform = [
            "platform engineer",
            "infrastructure engineer",
            "developer experience",
            "full stack engineer"
        ]

        self.noise = [
            "account executive",
            "sales",
            "marketing",
            "recruiter",
            "hr",
            "finance",
            "consultant",
            "business analyst"
        ]

        self.seniority_map = {
            "intern": "FRESHER",
            "graduate": "FRESHER",
            "junior": "FRESHER",
            "entry": "FRESHER",
            "fresher": "FRESHER",

            "senior": "SENIOR",
            "sr": "SENIOR",

            "staff": "STAFF",
            "principal": "STAFF",

            "manager": "MANAGER",
            "lead": "SENIOR"
        }

        self.leadership = [
            "engineering manager",
            "technical lead",
            "tech lead",
            "program manager",
            "product manager",
            "lead engineer"
        ]

    def classify_domain(self, title: str):

        text = title.lower()

        for r in self.noise:
            if r in text:
                return "NOISE"

        for r in self.cloud_core:
            if r in text:
                return "CLOUD_CORE"

        for r in self.engineering:
            if r in text:
                return "ENGINEERING"

        for r in self.platform:
            if r in text:
                return "PLATFORM"

        for r in self.leadership:
            return "LEADERSHIP"

        return "UNKNOWN"

    def classify_seniority(self, title: str):

        text = title.lower()

        for k, v in self.seniority_map.items():
            if k in text:
                return v

        return "UNKNOWN"