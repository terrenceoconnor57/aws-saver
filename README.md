# aws-saver

AWS cost-saving automation bot.

## Development Setup

### Prerequisites

- Docker or Colima
- VS Code with the Dev Containers extension

### Open in Dev Container

1. Open this folder in VS Code
2. When prompted, click "Reopen in Container" (or run `Dev Containers: Reopen in Container` from the command palette)
3. VS Code will build the container and install dependencies automatically

### Troubleshooting

**If Colima gets stuck or Docker commands hang:**

```bash
make fix-colima
# or directly: ./fix-colima.sh
```

This script will:
- Kill hung Colima/Lima/QEMU processes
- Clean up stale socket files
- Restart Colima with proper configuration

### Running Tests Inside Container

Once inside the dev container:

```bash
make test
```

### Available Make Commands

```bash
make install     # Install dependencies
make fmt         # Format code with ruff
make lint        # Lint code with ruff
make typecheck   # Type check with mypy
make test        # Run pytest
make clean       # Clean build artifacts
make fix-colima  # Fix stuck Colima/Docker
```

## Project Structure

```
aws-saver/
├── .devcontainer/         # Dev container configuration
├── .github/workflows/     # CI/CD workflows
├── src/saverbot/          # Main package
│   ├── config.py          # Configuration management
│   ├── jsonlog.py         # JSON logging
│   ├── assume.py          # STS assume role
│   └── errors.py          # Custom exceptions
└── tests/                 # Test suite
```

## Architecture

This project uses:
- **Python 3.11** with strict mypy type checking
- **pydantic-settings** for configuration management
- **boto3** for AWS SDK
- **ruff** for linting and formatting
- **pytest** with botocore Stubber for testing

## STS Assume Role

The `assume()` function provides a clean interface for assuming AWS IAM roles:

```python
from saverbot.assume import assume
from saverbot.errors import AssumeError

try:
    session = assume(
        role_arn="arn:aws:iam::123456789012:role/MyRole",
        external_id="my-external-id",
        duration=900
    )
    # Use the session...
except AssumeError as e:
    print(f"Failed to assume role: {e.code} - {e.message}")
```
