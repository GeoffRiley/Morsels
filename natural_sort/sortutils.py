from typing import List
import re
from functools import singledispatch

PICKNUMBER = re.compile(r'(\d+)')


@singledispatch
def natural_key(x: str) -> list:
    matches = PICKNUMBER.split(x)
    return [
        int(match) if match.isdigit() else match.casefold()
        for match in matches
    ]


def natural_sort(strings: List[str],
                 reverse: bool = False,
                 key: callable = None) -> List[str]:
    if key is None:
        key = natural_key
    return sorted(strings, key=key, reverse=reverse)
