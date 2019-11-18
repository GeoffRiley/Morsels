from datetime import date, timedelta
from enum import IntEnum


class Weekday(IntEnum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def meetup_date(year, month, nth=4, weekday=Weekday.THURSDAY):
    if nth < 0:
        nth += 1
        start = date(year, month + 1, 1) - timedelta(days=1)
        offset = -((7 - weekday + start.weekday()) % 7)
    else:
        nth -= 1
        start = date(year, month, 1)
        offset = (7 - start.weekday() + weekday) % 7
    start += timedelta(days=offset)
    start += timedelta(weeks=nth)
    return start
