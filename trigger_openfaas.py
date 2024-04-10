import boto3
import requests
import time
import os

# Configuration variables (placeholders)
OPENFAAS_URL = "<OPENFAAS_URL>"
FUNCTION_NAME = "project3"
CEPH_ENDPOINT = "<CEPH_ENDPOINT>"
INPUT_BUCKET = "<INPUT_BUCKET_NAME>"

# Initialize S3 client for Ceph
s3_client = boto3.client(
    's3',
    endpoint_url=CEPH_ENDPOINT,
    aws_access_key_id=os.environ.get('S3_AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('S3_AWS_SECRET_ACCESS_KEY'),
    use_ssl=False,
    verify=False
)

def call_openfaas():
    while True:
        try:
            response = s3_client.list_objects_v2(Bucket=INPUT_BUCKET)
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    if key.endswith('.mp4') or key.endswith('.MP4'):
                        # Trigger OpenFaaS function
                        res = requests.post(f"{OPENFAAS_URL}/function/{FUNCTION_NAME}", json={"key": key})
                        if res.status_code == 200:
                            print(f"Successfully triggered function for {key}")
                        else:
                            print(f"Failed to trigger function for {key}")
                        # Delete the object after processing
                        s3_client.delete_object(Bucket=INPUT_BUCKET, Key=key)
            time.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    call_openfaas()
