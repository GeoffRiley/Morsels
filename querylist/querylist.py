import operator
from collections import UserList
from dataclasses import dataclass
from typing import Any

OPERATIONS = {
    "eq": operator.eq,
    "ne": operator.ne,
    "lt": operator.lt,
    "gt": operator.gt,
    "le": operator.le,
    "ge": operator.ge,
    "contains": operator.contains,
    "in": lambda x, y: operator.contains(y, x),
}


class QueryList(UserList):
    def filter(self, *callable_queries, **kwarg_queries):
        queries = [
            *callable_queries,
            *filters_from_kwargs(kwarg_queries),
        ]
        return QueryList(obj for obj in self.data if all(
            f(obj) for f in queries))

    def attrs(self, *names):
        getter = operator.attrgetter(*names)
        return [getter(obj) for obj in self.data]


def filters_from_kwargs(queries):
    for query, value in queries.items():
        name, __, suffix = query.partition("__")
        if __ != "__":
            suffix = "eq"
        yield Filter(name, suffix, value)


class Field:
    def __getattr__(self, name):
        return Lookup(name)


F = Field()


@dataclass
class Lookup:
    name: str

    def make_matcher(self, op, value):
        return Filter(self.name, op, value)

    def __eq__(self, value):
        return self.make_matcher("eq", value)

    def __ne__(self, value):
        return self.make_matcher("ne", value)

    def __lt__(self, value):
        return self.make_matcher("lt", value)

    def __gt__(self, value):
        return self.make_matcher("gt", value)

    def __le__(self, value):
        return self.make_matcher("le", value)

    def __ge__(self, value):
        return self.make_matcher("ge", value)


@dataclass
class Filter:
    name: str
    op: str
    value: Any

    def __call__(self, obj):
        return OPERATIONS[self.op](getattr(obj, self.name), self.value)

    def __or__(self, other):
        return Joiner(any, self, other)

    def __and__(self, other):
        return Joiner(all, self, other)


class Joiner:
    def __init__(self, joiner, *filters):
        self.joiner = joiner
        self.filters = filters

    def __call__(self, obj):
        return self.joiner(f(obj) for f in self.filters)

    def __or__(self, other):
        if self.joiner == any:
            return Joiner(any, *self.filters, other)
        return Joiner(any, self, other)

    def __and__(self, other):
        if self.joiner == all:
            return Joiner(all, *self.filters, other)
        return Joiner(all, self, other)
