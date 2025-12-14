from typing import List, Dict, Optional

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.enums.pricing import PricingTypeEnum

from app.exceptions.general import NotFoundException

from app.repositories.pricing import PricingRepository
from app.utils.datetime_utils import DatetimeUtils


class PricingService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.repository = PricingRepository(db=db)

    async def get_prices(self, pricing_type: Optional[PricingTypeEnum] = None) -> List[Dict]:
        cr = self.repository.find()
        if pricing_type:
            cr = self.repository.find(type=pricing_type)

        return await cr

    async def change_price(self, new_price: float, pricing_type: PricingTypeEnum):
        updated_price = await self.repository.find_one_and_update(
            filters={'type': pricing_type},
            updates={'price': new_price},
        )

        if not updated_price:
            raise NotFoundException('Price')

        return updated_price

    async def determine_visit_end_time(self, start_time: datetime, payment_amount: float):
        hourly_price = (await self.get_prices(pricing_type=PricingTypeEnum.HOURLY))[0]['price']

        total_hours = payment_amount / hourly_price
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        seconds = int(((total_hours - hours) * 60 - minutes) * 60)

        return DatetimeUtils.get_datetime(hours=hours, minutes=minutes, seconds=seconds)
