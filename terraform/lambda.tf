locals {
  lambda_image = "${data.aws_ecr_repository.desserts_api_lambdas.repository_url}:${var.docker_image_tag}"
  datadog_env_vars = {
    DD_KMS_API_KEY            = var.datadog_kms_api_key
    DD_ENV                    = var.environment
    DD_SERVICE                = "desserts-api"
    DD_VERSION                = var.docker_image_tag
    DD_LOGS_ENABLED           = "true"
    DD_TRACE_ENABLED          = "true"
    DD_EXTENSION_LOGS_ENABLED = "true"
    DD_SITE                   = "us5.datadoghq.com"
  }
}

resource "aws_lambda_function" "app" {
  image_uri     = local.lambda_image
  package_type  = "Image"
  function_name = "desserts-api-us-east-1"
  role          = aws_iam_role.desserts_api_role.arn

  timeout     = 30
  memory_size = 1024

  image_config {
    command = ["datadog_lambda.handler.handler"]
  }

  environment {
    variables = merge(local.datadog_env_vars, {
      DYNAMODB_REGION                        = "us-east-1"
      DYNAMODB_ENDPOINT_URL                  = "https://dynamodb.us-east-1.amazonaws.com"
      DYNAMODB_DESSERTS_TABLE_NAME           = aws_dynamodb_table.desserts.name
      DYNAMODB_DESSERT_TYPE_COUNT_TABLE_NAME = aws_dynamodb_table.dessert_type_count.name
      DYNAMODB_PRICES_TABLE_NAME             = aws_dynamodb_table.prices.name
      DESSERT_IMAGES_BUCKET_NAME             = aws_s3_bucket.dessert_images_bucket.bucket
      REGION                                 = "us-east-1"
      DD_LAMBDA_HANDLER                      = "src.lambda_handler"
    })
  }
}

resource "aws_lambda_permission" "allow_api_gateway_handler" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*"
}
