from typing import Any


class SortedList:
    def __init__(self, values) -> None:
        self.values = set(values)

    def __repr__(self) -> str:
        params = ', '.join(str(x) for x in self.values)
        return f'{self.__class__.__name__}([{params}])'

    def __iter__(self):
        yield from self.values

    def __len__(self) -> int:
        return len(self.values)

    def __getitem__(self, ndx: int) -> Any:
        if ndx < 0:
            ndx += self.__len__()
        for n, x in enumerate(self):
            if n == ndx:
                return x
        raise IndexError

    def add(self, new_item: Any):
        self.values.add(new_item)

    def remove(self, old_item: Any):
        if old_item not in self.values:
            raise ValueError
        self.values.remove(old_item)

    def index(self, value: int, *, start: int = None, stop: int = None) -> Any:
        rng = range(start or 0, stop or self.__len__())
        for n, x in enumerate(self):
            if n in rng and x == value:
                return n
        raise ValueError

    def find(self, string: str) -> int:
        pass
