import os
import boto3
from dotenv import load_dotenv

# chemins distant
s3_embeddings_dir = "embeddings"
model_name = "openai/clip-vit-base-patch32"

# chemins locaux
embeddings_dir = "../embeddings"
embeddings_name = "clip_embeddings_20000.pt"
clip_path = "./clip_model"
image_dir = "../images"
env_path = "../.env"

# client s3
load_dotenv(dotenv_path=env_path)
bucket = os.getenv("BUCKET_NAME")
s3 = boto3.session.Session().client(
    service_name='s3',
    endpoint_url=os.getenv("ENDPOINT_URL"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
