data "aws_route53_zone" "desserts_api" {
  name = var.environment == "prod" ? "desserts-api.megsparadisecakes.com" : "desserts-dev-api.megsparadisecakes.com"
}

data "aws_route53_zone" "paradise_cakes" {
  name = var.environment == "prod" ? "megsparadisecakes.com" : "dev.megsparadisecakes.com"
}
