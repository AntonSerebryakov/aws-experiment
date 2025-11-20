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
