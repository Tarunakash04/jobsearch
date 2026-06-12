class JobClassifier:

    def __init__(self):

        # -----------------------------
        # CLOUD / DEVOPS / INFRA CORE
        # -----------------------------
        self.cloud_core = [
            "cloud engineer",
            "cloud support engineer",
            "cloud support",
            "devops engineer",
            "devops",
            "site reliability engineer",
            "sre",
            "platform engineer",
            "infrastructure engineer",
            "infra engineer",
            "security engineer",
            "devsecops",
            "systems engineer",
            "production engineer",
            "network engineer",
            "cloud operations",
            "platform operations"
        ]

        # -----------------------------
        # GENERAL ENGINEERING
        # -----------------------------
        self.engineering = [
            "software engineer",
            "backend engineer",
            "backend developer",
            "java developer",
            "python developer",
            "full stack engineer",
            "fullstack engineer",
            "application developer",
            "developer",
            "engineer"
        ]

        # -----------------------------
        # PLATFORM / SYSTEMS
        # -----------------------------
        self.platform = [
            "platform",
            "infrastructure",
            "systems",
            "linux",
            "kubernetes",
            "docker",
            "terraform",
            "aws",
            "azure",
            "gcp"
        ]

        # -----------------------------
        # HARD NOISE REJECTS
        # -----------------------------
        self.noise = [
            "account executive",
            "sales",
            "marketing",
            "recruiter",
            "hr",
            "finance",
            "customer success",
            "business analyst",
            "consultant",
            "talent acquisition",
            "human resources",
            "field sales"
        ]

        # -----------------------------
        # SENIORITY MAP
        # -----------------------------
        self.seniority_map = {
            "intern": "FRESHER",
            "graduate": "FRESHER",
            "junior": "FRESHER",
            "entry": "FRESHER",
            "associate": "FRESHER",
            "fresher": "FRESHER",

            "senior": "SENIOR",
            "sr": "SENIOR",
            "lead": "SENIOR",

            "staff": "STAFF",
            "principal": "STAFF",

            "manager": "MANAGER"
        }

        # -----------------------------
        # ENGINEERING LEADERSHIP
        # -----------------------------
        self.leadership = [
            "engineering manager",
            "technical lead",
            "tech lead",
            "lead engineer",
            "lead software engineer",
            "lead platform engineer"
        ]

    # -------------------------------------------------
    # DOMAIN CLASSIFICATION
    # -------------------------------------------------
    def classify_domain(self, title: str):

        text = title.lower()

        # -----------------------------
        # HARD NOISE FIRST
        # -----------------------------
        for r in self.noise:
            if r in text:
                return "NOISE"

        # -----------------------------
        # CLOUD CORE
        # -----------------------------
        for r in self.cloud_core:
            if r in text:
                return "CLOUD_CORE"

        # -----------------------------
        # PLATFORM
        # -----------------------------
        for r in self.platform:
            if r in text:
                return "PLATFORM"

        # -----------------------------
        # ENGINEERING
        # -----------------------------
        for r in self.engineering:
            if r in text:
                return "ENGINEERING"

        # -----------------------------
        # LEADERSHIP
        # -----------------------------
        for r in self.leadership:
            if r in text:
                return "LEADERSHIP"

        return "UNKNOWN"

    # -------------------------------------------------
    # SENIORITY CLASSIFICATION
    # -------------------------------------------------
    def classify_seniority(self, title: str):

        text = title.lower()

        for k, v in self.seniority_map.items():
            if k in text:
                return v

        return "UNKNOWN"