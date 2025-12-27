from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pricing import Pricing

from app.repositories.base_repository import BaseRepository


class PricingRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.model = Pricing

        super().__init__(db=self.db, model=self.model)
