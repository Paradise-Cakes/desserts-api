import uuid
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from botocore.stub import Stubber
from fastapi.testclient import TestClient
from freezegun import freeze_time

from src.api import app
from src.routes.patch_dessert import desserts_table, s3_client

test_client = TestClient(app)


@pytest.fixture(autouse=True, scope="function")
def desserts_dynamodb_stub():
    with Stubber(desserts_table.meta.client) as ddb_stubber:
        yield ddb_stubber
        ddb_stubber.assert_no_pending_responses()


@pytest.fixture(autouse=True, scope="function")
def s3_stub():
    with Stubber(s3_client) as s3_stubber:
        yield s3_stubber
        s3_stubber.assert_no_pending_responses()


@freeze_time("2024-12-12 12:00:00")
@patch("src.routes.patch_dessert.prices_table")
def test_handler_patch_dessert(mock_prices_table, desserts_dynamodb_stub):
    mock_batch_writer = MagicMock()
    mock_prices_table.batch_writer.__enter__.return_value = mock_batch_writer

    desserts_dynamodb_stub.add_response(
        "get_item",
        {
            "Item": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "whole"},
                                "base_price": {"N": "40.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                    ]
                },
                "ingredients": {"SS": ["flour", "sugar", "cocoa", "butter", "eggs"]},
                "images": {
                    "L": [
                        {
                            "M": {
                                "image_id": {"S": "IMAGE-1"},
                                "url": {"S": "https://example.com/image1.jpg"},
                                "position": {"N": "1"},
                                "file_name": {"S": "image1.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        }
                    ]
                },
            }
        },
    )

    desserts_dynamodb_stub.add_response(
        "update_item",
        {
            "Attributes": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": True},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
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
                                "position": {"N": "1"},
                                "file_name": {"S": "image1.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        }
                    ]
                },
            }
        },
        expected_params={
            "TableName": "desserts",
            "Key": {"dessert_id": "00000000-0000-0000-0000-000000000001"},
            "UpdateExpression": "SET #visible = :visible, #last_updated_at = :last_updated_at",
            "ExpressionAttributeNames": {
                "#visible": "visible",
                "#last_updated_at": "last_updated_at",
            },
            "ExpressionAttributeValues": {
                ":visible": True,
                ":last_updated_at": 1734004800,
            },
            "ReturnValues": "ALL_NEW",
        },
    )

    response = test_client.patch(
        "/desserts/00000000-0000-0000-0000-000000000001",
        json={"visible": True},
    )

    pytest.helpers.assert_responses_equal(
        response,
        200,
        {
            "dessert_id": "00000000-0000-0000-0000-000000000001",
            "name": "Chocolate Cake",
            "description": "A delicious chocolate cake",
            "dessert_type": "cake",
            "created_at": 1734004800,
            "last_updated_at": 1734004800,
            "visible": True,
            "prices": [
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "slice",
                    "base_price": 5.00,
                    "discount": 0.00,
                },
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "whole",
                    "base_price": 40.00,
                    "discount": 0.00,
                },
            ],
            "ingredients": ["flour", "sugar", "cocoa", "butter", "eggs"],
            "images": [
                {
                    "image_id": "IMAGE-1",
                    "url": "https://example.com/image1.jpg",
                    "position": 1,
                    "file_name": "image1.jpg",
                    "file_type": "jpg",
                }
            ],
        },
    )


@freeze_time("2024-12-12 12:00:00")
@patch("src.routes.patch_dessert.prices_table")
def test_handler_patch_dessert_prices(mock_prices_table, desserts_dynamodb_stub):
    mock_batch_writer = MagicMock()
    mock_prices_table.batch_writer.__enter__.return_value = mock_batch_writer

    desserts_dynamodb_stub.add_response(
        "get_item",
        {
            "Item": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "whole"},
                                "base_price": {"N": "40.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                    ]
                },
                "ingredients": {"SS": ["flour", "sugar", "cocoa", "butter", "eggs"]},
                "images": {
                    "L": [
                        {
                            "M": {
                                "image_id": {"S": "IMAGE-1"},
                                "url": {"S": "https://example.com/image1.jpg"},
                                "position": {"N": "1"},
                                "file_name": {"S": "image1.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        }
                    ]
                },
            }
        },
    )

    desserts_dynamodb_stub.add_response(
        "update_item",
        {
            "Attributes": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake  "},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": True},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "15.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "whole"},
                                "base_price": {"N": "140.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "half"},
                                "base_price": {"N": "120.00"},
                                "discount": {"N": "0.00"},
                            },
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
                                "position": {"N": "1"},
                                "file_name": {"S": "image1.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        }
                    ]
                },
            }
        },
        expected_params={
            "TableName": "desserts",
            "Key": {"dessert_id": "00000000-0000-0000-0000-000000000001"},
            "UpdateExpression": "SET #prices = :prices, #visible = :visible, #last_updated_at = :last_updated_at",
            "ExpressionAttributeNames": {
                "#visible": "visible",
                "#last_updated_at": "last_updated_at",
                "#prices": "prices",
            },
            "ExpressionAttributeValues": {
                ":visible": True,
                ":last_updated_at": 1734004800,
                ":prices": [
                    {
                        "dessert_id": "00000000-0000-0000-0000-000000000001",
                        "size": "slice",
                        "base_price": Decimal(15.00),
                        "discount": Decimal(0.00),
                    },
                    {
                        "dessert_id": "00000000-0000-0000-0000-000000000001",
                        "size": "whole",
                        "base_price": Decimal(140.00),
                        "discount": Decimal(0.00),
                    },
                    {
                        "dessert_id": "00000000-0000-0000-0000-000000000001",
                        "size": "half",
                        "base_price": Decimal(120.00),
                        "discount": Decimal(0.00),
                    },
                ],
            },
            "ReturnValues": "ALL_NEW",
        },
    )

    response = test_client.patch(
        "/desserts/00000000-0000-0000-0000-000000000001",
        json={
            "visible": True,
            "prices": [
                {"size": "slice", "base_price": 15.00, "discount": 0.00},
                {"size": "whole", "base_price": 140.00, "discount": 0.00},
                {"size": "half", "base_price": 120.00, "discount": 0.00},
            ],
        },
    )

    pytest.helpers.assert_responses_equal(
        response,
        200,
        {
            "dessert_id": "00000000-0000-0000-0000-000000000001",
            "name": "Chocolate Cake",
            "description": "A delicious chocolate cake  ",
            "dessert_type": "cake",
            "created_at": 1734004800,
            "last_updated_at": 1734004800,
            "visible": True,
            "prices": [
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "slice",
                    "base_price": 15.00,
                    "discount": 0.00,
                },
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "whole",
                    "base_price": 140.00,
                    "discount": 0.00,
                },
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "half",
                    "base_price": 120.00,
                    "discount": 0.00,
                },
            ],
            "ingredients": ["flour", "sugar", "cocoa", "butter", "eggs"],
            "images": [
                {
                    "image_id": "IMAGE-1",
                    "url": "https://example.com/image1.jpg",
                    "position": 1,
                    "file_name": "image1.jpg",
                    "file_type": "jpg",
                }
            ],
        },
    )


@freeze_time("2024-12-12 12:00:00")
def test_handler_patch_dessert_not_found(desserts_dynamodb_stub):
    desserts_dynamodb_stub.add_response(
        "get_item",
        {},
        expected_params={
            "TableName": "desserts",
            "Key": {"dessert_id": "00000000-0000-0000-0000-000000000001"},
        },
    )

    response = test_client.patch(
        "/desserts/00000000-0000-0000-0000-000000000001",
        json={"visible": True},
    )

    pytest.helpers.assert_responses_equal(
        response, 404, {"detail": "Dessert not found"}
    )


@freeze_time("2024-12-12 12:00:00")
@patch(
    "src.routes.patch_dessert.s3_client.generate_presigned_url",
    return_value="https://example.com/upload-url",
)
@patch("src.routes.patch_dessert.prices_table")
@patch(
    "uuid.uuid4",
    side_effect=[
        uuid.UUID("00000000-0000-0000-0000-000000000002"),
    ],
)
def test_handler_patch_dessert_images_change_image_position(
    mock_uuid, mock_prices_table, mock_s3_client, desserts_dynamodb_stub
):
    mock_batch_writer = MagicMock()
    mock_prices_table.batch_writer.__enter__.return_value = mock_batch_writer

    desserts_dynamodb_stub.add_response(
        "get_item",
        {
            "Item": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "whole"},
                                "base_price": {"N": "40.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                    ]
                },
                "ingredients": {"SS": ["flour", "sugar", "cocoa", "butter", "eggs"]},
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
                                "image_id": {"S": "IMAGE-3"},
                                "url": {"S": "https://example.com/image3.jpg"},
                                "upload_url": {"S": "https://example.com/upload-url"},
                                "position": {"N": "2"},
                                "file_name": {"S": "image3.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        },
                        {
                            "M": {
                                "image_id": {"S": "IMAGE-2"},
                                "url": {"S": "https://example.com/image2.jpg"},
                                "upload_url": {"S": "https://example.com/upload-url"},
                                "position": {"N": "3"},
                                "file_name": {"S": "image2.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        },
                    ]
                },
            }
        },
    )

    desserts_dynamodb_stub.add_response(
        "update_item",
        {
            "Attributes": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
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
                        {
                            "M": {
                                "image_id": {"S": "IMAGE-3"},
                                "url": {"S": "https://example.com/image3.jpg"},
                                "upload_url": {"S": "https://example.com/upload-url"},
                                "position": {"N": "3"},
                                "file_name": {"S": "image3.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        },
                    ]
                },
            }
        },
        expected_params={
            "TableName": "desserts",
            "Key": {"dessert_id": "00000000-0000-0000-0000-000000000001"},
            "UpdateExpression": "SET #images = :images, #last_updated_at = :last_updated_at",
            "ExpressionAttributeNames": {
                "#images": "images",
                "#last_updated_at": "last_updated_at",
            },
            "ExpressionAttributeValues": {
                ":images": [
                    {
                        "image_id": "IMAGE-1",
                        "url": "https://example.com/image1.jpg",
                        "upload_url": "https://example.com/upload-url",
                        "position": 1,
                        "file_name": "image1.jpg",
                        "file_type": "jpg",
                    },
                    {
                        "image_id": "IMAGE-2",
                        "url": "https://example.com/image2.jpg",
                        "upload_url": "https://example.com/upload-url",
                        "position": 2,
                        "file_name": "image2.jpg",
                        "file_type": "jpg",
                    },
                    {
                        "image_id": "IMAGE-3",
                        "url": "https://example.com/image3.jpg",
                        "upload_url": "https://example.com/upload-url",
                        "position": 3,
                        "file_name": "image3.jpg",
                        "file_type": "jpg",
                    },
                ],
                ":last_updated_at": 1734004800,
            },
            "ReturnValues": "ALL_NEW",
        },
    )

    response = test_client.patch(
        "/desserts/00000000-0000-0000-0000-000000000001",
        json={
            "images": [
                {
                    "image_id": "IMAGE-1",
                    "url": "https://example.com/image1.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 1,
                    "file_name": "image1.jpg",
                    "file_type": "jpg",
                },
                {
                    "image_id": "IMAGE-2",
                    "url": "https://example.com/image2.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 2,
                    "file_name": "image2.jpg",
                    "file_type": "jpg",
                },
                {
                    "image_id": "IMAGE-3",
                    "url": "https://example.com/image3.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 3,
                    "file_name": "image3.jpg",
                    "file_type": "jpg",
                },
            ]
        },
    )

    pytest.helpers.assert_responses_equal(
        response,
        200,
        {
            "dessert_id": "00000000-0000-0000-0000-000000000001",
            "name": "Chocolate Cake",
            "description": "A delicious chocolate cake",
            "dessert_type": "cake",
            "created_at": 1734004800,
            "last_updated_at": 1734004800,
            "visible": False,
            "prices": [
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "slice",
                    "base_price": 5.00,
                    "discount": 0.00,
                },
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "whole",
                    "base_price": 40.00,
                    "discount": 0.00,
                },
            ],
            "ingredients": ["flour", "sugar", "cocoa", "butter", "eggs"],
            "images": [
                {
                    "image_id": "IMAGE-1",
                    "url": "https://example.com/image1.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 1,
                    "file_name": "image1.jpg",
                    "file_type": "jpg",
                },
                {
                    "image_id": "IMAGE-2",
                    "url": "https://example.com/image2.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 2,
                    "file_name": "image2.jpg",
                    "file_type": "jpg",
                },
                {
                    "image_id": "IMAGE-3",
                    "url": "https://example.com/image3.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 3,
                    "file_name": "image3.jpg",
                    "file_type": "jpg",
                },
            ],
        },
    )


@freeze_time("2024-12-12 12:00:00")
@patch(
    "src.routes.patch_dessert.s3_client.generate_presigned_url",
    return_value="https://example.com/upload-url",
)
@patch("src.routes.patch_dessert.prices_table")
@patch(
    "uuid.uuid4",
    side_effect=[
        uuid.UUID("00000000-0000-0000-0000-000000000002"),
    ],
)
def test_handler_patch_dessert_images_add_image(
    mock_uuid, mock_prices_table, mock_s3_client, desserts_dynamodb_stub
):
    mock_batch_writer = MagicMock()
    mock_prices_table.batch_writer.__enter__.return_value = mock_batch_writer

    desserts_dynamodb_stub.add_response(
        "get_item",
        {
            "Item": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "whole"},
                                "base_price": {"N": "40.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                    ]
                },
                "ingredients": {"SS": ["flour", "sugar", "cocoa", "butter", "eggs"]},
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
                    ]
                },
            }
        },
    )

    desserts_dynamodb_stub.add_response(
        "update_item",
        {
            "Attributes": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
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
                                "image_id": {
                                    "S": "00000000-0000-0000-0000-000000000002"
                                },
                                "url": {
                                    "S": "https://dessert-images.s3.amazonaws.com/00000000-0000-0000-0000-000000000001/00000000-0000-0000-0000-000000000002"
                                },
                                "upload_url": {"S": "https://example.com/upload-url"},
                                "position": {"N": "2"},
                                "file_name": {"S": "image2.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        },
                    ]
                },
            }
        },
        expected_params={
            "TableName": "desserts",
            "Key": {"dessert_id": "00000000-0000-0000-0000-000000000001"},
            "UpdateExpression": "SET #images = :images, #last_updated_at = :last_updated_at",
            "ExpressionAttributeNames": {
                "#images": "images",
                "#last_updated_at": "last_updated_at",
            },
            "ExpressionAttributeValues": {
                ":images": [
                    {
                        "image_id": "IMAGE-1",
                        "url": "https://example.com/image1.jpg",
                        "upload_url": "https://example.com/upload-url",
                        "position": 1,
                        "file_name": "image1.jpg",
                        "file_type": "jpg",
                    },
                    {
                        "image_id": "00000000-0000-0000-0000-000000000002",
                        "url": "https://dessert-images.s3.amazonaws.com/00000000-0000-0000-0000-000000000001/00000000-0000-0000-0000-000000000002",
                        "upload_url": "https://example.com/upload-url",
                        "position": 2,
                        "file_name": "image2.jpg",
                        "file_type": "jpg",
                    },
                ],
                ":last_updated_at": 1734004800,
            },
            "ReturnValues": "ALL_NEW",
        },
    )

    response = test_client.patch(
        "/desserts/00000000-0000-0000-0000-000000000001",
        json={
            "images": [
                {
                    "image_id": "IMAGE-1",
                    "url": "https://example.com/image1.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 1,
                    "file_name": "image1.jpg",
                    "file_type": "jpg",
                },
                {
                    "position": 2,
                    "file_name": "image2.jpg",
                    "file_type": "jpg",
                },
            ]
        },
    )

    pytest.helpers.assert_responses_equal(
        response,
        200,
        {
            "dessert_id": "00000000-0000-0000-0000-000000000001",
            "name": "Chocolate Cake",
            "description": "A delicious chocolate cake",
            "dessert_type": "cake",
            "created_at": 1734004800,
            "last_updated_at": 1734004800,
            "visible": False,
            "prices": [
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "slice",
                    "base_price": 5.00,
                    "discount": 0.00,
                },
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "whole",
                    "base_price": 40.00,
                    "discount": 0.00,
                },
            ],
            "ingredients": ["flour", "sugar", "cocoa", "butter", "eggs"],
            "images": [
                {
                    "image_id": "IMAGE-1",
                    "url": "https://example.com/image1.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 1,
                    "file_name": "image1.jpg",
                    "file_type": "jpg",
                },
                {
                    "image_id": "00000000-0000-0000-0000-000000000002",
                    "url": "https://dessert-images.s3.amazonaws.com/00000000-0000-0000-0000-000000000001/00000000-0000-0000-0000-000000000002",
                    "upload_url": "https://example.com/upload-url",
                    "position": 2,
                    "file_name": "image2.jpg",
                    "file_type": "jpg",
                },
            ],
        },
    )


@freeze_time("2024-12-12 12:00:00")
@patch(
    "src.routes.patch_dessert.s3_client.generate_presigned_url",
    return_value="https://example.com/upload-url",
)
@patch("src.routes.patch_dessert.prices_table")
@patch(
    "uuid.uuid4",
    side_effect=[
        uuid.UUID("00000000-0000-0000-0000-000000000002"),
    ],
)
def test_handler_patch_dessert_images_remove_image(
    mock_uuid, mock_prices_table, mock_s3_client, desserts_dynamodb_stub, s3_stub
):
    mock_batch_writer = MagicMock()
    mock_prices_table.batch_writer.__enter__.return_value = mock_batch_writer

    desserts_dynamodb_stub.add_response(
        "get_item",
        {
            "Item": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "whole"},
                                "base_price": {"N": "40.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                    ]
                },
                "ingredients": {"SS": ["flour", "sugar", "cocoa", "butter", "eggs"]},
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
        },
    )

    s3_stub.add_response(
        "delete_object",
        {},
        expected_params={
            "Bucket": "dessert-images",
            "Key": f"00000000-0000-0000-0000-000000000001/IMAGE-1",
        },
    )

    desserts_dynamodb_stub.add_response(
        "update_item",
        {
            "Attributes": {
                "dessert_id": {"S": "00000000-0000-0000-0000-000000000001"},
                "name": {"S": "Chocolate Cake"},
                "description": {"S": "A delicious chocolate cake"},
                "dessert_type": {"S": "cake"},
                "created_at": {"N": "1734004800"},
                "last_updated_at": {"N": "1734004800"},
                "visible": {"BOOL": False},
                "prices": {
                    "L": [
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
                                "size": {"S": "slice"},
                                "base_price": {"N": "5.00"},
                                "discount": {"N": "0.00"},
                            }
                        },
                        {
                            "M": {
                                "dessert_id": {
                                    "S": "00000000-0000-0000-0000-000000000001"
                                },
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
                                "image_id": {"S": "IMAGE-2"},
                                "url": {"S": "https://example.com/image2.jpg"},
                                "upload_url": {"S": "https://example.com/upload-url"},
                                "position": {"N": "1"},
                                "file_name": {"S": "image2.jpg"},
                                "file_type": {"S": "jpg"},
                            }
                        },
                    ]
                },
            }
        },
        expected_params={
            "TableName": "desserts",
            "Key": {"dessert_id": "00000000-0000-0000-0000-000000000001"},
            "UpdateExpression": "SET #images = :images, #last_updated_at = :last_updated_at",
            "ExpressionAttributeNames": {
                "#images": "images",
                "#last_updated_at": "last_updated_at",
            },
            "ExpressionAttributeValues": {
                ":images": [
                    {
                        "image_id": "IMAGE-2",
                        "url": "https://example.com/image2.jpg",
                        "upload_url": "https://example.com/upload-url",
                        "position": 1,
                        "file_name": "image2.jpg",
                        "file_type": "jpg",
                    },
                ],
                ":last_updated_at": 1734004800,
            },
            "ReturnValues": "ALL_NEW",
        },
    )

    response = test_client.patch(
        "/desserts/00000000-0000-0000-0000-000000000001",
        json={
            "images": [
                {
                    "image_id": "IMAGE-2",
                    "url": "https://example.com/image2.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 1,
                    "file_name": "image2.jpg",
                    "file_type": "jpg",
                },
            ]
        },
    )

    pytest.helpers.assert_responses_equal(
        response,
        200,
        {
            "dessert_id": "00000000-0000-0000-0000-000000000001",
            "name": "Chocolate Cake",
            "description": "A delicious chocolate cake",
            "dessert_type": "cake",
            "created_at": 1734004800,
            "last_updated_at": 1734004800,
            "visible": False,
            "prices": [
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "slice",
                    "base_price": 5.00,
                    "discount": 0.00,
                },
                {
                    "dessert_id": "00000000-0000-0000-0000-000000000001",
                    "size": "whole",
                    "base_price": 40.00,
                    "discount": 0.00,
                },
            ],
            "ingredients": ["flour", "sugar", "cocoa", "butter", "eggs"],
            "images": [
                {
                    "image_id": "IMAGE-2",
                    "url": "https://example.com/image2.jpg",
                    "upload_url": "https://example.com/upload-url",
                    "position": 1,
                    "file_name": "image2.jpg",
                    "file_type": "jpg",
                },
            ],
        },
    )
