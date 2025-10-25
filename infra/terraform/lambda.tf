# IAM role for Lambda execution
resource "aws_iam_role" "lambda_exec" {
  name = "${var.function_name}-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = {
    Name        = "${var.function_name}-exec-role"
    ManagedBy   = "terraform"
    Application = "aws-saver"
  }
}

# Attach CloudWatch Logs policy
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda function
resource "aws_lambda_function" "scan_ec2_unattached_ebs" {
  function_name = var.function_name
  runtime       = "python3.10"
  handler       = "scan_ec2_unattached_ebs.handler.handler"
  filename      = local.artifact_path
  role          = aws_iam_role.lambda_exec.arn

  source_code_hash = filebase64sha256(local.artifact_path)

  timeout     = 60
  memory_size = 256

  tags = {
    Name        = var.function_name
    ManagedBy   = "terraform"
    Application = "aws-saver"
  }
}

