data "aws_cognito_user_pool" "paradise_cakes_user_pool" {
  user_pool_id = var.environment == "prod" ? "us-east-1_WveiNUhbs" : "us-east-1_hSy5PYR7I"
}
