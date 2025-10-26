# Terraform Cloud Setup

## Quick Start (One-Time Setup)

### 1. Login to Terraform Cloud

Inside the devcontainer, run:

```bash
terraform login
```

This will:
- Open a browser to generate a token
- Prompt you to paste the token back in the terminal
- Save the token to `~/.terraform.d/credentials.tfrc.json`

**Alternative**: If the browser doesn't open, manually go to:
https://app.terraform.io/app/settings/tokens

### 2. Configure AWS Credentials in Terraform Cloud

Go to your Terraform Cloud workspace:
https://app.terraform.io/app/aws-saver/workspaces/aws-saver-dev/variables

Add these **Environment Variables**:
- `AWS_ACCESS_KEY_ID` = (your AWS access key) - mark as **Sensitive**
- `AWS_SECRET_ACCESS_KEY` = (your AWS secret key) - mark as **Sensitive**
- `AWS_DEFAULT_REGION` = `us-east-1` (optional)

### 3. Set Terraform Variables (Optional)

In the same Variables page, add **Terraform Variables** if you want to override defaults:
- `region` = `"us-east-1"` (HCL format)
- `function_name` = `"aws-saver-scan-ebs-dev"` (HCL format)

## Deploy

That's it! Now just run:

```bash
cd /workspaces/aws-saver
make clean_dist && make build_lambda_scan_ebs
make tf_init
make tf_apply
```

Terraform will:
- Use the cloud backend (state stored remotely)
- Run the plan/apply in Terraform Cloud
- Use the AWS credentials from the workspace variables

## Multiple Workspaces

To use different workspaces (dev/staging/prod), edit `infra/terraform/backend.tf` and change:

```hcl
workspaces {
  name = "aws-saver-staging"  # or "aws-saver-prod"
}
```

Or use workspace tags (more flexible):

```hcl
workspaces {
  tags = ["aws-saver"]  # Allows switching between workspaces
}
```

Then select workspace:
```bash
cd infra/terraform
terraform workspace select aws-saver-dev
# or
terraform workspace select aws-saver-prod
```

