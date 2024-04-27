import json
import boto3
import os
import face_recognition
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def handle(req):
    try:
        # Parse the incoming request
        event = json.loads(req)
        logging.info(f"Received event: {event}")
        
        # Initialize S3 client
        s3 = boto3.client('s3',
                          aws_access_key_id=os.environ.get('S3_AWS_ACCESS_KEY_ID'),
                          aws_secret_access_key=os.environ.get('S3_AWS_SECRET_ACCESS_KEY'),
                          endpoint_url=os.environ.get('S3_HOST') + ":" + os.environ.get('S3_PORT'),
                          use_ssl=False,
                          verify=False)
        
        # Download the video from S3
        bucket_name = event['bucket_name']
        object_key = event['object_key']
        local_video_path = '/tmp/' + os.path.basename(object_key)
        s3.download_file(bucket_name, object_key, local_video_path)
        logging.info(f"Downloaded {object_key} from {bucket_name}")
        
        # TODO: Extract frames and perform face recognition
        # For now, we'll simulate a face recognition result
        recognized_name = "John Doe"
        logging.info(f"Recognized person: {recognized_name}")
        
        # Return the result
        return json.dumps({'recognized_person': recognized_name})
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return json.dumps({'error': str(e)})
