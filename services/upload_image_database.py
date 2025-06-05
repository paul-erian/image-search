import os
import boto3
import argparse
from dotenv import load_dotenv

def main(args):
    # Connexion au cloud
    print("Connexion au cloud")
    load_dotenv(dotenv_path=args.env_path)
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=args.endpoint_url,
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Upload de la BDD d'images sur R2
    for root, _, files in os.walk(args.directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, args.directory)
            s3_path = relative_path.replace("\\", "/")

            print(f"uploading {local_path} to s3://{args.bucket}/{s3_path}")
            s3.upload_file(local_path, args.bucket, s3_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str, help="Chemin vers la BDD d'images locale")
    parser.add_argument('--env_path', type=str, default='../.env', help='Chemin vers le fichier .env')
    parser.add_argument('--bucket', type=str, default='image-search-db', help='Nom du bucket S3/R2')
    parser.add_argument('--endpoint_url', type=str, default='https://16ee9e2a9099aedfcaf86cd5a5ef621f.r2.cloudflarestorage.com', help='Endpoint S3/R2')
    args = parser.parse_args()
    main(args)
