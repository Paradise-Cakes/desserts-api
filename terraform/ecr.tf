resource "aws_ecr_repository" "desserts_api_lambdas" {
  name                 = var.environment == "prod" ? "desserts-api-lambdas-us-east-1" : "dev-desserts-api-lambdas-us-east-1"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
}
