# Hybrid Cloud Face Recognition System

## Introduction

This project is a hybrid cloud application that leverages AWS and a self-hosted Ceph OpenFaaS cluster to perform face recognition on video files. When a video file is uploaded to a Ceph S3 bucket, the system automatically triggers a serverless function that processes the video, extracts frames, performs face recognition, and retrieves corresponding student information from a DynamoDB database.

## Purpose

The purpose of this project is to demonstrate the integration of cloud services and serverless computing to create a scalable and efficient face recognition system. By combining AWS services with a self-hosted Ceph storage cluster and OpenFaaS functions, the system showcases how hybrid cloud architectures can be used for computational tasks that require both storage and processing capabilities.

## Features

- Automated Processing: Automatically triggers processing when a new
  video is uploaded.
- Face Recognition: Extracts frames from videos and uses face recognition algorithms to identify individuals.
- AWS DynamoDB Integration: Retrieves student information based on recognized faces.
- Scalable Architecture: Utilizes OpenFaaS for serverless function execution and Ceph for scalable object storage.

## Project Structure

```plaintext
├── OpenFaas
│   └── project3
│       ├── handler.py
│       ├── awss3.py
│       ├── requirements.txt
│       └── __init__.py
├── ceph
│   ├── cluster-test.yaml
│   ├── notification.yaml
│   ├── object-test.yaml
│   ├── rgw-external.yaml
│   ├── toolbox.yaml
│   └── ...
├── trigger_openfaas.py
├── workload.py
├── credentials.env
└── README.md
```

## Installation

### Prerequisites

- Kubernetes cluster
- OpenFaaS installed on the cluster
- Ceph storage cluster configured
- AWS account with access to DynamoDB
- Python 3.6 or higher

### Steps

**Clone the Repository**

    git clone https://github.com/yourusername/hybrid-cloud-face-recognition.git
    cd hybrid-cloud-face-recognition

**Configure Credentials**

Update the `credentials.env` file with your AWS and Ceph credentials.

    # AWS DynamoDB Credentials
    export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
    export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>

    #Ceph S3 Buckets Credentials
    export S3_AWS_ACCESS_KEY_ID=<YOUR_S3_AWS_ACCESS_KEY_ID>
    export S3_AWS_SECRET_ACCESS_KEY=<YOUR_S3_AWS_SECRET_ACCESS_KEY>

**Deploy Ceph Components**

Apply the Ceph configuration files to your Kubernetes cluster.

    kubectl apply -f ceph/cluster-test.yaml
    kubectl apply -f ceph/object-test.yaml
    kubectl apply -f ceph/notification.yaml
    kubectl apply -f ceph/rgw-external.yaml

**Set Up OpenFaaS Function**
Navigate to the OpenFaaS function directory and deploy the function.

    cd OpenFaas
    faas-cli up -f project3.yml

**Set Environment Variables**

Source the `credentials.env` file.

    source credentials.env

**Install Python Dependencies**

    pip install -r OpenFaas/project3/requirements.txt

## Usage

**Start the Trigger Script**

Run the `trigger_openfaas.py` script to monitor the input bucket and trigger the OpenFaaS function.

    python3 trigger_openfaas.py

**Upload a Video**

Upload a video file (`.mp4`) to the input Ceph S3 bucket.

    aws s3 cp path/to/video.mp4 s3://your-input-bucket --endpoint-url http://your-ceph-endpoint

**Monitor the Process**

- The trigger script will detect the new video and invoke the OpenFaaS function.
- The function will process the video, perform face recognition, and store the result in the output bucket.

**Check the Output**

Retrieve the output from the Ceph S3 output bucket.

    aws s3 ls s3://your-output-bucket --endpoint-url http://your-ceph-endpoint

## Project Details

### OpenFaaS Function (`handler.py`)

The OpenFaaS function performs the following steps:

- Downloads the video from the input bucket.
- Extracts frames from the video using OpenCV.
- Performs face recognition on each frame using the `face_recognition` library.
- Queries AWS DynamoDB to retrieve student information based on the recognized face.
- Stores the result in the output bucket.

### Ceph Configuration

Ceph is used as the object storage system. The configuration includes:

- **Ceph Cluster Deployment**: Deploys a Ceph cluster on Kubernetes.
- **Object Store Setup**: Sets up an object store (S3-compatible) using Ceph RGW.
- **Bucket Notifications**: Configures bucket notifications to trigger events when new objects are created.

## Contact

- **Author**: Ilia Rubashkin
- **Email**: irubashk@asu.edu

## License

This project is licensed under the MIT License.
