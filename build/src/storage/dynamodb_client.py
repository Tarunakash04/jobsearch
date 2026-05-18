import boto3

TABLE_NAME = "applysei_jobs"

dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
table = dynamodb.Table(TABLE_NAME)


class DynamoDBClient:

    def job_exists(self, job_url: str) -> bool:
        response = table.get_item(
            Key={"job_url": job_url}
        )
        return "Item" in response

    def save_job(self, job):
        table.put_item(
            Item={
                "job_url": job.job_url,
                "external_job_id": job.external_job_id,
                "company": job.company,
                "source_ats": job.source_ats,
                "title": job.title,
                "location": job.location,
                "posted_date": job.posted_date,
                "relevancy_score": job.relevancy_score,
                "matched_keywords": job.matched_keywords,
                "scraped_at": job.scraped_at
            }
        )