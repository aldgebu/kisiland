from typing import Optional

from pydantic import BaseModel

from datetime import datetime

from app.enums.customer import CustomerStatusEnum


class MembershipStatisticSchema(BaseModel):
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None


class CustomerStatisticSchema(MembershipStatisticSchema):
    status: Optional[CustomerStatusEnum] = None
