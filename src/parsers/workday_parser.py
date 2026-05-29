import requests

class WorkdayParser:

    def __init__(self, company):

        self.company = company
        self.url = company["url"]

        # ---------------------------------
        # WORKDAY CONFIG
        # ---------------------------------

        self.api_url = (
            "https://barclays.wd3.myworkdayjobs.com/"
            "wday/cxs/barclays/"
            "External_Career_Site_Barclays/jobs"
        )

        self.career_base_url = (
            "https://barclays.wd3.myworkdayjobs.com"
            "/en-US/External_Career_Site_Barclays"
        )

    def run(self):

        print("[INFO] Workday parser started")

        jobs = []

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
            "Origin": "https://barclays.wd3.myworkdayjobs.com",
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

                print(f"[DEBUG] STATUS: {response.status_code}")

                if response.status_code != 200:

                    print("[ERROR] Failed request")
                    print(response.text[:500])

                    break

                data = response.json()

                postings = data.get("jobPostings", [])

                print(f"[DEBUG] JOBS FETCHED: {len(postings)}")

                if not postings:
                    break

                for posting in postings:

                    title = (
                        posting.get("title", "")
                        .strip()
                    )

                    location = (
                        posting.get("locationsText", "")
                        .strip()
                    )

                    external_path = (
                        posting.get("externalPath", "")
                        .strip()
                    )

                    if not external_path:
                        continue

                    # ---------------------------------
                    # CHENNAI FILTER
                    # ---------------------------------

                    if "chennai" not in location.lower():
                        continue

                    # ---------------------------------
                    # FIXED WORKDAY URL
                    # ---------------------------------

                    full_url = (
                        self.career_base_url
                        + external_path
                    )

                    job = {
                        "title": title,
                        "location": location,
                        "job_url": full_url
                    }

                    jobs.append(job)

                    print(f"[MATCHED] {title}")

                # ---------------------------------
                # NEXT PAGE
                # ---------------------------------

                payload["offset"] += payload["limit"]

        except Exception as e:

            print(f"[WORKDAY ERROR] {str(e)}")

        print(f"[DEBUG] TOTAL WORKDAY JOBS: {len(jobs)}")

        return jobs
