resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/lambda/desserts-api-us-east-1"
  retention_in_days = var.environment == "prod" ? 7 : 3
}