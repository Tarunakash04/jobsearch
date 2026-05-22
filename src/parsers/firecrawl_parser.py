from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()


class FirecrawlParser:

    def __init__(self, company):
        self.company = company
        self.url = company["url"]

        self.app = FirecrawlApp(
            api_key=os.getenv("FIRECRAWL_API_KEY")
        )

    def extract_json_ld(self, markdown):
        """
        Try to extract SmartRecruiters structured JSON if present
        """
        json_blocks = re.findall(
            r"<script type=\"application/ld\+json\">(.*?)</script>",
            markdown,
            re.DOTALL
        )

        jobs = []

        for block in json_blocks:
            try:
                data = json.loads(block.strip())

                if isinstance(data, dict):
                    if "title" in data and "hiringOrganization" in data:
                        jobs.append(data)

            except:
                continue

        return jobs

    def run(self):

        jobs = []

        result = self.app.scrape_url(
            self.url,
            formats=["markdown"]
        )

        content = result.markdown.lower()

        # -----------------------------
        # QUICK GLOBAL CHECK (no regex filtering yet)
        # -----------------------------
        job_urls = re.findall(
            r"https://jobs\.smartrecruiters\.com/[^\)\s]+",
            content
        )

        job_urls = list(set(job_urls))

        for url in job_urls:

            try:
                detail = self.app.scrape_url(url, formats=["markdown"])

                md = detail.markdown

                # -----------------------------
                # LOCATION CHECK (SAFE VERSION)
                # -----------------------------
                if not any(x in md.lower() for x in ["chennai", "india"]):
                    continue

                # -----------------------------
                # TITLE EXTRACTION (fallback regex)
                # -----------------------------
                title_match = re.search(r"\*\*(.*?)\*\*", md)
                title = title_match.group(1).strip() if title_match else "Unknown Role"

                jobs.append({
                    "title": title,
                    "location": "Chennai",
                    "job_url": url
                })

                print(f"[MATCHED] {title}")

            except Exception as e:
                print(f"[ERROR] {url} -> {e}")

        return jobs