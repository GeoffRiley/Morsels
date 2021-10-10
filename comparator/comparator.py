from numbers import Number
from contextlib import contextmanager


class Comparator:
    _default_delta: float = 0.0000001

    def __init__(self, value, delta: float = None) -> None:
        self.value = value
        self.delta = delta or Comparator._default_delta

    @property
    def _hi(self):
        return self.value + self.delta

    @property
    def _lo(self):
        return self.value - self.delta

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Number):
            return self._lo <= o <= self._hi
        elif isinstance(o, Comparator):
            return self._lo <= o._lo <= self._hi or self._lo <= o._hi <= self._hi
        return NotImplemented

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.value}, delta={self.delta})'

    def __add__(self, o: object) -> 'Comparator':
        if isinstance(o, Number):
            return Comparator(self.value + o, delta=self.delta)
        elif isinstance(o, Comparator):
            return Comparator(self.value + o.value,
                              delta=max(self.delta, o.delta))
        return NotImplemented

    __radd__ = __add__

    def __sub__(self, o: object) -> 'Comparator':
        if isinstance(o, Number):
            return Comparator(self.value - o, delta=self.delta)
        elif isinstance(o, Comparator):
            return Comparator(self.value - o.value,
                              delta=max(self.delta, o.delta))
        return NotImplemented

    def __rsub__(self, o: object) -> 'Comparator':
        if isinstance(o, Number):
            return Comparator(o - self.value, delta=self.delta)
        elif isinstance(o, Comparator):
            return Comparator(o.value - self.value,
                              delta=max(self.delta, o.delta))
        return NotImplemented

    @classmethod
    @contextmanager
    def default_delta(cls, delta: float):
        original_delta = cls._default_delta
        try:
            cls._default_delta = delta
            yield
        finally:
            cls._default_delta = original_delta
