import os
import uuid
from datetime import datetime, timezone

import boto3
import pytest
from dotenv import load_dotenv
from request_helper import RequestHelper

load_dotenv()


@pytest.fixture(scope="session")
def api_url():
    local_port = os.getenv("LOCAL_PORT")

    if local_port:
        return f"http://localhost:{local_port}"

    return "https://desserts-dev-api.megsparadisecakes.com"


@pytest.fixture(scope="session")
def request_helper(api_url):
    return RequestHelper(api_url, {})


@pytest.fixture(scope="session")
def dynamodb_client():
    return boto3.client("dynamodb", region_name="us-east-1")


@pytest.fixture(scope="function")
def function_prices(dynamodb_client, cleanup_prices):
    def _create_prices(dessert_id):
        records = [
            {
                "dessert_id": {"S": dessert_id},
                "size": {"S": "slice"},
                "base_price": {"N": "5.00"},
                "discount": {"N": "0.00"},
            },
            {
                "dessert_id": {"S": dessert_id},
                "size": {"S": "whole"},
                "base_price": {"N": "40.00"},
                "discount": {"N": "0.00"},
            },
        ]

        for record in records:
            dynamodb_client.put_item(
                TableName="prices",
                Item=record,
            )
        cleanup_prices.extend(records)

        return {"dessert_id": dessert_id, "records": records}

    return _create_prices


@pytest.fixture(scope="function")
def function_dessert(dynamodb_client, cleanup_desserts):
    dessert_id = f"DESSERT-{str(uuid.uuid4())}"

    record = {
        "dessert_id": {"S": dessert_id},
        "name": {"S": "Chocolate Cake"},
        "description": {"S": "its a chocolate cake"},
        "dessert_type": {"S": "cake"},
        "created_at": {"N": f"{int(datetime.now(tz=timezone.utc).timestamp())}"},
        "last_updated_at": {"N": f"{int(datetime.now(tz=timezone.utc).timestamp())}"},
        "visible": {"BOOL": False},
        "prices": {
            "L": [
                {
                    "M": {
                        "dessert_id": {"S": dessert_id},
                        "size": {"S": "slice"},
                        "base_price": {"N": "5.00"},
                        "discount": {"N": "0.00"},
                    }
                },
                {
                    "M": {
                        "dessert_id": {"S": dessert_id},
                        "size": {"S": "whole"},
                        "base_price": {"N": "40.00"},
                        "discount": {"N": "0.00"},
                    }
                },
            ]
        },
        "ingredients": {
            "L": [
                {"S": "flour"},
                {"S": "sugar"},
                {"S": "cocoa"},
                {"S": "butter"},
                {"S": "eggs"},
            ]
        },
        "images": {
            "L": [
                {
                    "M": {
                        "image_id": {"S": "IMAGE-1"},
                        "url": {"S": "https://example.com/image1.jpg"},
                        "upload_url": {"S": "https://example.com/upload-url"},
                        "position": {"N": "1"},
                        "file_name": {"S": "image1.jpg"},
                        "file_type": {"S": "jpg"},
                    }
                },
                {
                    "M": {
                        "image_id": {"S": "IMAGE-2"},
                        "url": {"S": "https://example.com/image2.jpg"},
                        "upload_url": {"S": "https://example.com/upload-url"},
                        "position": {"N": "2"},
                        "file_name": {"S": "image2.jpg"},
                        "file_type": {"S": "jpg"},
                    }
                },
            ]
        },
    }

    dynamodb_client.put_item(
        TableName="desserts",
        Item=record,
    )

    dynamodb_client.batch_write_item(
        RequestItems={
            "prices": [
                {
                    "PutRequest": {
                        "Item": {
                            "dessert_id": {"S": dessert_id},
                            "size": {"S": "slice"},
                            "base_price": {"N": "5.00"},
                            "discount": {"N": "0.00"},
                        }
                    }
                },
                {
                    "PutRequest": {
                        "Item": {
                            "dessert_id": {"S": dessert_id},
                            "size": {"S": "whole"},
                            "base_price": {"N": "40.00"},
                            "discount": {"N": "0.00"},
                        }
                    }
                },
            ]
        }
    )
    cleanup_desserts.append(dessert_id)

    return {"dessert_id": dessert_id, "record": record}


@pytest.fixture(scope="function")
def cleanup_desserts(dynamodb_client):
    desserts_to_cleanup = []
    yield desserts_to_cleanup

    # Cleanup logic
    for dessert_id in desserts_to_cleanup:
        try:
            dessert_prices = dynamodb_client.query(
                TableName="prices",
                KeyConditionExpression="dessert_id = :dessert_id",
                ExpressionAttributeValues={":dessert_id": {"S": dessert_id}},
            )
            for price in dessert_prices.get("Items"):
                dynamodb_client.delete_item(
                    Key={
                        "dessert_id": {"S": dessert_id},
                        "size": price.get("size"),
                    },
                    TableName="prices",
                )
            print(f"Deleted test dessert prices: {dessert_id}")
            dynamodb_client.delete_item(
                Key={
                    "dessert_id": {"S": dessert_id},
                },
                TableName="desserts",
            )
            print(f"Deleted test dessert: {dessert_id}")
        except Exception as e:
            print(f"Failed to delete dessert {dessert_id}: {e}")
            raise e


@pytest.fixture(scope="function")
def cleanup_prices(dynamodb_client):
    prices_to_cleanup = []
    yield prices_to_cleanup

    for price in prices_to_cleanup:
        dessert_id = price.get("dessert_id").get("S")
        size = price.get("size").get("S")
        try:
            dynamodb_client.delete_item(
                Key={
                    "dessert_id": {"S": dessert_id},
                    "size": {"S": size},
                },
                TableName="prices",
            )
            print(f"Deleted test price: {dessert_id} - {size}")
        except Exception as e:
            print(f"Failed to delete price {dessert_id} - {size}: {e}")
            raise e
