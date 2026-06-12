import requests


class WorkdayParser:

    def __init__(self, company):

        self.company = company

        self.api_url = company["api_url"]

        self.career_base_url = company["career_base_url"]

    def run(self):

        print(
            f"[INFO] Workday parser started: "
            f"{self.company['company']}"
        )

        jobs = []

        page_count = 0

        total_jobs = None

        seen_urls = set()

        payload = {
            "appliedFacets": {},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": self.career_base_url
        }

        try:

            while True:

                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=30
                )

                if response.status_code != 200:

                    print(
                        f"[ERROR] Workday request failed "
                        f"({response.status_code})"
                    )

                    print(response.text[:500])

                    break

                data = response.json()

                if total_jobs is None:
                    total_jobs = data.get("total", 0)

                postings = data.get(
                    "jobPostings",
                    []
                )

                if not postings:
                    break

                page_count += 1

                jobs_before_page = len(jobs)

                for posting in postings:

                    title = (
                        posting.get(
                            "title",
                            ""
                        ).strip()
                    )

                    location = (
                        posting.get(
                            "locationsText",
                            ""
                        ).strip()
                    )

                    external_path = (
                        posting.get(
                            "externalPath",
                            ""
                        ).strip()
                    )

                    if not external_path:
                        continue

                    full_url = (
                        self.career_base_url
                        + external_path
                    )

                    if full_url in seen_urls:
                        continue

                    seen_urls.add(full_url)

                    job = {
                        "title": title,
                        "location": location,
                        "job_url": full_url
                    }

                    jobs.append(job)

                jobs_after_page = len(jobs)

                if jobs_after_page == jobs_before_page:

                    print(
                        "[DEBUG] No new jobs found. "
                        "Stopping pagination."
                    )

                    break

                payload["offset"] += payload["limit"]

                if (
                    total_jobs
                    and payload["offset"] >= total_jobs
                ):
                    break

        except Exception as e:

            print(
                f"[WORKDAY ERROR] "
                f"{str(e)}"
            )

        print(
            f"[DEBUG] Pages: {page_count} | "
            f"Jobs: {len(jobs)}"
        )

        return jobs