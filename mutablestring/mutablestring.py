from collections import UserString


class MutableString(UserString):
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

    def append(self, val):
        self.data += val

    def insert(self, index, val):
        b4, subj, aft = self._parts_(index)
        self.data = b4 + val + subj + aft

    def pop(self, index=-1):
        b4, subj, aft = self._parts_(index)
        self.data = b4 + aft
        return MutableString(subj)
