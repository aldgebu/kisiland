from typing import Optional, Self, List

from pydantic import BaseModel, Field, model_validator

from app.schemas.pagination import PaginationSchema


class MembershipCreateSchema(BaseModel):
    allowed_visits: int = Field(..., ge=1)
    payment_amount: float = Field(..., ge=1)

    first_name: str
    last_name: str
    personal_number: Optional[str] = None
    parent_first_name: Optional[str] = None
    parent_last_name: Optional[str] = None

    comment: Optional[str] = None


class MembershipUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    personal_number: Optional[str] = None

    comment: Optional[str] = None

    parent_first_name: Optional[str] = None
    parent_last_name: Optional[str] = None


class MembershipFindSchema(PaginationSchema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    personal_number: Optional[str] = None
    parent_first_name: Optional[str] = None
    parent_last_name: Optional[str] = None


class MembershipSchema(MembershipCreateSchema):
    id: int
    visits: int
    remaining_visits: int = 0

    @model_validator(mode='after')
    @classmethod
    def validate_after(cls, data: Self):
        data.remaining_visits = data.allowed_visits - data.visits

        return data


class MembershipFindResponseSchema(BaseModel):
    income: float
    total_pages: int
    memberships: List[MembershipSchema]
