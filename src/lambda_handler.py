
from src.handlers.job_runner import run_pipeline


def lambda_handler(event, context):
    """
    AWS Lambda entry point for ApplySei pipeline
    """

    print("[ApplySei] Lambda triggered")

    try:

        run_pipeline()

        return {
            "statusCode": 200,
            "body": "Pipeline executed successfully"
        }

    except Exception as e:

        print(f"[ERROR] {e}")

        return {
            "statusCode": 500,
            "body": str(e)
        }


if __name__ == "__main__":

    print("[LOCAL TEST] Triggering Lambda handler")

    result = lambda_handler({}, {})

    print("[RESULT]", result)
