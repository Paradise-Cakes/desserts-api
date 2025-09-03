from fastapi import HTTPException, Request


def get_jwt_claims(request: Request) -> dict:
    try:
        claims = request.scope["aws.event"]["requestContext"]["authorizer"]["claims"]
        return claims
    except KeyError:
        raise HTTPException(status_code=401, detail="Unauthorized")
