from typing import Optional

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.document import DocumentRepository


class MembershipRepository(DocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = "memberships"

        super().__init__(db=db, collection_name=self.collection_name)

    async def get_memberships(
        self,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
    ):
        filters = {}

        if from_time or to_time:
            filters['created_at'] = {}
            if from_time:
                filters['created_at']['$gte'] = from_time
            if to_time:
                filters['created_at']['$lte'] = to_time

        cursor = self.collection.find(filters)
        return await cursor.to_list(length=None)
