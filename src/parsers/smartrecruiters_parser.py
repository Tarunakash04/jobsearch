import re

from firecrawl import FirecrawlApp

from src.parsers.base_parser import BaseParser


class SmartRecruitersParser(BaseParser):

    def __init__(self, company):

        super().__init__(company)

        self.company_name = company["company"]
        self.url = company["url"]

        self.firecrawl = FirecrawlApp()

    # -----------------------------------
    # MAIN
    # -----------------------------------
    def run(self):

        try:

            response = self.firecrawl.scrape_url(
                self.url,
                formats=["markdown"]
            )

            markdown = response.markdown

            print("\n========== CONTENT PREVIEW ==========\n")
            print(markdown[:5000])

            jobs = self.extract_jobs(markdown)

            return jobs

        except Exception as e:

            print(f"[ERROR] SmartRecruiters parser failed: {str(e)}")

            return []

    # -----------------------------------
    # EXTRACTION
    # -----------------------------------
    def extract_jobs(self, markdown):

        jobs = []

        urls = re.findall(
            r"https://jobs\.smartrecruiters\.com/[^\s)]+",
            markdown
        )

        urls = list(set(urls))

        print(f"\n[DEBUG] TOTAL JOB URLS FOUND: {len(urls)}")

        for u in urls:
            print("[JOB URL]", u)

        for url in urls:

            slug = url.split("/")[-1]

            title = slug.replace("-", " ")
            title = re.sub(r"\d+", "", title)
            title = title.strip().title()

            if self.is_relevant(title):

                print(f"[MATCHED] {title}")

                jobs.append({
                    "title": title,
                    "location": "Chennai",
                    "job_url": url
                })

        return jobs

    # -----------------------------------
    # FILTER
    # -----------------------------------
    def is_relevant(self, title):

        text = title.lower()

        positive_keywords = [

            "cloud",
            "devops",
            "sre",
            "platform",
            "infrastructure",
            "backend",
            "software engineer",
            "systems engineer",
            "security engineer",
            "site reliability",
            "full stack",
            "java developer",
            "developer"
        ]

        negative_keywords = [

            "sales",
            "marketing",
            "account executive",
            "customer success",
            "business development",
            "finance",
            "hr",
            "recruiter",
            "consultant"
        ]

        for k in negative_keywords:
            if k in text:
                return False

        for k in positive_keywords:
            if k in text:
                return True

        return False