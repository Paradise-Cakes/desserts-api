locals {
  opensearch_domain_name = "pcakes-opensearch-${var.environment}"
}

resource "aws_opensearch_domain" "pcakes_opensearch" {
  domain_name    = local.opensearch_domain_name
  engine_version = "OpenSearch_2.11"

  cluster_config {
    instance_type          = "t3.small.search"
    instance_count         = 1
    zone_awareness_enabled = false
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
    volume_type = "gp3"
  }

  encrypt_at_rest {
    enabled = true
  }

  node_to_node_encryption {
    enabled = true
  }

  domain_endpoint_options {
    enforce_https       = true
    tls_security_policy = "Policy-Min-TLS-1-2-2019-07"
  }

  # Lock to your IP and/or account (replace with YOUR_IP/32)
  access_policies = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { AWS = "*" },
      Action    = "es:*",
      Resource  = "arn:aws:es:${data.aws_region.current.name}:${data.aws_caller_identity.me.account_id}:domain/${local.opensearch_domain_name}/*",
      Condition = {
        StringEquals = { "aws:PrincipalAccount" : data.aws_caller_identity.me.account_id },
        IpAddress    = { "aws:SourceIp" : ["99.145.200.165/32"] }
      }
    }]
  })
}

data "aws_caller_identity" "me" {}
data "aws_region" "current" {}
