from typing import Deque, Iterable, NamedTuple


class LoopHelper(NamedTuple):
    index: int = 0
    previous: object = None
    current: object = None
    next: object = None
    is_first: bool = False
    is_last: bool = False


def loop_helper(it: Iterable, previous_default=None):
    def make_yield_return(index: int, items: Deque, is_first: bool,
                          is_last: bool):
        info = LoopHelper(index=index,
                          previous=items[0],
                          current=items[1],
                          next=items[2],
                          is_first=is_first,
                          is_last=is_last)
        return items[1], info

    items = Deque([previous_default], maxlen=3)
    for n, item in enumerate(it):
        items.append(item)
        if len(items) == 3:
            yield make_yield_return(n - 1, items, n == 1, False)
    if len(items) > 1:
        items.append(None)
        yield make_yield_return(n, items, n == 0, True)
