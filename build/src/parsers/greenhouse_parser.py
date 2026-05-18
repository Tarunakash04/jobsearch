import requests
from typing import List, Dict, Any

from src.parsers.base_parser import BaseParser
from src.models.job import Job
from src.utils.hashing import generate_job_id


class GreenhouseParser(BaseParser):

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        company_slug = self.company_config.get("slug")

        url = f"https://boards-api.greenhouse.io/v1/boards/{company_slug}/jobs"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch jobs for {self.company_name}")

        return response.json().get("jobs", [])

    def parse_job(self, raw_job: Dict[str, Any]) -> Job:
        title = raw_job.get("title")
        location = raw_job.get("location", {}).get("name")
        job_url = raw_job.get("absolute_url")
        external_id = str(raw_job.get("id"))
        updated_at = raw_job.get("updated_at")

        job_id = generate_job_id(
            self.company_name,
            title,
            location,
            job_url
        )

        return Job(
            job_id=job_id,
            external_job_id=external_id,
            company=self.company_name,
            source_ats="greenhouse",
            title=title,
            location=location,
            job_url=job_url,
            posted_date=updated_at,
            experience_text=None,
            short_description=None,
            skills=[],
            scraped_at=""
        )