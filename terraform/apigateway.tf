module "api_gateway" {
  source = "git@github.com:Paradise-Cakes/pc-terraform-modules.git//apiGateway?ref=v1.9.3"

  app_arn                 = aws_lambda_function.app.arn
  app_name                = aws_lambda_function.app.function_name
  api_gateway_name        = "desserts-api-gateway"
  api_description         = "Proxy to handle requests to desserts API"
  binary_media_types      = ["multipart/form-data"]
  stage_name              = "v1"
  api_acm_certificate_arn = data.aws_acm_certificate.desserts_api.arn
  api_domain_name         = data.aws_acm_certificate.desserts_api.domain
  environment             = var.environment
  api_zone_id             = data.aws_route53_zone.desserts_api.zone_id
  website_zone_id         = data.aws_route53_zone.paradise_cakes.zone_id
  http_methods = {
    "GET" = {
      authorization = "NONE"
      authorizer_id = ""
    }
    "POST" = {
      authorization = "CUSTOM"
      authorizer_id = aws_api_gateway_authorizer.desserts_api_lambda_authorizer.id
    }
    "PATCH" = {
      authorization = "CUSTOM"
      authorizer_id = aws_api_gateway_authorizer.desserts_api_lambda_authorizer.id
    }
    "DELETE" = {
      authorization = "CUSTOM"
      authorizer_id = aws_api_gateway_authorizer.desserts_api_lambda_authorizer.id
    }
  }

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

resource "aws_api_gateway_authorizer" "desserts_api_lambda_authorizer" {
  name                   = "desserts-api-authorizer"
  rest_api_id            = aws_api_gateway_rest_api.rest_api.id
  authorizer_uri         = aws_lambda_function.desserts_api_lambda_authorizer.invoke_arn
  type                   = "REQUEST"
  identity_source        = "method.request.header.Authorization"
}