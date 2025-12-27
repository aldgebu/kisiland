from typing import Optional

from datetime import datetime

from operator import le

from sqlalchemy import select

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
