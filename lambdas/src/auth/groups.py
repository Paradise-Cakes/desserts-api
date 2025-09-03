from fastapi import Depends, HTTPException

from src.auth.claims import get_jwt_claims


def require_admin_user(claims=Depends(get_jwt_claims)):
    groups = claims.get("cognito:groups", [])
    if "admins" not in groups:
        raise HTTPException(status_code=404, detail="Not found")
