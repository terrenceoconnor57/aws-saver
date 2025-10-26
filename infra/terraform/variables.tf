variable "region" {
  description = "AWS region to deploy Lambda function"
  type        = string
  default     = "us-east-1"
}

variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "aws-saver-scan-ec2-unattached-ebs"
}

variable "tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}

