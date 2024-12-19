from aws_lambda_powertools import Logger
from fastapi import APIRouter

from src.lib.response import fastapi_gateway_response

logger = Logger()
router = APIRouter()


@logger.inject_lambda_context(log_event=True)
@router.get("/hello", status_code=200)
def hello():
    logger.info("Hello, world!")
    return fastapi_gateway_response(200, {}, {"message": "Hello, world!"})
