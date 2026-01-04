from typing import Optional

from datetime import datetime

from operator import ge, le, eq

from sqlalchemy import select, desc, func

from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.payment import PaymentTypeEnum
from app.models.customer import Customers

from app.enums.customer import CustomerStatusEnum, CustomerVisitTypeEnum

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

    async def get_customers_total_income(
        self,
        id: Optional[int] = None,
        last_name: Optional[str] = None,
        first_name: Optional[str] = None,
        to_time: Optional[datetime] = None,
        from_time: Optional[datetime] = None,
        membership_id: Optional[int] = None,
        status: Optional[CustomerStatusEnum] = None,
        payment_type: Optional[PaymentTypeEnum] = None,
        visit_type: Optional[CustomerVisitTypeEnum] = None,
    ):
        stmt = select(func.coalesce(func.sum(self.model.payment_amount), 0))

        if id is not None:
            stmt = stmt.where(eq(self.model.id, id))
        if first_name is not None:
            stmt = stmt.where(eq(self.model.first_name, first_name))
        if last_name is not None:
            stmt = stmt.where(eq(self.model.last_name, last_name))
        if membership_id is not None:
            stmt = stmt.where(eq(self.model.membership_id, membership_id))
        if status is not None:
            stmt = stmt.where(eq(self.model.status, status))
        if payment_type is not None:
            stmt = stmt.where(eq(self.model.payment_type, payment_type))
        if visit_type is not None:
            stmt = stmt.where(eq(self.model.visit_type, visit_type))
        if from_time is not None:
            stmt = stmt.where(ge(self.model.start_time, from_time))
        if to_time is not None:
            stmt = stmt.where(le(self.model.end_time, to_time))

        result = await self.db.execute(stmt)
        return result.scalar_one()
