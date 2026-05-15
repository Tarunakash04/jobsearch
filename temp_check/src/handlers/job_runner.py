from src.parsers.greenhouse_parser import GreenhouseParser
from src.filtering.job_filter import JobFilter
from src.scoring.relevance_engine import RelevanceEngine
import json

def load_companies():
    with open("src/config/companies.json", "r") as f:
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

        # ✅ DEBUG LINE (your request added properly)
        print(f"[DEBUG] Raw jobs from {company['company']}: {len(jobs)}")

        # store raw jobs properly
        all_jobs.extend(jobs)

        # quick sanity sample
        if jobs:
            print("[DEBUG SAMPLE]", jobs[0].title)

        for job in jobs:
            allowed, reason = filter_engine.is_relevant(job)

            if not allowed:
                continue

            score_data = scorer.score(job)
            job.relevancy_score = score_data["score"]
            job.matched_keywords = score_data["reasons"]

            filtered_jobs.append(job)

    print(f"\nRAW JOBS: {len(all_jobs)}")
    print(f"FILTERED JOBS: {len(filtered_jobs)}\n")

    for job in filtered_jobs[:10]:
        print({
            "company": job.company,
            "title": job.title,
            "location": job.location,
            "score": job.relevancy_score,
            "reasons": job.matched_keywords[:3],
            "url": job.job_url
        })

if __name__ == "__main__":
    run_pipeline()