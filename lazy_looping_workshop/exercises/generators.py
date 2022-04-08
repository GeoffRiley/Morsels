"""Generator Expression Exercises."""

from itertools import chain, zip_longest
from typing import Iterable

SEMAPHORE = object()


def sum_all(matrix):
    """Return the sum of all numbers in the given list-of-lists."""
    return sum(item for row in matrix for item in row)


def all_together(*matrix):
    """String together all items from the given iterables."""
    return chain(*matrix)


def interleave(it1, it2):
    """Return iterable of one item at a time from each list."""
    yield from (x for pair in zip_longest(it1, it2, fillvalue=SEMAPHORE)
                for x in pair if x is not SEMAPHORE)


def deep_add(matrix):
    """Return sum of values in given iterable, iterating deeply."""
    if isinstance(matrix, Iterable):
        return sum(deep_add(mat) for mat in matrix)
    return matrix


def parse_ranges(range_str: str):
    """Return a list of numbers corresponding to number ranges in a string"""
    for r in range_str.split(','):
        a, b = map(int, r.strip().split('-'))
        yield from range(a, b + 1)


def is_prime(candidate):
    """Return True if candidate number is prime."""
    return all(candidate % n != 0 for n in range(2, candidate // 2))
