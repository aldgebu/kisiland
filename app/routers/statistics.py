from fastapi import APIRouter, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.mongo import get_mongo_db
from app.schemas.statistic import CustomerStatisticSchema, MembershipStatisticSchema
from app.services.customer import CustomerService
from app.services.membership import MembershipService

router = APIRouter(prefix='/statistic', tags=['statistic'])


@router.get('/customers', status_code=status.HTTP_200_OK)
async def get_statistic(
    params: CustomerStatisticSchema = Depends(),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    service = CustomerService(db=mongo_db)
    return await service.get_statistics(params=params)


@router.get('/memberships')
async def get_memberships(
    params: MembershipStatisticSchema = Depends(),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
):
    service = MembershipService(db=mongo_db)
    return await service.get_statistics(params=params)
