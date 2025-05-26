import pytest
from fastapi import HTTPException

from src.auth.groups import require_admin_user


def test_require_admin_user_success():
    claims = {"cognito:groups": ["admins", "users"]}
    require_admin_user(claims=claims)


def test_require_admin_user_no_groups():
    with pytest.raises(HTTPException) as exc:
        require_admin_user(claims={})
    assert exc.value.status_code == 404
    assert exc.value.detail == "Not found"


def test_require_admin_user_wrong_group():
    claims = {"cognito:groups": ["users"]}
    with pytest.raises(HTTPException) as exc:
        require_admin_user(claims=claims)
    assert exc.value.status_code == 404
