from fastapi import FastAPI, Request

from app.db import engine

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

    @fastapi_app.middleware("http")
    async def dispose_engine_middleware(request: Request, call_next):
        response = await call_next(request)
        await engine.dispose()
        return response

    return fastapi_app


app = create_fastapi_app()
