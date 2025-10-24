"""AWS STS assume role functionality."""

import boto3
from botocore.exceptions import ClientError

from saverbot.errors import AssumeError


def assume(role_arn: str, external_id: str, duration: int = 900) -> boto3.Session:
    """Assume an AWS IAM role and return a session with temporary credentials.

    Args:
        role_arn: ARN of the role to assume
        external_id: External ID for assume role
        duration: Session duration in seconds (default: 900, min: 900, max: 43200)

    Returns:
        boto3.Session configured with temporary credentials

    Raises:
        AssumeError: If assume role fails with error code and message
    """
    if duration < 900 or duration > 43200:
        raise AssumeError(
            code="InvalidParameter",
            message=f"Duration must be between 900 and 43200 seconds, got {duration}",
        )

    try:
        sts_client = boto3.client("sts")
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="saverbot-session",
            ExternalId=external_id,
            DurationSeconds=duration,
        )

        credentials = response["Credentials"]

        return boto3.Session(
            aws_access_key_id=credentials["AccessKeyId"],
            aws_secret_access_key=credentials["SecretAccessKey"],
            aws_session_token=credentials["SessionToken"],
        )

    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        raise AssumeError(code=error_code, message=error_message) from e

