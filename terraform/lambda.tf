locals {
  lambda_image = "${data.aws_ecr_repository.desserts_api_lambdas.repository_url}:${var.docker_image_tag}"
}

resource "aws_lambda_function" "app" {
  image_uri     = local.lambda_image
  package_type  = "Image"
  function_name = "desserts-api-us-east-1"
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
      DESSERT_IMAGES_BUCKET_NAME             = aws_s3_bucket.dessert_images_bucket.bucket
      REGION                                 = "us-east-1"
    }
  }
}

resource "aws_lambda_function" "desserts_api_lambda_authorizer" {
  image_uri     = local.lambda_image
  package_type  = "Image"
  function_name = "desserts-api-lambda-authorizer"
  role          = aws_iam_role.api_authorizer_role.arn

  image_config {
    command = ["src.api_authorizer.handler.lambda_handler"]
  }

  timeout     = 30
  memory_size = 256
}

resource "aws_lambda_permission" "allow_api_gateway_handler" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*"
}

resource "aws_lambda_permission" "allow_api_gateway_authorizer" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.desserts_api_lambda_authorizer.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*"
}