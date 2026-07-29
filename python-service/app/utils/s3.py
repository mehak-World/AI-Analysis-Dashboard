import io

import boto3
import pandas as pd

from app.core.config import settings


s3_client = boto3.client(
    "s3",
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


async def load_dataframe_from_s3(s3_key: str) -> pd.DataFrame:
    """
    Downloads a CSV from S3 and loads it into a pandas DataFrame.

    Args:
        s3_key: The object key in S3.
                Example: uploads/12345/data.csv

    Returns:
        pandas.DataFrame

    Raises:
        Exception if the file cannot be downloaded or parsed.
    """

    response = s3_client.get_object(
        Bucket=settings.AWS_S3_BUCKET,
        Key=s3_key,
    )

    csv_bytes = response["Body"].read()

    df = pd.read_csv(io.BytesIO(csv_bytes))

    return df