from zoneinfo import ZoneInfo
from datetime import datetime, timedelta, time


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
        get_naive: bool = True,
    ):
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        dt = datetime.now(tz=tz) + delta

        dt = dt.replace(tzinfo=None)
        return dt.isoformat() if in_iso_format else dt

    @classmethod
    def end_of_today(
        cls,
        tz: ZoneInfo = ZoneInfo("UTC"),
        in_iso_format: bool = False,
    ):
        now = datetime.now(tz)
        end_of_day = datetime.combine(
            now.date(),
            time(23, 59, 59),
            tzinfo=tz,
        )
        end_of_day = end_of_day.replace(tzinfo=None)
        return end_of_day.isoformat() if in_iso_format else end_of_day
