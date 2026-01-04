from typing import Optional

from datetime import datetime

from operator import le, eq

from sqlalchemy import select, func

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.membership import Membership

from app.repositories.base_repository import BaseRepository


class MembershipRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Membership

        super().__init__(db=self.db, model=self.model)

    async def get_memberships(
        self,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
    ):
        stmt = select(self.model)

        if from_time:
            stmt = stmt.where(le(from_time, self.model.created_at))
        if to_time:
            stmt = stmt.where(le(self.model.created_at, to_time))

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_memberships_total_income(
        self,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        personal_number: Optional[str] = None,
        parent_last_name: Optional[str] = None,
        parent_first_name: Optional[str] = None,
    ):
        stmt = select(func.coalesce(func.sum(self.model.payment_amount), 0))

        if last_name:
            stmt = stmt.where(eq(self.model.last_name, last_name))
        if first_name:
            stmt = stmt.where(eq(self.model.first_name, first_name))
        if personal_number:
            stmt = stmt.where(eq(self.model.personal_number, personal_number))
        if parent_last_name:
            stmt = stmt.where(eq(self.model.parent_last_name, parent_last_name))
        if parent_first_name:
            stmt = stmt.where(eq(self.model.parent_first_name, parent_first_name))

        result = await self.db.execute(stmt)
        return result.scalar_one()
