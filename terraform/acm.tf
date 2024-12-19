data "aws_acm_certificate" "desserts_api" {
  domain      = var.environment == "prod" ? "desserts-api.megsparadisecakes.com" : "desserts-dev-api.megsparadisecakes.com"
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}
