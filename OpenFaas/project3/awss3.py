import boto3
import os

class S3Client:
    def __init__(self):
        self.client = boto3.client('s3',
                                   endpoint_url=os.environ.get('S3_ENDPOINT'),
                                   aws_access_key_id=os.environ.get('S3_AWS_ACCESS_KEY_ID'),
                                   aws_secret_access_key=os.environ.get('S3_AWS_SECRET_ACCESS_KEY'),
                                   use_ssl=False,
                                   verify=False)
    # TODO: Implement S3 methods
