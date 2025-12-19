from typing import List

from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.customer import Customers

from app.enums.payment import PaymentTypeEnum
from app.enums.pricing import PricingTypeEnum
from app.enums.customer import CustomerVisitTypeEnum, CustomerStatusEnum

from app.services.pricing import PricingService
from app.services.membership import MembershipService

from app.utils.datetime_utils import DatetimeUtils

from app.repositories.customer import CustomerRepository

from app.exceptions.general import NotFoundException, UnlimitedVisitPricingException

from app.schemas.statistic import CustomerStatisticSchema
from app.schemas.customer import CustomerCreateSchema, CustomerSchema, CustomerFindSchema


class CustomerService:
    def __init__(self, db: AsyncSession):
        self.pricing_service = PricingService(db=db)
        self.membership_service = MembershipService(db=db)

        self.repository = CustomerRepository(db)

    async def get_statistics(self, params: CustomerStatisticSchema):
        customers = await self.repository.get_customers(
            from_time=params.from_time,
            to_time=params.to_time,
            status=params.status
        )

        income = 0
        for customer in customers:
            income += customer.payment_amount or 0

        return {'income': income}

    async def find(self, filters: CustomerFindSchema) -> List[CustomerSchema]:
        return await self.repository.find(
            sort_by_start_time_desc=True,
            **filters.model_dump(exclude_none=True)
        )

    async def get_active_customers(self):
        current_time = DatetimeUtils.get_datetime()
        return await self.repository.get_active_customers(
            current_time=current_time,
        )

    async def create(self, customer: CustomerCreateSchema) -> CustomerSchema:
        start_time = DatetimeUtils.get_datetime()
        end_time = DatetimeUtils.end_of_today()

        if customer.payment_type == PaymentTypeEnum.MEMBERSHIP:
            membership = await self.membership_service.validate_and_use_membership_visit(
                membership_id=customer.membership_id
            )

            customer.last_name=membership.lsat_name
            customer.first_name=membership.first_name
        elif customer.visit_type == CustomerVisitTypeEnum.HOURLY:
            end_time = await self.pricing_service.determine_visit_end_time(
                payment_amount=customer.payment_amount,
            )
        elif customer.visit_type == CustomerVisitTypeEnum.UNLIMITED:
            prices = await self.pricing_service.get_prices(pricing_type=PricingTypeEnum.UNLIMITED)
            unlimited_visit_price = prices[0].price

            if customer.payment_amount != unlimited_visit_price:
                raise UnlimitedVisitPricingException(
                    actual_price=unlimited_visit_price,
                    payed_amount=customer.payment_amount,
                )

        customer = await self.repository.create(
            start_time=start_time,
            end_time=end_time,
            status=CustomerStatusEnum.SUCCESSFUL,
            **customer.model_dump()
        )
        return customer

    async def update(self, customer_id: int, updates: dict | BaseModel) -> Customers:
        if not isinstance(updates, dict):
            updates = updates.model_dump(exclude_none=True)

        customer = await self.repository.find(id=customer_id, status=CustomerStatusEnum.SUCCESSFUL, get_first=True)
        if not customer:
            raise NotFoundException(data_name='Customer')

        for key, value in updates.items():
            setattr(customer, key, value)

        await self.repository.save_to_db(customer, commit=True)
        return customer

    async def delete(self, customer_id: int, deleting_reason: str):
        customer = await self.update(
            customer_id=customer_id,
            updates={
                'deleting_reason': deleting_reason,
                'status': CustomerStatusEnum.DELETED,
            }
        )

        if customer.payment_type == PaymentTypeEnum.MEMBERSHIP:
            await self.membership_service.delete_visit(membership_id=customer.membership_id)
