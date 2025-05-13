import os

from aws_lambda_powertools import Logger

logger = Logger(
    service=os.environ.get("DD_SERVICE", "desserts-api"),
    environment=os.environ.get("DD_ENV", "dev"),
    version=os.environ.get("DD_VERSION"),
)
