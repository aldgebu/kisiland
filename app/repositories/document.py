from typing import List, Tuple, Optional

from bson import ObjectId

from motor.motor_asyncio import AsyncIOMotorDatabase

from pymongo import ReturnDocument

from app.utils.datetime_utils import DatetimeUtils


class DocumentRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.db = db
        self.collection = db[collection_name]

    async def find(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort: Optional[List[Tuple[str, int]]] = None,
        **kwargs
    ):
        if kwargs.get('_id', None):
            kwargs['_id'] = ObjectId(kwargs['id'])

        if kwargs.get('id', None):
            kwargs['_id'] = ObjectId(kwargs['id'])
            kwargs.pop('id')

        if kwargs.get('start_time'):
            kwargs['start_time'] = {'$gte': kwargs['start_time']}

        if kwargs.get('end_time'):
            kwargs['end_time'] = {'$lte': kwargs['end_time']}

        cursor = self.collection.find(kwargs)
        if sort:
            cursor = cursor.sort(sort)

        if page is not None and page_size is not None:
            cursor = cursor.skip(page * page_size).limit(page_size)

        return await cursor.to_list(length=None)

    async def insert_one(self, **kwargs):
        kwargs['created_at'] = DatetimeUtils.get_datetime()

        result = await self.collection.insert_one(kwargs)
        return str(result.inserted_id)

    async def find_one_and_update(self, filters: dict, updates: dict):
        updates['updated_at'] = DatetimeUtils.get_datetime()

        if filters.get('_id', None):
            filters['_id'] = ObjectId(filters['_id'])

        return await self.collection.find_one_and_update(
            filter=filters,
            update={'$set': updates},
            return_document=ReturnDocument.AFTER
        )

    async def delete_one(self, filters: dict):
        if filters.get('_id', None):
            filters['_id'] = ObjectId(filters['_id'])

        await self.collection.delete_one(filter=filters)
