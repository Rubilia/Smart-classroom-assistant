import json
import boto3
import os
import face_recognition
import logging

logging.basicConfig(level=logging.INFO)

def download_video(s3, bucket_name, object_key, local_path):
    try:
        s3.download_file(bucket_name, object_key, local_path)
        logging.info(f"Downloaded {object_key} from {bucket_name}")
    except Exception as e:
        logging.error(f"Failed to download video: {e}")
        raise

def process_video(local_video_path):
    # TODO: Implement video processing and face recognition
    recognized_name = "John Doe"  # Placeholder
    logging.info(f"Processed video and recognized: {recognized_name}")
    return recognized_name

def handle(req):
    try:
        event = json.loads(req)
        logging.info(f"Received event: {event}")

        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get('S3_AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('S3_AWS_SECRET_ACCESS_KEY'),
                          endpoint_url=os.environ.get('S3_HOST') + ":" + os.environ.get('S3_PORT'),
                          use_ssl=False,
                          verify=False)

        bucket_name = event['bucket_name']
        object_key = event['object_key']
        local_video_path = '/tmp/' + os.path.basename(object_key)

        download_video(s3, bucket_name, object_key, local_video_path)
        recognized_name = process_video(local_video_path)

        # Clean up local file
        os.remove(local_video_path)
        logging.info(f"Removed local video file: {local_video_path}")

        return json.dumps({'recognized_person': recognized_name})
    except Exception as e:
        logging.error(f"Error in handler: {e}")
        return json.dumps({'error': str(e)})
