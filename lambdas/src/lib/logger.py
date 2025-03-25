import os

from aws_lambda_powertools import Logger

logger = Logger(
    service=os.environ.get("DD_SERVICE", "desserts-api"),
    environment=os.environ.get("DD_ENV", "dev"),
    version=os.environ.get("DD_VERSION"),
)

print("ENV VARS DUMP:")
logger.info("ENV VARS DUMP:")
for k, v in os.environ.items():
    print(f"{k} = {v}")
    logger.info(f"{k} = {v}")
print("END ENV VARS DUMP")
