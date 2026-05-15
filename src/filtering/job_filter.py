from src.models.job import Job


class JobFilter:

    def __init__(self):
        # hard reject signals (fast elimination)
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

        # must-keep signals (cloud direction)
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
            "support engineer"
        ]

    def is_location_allowed(self, location: str) -> bool:
        if not location:
            return False

        loc = location.lower()

        # India cities
        india_keywords = [
            "bangalore",
            "bengaluru",
            "chennai",
            "madras"
        ]

        # allowed remote types
        safe_remote_keywords = [
            "remote india",
            "india remote",
            "remote (india)",
            "global remote",
            "worldwide",
            "anywhere"
        ]

        # blocked remote regions
        blocked_remote_keywords = [
            "united states",
            "usa",
            "us",
            "canada",
            "uk",
            "europe"
        ]

        # 1. direct India city match
        if any(k in loc for k in india_keywords):
            return True

        # 2. explicitly India/global safe remote
        if any(k in loc for k in safe_remote_keywords):
            return True

        # 3. block country-specific remote (US/Canada etc.)
        if "remote" in loc and any(k in loc for k in blocked_remote_keywords):
            return False

        # 4. plain "remote" fallback (unknown remote → allow for now)
        if "remote" in loc:
            return True

        return False

    def is_relevant(self, job: Job):

        text = f"{job.title} {job.location or ''}".lower()

        # 1. LOCATION FILTER (FIRST GATE)
        if not self.is_location_allowed(job.location):
            return False, "Location not allowed"

        # 2. HARD REJECT
        for keyword in self.reject_keywords:
            if keyword in text:
                return False, f"Rejected due to keyword: {keyword}"

        # 3. SOFT ACCEPT (positive signal)
        for keyword in self.keep_keywords:
            if keyword in text:
                return True, f"Matched cloud signal: {keyword}"

        # 4. DEFAULT REJECT
        return False, "No cloud relevance signals found"