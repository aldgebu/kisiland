from pydantic import BaseModel

from app.enums.pricing import PricingTypeEnum


class PricingSchema(BaseModel):
    price: float
    type: PricingTypeEnum
