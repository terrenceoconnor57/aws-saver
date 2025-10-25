#!/usr/bin/env python3
"""Local Lambda handler invocation script for testing."""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from lambdas.scan_ec2_unattached_ebs.handler import handler


def main() -> None:
    """Load event JSON and invoke handler locally."""
    if len(sys.argv) > 1:
        # Load from file
        event_file = Path(sys.argv[1])
        if not event_file.exists():
            print(f"Error: File not found: {event_file}", file=sys.stderr)
            sys.exit(1)
        with open(event_file) as f:
            event = json.load(f)
    else:
        # Load from stdin
        try:
            event = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON on stdin: {e}", file=sys.stderr)
            sys.exit(1)

    # Invoke handler (context is unused, pass None)
    result = handler(event, None)

    # Print result as formatted JSON
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

