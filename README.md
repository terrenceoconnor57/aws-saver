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

## Packaging & Terraform (validate-only)

This section covers building the Lambda deployment artifact and validating the Terraform configuration. **Note:** This is validation-only; actual deployment to AWS is a later stage.

### Build the Lambda ZIP

Build the deployment artifact for the `scan_ec2_unattached_ebs` Lambda:

```bash
make clean_dist && make build_lambda_scan_ebs
```

This creates `dist/scan_ec2_unattached_ebs.zip` containing:
- The Lambda handler from `src/lambdas/scan_ec2_unattached_ebs/`
- The shared `saverbot` package from `src/saverbot/`

### Validate Terraform Configuration

Initialize and validate the Terraform configuration (no AWS credentials needed):

```bash
cd infra/terraform
terraform init
terraform validate
cd ../..
```

The Terraform files define a minimal Lambda function with:
- IAM execution role with CloudWatch Logs permissions
- Lambda function configured for Python 3.11
- Handler: `scan_ec2_unattached_ebs.handler.handler`
- Timeout: 60 seconds, Memory: 256 MB

### Local Invoke (Shape Validation)

Test the handler locally with a sample event to verify the input/output shape:

```bash
python scripts/local_invoke.py scripts/sample_event.json
```

**Note:** This validates the event structure and handler signature only. It will fail with AWS credential errors since it attempts to assume a role. For actual AWS integration testing, use the unit tests with `moto`:

```bash
pytest -k ec2_unattached
```

### Terraform Files

The Terraform configuration is in `infra/terraform/`:
- `versions.tf` - Terraform and provider version constraints
- `provider.tf` - AWS provider configuration
- `variables.tf` - Input variables (region, function_name)
- `locals.tf` - Local values (artifact path)
- `lambda.tf` - IAM role and Lambda function resources
- `outputs.tf` - Output values (lambda_name, lambda_arn)
- `terraform.tfvars.example` - Example variable values

**Real deployment** (terraform apply) requires:
- AWS credentials configured
- Appropriate IAM permissions
- Will be covered in a later stage
