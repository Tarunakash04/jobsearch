from src.filtering.job_filter import JobFilter
from src.scoring.relevance_engine import RelevanceEngine
from src.notifications.telegram_notifier import TelegramNotifier
from src.storage.dynamodb_client import DynamoDBClient
from src.models.job import Job

import json
import os


db = DynamoDBClient()


# -----------------------------
# LOAD COMPANIES
# -----------------------------
def load_companies():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(
        base_dir,
        "..",
        "config",
        "companies.json"
    )

    with open(config_path, "r") as f:
        return json.load(f)


# -----------------------------
# NORMALIZER
# -----------------------------
def normalize_job(job, company_name, ats_type):

    if isinstance(job, Job):
        return job

    return Job(

        job_id=job.get("job_url"),
        external_job_id=job.get("job_url"),
        company=company_name,
        source_ats=ats_type,
        title=job.get("title"),
        location=job.get("location"),
        job_url=job.get("job_url"),

        posted_date=job.get("posted_date"),
        experience_text=None,
        short_description=None,
        skills=[],
        relevancy_score=0,
        matched_keywords=[],
        scraped_at=""
    )


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():

    companies = load_companies()

    filter_engine = JobFilter()
    scorer = RelevanceEngine()
    db = DynamoDBClient()

    all_jobs = []
    filtered_jobs = []
    failed_companies = []

    location_pass = 0
    relevance_pass = 0

    for company in companies:

        try:

            ats_type = company.get("ats", "").lower()

            # -----------------------------
            # PARSER ROUTING
            # -----------------------------
            if ats_type == "smartrecruiters":

                from src.parsers.smartrecruiters_parser import SmartRecruitersParser

                parser = SmartRecruitersParser(company)

            elif ats_type == "workday":

                from src.parsers.workday_parser import WorkdayParser

                parser = WorkdayParser(company)

            elif ats_type == "greenhouse":

                from src.parsers.greenhouse_parser import GreenhouseParser

                parser = GreenhouseParser(company)

            else:

                print(f"[WARNING] Unsupported ATS: {ats_type}")
                continue

            # -----------------------------
            # RUN PARSER
            # -----------------------------
            jobs = parser.run()

            print(f"\n[DEBUG] {company['company']} RAW JOBS: {len(jobs)}")

            if jobs:
                print("[DEBUG SAMPLE]", jobs[0])

            all_jobs.extend(jobs)

            # -----------------------------
            # PROCESS JOBS
            # -----------------------------
            for raw_job in jobs:

                job = normalize_job(
                    raw_job,
                    company["company"],
                    ats_type
                )

                # LOCATION FILTER
                if not filter_engine.is_location_allowed(job.location):
                    continue

                location_pass += 1

                # RELEVANCE FILTER
                allowed, reason = filter_engine.is_relevant(job)

                if not allowed:
                    continue

                relevance_pass += 1

                # SCORE
                score_data = scorer.score(job)

                job.relevancy_score = score_data["score"]
                job.matched_keywords = score_data["reasons"]

                print(f"[DEBUG SCORE] {job.title} -> {job.relevancy_score}")

                # DEDUP
                if db.job_exists(job.job_url):
                    continue

                filtered_jobs.append(job)

        except Exception as e:

            print(f"[ERROR] Failed for {company['company']}: {str(e)}")

            failed_companies.append({
                "company": company["company"],
                "error": str(e)
            })

    # -----------------------------
    # SUMMARY
    # -----------------------------
    print(f"\nRAW JOBS: {len(all_jobs)}")
    print(f"FILTERED JOBS (pre-final gate): {len(filtered_jobs)}")

    from collections import Counter

    locations = Counter()

    for job in all_jobs:

        location = None

        if isinstance(job, Job):
            location = job.location
        else:
            location = job.get("location")

        locations[location or "EMPTY"] += 1

    print("\nTOP 100 LOCATIONS")

    for loc, count in locations.most_common(100):
        print(f"{count:4} | {loc}")

    filtered_jobs.sort(
        key=lambda x: x.relevancy_score,
        reverse=True
    )

    print("\n[DEBUG SCORE DISTRIBUTION]")

    for j in filtered_jobs:
        print(j.title, j.location, j.relevancy_score)

    # -----------------------------
    # FINAL THRESHOLD
    # -----------------------------
    THRESHOLD = 6

    final_jobs = [
        j for j in filtered_jobs
        if j.relevancy_score >= THRESHOLD
    ]

    print("\n[DEBUG FINAL COUNT]", len(final_jobs))
    print("[DEBUG FINAL IDS]", [j.job_id for j in final_jobs])

    # -----------------------------
    # TELEGRAM
    # -----------------------------
    def format_jobs(jobs):

        if not jobs:
            return "⚠️ No high-quality jobs found today."

        msg = "🔥 High-Quality Job Matches\n\n"

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

    message = format_jobs(final_jobs)

    print("[DEBUG TELEGRAM PAYLOAD SIZE]", len(message))

    notifier.send_message(message)

    # -----------------------------
    # DYNAMODB SAVE
    # -----------------------------
    for job in final_jobs:
        db.save_job(job)

    print("[PIPELINE COMPLETED SUCCESSFULLY]")


if __name__ == "__main__":
    run_pipeline()