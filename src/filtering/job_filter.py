from src.models.job import Job


class JobFilter:

    def __init__(self):

        # ---------------------------------
        # HARD REJECT SIGNALS
        # ---------------------------------
        self.reject_keywords = [
            "sales",
            "account executive",
            "marketing",
            "recruiter",
            "human resources",
            "hr",
            "finance",
            "business analyst",
            "consultant",
            "customer success"
        ]

        # ---------------------------------
        # SENIORITY REJECTION
        # ---------------------------------
        self.seniority_keywords = [
            "senior",
            "staff",
            "principal",
            "lead",
            "director",
            "architect",
            "head"
        ]

        # ---------------------------------
        # MUST-KEEP CLOUD SIGNALS
        # ---------------------------------
        self.keep_keywords = [
            "cloud",
            "aws",
            "devops",
            "sre",
            "linux",
            "infrastructure",
            "network",
            "security",
            "platform",
            "support engineer",
            "site reliability",
            "backend",
            "systems",
            "infra",
            "cybersecurity",
            "kubernetes",
            "docker",
            "observability"
        ]

        # ---------------------------------
        # FRESHER SIGNALS
        # ---------------------------------
        self.fresher_keywords = [
            "intern",
            "internship",
            "new grad",
            "graduate",
            "entry level",
            "associate",
            "junior",
            "early career",
            "fresher"
        ]

    # ---------------------------------
    # LOCATION FILTER (STRICT CHENNAI ONLY)
    # ---------------------------------
    def is_location_allowed(self, location: str) -> bool:

        if not location:
            return False

        loc = location.lower().replace(" ", "")

        allowed_tokens = [
            "chennai",
            "madras",
            "bangalore",
            "bengaluru",
            "blr",
            "bengaluruurban"
        ]

        return any(token in loc for token in allowed_tokens)

    # ---------------------------------
    # MAIN FILTER ENGINE
    # ---------------------------------
    def is_relevant(self, job: Job):

        text = f"{job.title} {job.location or ''}".lower()

        # 1. LOCATION FILTER
        if not self.is_location_allowed(job.location):
            return False, "Location not Chennai"

        # 2. SENIORITY FILTER
        for keyword in self.seniority_keywords:
            if keyword in text:
                return False, f"Senior role filtered: {keyword}"

        # 3. HARD REJECT FILTER
        for keyword in self.reject_keywords:
            if keyword in text:
                return False, f"Rejected due to keyword: {keyword}"

        # 4. FRESHER BOOST
        for keyword in self.fresher_keywords:
            if keyword in text:
                return True, f"Matched fresher signal: {keyword}"

        # 5. CLOUD / INFRA SIGNALS
        for keyword in self.keep_keywords:
            if keyword in text:
                return True, f"Matched cloud signal: {keyword}"

        # 6. DEFAULT REJECT
        return False, "No cloud relevance signals found"