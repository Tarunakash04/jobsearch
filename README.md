# ApplySei Job Search Pipeline

Automates scraping and ranking of cloud-based engineering roles from multiple ATS sources, filters for relevance, sends a daily shortlist to Telegram, and persists seen jobs in DynamoDB to avoid duplicates.


---

## What this repo does

1. **Loads configured companies/ATS endpoints** from `src/config/companies.json`.
2. For each company, **runs the matching ATS parser** (Workday / Greenhouse / SmartRecruiters / etc.).
3. **Normalizes** raw job dicts into a `Job` dataclass.
4. **Filters** jobs:
   - Location gate (currently Chennai/Tamil Nadu only)
   - Rejects obvious non-target roles (sales/marketing/HR/etc.)
   - Rejects executive/senior leadership keywords
   - Requires at least one tech keyword match (fallback for generic engineer/developer)
5. **Scores** jobs using `src/scoring/relevance_engine.py` and `src/scoring/job_classifier.py`.
6. **Deduplicates** via DynamoDB (`applysei_jobs` table, keyed by `job_url`).
7. Sends the top matches to Telegram.
8. Saves accepted jobs to DynamoDB.

---

## Architecture (high level)

- Entry point: `src/lambda_handler.py`
- Pipeline orchestration: `src/handlers/job_runner.py`
- Data model: `src/models/job.py`
- Filtering: `src/filtering/job_filter.py`
- Scoring:
  - `src/scoring/job_classifier.py` (domain + seniority classification)
  - `src/scoring/relevance_engine.py` (final score + keyword reasons)
- ATS parsing:
  - `src/parsers/*_parser.py`
  - `src/parsers/parser_factory.py` (optional routing)
- Integrations:
  - Telegram: `src/notifications/telegram_notifier.py`
  - DynamoDB: `src/storage/dynamodb_client.py`

---

## Project structure

- `src/`
  - `config/companies.json` – list of target companies and their ATS configuration
  - `handlers/job_runner.py` – scrape → filter → score → notify → persist
  - `models/job.py` – `Job` dataclass
  - `parsers/` – ATS scrapers/extractors
  - `filtering/` – location + keyword gating
  - `scoring/` – job classification + scoring logic
  - `notifications/` – Telegram sender
  - `storage/` – DynamoDB dedupe + persistence
  - `utils/` – small helpers (e.g., hashing)

---

## Configuration

### 1) `src/config/companies.json`

This file controls what companies are scraped and which parser to use.

Each entry includes at least:
- `company`
- `ats` (e.g. `workday`, `greenhouse`, `smartrecruiters`)

Additional fields are ATS-specific (example: Workday uses fields like `career_base_url` / `api_url`; Greenhouse uses `board_token`).

> Security note: do not commit ATS API endpoints/keys you wouldn’t want to share publicly. Keep secrets in environment variables or your deployment platform.

> Note: there is also a top-level `companies.txt`, but the pipeline uses `src/config/companies.json`.

---

## Required environment variables

### Telegram
Required by `src/notifications/telegram_notifier.py`:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

These must be set in your runtime environment (local or AWS Lambda).

### AWS / DynamoDB
`src/storage/dynamodb_client.py` uses `boto3` and expects AWS credentials in the standard boto3 locations (e.g., IAM role in Lambda or `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` locally).

- DynamoDB table name: `applysei_jobs`
- Region in code: `us-west-2`
- Primary key used for dedupe: `job_url`

---

## How to run locally

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Set env vars

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`
- plus AWS credentials for DynamoDB access

### 3) Run the pipeline

```bash
python src/lambda_handler.py
```

or directly:

```bash
python -c "from src.handlers.job_runner import run_pipeline; run_pipeline()"
```

---

## AWS deployment & scheduling

### AWS services used
- **AWS Lambda**: runs the job scraping + filtering + scoring pipeline (triggered by EventBridge).
- **Amazon EventBridge Scheduler (cron)**: schedules the Lambda to run **once a day at 8:00 AM**.
- **Amazon DynamoDB**: stores job records and performs deduplication in the `applysei_jobs` table.
- **Amazon CloudWatch Logs/metrics**: captures Lambda logs (prints/exceptions) so you can monitor executions and troubleshoot failures.

### Build / deployment (AWS Lambda)

Architecture diagram:
- `Architecture.png`

The repo includes a PowerShell script to package the code:



- `rebuild.ps1`
  - cleans `build/`
  - copies `src/` into `build/src/`
  - installs a minimal set of dependencies into `build/`
  - creates `lambda_package.zip`

Run:

```powershell
.trebuild.ps1
```

Upload `lambda_package.zip` to your Lambda deployment.

---

## Filtering + scoring behavior (summary)

### Location filter
- Accepts jobs where `location` contains: `chennai` or `tamil nadu`
- Jobs without `location` are rejected.

### Relevance filter
- Rejects roles containing non-target keywords (marketing/sales/HR/etc.)
- Rejects executive-ish titles (VP/CEO/CTO/CISO/COO keywords)
- Rejects high-seniority leadership keywords (lead/manager/director/head/architect, etc.)
- Accepts jobs that match at least one tech keyword
- Fallback: if the title contains `engineer` or `developer`, it may pass

### Scoring
- `JobClassifier` classifies domain (cloud core / platform / engineering / leadership / noise)
- `JobClassifier` classifies seniority (fresher/mid/senior/manager/staff/executive)
- `RelevanceEngine` computes a bounded score (clamped to `[-10, 10]`) based on:
  - domain + seniority base adjustments
  - keyword boosts
  - keyword penalties

### Final threshold
- Only jobs with `relevancy_score >= 5` are included in the Telegram message.

---

## Tests

- `src/test_telegram.py` – sends a Telegram test message (requires Telegram env vars)
- `test.py` – quick outbound request example (Workday API call)

---

## Notes / caveats

- ATS parsing quality varies by source; some parsers scrape HTML/markdown and rely on regex extraction.
- DynamoDB dedupe is currently based on `job_url`.
- If a parser fails for a company, the pipeline continues and records the company error in `failed_companies`.

---

## License

This project is licensed under the MIT License. See the included `LICENSE` file for full terms.
