from collections import UserString


class MutableString(UserString, str):
    def _parts_(self, index):
        if isinstance(index, slice):
            start, stop, _ = index.indices(len(self))
        else:
            if index < 0:
                index = len(self) + index
            start, stop, _ = index, index + 1, None
        b4 = self[:start] if start > 0 else ''
        subj = self[start:stop]
        aft = self[stop:] if stop < len(self) else ''
        return b4, subj, aft

    def __setitem__(self, index, val):
        b4, _, aft = self._parts_(index)
        self.data = b4 + val + aft

    def __delitem__(self, index):
        self[index] = ''

    def __eq__(self, o: object) -> bool:
        if isinstance(o, MutableString):
            return self.data == o.data
        elif isinstance(o, str):
            return self.data == o
        return NotImplemented

    def __ne__(self, o: object) -> bool:
        res = self.__eq__(o)
        return res if res is NotImplemented else not res

    def append(self, val):
        self.data += val

    def insert(self, index, val):
        b4, subj, aft = self._parts_(index)
        self.data = b4 + val + subj + aft

    def pop(self, index=-1):
        b4, subj, aft = self._parts_(index)
        self.data = b4 + aft
        return MutableString(subj)

    def __iadd__(self, other):
        if isinstance(other, MutableString):
            self.data += other.data
        elif isinstance(other, str):
            self.data += other
        else:
            return NotImplemented
        return self

    def __imul__(self, other):
        if isinstance(other, int):
            self.data *= other
        else:
            return NotImplemented
        return self
