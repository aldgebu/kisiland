from fastapi import FastAPI

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from app.exceptions.general import register_exceptions
from app.mongo import connect_to_mongo_db, disconnect_to_mongo_db

from app.routers.api import include_routers


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await connect_to_mongo_db()

    yield

    await disconnect_to_mongo_db()


def create_fastapi_app() -> FastAPI:
    fastapi_app = FastAPI(lifespan=lifespan)

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
