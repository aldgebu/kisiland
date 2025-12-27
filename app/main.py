from fastapi import FastAPI

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.general import register_exceptions

from app.routers.api import include_routers


def create_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI()

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    register_exceptions(fastapi_app)
    include_routers(fastapi_app)

    return fastapi_app


app = create_fastapi_app()
