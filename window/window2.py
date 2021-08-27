from typing import List


def window(lst: list, n: int, *, fillvalue=None) -> List[tuple]:
    if not n:
        return []
    res = []
    c = 0
    for item in lst:
        c += 1
        res.append(item)
        if len(res) == n:
            yield tuple(res)
            res.pop(0)
    if c < n:
        res.extend([fillvalue] * (n - len(res)))
        yield tuple(res)
