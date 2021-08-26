from typing import List


def window(l: list, n: int, *, fillvalue=None) -> List[tuple]:
    if not n:
        return []
    result = []
    res = []
    c = 0
    for item in l:
        c += 1
        res.append(item)
        if len(res) == n:
            # result.append(tuple(res))
            yield tuple(res)
            res.pop(0)
    if c < n:
        res.extend([fillvalue] * (n - len(res)))
        yield tuple(res)
