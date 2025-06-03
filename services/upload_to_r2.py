import argparse
import os
import boto3

def upload_directory_to_r2(directory, bucket, endpoint_url, access_key, secret_key):
    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    for root, dirs, files in os.walk(directory):
        for file in files:
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, directory)
            s3_path = relative_path.replace("\\", "/")  # Windows fix

            print(f"Uploading {local_path} to s3://{bucket}/{s3_path}")
            # s3.upload_file(local_path, bucket, s3_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a directory to Cloudflare R2")
    parser.add_argument("directory", type=str, help="Path to the local directory to upload")
    parser.add_argument("--bucket", type=str, required=True, help="R2 bucket name")
    parser.add_argument("--endpoint", type=str, required=True, help="R2 endpoint URL")
    parser.add_argument("--access_key", type=str, required=True, help="R2 access key")
    parser.add_argument("--secret_key", type=str, required=True, help="R2 secret key")

    args = parser.parse_args()

    upload_directory_to_r2(
        args.directory,
        args.bucket,
        args.endpoint,
        args.access_key,
        args.secret_key
    )
