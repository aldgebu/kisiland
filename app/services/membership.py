from motor.motor_asyncio import AsyncIOMotorDatabase

from app.exceptions.general import NotFoundException, MembershipVisitsLimitReachedException
from app.schemas.membership import MembershipSchema, MembershipCreateSchema, MembershipFindSchema, \
    MembershipUpdateSchema

from app.repositories.membership import MembershipRepository
from app.schemas.statistic import MembershipStatisticSchema


class MembershipService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = MembershipRepository(db=db)

    async def get_statistics(self, params: MembershipStatisticSchema):
        memberships = await self.repository.get_memberships(from_time=params.from_time, to_time=params.to_time)

        income = 0
        for membership in memberships:
            income += membership['payment_amount'] or 0

        return {'income': income}

    async def find(self, membership_info: MembershipFindSchema):
        return await self.repository.find(
            sort=[('created_at', 1)],
            **membership_info.model_dump(exclude_none=True)
        )

    async def create(self, member_data: MembershipCreateSchema) -> MembershipSchema:
        inserted_id = await self.repository.insert_one(
            visits=0,
            **member_data.model_dump()
        )
        member = MembershipSchema(
            id=inserted_id,
            visits=0,
            **member_data.model_dump()
        )

        return member

    async def update(self, membership_id: str, membership_updates: MembershipUpdateSchema):
        updated_data = await self.repository.find_one_and_update(
            filters={'_id': membership_id},
            updates={**membership_updates.model_dump(exclude_none=True)}
        )

        return MembershipSchema(**updated_data)

    async def delete_membership(self, membership_id: str):
        await self.repository.delete_one(filters={'_id': membership_id})

    async def validate_and_use_membership_visit(self, membership_id: str):
        memberships = await self.repository.find(id=membership_id)
        if not memberships:
            raise NotFoundException('Membership')

        membership = memberships[0]
        if not membership['visits'] < membership['allowed_visits']:
            raise MembershipVisitsLimitReachedException()

        return await self.repository.find_one_and_update(
            filters={'_id': membership_id},
            updates={'visits': membership['visits'] + 1}
        )

    async def delete_visit(self, membership_id: str):
        membership = (await self.repository.find(id=membership_id))[0]

        membership = self.repository.find_one_and_update(
            filters={'_id': membership_id},
            updates={'visits': membership['visits'] - 1}
        )

        return membership
