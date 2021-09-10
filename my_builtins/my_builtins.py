from itertools import count
from sys import stdout
from typing import Iterator

SEMAPHORE = object()


def len(obj) -> int:
    if callable(getattr(obj, '__len__', None)):
        return obj.__len__()
    raise TypeError(f"object of type '{obj.__class__.__name__}' has no len()")


def sum(obj, start: float = 0) -> float:
    if isinstance(start, str):
        raise TypeError("sum() can't sum strings [ use ''.join(seq) instead")
    for i in obj:
        if isinstance(i, str):
            raise TypeError(
                "sum() can't sum strings [ use ''.join(seq) instead")
        else:
            start += i
    return start


def all(obj) -> bool:
    for i in obj:
        if not i:
            return False
    return True


def enumerate(obj, start: int = 0):
    c = count(start)
    yield from zip(c, obj)


def print(*args, **kwargs) -> None:
    sep = kwargs.get('sep', ' ')
    if sep is None:
        sep = ' '
    if not isinstance(sep, str):
        raise TypeError('sep must be a string')
    end = kwargs.get('end', '\n')
    if end is None:
        end = '\n'
    if not isinstance(end, str):
        raise TypeError('end must be a string')
    file = kwargs.get('file', stdout)

    file.write(sep.join(str(arg) for arg in args))

    if end:
        file.write(end)

    if kwargs.get('flush', False):
        file.flush()


def next(obj: iter, default=SEMAPHORE):
    if not isinstance(obj, Iterator):
        raise TypeError('next operated on iterables')
    try:
        res = obj.__next__()
    except StopIteration:
        if default is not SEMAPHORE:
            res = default
        else:
            raise
    return res
