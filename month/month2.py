from dataclasses import dataclass
from datetime import date
from typing import Union


@dataclass(order=True)
class Month:
    year: int
    month: int

    def __add__(self, other) -> 'Month':
        if isinstance(other, MonthDelta):
            x, m = divmod(self.month + other.months, 12)
            if m == 0:
                x, m = x - 1, 12
            y = self.year + x
            return Month(y, m or 12)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other) -> 'Month':
        if isinstance(other, MonthDelta):
            x, m = divmod(self.month - other.months, 12)
            if m == 0:
                x, m = x - 1, 12
            y = self.year + x
            return Month(y, m)
        elif isinstance(other, Month):
            y = self.year - other.year
            m = self.month - other.month
            return MonthDelta(y * 12 + m)
        return NotImplemented

    @property
    def _start_of_month(self) -> date:
        return date(year=self.year, month=self.month, day=1)

    def __format__(self, format_spec: str) -> str:
        return self._start_of_month.strftime(format_spec)


@dataclass
class MonthDelta:
    months: int

    def __add__(self, other) -> 'MonthDelta':
        if isinstance(other, MonthDelta):
            return MonthDelta(self.months + other.months)
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, other) -> 'MonthDelta':
        if isinstance(other, MonthDelta):
            return MonthDelta(self.months - other.months)
        return NotImplemented

    def __mul__(self, other) -> 'MonthDelta':
        if isinstance(other, int):
            return MonthDelta(self.months * other)
        return NotImplemented

    __rmul__ = __mul__

    def __truediv__(self, other) -> float:
        if isinstance(other, MonthDelta):
            return self.months / other.months
        return NotImplemented

    def __floordiv__(self, other) -> Union['MonthDelta', int]:
        if isinstance(other, int):
            return MonthDelta(self.months // other)
        elif isinstance(other, MonthDelta):
            return self.months // other.months
        return NotImplemented

    def __mod__(self, other) -> Union['MonthDelta', int]:
        if isinstance(other, int):
            return MonthDelta(self.months % other)
        elif isinstance(other, MonthDelta):
            return self.months % other.months
        return NotImplemented

    def __neg__(self) -> 'MonthDelta':
        return MonthDelta(-self.months)
