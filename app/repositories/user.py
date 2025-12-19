from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import Users

from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Users

        super().__init__(db=self.db, model=self.model)
