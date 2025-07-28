data "aws_ecr_repository" "desserts_api_lambdas" {
  name = var.environment == "prod" ? "desserts-api-lambdas-us-east-1" : "dev-desserts-api-lambdas-us-east-1"
}

resource "aws_ecr_repository_policy" "desserts_api_repo_policy" {
  repository = data.aws_ecr_repository.desserts_api_lambdas.name

  policy = jsonencode({
    Version = "2008-10-17",
    Statement = [
      {
        Sid    = "LambdaECRImageRetrievalPolicy",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = [
          "ecr:BatchCheckLayerAvailability",
          "ecr:BatchGetImage",
          "ecr:GetDownloadUrlForLayer"
        ],
        Condition = {
          StringLike = {
            "aws:sourceArn" = "arn:aws:lambda:us-east-1:${data.aws_caller_identity.current.account_id}:function:*"
          }
        }
      }
    ]
  })
}

