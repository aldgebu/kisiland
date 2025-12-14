from typing import Optional

from datetime import datetime

from pydantic import BaseModel, model_validator

from app.enums.payment import PaymentTypeEnum

from app.enums.customer import CustomerVisitTypeEnum, CustomerStatusEnum
from app.schemas.pagination import PaginationSchema


class CustomerCreateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    visit_type: CustomerVisitTypeEnum = CustomerVisitTypeEnum.UNLIMITED

    payment_type: PaymentTypeEnum
    membership_id: Optional[str] = None
    payment_amount: Optional[float] = None

    comment: Optional[str] = None


class CustomerUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    comment: Optional[str] = None


class CustomerFindSchema(PaginationSchema):
    id: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None

    membership_id: Optional[str] = None

    status: Optional[CustomerStatusEnum] = None

    payment_type: Optional[PaymentTypeEnum] = None
    visit_type: Optional[CustomerVisitTypeEnum] = None

    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class CustomerSchema(CustomerCreateSchema):
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None

    status: CustomerStatusEnum

    @model_validator(mode='before')
    @classmethod
    def validate_before(cls, data: dict):
        _id = data.get('_id')
        if _id and not isinstance(_id, str):
            data['id'] = str(data['_id'])

        return data
