module "api_gateway" {
  source = "git@github.com:Paradise-Cakes/pc-terraform-modules.git//apiGateway?ref=v1.9.2"

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
    }
    "POST" = {
      authorization = "CUSTOM"
      authorizer_id = aws_lambda_function.desserts_api_lambda_authorizer.arn
    }
    "PATCH" = {
      authorization = "CUSTOM"
      authorizer_id = aws_lambda_function.desserts_api_lambda_authorizer.arn
    }
    "DELETE" = {
      authorization = "CUSTOM"
      authorizer_id = aws_lambda_function.desserts_api_lambda_authorizer.arn
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