from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

from app.services.customer import CustomerService
from app.services.membership import MembershipService

from app.schemas.statistic import CustomerStatisticSchema, MembershipStatisticSchema


router = APIRouter(prefix='/statistic', tags=['statistic'])


@router.get('/customers', status_code=status.HTTP_200_OK)
async def get_statistic(
    params: CustomerStatisticSchema = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = CustomerService(db=db)
    return await service.get_statistics(params=params)


@router.get('/memberships')
async def get_memberships(
    params: MembershipStatisticSchema = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = MembershipService(db=db)
    return await service.get_statistics(params=params)
