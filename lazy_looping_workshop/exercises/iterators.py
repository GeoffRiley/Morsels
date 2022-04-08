"""Iterator exercises"""

from random import randint


def first(it):
    """Return the first item in given iterable."""
    return next(iter(it))


def is_iterator(it):
    """Return True if given iterable is an iterator."""
    i = iter(it)
    return i is it


class Point:
    """3-D Point objects"""
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


SEMAPHORE = object()


def all_same(it):
    """Return True if all items in the given iterable are the same."""
    i = iter(it)
    n = next(i, SEMAPHORE)
    if n is SEMAPHORE:
        return True
    return all(b == n for b in i)


def minmax(it):
    """Return minimum and maximum values from given iterable."""
    i = iter(it)
    mn = mx = next(i, SEMAPHORE)
    if mn is SEMAPHORE:
        raise ValueError
    for v in i:
        mn = min(mn, v)
        mx = max(mx, v)
    return mn, mx


class RandomNumberGenerator:
    """Return infinite series of randomly generator numbers."""
    def __init__(self, low, high) -> None:
        self.low = low
        self.high = high

    def __iter__(self):
        return self

    def __next__(self):
        return randint(self.low, self.high)
