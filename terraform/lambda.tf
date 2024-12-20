locals {
  lambda_image = "${data.aws_ecr_repository.desserts_api_lambdas.repository_url}:${var.docker_image_tag}"
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
      DYNAMODB_REGION                        = "us-east-1"
      DYNAMODB_ENDPOINT_URL                  = "https://dynamodb.us-east-1.amazonaws.com"
      DYNAMODB_DESSERTS_TABLE_NAME           = aws_dynamodb_table.desserts.name
      DYNAMODB_DESSERT_TYPE_COUNT_TABLE_NAME = aws_dynamodb_table.dessert_type_count.name
      DYNAMODB_PRICES_TABLE_NAME             = aws_dynamodb_table.prices.name
      DESSERT_IMAGES_BUCKET_NAME             = aws_s3_bucket.pc_dessert_images_bucket.bucket
      REGION                                 = "us-east-1"
    }
  }
}


