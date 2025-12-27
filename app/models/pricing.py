from sqlalchemy import Integer, Column, Float, Enum

from app.db import Base

from app.enums.pricing import PricingTypeEnum


class Pricing(Base):
    __tablename__ = "pricing"

    id = Column(Integer, primary_key=True)

    price = Column(Float, nullable=False)
    type = Column(
        Enum(
            PricingTypeEnum,
            name='pricing_type_enum',
            native_enum=True,
            validate_strings=True
        ),
        nullable=False
    )
