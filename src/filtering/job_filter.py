from src.models.job import Job


class JobFilter:

    def __init__(self):

        # -----------------------------
        # HARD NON-TECH REJECTS ONLY
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
            "partnership manager"
        ]

        # -----------------------------
        # TRUE EXEC BLOCK
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
        # ENGINEERING SIGNALS
        # -----------------------------
        self.tech_keywords = [

            # cloud / infra
            "aws",
            "azure",
            "gcp",
            "cloud",
            "devops",
            "sre",
            "site reliability",
            "platform",
            "infrastructure",
            "infra",
            "terraform",
            "kubernetes",
            "docker",
            "linux",

            # engineering
            "software engineer",
            "backend engineer",
            "full stack engineer",
            "systems engineer",
            "data engineer",
            "network engineer",
            "security engineer",
            "developer",

            # generic engineering
            "engineer",
            "engineering"
        ]

    # -----------------------------
    # LOCATION FILTER
    # -----------------------------
    def is_location_allowed(self, location: str) -> bool:

        if not location:
            return True

        loc = location.lower()

        if any(x in loc for x in [
            "india",
            "chennai",
            "bangalore",
            "hyderabad",
            "pune",
            "remote"
        ]):
            return True

        blocked = [
            "united states",
            "usa",
            "canada",
            "germany",
            "uk",
            "france",
            "netherlands",
            "singapore"
        ]

        return not any(x in loc for x in blocked)

    # -----------------------------
    # MAIN FILTER
    # -----------------------------
    def is_relevant(self, job: Job):

        text = f"{job.title} {job.location or ''}".lower()

        # -----------------------------
        # HARD REJECTS
        # -----------------------------
        for kw in self.reject_keywords:
            if kw in text:
                return False, f"Rejected non-tech role: {kw}"

        # -----------------------------
        # EXEC BLOCK
        # -----------------------------
        for kw in self.executive_keywords:
            if kw in text:
                return False, f"Rejected executive role: {kw}"

        # -----------------------------
        # TECH SIGNAL
        # -----------------------------
        for kw in self.tech_keywords:
            if kw in text:
                return True, f"Matched tech keyword: {kw}"

        # -----------------------------
        # DEFAULT ALLOW ENGINEERING
        # -----------------------------
        if "engineer" in text or "developer" in text:
            return True, "Generic engineering role"

        return False, "No tech relevance"