import operator
from collections import UserList
from operator import attrgetter
from typing import Any, Tuple


def field_in(x, y):
    return x in y


FILTER_FUNCTIONS = {
    '': operator.eq,
    'eq': operator.eq,
    'gt': operator.gt,
    'lt': operator.lt,
    'ne': operator.ne,
    'in': field_in,
    'contains': operator.contains
}


def _check_record_match(match_record, filters):
    return all(
        func(getattr(match_record, field_name), target_value)
        for field_name, target_value, func in filters)


class QueryList(UserList):
    def filter(self, *args, **kwargs):
        filters = []
        # Since there can be multiple instances of, say, 'color != ...' these cannnot
        # go into a dictionary… the alternative is to have everything in a list of tuples
        queries = [*args, *kwargs.items()]
        for key, value in queries:
            attr_name, _, func = key.partition('__')
            filters.append((attr_name, value, FILTER_FUNCTIONS[func]))

        return QueryList(entry for entry in self.data
                         if _check_record_match(entry, filters))

    def attrs(self, *args):
        doit = attrgetter(*args)
        return [doit(rec) for rec in iter(self)]


class Lookup:
    def __init__(self, name: str) -> None:
        self.name = name

    def make_query(self, op, __o: object) -> Tuple[str, Any]:
        return (f"{self.name}__{op}", __o)

    def __eq__(self, __o: object) -> Tuple[str, Any]:
        return self.make_query('eq', __o)

    def __ne__(self, __o: object) -> Tuple[str, Any]:
        return self.make_query('ne', __o)

    def __lt__(self, __o: object) -> Tuple[str, Any]:
        return self.make_query('lt', __o)

    def __gt__(self, __o: object) -> Tuple[str, Any]:
        return self.make_query('gt', __o)

    def __le__(self, __o: object) -> Tuple[str, Any]:
        return self.make_query('le', __o)

    def __ge__(self, __o: object) -> Tuple[str, Any]:
        return self.make_query('ge', __o)


class Field:
    def __getattr__(self, name: str):
        return Lookup(name)


F = Field()
