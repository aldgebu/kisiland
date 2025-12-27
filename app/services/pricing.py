from typing import List, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.pricing import Pricing

from app.enums.pricing import PricingTypeEnum

from app.utils.datetime_utils import DatetimeUtils

from app.repositories.pricing import PricingRepository



class PricingService:
    def __init__(self, db: AsyncSession):
        self.model = Pricing
        self.repository = PricingRepository(db=db)

    async def get_prices(self, pricing_type: Optional[PricingTypeEnum] = None) -> List[Pricing]:
        cr = self.repository.find()
        if pricing_type:
            cr = self.repository.find(type=pricing_type)

        return await cr

    async def change_price(self, new_price: float, pricing_type: PricingTypeEnum):
        price = await self.repository.find(type=pricing_type, get_first=True)
        if not price:
            price = self.model(price=new_price, type=pricing_type)
        else:
            price.price = new_price

        await self.repository.save_to_db(price, commit=True)
        return price

    async def determine_visit_end_time(self, payment_amount: float):
        hourly_price = (await self.get_prices(pricing_type=PricingTypeEnum.HOURLY))[0].price

        total_hours = payment_amount / hourly_price
        hours = int(total_hours)
        minutes = int((total_hours - hours) * 60)
        seconds = int(((total_hours - hours) * 60 - minutes) * 60)

        return DatetimeUtils.get_datetime(hours=hours, minutes=minutes, seconds=seconds)
