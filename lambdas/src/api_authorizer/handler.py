import jwt

from src.lib.logger import logger


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    try:
        resource = event.get("methodArn")
        token = event.get("headers").get("Authorization").split("Bearer ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        user_sub = decoded_token.get("sub")
        user_groups = decoded_token.get("cognito:groups", [])

        return generate_policy("Allow", resource, user_sub, user_groups)

    except Exception as e:
        logger.exception(e)
        return generate_policy("Deny", event["methodArn"], None, None)


def generate_policy(effect, resource, user_sub, user_groups):
    policy = {
        "principalId": user_sub if user_sub else "Unknown",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        },
        "context": {
            "user_sub": user_sub,
            "user_groups": ",".join(user_groups) if user_groups else "",
        },
    }
    return policy
