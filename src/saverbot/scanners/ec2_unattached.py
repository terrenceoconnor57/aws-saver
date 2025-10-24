"""EC2 unattached EBS volumes scanner."""

from typing import Any

import boto3


def list_unattached_volumes(session: boto3.Session, region: str) -> list[dict[str, Any]]:
    """List all unattached EBS volumes in a region.

    Args:
        session: Authenticated boto3 session
        region: AWS region to scan

    Returns:
        List of unattached volumes with metadata
    """
    ec2_client = session.client("ec2", region_name=region)

    # Describe all volumes with filter for available (unattached) state
    response = ec2_client.describe_volumes(
        Filters=[{"Name": "status", "Values": ["available"]}]
    )

    volumes = []
    for volume in response.get("Volumes", []):
        # Convert tags to dict
        tags = {}
        for tag in volume.get("Tags", []):
            tags[tag["Key"]] = tag["Value"]

        volumes.append({
            "Region": region,
            "VolumeId": volume["VolumeId"],
            "Size": volume["Size"],
            "CreateTime": volume["CreateTime"].isoformat(),
            "Tags": tags,
        })

    return volumes

