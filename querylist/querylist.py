import operator
from collections import UserList
from operator import attrgetter


def field_in(a, b):
    return a in b


FILTER_FUNCTIONS = {
    '': operator.eq,
    'gt': operator.gt,
    'lt': operator.lt,
    'ne': operator.ne,
    'in': field_in,
    'contains': operator.contains
}


class QueryList(UserList):
    def __init__(self, a_list: list) -> None:
        super().__init__(a_list)
        self.current_filter = None
        self.filters = ()
        self._pos = 0

    def filter(self, **kwargs):
        names = {}
        self.filters = []
        for key, value in kwargs.items():
            attr_name, _, func = key.partition('__')
            names[attr_name] = value
            self.filters.append((value, FILTER_FUNCTIONS[func]))
        self.current_filter = attrgetter(*names.keys()) if len(names) else None
        self.filters = tuple(
            self.filters) if len(self.filters) != 1 else self.filters[0]
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
            if self.current_filter:
                rec2 = self.current_filter(rec)
                if not self._check_record_match(rec2):
                    continue
            return rec

    def _check_record_match(self, match_record):
        return all(
            func(param1, param2)
            for param1, param2, func in zip(match_record, *zip(
                *self.filters))) if isinstance(
                    match_record, tuple) else self.filters[1](match_record,
                                                              self.filters[0])

    def attrs(self, *args):
        doit = attrgetter(*args)
        result = [doit(rec) for rec in iter(self)]
        return result if len(result) != 1 else result[0]
