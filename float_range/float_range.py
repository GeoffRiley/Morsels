from math import ceil


class float_range(object):
    def __init__(self, *args):
        if len(args) == 3:
            self._start = args[0]
            self._end = args[1]
            self._inc = args[2]
        elif len(args) == 2:
            self._start = args[0]
            self._end = args[1]
            self._inc = 1.0
        elif len(args) == 1:
            self._start = 0.0
            self._end = args[0]
            self._inc = 1.0
        else:
            raise TypeError('Improper arguments provided to class')
        self._current = self._start

    def __next__(self):
        ret = self._current
        if ((self._inc > 0 and float(self._current) < float(self._end)) or
                (self._inc < 0 and float(self._current) > float(self._end))):
            self._current += self._inc
            return ret
        raise StopIteration

    def __iter__(self):
        self._current = self._start
        return self

    def __len__(self):
        if self._inc < 0:
            ret = ceil((self._current - self._end) / -self._inc)
        else:
            ret = ceil((self._end - self._current) / self._inc)
        return ret if ret > 0 else 0

    def __reversed__(self):
        return float_range(self._start + self._inc * (self.__len__() - 1), self._start - self._inc, -self._inc)

    def __eq__(self, other):
        if type(other) == type(self):
            return (self.__len__() == other.__len__() and (
                    self.__len__() == 0 or
                    (self.__len__() == 1 and self._start == other._start) or
                    (self._start == other._start and self._inc == other._inc)))
        elif isinstance(other, range):
            return (self.__len__() == other.__len__() and (
                    self.__len__() == 0 or
                    (float(self._start) == float(other.start) and
                     float(self._inc) == float(other.step))))
        return other == self

    def __repr__(self):
        return f'{self.__class__.__name__}({self._start}, {self._end}, {self._inc})'
