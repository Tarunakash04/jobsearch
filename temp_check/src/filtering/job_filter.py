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

    def is_relevant(self, job: Job) -> bool:
        text = f"{job.title} {job.location or ''}".lower()

        # HARD REJECT FIRST
        for keyword in self.reject_keywords:
            if keyword in text:
                return False, f"Rejected due to keyword: {keyword}"

        # SOFT ACCEPT (cloud signal presence)
        for keyword in self.keep_keywords:
            if keyword in text:
                return True, f"Matched cloud signal: {keyword}"

        # fallback: reject unknown noise
        return False, "No cloud relevance signals found"