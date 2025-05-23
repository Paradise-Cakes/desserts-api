resource "aws_api_gateway_rest_api" "rest_api" {
  name        = "desserts-api-gateway"
  description = "Proxy to handle requests to desserts API"

  binary_media_types = ["multipart/form-data"]
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = "{proxy+}"
}


resource "aws_api_gateway_method" "get_desserts" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_desserts_integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.get_desserts.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn
}

resource "aws_api_gateway_method" "post_desserts" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "POST"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id
}

resource "aws_api_gateway_integration" "post_desserts_integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.post_desserts.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn

  request_parameters = {
    "integration.request.header.user-groups" = "context.user_groups"
  }
}

resource "aws_api_gateway_method" "patch_desserts" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "PATCH"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id
}

resource "aws_api_gateway_integration" "patch_desserts_integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.patch_desserts.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn

  request_parameters = {
    "integration.request.header.user-groups" = "context.user_groups"
  }
}

resource "aws_api_gateway_method" "delete_desserts" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "DELETE"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id
}

resource "aws_api_gateway_integration" "delete_desserts_integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.proxy.id
  http_method             = aws_api_gateway_method.delete_desserts.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app.invoke_arn

  request_parameters = {
    "integration.request.header.user-groups" = "context.user_groups"
  }
}

resource "aws_api_gateway_stage" "stage" {
  stage_name           = "v1"
  rest_api_id          = aws_api_gateway_rest_api.rest_api.id
  deployment_id        = aws_api_gateway_deployment.deployment.id
  xray_tracing_enabled = true
  cache_cluster_size   = "0.5"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  depends_on = [
    aws_api_gateway_integration.get_desserts_integration,
    aws_api_gateway_integration.post_desserts_integration,
    aws_api_gateway_integration.patch_desserts_integration,
    aws_api_gateway_integration.delete_desserts_integration,
    aws_api_gateway_integration.cors,
  ]

  triggers = {
    redeployment = timestamp()
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_domain_name" "domain_name" {
  certificate_arn = data.aws_acm_certificate.desserts_api.arn
  domain_name     = data.aws_acm_certificate.desserts_api.domain
}

resource "aws_api_gateway_base_path_mapping" "base_path_mapping" {
  api_id      = aws_api_gateway_rest_api.rest_api.id
  stage_name  = aws_api_gateway_stage.stage.stage_name
  domain_name = aws_api_gateway_domain_name.domain_name.domain_name
  base_path   = aws_api_gateway_stage.stage.stage_name
}

resource "aws_api_gateway_rest_api_policy" "rest_api_policy" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id

  policy = <<EOF
  {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": "*",
        "Action": "execute-api:Invoke",
        "Resource": ["execute-api:/*/*/*"]
      }
    ]
  }
EOF
}

resource "aws_api_gateway_method" "cors" {
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "OPTIONS"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "cors" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.cors.http_method
  type        = "MOCK"
  request_templates = {
    "application/json" = <<EOF
    {
      "statusCode": 200
    }
    EOF
  }
}

resource "aws_api_gateway_method_response" "cors" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.cors.http_method
  status_code = 200

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = true
    "method.response.header.Access-Control-Allow-Methods" = true
    "method.response.header.Access-Control-Allow-Origin"  = true
  }
}

resource "aws_api_gateway_integration_response" "cors" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.cors.http_method
  status_code = 200

  depends_on = [
    aws_api_gateway_integration.get_desserts_integration,
    aws_api_gateway_integration.post_desserts_integration,
    aws_api_gateway_integration.patch_desserts_integration,
    aws_api_gateway_integration.delete_desserts_integration,
  ]

  response_parameters = {
    "method.response.header.Access-Control-Allow-Headers" = "'Content-Type,Authorization,User-Agent'"
    "method.response.header.Access-Control-Allow-Methods" = "'POST,OPTIONS,GET,PUT,DELETE,PATCH'"
    "method.response.header.Access-Control-Allow-Origin"  = "'*'"
  }
}

resource "aws_api_gateway_authorizer" "cognito_authorizer" {
  name            = "cognito-authorizer-us-east-1"
  type            = "COGNITO_USER_POOLS"
  rest_api_id     = aws_api_gateway_rest_api.rest_api.id
  identity_source = "method.request.header.Authorization"
  provider_arns   = [data.aws_cognito_user_pool.paradise_cakes_user_pool.arn]
}
