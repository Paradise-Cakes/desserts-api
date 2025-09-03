from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from src.auth.claims import get_jwt_claims


def test_get_jwt_claims():
    request = MagicMock()
    request.scope = {
        "aws.event": {
            "requestContext": {
                "authorizer": {"claims": {"cognito:groups": ["admins", "users"]}}
            }
        }
    }
    claims = get_jwt_claims(request)
    assert claims == {"cognito:groups": ["admins", "users"]}


def test_get_jwt_claims_no_claims():
    request = MagicMock()
    request.scope = {"aws.event": {"requestContext": {"authorizer": {}}}}
    with pytest.raises(HTTPException) as exc:
        get_jwt_claims(request)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Unauthorized"
