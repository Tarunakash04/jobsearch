import requests
from bs4 import BeautifulSoup


class SmartRecruitersParser:

    def __init__(self, company):

        self.company = company
        self.url = company["url"]

    def run(self):

        response = requests.get(
            self.url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(response.text, "html.parser")

        jobs = []

        links = soup.find_all("a", href=True)

        for link in links:

            href = link["href"]
            title = link.get_text(strip=True)

            if "/744" not in href:
                continue

            if not title:
                continue

            # Chennai-only filter early
            page_text = link.parent.get_text(" ", strip=True).lower()

            if "chennai" not in page_text:
                continue

            jobs.append({
                "title": title,
                "location": "Chennai",
                "job_url": href
            })

            print(f"[MATCHED] {title}")

        return jobs