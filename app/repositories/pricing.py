from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.document import DocumentRepository


class PricingRepository(DocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = 'prices'

        super().__init__(db=db, collection_name=self.collection_name)
