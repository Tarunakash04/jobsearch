import requests


class WorkdayParser:

    def __init__(self, company):

        self.company = company
        self.url = company["url"]

        # -----------------------------
        # SAFETY CHECK (IMPORTANT FIX)
        # -----------------------------
        if "wday" not in self.url:
            raise Exception("Invalid Workday API URL")

    def run(self):

        payload = {
            "appliedFacets": {},
            "limit": 20,
            "offset": 0,
            "searchText": ""
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        try:
            response = requests.post(
                self.url,
                json=payload,
                headers=headers,
                timeout=15
            )

        except Exception as e:
            raise Exception(f"Workday request failed: {str(e)}")

        # -----------------------------
        # ERROR HANDLING (IMPORTANT FIX)
        # -----------------------------
        if response.status_code != 200:
            print("[WORKDAY RAW RESPONSE]", response.text[:500])
            raise Exception(f"Workday fetch failed: {response.status_code}")

        data = response.json()

        # -----------------------------
        # SAFE PARSING (CRITICAL FIX)
        # -----------------------------
        jobs = (
            data.get("jobPostings")
            or data.get("postings")
            or data.get("jobs")
            or []
        )

        print(f"[WORKDAY DEBUG] Jobs fetched: {len(jobs)}")

        if jobs:
            print("\n[WORKDAY SAMPLE JOB]")
            print(jobs[0])

        return jobs