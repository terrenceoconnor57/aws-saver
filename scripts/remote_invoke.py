#!/usr/bin/env python3
"""
Remote Lambda invocation script using boto3.

Usage:
    python scripts/remote_invoke.py --function-name saverbot-scan-ebs \
                                     --region us-east-1 \
                                     --event-file scripts/sample_event.json
"""

import argparse
import json
import sys
from pathlib import Path

import boto3


def main() -> None:
    parser = argparse.ArgumentParser(description="Invoke a Lambda function remotely")
    parser.add_argument(
        "--function-name",
        required=True,
        help="Name of the Lambda function to invoke",
    )
    parser.add_argument(
        "--region",
        required=True,
        help="AWS region where the Lambda function is deployed",
    )
    parser.add_argument(
        "--event-file",
        required=True,
        type=Path,
        help="Path to JSON file containing the event payload",
    )
    args = parser.parse_args()

    # Read the event payload
    try:
        with open(args.event_file, "r") as f:
            event = json.load(f)
    except FileNotFoundError:
        print(f"Error: Event file not found: {args.event_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in event file: {e}", file=sys.stderr)
        sys.exit(1)

    # Create Lambda client
    lambda_client = boto3.client("lambda", region_name=args.region)

    # Invoke the function
    print(f"Invoking Lambda: {args.function_name} in {args.region}...")
    try:
        response = lambda_client.invoke(
            FunctionName=args.function_name,
            Payload=json.dumps(event),
        )
    except Exception as e:
        print(f"Error invoking Lambda: {e}", file=sys.stderr)
        sys.exit(1)

    # Check response status
    status_code = response.get("StatusCode", 0)
    print(f"StatusCode: {status_code}")

    # Read and print the response payload
    payload = response["Payload"].read().decode("utf-8")
    try:
        result = json.loads(payload)
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError:
        print(f"Raw response: {payload}")

    # Exit with error if not successful
    if status_code != 200:
        print(f"Error: Lambda invocation failed with status {status_code}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

