from typing import List, Optional

from fastapi import APIRouter, Depends, status

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.enums.pricing import PricingTypeEnum

from app.mongo import get_mongo_db

from app.schemas.pricing import PricingSchema
from app.services.auth import AuthService

from app.services.pricing import PricingService


router = APIRouter(prefix='/price', tags=['Price'])


@router.get('', status_code=status.HTTP_200_OK, response_model=List[PricingSchema])
async def get_prices(
    pricing_type: Optional[PricingTypeEnum] = None,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = PricingService(db=mongo_db)
    return await service.get_prices(pricing_type=pricing_type)


@router.post('/hourly', status_code=status.HTTP_200_OK, response_model=PricingSchema)
async def change_hourly_membership_price(
    new_price: float,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = PricingService(db=mongo_db)
    return await service.change_price(new_price=new_price, pricing_type=PricingTypeEnum.HOURLY)


@router.post('/unlimited', status_code=status.HTTP_200_OK, response_model=PricingSchema)
async def change_unlimited_membership_price(
    new_price: float,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = PricingService(db=mongo_db)
    return await service.change_price(new_price=new_price, pricing_type=PricingTypeEnum.UNLIMITED)
