from abc import ABC, abstractmethod
from typing import List, Dict, Any

from models.job import Job


class BaseParser(ABC):
    """
    Contract for all ATS parsers.
    Every ATS must implement this interface.
    """

    def __init__(self, company_config: Dict[str, Any]):
        self.company_config = company_config
        self.company_name = company_config.get("company")
        self.base_url = company_config.get("url")

    @abstractmethod
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        """
        Step 1: Fetch raw job data from ATS source.
        Must return raw JSON / dict list (NOT Job objects yet).
        """
        pass

    @abstractmethod
    def parse_job(self, raw_job: Dict[str, Any]) -> Job:
        """
        Step 2: Convert raw ATS job → standardized Job model.
        """
        pass

    def run(self) -> List[Job]:
        """
        Full pipeline:
        fetch → parse → return standardized jobs
        """
        raw_jobs = self.fetch_jobs()

        jobs = []
        for raw in raw_jobs:
            try:
                job = self.parse_job(raw)
                jobs.append(job)
            except Exception as e:
                # We never want one bad job breaking the pipeline
                print(f"[PARSER ERROR] {self.company_name}: {e}")

        return jobs