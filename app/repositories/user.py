from motor.motor_asyncio import AsyncIOMotorDatabase

from app.repositories.document import DocumentRepository


class UserRepository(DocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection_name = 'users'

        super().__init__(db=self.db, collection_name=self.collection_name)
