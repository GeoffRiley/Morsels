from collections import UserList
from operator import attrgetter


class QueryList(UserList):
    def __init__(self, a_list: list) -> None:
        super().__init__(a_list)
        self.current_filter = None
        self.filter_vals = ()
        self._pos = 0

    def filter(self, **kwargs):
        names = []
        self.filter_vals = []
        for key, value in kwargs.items():
            a, _, b = key.partition('__')
            names.append(a)
            self.filter_vals.append(value)
        self.current_filter = attrgetter(*names) if len(kwargs) else None
        if len(self.filter_vals) == 1:
            self.filter_vals = self.filter_vals[0]
        return iter(self)

    def __iter__(self):
        self._pos = 0
        return self

    def __next__(self):
        while True:
            if self._pos >= len(self.data):
                raise StopIteration
            rec = self.data[self._pos]
            self._pos += 1
            if self.current_filter and self.current_filter(
                    rec) != self.filter_vals:
                continue
            return rec

    def attrs(self, *args):
        doit = attrgetter(*args)
        result = [doit(rec) for rec in iter(self)]
        return result if len(result) != 1 else result[0]
