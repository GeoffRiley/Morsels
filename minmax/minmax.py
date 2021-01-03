from typing import Tuple, Iterable, Any, Callable, NamedTuple


class Minmax(NamedTuple):
    min: Any
    max: Any


def minmax(lst: Iterable[Any], *, key: Callable = None) -> Tuple[Any, Any]:
    lst = list(lst)
    return Minmax(min(lst, key=key), max(lst, key=key))
