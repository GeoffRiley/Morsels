from datetime import date
from dateutil.relativedelta import relativedelta


class Month(object):
    __slots__ = ['_year', '_month']

    def __init__(self, year: int, month: int):
        self._year = year
        self._month = month

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._month

    @property
    def first_day(self):
        return date(year=self.year, month=self.month, day=1)

    @property
    def last_day(self):
        fst = self.first_day
        return fst + relativedelta(day=31)

    @classmethod
    def from_date(cls, dt: date):
        return cls(dt.year, dt.month)

    def strftime(self,fmt):
        return self.first_day.strftime(fmt)

    def __str__(self):
        return f'{self.year}-{self.month:02}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.year}, {self.month})'

    def __eq__(self, other):
        if isinstance(other, Month):
            return self.month == other.month and self.year == other.year
        return False

    def __gt__(self, other):
        if isinstance(other, Month):
            return self.year > other.year or (self.year == other.year and self.month > other.month)
        raise NotImplemented

    def __ge__(self, other):
        if isinstance(other, Month):
            return self.year >= other.year or (self.year == other.year and self.month >= other.month)
        raise NotImplemented

    def __hash__(self):
        return hash((self._year,self._month))
