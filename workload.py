import boto3
import os
import time

INPUT_BUCKET = "<INPUT_BUCKET_NAME>"
TEST_CASES_DIR = "test_cases/"

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
)

def upload_test_videos():
    for root, dirs, files in os.walk(TEST_CASES_DIR):
        for file in files:
            if file.endswith('.mp4') or file.endswith('.MP4'):
                file_path = os.path.join(root, file)
                s3_client.upload_file(file_path, INPUT_BUCKET, file)
                print(f"Uploaded {file} to {INPUT_BUCKET}")
                time.sleep(1)

if __name__ == "__main__":
    upload_test_videos()
