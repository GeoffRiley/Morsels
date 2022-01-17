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


class NextDate:
    def __init__(self, day: Weekday, after_today: bool = False) -> None:
        self.target = day
        self.after_today = after_today

    def days_until(self) -> int:
        dow = date.today().weekday()
        if self.after_today and self.target == dow:
            return 7
        return (self.target - dow) % 7

    def date(self) -> date:
        return date.today() + timedelta(days=self.days_until())

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}' \
               f'({self.target!r}, after_today={self.after_today!r})'


def next_date(day: Weekday, *, after_today: bool = False) -> date:
    d = NextDate(day, after_today)
    return d.date()


def days_until(day: Weekday, *, after_today: bool = False) -> int:
    d = NextDate(day, after_today)
    return d.days_until()


def next_tuesday(after_today: bool = False) -> date:
    return next_date(Weekday.TUESDAY, after_today=after_today)


def days_to_tuesday(after_today: bool = False) -> int:
    return days_until(Weekday.TUESDAY, after_today=after_today)
