from random import shuffle
from typing import Any


class RandomLooper:
    def __init__(self, *elements) -> None:
        self.items = [e for elem in elements for e in elem]

    def __iter__(self) -> Any:
        items = self.items.copy()
        if len(items) > 1:
            shuffle(items)
        yield from items

    def __len__(self) -> int:
        return len(self.items)
