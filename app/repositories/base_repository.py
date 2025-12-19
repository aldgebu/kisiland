from typing import Optional

from sqlalchemy import select, delete, desc

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, db: AsyncSession, model=None):
        self.db = db
        self.model = model

    async def save_to_db(self, obj, flush: bool = False, commit: bool = False):
        try:
            self.db.add(obj)
            if flush:
                await self.db.flush()
            if commit:
                await self.commit_session()
            await self.db.refresh(obj)
        except Exception as e:
            try:
                await self.db.rollback()
            except Exception as e:
                pass

    async def remove_from_db(self, obj, flush: bool = False, commit: bool = False):
        try:
            await self.db.delete(obj)
            if flush:
                await self.db.flush()
            if commit:
                await self.commit_session()
        except Exception as e:
            try:
                await self.db.rollback()
            except Exception as e:
                pass

    async def commit_session(self):
        try:
            await self.db.commit()
        except Exception as e:
            pass

    # General methods all models
    async def find(
        self,
        type: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        membership_id: Optional[str] = None,
        payment_type: Optional[str] = None,
        visit_type: Optional[str] = None,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        personal_number: Optional[str] = None,
        parent_first_name: Optional[str] = None,
        parent_last_name: Optional[str] = None,
        status: Optional[str] = None,
        username: Optional[str] = None,
        sort_by_start_time_desc: bool = False,
        sort_by_created_at_desc: bool = False,
        get_first: bool = False,
    ):
        stmt = select(self.model)

        if id:
            stmt = stmt.where(self.model.id == id)
        if type:
            stmt = stmt.where(self.model.type == type)
        if first_name:
            stmt = stmt.where(self.model.first_name == first_name)
        if last_name:
            stmt = stmt.where(self.model.last_name == last_name)
        if membership_id:
            stmt = stmt.where(self.model.membership_id == membership_id)
        if payment_type:
            stmt = stmt.where(self.model.payment_type == payment_type)
        if personal_number:
            stmt = stmt.where(self.model.personal_number == personal_number)
        if parent_first_name:
            stmt = stmt.where(self.model.parent_first_name == parent_first_name)
        if parent_last_name:
            stmt = stmt.where(self.model.parent_last_name == parent_last_name)
        if visit_type:
            stmt = stmt.where(self.model.visit_type == visit_type)
        if from_time:
            stmt = stmt.where(from_time <= self.model.start_time)
        if to_time:
            stmt = stmt.where(self.model.start_time <= to_time)
        if username:
            stmt = stmt.where(self.model.username == username)
        if status:
            stmt = stmt.where(self.model.status == status)

        if sort_by_start_time_desc:
            stmt = stmt.order_by(desc(self.model.start_time))
        if sort_by_created_at_desc:
            stmt = stmt.order_by(desc(self.model.created_at))

        if page and page_size:
            stmt = stmt.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(stmt)

        if get_first:
            return result.scalars().first()
        return result.scalars().all()

    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        await self.save_to_db(obj, commit=True)
        return obj

    async def delete_by_id(self, data_id: int):
        stmt = delete(self.model).where(self.model.id == data_id)

        result = await self.db.execute(stmt)
        await self.commit_session()
        return int(result.rowcount or 0)
