from zoneinfo import ZoneInfo
from datetime import datetime, timedelta


class DatetimeUtils:
    @classmethod
    def get_datetime(
        cls,
        days: int = 0,
        hours: int = 0,
        minutes: int = 0,
        seconds: int = 0,
        tz: ZoneInfo = ZoneInfo('UTC'),
        in_iso_format: bool = False,
    ):
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        dt = datetime.now(tz=tz) + delta

        return dt.isoformat() if in_iso_format else dt
