import os
import requests
import google.generativeai as genai

from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class GeminiParser:

    def __init__(self):

        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = genai.GenerativeModel(
        "gemini-2.0-flash"
        )

    def fetch_page_text(self, url):

        try:

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=20
            )

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            # token safety
            return text[:5000]

        except Exception as e:

            print(f"[FETCH ERROR] {url} -> {e}")
            return None

    def parse_job(self, url):

        page_text = self.fetch_page_text(url)

        if not page_text:
            return None

        prompt = f"""
You are a job extraction engine.

Extract ONLY if this is a REAL technical/cloud/infrastructure/software role.

Return STRICT JSON ONLY.

Required JSON format:

{{
  "valid_job": true,
  "title": "",
  "location": "",
  "seniority": "",
  "cloud_relevance_score": 0,
  "summary": "",
  "skills": []
}}

Rules:
- cloud_relevance_score must be from 0 to 10
- Reject non-technical jobs
- Reject sales jobs
- Reject HR jobs
- Reject marketing jobs
- Reject finance jobs

Job page content:
{page_text}
"""

        try:

            response = self.model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            print(f"[GEMINI ERROR] {url} -> {e}")
            return None