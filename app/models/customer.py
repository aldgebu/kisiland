from sqlalchemy import Column, Integer, DateTime, Enum, String, Float, ForeignKey

from app.db import Base

from app.enums.payment import PaymentTypeEnum
from app.enums.customer import CustomerStatusEnum, CustomerVisitTypeEnum


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    comment = Column(String, nullable=True)
    payment_amount = Column(Float, nullable=True)

    start_time = Column(DateTime)
    end_time = Column(DateTime)

    membership_id = Column(String(100), ForeignKey('membership.id'), nullable=True)

    status = Column(
        Enum(
            CustomerStatusEnum,
            name='customer_status_enum',
            native_enum=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    visit_type = Column(
        Enum(
            CustomerVisitTypeEnum,
            name='customer_visit_type_enum',
            native_enum=True,
            validate_strings=True,
        ),
        nullable=False,
    )
    payment_type = Column(
        Enum(
            PaymentTypeEnum,
            name='payment_type_enum',
            native_enum=True,
            validate_strings=True,
        ),
        nullable=False,
    )
