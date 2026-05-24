from firecrawl import FirecrawlApp
from dotenv import load_dotenv

import os
import re

load_dotenv()


class FirecrawlParser:

    def __init__(self, company):

        self.company = company
        self.url = company["url"]

        self.app = FirecrawlApp(
            api_key=os.getenv("FIRECRAWL_API_KEY")
        )

    def run(self):

        jobs = []

        try:

            # ---------------------------------
            # SINGLE COMPANY PAGE SCRAPE
            # ---------------------------------
            result = self.app.scrape_url(
                self.url,
                formats=["markdown"]
            )

            content = result.markdown

            print("\n========== CONTENT PREVIEW ==========\n")
            print(content[:3000])

            # ---------------------------------
            # EXTRACT SMARTRECRUITERS JOB URLS
            # ---------------------------------
            job_urls = re.findall(
                r"https://jobs\.smartrecruiters\.com/[^\)\s]+",
                content
            )

            # ---------------------------------
            # REMOVE DUPLICATES
            # ---------------------------------
            job_urls = list(set(job_urls))

            print(f"\n[DEBUG] TOTAL JOB URLS FOUND: {len(job_urls)}\n")

            # ---------------------------------
            # RETURN ONLY URLS
            # ---------------------------------
            for url in job_urls:

                cleaned_url = url.strip()

                jobs.append({
                    "job_url": cleaned_url
                })

                print(f"[JOB URL] {cleaned_url}")

        except Exception as e:

            print(f"[FIRECRAWL ERROR] {self.url} -> {str(e)}")

        return jobs