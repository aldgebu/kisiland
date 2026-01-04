from typing import List, Optional

from datetime import datetime

from pydantic import BaseModel

from app.enums.payment import PaymentTypeEnum

from app.enums.customer import CustomerVisitTypeEnum, CustomerStatusEnum
from app.schemas.pagination import PaginationSchema


class CustomerCreateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    visit_type: CustomerVisitTypeEnum = CustomerVisitTypeEnum.UNLIMITED

    payment_type: PaymentTypeEnum
    membership_id: Optional[int] = None
    payment_amount: Optional[float] = None

    comment: Optional[str] = None


class CustomerUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    comment: Optional[str] = None


class CustomerFindSchema(PaginationSchema):
    id: Optional[int] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    membership_id: Optional[int] = None

    status: Optional[CustomerStatusEnum] = None

    payment_type: Optional[PaymentTypeEnum] = None
    visit_type: Optional[CustomerVisitTypeEnum] = None

    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None


class CustomerSchema(CustomerCreateSchema):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None

    status: CustomerStatusEnum


class CustomerFindResponseSchema(BaseModel):
    income: float
    customers: List[CustomerSchema]
