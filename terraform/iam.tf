resource "aws_iam_role" "desserts_api_role" {
  name = "desserts-api-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_policy" "desserts_api_policy" {
  name        = "desserts-api-policy"
  description = "desserts api policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = [
          "execute-api:Invoke"
        ],
        Effect   = "Allow",
        Resource = "arn:aws:execute-api:us-east-1:${data.aws_caller_identity.current.account_id}:*/*/*/*"
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "logs:PostLogEvents",
        ],
        Effect   = "Allow",
        Resource = "*"
      },
      {
        Action   = "dynamodb:Query",
        Effect   = "Allow",
        Resource = "arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/desserts/index/dessert-type-index"
      },
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:DeleteItem",
          "dynamodb:UpdateItem",
          "dynamodb:Scan",
          "dynamodb:Query",
          "dynamodb:BatchWriteItem",
          "dynamodb:BatchGetItem",
        ]
        Effect   = "Allow",
        Resource = "arn:aws:dynamodb:us-east-1:${data.aws_caller_identity.current.account_id}:table/*"
      },
      {
        Action = [
          "s3:PutObject",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:DeleteObject",
        ]
        Effect = "Allow",
        Resource = [
          "arn:aws:s3:::desserts-images",
          "arn:aws:s3:::desserts-images/*"
        ]
      },
      {
        Effect = "Allow",
        Action = [
          "ecr:*"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_policy" "datadog_kms_decrypt" {
  name = "DatadogKMSDecrypt"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = "kms:Decrypt",
        Resource = "arn:aws:kms:us-east-1:${data.aws_caller_identity.current.account_id}:key/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "api_gateway_attachment" {
  policy_arn = aws_iam_policy.desserts_api_policy.arn
  role       = aws_iam_role.desserts_api_role.name
}

resource "aws_iam_role_policy_attachment" "datadog_kms_decrypt_attachment" {
  policy_arn = aws_iam_policy.datadog_kms_decrypt.arn
  role       = aws_iam_role.desserts_api_role.name
}
