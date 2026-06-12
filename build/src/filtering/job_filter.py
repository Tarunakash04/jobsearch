from src.models.job import Job


class JobFilter:

    def __init__(self):

        # -----------------------------
        # HARD NON-TECH REJECTS
        # -----------------------------
        self.reject_keywords = [
            "marketing",
            "sales",
            "account executive",
            "business development",
            "hr",
            "human resources",
            "recruiter",
            "finance",
            "accounting",
            "customer success",
            "operations manager",
            "field sales",
            "partnership manager",
            "talent acquisition",
            "people operations",
            "customer support representative",
            "legal",
            "counsel",
            "attorney"
        ]

        # -----------------------------
        # EXECUTIVE BLOCK
        # -----------------------------
        self.executive_keywords = [
            "vice president",
            "chief ",
            "cto",
            "ceo",
            "ciso",
            "coo"
        ]

        # -----------------------------
        # SENIORITY BLOCK
        # -----------------------------
        self.seniority_keywords = [
            "senior",
            "staff",
            "principal",
            "lead",
            "manager",
            "director",
            "head ",
            "head of",
            "architect"
        ]

        # -----------------------------
        # ENGINEERING SIGNALS
        # -----------------------------
        self.tech_keywords = [

            # cloud
            "cloud",
            "aws",
            "azure",
            "gcp",

            # infra
            "infrastructure",
            "infra",
            "platform",

            # devops / sre
            "devops",
            "sre",
            "site reliability",

            # tooling
            "terraform",
            "kubernetes",
            "docker",
            "linux",
            "ansible",

            # security
            "security engineer",

            # engineering
            "software engineer",
            "backend engineer",
            "systems engineer",
            "network engineer",
            "data engineer",
            "platform engineer",
            "cloud engineer",
            "devops engineer",
            "site reliability engineer",

            # generic
            "engineer",
            "developer"
        ]

    # -----------------------------
    # LOCATION FILTER
    # -----------------------------
    def is_location_allowed(self, location: str) -> bool:

        if not location:
            return False

        loc = location.lower()

        allowed_locations = [
            "chennai",
            "tamil nadu"
        ]

        return any(
            keyword in loc
            for keyword in allowed_locations
        )

    # -----------------------------
    # MAIN FILTER
    # -----------------------------
    def is_relevant(self, job: Job):

        text = f"{job.title} {job.location or ''}".lower()

        # -----------------------------
        # HARD NON-TECH REJECTS
        # -----------------------------
        for kw in self.reject_keywords:
            if kw in text:
                return False, f"Rejected non-tech role: {kw}"

        # -----------------------------
        # EXECUTIVE BLOCK
        # -----------------------------
        for kw in self.executive_keywords:
            if kw in text:
                return False, f"Rejected executive role: {kw}"

        # -----------------------------
        # SENIORITY BLOCK
        # -----------------------------
        for kw in self.seniority_keywords:
            if kw in text:
                return False, f"Rejected senior role: {kw}"

        # -----------------------------
        # TECH SIGNAL
        # -----------------------------
        for kw in self.tech_keywords:
            if kw in text:
                return True, f"Matched tech keyword: {kw}"

        # -----------------------------
        # FALLBACK
        # -----------------------------
        if "engineer" in text or "developer" in text:
            return True, "Generic engineering role"

        return False, "No tech relevance"