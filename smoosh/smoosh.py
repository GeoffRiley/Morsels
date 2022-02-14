from functools import partial
from typing import Any, Iterable

__all__ = [f'smoo{"o"*i}sh' for i in range(9)]


def isiterable(it):
    return isinstance(it, Iterable) and not isinstance(it, str)


def smoosh(it, *, level=1):
    if level < 0 or not (isiterable(it)):
        yield it
    else:
        for i in it:
            yield from smoosh(i, level=level - 1)


def __getattr__(name: str) -> Any:
    if name.startswith('sm') and name.endswith('sh'):
        ohs = name[2:-2]
        if set(ohs) == {'o'}:
            depth = len(ohs) - 1
            return partial(smoosh, level=depth)
    raise AttributeError(f"module {__name__} has no attribute {name}")


def __dir__():
    return sorted(__all__)
