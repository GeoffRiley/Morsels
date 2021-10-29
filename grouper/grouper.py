from typing import Any, Callable, Iterable
from collections import UserDict, defaultdict


class Grouper(UserDict):
    def __init__(self, it: Iterable = None, key: Callable = None) -> None:
        keyfunc = key if key is not None else self.passthru
        self.data = defaultdict(list)
        self.keyfunc = keyfunc
        self.update(it)

    def passthru(self, x):
        return x

    def update(self, it: Iterable) -> 'Grouper':
        if it is not None:
            if isinstance(it, dict):
                for k, v in it.items():
                    self.data[k].extend(v)
            else:
                for s in iter(it):
                    self.data[self.keyfunc(s)].append(s)
        return self

    def add(self, value: Any) -> 'Grouper':
        self.data[self.keyfunc(value)].append(value)
        return self

    def group_for(self, value: Any) -> Any:
        return self.keyfunc(value)

    def __add__(self, other) -> 'Grouper':
        if not isinstance(other, Grouper):
            return NotImplemented
        if self.keyfunc != other.keyfunc:
            raise ValueError('Key functions differ')
        return Grouper(self.data, self.keyfunc).update(other.data)
