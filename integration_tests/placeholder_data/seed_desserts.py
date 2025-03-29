from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import boto3

load_dotenv(dotenv_path=".env.local")

client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION"))

response = client.initiate_auth(
    ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={
        "USERNAME": os.getenv("SUPER_ADMIN_TESTER_EMAIL"),
        "PASSWORD": os.getenv("SUPER_ADMIN_TESTER_PASSWORD"),
    },
)

access_token = response["AuthenticationResult"]["AccessToken"]

desserts = [
    {
        "name": "Chocolate Cake",
        "description": "A rich chocolate cake with layers of chocolate frosting.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "cocoa powder", "eggs", "butter"],
        "images": [
            {
                "url": "https://sugargeekshow.com/wp-content/uploads/2023/10/easy_chocolate_cake_slice.jpg",
                "file_name": "chocolate_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://theloopywhisk.com/wp-content/uploads/2021/05/Small-Batch-Gluten-Free-Chocolate-Cake_730px-featured.jpg",
                "file_name": "chocolate_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    }
]


for dessert in desserts:
    response = requests.post(
        "https://desserts-dev-api.megsparadisecakes.com/v1/desserts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=dessert,
    )
    print(f"Posted dessert: {dessert['name']}, Response: {response.status_code}")
