from typing import Optional

from motor.motor_asyncio import AsyncIOMotorDatabase

from datetime import datetime

from app.enums.customer import CustomerStatusEnum

from app.repositories.document import DocumentRepository


class CustomerRepository(DocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = 'customers'
        self.collection = self.db[self.collection_name]

        super().__init__(db=self.db, collection_name=self.collection_name)

    async def get_active_customers(self, current_time: datetime):
        cursor = self.collection.find(
            {
                'start_time': {'$lte': current_time},
                'end_time': {'$gte': current_time},
                'status': CustomerStatusEnum.SUCCESSFUL,
            }
        )

        cursor.sort([('start_time', -1)])
        return await cursor.to_list(length=None)

    async def get_customers(
        self,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        status: Optional[CustomerStatusEnum] = None
    ):
        filters = {}

        if from_time or to_time:
            filters['start_time'] = {}
            if from_time:
                filters['start_time']['$gte'] = from_time
            if to_time:
                filters['start_time']['$lte'] = to_time

        if status:
            filters['status'] = status

        cursor = self.collection.find(filters)
        return await cursor.to_list(length=None)
