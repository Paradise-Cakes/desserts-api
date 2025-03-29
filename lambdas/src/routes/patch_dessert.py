import os
import uuid
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

import arrow
import boto3
from boto3.dynamodb.conditions import Attr
from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from src.lib.dynamodb import DynamoConnection, update_attributes_expression
from src.lib.logger import logger
from src.lib.response import fastapi_gateway_response
from src.models import Dessert, PatchDessertRequest
from src.models.desserts import Price

router = APIRouter()
s3_client = boto3.client("s3")

desserts_table = DynamoConnection(
    os.environ.get("DYNAMODB_REGION", "us-east-1"),
    os.environ.get("DYNAMODB_ENDPOINT_URL", None),
    os.environ.get("DYNAMODB_DESSERTS_TABLE_NAME", "desserts"),
).table


prices_table = DynamoConnection(
    os.environ.get("DYNAMODB_REGION", "us-east-1"),
    os.environ.get("DYNAMODB_ENDPOINT_URL", None),
    os.environ.get("DYNAMODB_PRICES_TABLE_NAME", "prices"),
).table


class PatchDessertResponse(Dessert):
    pass


def format_price(price):
    return {
        **price.clean(),
        "base_price": Decimal(price.base_price).quantize(
            Decimal(".01"), rounding=ROUND_HALF_UP
        ),
        "discount": Decimal(price.discount).quantize(
            Decimal(".01"), rounding=ROUND_HALF_UP
        ),
    }


def generate_upload_url(dessert_id, dessert_image, bucket_name):
    upload_url = s3_client.generate_presigned_url(
        ClientMethod="put_object",
        Params={
            "Bucket": bucket_name,
            "Key": f'{dessert_id}/{dessert_image.get("image_id")}',
            "ContentType": dessert_image.get("file_type"),
        },
        ExpiresIn=60 * 60 * 24,
    )
    return upload_url


@logger.inject_lambda_context(log_event=True)
@router.patch(
    "/desserts/{dessert_id}",
    status_code=200,
    response_model=PatchDessertResponse,
    tags=["Desserts"],
)
def patch_dessert(request: Request, body: PatchDessertRequest, dessert_id: str):
    logger.info(f"Updating dessert: {dessert_id}")
    logger.append_keys(dessert_id=dessert_id)

    get_dessert_response = desserts_table.get_item(Key={"dessert_id": dessert_id})
    if "Item" not in get_dessert_response:
        raise HTTPException(status_code=404, detail="Dessert not found")

    updated_dessert = {
        **body.model_dump(exclude_unset=True),
        "last_updated_at": int(arrow.utcnow().timestamp()),
    }

    update_expression_data = {
        **updated_dessert,
    }

    if "images" in updated_dessert:
        dessert_images_bucket = os.environ.get(
            "DESSERT_IMAGES_BUCKET_NAME", "pc-dessert-images-bucket-dev"
        )

        updated_images = []
        for image in updated_dessert.get("images"):
            if "image_id" not in image:
                image_id = str(uuid.uuid4())
                object_url = f"https://{dessert_images_bucket}.s3.amazonaws.com/{dessert_id}/{image_id}"
                image["image_id"] = image_id
                image["url"] = object_url
                image["upload_url"] = generate_upload_url(
                    dessert_id, image, dessert_images_bucket
                )
            updated_images.append(image)

        if "images" in get_dessert_response["Item"]:
            for image in get_dessert_response["Item"]["images"]:
                if image["image_id"] not in [
                    img["image_id"] for img in updated_images
                ] and image.get("upload_url"):
                    s3_client.delete_object(
                        Bucket=dessert_images_bucket,
                        Key=f"{dessert_id}/{image['image_id']}",
                    )

        update_expression_data["images"] = updated_images

    if "prices" in updated_dessert:
        updated_dessert["prices"] = [
            Price(
                dessert_id=dessert_id,
                size=price.get("size"),
                base_price=price.get("base_price"),
                discount=price.get("discount") if price.get("discount") else 0,
            )
            for price in updated_dessert.get("prices")
        ]

        with prices_table.batch_writer() as batch:
            for price in updated_dessert.get("prices"):
                batch.put_item(Item=format_price(price))

        update_expression_data["prices"] = [
            format_price(price) for price in updated_dessert["prices"]
        ]

    update_response = desserts_table.update_item(
        Key={"dessert_id": dessert_id},
        ReturnValues="ALL_NEW",
        **update_attributes_expression(update_expression_data),
    )

    response = PatchDessertResponse(**update_response["Attributes"])
    logger.info(f"Updated dessert: {response}")
    return fastapi_gateway_response(200, {}, response.clean())
