from typing import Optional

from datetime import datetime

from operator import le, eq

from sqlalchemy import select, desc

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customers

from app.enums.customer import CustomerStatusEnum

from app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Customers

        super().__init__(db=self.db, model=self.model)

    async def get_active_customers(self, current_time: datetime):
        stmt = (
            select(self.model)
            .where(
                le(self.model.start_time, current_time),
                le(current_time, self.model.end_time),
                self.model.status == CustomerStatusEnum.SUCCESSFUL
            )
        )

        stmt = stmt.order_by(desc(self.model.start_time))  # type: ignore - pycharm wrong warning!

        result = await self.db.execute(stmt)
        return result.scalars().all()

    async def get_customers(
        self,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        status: Optional[CustomerStatusEnum] = None
    ):
        stmt = select(self.model)

        if from_time:
            stmt = stmt.where(le(from_time, self.model.start_time))
        if to_time:
            stmt = stmt.where(le(self.model.start_time, to_time))
        if status:
            stmt = stmt.where(eq(self.model.status, status))

        result = await self.db.execute(stmt)
        return result.scalars().all()
