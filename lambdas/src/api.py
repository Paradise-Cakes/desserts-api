from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from mangum import Mangum

from src.routes import (
    delete_dessert,
    get_dessert,
    get_desserts,
    post_dessert,
    patch_dessert,
)

app = FastAPI(title="Desserts API", version="1.0.0", root_path="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(delete_dessert.router)
app.include_router(get_dessert.router)
app.include_router(get_desserts.router)
app.include_router(post_dessert.router)
app.include_router(patch_dessert.router)


def lambda_handler(event, context):
    handler = Mangum(app, lifespan="on", api_gateway_base_path="/v1")
    return handler(event, context)
