locals {
  lambda_image = "${aws_ecr_repository.desserts_api_lambdas.repository_url}:${var.docker_image_tag}"
}

resource "aws_lambda_function" "app" {
  image_uri     = local.lambda_image
  package_type  = "Image"
  function_name = var.environment == "prod" ? "desserts-api-us-east-1" : "dev-desserts-api-us-east-1"
  role          = aws_iam_role.desserts_api_role.arn

  timeout     = 30
  memory_size = 1024

  image_config {
    command = ["src.api.lambda_handler"]
  }

  environment {
    variables = {
      REGION = "us-east-1"
    }
  }
}


