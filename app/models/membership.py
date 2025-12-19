from sqlalchemy import Column, Integer, Float, String, DateTime

from app.db import Base


class Membership(Base):
    __tablename__ = "membership"

    id = Column(Integer, primary_key=True)
    allowed_visits = Column(Integer, nullable=False)
    payment_amount = Column(Float, nullable=False)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    comment = Column(String, nullable=False)
    personal_number = Column(String(100), nullable=False)
    parent_first_name = Column(String(100), nullable=False)
    parent_last_name = Column(String(100), nullable=False)
