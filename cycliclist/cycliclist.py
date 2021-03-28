from typing import Iterable


class CyclicList:
    _elements: list

    def __init__(self, lst: Iterable):
        self._elements = list(lst)
        self._pos = 0

    def __iter__(self):
        """Return a copy of ourself as an iterator"""
        return CyclicList(self._elements)

    def __next__(self):
        result = self._elements[self._pos]
        self._pos = self._contain_key((self._pos + 1))
        return result

    def __len__(self):
        return len(self._elements)

    def __getitem__(self, item):
        if isinstance(item, slice):
            step = item.step or 1
            start = item.start or 0
            stop = item.stop or (self.__len__() if start >= 0 else 0)
            t = [self._elements[self._contain_key(e)] for e in range(start, stop, step)]
            return t
        else:
            return self._elements[self._contain_key(item)]

    def __setitem__(self, key, value):
        self._elements[self._contain_key(key)] = value

    def _contain_key(self, key):
        """Ensure that the index key is within the actual range of the _elements array"""
        return key % len(self._elements)

    def append(self, element):
        self._elements.append(element)

    def pop(self, index=None):
        if index is None:
            index = self.__len__() - 1
        return self._elements.pop(index)
