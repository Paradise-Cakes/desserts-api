import os

import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.types import TypeDeserializer
from fastapi import APIRouter
from fastapi.exceptions import HTTPException

from src.lib.dynamodb import DynamoConnection
from src.lib.logger import logger
from src.lib.response import fastapi_gateway_response
from src.models import Dessert

router = APIRouter()

dynamodb_client = boto3.client("dynamodb", "us-east-1")

desserts_table = DynamoConnection(
    os.environ.get("DYNAMODB_REGION", "us-east-1"),
    os.environ.get("DYNAMODB_ENDPOINT_URL", None),
    os.environ.get("DYNAMODB_DESSERTS_TABLE_NAME", "desserts"),
).table


@logger.inject_lambda_context(log_event=True)
@router.get(
    "/desserts",
    status_code=200,
    tags=["Desserts"],
)
def get_desserts(dessert_type: str = None):
    if dessert_type:
        logger.info(f"Getting desserts of type {dessert_type}")

        desserts_response = desserts_table.query(
            IndexName="dessert_type_index",
            KeyConditionExpression=Key("dessert_type").eq(dessert_type),
        )

    else:
        logger.info("Getting all desserts")
        desserts_response = desserts_table.scan()

    if not desserts_response.get("Items"):
        return fastapi_gateway_response(200, {}, [])

    desserts = [Dessert(**d).clean() for d in desserts_response.get("Items")]

    return fastapi_gateway_response(200, {}, desserts)
