from src.parsers.greenhouse_parser import GreenhouseParser
from src.filtering.job_filter import JobFilter
from src.scoring.relevance_engine import RelevanceEngine
from src.notifications.telegram_notifier import TelegramNotifier
import json
import os
from src.storage.dynamodb_client import DynamoDBClient

from temp_check.src.models import job

db = DynamoDBClient()

def load_companies():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "..", "config", "companies.json")

    with open(config_path, "r") as f:
        return json.load(f)


def run_pipeline():
    companies = load_companies()

    filter_engine = JobFilter()
    scorer = RelevanceEngine()

    all_jobs = []
    filtered_jobs = []

    for company in companies:
        parser = GreenhouseParser(company)
        jobs = parser.run()

        print(f"[DEBUG] Raw jobs from {company['company']}: {len(jobs)}")

        all_jobs.extend(jobs)

        if jobs:
            print("[DEBUG SAMPLE]", jobs[0].title)

        for job in jobs:
            allowed, reason = filter_engine.is_relevant(job)

            if not allowed:
                continue

            score_data = scorer.score(job)
            job.relevancy_score = score_data["score"]
            job.matched_keywords = score_data["reasons"]

    # -----------------------------
    # DEDUPE CHECK (NEW LOGIC)
    # -----------------------------
            if db.job_exists(job.job_url):
                continue

            filtered_jobs.append(job)

            print("\n[JOB OBJECT DEBUG]")
            print(vars(job))
            
            print("[DEBUG SCORE CHECK]")
            for j in filtered_jobs:
                print(j.title, j.relevancy_score, type(j.relevancy_score))

    print(f"\nRAW JOBS: {len(all_jobs)}")
    print(f"FILTERED JOBS: {len(filtered_jobs)}\n")

    # 🔥 EVERYTHING BELOW MUST BE INSIDE FUNCTION

    filtered_jobs.sort(key=lambda x: x.relevancy_score, reverse=True)

    top_jobs = [job for job in filtered_jobs if job.relevancy_score >= 6]


    def format_jobs(jobs):
        if not jobs:
            return "No jobs met the threshold today (≥ 6)."

        msg = "🔥 High-Quality Job Matches (Score ≥ 6)\n\n"

        for i, job in enumerate(jobs, 1):
            msg += (
                f"{i}. {job.title}\n"
                f"🏢 {job.company}\n"
                f"📍 {job.location}\n"
                f"⭐ Score: {job.relevancy_score}\n"
                f"🔗 {job.job_url}\n\n"
            )

        return msg


    notifier = TelegramNotifier()
    message = format_jobs(top_jobs)

    if top_jobs:
        notifier.send_message(message)

        # SAVE ONLY AFTER SUCCESSFUL SEND
        for job in top_jobs:
            db.save_job(job)

if __name__ == "__main__":
    run_pipeline()