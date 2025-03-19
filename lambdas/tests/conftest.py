import json

import pytest


@pytest.fixture(autouse=True)
def monkeypatch_env(monkeypatch):
    monkeypatch.setenv("DYNAMODB_REGION", "us-east-1")
    monkeypatch.setenv("DYNAMODB_ENDPOINT_URL", "http://localhost:8000")
    monkeypatch.setenv("DYNAMODB_DESSERTS_TABLE_NAME", "desserts")
    monkeypatch.setenv("DESSERT_IMAGES_BUCKET_NAME", "dessert-images")
    monkeypatch.setenv("DYNAMODB_PRICES_TABLE_NAME", "prices")
    monkeypatch.setenv("DYNAMODB_DESSERT_TYPE_COUNT_TABLE_NAME", "dessert_type_count")
    monkeypatch.setenv("REGION", "us-east-1")


@pytest.helpers.register
def assert_response_equal(r1, r2):
    assert json.loads(r1.get("body")) == json.loads(r2.get("body"))
    assert r1.get("statusCode") == r2.get("statusCode")


@pytest.helpers.register
def assert_responses_equal(r1, status_code=None, r2=None, headers=None):
    assert (
        status_code or json or headers
    ), "You must assert one of: status_code, json, or headers"

    if status_code:
        assert r1.status_code == status_code

    if r2:
        assert r1.json() == r2
