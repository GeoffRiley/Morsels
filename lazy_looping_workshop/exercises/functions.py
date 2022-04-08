"""Generator Function Exercises."""

from itertools import count, filterfalse, islice, takewhile, zip_longest
from typing import Iterable, Union

SEMAPHORE = object()


def unique(it):
    """Yield iterable elements in order, skipping duplicate values."""
    seen = set()
    for i in it:
        if i not in seen:
            yield i
            seen.add(i)


def float_range(start: float,
                stop: Union[object, float] = SEMAPHORE,
                step: int = 1):
    """Return iterable of numbers from start to stop by step."""
    if stop is SEMAPHORE:
        start, stop = 0, start
    now = start
    while now < stop:  # type: ignore
        yield now
        now += step


def head(it, n):
    """Return first n items of a given iterable."""
    yield from islice(it, n)


def pairwise(it):
    """
    Yield a tuple containing each item and the item following it.

    The item after the last one is treated as ``None``.
    """
    yield from zip_longest(it, it[1:])


def around(it):
    """
    Yield a tuple of the previous, current, and next items.

    The previous item should start at ``None`` and the next item should
    be ``None`` for the last item in the iterable.
    """
    itr = iter(it)
    prv, crr = None, next(itr, SEMAPHORE)
    if crr is not SEMAPHORE:
        for nxt in itr:
            if crr is not SEMAPHORE:
                yield prv, crr, nxt
            prv, crr = crr, nxt
    if crr is not SEMAPHORE:
        yield prv, crr, None


def stop_on(it, n):
    """Yield from the iterable until the given value is reached."""
    yield from takewhile(lambda x: x != n, it)


def deep_flatten(matrix):
    """Flatten an iterable of iterables."""
    if isinstance(matrix, Iterable):
        for mat in matrix:
            if isinstance(mat, Iterable):
                yield from deep_flatten(mat)
            else:
                yield mat
    else:
        yield matrix


def get_primes_over(n):
    """Return given number of primes over 1,000,000."""
    def is_not_prime(candidate):
        """Return True if candidate number is prime."""
        return any(candidate % n == 0 for n in range(2, candidate))

    counter = count(1_000_000)
    yield from islice(filterfalse(is_not_prime, counter), n)
