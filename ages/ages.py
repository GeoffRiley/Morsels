from datetime import date
from fractions import Fraction


def is_over(target: int, birthdate: str) -> bool:
    return get_age(birthdate) >= target


def get_age(birthdate_s: str, exact: bool = False) -> int:
    birthdate = date.fromisoformat(birthdate_s)
    currentdate = date.today()
    age = currentdate.year - birthdate.year - (0 if later_in_year(
        birthdate, currentdate) else 1)

    if exact:
        age += year_fraction(birthdate, currentdate, age)

    return age


def year_fraction(birthdate, currentdate, age):
    birthday = date(birthdate.year + age, birthdate.month, birthdate.day)
    next_birthday = date(birthday.year + 1, birthday.month, birthday.day)
    if ((is_leapyear(birthday)
         and later_in_year(date(birthday.year, 2, 29), birthday)) or
        (is_leapyear(next_birthday)
         and later_in_year(date(next_birthday.year, 3, 1), next_birthday))):
        divisor = 366
    else:
        divisor = 365

    days_after_birthday = (currentdate - birthday).days
    return Fraction(days_after_birthday, divisor)


def later_in_year(date1: date, date2: date) -> bool:
    return (date1.month, date1.day) <= (date2.month, date2.day)


def is_leapyear(dt: date) -> bool:
    return dt.year % 4 == 0 and (dt.year % 100 != 0 or dt.year % 400 == 0)
