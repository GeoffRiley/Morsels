import types
from typing import Iterable


def deep_flatten(lst):
    return flatten(lst)


def flatten(lst):
    if type(lst) != str and isinstance(lst, Iterable):
        for l in lst:
            if type(l) != str and isinstance(l, Iterable):
                for m in flatten(l):
                    yield m
            else:
                yield l
    else:
        yield lst
