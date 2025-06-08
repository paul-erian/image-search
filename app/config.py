import os
import boto3
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

bucket = os.getenv("BUCKET_NAME")

session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url=os.getenv("ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
