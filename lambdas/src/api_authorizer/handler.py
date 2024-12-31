import jwt
from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    try:
        resource = event.get("methodArn")
        token = event.get("headers").get("Authorization").split("Bearer ")[1]
        decoded_token = jwt.decode(token, options={"verify_signature": False})

        user_email = decoded_token.get("email")
        user_groups = decoded_token.get("cognito:groups", [])

        return generate_policy("Allow", resource, user_email, user_groups)

    except Exception as e:
        logger.exception(e)
        return generate_policy("Deny", event["methodArn"], None, None)


def generate_policy(effect, resource, user_email, user_groups):
    policy = {
        "principalId": user_email if user_email else "Unknown",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {"Action": "execute-api:Invoke", "Effect": effect, "Resource": resource}
            ],
        },
        "context": {
            "user_email": user_email,
            "user_groups": user_groups if user_groups else [],
        },
    }
    return policy
