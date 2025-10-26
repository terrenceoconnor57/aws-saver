output "lambda_name" {
  description = "Name of the deployed Lambda function"
  value       = aws_lambda_function.scan_ec2_unattached_ebs.function_name
}

output "lambda_arn" {
  description = "ARN of the deployed Lambda function"
  value       = aws_lambda_function.scan_ec2_unattached_ebs.arn
}

output "log_group_name" {
  description = "Name of the CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

