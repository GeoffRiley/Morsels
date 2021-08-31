from typing import Any, Callable, NamedTuple

SEMAPHORE = object()


class MinMax(NamedTuple):
    min: Any
    max: Any


def minmax(*args, key: Callable = None, default: Any = SEMAPHORE) -> MinMax:
    # check the number of positional arguments and adjust the working
    # 'lst' as appropriate
    if len(args) == 1:
        lst = list(args[0])
    elif len(args) > 1:
        lst = args
    elif default is not SEMAPHORE:
        return MinMax(min=default, max=default)
    else:
        raise TypeError('Empty lists have no max nor min')

    if default is not SEMAPHORE:
        mn = min(lst, key=key, default=default)
        mx = max(lst, key=key, default=default)
    else:
        mn = min(lst, key=key)
        mx = max(lst, key=key)

    return MinMax(min=mn, max=mx)
