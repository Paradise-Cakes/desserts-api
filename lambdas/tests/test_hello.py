import pytest
from fastapi.testclient import TestClient

from src.api import app

test_client = TestClient(app)


def test_hello():
    response = test_client.get("/hello")
    pytest.helpers.assert_responses_equal(
        response,
        200,
        {"message": "Hello, world!"},
    )
