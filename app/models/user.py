from sqlalchemy import Column, Integer, String, Enum

from app.db import Base
from app.enums.user import UserStatusEnum


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    status = Column(
        Enum(
            UserStatusEnum,
            name='user_status_enum',
            native_enum=True,
            validate_strings=True
        ),
        nullable=False
    )
