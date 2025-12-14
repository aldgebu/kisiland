from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.pricing import router as pricing_router
from app.routers.customer import router as customer_router
from app.routers.membership import router as membership_router
from app.routers.statistics import router as statistics_router


def include_routers(app: FastAPI):
    app.include_router(auth_router)

    app.include_router(pricing_router)

    app.include_router(customer_router)
    app.include_router(membership_router)
    app.include_router(statistics_router)
