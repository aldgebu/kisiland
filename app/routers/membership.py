from typing import List

from fastapi import APIRouter, Depends, status

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.mongo import get_mongo_db

from app.services.auth import AuthService
from app.services.membership import MembershipService

from app.schemas.membership import MembershipSchema, MembershipFindSchema, MembershipUpdateSchema, \
    MembershipCreateSchema


router = APIRouter(prefix='/membership', tags=['membership'])


@router.get('', status_code=status.HTTP_200_OK, response_model=List[MembershipSchema])
async def get_members(
    membership_info: MembershipFindSchema = Depends(),
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = MembershipService(db=mongo_db)
    return await service.find(membership_info=membership_info)


@router.post('', status_code=status.HTTP_201_CREATED, response_model=MembershipSchema)
async def create_membership(
    member_data: MembershipCreateSchema,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = MembershipService(db=mongo_db)
    return await service.create(member_data=member_data)


@router.put('', status_code=status.HTTP_200_OK, response_model=MembershipSchema)
async def update_membership(
    membership_id: str,
    membership_updates: MembershipUpdateSchema,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = MembershipService(db=mongo_db)
    return await service.update(membership_id=membership_id, membership_updates=membership_updates)


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_membership(
    membership_id: str,
    mongo_db: AsyncIOMotorDatabase = Depends(get_mongo_db),
    token_payload: dict = Depends(AuthService.token_required),
):
    service = MembershipService(db=mongo_db)
    await service.delete_membership(membership_id=membership_id)
