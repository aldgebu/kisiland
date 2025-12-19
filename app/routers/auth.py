from fastapi import APIRouter, status, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

from app.schemas.auth import AuthSchema
from app.services.auth import AuthService


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('', status_code=status.HTTP_201_CREATED)
async def authenticate(
    auth_data: AuthSchema,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db=db)
    return await service.authenticate(auth_data=auth_data)
