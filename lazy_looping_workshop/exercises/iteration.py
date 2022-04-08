"""Itertools exercises"""

from itertools import chain, dropwhile


def total_length(*matrix):
    """Return the total number of items in all given iterables."""
    return len(list(chain(*matrix)))


def lstrip(it, ch):
    """Return iterable with strip_value items removed from beginning."""
    return dropwhile(lambda x: x == ch, it)
