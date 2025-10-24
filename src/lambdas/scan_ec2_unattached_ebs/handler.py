"""Lambda handler for scanning unattached EBS volumes."""

import time
from datetime import UTC, datetime
from typing import Any

from saverbot.assume import assume
from saverbot.errors import AssumeError
from saverbot.scanners.ec2_unattached import list_unattached_volumes


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Scan for unattached EBS volumes across regions.

    Args:
        event: Lambda event with role_arn, external_id, and regions
        context: Lambda context (unused)

    Returns:
        Scan results with metadata or error dict
    """
    start_time = time.time()

    # Validate required fields
    if not isinstance(event, dict):
        return {
            "error": {
                "code": "BadRequest",
                "message": "Event must be a dictionary",
            }
        }

    role_arn = event.get("role_arn")
    external_id = event.get("external_id")
    regions = event.get("regions")

    # Validate role_arn
    if not role_arn or not isinstance(role_arn, str):
        return {
            "error": {
                "code": "BadRequest",
                "message": "Missing or invalid 'role_arn' field",
            }
        }

    # Validate external_id
    if not external_id or not isinstance(external_id, str):
        return {
            "error": {
                "code": "BadRequest",
                "message": "Missing or invalid 'external_id' field",
            }
        }

    # Validate regions
    if not regions or not isinstance(regions, list) or len(regions) == 0:
        return {
            "error": {
                "code": "BadRequest",
                "message": "Missing or invalid 'regions' field (must be non-empty list)",
            }
        }

    for region in regions:
        if not isinstance(region, str):
            return {
                "error": {
                    "code": "BadRequest",
                    "message": "All regions must be strings",
                }
            }

    # Assume role
    try:
        session = assume(role_arn, external_id)
    except AssumeError as e:
        return {
            "error": {
                "code": e.code,
                "message": e.message,
            }
        }

    # Scan all regions
    all_items = []
    for region in regions:
        volumes = list_unattached_volumes(session, region)
        all_items.extend(volumes)

    # Calculate duration
    duration_ms = int((time.time() - start_time) * 1000)

    # Return results
    return {
        "meta": {
            "service": "ec2",
            "rule": "ebs-unattached",
            "regions": regions,
            "scanned_at": datetime.now(UTC).isoformat(),
            "duration_ms": duration_ms,
        },
        "items": all_items,
        "count": len(all_items),
    }

