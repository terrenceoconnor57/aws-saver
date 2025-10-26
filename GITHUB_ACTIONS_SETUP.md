# GitHub Actions Setup for Terraform Cloud

This guide shows you how to configure GitHub Actions to automatically run Terraform commands against your Terraform Cloud workspace.

## 🔑 Step 1: Create Terraform Cloud API Token

### Option A: User API Token (Recommended for Personal Projects)

1. Go to https://app.terraform.io/app/settings/tokens
2. Click **"Create an API token"**
3. Give it a name like `github-actions-aws-saver`
4. Copy the token (you'll only see it once!)

### Option B: Team API Token (Recommended for Organizations)

1. Go to your organization: https://app.terraform.io/app/aws-saver/settings/teams
2. Select the team or create one for CI/CD
3. Generate a team token
4. Copy the token

## 🔐 Step 2: Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Name: `TF_API_TOKEN`
5. Value: Paste the token from Step 1
6. Click **"Add secret"**

## ✅ Step 3: Verify Setup

Push a commit or create a PR to trigger the workflow. The CI pipeline will now:

### On Pull Requests:
- ✅ Run tests (lint, typecheck, pytest)
- ✅ Build Lambda package
- ✅ Run `terraform plan` (shows what will change)

### On Merge to Main:
- ✅ All PR checks above
- ✅ Run `terraform apply` (automatically deploys changes!)

## 🎯 Workflow Behavior

| Event | Jobs Run | Result |
|-------|----------|--------|
| PR opened/updated | `test` → `build-lambda` → `terraform-plan` | Shows plan, no deployment |
| Push to main | `test` → `build-lambda` → `terraform-plan` → `terraform-apply` | Automatic deployment |

## 📋 Required Variables in Terraform Cloud

Make sure your Terraform Cloud workspace has these **Environment Variables** set:

- `AWS_ACCESS_KEY_ID` (Sensitive)
- `AWS_SECRET_ACCESS_KEY` (Sensitive)

These are used when GitHub Actions triggers `terraform apply`.

## 🔍 View Runs

### In GitHub:
- Go to **Actions** tab in your repo
- See workflow status for each commit/PR

### In Terraform Cloud:
- Go to https://app.terraform.io/app/aws-saver/workspaces/aws-saver-dev/runs
- See detailed Terraform plan/apply output
- Review state changes

## 🚨 Troubleshooting

### "Error: Required token could not be found"
- Make sure `TF_API_TOKEN` secret is set in GitHub
- Check the token hasn't expired

### "Error: No valid credential sources found"
- Make sure AWS credentials are set in Terraform Cloud workspace variables
- Verify they're marked as "Environment Variables" (not Terraform variables)

### "Error: workspace "aws-saver-dev" not found"
- Verify `infra/terraform/backend.tf` has the correct workspace name
- Make sure the workspace exists in Terraform Cloud

## 🎉 That's It!

Your GitHub repo is now connected to Terraform Cloud. Every merge to main will automatically deploy your Lambda function!

## Optional: Manual Deployment

You can still deploy manually from your local devcontainer:

```bash
make clean_dist && make build_lambda_scan_ebs
make tf_init
make tf_apply
```

Both GitHub Actions and local deployments use the same Terraform Cloud workspace, so they won't conflict.

