from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.statistic import MembershipStatisticSchema
from app.schemas.membership import MembershipSchema, MembershipCreateSchema, MembershipFindSchema, \
    MembershipUpdateSchema

from app.repositories.membership import MembershipRepository

from app.exceptions.general import NotFoundException, MembershipVisitsLimitReachedException


class MembershipService:
    def __init__(self, db: AsyncSession):
        self.repository = MembershipRepository(db=db)

    async def get_statistics(self, params: MembershipStatisticSchema):
        memberships = await self.repository.get_memberships(from_time=params.from_time, to_time=params.to_time)

        income = 0
        for membership in memberships:
            income += membership.payment_amount or 0

        return {'income': income}

    async def find(self, membership_info: MembershipFindSchema):
        memberships = await self.repository.find(
            sort_by_created_at_desc=True,
            **membership_info.model_dump(exclude_none=True)
        )

        income = await self.repository.get_memberships_total_income(
            **membership_info.model_dump(exclude={'page', 'page_size'})
        )

        return {
            'income': income,
            'memberships': memberships,
        }

    async def create(self, member_data: MembershipCreateSchema) -> MembershipSchema:
        return await self.repository.create(
            **member_data.model_dump()
        )

    async def update(self, membership_id: int, membership_updates: MembershipUpdateSchema):
        membership = await self.repository.find(id=membership_id, get_first=True)
        if not membership:
            raise NotFoundException('Membership')

        update_data = membership_updates.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(membership, key, value)

        await self.repository.save_to_db(membership, commit=True)
        return membership

    async def delete_membership(self, membership_id: int):
        if not await self.repository.delete_by_id(data_id=membership_id):
            raise NotFoundException('Membership')

    async def validate_and_use_membership_visit(self, membership_id: int):
        membership = await self.repository.find(id=membership_id, get_first=True)
        if not membership:
            raise NotFoundException('Membership')

        if not membership.visits < membership.allowed_visits:
            raise MembershipVisitsLimitReachedException()

        membership.visits += 1
        await self.repository.save_to_db(membership, commit=True)
        return membership

    async def delete_visit(self, membership_id: int):
        membership = await self.repository.find(id=membership_id, get_first=True)
        if not membership:
            raise NotFoundException('Membership')

        membership.visits = membership.visits - 1
        await self.repository.save_to_db(membership, commit=True)

        return membership
