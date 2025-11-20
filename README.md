# README – AWS Homework (Part 1 & Part 2)

## Part 1 — Deploying Application to EC2 using GitHub Actions

### 1. Overview
This workflow automates deployment of my application to an EC2 instance.  
The pipeline performs the following steps:

- Checks out the repository  
- Builds and pushes a Docker image to GHCR  
- Connects to the EC2 instance via SSH  
- Pulls the latest Docker image  
- Restarts the application using `docker compose up -d`

---

### 2. GitHub Secrets Used
The following secrets are configured in the repository:

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM User access key |
| `AWS_SECRET_ACCESS_KEY` | IAM User secret key |
| `AWS_REGION` | AWS region |
| `EC2_HOST` | Public EC2 hostname/IP |
| `EC2_USER` | SSH user (ubuntu) |
| `EC2_SSH_KEY` | Private key from ec2-ssh-key |
| `GHCR_PAT` | GitHub Personal Access Token (packages: write/read) |

---

### 3. GitHub repo

The application runs as a Docker container pulled from:
ghcr.io/antonserebryakov/aws-experiment:latest



---

### 4. Deployment Workflow

Deployment is triggered on every push to the **main** branch.

---

## Part 2 — Lambda Function

### 5. Lambda Function

Created a function named `HelloStudentFunction` (region: `eu-north-1`) with runtime Python 3.x.

Lambda code:


def lambda_handler(event, context):
    name = event.get('name', 'World')
    return {
        'statusCode': 200,
        'body': f'Hello, {name}!'
    }


---

### 6. Invoking Lambda Using Boto3

import json
import boto3


def main():
    lambda_client = boto3.client("lambda", region_name="eu-north-1")

    event = {"name": "Anton"}

    response = lambda_client.invoke(
        FunctionName="HelloStudentFunction",
        InvocationType="RequestResponse",
        Payload=json.dumps(event).encode("utf-8"),
    )

    payload_bytes = response["Payload"].read()
    payload = json.loads(payload_bytes.decode("utf-8"))

    print("Lambda payload:", payload)


if __name__ == "__main__":
    main()


### 7. Invoking Lambda Using Boto3

To verify AWS credentials and ensure the Lambda function is reachable from CI,
the workflow also performs an automated Lambda invocation.

GitHub Actions step:

- name: Test AWS by invoking Lambda
  run: |
    echo "Invoking HelloStudentFunction from CI..."
    aws lambda invoke \
      --function-name HelloStudentFunction \
      --payload '{"name": "Anton from CI"}' \
      --cli-binary-format raw-in-base64-out \
      lambda_response.json

    echo "Lambda response:"
    cat lambda_response.json


---