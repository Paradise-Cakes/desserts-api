resource "aws_dynamodb_table" "desserts" {
  name         = "desserts"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dessert_id"

  attribute {
    name = "dessert_id"
    type = "S"
  }

  attribute {
    name = "dessert_type"
    type = "S"
  }

  attribute {
    name = "last_updated"
    type = "N"
  }

  global_secondary_index {
    name            = "dessert_type_index"
    hash_key        = "dessert_type"
    range_key       = "last_updated"
    projection_type = "ALL"
  }
}

resource "aws_dynamodb_table" "dessert_type_count" {
  name         = "dessert_type_count"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dessert_type"

  attribute {
    name = "dessert_type"
    type = "S"
  }
}

data "aws_dynamodb_table" "dessert_type_count_created" {
  name       = "dessert_type_count"
  depends_on = [aws_dynamodb_table.dessert_type_count]
}

resource "aws_dynamodb_table" "prices" {
  name         = "prices"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "dessert_id"
  range_key    = "size"

  attribute {
    name = "dessert_id"
    type = "S"
  }

  attribute {
    name = "size"
    type = "S"
  }
}
