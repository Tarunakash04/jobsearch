import hashlib


def generate_job_id(company: str, title: str, location: str, url: str) -> str:
    """
    Stable deduplication key across ATS systems.
    """

    base = f"{company}|{title}|{location}|{url}"

    return hashlib.sha256(base.encode()).hexdigest()