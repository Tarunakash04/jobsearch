from dataclasses import dataclass, field
from typing import List, Optional, Dict


@dataclass
class Job:
    # ---------- Identity ----------
    job_id: str  # internal hash (dedup key)
    external_job_id: Optional[str]  # ATS-provided ID if exists
    company: str
    source_ats: str  # greenhouse / lever / workday

    # ---------- Core Info ----------
    title: str
    location: Optional[str]
    job_url: str
    posted_date: Optional[str]

    # ---------- Extracted Signals ----------
    experience_text: Optional[str]
    short_description: Optional[str]
    skills: List[str] = field(default_factory=list)

    # ---------- Intelligence Layer ----------
    relevancy_score: int = 0
    matched_keywords: List[str] = field(default_factory=list)

    # ---------- System Metadata ----------
    scraped_at: str = ""