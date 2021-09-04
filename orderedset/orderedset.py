from typing import Any


class OrderedSet:
    def __init__(self, it: iter = None) -> None:
        items = []
        item_set = set()
        if it is not None:
            for item in it:
                if item not in item_set:
                    items.append(item)
                    item_set.add(item)

        self._data = items
        self._data_set = item_set

    def __iter__(self):
        yield from self._data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._data!r})"

    def __contains__(self, item: Any):
        return item in self._data_set

    def __len__(self) -> int:
        return len(self._data)

    def __eq__(self, o: object) -> bool:
        if isinstance(o, OrderedSet):
            return len(self._data) == len(o._data) and all(
                x == y for x, y in zip(self._data, o._data))
        elif isinstance(o, set):
            return self._data_set == o
        else:
            return NotImplemented

    def add(self, item: Any):
        if item not in self._data_set:
            self._data.append(item)
            self._data_set.add(item)

    def discard(self, item: Any):
        if item in self._data_set:
            self._data.remove(item)
            self._data_set.remove(item)
