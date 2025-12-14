from typing import List

from fastapi import APIRouter, status, Depends

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.mongo import get_mongo_db


from app.services.auth import AuthService
from app.services.customer import CustomerService

from app.schemas.customer import CustomerCreateSchema, CustomerUpdateSchema, CustomerSchema, CustomerFindSchema

router = APIRouter(prefix='/customer', tags=['Customers'])


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[CustomerSchema])
async def get_customers(
    filters: CustomerFindSchema = Depends(),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = CustomerService(db=mongo_db)
    return await service.find(filters=filters)


@router.get('/active', status_code=status.HTTP_200_OK, response_model=CustomerSchema)
async def get_active_customers(
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = CustomerService(db=mongo_db)
    return await service.get_active_customers()


@router.post('', status_code=status.HTTP_201_CREATED, response_model=CustomerSchema)
async def create_customer(
    customer: CustomerCreateSchema,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = CustomerService(db=mongo_db)
    return await service.create(customer=customer)


@router.put('', status_code=status.HTTP_200_OK, response_model=CustomerSchema)
async def update_customer(
    customer_id: str,
    customer_updates: CustomerUpdateSchema,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = CustomerService(db=mongo_db)
    return await service.update(customer_id=customer_id, updates=customer_updates)


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: str,
    deleting_reason: str,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = CustomerService(db=mongo_db)
    return await service.delete(customer_id=customer_id, deleting_reason=deleting_reason)
