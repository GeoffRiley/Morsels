from collections import UserList
from heapq import heapify, heappop, heappush
from typing import Callable, Iterable


class MaxHeapObj(object):
    """Inverted comparison object

    This allows the standard `heapq` module to sort in reverse.
    """
    def __init__(self, val):
        self.val = val

    def __lt__(self, other):
        return self.val > other.val

    def __eq__(self, other):
        return self.val == other.val

    def __repr__(self):
        return str(self.val)


class MinHeap(UserList):
    def __init__(self, it: Iterable, *, key: Callable = None) -> None:
        self._key_fn = key if key is not None else lambda x: x
        self.data = [(self.key(v), v) for v in it]
        heapify(self.data)

    def push(self, value):
        heappush(self.data, (self.key(value), value))

    def pop(self):
        return heappop(self.data)[1]

    def peek(self):
        return self.data[0][1]

    def key(self, value):
        return self._key_fn(value)


class MaxHeap(MinHeap):
    def key(self, value):
        return MaxHeapObj(super().key(value))
