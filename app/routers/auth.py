from fastapi import APIRouter, status, Depends

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.mongo import get_mongo_db
from app.schemas.auth import AuthSchema
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def authenticate(
    auth_data: AuthSchema,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db)
):
    service = AuthService(db=mongo_db)
    return await service.authenticate(auth_data=auth_data)
