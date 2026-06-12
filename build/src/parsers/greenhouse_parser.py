import requests

from src.parsers.base_parser import BaseParser


class GreenhouseParser(BaseParser):

    def run(self):

        print("[INFO] Greenhouse parser started")

        jobs = []

        board_token = self.company["board_token"]

        api_url = (
            f"https://boards-api.greenhouse.io/v1/boards/"
            f"{board_token}/jobs"
        )

        try:

            response = requests.get(
                api_url,
                timeout=30
            )

            print(
                f"[DEBUG] STATUS: "
                f"{response.status_code}"
            )

            if response.status_code != 200:

                print(
                    "[ERROR] Failed Greenhouse request"
                )

                return jobs

            data = response.json()

            postings = data.get(
                "jobs",
                []
            )

            print(
                f"[DEBUG] {self.company['company']} "
                f"GREENHOUSE JOBS: {len(postings)}"
            )

            for posting in postings:

                title = posting.get(
                    "title",
                    ""
                ).strip()

                location = (
                    posting.get(
                        "location",
                        {}
                    )
                    .get(
                        "name",
                        ""
                    )
                    .strip()
                )

                print(
                    f"[LOCATION] {location}"
                )

                job = {
                    "title": title,
                    "location": location,
                    "job_url": posting.get(
                        "absolute_url",
                        ""
                    )
                }

                jobs.append(job)

                print(
                    f"[JOB] {title} | {location}"
                )

        except Exception as e:

            print(
                f"[GREENHOUSE ERROR] "
                f"{str(e)}"
            )

        print(
            f"[DEBUG] TOTAL GREENHOUSE JOBS: "
            f"{len(jobs)}"
        )

        return jobs