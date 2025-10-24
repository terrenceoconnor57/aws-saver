"""Test error handling in assume role functionality."""

from typing import Any

import boto3
import pytest
from botocore.stub import Stubber

from saverbot.assume import assume
from saverbot.errors import AssumeError


def test_assume_invalid_duration_too_low() -> None:
    """Test that invalid duration (too low) raises AssumeError."""
    with pytest.raises(AssumeError) as exc_info:
        assume(
            role_arn="arn:aws:iam::123456789012:role/test",
            external_id="test-external-id",
            duration=899,
        )

    assert exc_info.value.code == "InvalidParameter"
    assert "900" in exc_info.value.message


def test_assume_invalid_duration_too_high() -> None:
    """Test that invalid duration (too high) raises AssumeError."""
    with pytest.raises(AssumeError) as exc_info:
        assume(
            role_arn="arn:aws:iam::123456789012:role/test",
            external_id="test-external-id",
            duration=43201,
        )

    assert exc_info.value.code == "InvalidParameter"
    assert "43200" in exc_info.value.message


def test_assume_access_denied() -> None:
    """Test that AccessDenied error is properly mapped to AssumeError."""
    sts_client = boto3.client("sts", region_name="us-east-1")
    stubber = Stubber(sts_client)

    stubber.add_client_error(
        "assume_role",
        service_error_code="AccessDenied",
        service_message="User: arn:aws:iam::123456789012:user/test is not authorized",
    )

    stubber.activate()

    # Monkey patch the client creation
    original_client = boto3.client

    def mock_client(service_name: str, **kwargs: Any) -> Any:
        if service_name == "sts":
            return sts_client
        return original_client(service_name, **kwargs)  # type: ignore[call-overload]

    boto3.client = mock_client  # type: ignore[assignment]

    try:
        with pytest.raises(AssumeError) as exc_info:
            assume(
                role_arn="arn:aws:iam::123456789012:role/test-role",
                external_id="test-external-id",
            )

        assert exc_info.value.code == "AccessDenied"
        assert "not authorized" in exc_info.value.message
    finally:
        boto3.client = original_client
        stubber.deactivate()


def test_assume_malformed_policy_document() -> None:
    """Test that MalformedPolicyDocument error is properly mapped."""
    sts_client = boto3.client("sts", region_name="us-east-1")
    stubber = Stubber(sts_client)

    stubber.add_client_error(
        "assume_role",
        service_error_code="MalformedPolicyDocument",
        service_message="The policy document is malformed",
    )

    stubber.activate()

    original_client = boto3.client

    def mock_client(service_name: str, **kwargs: Any) -> Any:
        if service_name == "sts":
            return sts_client
        return original_client(service_name, **kwargs)  # type: ignore[call-overload]

    boto3.client = mock_client  # type: ignore[assignment]

    try:
        with pytest.raises(AssumeError) as exc_info:
            assume(
                role_arn="arn:aws:iam::123456789012:role/test-role",
                external_id="test-external-id",
            )

        assert exc_info.value.code == "MalformedPolicyDocument"
        assert "malformed" in exc_info.value.message.lower()
    finally:
        boto3.client = original_client
        stubber.deactivate()


def test_assume_error_repr() -> None:
    """Test AssumeError string representation."""
    error = AssumeError(code="TestCode", message="Test message")
    assert repr(error) == "AssumeError(code='TestCode', message='Test message')"
    assert str(error) == "TestCode: Test message"


def test_assume_success() -> None:
    """Test successful assume role returns a valid session."""
    sts_client = boto3.client("sts", region_name="us-east-1")
    stubber = Stubber(sts_client)

    expected_params = {
        "RoleArn": "arn:aws:iam::123456789012:role/test-role",
        "RoleSessionName": "saverbot-session",
        "ExternalId": "test-external-id",
        "DurationSeconds": 900,
    }

    response = {
        "Credentials": {
            "AccessKeyId": "AKIAIOSFODNN7EXAMPLE",
            "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "SessionToken": "FwoGZXIvYXdzEBYaDH3example",
            "Expiration": "2024-01-01T12:00:00Z",
        },
        "AssumedRoleUser": {
            "AssumedRoleId": "AROA123456789012:saverbot-session",
            "Arn": "arn:aws:sts::123456789012:assumed-role/test-role/saverbot-session",
        },
    }

    stubber.add_response("assume_role", response, expected_params)
    stubber.activate()

    original_client = boto3.client

    def mock_client(service_name: str, **kwargs: Any) -> Any:
        if service_name == "sts":
            return sts_client
        return original_client(service_name, **kwargs)  # type: ignore[call-overload]

    boto3.client = mock_client  # type: ignore[assignment]

    try:
        session = assume(
            role_arn="arn:aws:iam::123456789012:role/test-role",
            external_id="test-external-id",
        )

        assert isinstance(session, boto3.Session)
        assert session.get_credentials() is not None
        assert session.get_credentials().access_key == "AKIAIOSFODNN7EXAMPLE"  # type: ignore[union-attr]
    finally:
        boto3.client = original_client
        stubber.deactivate()

