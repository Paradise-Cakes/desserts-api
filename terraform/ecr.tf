data "aws_ecr_repository" "desserts_api_lambdas" {
  name = var.environment == "prod" ? "desserts-api-lambdas-us-east-1" : "dev-desserts-api-lambdas-us-east-1"
}

data "aws_ecr_image" "desserts_api" {
  repository_name = data.aws_ecr_repository.desserts_api_lambdas.name
  image_tag       = var.docker_image_tag # "${BRANCH_NAME}-${SHORT_SHA}" from your workflow
}
