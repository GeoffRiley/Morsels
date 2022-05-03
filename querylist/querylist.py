import operator
from collections import UserList
from operator import attrgetter
from typing import Callable, Optional


def field_in(a, b):
    return a in b


def field_contains(a, b):
    return b in a


FILTER_FUNCTIONS = {
    '': operator.eq,
    'gt': operator.gt,
    'lt': operator.lt,
    'ne': operator.ne,
    'in': field_in,
    'contains': field_contains
}


class QueryList(UserList):
    def __init__(self, a_list: list) -> None:
        super().__init__(a_list)
        self.current_filter = None
        self.filter_vals = ()
        self.filter_funcs = ()
        self._pos = 0

    def filter(self, **kwargs):
        names = {}
        self.filter_vals = []
        self.filter_funcs = []
        for key, value in kwargs.items():
            attr_name, _, func = key.partition('__')
            names[attr_name] = value
            self.filter_vals.append(value)
            self.filter_funcs.append(FILTER_FUNCTIONS[func])
        self.current_filter = attrgetter(*names.keys()) if len(names) else None
        if len(self.filter_vals) == 1:
            self.filter_vals = self.filter_vals[0]
            self.filter_funcs = self.filter_funcs[0]
        else:
            self.filter_vals = tuple(self.filter_vals)
            self.filter_funcs = tuple(self.filter_funcs)
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
                # if isinstance(rec2, tuple):
                if not self._check_record_match(rec2):
                    continue
                # else:
                #     if not self.filter_funcs(rec2, self.filter_vals):
                #         continue
            return rec

    def _check_record_match(self, match_record):
        if not isinstance(match_record, tuple):
            return self.filter_funcs(match_record, self.filter_vals)
        return all(
            func(param1, param2) for param1, func, param2 in zip(
                match_record, self.filter_funcs, self.filter_vals))

    def attrs(self, *args):
        doit = attrgetter(*args)
        result = [doit(rec) for rec in iter(self)]
        return result if len(result) != 1 else result[0]
