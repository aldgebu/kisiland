from typing import AsyncGenerator

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.settings import settings
from app.utils.datetime_utils import DatetimeUtils


class Base(declarative_base()):
    created_at = Column(DateTime, nullable=False, default=lambda: DatetimeUtils.get_datetime())


engine = create_async_engine(settings.database_url, pool_pre_ping=True)

AsyncSessionLocal: sessionmaker[AsyncSession] = sessionmaker(  # type: ignore
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
